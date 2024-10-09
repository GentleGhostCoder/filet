import asyncio
import logging
from typing import Optional

from filet.boto3.async_handler import AsyncHandler
from filet.boto3.schema import ListObjectsV2CommonPrefix, ListObjectsV2Content, ListObjectsV2Result
from filet.boto3.utils import extract_file_meta
from filet.config.objects_pattern import ObjectsPattern

logger = logging.getLogger(__name__)


def fetch_s3_sources(
    s3_client,
    bucket_name,
    max_keys_per_prefix: int = 20,
    objects_pattern: Optional[ObjectsPattern] = None,
    async_handler: Optional[AsyncHandler] = None,
    prefix: str = "",
):
    if not async_handler:
        async_handler = AsyncHandler()

    objects = ListObjectsV2Result(
        **s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter="/", MaxKeys=max_keys_per_prefix)
    )

    async def _fetch_prefix(prefix: ListObjectsV2CommonPrefix):
        """Asynchronously fetch objects for a given prefix."""
        logger.debug("Fetching objects for prefix %s", prefix.Prefix)
        async with async_handler.semaphore:
            _objects = s3_client.list_objects_v2(
                Bucket=bucket_name, Prefix=prefix.Prefix, Delimiter="/", MaxKeys=max_keys_per_prefix
            )
            if "Contents" in _objects:
                objects.Contents.extend(ListObjectsV2Content(**obj) for obj in _objects["Contents"])
            if "CommonPrefixes" in _objects:
                prefixes = [ListObjectsV2CommonPrefix(**prefix) for prefix in _objects["CommonPrefixes"]]
                objects.CommonPrefixes.extend(prefixes)
                await asyncio.gather(*(_fetch_prefix(prefix) for prefix in prefixes))

    async_handler.event_loop.run_until_complete(
        asyncio.gather(*(_fetch_prefix(prefix) for prefix in objects.CommonPrefixes))
    )

    return extract_file_meta(objects, objects_pattern or ObjectsPattern())
