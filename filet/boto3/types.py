from typing import TYPE_CHECKING, Dict

from botocore.client import BaseClient

if TYPE_CHECKING:
    from mypy_boto3_s3.client import S3Client
    from mypy_boto3_s3.type_defs import (
        BucketTypeDef,
        CompletedMultipartUploadTypeDef,
        ListObjectsV2OutputTypeDef,
        OwnerTypeDef,
        ResponseMetadataTypeDef,
    )
else:
    S3Client = BaseClient
    CompletedMultipartUploadTypeDef = Dict[str, list]
    ResponseMetadataTypeDef = Dict[str, str]
    BucketTypeDef = Dict[str, str]
    OwnerTypeDef = Dict[str, str]
    ListObjectsV2OutputTypeDef = Dict[str, list]

__all__ = [
    "S3Client",
    "CompletedMultipartUploadTypeDef",
    "ResponseMetadataTypeDef",
    "BucketTypeDef",
    "OwnerTypeDef",
    "ListObjectsV2OutputTypeDef",
]
