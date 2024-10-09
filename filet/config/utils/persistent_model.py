import pickle

from pydantic import BaseModel, ConfigDict, Field
from sqlitedict import SqliteDict


class PersistentModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    db_path: str = Field(default=":memory:", init_var=True)

    def get_db(self) -> SqliteDict:
        return SqliteDict(self.db_path, tablename=self.__class__.__name__, autocommit=True)

    def __init__(self, **data):
        super().__init__(**data)
        # Initialize the _db attribute
        self._db = self.get_db()
        # Load existing values from the database
        self._load_from_db()

    def _load_from_db(self):
        # Load and set each field from the database, if present
        for key in self.model_fields:
            if key in self._db:  # Check if the key exists in the database
                value = pickle.loads(self._db[key])
                super().__setattr__(key, value)  # Use super to avoid re-saving

    def _save_to_db(self, key, value):
        serialized_value = pickle.dumps(value)
        self._db[key] = serialized_value

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name in self.model_fields:
            self._save_to_db(name, value)

    def __getattr__(self, item):
        if item in self._db:
            return pickle.loads(self._db[item])
        return super().__getattr__(item)

    def save(self):
        for key in self.model_fields:
            self._save_to_db(key, getattr(self, key))

    def clear(self):
        self._db.clear()
        self._db.commit()
        self._db.close()
