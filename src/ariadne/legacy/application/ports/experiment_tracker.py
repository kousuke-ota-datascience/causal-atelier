"""Application-layer port for experiment tracking.

This Protocol keeps Application and Domain code independent of MLflow or any
other tracking backend SDK.  Adapters in ``infrastructure/tracking/`` implement
the protocol; callers use only the types defined here.

Retry / idempotency contract
-----------------------------
- ``create_or_resume_run`` is idempotent when called with the same
  ``execution_id`` tag: it returns the existing run rather than creating a
  duplicate.
- ``find_run_by_execution_id`` is read-only and safe to retry without side
  effects.
- ``log_params``, ``log_metrics``, ``set_tags``, ``log_artifact`` are
  best-effort; callers must not assume atomicity with the DB transaction.
- ``terminate_run`` is idempotent for the same terminal status; attempting to
  re-terminate with a different status may raise ``TrackingError``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class TrackingRunReference:
    """Minimal run identity returned by tracker operations."""

    experiment_id: str
    run_id: str
    lifecycle_status: str | None = None


class ExperimentTracker(Protocol):
    """MLflow-agnostic experiment tracking port."""

    def create_or_resume_run(
        self,
        *,
        experiment_name: str,
        tags: dict[str, str],
        run_name: str | None = None,
        execution_id: str,
    ) -> TrackingRunReference:
        """Create a new MLflow Run or return an existing one by execution_id tag.

        The implementation must search by ``ariadne.execution_id`` tag before
        creating a new run.  If exactly one match is found, that run is returned.
        If multiple matches are found, a ``TrackingError`` is raised rather than
        auto-selecting.
        """
        ...

    def find_run_by_execution_id(
        self, execution_id: str, experiment_name: str
    ) -> TrackingRunReference | None:
        """Search for an existing run tagged with the given execution_id.

        Returns ``None`` if no match is found.
        Raises ``TrackingError`` (with ``duplicate=True``) if multiple matches
        exist.
        """
        ...

    def log_params(self, run_id: str, params: dict[str, object]) -> None:
        """Log scalar parameters.  Values are coerced to str by the adapter."""
        ...

    def log_metrics(
        self, run_id: str, metrics: dict[str, float], step: int | None = None
    ) -> None:
        """Log numeric metrics.  NaN/Inf are replaced by the adapter per policy."""
        ...

    def set_tags(self, run_id: str, tags: dict[str, str]) -> None:
        """Set string tags.  Values are coerced to str by the adapter."""
        ...

    def log_artifact(
        self,
        run_id: str,
        local_path: str,
        artifact_path: str | None = None,
    ) -> None:
        """Upload a local file to the run artifact store."""
        ...

    def terminate_run(self, run_id: str, status: str) -> None:
        """Set the run to a terminal MLflow status: FINISHED, FAILED, or KILLED."""
        ...


__all__ = ["ExperimentTracker", "TrackingRunReference"]
