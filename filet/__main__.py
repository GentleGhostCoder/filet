"""Main Entrypoint for the module."""
import logging
import sys

from rich import print
import typer

from filet.cli.global_options import CommonOptions
from filet.cli.stage import add_group
from filet.cli.utils import is_help
logger = logging.getLogger(__name__)


def callback(ctx: typer.Context):
    """Callback function for the app."""
    if ctx.invoked_subcommand is None or (is_help() and ctx.command_path == "filet"):
        # print logo on help (every)
        print("""[blue]\n\t     FILET\n\t ૮₍ ˶ᵔ ᵕ ᵔ˶ ₎ა""")
    if ctx.invoked_subcommand is None:
        # print help on group calling without command
        ctx.get_help()
        ctx.exit()


app_settings = {
    "context_settings": {
        "help_option_names": ["-h", "--help"],
        "ignore_unknown_options": True,
        "allow_extra_args": True,
    },
    "invoke_without_command": True,
    "callback": callback,
    "chain": True,
}

app = typer.Typer(CommonOptions, **app_settings, add_completion=False)  # type: ignore

for cli_group in [add_group]:
    app.add_typer(cli_group, **app_settings)  # type: ignore


def main():
    """Main Entrypoint for the module."""
    try:
        app()  # type: ignore
        if len(sys.argv) > 1:
            logger.info("Execution completed successfully.")
            logger.info("Status: 0")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=logging.root.level == logging.DEBUG)
        logger.error("Status: 1")
        sys.exit(1)


if __name__ == "__main__":
    main()

_app_click_obj = typer.main.get_group(app)  # used for docs -> CLI commands

__all__ = ["app", "main", "_app_click_obj"]
