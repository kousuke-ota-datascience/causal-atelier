"""Unit tests for NullTracker.

Covers:
- SDK is never called
- Pseudo-IDs are never returned
- Log operations are silent no-ops
- create_or_resume_run raises TrackingDisabledError
- find_run_by_execution_id raises TrackingDisabledError
- terminate_run is a no-op (does not raise)
"""

from __future__ import annotations

import pytest

from ariadne.infrastructure.tracking.exceptions import TrackingDisabledError
from ariadne.infrastructure.tracking.null_tracker import NullTracker


@pytest.fixture
def tracker() -> NullTracker:
    return NullTracker()


class TestNullTrackerDisabledOperations:
    def test_create_or_resume_run_raises_disabled(self, tracker: NullTracker) -> None:
        with pytest.raises(TrackingDisabledError):
            tracker.create_or_resume_run(
                experiment_name="test",
                tags={},
                execution_id="exec-1",
            )

    def test_find_run_raises_disabled(self, tracker: NullTracker) -> None:
        with pytest.raises(TrackingDisabledError):
            tracker.find_run_by_execution_id("exec-1", "experiment")


class TestNullTrackerNoOps:
    def test_log_params_is_noop(self, tracker: NullTracker) -> None:
        tracker.log_params("run-id", {"param": "value"})  # must not raise

    def test_log_metrics_is_noop(self, tracker: NullTracker) -> None:
        tracker.log_metrics("run-id", {"metric": 1.0})  # must not raise

    def test_set_tags_is_noop(self, tracker: NullTracker) -> None:
        tracker.set_tags("run-id", {"tag": "value"})  # must not raise

    def test_log_artifact_is_noop(self, tracker: NullTracker) -> None:
        tracker.log_artifact("run-id", "/tmp/file.json")  # must not raise

    def test_terminate_run_is_noop(self, tracker: NullTracker) -> None:
        tracker.terminate_run("run-id", "FINISHED")  # must not raise

    def test_log_params_empty_is_noop(self, tracker: NullTracker) -> None:
        tracker.log_params("run-id", {})

    def test_log_metrics_empty_is_noop(self, tracker: NullTracker) -> None:
        tracker.log_metrics("run-id", {})

    def test_set_tags_empty_is_noop(self, tracker: NullTracker) -> None:
        tracker.set_tags("run-id", {})


class TestNullTrackerNoPseudoIds:
    def test_disabled_error_has_no_run_id(self, tracker: NullTracker) -> None:
        with pytest.raises(TrackingDisabledError) as exc_info:
            tracker.create_or_resume_run(
                experiment_name="test",
                tags={},
                execution_id="exec-1",
            )
        # The exception message must not look like a UUID (no pseudo-id generated)
        import re
        uuid_pattern = re.compile(
            r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
        )
        assert not uuid_pattern.search(str(exc_info.value))
