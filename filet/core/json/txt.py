from io import BytesIO
import json
import logging
from typing import Union

import avro
import avro.datafile
import avro.schema
import boto3
import orjson

from filet.boto3.chunk_download import ChunkDownload
from filet.boto3.schema import S3Source
from filet.boto3.types import S3Client
from filet.config.cache_db import SQL, Stage, store
from filet.config.trino_client import TrinoDwhConfig
from filet.core.create_schema import create_schema
from filet.core.json.avro_schema_handler import eval_json
from filet.core.json.utils import get_type
from filet.core.type_mapping import JsonType, TrinoAvroTypeMapping

logger = logging.getLogger(__name__)


def generate_txt_selection_from_schema(  # noqa: C901
    json_schema, table_name, table_schema, external_location, trino_dwh_config, json_column="raw_data"
):  # noqa: C901
    """
    Generate a Trino SQL query to select from a table with a given schema and JSON paths.

    Args:
    - table_name: str, the name of the table to select from
    - json_paths: list of str, the JSON paths to select

    Returns:
    - str, the Trino SQL query
    """
    selections: list = []
    column_names: list = []
    column_types: list = []
    joins: list = []

    def _add_cross_join(prefix, key, json_table, with_index=False):
        nonlocal joins
        current_key = f"{prefix}.{key}" if prefix else key
        new_table_prefix = f"t{len(joins) + 1}"
        table_values = f'"{key}"' + (f', "{key}_idx"' if with_index else "")
        join = (
            "CROSS JOIN UNNEST(CAST(json_extract("
            f"{json_table}, '$.{current_key}') AS ARRAY<json>)) "
            f"{'WITH ORDINALITY' if with_index else ''} "
            f"AS {new_table_prefix}({table_values})"
        )
        joins.append(join)
        if with_index:
            # add <key>_idx to selections
            selections.append(f"{new_table_prefix}.{key}_idx")
        return f'{new_table_prefix}."{key}"'

    def _add_basic_selection(prefix, key, json_table, json_type):
        nonlocal selections
        current_key = f"{prefix}.{key}" if prefix else key
        selection = f"json_extract_scalar({json_table}, '$.{current_key}') as \"{current_key}\""
        column_names.append(f'"{current_key}"')
        column_types.append(TrinoAvroTypeMapping(json_type.value).name)
        selections.append(selection)

    def _add_cast_selection(index, key, json_table, json_type):
        nonlocal selections
        mapped_type = TrinoAvroTypeMapping(json_type.value).name
        current_key = f"{key}_{index}"
        selection = f"CAST(json_extract({json_table}, '$[{index}]') AS {mapped_type}) AS \"{current_key}\""
        column_names.append(f'"{current_key}"')
        column_types.append(mapped_type)
        selections.append(selection)

    def _analyze_items(
        items: Union[dict, list, str],
        json_table: str = "",
        key: str = "",
        prefix: str = "",
        index: int = -1,
        json_type=JsonType.string,
    ):

        if len(items) == 1 and isinstance(items[0], dict):
            key, json_type = get_type(items[0])

            if json_type == JsonType.array:
                _analyze_items(items[0]["items"], json_table, key, prefix, index, json_type)
                key = ""
                return

            if json_type == JsonType.record:
                _analyze_items(items[0]["fields"], json_table, key, prefix, index, json_type)
                key = ""
                return

        for item in items:
            if isinstance(item, str):
                if index == -1:
                    _add_basic_selection(prefix, key, json_table, json_type)
                    continue
                _add_cast_selection(index, key, json_table, JsonType(item))
                index += 1
                continue
            if "type" not in item:
                continue

            if isinstance(item["type"], list):
                _analyze_items([item["type"]], json_table, key, prefix, index)
                continue

            key, json_type = get_type(item)

            if json_type.value in TrinoAvroTypeMapping:
                if index == -1:
                    _add_basic_selection(prefix, key, json_table, json_type)
                    continue
                _add_cast_selection(index, key, json_table, json_type)
                index += 1
                continue

            if json_type == JsonType.record:
                prefix = f"{prefix}.{key}" if prefix else key
                fields = item["type"]["fields"] if isinstance(item["type"], dict) else item["fields"]
                _analyze_items(fields, json_table, key, prefix, index, json_type)
                key = ""
                continue

            if json_type == JsonType.array:
                items = item["type"]["items"] if isinstance(item["type"], dict) else item["items"]
                if isinstance(items, list) and len(items) == 1 and isinstance(items[0], dict) and "items" in items[0]:
                    items = items[0]
                if isinstance(items, dict) and "items" in items:
                    index = 0
                    # nested array -> union
                    json_table = _add_cross_join("", key, json_table, with_index=True)
                    _analyze_items(items["items"], json_table, key, "", index, json_type)
                    key = ""
                    continue
                json_table = _add_cross_join(prefix, key, json_table)
                _analyze_items(items, json_table, key, "", index, json_type)
                key = ""

    if "fields" in json_schema:
        _analyze_items(json_schema["fields"], f't0."{json_column}"')
    elif "items" in json_schema:
        _analyze_items(json_schema["items"], f't0."{json_column}"')

    selections.extend(['"$path" as path', '"$file_modified_time" as file_modified_time', '"$file_size" as file_size'])
    column_names.extend(['"path"', '"file_modified_time"', '"file_size"'])
    column_types.extend(["VARCHAR", "TIMESTAMP(6)", "BIGINT"])

    stage = Stage(
        table_name=table_name,
        db_schema=table_schema,
        external_location=external_location,
        schema=json_schema,
    )

    create_table_sql = f"""-- Staging Table SQL
CREATE TABLE {trino_dwh_config.hive_catalog}.{table_schema}.{table_name}(
  {json_column} VARCHAR
) WITH (
 format = 'TEXTFILE',
 external_location = '{external_location}'
)"""

    create_stage_view_sql = f"""-- Trino SQL to select / parse an TXT File (with Json) as a Table
CREATE VIEW {trino_dwh_config.iceberg_catalog}.{trino_dwh_config.bronze_schema_name}.{table_schema}_{table_name}_view
COMMENT  'Trino SQL to select / parse an TXT File (with Json) as a Table.'
AS
SELECT {''',
'''.join(selections)}
FROM {trino_dwh_config.hive_catalog}.{table_schema}.{table_name} t0
{'''
'''.join(joins)}"""
    # PREPARE "select_{table_name.replace(".", "_")}" FROM
    create_target_table_sql = rf"""-- Target Table SQL (silver)
CREATE TABLE {trino_dwh_config.iceberg_catalog}.{trino_dwh_config.silver_schema_name}.{table_schema}_{table_name}(
    {''',
'''.join([f"{column_names[i]} {column_types[i]}" for i in range(len(column_names))])}
) WITH (
    format = 'PARQUET',
    partitioning = ARRAY\['month(file_modified_time)', 'path']
)"""  # noqa: W605  invalid escape sequence '\['

    # PREPARE "insert_{table_schema}_{table_name}" FROM
    insert_into_target_table_sql = f"""-- Insert into Target Table SQL (silver)
INSERT INTO {trino_dwh_config.iceberg_catalog}.{trino_dwh_config.silver_schema_name}.{table_schema}_{table_name}
SELECT {''',
'''.join([f"src.{col}" for col in column_names])}
FROM {trino_dwh_config.iceberg_catalog}.{trino_dwh_config.bronze_schema_name}.{table_schema}_{table_name}_view AS src
WHERE path = ?
AND NOT EXISTS (
    SELECT 1
    FROM  {trino_dwh_config.iceberg_catalog}.{trino_dwh_config.silver_schema_name}.{table_schema}_{table_name} AS tgt
    WHERE tgt.path = src.path
)"""

    stage.sql = SQL(
        create_table=create_table_sql,
        create_target_table=create_target_table_sql,
        drop_table=f"DROP TABLE {trino_dwh_config.hive_catalog}.{table_schema}.{table_name}",
        select=create_stage_view_sql,
        insert=insert_into_target_table_sql,
    )

    return stage


def stage_json(s3_client: S3Client, s3_source: S3Source, trino_dwh_config: TrinoDwhConfig):
    """Stage CSV files from S3 to local."""
    logger.debug("Trino DWH Config: %s", trino_dwh_config)
    schema = s3_source.Bucket.replace("-", "_").lower()
    # first element
    chunk_download = ChunkDownload(s3_client, s3_source)
    # chunk_download.estimated_parts = 1
    # chunk_download.chunk_size = chunk_download.estimated_size
    first_part = chunk_download.get_part()

    # evaluate csv file header
    json_schema = eval_json(first_part)
    logger.debug("JSON Schema: %s", json_schema)
    json_schema["namespace"] = "com.trino.staging"
    avro_schema = avro.schema.parse(json.dumps(json_schema))  # validate

    # engine = create_engine(**trino_dwh_config.client_config.model_dump())
    # connection = engine.connect()

    table_name = s3_source.Prefix.split("/")[-1].lower().replace("-", "_")

    avro_schema_file_name = f"{schema}/{s3_source.Prefix}/schema/{table_name}.avsc"
    target_s3_client: S3Client = boto3.client(**trino_dwh_config.boto3_client.model_dump())
    target_s3_client.put_object(
        Bucket=trino_dwh_config.external_location,
        Key=avro_schema_file_name,
        Body=json.dumps(avro_schema.to_json()),
    )

    external_location = f"s3a://{s3_source.Bucket}/{s3_source.Prefix}"
    # target_external_location = f"s3a://{trino_dwh_config.external_location}/{schema}/{s3_source.Prefix}/data/"

    stage = generate_txt_selection_from_schema(json_schema, table_name, schema, external_location, trino_dwh_config)
    stage.s3_source = s3_source
    store.stages[table_name] = stage
    store.save()


def ingest_json(s3_client: S3Client, s3_source: S3Source, trino_dwh_config: TrinoDwhConfig):
    schema = s3_source.Bucket.replace("-", "_").lower()
    logger.debug("Trino DWH Config: %s", trino_dwh_config)
    create_schema(trino_dwh_config, schema)
    table_name = s3_source.Prefix.split("/")[-1].lower().replace("-", "_")
    existing_avro_schema_file_name = f"{schema}/{s3_source.Prefix}/schema/{table_name}.avsc"

    schema_file_exists = (
        s3_client.list_objects_v2(
            Bucket=trino_dwh_config.external_location,
            Prefix=existing_avro_schema_file_name,
        ).get("KeyCount", 0)
        > 0
    )

    previous_schema = {}
    if schema_file_exists:
        existing_schema = s3_client.get_object(
            Bucket=trino_dwh_config.external_location,
            Key=existing_avro_schema_file_name,
        )
        existing_schema_bytes = existing_schema["Body"].read()
        previous_schema = orjson.loads(existing_schema_bytes)

    download = ChunkDownload(s3_client, s3_source)
    download.estimated_parts = 1
    download.chunk_size = download.estimated_size
    source_bytes = download.get_part()
    source_json = orjson.loads(source_bytes)  # TODO (sgeist): Error-Handling for invalid JSON
    # new_schema = eval_json(source_bytes)
    # new_schema["namespace"] = "com.trino.staging"
    # handler = PyAvroSchemaHandler()
    # handler.read_existing_schema(previous_schema.copy())
    # updated_schema = handler.update_schema(new_schema)
    # check compatibility

    # updated_avro_schema = avro.schema.parse(json.dumps(new_schema))
    # previous_avro_schema = avro.schema.parse(json.dumps(previous_schema))
    # compatibility = ReaderWriterCompatibilityChecker().get_compatibility(reader=previous_avro_schema,
    #                                                                      writer=updated_avro_schema)
    # if compatibility.compatibility != SchemaCompatibilityType.compatible:
    # write updated schema to current schema and move the old schema to a backup location
    #     s3_client.put_object(
    #         Bucket=trino_dwh_config.external_location,
    #         Key=existing_avro_schema_file_name,
    #         Body=json.dumps(new_schema),
    #     )
    #     current_date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    #     s3_client.put_object(
    #         Bucket=trino_dwh_config.external_location,
    #         Key=f"{existing_avro_schema_file_name.replace('.avsc', '')}_{current_date_str}.avsc",
    #         Body=json.dumps(previous_avro_schema.to_json()),
    #     )
    # if source_bytes.startswith(b"["):
    #     source_json = {"root": source_json}
    # logger.debug("JSON Schema: %s", updated_schema)

    avro_schema = avro.schema.parse(json.dumps(previous_schema))

    avro_bytes_buf = BytesIO()
    writer = avro.datafile.DataFileWriter(avro_bytes_buf, avro.io.DatumWriter(), avro_schema)
    writer.append(source_json)
    writer.flush()
    avro_bytes_buf.seek(0)
    avro_bytes = avro_bytes_buf.read()

    avro_data_key = f"{schema}/{s3_source.Prefix}/data/{s3_source.ObjectBaseName.split('/')[-1]}.avro"

    target_s3_client: S3Client = boto3.client(**trino_dwh_config.boto3_client.model_dump())
    target_s3_client.put_object(
        Bucket=trino_dwh_config.external_location,
        Key=avro_data_key,
        Body=avro_bytes,
    )
