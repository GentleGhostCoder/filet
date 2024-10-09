import logging

from filet.boto3.chunk_download import ChunkDownload
from filet.boto3.schema import S3Source
from filet.boto3.types import S3Client
from filet.config.trino_client import TrinoDwhConfig
from filet.core.stage_table import stage_flat_table
from filet.cpputils import eval_flat_json

logger = logging.getLogger(__name__)


def stage_flat_json(s3_client: S3Client, s3_source: S3Source, trino_dwh_config: TrinoDwhConfig):
    """Stage CSV files from S3 to local."""
    logger.debug("Trino DWH Config: %s", trino_dwh_config)

    # first element
    chunk_download = ChunkDownload(s3_client, s3_source)
    # chunk_download.estimated_parts = 1
    # chunk_download.chunk_size = chunk_download.estimated_size
    total_body = chunk_download.get_part()

    # fix_handler = JsonFixHandler()
    # total_body = eval_flat_json(total_body)
    # logger.debug("Total Body: %s", total_body)
    # evaluate csv file header
    json_flat_schema = eval_flat_json(total_body)

    s3_source.Bucket = trino_dwh_config.external_location
    s3_source.Prefix = f"{trino_dwh_config.bronze_schema_name}/{s3_source.Prefix}"

    return stage_flat_table(json_flat_schema, s3_source, trino_dwh_config)


def ingest_flat_json():
    """Ingest flat json data to trino as parquet."""
    ...
