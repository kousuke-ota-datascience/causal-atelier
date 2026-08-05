"""Tracking-specific exceptions mapped to application-understandable categories."""

from __future__ import annotations


class TrackingError(Exception):
    """Base class for all experiment tracking errors."""

    def __init__(self, message: str, *, redacted: bool = True) -> None:
        super().__init__(message)
        self.redacted = redacted


class TrackingConnectionError(TrackingError):
    """Cannot reach the tracking server (network / timeout)."""


class TrackingAuthError(TrackingError):
    """Authentication or authorisation failure with the tracking server."""


class TrackingNotFoundError(TrackingError):
    """A requested run or experiment was not found."""


class TrackingDuplicateRunError(TrackingError):
    """Multiple runs matched the same execution_id tag."""

    def __init__(self, execution_id: str, run_ids: list[str]) -> None:
        count = len(run_ids)
        super().__init__(
            f"Found {count} MLflow runs for execution_id={execution_id}; "
            "cannot auto-select. Manual cleanup required.",
        )
        self.execution_id = execution_id
        self.run_ids = run_ids


class TrackingArtifactError(TrackingError):
    """Artifact upload or download failed."""


class TrackingTerminalError(TrackingError):
    """Transitioning a run to a terminal state failed."""


class TrackingDisabledError(TrackingError):
    """Tracking is disabled (Null Tracker); the operation is a no-op."""
