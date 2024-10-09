from dataclasses import dataclass, field
import logging
from typing import Annotated

import typer

import filet
from filet.config.boto3_client import Boto3ClientConfig
from filet.config.objects_pattern import ObjectsPattern
from filet.config.trino_client import TrinoDwhConfig
from filet.config.utils.setup_logging import setup_logging

SilentOption = typer.Option(
    "--silent",
    "-s",
    help="Suppress progress output.",
    is_eager=True,
    is_flag=True,
)

VerboseOption = typer.Option(
    "--verbose",
    "-v",
    help="Set logging level is set to logging.DEBUG for module-level loggers.",
    is_eager=True,
    is_flag=True,
)

VerboseAllOption = typer.Option(
    "--verbose-all",
    "-vv",
    help="Set logging level is set to logging.DEBUG for all loggers.",
    is_eager=True,
    is_flag=True,
)

LogConfigOption = typer.Option(
    "--log-config",
    "-l",
    help="Path to logging config file. Use Debug level only in Development to prevent show secrets.",
    envvar=f"{filet.__name__.upper()}_LOG_CONFIG",
    is_eager=True,
    is_flag=True,
)

S3cfgOption = typer.Option(..., help="S3 Configs for the boto3 client.", rich_help_panel="Optional Config Overwrites")

ObjectsPatternOption = typer.Option(
    ..., help="Runtime Configs for the filet module.", rich_help_panel="Optional Config Overwrites"
)
TrinoDwhConfigOption = typer.Option(
    ..., help="Trino DWH Configs for the filet module.", rich_help_panel="Optional Config Overwrites"
)


@dataclass
class CommonOptions:
    """Dataclass defining CLI options used by all commands."""

    instance = None

    def __post_init__(self):
        self.logging_callback()
        CommonOptions.instance = self

    ctx: typer.Context
    silent: Annotated[bool, SilentOption] = False
    verbose: Annotated[bool, VerboseOption] = False
    verbose_all: Annotated[bool, VerboseAllOption] = False
    log_config: Annotated[str, LogConfigOption] = ""

    def logging_callback(self):
        """Default Option for verbose logging."""
        if self.verbose_all:
            setup_logging(default_level=logging.DEBUG, force=True)
            return

        loggers = []
        if hasattr(self.ctx.command.callback, "__module__") and self.ctx.command.callback.__module__:
            main_module_name = (
                self.ctx.command.callback.__module__.split(".", 1)[0] if self.ctx.command.callback.__module__ else None
            )
            loggers = [logger for logger in logging.root.manager.loggerDict if main_module_name in logger]
        setup_logging(
            default_level=logging.DEBUG if self.verbose else logging.root.level,
            loggers=loggers,
            default_path=self.log_config,
        )


@dataclass
class ProcessOptions(CommonOptions):
    """Options for processing."""

    s3cfg: Annotated[Boto3ClientConfig, S3cfgOption] = field(default_factory=lambda: Boto3ClientConfig())
    objects_pattern: Annotated[ObjectsPattern, ObjectsPatternOption] = field(default_factory=ObjectsPattern)
    trino_dwh_config: Annotated[TrinoDwhConfig, TrinoDwhConfigOption] = field(default_factory=TrinoDwhConfig)
