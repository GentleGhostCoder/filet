from typing import Dict, List, Tuple

from pydantic_settings import BaseSettings, SettingsConfigDict

from filet.config.cache_db import store
from filet.config.utils.default_config import default_config


class ObjectsPattern(BaseSettings):
    """Runtime Configuration of parsing."""

    model_config = SettingsConfigDict(env_file=default_config(store.default_config), extra="ignore")
    date_regex_patterns: Tuple[str, ...] = (
        r"\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}",
        r"\d{4}-\d{2}-\d{2}",
        r"\d{8}_\d{6}",
        r"\d{8}",
    )
    extra_regex_patterns: Dict[str, List[str]] = {
        "uuid": ["[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}"],
        "part": [r"part-\d{1,5}"],
        "space": ["[ ]"],
        "o_bracket": ["[(]"],
        "c_bracket": ["[)]"],
    }
    date_formats: Tuple[str, ...] = (
        "%Y-%m-%d_%H:%M:%S",
        "%Y%m%d_%H%M%S",
        "%Y-%m-%d",
        "%Y%m%d",
    )
    special_header_characters: Tuple[str, ...] = (
        ".",
        " ",
    )
