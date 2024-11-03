"""pydantic patch"""
from pydantic import *  # noqa: F403, F401

# patched objects
from aiapy.patches.pydantic_validator import BaseSettings, model_validator  # noqa: F403, F401
