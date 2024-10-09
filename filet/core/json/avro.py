import json
import logging

import avro
import boto3

from filet.boto3.chunk_download import ChunkDownload
from filet.boto3.schema import S3Source
from filet.boto3.types import S3Client
from filet.config.trino_client import TrinoDwhConfig
from filet.core.json.avro_schema_handler import eval_json

logger = logging.getLogger(__name__)

AVRO_TRINO_TYPE_MAP = {
    "string": "VARCHAR",
    "int": "INTEGER",
    "long": "BIGINT",
    "float": "REAL",
    "double": "DOUBLE",
    "boolean": "BOOLEAN",
}


def quote_field_name(field_name):
    return f'"{field_name}"'


def map_avro_type_to_trino(avro_type):
    """Map an Avro type to a Trino type, handling complex and union types, including nullable fields."""
    if isinstance(avro_type, dict):
        type_name = avro_type.get("type")
        if type_name in AVRO_TRINO_TYPE_MAP:
            return AVRO_TRINO_TYPE_MAP[type_name]
        elif type_name == "array":
            items_type = avro_type["items"]
            if isinstance(items_type, list):  # Handle union types for array items
                items_type = [t for t in items_type if t != "null"][0]  # Pick the first non-null type
            mapped_type = map_avro_type_to_trino(items_type)
            return f"ARRAY<{mapped_type}>" if mapped_type else None
        elif type_name == "record":
            field_definitions = [
                f"{quote_field_name(field['name'])} {map_avro_type_to_trino(field['type'])}"
                for field in avro_type["fields"]
                if map_avro_type_to_trino(field["type"]) is not None
            ]
            return f"ROW({', '.join(field_definitions)})" if field_definitions else None
        else:
            raise ValueError(f"Unsupported Avro type: {type_name}")
    elif isinstance(avro_type, list):  # Handling union types
        non_null_types = [t for t in avro_type if t != "null"]
        if not non_null_types:
            raise ValueError("Invalid Avro union type: all types are null")
        mapped_type = map_avro_type_to_trino(non_null_types[0])
        return mapped_type if mapped_type else None
    elif avro_type == "null":
        return None  # Handle 'null' by returning None
    elif avro_type in AVRO_TRINO_TYPE_MAP:
        return AVRO_TRINO_TYPE_MAP[avro_type]
    else:
        raise ValueError(f"Invalid Avro type definition: {avro_type}")


def avro_table_create_sql(avro_schema, table_name, **extra_properties):
    """Generate a Trino CREATE TABLE statement from an Avro schema."""
    if isinstance(avro_schema, str):
        parsed_schema = json.loads(avro_schema)
    else:
        parsed_schema = avro_schema

    field_definitions = []
    for field in parsed_schema["fields"]:
        trino_type = map_avro_type_to_trino(field["type"])
        if trino_type is not None:  # Only include fields with a valid Trino type
            field_definitions.append(f"{field['name']} {trino_type}")

    fields_statement = ", ".join(field_definitions)

    # extra_properties["format"] = "AVRO"
    extra_properties_string = ",\n".join([f"{key} = '{value}'" for key, value in extra_properties.items()])

    create_table_statement = (
        f"CREATE TABLE IF NOT EXISTS {table_name}\n({fields_statement})\nWITH\n({extra_properties_string})"
    )
    return create_table_statement


def stage_avro_json(s3_client: S3Client, s3_source: S3Source, trino_dwh_config: TrinoDwhConfig):
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
    table_path = f"{trino_dwh_config.hive_catalog}.{schema}.{table_name}"

    avro_schema_file_name = f"{schema}/{s3_source.Prefix}/schema/{table_name}.avsc"
    target_s3_client: S3Client = boto3.client(**trino_dwh_config.boto3_client.model_dump())
    target_s3_client.put_object(
        Bucket=trino_dwh_config.external_location,
        Key=avro_schema_file_name,
        Body=json.dumps(avro_schema.to_json()),
    )
    external_location = f"s3a://{trino_dwh_config.external_location}/{schema}/{s3_source.Prefix}/data/"
    avro_schema_url = f"s3a://{trino_dwh_config.external_location}/{avro_schema_file_name}"

    # drop_table_sql = f"DROP TABLE IF EXISTS {table_path}"
    # create_table_sql = f"""
    # CREATE TABLE IF NOT EXISTS {table_path} (
    #    dummy VARCHAR
    # )
    # WITH (
    #     external_location = '{external_location}',
    #     format = 'AVRO',
    #     avro_schema_url = '{avro_schema_url}'
    # )
    # """

    create_table_sql = avro_table_create_sql(
        json.dumps(json_schema),
        table_path,
        external_location=external_location,
        format="JSON",
        avro_schema_url=avro_schema_url,
    )

    return create_table_sql
