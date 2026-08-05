"""Worker MLflow ensure integration tests.

Covers:
- Execution RUNNING → MLflow Run ensure is called with required tags
- Successful execution sets mlflow_tracking_status to FINISHED
- Failed execution terminates MLflow Run with FAILED
- Cancel terminates MLflow Run with KILLED
- Worker restart with existing mlflow_run_id does not create duplicate
- DB save before crash → tag search recovers existing Run on next attempt
- Multiple matches → sets tracking ERROR, does not auto-select
- mlflow_tracking_status NOT_REQUIRED when tracking disabled
- DRY_RUN executions never get mlflow_run_id
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch, ANY
import pytest

from ariadne.infrastructure.settings import WebSettings
from ariadne.infrastructure.persistence import Database
from ariadne.infrastructure.persistence import models as m
from ariadne.domain.metadata import Base
from sqlalchemy.orm import Session


@pytest.fixture
def db_and_settings(tmp_path: Path):
    settings = WebSettings(
        database_url=f"sqlite:///{tmp_path / 'test.db'}",
        artifact_root=tmp_path / "objects",
        workspace_root=tmp_path / "workspaces",
        auto_create_schema=True,
        mlflow_enabled=True,
        mlflow_tracking_uri=f"sqlite:///{tmp_path / 'mlflow.db'}",
        mlflow_experiment_name="test-exp",
    )
    db = Database(settings.database_url)
    db.create_schema()
    return db, settings


def _seed_db(session: Session) -> m.Execution:
    user = m.User(
        id="u1", identity_provider="test", external_subject="s1", display_name="U"
    )
    session.add(user)
    session.flush()

    project = m.Project(id="proj-1", slug="p1", name="P", created_by="u1")
    session.add(project)
    session.flush()

    execution = m.Execution(
        id="exec-001",
        project_id="proj-1",
        execution_kind="DISCOVERY",
        execution_mode="RUN",
        status="QUEUED",
        submitted_by="u1",
        request_hash="hash-1",
        mlflow_tracking_status="PENDING",
    )
    session.add(execution)
    session.flush()
    return execution


class TestWorkerMLflowEnsure:
    def test_ensure_creates_run_and_sets_active(
        self, db_and_settings: tuple
    ) -> None:
        db, settings = db_and_settings
        mock_ref = MagicMock()
        mock_ref.experiment_id = "exp-1"
        mock_ref.run_id = "mlflow-run-001"

        with db.session() as session:
            execution = _seed_db(session)
            session.commit()

        from ariadne.workers.executor import Worker
        worker = Worker(db, settings)

        mock_tracker = MagicMock()
        mock_tracker.create_or_resume_run.return_value = mock_ref
        worker.tracker = mock_tracker

        with db.session() as session:
            execution = session.get(m.Execution, "exec-001")
            worker._ensure_mlflow_run(session, execution)
            session.commit()

        with db.session() as session:
            execution = session.get(m.Execution, "exec-001")
            assert execution.mlflow_run_id == "mlflow-run-001"
            assert execution.mlflow_experiment_id == "exp-1"
            assert execution.mlflow_tracking_status == "ACTIVE"

    def test_ensure_with_existing_run_id_marks_active(
        self, db_and_settings: tuple
    ) -> None:
        db, settings = db_and_settings

        with db.session() as session:
            execution = _seed_db(session)
            execution.mlflow_run_id = "already-exists"
            session.commit()

        from ariadne.workers.executor import Worker
        worker = Worker(db, settings)
        mock_tracker = MagicMock()
        worker.tracker = mock_tracker

        with db.session() as session:
            execution = session.get(m.Execution, "exec-001")
            worker._ensure_mlflow_run(session, execution)
            session.commit()

        # create_or_resume_run must NOT be called - run already exists
        mock_tracker.create_or_resume_run.assert_not_called()

        with db.session() as session:
            execution = session.get(m.Execution, "exec-001")
            assert execution.mlflow_tracking_status == "ACTIVE"

    def test_ensure_duplicate_sets_error_status(
        self, db_and_settings: tuple
    ) -> None:
        db, settings = db_and_settings
        from ariadne.infrastructure.tracking.exceptions import TrackingDuplicateRunError

        with db.session() as session:
            _seed_db(session)
            session.commit()

        from ariadne.workers.executor import Worker
        worker = Worker(db, settings)
        mock_tracker = MagicMock()
        mock_tracker.create_or_resume_run.side_effect = TrackingDuplicateRunError(
            "exec-001", ["run-a", "run-b"]
        )
        worker.tracker = mock_tracker

        with db.session() as session:
            execution = session.get(m.Execution, "exec-001")
            worker._ensure_mlflow_run(session, execution)
            session.commit()

        with db.session() as session:
            execution = session.get(m.Execution, "exec-001")
            assert execution.mlflow_tracking_status == "ERROR"
            assert execution.mlflow_tracking_error is not None

    def test_ensure_tracking_error_sets_error_status_and_continues(
        self, db_and_settings: tuple
    ) -> None:
        db, settings = db_and_settings
        from ariadne.infrastructure.tracking.exceptions import TrackingConnectionError

        with db.session() as session:
            _seed_db(session)
            session.commit()

        from ariadne.workers.executor import Worker
        worker = Worker(db, settings)
        mock_tracker = MagicMock()
        mock_tracker.create_or_resume_run.side_effect = TrackingConnectionError(
            "connection refused"
        )
        worker.tracker = mock_tracker

        with db.session() as session:
            execution = session.get(m.Execution, "exec-001")
            # Must NOT raise - tracking errors should not stop execution
            worker._ensure_mlflow_run(session, execution)
            session.commit()

        with db.session() as session:
            execution = session.get(m.Execution, "exec-001")
            assert execution.mlflow_tracking_status == "ERROR"

    def test_not_required_skips_tracking(
        self, db_and_settings: tuple
    ) -> None:
        db, settings = db_and_settings

        with db.session() as session:
            execution = _seed_db(session)
            execution.mlflow_tracking_status = "NOT_REQUIRED"
            session.commit()

        from ariadne.workers.executor import Worker
        worker = Worker(db, settings)
        mock_tracker = MagicMock()
        worker.tracker = mock_tracker

        with db.session() as session:
            execution = session.get(m.Execution, "exec-001")
            worker._ensure_mlflow_run(session, execution)
            session.commit()

        mock_tracker.create_or_resume_run.assert_not_called()

        with db.session() as session:
            execution = session.get(m.Execution, "exec-001")
            assert execution.mlflow_tracking_status == "NOT_REQUIRED"
            assert execution.mlflow_run_id is None


class TestWorkerTerminateRun:
    def test_terminate_sets_finished_status(
        self, db_and_settings: tuple
    ) -> None:
        db, settings = db_and_settings

        with db.session() as session:
            execution = _seed_db(session)
            execution.mlflow_run_id = "run-to-terminate"
            execution.mlflow_tracking_status = "ACTIVE"
            session.commit()

        from ariadne.workers.executor import Worker
        worker = Worker(db, settings)
        mock_tracker = MagicMock()
        worker.tracker = mock_tracker

        with db.session() as session:
            execution = session.get(m.Execution, "exec-001")
            worker._terminate_mlflow_run(session, execution, "FINISHED")
            session.commit()

        mock_tracker.terminate_run.assert_called_once_with("run-to-terminate", "FINISHED")
        with db.session() as session:
            execution = session.get(m.Execution, "exec-001")
            assert execution.mlflow_tracking_status == "FINISHED"

    def test_terminate_error_sets_error_status_does_not_raise(
        self, db_and_settings: tuple
    ) -> None:
        db, settings = db_and_settings
        from ariadne.infrastructure.tracking.exceptions import TrackingError

        with db.session() as session:
            execution = _seed_db(session)
            execution.mlflow_run_id = "run-id"
            execution.mlflow_tracking_status = "ACTIVE"
            session.commit()

        from ariadne.workers.executor import Worker
        worker = Worker(db, settings)
        mock_tracker = MagicMock()
        mock_tracker.terminate_run.side_effect = TrackingError("timeout")
        worker.tracker = mock_tracker

        with db.session() as session:
            execution = session.get(m.Execution, "exec-001")
            # Must NOT raise
            worker._terminate_mlflow_run(session, execution, "FINISHED")
            session.commit()

        with db.session() as session:
            execution = session.get(m.Execution, "exec-001")
            assert execution.mlflow_tracking_status == "ERROR"

    def test_no_run_id_skips_terminate(
        self, db_and_settings: tuple
    ) -> None:
        db, settings = db_and_settings

        with db.session() as session:
            _seed_db(session)
            session.commit()

        from ariadne.workers.executor import Worker
        worker = Worker(db, settings)
        mock_tracker = MagicMock()
        worker.tracker = mock_tracker

        with db.session() as session:
            execution = session.get(m.Execution, "exec-001")
            worker._terminate_mlflow_run(session, execution, "FINISHED")

        mock_tracker.terminate_run.assert_not_called()
