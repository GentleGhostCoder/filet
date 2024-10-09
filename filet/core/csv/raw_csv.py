import logging

from filet.boto3.chunk_download import ChunkDownload
from filet.boto3.schema import S3Source
from filet.boto3.types import S3Client
from filet.config.trino_client import TrinoDwhConfig
from filet.core.stage_table import stage_flat_table
from filet.cpputils import eval_csv

logger = logging.getLogger(__name__)


def stage_csv(s3_client: S3Client, s3_source: S3Source, trino_dwh_config: TrinoDwhConfig):
    """Stage CSV files from S3 to local."""
    logger.debug("Trino DWH Config: %s", trino_dwh_config)

    # first element
    chunk_download = ChunkDownload(s3_client, s3_source)
    first_part = chunk_download.get_part()

    # evaluate csv file header
    csv_schema = eval_csv(first_part)

    return stage_flat_table(csv_schema, s3_source, trino_dwh_config)


def setup_csv_integration():
    pass
