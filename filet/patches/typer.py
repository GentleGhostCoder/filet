"""typer patch"""
from typer import *  # noqa: F403, F401
import typer.main

# patched objects
from aiapy.patches.typer_cli_wrapper import Typer  # noqa: F403, F401
from aiapy.patches.typer_cli_wrapper import get_click_param as _get_click_param  # noqa: F403, F401
from aiapy.patches.typer_cli_wrapper import get_click_type as _get_click_type

typer.main.get_click_param = _get_click_param
typer.main.get_click_type = _get_click_type
