from filet.config.cache_db import SQL, Stage
from filet.config.trino_client import TrinoDwhConfig
from filet.core.json.txt import generate_txt_selection_from_schema

schema = {
    "type": "record",
    "fields": [
        {"name": "status", "type": "string"},
        {
            "name": "data",
            "type": {
                "type": "record",
                "fields": [
                    {"name": "resultType", "type": "string"},
                    {
                        "name": "result",
                        "type": {
                            "type": "array",
                            "items": [
                                {
                                    "type": "record",
                                    "fields": [
                                        {
                                            "name": "metric",
                                            "type": {
                                                "type": "record",
                                                "fields": [
                                                    {"name": "__name__", "type": "string"},
                                                    {"name": "alias", "type": "string"},
                                                    {"name": "cluster", "type": "string"},
                                                    {"name": "datacenter", "type": "string"},
                                                    {"name": "instance", "type": "string"},
                                                    {"name": "job", "type": ["null", "string"], "default": None},
                                                    {"name": "recordings", "type": ["null", "string"], "default": None},
                                                ],
                                                "name": "root_data_result__metric",
                                            },
                                        },
                                        {
                                            "name": "values",
                                            "type": {
                                                "items": {"items": ["int", "string"], "type": "array"},
                                                "type": "array",
                                            },
                                        },
                                    ],
                                    "name": "root_data_result_",
                                }
                            ],
                        },
                    },
                ],
                "name": "root_data",
            },
        },
    ],
    "name": "root",
}


def test_generate_table_select_sql():
    create_table = """-- Staging Table SQL
CREATE TABLE hive.test_schema.hive.ionosdataspace_techops_ionos.node_cpu_seconds_total(
  raw_data VARCHAR
) WITH (
 format = 'TEXTFILE',
 external_location = 'external_location'
)"""

    select = """-- Trino SQL to select / parse an TXT File (with Json) as a Table
CREATE VIEW iceberg.bronze.test_schema_hive.ionosdataspace_techops_ionos.node_cpu_seconds_total_view
COMMENT  'Trino SQL to select / parse an TXT File (with Json) as a Table.'
AS
SELECT json_extract_scalar(t0."raw_data", '$.status') as "status",
json_extract_scalar(t0."raw_data", '$.data.resultType') as "data.resultType",
json_extract_scalar(t1."result", '$.metric.__name__') as "metric.__name__",
json_extract_scalar(t1."result", '$.metric.alias') as "metric.alias",
json_extract_scalar(t1."result", '$.metric.cluster') as "metric.cluster",
json_extract_scalar(t1."result", '$.metric.datacenter') as "metric.datacenter",
json_extract_scalar(t1."result", '$.metric.instance') as "metric.instance",
t2.values_idx,
CAST(json_extract(t2."values", '$[0]') AS BIGINT) AS "values_0",
CAST(json_extract(t2."values", '$[1]') AS VARCHAR) AS "values_1",
"$path" as path,
"$file_modified_time" as file_modified_time,
"$file_size" as file_size
FROM hive.test_schema.hive.ionosdataspace_techops_ionos.node_cpu_seconds_total t0
CROSS JOIN UNNEST(CAST(json_extract(t0."raw_data", '$.data.result') AS ARRAY<json>))  AS t1("result")
CROSS JOIN UNNEST(CAST(json_extract(t1."result", '$.values') AS ARRAY<json>)) WITH ORDINALITY AS t2("values", "values_idx")"""
    generated = generate_txt_selection_from_schema(
        schema,
        "hive.ionosdataspace_techops_ionos.node_cpu_seconds_total",
        "test_schema",
        "external_location",
        TrinoDwhConfig(),
        "raw_data",
    )
    insert = """-- Insert into Target Table SQL (silver)
INSERT INTO iceberg.silver.test_schema_hive.ionosdataspace_techops_ionos.node_cpu_seconds_total
SELECT src."status",
src."data.resultType",
src."metric.__name__",
src."metric.alias",
src."metric.cluster",
src."metric.datacenter",
src."metric.instance",
src."values_0",
src."values_1",
src."path",
src."file_modified_time",
src."file_size"
FROM iceberg.bronze.test_schema_hive.ionosdataspace_techops_ionos.node_cpu_seconds_total_view AS src
WHERE path = ?
AND NOT EXISTS (
    SELECT 1
    FROM  iceberg.silver.test_schema_hive.ionosdataspace_techops_ionos.node_cpu_seconds_total AS tgt
    WHERE tgt.path = src.path
)"""
    static = Stage(
        table_name="hive.ionosdataspace_techops_ionos.node_cpu_seconds_total",
        db_schema="test_schema",
        external_location="external_location",
        schema=schema,
        sql=SQL(create_table=create_table, select=select, insert=insert),
        s3_source=None,
    )
    assert static.sql.create_table == generated.sql.create_table
    assert static.sql.select == generated.sql.select
    assert static.sql.insert == generated.sql.insert
    assert static.table_name == generated.table_name
    assert static.db_schema == generated.db_schema
    assert static.external_location == generated.external_location
