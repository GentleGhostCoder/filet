"""ChunkDownload class for asynchronous downloading of byte-sized chunks from an S3 object."""

import asyncio
import logging
import os
from typing import Any, Callable, Optional
import zlib

import gnupg

from filet.boto3.async_handler import AsyncHandler
from filet.boto3.schema import Compression, Encryption, S3Source
from filet.boto3.types import S3Client


class ChunkDownload(AsyncHandler):
    logger = logging.getLogger(__name__)

    def __init__(
        self,
        boto3_client: S3Client,
        s3_source: S3Source,
        callback_func: Optional[Callable[[bytes], Any]] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.logger.debug("Initializing ChunkDownload for %s", s3_source)
        if not s3_source.Key:
            raise ValueError(f"S3Source {s3_source!r} has no key!")

        if s3_source.Extra:
            self.gpg_home = s3_source.Extra.GPGHome
            self.keyring_file_path = s3_source.Extra.KeyringFilePath
            self.passphrase = s3_source.Extra.Passphrase

        self.encryption = s3_source.ObjectEncryption
        self.compression = s3_source.ObjectCompression

        self.gz_compress = (
            self.compression == Compression.gzip
            or (self.compression == Compression.none and ".gz" in s3_source.Key[-3:])
            or None
        )
        self.gz_decompress_obj = self.gz_compress and zlib.decompressobj(zlib.MAX_WBITS | 16) or None
        self.decrypt_obj = (
            self.encryption != Encryption.none and gnupg.GPG(gnupghome=os.path.expanduser(self.gpg_home)) or None
        )

        self.__callback_func = callback_func or (lambda x: x)
        self.boto3_client = boto3_client
        self.Bucket: str = s3_source.Bucket
        self.Key: str = s3_source.Key
        self.VersionId: str = s3_source.VersionId
        self.chunk_size: int = s3_source.ChunkSize

        object_response = self.boto3_client.list_objects_v2(Bucket=s3_source.Bucket, Prefix=s3_source.Key)
        if object_response.get("KeyCount", 0) > 0:
            self.estimated_size = object_response["Contents"][0]["Size"]
        else:
            raise Exception("Object not found.")

        self.estimated_parts: int = round(self.estimated_size / self.chunk_size + 0.5)
        self.upload_contents: bytearray = bytearray()
        self.part_counter: int = 0
        self.current_upload_content_count: int = 0

        # Adjust the get_part method based on encryption and compression
        if self.encryption != Encryption.none:
            self.estimated_parts = 1
            self.chunk_size = self.estimated_size
            self.get_part = self.__get_encrypted_part
        elif self.gz_compress:
            self.get_part = self.__get_compressed_part
        else:
            self.get_part = self.__get_raw_part

    def decrypt_data(self, encrypted_data):
        """
        Decrypts encrypted data using GPG.
        """
        if self.keyring_file_path:
            with open(os.path.expanduser(self.keyring_file_path), "rb") as keyring_file:
                import_result = self.decrypt_obj.import_keys(keyring_file.read())
                self.logger.debug(f"Key Import Result: {import_result.summary()}")
        self.logger.debug(f"Decrypting data... {len(encrypted_data)} bytes.")
        decrypted_data = self.decrypt_obj.decrypt(encrypted_data, passphrase=self.passphrase)
        if decrypted_data.ok:
            self.logger.debug("Decryption successful.")
            return decrypted_data.data
        else:
            self.logger.error(f"Decryption failed: {decrypted_data.status}")
            return None

    def __get_encrypted_part(self):
        """
        Fetches an encrypted part of the S3 object, decrypts it, and optionally decompresses it.
        """
        encrypted_part = self.__get_raw_part()
        self.logger.debug(f"Encrypted Part: {len(encrypted_part)}")
        decrypted_part = self.decrypt_data(encrypted_part)
        if self.gz_compress:
            return self.gz_decompress_obj.decompress(decrypted_part)
        return decrypted_part

    def __get_raw_part(self):
        """Internal method to fetch a raw part of an S3 object, based on the current part counter.

        :return: The raw part as bytes.
        :rtype: bytes
        """
        self.part_counter += 1
        self.logger.debug(f"parts: {self.part_counter} / {self.estimated_parts}")
        # TODO Here we can implement more error-handling from response if needed
        return self.boto3_client.get_object(
            Bucket=self.Bucket,
            Key=self.Key,
            Range=f"bytes={(self.part_counter - 1) * self.chunk_size}-" f"{self.part_counter * self.chunk_size - 1}",
        )["Body"].read()

    def __get_compressed_part(self):
        """Internal method to fetch a compressed part of an S3 object and decompress it.

        :return: The decompressed part as bytes.
        :rtype: bytes
        """
        return self.gz_decompress_obj.decompress(self.__get_raw_part())

    def __get_last_part(self):
        """Internal method to fetch the last part of an S3 object.

        :return: The last part as bytes.
        :rtype: bytes
        """
        self.part_counter += 1
        # TODO Here we can implement more error-handling from response if needed
        return self.boto3_client.get_object(
            Bucket=self.Bucket,
            Key=self.Key,
            VersionId=self.VersionId or "null",
            Range=f"bytes={(self.part_counter - 1) * self.chunk_size}-" f"{self.estimated_size}",
        )["Body"].read()

    async def __run_until_complete(self):
        """Internal asynchronous method that runs until all parts are downloaded."""

        async def run():
            async with self.semaphore:
                self.__callback_func(self.get_part())

        await asyncio.gather(*(run() for _ in range(self.estimated_parts - self.part_counter)))

    def run_until_complete(self):
        """Executes the download process until completion.

        :return: The result of applying the callback function on the last downloaded chunk.
        :rtype: Any

        :Example:

        .. code-block:: python

            result = chunk_download.run_until_complete()  # xdoctest: +SKIP
        """
        self.event_loop.run_until_complete(self.__run_until_complete())
        last_part = bytearray(
            self.gz_decompress_obj.decompress(self.__get_last_part())
            if self.gz_decompress_obj
            else self.__get_last_part()
        )
        if self.gz_decompress_obj:
            last_part.extend(self.gz_decompress_obj.flush())
        return self.__callback_func(last_part)
