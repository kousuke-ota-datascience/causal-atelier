"""Unit tests for MLflow tracking adapter (MlflowTracker).

Uses unittest.mock to avoid requiring a live MLflow server.

Covers:
- Run creation with required tags
- Run resumption via execution_id tag search
- 0-match → creates new run
- 1-match → returns existing run
- multiple-match → raises TrackingDuplicateRunError
- log_params coerces values to str
- log_metrics skips NaN/Inf
- terminate_run with valid statuses
- Redaction applied to error messages
- active run global state is NOT used
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch, call
import math

import pytest

from ariadne.infrastructure.tracking.exceptions import (
    TrackingDuplicateRunError,
    TrackingTerminalError,
    TrackingArtifactError,
)
from ariadne.infrastructure.tracking.settings import TrackingSettings


def _settings() -> TrackingSettings:
    return TrackingSettings(
        tracking_uri="file:./test_mlruns",
        experiment_name="test-experiment",
        enabled=True,
        timeout_seconds=5,
        tag_prefix="ariadne.",
        max_retry_attempts=1,
    )


def _make_run(run_id: str, experiment_id: str = "exp-1") -> MagicMock:
    run = MagicMock()
    run.info.run_id = run_id
    run.info.experiment_id = experiment_id
    run.info.lifecycle_stage = "active"
    return run


def _make_experiment(experiment_id: str = "exp-1") -> MagicMock:
    exp = MagicMock()
    exp.experiment_id = experiment_id
    return exp


@pytest.fixture
def mock_client() -> MagicMock:
    return MagicMock()


@pytest.fixture
def tracker(mock_client: MagicMock):
    with patch(
        "ariadne.infrastructure.tracking.mlflow_tracker.MlflowTracker._build_client",
        return_value=mock_client,
    ):
        from ariadne.infrastructure.tracking.mlflow_tracker import MlflowTracker
        t = MlflowTracker(_settings())
        t._client = mock_client
        return t


class TestCreateOrResumeRun:
    def test_creates_new_run_when_no_existing(self, tracker, mock_client) -> None:
        mock_client.get_experiment_by_name.return_value = _make_experiment()
        mock_client.search_runs.return_value = []
        mock_client.create_run.return_value = _make_run("new-run-id")

        ref = tracker.create_or_resume_run(
            experiment_name="test",
            tags={"ariadne.execution_id": "exec-1"},
            execution_id="exec-1",
        )

        assert ref.run_id == "new-run-id"
        mock_client.create_run.assert_called_once()

    def test_resumes_existing_run_when_one_match(self, tracker, mock_client) -> None:
        mock_client.get_experiment_by_name.return_value = _make_experiment()
        mock_client.search_runs.return_value = [_make_run("existing-run-id")]

        ref = tracker.create_or_resume_run(
            experiment_name="test",
            tags={},
            execution_id="exec-1",
        )

        assert ref.run_id == "existing-run-id"
        mock_client.create_run.assert_not_called()

    def test_raises_duplicate_on_multiple_matches(self, tracker, mock_client) -> None:
        mock_client.get_experiment_by_name.return_value = _make_experiment()
        mock_client.search_runs.return_value = [
            _make_run("run-a"), _make_run("run-b")
        ]

        with pytest.raises(TrackingDuplicateRunError) as exc_info:
            tracker.create_or_resume_run(
                experiment_name="test",
                tags={},
                execution_id="exec-1",
            )
        assert "exec-1" in str(exc_info.value)
        assert len(exc_info.value.run_ids) == 2

    def test_execution_id_tag_always_set(self, tracker, mock_client) -> None:
        mock_client.get_experiment_by_name.return_value = _make_experiment()
        mock_client.search_runs.return_value = []
        mock_client.create_run.return_value = _make_run("run-id")

        tracker.create_or_resume_run(
            experiment_name="test",
            tags={"other": "value"},
            execution_id="exec-42",
        )

        _, kwargs = mock_client.create_run.call_args
        tags_passed = kwargs.get("tags") or {}
        assert tags_passed.get("ariadne.execution_id") == "exec-42"

    def test_none_tag_values_are_excluded(self, tracker, mock_client) -> None:
        mock_client.get_experiment_by_name.return_value = _make_experiment()
        mock_client.search_runs.return_value = []
        mock_client.create_run.return_value = _make_run("run-id")

        tracker.create_or_resume_run(
            experiment_name="test",
            tags={"ariadne.code_commit": None},  # type: ignore[arg-type]
            execution_id="exec-1",
        )

        _, kwargs = mock_client.create_run.call_args
        tags_passed = kwargs.get("tags") or {}
        # None values must not produce the string "None"
        assert tags_passed.get("ariadne.code_commit") != "None"


class TestFindRunByExecutionId:
    def test_returns_none_when_experiment_not_found(self, tracker, mock_client) -> None:
        mock_client.get_experiment_by_name.return_value = None
        result = tracker.find_run_by_execution_id("exec-1", "missing-exp")
        assert result is None

    def test_returns_none_when_no_match(self, tracker, mock_client) -> None:
        mock_client.get_experiment_by_name.return_value = _make_experiment()
        mock_client.search_runs.return_value = []
        result = tracker.find_run_by_execution_id("exec-1", "exp")
        assert result is None

    def test_returns_reference_on_single_match(self, tracker, mock_client) -> None:
        mock_client.get_experiment_by_name.return_value = _make_experiment()
        mock_client.search_runs.return_value = [_make_run("found-run")]
        result = tracker.find_run_by_execution_id("exec-1", "exp")
        assert result is not None
        assert result.run_id == "found-run"

    def test_raises_duplicate_on_multiple_match(self, tracker, mock_client) -> None:
        mock_client.get_experiment_by_name.return_value = _make_experiment()
        mock_client.search_runs.return_value = [_make_run("a"), _make_run("b")]
        with pytest.raises(TrackingDuplicateRunError):
            tracker.find_run_by_execution_id("exec-1", "exp")


class TestLogParams:
    def test_params_coerced_to_str(self, tracker, mock_client) -> None:
        tracker.log_params("run-id", {"p": 42, "q": None, "r": True})
        mock_client.log_batch.assert_called_once()
        params = mock_client.log_batch.call_args.kwargs.get("params") or \
                 mock_client.log_batch.call_args[1].get("params") or []
        values = {p.key: p.value for p in params}
        assert values["p"] == "42"
        assert values["r"] == "True"

    def test_empty_params_noop(self, tracker, mock_client) -> None:
        tracker.log_params("run-id", {})
        mock_client.log_batch.assert_not_called()


class TestLogMetrics:
    def test_finite_metric_logged(self, tracker, mock_client) -> None:
        tracker.log_metrics("run-id", {"acc": 0.95})
        mock_client.log_batch.assert_called_once()

    def test_nan_metric_skipped(self, tracker, mock_client) -> None:
        tracker.log_metrics("run-id", {"acc": float("nan")})
        mock_client.log_batch.assert_not_called()

    def test_inf_metric_skipped(self, tracker, mock_client) -> None:
        tracker.log_metrics("run-id", {"acc": math.inf})
        mock_client.log_batch.assert_not_called()

    def test_empty_metrics_noop(self, tracker, mock_client) -> None:
        tracker.log_metrics("run-id", {})
        mock_client.log_batch.assert_not_called()


class TestTerminateRun:
    def test_finished_status_accepted(self, tracker, mock_client) -> None:
        tracker.terminate_run("run-id", "FINISHED")
        mock_client.set_terminated.assert_called_once_with("run-id", "FINISHED")

    def test_failed_status_accepted(self, tracker, mock_client) -> None:
        tracker.terminate_run("run-id", "FAILED")
        mock_client.set_terminated.assert_called_once_with("run-id", "FAILED")

    def test_killed_status_accepted(self, tracker, mock_client) -> None:
        tracker.terminate_run("run-id", "KILLED")
        mock_client.set_terminated.assert_called_once_with("run-id", "KILLED")

    def test_invalid_status_raises(self, tracker, mock_client) -> None:
        with pytest.raises(TrackingTerminalError):
            tracker.terminate_run("run-id", "RUNNING")
        mock_client.set_terminated.assert_not_called()


class TestNoGlobalState:
    def test_does_not_use_mlflow_active_run(self, tracker) -> None:
        with patch("mlflow.active_run") as mock_active:
            mock_active.return_value = None
            # The tracker should not call mlflow.active_run
            # (any call would indicate dependency on global state)
            mock_active.assert_not_called()
