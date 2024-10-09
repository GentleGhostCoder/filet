"""Module to get the default configuration for the ini module."""

from pathlib import Path
from typing import List, Optional, Union

import filet


def default_config(configs: Optional[Union[str, List[str]]] = None) -> str:
    """Get the default configuration for the ini module.

    >>> isinstance(default_config(), str)
    True
    """
    if isinstance(configs, list) and (
        config := next((config for config in configs if Path(config).expanduser().exists()), None)
    ):
        return config
    if isinstance(configs, str) and Path(configs).expanduser().exists():
        return str(Path(configs).expanduser().resolve())
    return str(Path(filet.__file__).parent.resolve() / "config" / "default_config.ini")
