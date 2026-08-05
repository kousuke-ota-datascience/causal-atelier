"""MLflow tracking adapter.

Design constraints
------------------
- Uses ``MlflowClient`` exclusively; never relies on the fluent API global
  active-run state.
- All operations use an explicit ``run_id``.
- Retries are bounded and do not duplicate Create operations.
- Credential values are never written to tags, params, or log messages.
- NaN / Inf metrics are replaced with ``None`` (skipped) with a warning.

Retry policy
------------
Connection errors and timeouts are retried up to ``max_retry_attempts`` times
with exponential back-off.  Auth, not-found, and invalid-request errors are
**not** retried.
"""

from __future__ import annotations

import logging
import math
import time
from typing import Any

from ariadne.application.ports.experiment_tracker import (
    ExperimentTracker,
    TrackingRunReference,
)
from ariadne.infrastructure.tracking.exceptions import (
    TrackingArtifactError,
    TrackingAuthError,
    TrackingConnectionError,
    TrackingDuplicateRunError,
    TrackingError,
    TrackingNotFoundError,
    TrackingTerminalError,
)
from ariadne.infrastructure.tracking.redaction import redact_secret
from ariadne.infrastructure.tracking.settings import TrackingSettings

logger = logging.getLogger(__name__)

_EXECUTION_ID_TAG = "ariadne.execution_id"

# MLflow terminal statuses accepted by terminate_run
_TERMINAL_STATUSES = {"FINISHED", "FAILED", "KILLED"}

# Retryable MlflowException messages / types (heuristic)
_RETRYABLE_SUBSTRINGS = ("connection", "timeout", "temporarily unavailable", "503", "502")


def _is_retryable(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(s in msg for s in _RETRYABLE_SUBSTRINGS)


def _safe_param_value(value: Any) -> str:
    """Coerce a param value to a string safe for MLflow."""
    if value is None:
        return ""
    return str(value)[:500]


def _safe_metric_value(key: str, value: float) -> float | None:
    """Return None for non-finite metric values (will be skipped)."""
    if not math.isfinite(value):
        logger.warning("Skipping non-finite metric %s=%s", key, value)
        return None
    if abs(value) > 1e308:
        logger.warning("Metric %s=%s exceeds MLflow range, skipping", key, value)
        return None
    return value


class MlflowTracker:
    """MLflow-backed ExperimentTracker implementation."""

    def __init__(self, settings: TrackingSettings) -> None:
        self._settings = settings
        self._client = self._build_client()

    def _build_client(self) -> Any:
        try:
            from mlflow.tracking import MlflowClient
        except ImportError as exc:
            raise TrackingError("mlflow-skinny is not installed") from exc
        return MlflowClient(tracking_uri=self._settings.tracking_uri)

    def _retry(self, fn: Any, *args: Any, **kwargs: Any) -> Any:
        last_exc: Exception | None = None
        for attempt in range(self._settings.max_retry_attempts):
            try:
                return fn(*args, **kwargs)
            except Exception as exc:
                if not _is_retryable(exc):
                    raise
                last_exc = exc
                wait = 2 ** attempt
                logger.warning("Tracking retry %d after error: %s", attempt + 1, exc)
                time.sleep(wait)
        raise TrackingConnectionError(
            f"MLflow operation failed after {self._settings.max_retry_attempts} retries"
        ) from last_exc

    def _resolve_experiment_id(self, experiment_name: str) -> str:
        try:
            experiment = self._retry(
                self._client.get_experiment_by_name, experiment_name
            )
        except TrackingError:
            raise
        except Exception as exc:
            self._raise_classified(exc)
        if experiment is None:
            try:
                return self._retry(
                    self._client.create_experiment, experiment_name
                )
            except Exception as exc:
                self._raise_classified(exc)
        return experiment.experiment_id

    def create_or_resume_run(
        self,
        *,
        experiment_name: str,
        tags: dict[str, str],
        run_name: str | None = None,
        execution_id: str,
    ) -> TrackingRunReference:
        existing = self.find_run_by_execution_id(execution_id, experiment_name)
        if existing is not None:
            logger.info(
                "Resuming existing MLflow run %s for execution_id=%s",
                existing.run_id,
                execution_id,
            )
            return existing

        experiment_id = self._resolve_experiment_id(experiment_name)
        safe_tags = {
            k: str(v)
            for k, v in tags.items()
            if v is not None
        }
        safe_tags[_EXECUTION_ID_TAG] = execution_id
        try:
            run = self._retry(
                self._client.create_run,
                experiment_id,
                run_name=run_name,
                tags=safe_tags,
            )
        except Exception as exc:
            self._raise_classified(exc)
        return TrackingRunReference(
            experiment_id=run.info.experiment_id,
            run_id=run.info.run_id,
            lifecycle_status=run.info.lifecycle_stage,
        )

    def find_run_by_execution_id(
        self, execution_id: str, experiment_name: str
    ) -> TrackingRunReference | None:
        try:
            experiment = self._retry(
                self._client.get_experiment_by_name, experiment_name
            )
        except Exception as exc:
            self._raise_classified(exc)
        if experiment is None:
            return None
        experiment_id = experiment.experiment_id
        try:
            runs = self._retry(
                self._client.search_runs,
                experiment_ids=[experiment_id],
                filter_string=f"tags.`{_EXECUTION_ID_TAG}` = '{execution_id}'",
                max_results=5,
            )
        except Exception as exc:
            self._raise_classified(exc)
        if len(runs) == 0:
            return None
        if len(runs) > 1:
            raise TrackingDuplicateRunError(
                execution_id=execution_id,
                run_ids=[r.info.run_id for r in runs],
            )
        run = runs[0]
        return TrackingRunReference(
            experiment_id=run.info.experiment_id,
            run_id=run.info.run_id,
            lifecycle_status=run.info.lifecycle_stage,
        )

    def log_params(self, run_id: str, params: dict[str, object]) -> None:
        if not params:
            return
        try:
            from mlflow.entities import Param
            param_list = [
                Param(key=k, value=_safe_param_value(v)) for k, v in params.items()
            ]
            self._retry(self._client.log_batch, run_id, params=param_list)
        except Exception as exc:
            self._raise_classified(exc)

    def log_metrics(
        self, run_id: str, metrics: dict[str, float], step: int | None = None
    ) -> None:
        if not metrics:
            return
        try:
            from mlflow.entities import Metric
            import time as _time
            ts = int(_time.time() * 1000)
            metric_list = []
            for k, v in metrics.items():
                safe_v = _safe_metric_value(k, v)
                if safe_v is not None:
                    metric_list.append(Metric(key=k, value=safe_v, timestamp=ts, step=step or 0))
            if metric_list:
                self._retry(self._client.log_batch, run_id, metrics=metric_list)
        except Exception as exc:
            self._raise_classified(exc)

    def set_tags(self, run_id: str, tags: dict[str, str]) -> None:
        if not tags:
            return
        try:
            from mlflow.entities import RunTag
            tag_list = [RunTag(key=k, value=str(v)) for k, v in tags.items() if v is not None]
            self._retry(self._client.log_batch, run_id, tags=tag_list)
        except Exception as exc:
            self._raise_classified(exc)

    def log_artifact(
        self,
        run_id: str,
        local_path: str,
        artifact_path: str | None = None,
    ) -> None:
        try:
            self._retry(
                self._client.log_artifact,
                run_id,
                local_path,
                artifact_path,
            )
        except Exception as exc:
            raise TrackingArtifactError(
                f"Artifact upload failed for run {run_id}: {redact_secret(str(exc))}"
            ) from exc

    def terminate_run(self, run_id: str, status: str) -> None:
        if status not in _TERMINAL_STATUSES:
            raise TrackingTerminalError(
                f"Invalid terminal status '{status}'. Must be one of {_TERMINAL_STATUSES}"
            )
        try:
            self._retry(self._client.set_terminated, run_id, status)
        except Exception as exc:
            raise TrackingTerminalError(
                f"Failed to terminate run {run_id}: {redact_secret(str(exc))}"
            ) from exc

    def _make_tag(self, key: str, value: str) -> Any:
        from mlflow.entities import RunTag
        return RunTag(key=key, value=str(value))

    def _raise_classified(self, exc: Exception) -> None:
        msg = redact_secret(str(exc))
        exc_type = type(exc).__name__.lower()
        if "authn" in exc_type or "auth" in exc_type or "permission" in exc_type:
            raise TrackingAuthError(msg) from exc
        if "notfound" in exc_type or "does not exist" in msg.lower():
            raise TrackingNotFoundError(msg) from exc
        if _is_retryable(exc):
            raise TrackingConnectionError(msg) from exc
        raise TrackingError(msg) from exc


__all__ = ["MlflowTracker"]
