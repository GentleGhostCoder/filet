from datetime import datetime
from enum import Enum
from typing import List, Optional, TypeVar

from pydantic import BaseModel, Field

from filet.boto3.types import ListObjectsV2OutputTypeDef

_T = TypeVar("_T")


class Owner(BaseModel):
    DisplayName: str
    ID: str


class Bucket(BaseModel):
    Name: str
    CreationDate: datetime


class ListObjectsV2ResponseMeta(BaseModel):
    HostId: str = ""
    HTTPStatusCode: int = 0
    RequestId: str = ""
    RetryAttempts: int = 0
    HTTPHeaders: dict = Field(default_factory=dict)


class ListBucketsResult(BaseModel):
    ResponseMetadata: ListObjectsV2ResponseMeta = Field(default_factory=ListObjectsV2ResponseMeta)
    Buckets: List[Bucket] = Field(default_factory=list)
    Owner: Owner


class ListObjectsV2ContentsOwner(BaseModel):
    DisplayName: str = ""
    ID: str = ""


class ListObjectsV2ContentsRestoreStatus(BaseModel):
    IsRestoreInProgress: bool = False
    RestoreExpiryDate: str = ""


class ListObjectsV2CommonPrefix(BaseModel):
    Prefix: str = ""


class ListObjectsV2ContentsChecksumAlgorithm(BaseModel):
    CRC32: str = ""
    CRC32C: str = ""
    SHA1: str = ""
    SHA256: str = ""


class ListObjectsV2Content(BaseModel):
    Key: str = ""
    LastModified: datetime = datetime.now()
    ETag: str = ""
    ChecksumAlgorithm: List[ListObjectsV2ContentsChecksumAlgorithm] = Field(default_factory=list)
    Size: int = 0
    StorageClass: str = ""
    Owner: ListObjectsV2ContentsOwner = Field(default_factory=ListObjectsV2ContentsOwner)
    RestoreStatus: ListObjectsV2ContentsRestoreStatus = Field(default_factory=ListObjectsV2ContentsRestoreStatus)


class ListObjectsV2Version(ListObjectsV2Content):
    VersionId: str = ""
    IsLatest: bool = False


class ListObjectsV2Result(BaseModel):
    ResponseMetadata: ListObjectsV2ResponseMeta = Field(default_factory=ListObjectsV2ResponseMeta)
    IsTruncated: bool = False
    Contents: List[ListObjectsV2Content] = Field(default_factory=list)
    Name: str = ""
    Prefix: str = ""
    Delimiter: str = "/"
    MaxKeys: int = 1000
    CommonPrefixes: List[ListObjectsV2CommonPrefix] = Field(default_factory=list)
    EncodingType: Optional[str] = None
    KeyCount: Optional[int] = None
    ContinuationToken: Optional[str] = None
    NextContinuationToken: Optional[str] = None
    StartAfter: Optional[str] = None
    RequestCharged: Optional[str] = None


class Encryption(Enum):
    """String representation of encryption."""

    gpg = ".gpg"
    pgp = ".pgp"
    none = ""


class Compression(Enum):
    """String representation of compressions."""

    gzip = ".gz"
    # TODO: Other compressions not implemented
    zstd = ".zstd"
    lz4 = ".lz4"
    snappy = ".snappy"
    none = ""


class Format(Enum):
    """String representation of file formats."""

    csv = ".csv"
    json = ".json"
    parquet = ".parquet"
    avro = ".avro"
    txt = ".txt"
    none = ""


class S3SourceExtra(BaseModel):
    """Extra options for S3Source."""

    GPGHome: str = ""
    KeyringFilePath: str = ""
    Passphrase: str = ""


class S3Source(ListObjectsV2Version):
    """Objects Meta with extracted Date and other attributes."""

    Bucket: str = ""
    Prefix: str = ""
    DateStr: str = ""
    DateFormat: str = ""
    FileDate: datetime = datetime.now()
    KeyPattern: str = ""
    ObjectBaseName: str = ""
    ObjectCompression: Compression = Compression.none
    ObjectFormat: Format = Format.none
    ObjectEncryption: Encryption = Encryption.none
    ObjectSuffix: str = ""
    Extra: Optional[S3SourceExtra] = None
    ChunkSize: int = 100000


# class Stage(Bucket):
#     """Stage with S3Source objects."""
#
#     Name: str = ""
#     Objects: List[S3Source] = Field(default_factory=list)
#     Owner: Owner
#     Location: str = ""
#     Catalog: str = ""
#     Schema: str = ""


def parse_list_objects_v2_result(response: ListObjectsV2OutputTypeDef) -> ListObjectsV2Result:
    """Parse ListObjectsV2Result from boto3 response."""
    return ListObjectsV2Result.parse_obj(response)
