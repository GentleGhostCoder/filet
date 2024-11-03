"""This Module Wraps the pydantic model_validator.

 It allows to use self as data mapping with autocompletion.
 Additionally, it allows to pass a profile and overwrite the env_file or select a specific profile.
"""

import configparser
from functools import wraps
from inspect import isclass, signature
from os import path
from typing import Literal, Optional

from pydantic import AliasChoices
from pydantic import BaseModel as PydanticBaseModel
from pydantic import model_validator as pydantic_model_validator
from pydantic_core import PydanticUndefinedType
from pydantic_settings import BaseSettings as PydanticBaseSettings

from aiapy.patches.utils.check_type import get_actual_type


def get_field_default(field):
    return (
        field.default
        if not isinstance(field.default, PydanticUndefinedType)
        else field.default_factory()
        if callable(field.default_factory)
        else None
    )


def remove_edge_quotes(value):
    if isinstance(value, str):
        return value.lstrip("'\"").rstrip("'\"")
    return value


def _map_validation_data(cls: PydanticBaseModel, data):
    """Map the data to the actual pydantic field, if the key is an alias."""
    _mapping = {}
    _nested_mapping_method = {}
    new_data = {}

    def _map_subclass(field, value, key):
        actual_type = get_actual_type(field.annotation)
        if isclass(actual_type) and issubclass(actual_type, PydanticBaseModel):
            i, m = _map_validation_data(actual_type, value)
            _nested_mapping_method[key] = m
            return i
        return value

    for key, field in cls.model_fields.items():
        if key in data:
            new_data[key] = _map_subclass(field, data.pop(key), key)
            _mapping[key] = key
            continue

        default = get_field_default(field)
        aliases = (
            field.validation_alias.choices
            if isinstance(field.validation_alias, AliasChoices)
            else [str(field.validation_alias)]
        )

        for alias in aliases:
            if alias in data:
                new_data[key] = _map_subclass(field, data.pop(alias, default), alias)
                _mapping[key] = alias
                break

    instance = cls.model_construct(**new_data)

    def mapping(i: PydanticBaseModel):
        return {
            _mapping[k]: remove_edge_quotes(val) if k not in _nested_mapping_method else _nested_mapping_method[k](val)
            for k in i.model_fields
            if k in _mapping
            if (val := getattr(i, k, get_field_default(field))) is not get_field_default(field)
        }

    return instance, mapping


def _nest_data(data, keys, value):
    if len(keys) == 1:
        data[keys[0]] = value
        return
    if keys[0] not in data:
        data[keys[0]] = {}
    _nest_data(data[keys[0]], keys[1:], value)


def _read_profile(cls, instance, data):
    if "profile" in data and data["profile"]:
        instance.model_config["profile"] = data.pop("profile")
    if "profile" in instance.model_config and instance.model_config["profile"]:
        profile = instance.model_config["profile"]
        env_file = instance.model_config["env_file"]
        config = configparser.ConfigParser(default_section="default")
        config.read(path.expanduser(env_file), encoding=instance.model_config["env_file_encoding"])
        if len(config.keys()) > 0 and profile not in config:
            profile = list(config.keys())[0]

        section_data = dict(config.items(profile, raw=True))
        # if the instance.mocel_config has env_nested_delimiter, then we need to nest the data by the delimiter
        if instance.model_config["env_nested_delimiter"]:
            nested_section_data = {}
            for k, v in section_data.items():
                if instance.model_config["env_nested_delimiter"] in k:
                    keys = k.split(instance.model_config["env_nested_delimiter"])
                    value = section_data.get(k)
                    # set the first key into the section_data and nest the rest of the keys
                    _nest_data(nested_section_data, keys, value)
            section_data.update(nested_section_data)

        # if the instance.model_config has env_prefix, then we need to remove the prefix from the keys
        if cls.model_config.get("env_prefix", None):
            prefix = cls.model_config["env_prefix"]
            section_data = {k.replace(prefix, ""): v for k, v in section_data.items()}

        return {key: remove_edge_quotes(value) for key, value in section_data.items()}


def model_validator(*, mode: Literal["wrap", "before", "after"]):  # noqa: C901
    """Wrapper method of the pydantic model_validation decorator.

    It helps to get the actual value from the pydantic field, if the key is an alias."""

    def wrapper(func):
        params = list(signature(func).parameters.keys())[1:]

        @wraps(func)
        @pydantic_model_validator(mode=mode)
        def wrapped(cls: PydanticBaseModel, data, *args, **kwargs) -> dict:
            if "data" in params:
                kwargs["data"] = data
            instance, mapping = _map_validation_data(cls, data)

            section_data = _read_profile(cls, instance, data)
            if section_data:
                section_instance, section_mapping = _map_validation_data(instance, section_data)
                section_data = section_mapping(section_instance)
                new_data = mapping(instance)
                new_data.update(section_data)
                instance, mapping = _map_validation_data(cls, new_data)

            new_instance = func(instance, *args, **kwargs)
            if new_instance is None:
                result = mapping(instance)
                return result
            return mapping(instance)

        return wrapped

    return wrapper


class BaseSettings(PydanticBaseSettings):
    """Wrapper for the BaseSettings class to support the model_validator decorator."""
    # profile: Optional[str] = None
    # _env_file: Optional[str] = None

    def __init__(self, *args, **values):
        # Check if profile is provided and set it
        if "profile" in self.model_config and self.model_config["profile"]:
            section_data = _read_profile(self.__class__, self, values)
            values.update(section_data)
        super().__init__(*args, **values)
        if "profile" in values and values["profile"]:
            self.model_config["profile"] = values.get("profile")
