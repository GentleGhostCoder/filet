import logging

from filet.core.type_mapping import TrinoPythonTypesMapping

logger = logging.getLogger(__name__)


def stage_flat_table(table_schema, s3_source, trino_dwh_config):
    logger.debug("CSV Schema: %s", table_schema)
    if table_schema.header:
        # HEADER: csv_schema["header"]
        # normalize header names and replace special characters
        special_chars = [" ", "-", "(", ")", "/", "\\", ".", ",", ":", ";", "'", '"']
        normalized_header = [header.lower() for header in table_schema.header]
        for char in special_chars:
            normalized_header = [header.replace(char, "_") for header in normalized_header]

        # replace __ with _ or ending _
        normalized_header = [header.replace("__", "_") for header in normalized_header]
        normalized_header = [header[:-1] if header.endswith("_") else header for header in normalized_header]
    else:
        # NO HEADER: csv_schema["columns"]
        # generate normalized header names
        normalized_header = [f"column_{i}" for i in range(table_schema.column_count)]

    # create a trino create table statement with external location of the s3 prefix, csv format, delimiter, and header
    # table name
    table_name = s3_source.Prefix.split("/")[-1].lower().replace("-", "_")
    schema = s3_source.Bucket.lower().replace("-", "_")
    quoting = f"csv_quote = '{table_schema.quoting_character}'," if table_schema.quoting_character else ""
    # create table statement
    create_table_statement = f"""
CREATE TABLE IF NOT EXISTS {trino_dwh_config.hive_catalog}.{schema}.{table_name} (
{''',
'''.join([f'{header} varchar' for header in normalized_header])}
) WITH (
    external_location = 's3a://{s3_source.Bucket}/{s3_source.Prefix}',
    format = 'CSV',
    {quoting}
    csv_separator =  '{table_schema.column_separator}',
    skip_header_line_count = {int(table_schema.has_header)}
)
"""
    # logger.debug("Create Table Statement: %s", create_table_statement)
    # engine = create_engine(**trino_dwh_config.client_config.model_dump())
    # connection = engine.connect()
    # connection.execute(text(create_table_statement))

    #     # View with csv types and header (weak typed)
    #     # create view statement
    if table_schema.parsed_line_count < 2:
        # TODO: Think about this
        raise ValueError(f"CSV file has less than 2 lines! Parsed schema: {table_schema}")

    # column_types
    if not table_schema.column_types:
        raise ValueError(f"CSV file has no schema types! Parsed schema: {table_schema}")

    types = [TrinoPythonTypesMapping(t) for t in table_schema.column_types]

    # column_types
    create_view_statement = f'''
CREATE OR REPLACE VIEW  "{trino_dwh_config.iceberg_catalog}"."{trino_dwh_config.bronze_schema_name}"."{table_name}_view" AS
SELECT
{""",
""".join([f'CAST({header} AS {types[i].name}) AS {header}' for i, header in enumerate(normalized_header)])}
FROM "{trino_dwh_config.hive_catalog}"."{schema}"."{table_name}"
'''
    logger.debug("Create View Statement: %s", create_view_statement)
    # connection.execute(text(create_view_statement))
    # connection.close()

    return (create_table_statement, create_view_statement)
