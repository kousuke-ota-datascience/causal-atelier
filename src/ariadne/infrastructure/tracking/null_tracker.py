"""Null experiment tracker for DRY_RUN, VALIDATE_ONLY, and --disable-mlflow.

Invariants
----------
- Never calls the MLflow SDK.
- Never generates pseudo run IDs.
- All log operations are silent no-ops.
- Callers can detect that tracking is disabled by catching
  ``TrackingDisabledError`` from ``find_run_by_execution_id``, or by checking
  ``isinstance(tracker, NullTracker)``.
"""

from __future__ import annotations

from ariadne.application.ports.experiment_tracker import (
    ExperimentTracker,
    TrackingRunReference,
)
from ariadne.infrastructure.tracking.exceptions import TrackingDisabledError


class NullTracker:
    """No-op tracker used when MLflow tracking is disabled."""

    def create_or_resume_run(
        self,
        *,
        experiment_name: str,
        tags: dict[str, str],
        run_name: str | None = None,
        execution_id: str,
    ) -> TrackingRunReference:
        raise TrackingDisabledError(
            "Tracking is disabled; create_or_resume_run is not available"
        )

    def find_run_by_execution_id(
        self, execution_id: str, experiment_name: str
    ) -> TrackingRunReference | None:
        raise TrackingDisabledError(
            "Tracking is disabled; find_run_by_execution_id is not available"
        )

    def log_params(self, run_id: str, params: dict[str, object]) -> None:
        pass

    def log_metrics(
        self, run_id: str, metrics: dict[str, float], step: int | None = None
    ) -> None:
        pass

    def set_tags(self, run_id: str, tags: dict[str, str]) -> None:
        pass

    def log_artifact(
        self,
        run_id: str,
        local_path: str,
        artifact_path: str | None = None,
    ) -> None:
        pass

    def terminate_run(self, run_id: str, status: str) -> None:
        pass


# Runtime check that NullTracker satisfies the ExperimentTracker protocol.
def _check_protocol() -> None:
    import typing
    assert typing.get_type_hints  # noqa: S101 – dev-time assertion only


__all__ = ["NullTracker"]
