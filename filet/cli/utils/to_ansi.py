from typing import Optional

from prompt_toolkit import ANSI
from rich import get_console
from rich.console import Console


def to_ansi(*args, console: Optional[Console] = None, **kwargs):
    """Print the object as rich output."""
    if not console:
        console = get_console()
    with console.capture() as capture:
        console.print(*args, **kwargs)
    return ANSI(capture.get())
