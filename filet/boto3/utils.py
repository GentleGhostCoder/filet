from datetime import datetime
from itertools import chain
import logging
from pathlib import Path
import re
from typing import List
from urllib.parse import urlparse

from filet.boto3.schema import (
    Compression,
    Encryption,
    Format,
    ListObjectsV2Content,
    ListObjectsV2Result,
    S3Source,
)
from filet.config.objects_pattern import ObjectsPattern

logger = logging.getLogger(__name__)


def validate_date(date_text, date_format):
    """Extract date from String according to given format."""
    try:
        return datetime.strptime(date_text, date_format)
    except ValueError:
        return


def extract_file_meta(  # noqa: C901 TODO: reduce complexity
    objects: ListObjectsV2Result, objects_pattern: ObjectsPattern
) -> List[S3Source]:
    """Extract the file date from the key."""
    logger.debug("Extracting file meta for %s, %s (objects)", objects.Name, len(objects.Contents))

    def extract_date(obj: ListObjectsV2Content) -> S3Source:
        if not obj.Key or str(obj.Key) == "nan":
            return S3Source(Bucket=objects.Name, **obj.model_dump())
        date_strs = list(
            chain(
                *[
                    match
                    for match in [re.findall(pattern, str(obj.Key)) for pattern in objects_pattern.date_regex_patterns]
                    if match
                ]
            )
        )
        if not date_strs:
            extended_obj = S3Source(Bucket=objects.Name, **obj.model_dump())
            extended_obj.KeyPattern = obj.Key
            return extended_obj

        file_dates = []
        date_formats_used = []
        key_pattern = obj.Key
        extended_obj = S3Source(Bucket=objects.Name, **obj.model_dump())
        for date_str in date_strs:
            for date_format in objects_pattern.date_formats:
                if file_date := validate_date(date_str, date_format):
                    file_dates.append(file_date)
                    date_formats_used.append(date_format)
                    key_pattern = key_pattern.replace(date_str, f"<{date_format.replace('%', '')}>")
        if file_dates:
            extended_obj.DateStr = date_strs[0]
            extended_obj.DateFormat = date_formats_used[0]
            extended_obj.FileDate = file_dates[0]
            extended_obj.KeyPattern = key_pattern
        return extended_obj

    def extract_pattern(obj: S3Source) -> S3Source:
        if not obj.KeyPattern:
            return obj

        for pattern_key, patterns in objects_pattern.extra_regex_patterns.items():
            extra_strs = list(
                chain(
                    *[
                        match if len(match) == 1 else list(chain(*match))
                        for match in [
                            re.findall(
                                pattern,
                                str(obj.KeyPattern),
                            )
                            for pattern in patterns
                        ]
                        if match
                    ]
                )
            )
            if not extra_strs:
                continue
            key_pattern = obj.KeyPattern
            obj.KeyPattern = obj.Key
            replace_str = f"<{pattern_key}>".replace("%", "_")
            for extra_str in extra_strs:
                key_pattern = key_pattern.replace(extra_str, replace_str)
            while f"{replace_str}{replace_str}" in key_pattern:
                key_pattern = key_pattern.replace(f"{replace_str}{replace_str}", replace_str)
            obj.KeyPattern = key_pattern
        return obj

    def extract_ext(obj: S3Source) -> S3Source:
        url = urlparse(obj.Key)
        obj.ObjectBaseName = url.path.lstrip("/")
        obj.ObjectSuffix = Path(url.path).suffix
        if not obj.ObjectSuffix:
            return obj

        if obj.ObjectSuffix in [c.value for c in Encryption]:
            obj.ObjectEncryption = Encryption(obj.ObjectSuffix)
            obj.ObjectBaseName = obj.ObjectBaseName[: -len(obj.ObjectSuffix)]
            obj.ObjectSuffix = Path(obj.ObjectBaseName).suffix

        if obj.ObjectSuffix in [c.value for c in Compression]:
            obj.ObjectCompression = Compression(obj.ObjectSuffix)
            obj.ObjectBaseName = obj.ObjectBaseName[: -len(obj.ObjectSuffix)]
            obj.ObjectSuffix = Path(obj.ObjectBaseName).suffix

        if obj.ObjectSuffix in [f.value for f in Format]:
            obj.ObjectFormat = Format(obj.ObjectSuffix)
            obj.ObjectBaseName = obj.ObjectBaseName[: -len(obj.ObjectSuffix)]
            obj.ObjectSuffix = Path(obj.ObjectBaseName).suffix

        obj.Prefix = obj.ObjectBaseName.rsplit("/", 1)[0]
        if obj.Prefix == obj.Bucket:
            obj.Prefix = ""
        return obj

    return [extract_ext(extract_pattern(extract_date(obj))) for obj in objects.Contents]
