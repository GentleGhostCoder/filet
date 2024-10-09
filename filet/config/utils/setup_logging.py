import fcntl
import logging
import logging.config
import os
import sys
from typing import List, Optional

from rich.logging import RichHandler
from rich.pretty import pretty_repr
import yaml

import filet


class UnblockTTY:
    def __enter__(self):
        self.fd = sys.stdin.fileno()
        self.flags_save = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        flags = self.flags_save & ~os.O_NONBLOCK
        fcntl.fcntl(self.fd, fcntl.F_SETFL, flags)

    def __exit__(self, *args):
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.flags_save)


class UnblockTTYRichHandler(RichHandler):
    """This handler unblocks the TTY before emitting a log record.

    This is useful when using the prompt_toolkit library (fix for BlockingIOError).
    """

    def emit(self, record):
        with UnblockTTY():
            super().emit(record)


class PrettyFormatter(logging.Formatter):
    def format(self, record):
        # Process each argument with pretty_repr if it's not a string
        if record.args:
            pretty_args = []
            if isinstance(record.args, dict):
                pretty_args = [pretty_repr(record.args, expand_all=True)]
            else:
                for arg in record.args:
                    if not isinstance(arg, str):
                        pretty_arg = pretty_repr(arg, expand_all=True)
                        pretty_args.append(pretty_arg)
                    else:
                        pretty_args.append(arg)
            record.args = tuple(pretty_args)

        format_specifiers_count = 0
        # Check if record.msg is not a string and convert it to a string
        if not isinstance(record.msg, str):
            record.msg = pretty_repr(record.msg, expand_all=True)
        else:
            # Count the number of format specifiers in the message
            format_specifiers_count = record.msg.count("%")

        # If there are more arguments than format specifiers
        if len(record.args) > format_specifiers_count:
            # Append the extra arguments to the message
            record.msg += " " + " ".join(map(str, record.args[format_specifiers_count:]))
            # Keep only the arguments that match the format specifiers
            record.args = record.args[:format_specifiers_count]

        # Format the record with pretty-printed arguments
        formatted_message = super().format(record)
        return formatted_message


def setup_logging(  # noqa: C901
    default_path: str = "",
    default_level: Optional[int] = None,
    env_key: str = f"{filet.__name__.upper()}_LOG_CONFIG",
    force: bool = False,
    loggers: Optional[List[str]] = None,
    handlers: Optional[List[str]] = None,
    **kwargs,
):
    """Setup logging configuration.

    :param force: Overwrite current log-level
    :param default_path: Default path to logging config file.
    :param default_level: Default log-level (Logging.INFO).
    :param env_key: Environment key to use for logging configuration.
    :param loggers: List of loggers to set log-level for.
    :param handlers: List of handlers to set log-level for.
    :param kwargs: arguments to pass to rich_handler
    """
    if value := os.getenv(env_key, None):
        default_path = value

    if os.path.exists(default_path):
        with open(default_path) as f:
            config = yaml.safe_load(f.read())
            if default_level:
                if force:
                    for handler_name in config["root"]["handlers"]:
                        if handlers and handler_name in handlers:
                            config["handlers"][handler_name]["level"] = default_level or logging.root.level
                    for logger in config["root"]["loggers"]:
                        if loggers and logger in loggers:
                            config["loggers"][logger]["level"] = default_level or logging.root.level
                config["root"]["level"] = default_level or logging.root.level
            logging.config.dictConfig(config)
    else:
        logging.config.dictConfig(
            {
                "version": 1,
                "formatters": {
                    "default": {
                        "()": PrettyFormatter,
                        "format": "[%(asctime)s] [%(name)s] [%(levelname)s] - %(funcName)s() - %(message)s",
                        "datefmt": "[%Y-%m-%d %H:%M:%S]",
                    },
                    "detailed": {
                        "format": "[%(asctime)s] [%(name)s] [%(levelname)s] [%(module)s] [%(process)d] [%(thread)d] - %(funcName)s() - %(message)s",
                        "datefmt": "[%Y-%m-%d %H:%M:%S]",
                    },
                },
                "handlers": {
                    "default": {
                        "class": (
                            "filet.config.utils.setup_logging.UnblockTTYRichHandler"
                            if "PYTEST_CURRENT_TEST" not in os.environ
                            else "logging.StreamHandler"
                        ),
                        "level": default_level or logging.root.level,
                        "formatter": "default",
                        "rich_tracebacks": True,
                    },
                },
                "root": {
                    "level": default_level or logging.root.level,
                    "handlers": ["default"],
                },
                "disable_existing_loggers": not force,
            }
        )
        for handler in logging.root.handlers:
            if hasattr(handler, "setLevel") and force:
                handler.setLevel(default_level or logging.root.level)
        for logger_name, logger in logging.root.manager.loggerDict.items():
            if isinstance(logger, logging.Logger) and loggers and logger_name in loggers:
                logger.disabled = False
                logger.setLevel(default_level or logging.root.level)
        if isinstance(logging.root, logging.Logger):
            logging.root.setLevel(default_level or logging.root.level)
