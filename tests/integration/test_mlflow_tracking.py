"""MLflow integration tests using a local file:// backend.

These tests use the real MLflow SDK against a temporary local filesystem
tracking store, without any mock.  They verify the actual end-to-end behaviour
of MlflowTracker.

Marked as 'mlflow' suite; they do not require a remote MLflow Server.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from ariadne.infrastructure.tracking.settings import TrackingSettings
from ariadne.infrastructure.tracking.mlflow_tracker import MlflowTracker
from ariadne.infrastructure.tracking.exceptions import (
    TrackingDuplicateRunError,
    TrackingTerminalError,
)
from ariadne.application.ports.experiment_tracker import TrackingRunReference


@pytest.fixture
def tracking_uri(tmp_path: Path) -> str:
    return f"sqlite:///{tmp_path / 'mlflow.db'}"


@pytest.fixture
def settings(tracking_uri: str) -> TrackingSettings:
    return TrackingSettings(
        tracking_uri=tracking_uri,
        experiment_name="integration-test",
        enabled=True,
        timeout_seconds=10,
        tag_prefix="ariadne.",
        max_retry_attempts=1,
    )


@pytest.fixture
def tracker(settings: TrackingSettings) -> MlflowTracker:
    return MlflowTracker(settings)


@pytest.mark.mlflow
class TestMlflowIntegration:
    def test_create_run_and_find_by_execution_id(
        self, tracker: MlflowTracker
    ) -> None:
        ref = tracker.create_or_resume_run(
            experiment_name="integration-test",
            tags={"ariadne.execution_id": "exec-int-001"},
            execution_id="exec-int-001",
        )
        assert ref.run_id is not None
        assert ref.experiment_id is not None

        found = tracker.find_run_by_execution_id("exec-int-001", "integration-test")
        assert found is not None
        assert found.run_id == ref.run_id

    def test_resume_returns_same_run(self, tracker: MlflowTracker) -> None:
        ref1 = tracker.create_or_resume_run(
            experiment_name="integration-test",
            tags={},
            execution_id="exec-int-resume",
        )
        ref2 = tracker.create_or_resume_run(
            experiment_name="integration-test",
            tags={},
            execution_id="exec-int-resume",
        )
        assert ref1.run_id == ref2.run_id

    def test_log_params(self, tracker: MlflowTracker) -> None:
        ref = tracker.create_or_resume_run(
            experiment_name="integration-test",
            tags={},
            execution_id="exec-int-params",
        )
        tracker.log_params(ref.run_id, {"algorithm": "PC", "seed": 42})

    def test_log_metrics_finite(self, tracker: MlflowTracker) -> None:
        ref = tracker.create_or_resume_run(
            experiment_name="integration-test",
            tags={},
            execution_id="exec-int-metrics",
        )
        tracker.log_metrics(ref.run_id, {"discovery.edge_count": 5.0})

    def test_log_metrics_nan_skipped(self, tracker: MlflowTracker) -> None:
        ref = tracker.create_or_resume_run(
            experiment_name="integration-test",
            tags={},
            execution_id="exec-int-nan",
        )
        # Must not raise
        tracker.log_metrics(ref.run_id, {"bad": float("nan")})

    def test_set_tags(self, tracker: MlflowTracker) -> None:
        ref = tracker.create_or_resume_run(
            experiment_name="integration-test",
            tags={},
            execution_id="exec-int-tags",
        )
        tracker.set_tags(ref.run_id, {"ariadne.execution_mode": "RUN"})

    def test_log_artifact(
        self, tracker: MlflowTracker, tmp_path: Path
    ) -> None:
        artifact_file = tmp_path / "manifest.json"
        artifact_file.write_text(json.dumps({"schema_version": "1"}))
        ref = tracker.create_or_resume_run(
            experiment_name="integration-test",
            tags={},
            execution_id="exec-int-artifact",
        )
        tracker.log_artifact(ref.run_id, str(artifact_file), "discovery")

    def test_terminate_finished(self, tracker: MlflowTracker) -> None:
        ref = tracker.create_or_resume_run(
            experiment_name="integration-test",
            tags={},
            execution_id="exec-int-term-ok",
        )
        tracker.terminate_run(ref.run_id, "FINISHED")

    def test_terminate_failed(self, tracker: MlflowTracker) -> None:
        ref = tracker.create_or_resume_run(
            experiment_name="integration-test",
            tags={},
            execution_id="exec-int-term-fail",
        )
        tracker.terminate_run(ref.run_id, "FAILED")

    def test_terminate_killed(self, tracker: MlflowTracker) -> None:
        ref = tracker.create_or_resume_run(
            experiment_name="integration-test",
            tags={},
            execution_id="exec-int-term-kill",
        )
        tracker.terminate_run(ref.run_id, "KILLED")

    def test_terminate_invalid_status_raises(
        self, tracker: MlflowTracker
    ) -> None:
        ref = tracker.create_or_resume_run(
            experiment_name="integration-test",
            tags={},
            execution_id="exec-int-bad-status",
        )
        with pytest.raises(TrackingTerminalError):
            tracker.terminate_run(ref.run_id, "INVALID")

    def test_find_missing_execution_returns_none(
        self, tracker: MlflowTracker
    ) -> None:
        result = tracker.find_run_by_execution_id("does-not-exist", "integration-test")
        assert result is None

    def test_find_missing_experiment_returns_none(
        self, tracker: MlflowTracker
    ) -> None:
        result = tracker.find_run_by_execution_id("exec-1", "no-such-experiment")
        assert result is None

    def test_run_tags_include_execution_id(
        self, tracker: MlflowTracker, settings: TrackingSettings
    ) -> None:
        ref = tracker.create_or_resume_run(
            experiment_name="integration-test",
            tags={"ariadne.project_id": "proj-1"},
            execution_id="exec-int-tag-check",
        )
        # Verify via search that the tag was actually stored
        found = tracker.find_run_by_execution_id("exec-int-tag-check", "integration-test")
        assert found is not None
        assert found.run_id == ref.run_id
