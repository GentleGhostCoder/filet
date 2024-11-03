import logging
from typing import Annotated, Optional, Union

from pydantic import BaseModel, ConfigDict, PlainSerializer, SecretStr
from pydantic_settings import SettingsConfigDict, BaseSettings
from trino.auth import BasicAuthentication
from urllib3 import disable_warnings
import urllib3.exceptions

from filet.config.boto3_client import Boto3ClientSettings
from filet.config.cache_db import store
from filet.config.utils.default_ca_path import default_ca_path
from filet.patches.pydantic import AnyUrl, Field, model_validator

logger = logging.getLogger(__name__)


class TrinoConnectionArgs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    verify: Union[bool, str] = default_ca_path()
    user: Optional[str] = None
    auth: Optional[Union[BasicAuthentication, str]] = None
    http_scheme: str = "http"

    @model_validator(mode="before")
    def _auth_validator(self):
        if self.auth and len(auth := self.auth.split(":")) == 2:
            self.auth = BasicAuthentication(*auth)
            logger.debug("Basic Authentication: %s", self.auth)


class TrinoClientConfig(BaseModel):
    url: Optional[Annotated[AnyUrl, PlainSerializer(lambda x: str(x), return_type=str)]] = Field(default=None)
    connect_args: TrinoConnectionArgs = Field(default_factory=TrinoConnectionArgs)


class TrinoDwhConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=store.default_config,
        profile=store.default_profile,  # type: ignore
        env_prefix="trino_dwh_",
        env_nested_delimiter=".",
        extra="ignore",
    )

    boto3_client: Boto3ClientSettings = Field(
        default_factory=lambda: Boto3ClientSettings(
            aws_access_key_id=SecretStr(""), aws_secret_access_key=SecretStr("")
        )
    )
    client_config: TrinoClientConfig = Field(default_factory=TrinoClientConfig)
    disable_insecure_request_warning: bool = False
    hive_catalog: str = Field(default=None)
    iceberg_catalog: str = Field(default=None)
    external_location: str = Field(default=None)
    bronze_schema_name: str = "bronze"
    silver_schema_name: str = "silver"
    gold_schema_name: str = "gold"

    @model_validator(mode="before")
    def disable_warning(self):
        if self.external_location.startswith("s3a://"):
            self.external_location = self.external_location[6:]
        if self.disable_insecure_request_warning and not self.client_config.connect_args.verify:
            disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            logger.debug("Insecure Request Warning Disabled.")
