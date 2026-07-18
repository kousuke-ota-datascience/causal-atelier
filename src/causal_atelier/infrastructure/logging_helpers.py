"""Logging helpers used by CLI entrypoints."""

from __future__ import annotations

import logging


def configure_logging(level: int = logging.INFO) -> None:
    """Configure a compact default logging format."""

    logging.basicConfig(level=level, format="%(levelname)s:%(name)s:%(message)s")


def get_logger(name: str) -> logging.Logger:
    """Return a named logger."""

    return logging.getLogger(name)


__all__ = ["configure_logging", "get_logger"]
