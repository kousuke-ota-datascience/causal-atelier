"""Tracking configuration resolved from CLI args, env vars, and defaults.

Priority (highest first):
  1. CLI arguments (caller passes overrides as constructor kwargs)
  2. Environment variables
  3. Hard-coded defaults
"""

from __future__ import annotations

import os
from dataclasses import dataclass


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


def _env_bool(name: str, default: bool) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    v = os.getenv(name)
    if v is None:
        return default
    try:
        return int(v)
    except ValueError:
        return default


@dataclass(frozen=True)
class TrackingSettings:
    """Resolved tracking configuration.  Credentials must not be stored here."""

    tracking_uri: str
    experiment_name: str
    enabled: bool
    timeout_seconds: int
    tag_prefix: str
    max_retry_attempts: int

    @classmethod
    def from_env(
        cls,
        *,
        tracking_uri: str | None = None,
        experiment_name: str | None = None,
        enabled: bool | None = None,
        timeout_seconds: int | None = None,
        tag_prefix: str | None = None,
    ) -> "TrackingSettings":
        """Build settings from environment variables with optional CLI overrides."""
        return cls(
            tracking_uri=tracking_uri or _env("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db"),
            experiment_name=experiment_name or _env("MLFLOW_EXPERIMENT_NAME", "ariadne"),
            enabled=enabled if enabled is not None else _env_bool("MLFLOW_ENABLED", True),
            timeout_seconds=timeout_seconds or _env_int("MLFLOW_TIMEOUT_SECONDS", 30),
            tag_prefix=tag_prefix or _env("MLFLOW_TAG_PREFIX", "ariadne."),
            max_retry_attempts=_env_int("MLFLOW_MAX_RETRY_ATTEMPTS", 3),
        )

    @classmethod
    def disabled(cls) -> "TrackingSettings":
        """Return settings with tracking disabled (for DRY_RUN / --disable-mlflow)."""
        return cls(
            tracking_uri="sqlite:///mlflow.db",
            experiment_name="ariadne",
            enabled=False,
            timeout_seconds=30,
            tag_prefix="ariadne.",
            max_retry_attempts=3,
        )


__all__ = ["TrackingSettings"]
