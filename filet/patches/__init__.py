"""This modul includes some enrichment for the pydantic / Typer library.

- Typer (click) CLI options Types support
- Typer global / common options support (passed by a dataclass)
- model_validator wrapper to use a SimpleNamespace instead data (dict)
"""

import pydantic
import pydantic_settings
import pydantic_core
import typer

__all__ = ["pydantic", "typer", "pydantic_settings", "pydantic_core"]
