import logging

from sqlalchemy import create_engine, text

from filet.config.trino_client import TrinoDwhConfig

logger = logging.getLogger(__name__)


def create_schema(trino_dwh_config: TrinoDwhConfig, *schema_names: str):
    engine = create_engine(**trino_dwh_config.client_config.model_dump())
    connection = engine.connect()
    catalogs = [catalog[0] for catalog in connection.execute(text("SHOW CATALOGS")).fetchall()]

    # TODO: check this in another method / location
    if trino_dwh_config.hive_catalog not in catalogs:
        raise ValueError(f"Catalog {trino_dwh_config.hive_catalog} not found! Available catalogs: {catalogs}")
    if trino_dwh_config.iceberg_catalog not in catalogs:
        raise ValueError(f"Catalog {trino_dwh_config.iceberg_catalog} not found! Available catalogs: {catalogs}")

    create_schema_sqls = [
        *[
            (
                f'CREATE SCHEMA IF NOT EXISTS "{trino_dwh_config.hive_catalog}"."{schema_name.lower().replace("-", "_")}"'
                f" WITH (location = 's3a://{schema_name}/')"
            )
            for schema_name in schema_names
        ],
        *[
            (
                f'CREATE SCHEMA IF NOT EXISTS "{trino_dwh_config.iceberg_catalog}"."{schema_name}"'
                f" WITH (location = 's3a://{trino_dwh_config.external_location.rstrip('/')}/{schema_name}')"
            )
            for schema_name in [
                trino_dwh_config.bronze_schema_name,
                trino_dwh_config.silver_schema_name,
                trino_dwh_config.gold_schema_name,
            ]
        ],
    ]
    logger.debug("Creating Schemas:\n%s", create_schema_sqls)
    for create_schema_sql in create_schema_sqls:
        connection.execute(text(create_schema_sql))
    connection.close()
