"""CLI Utils methods."""

import sys


def is_help():
    return len(sys.argv) == 1 or any(arg in ["-h", "--help"] for arg in sys.argv)


__all__ = ["is_help"]
