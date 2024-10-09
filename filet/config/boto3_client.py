import os
from typing import Annotated, Dict, Optional, Union

import boto3
from botocore.config import Config
from pydantic import BaseModel, ConfigDict, PlainSerializer, AliasChoices, Field, SecretStr, AnyUrl, model_validator, \
    BeforeValidator
from pydantic_settings import SettingsConfigDict, BaseSettings

from filet.config.cache_db import store
from filet.config.utils.default_ca_path import default_ca_path
from filet.config.utils.default_config import default_config


class BotocoreConfig(BaseModel):
    """This class is used to manage the configuration for Botocore -> compatible with AWS-ENV, .aws and s3cfg."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    proxies: Optional[Union[Dict[str, str], str]] = Field(default=None, validation_alias=AliasChoices("proxies", "proxy"), exclude=True)


class Boto3ClientSettings(BaseModel):
    """This class is used to manage the configuration for Boto3 client -> compatible with AWS-ENV, .aws and s3cfg."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    endpoint_url: Optional[Annotated[AnyUrl, PlainSerializer(lambda x: str(x), return_type=str)]] = Field(
        default=None, validation_alias=AliasChoices("aws_endpoint_url")
    )
    aws_access_key_id: Annotated[
        SecretStr, PlainSerializer(lambda x: x.get_secret_value(), return_type=str)] = SecretStr("")
    aws_secret_access_key: Annotated[
        SecretStr, PlainSerializer(lambda x: x.get_secret_value(), return_type=str)] = SecretStr("")

    # s3cfg compatible proxy_host, proxy_port
    proxies: Optional[Union[Dict[str, str], str]] = Field(
        default=None, validation_alias=AliasChoices("proxies", "proxy_host"), exclude=True
    )

    # optional configs (with defaults)
    service_name: str = Field(default="s3")
    region_name: Optional[str] = Field(default=None, validation_alias=AliasChoices("aws_default_region"))
    verify: str = Field(
        default_factory=default_ca_path, validation_alias=AliasChoices("aws_ca_bundle")
    )
    # automatically set
    config: Optional[BotocoreConfig] = Field(default=None)

    #     # Proxies
    #     if not self.proxies:
    #         return self
    #
    #     if isinstance(self.proxies, dict):
    #         # overwrite port if provided
    #         self.config = Config(proxies=self.proxies)
    #
    #     proxy_host = AnyUrl(str(self.proxies))
    #     protocol = proxy_host.scheme if proxy_host.scheme else "http"
    #     self.config = Config(
    #         proxies={
    #             "http": f"{protocol}://{proxy_host}:{self.proxy_port}",
    #             "https": f"{protocol}://{proxy_host}:{self.proxy_port}",
    #         }
    #     )


class Boto3ClientConfig(BaseSettings, Boto3ClientSettings):
    """This class is used to manage the configuration for Boto3 client -> compatible with AWS-ENV, .aws and s3cfg..

    :ivar endpoint_url: The endpoint URL for the Boto3 client.
    :ivar aws_access_key_id: The AWS access key ID.
    :ivar aws_secret_access_key: The AWS secret access key.
    :ivar proxies: The proxies to be used.
    :ivar service_name: The service name for the Boto3 client.
    :ivar region_name: The region name for the Boto3 client.
    :ivar verify: The verify setting for the Boto3 client.
    :ivar config: The config for the Boto3 client.

    Example:
        >>> boto_config = Boto3ClientConfig(endpoint_url="https://s3.endpoint.com",
        >>> aws_access_key_id="my-access-key", aws_secret_access_key="my-secret-key")
        >>> str(boto_config.endpoint_url)
        >>> 'https://s3.endpoint.com'
        >>> boto_config.aws_access_key_id  # This won't be visible in repr
        >>> 'my-access-key'
        >>> boto_config.aws_secret_access_key  # This won't be visible in repr
        >>> 'my-secret-key'
    """
    model_config = SettingsConfigDict(
        env_file=os.getenv("AWS_SHARED_CREDENTIALS_FILE", default_config([store.default_config, "~/.aws/credentials"])),
        extra="ignore",
        env_nested_delimiter=".",
    )


boto_config = Boto3ClientConfig(_env_file="~/.trinostage-rc", use_https=False)
