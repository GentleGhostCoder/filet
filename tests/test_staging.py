"""Test the trino staging for test data."""

import logging
import os
import subprocess
import time
import zlib

import boto3
from botocore.exceptions import EndpointConnectionError
from pydantic_settings import SettingsConfigDict
import pytest
from sqlalchemy import create_engine
from trino.exceptions import TrinoQueryError

from tests.generate_data import (
    generate_complex_csv_data,
    generate_complex_json_data,
    generate_simple_csv_data,
    generate_simple_json_data,
)
from filet.boto3.fetch_s3_sources import fetch_s3_sources
from filet.boto3.schema import Format, ListBucketsResult
from filet.boto3.types import S3Client
from filet.config.boto3_client import Boto3ClientConfig
from filet.config.cache_db import store
from filet.config.objects_pattern import ObjectsPattern
from filet.config.trino_client import TrinoDwhConfig
from filet.config.utils.default_config import default_config
from filet.core.csv.raw_csv import stage_csv
from filet.core.json.txt import stage_json
from filet.patches.pydantic import BaseSettings

logger = logging.getLogger(__name__)


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.getenv("INTEGRATION_TEST_CONFIG", default_config(store.default_config)),
        env_prefix="test_",
        extra="ignore",
        profile=os.getenv("INTEGRATION_TEST_PROFILE", "default"),  # type: ignore
    )
    staging_bucket: str = "trino-staging"
    # csv_stage_bucket: str = "trino-staging"
    # json_stage_bucket: str = "trino-staging"
    # csv_stage_prefix: str = ""
    # json_stage_prefix: str = ""


def upload_data_to_s3(
    s3_client: S3Client, trino_dwh_config: TrinoDwhConfig, test_config: Config, data: bytes, key: str
):
    compress_obj = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, zlib.MAX_WBITS | 16)
    buckets = s3_client.list_buckets()["Buckets"]
    if not any(bucket["Name"] == test_config.staging_bucket for bucket in buckets):
        s3_client.create_bucket(Bucket=test_config.staging_bucket)
    s3_client.put_object(
        Bucket=test_config.staging_bucket,
        Key=key,
        Body=compress_obj.compress(data) + compress_obj.flush(),
    )


def generate_and_upload_data_to_s3(s3_client: S3Client, trino_dwh_config: TrinoDwhConfig, test_config: Config):
    # Set the AWS credentials

    # Call the functions to generate data
    simple_data = generate_simple_json_data()
    complex_data = generate_complex_json_data()

    upload_data_to_s3(
        s3_client,
        trino_dwh_config,
        test_config,
        simple_data.encode("utf-8"),
        f"simple_json_data/simple_data.json.gz",
    )
    upload_data_to_s3(
        s3_client,
        trino_dwh_config,
        test_config,
        complex_data.encode("utf-8"),
        f"complex_json_data/complex_data.json.gz",
    )

    # Call the functions to generate data
    simple_data = generate_simple_csv_data()
    complex_data = generate_complex_csv_data()

    upload_data_to_s3(
        s3_client,
        trino_dwh_config,
        test_config,
        simple_data.to_csv(index=False).encode("utf-8"),
        f"simple_csv_data/simple_data.csv.gz",
    )
    upload_data_to_s3(
        s3_client,
        trino_dwh_config,
        test_config,
        complex_data.to_csv(index=False).encode("utf-8"),
        f"complex_csv_data/complex_data.csv.gz",
    )


def stage_data(stage_format: Format, stage_method):
    """Test the trino staging for test data."""
    profile = os.getenv("INTEGRATION_TEST_PROFILE", "default")
    test_config = Config(profile=profile)
    s3_config = Boto3ClientConfig(profile=profile)
    trino_dwh_config = TrinoDwhConfig(profile=profile)
    logger.info("Test Config: %s", test_config)
    logger.info("S3 Config: %s", s3_config)
    logger.info("Trino Config: %s", trino_dwh_config)

    s3_client: S3Client = boto3.client(**s3_config.model_dump())

    logger.info("S3 Client: %s", s3_client)
    try:
        # run docker compose up  inside docker folder if the localhost:9000 is not running
        # s3_client.head_bucket(Bucket=test_config.staging_bucket)
        buckets = s3_client.list_buckets()
        logger.info("S3 Buckets: %s", list(bucket["Name"] for bucket in buckets["Buckets"]))
        logger.info("Stage Bucket: %s", test_config.staging_bucket)
        logger.info(
            "S3 Buckets: %s", any(bucket["Name"] == test_config.staging_bucket for bucket in buckets["Buckets"])
        )
        if not any(bucket["Name"] == test_config.staging_bucket for bucket in buckets["Buckets"]):
            raise ValueError(f"TEST Bucket {test_config.staging_bucket} not found")
    except EndpointConnectionError:
        process = subprocess.Popen(["docker", "compose", "up", "-d"], cwd="docker")
        process.wait()

    logger.info("Start generate and upload data to S3.")
    generate_and_upload_data_to_s3(s3_client, trino_dwh_config, test_config)
    objects_pattern = ObjectsPattern()

    logging.info("Fetching S3 sources")
    objects_extended = fetch_s3_sources(s3_client, test_config.staging_bucket, 30, objects_pattern)

    s3_sources = list(obj for obj in objects_extended if obj.ObjectFormat == stage_format)
    for s3_source in s3_sources:
        logging.info(s3_source)
        try:
            create_engine(**trino_dwh_config.client_config.model_dump()).connect()
        except TrinoQueryError as e:
            # Trino server is still initializing
            if "Server is still initializing" in str(e.message):
                time.sleep(5)
        logger.info("Staging %s", s3_source.Key)
        stage_method(s3_client, s3_source, trino_dwh_config)
    return True


# @pytest.mark.skipif(os.environ.get("NOX_RUNNING", "False"))
# def test_stage_csv_data():
#     """Test the trino staging for test data."""
#     assert stage_data(Format.csv, stage_csv)
#
#
# @pytest.mark.skipif(os.environ.get("NOX_RUNNING", "False"))
# def test_stage_json_data():
#     """Test the trino staging for test data."""
#     assert stage_data(Format.json, stage_json)
