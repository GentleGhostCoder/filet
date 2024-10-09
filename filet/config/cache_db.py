from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional, Union

import filet
from filet.boto3.schema import S3Source
from filet.config.utils.default_config import default_config
from filet.config.utils.persistent_model import PersistentModel
from filet.cpputils import CsvEvaluationResult

DATABASE_URL = str(Path(filet.__file__).parent.resolve() / "config" / "cache.db")


@dataclass
class SQL:
    """SQL queries for the stage"""
    create_table: Optional[str] = None
    create_target_table: Optional[str] = None
    drop_table: Optional[str] = None
    select: Optional[str] = None
    insert: Optional[str] = None


@dataclass
class Stage:
    table_name: Optional[str] = None
    db_schema: Optional[str] = None
    external_location: Optional[str] = None
    schema: Optional[Union[CsvEvaluationResult, Dict[str, Any]]] = None
    sql: SQL = field(default_factory=SQL)
    s3_source: Optional[S3Source] = None


class Store(PersistentModel):
    """Persistent storage for global configuration and profile"""
    db_path: str = DATABASE_URL
    default_config: str = default_config(".env")

    stages: Dict[str, Stage] = field(default_factory=dict)


@dataclass
class Cache:
    """In memory cache"""
    global_config: Optional[str] = None
    global_profile: Optional[str] = None


store = Store()
cache = Cache()
