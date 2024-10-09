"""MultipartUpload class for uploading large data in parts to S3."""

import gc
import logging
import zlib

from mypy_boto3_s3.type_defs import CompletedMultipartUploadTypeDef

from filet.boto3.schema import Compression, S3Source
from filet.boto3.types import S3Client


class MultipartUpload:
    """Handles uploading byte-sized chunks to an S3 object in a memory-efficient manner.

    Supports optional GZIP compression before uploading to S3.

    :Example:
        >>> import boto3
        >>> from filet.boto3.schema import Compression, S3Source
        >>> from filet.config.boto3_client import Boto3ClientConfig
        >>> fake_boto3_client = boto3.client( # xdoctest: +SKIP
        ... **Boto3ClientConfig(endpoint_url="",aws_access_key_id="",aws_secret_access_key=""))
        >>> fake_s3_source = S3Source(bucket='test_bucket', key='test_key')
        >>> uploader = MultipartUpload(fake_boto3_client, fake_s3_source)  # xdoctest: +SKIP
        >>> uploader.upload_part(b"some bytes") # xdoctest: +SKIP
        >>> uploader.complete() # xdoctest: +SKIP
    """

    logger = logging.getLogger(__name__)

    def __init__(
        self,
        s3_client: S3Client,
        s3_source: S3Source,
        chunk_size: int = 10000000,
        **kwargs,
    ):
        """Initialize MultipartUpload.

        :param boto3_client: A boto3 S3 client object.
        :param s3_source: A S3Source object that contains information about the S3 destination.
        :param kwargs: Additional keyword arguments (current unused).
        :raises ValueError: If the s3_source object does not contain a key.
        """
        if not s3_source.Key:
            raise ValueError(f"S3Source {s3_source!r} has no key!")
        gz_compress = (
            s3_source.ObjectCompression == Compression.gzip
            or (s3_source.ObjectCompression == Compression.none and ".gz" in s3_source.Key[-3:])
            or None
        )
        if s3_source.ObjectCompression.value == Compression.gzip and ".gz" not in s3_source.Key[-3:]:
            s3_source.Key += ".gz"  # append .gz in key object if not exists
        self.gz_compress_obj = (
            gz_compress and zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, zlib.MAX_WBITS | 16) or None
        )
        self.boto3_client = s3_client
        self.Bucket: str = s3_source.Bucket
        self.Key: str = s3_source.Key
        self.VersionId: str = s3_source.VersionId
        self.chunk_size: int = chunk_size
        self.multipart_upload = s3_client.create_multipart_upload(Bucket=self.Bucket, Key=self.Key)
        self.parts: list = []
        self.upload_contents: bytearray = bytearray()
        self.part_counter: int = 0
        super().__init__(**kwargs)

    def upload_part_skip_cache(self, content: bytes):
        """Uploads a part to S3 directly, without utilizing the internal buffer.

        :param content: The byte content to upload as part of the multipart upload.
        """
        self.part_counter += 1
        self.parts.append(
            self.boto3_client.upload_part(
                Bucket=self.Bucket,
                Key=self.Key,
                PartNumber=self.part_counter,
                UploadId=self.multipart_upload["UploadId"],
                Body=content,
            )
        )

    def upload_part(self, content: bytes) -> None:
        """Adds content to the upload buffer and uploads to S3 when a certain size is reached.

        :param content: The byte content to add to the upload buffer.

        :Example:
            >>> uploader.upload_part(b'Hello, world!')  # xdoctest: +SKIP
        """
        self.upload_contents.extend(self.gz_compress_obj.compress(content) if self.gz_compress_obj else content)
        size = len(self.upload_contents)
        self.logger.info(
            f"add s3-upload buffer, size: {size}, parts: {self.part_counter}",
            extra={"buffer_size": size, "part_id": self.part_counter},
        )
        if size >= 20000000:
            self.upload_part_skip_cache(self.upload_contents[: size - 10000000])
            del self.upload_contents[: size - 10000000]
            gc.collect()

    async def async_upload_part(self, content: bytes) -> None:
        """Asynchronous wrapper for the upload_part method.

        :param content: The byte content to add to the upload buffer.

        :Example:
            >>> asyncio.run(uploader.async_upload_part(b'Hello, world!')) # xdoctest: +SKIP
        """
        self.upload_part(content)

    def __upload_last(self):
        """Internal method to handle the upload of the last part and clear the internal buffer."""
        if self.gz_compress_obj:
            self.upload_contents.extend(self.gz_compress_obj.flush())
        self.upload_part_skip_cache(self.upload_contents)
        self.upload_contents.clear()

    def abort(self) -> None:
        """Aborts the current multipart upload and cleans up any uploaded parts.

        :Example:
            >>> uploader.abort()  # xdoctest: +SKIP
        """
        self.boto3_client.abort_multipart_upload(
            Bucket=self.Bucket, Key=self.Key, UploadId=self.multipart_upload["UploadId"]
        )

    def complete(self) -> None:
        """Completes the multipart upload by sending a completion request to S3.

        :Example:
            >>> uploader.complete()  # xdoctest: +SKIP
        """
        try:
            if len(self.upload_contents):
                if self.part_counter:
                    self.__upload_last()
                else:
                    try:
                        self.logger.warning("Upload small Object with Size under 10Mb")
                        if self.gz_compress_obj:
                            self.upload_contents.extend(self.gz_compress_obj.flush())
                        self.boto3_client.put_object(Body=self.upload_contents, Bucket=self.Bucket, Key=self.Key)
                    except Exception as e:
                        self.logger.error(e, exc_info=True)
                        self.logger.error(
                            "Not parts uploaded!" + "Currently small Data not implemented for MultipartUpload!"
                        )
                        self.abort()
                    return
            part_info: CompletedMultipartUploadTypeDef = {
                "Parts": list({"PartNumber": x + 1, "ETag": self.parts[x]["ETag"]} for x in range(len(self.parts)))
            }
            self.logger.info("Complete Upload", extra={"part_info": part_info})
            self.boto3_client.complete_multipart_upload(
                Bucket=self.Bucket,
                Key=self.Key,
                UploadId=self.multipart_upload["UploadId"],
                MultipartUpload=part_info,
            )
        except Exception as e:
            self.logger.error(e)
            self.abort()
