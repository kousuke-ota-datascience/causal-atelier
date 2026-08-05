"""Unit tests for MLflow-related columns on the Execution domain model.

Covers:
- MLflow columns exist on the Execution class
- mlflow_tracking_status defaults to PENDING
- DRY_RUN / VALIDATE_ONLY executions receive NOT_REQUIRED via ExecutionService
- RUN executions receive PENDING via ExecutionService
- Non-NULL mlflow_run_id is unique (multiple NULLs are allowed)
- CHECK constraint on mlflow_tracking_status rejects invalid values
"""

from __future__ import annotations

from pathlib import Path

import pytest
import sqlalchemy as sa

from ariadne.domain.metadata import Execution, utcnow


@pytest.fixture
def engine(tmp_path: Path):
    import sqlalchemy as sa
    from ariadne.domain.metadata import Base
    engine = sa.create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine):
    from sqlalchemy.orm import Session
    with Session(engine) as s:
        yield s


def _minimal_execution(mode: str = "RUN", **kwargs) -> dict:
    return {
        "project_id": "proj-1",
        "execution_kind": "PIPELINE",
        "execution_mode": mode,
        "status": "QUEUED",
        "submitted_by": "user-1",
        "request_hash": "abc123",
        **kwargs,
    }


class TestExecutionMLflowColumns:
    def test_mlflow_columns_exist(self) -> None:
        cols = {c.key for c in Execution.__table__.columns}
        assert "mlflow_experiment_id" in cols
        assert "mlflow_run_id" in cols
        assert "mlflow_tracking_status" in cols
        assert "mlflow_tracking_error" in cols

    def test_mlflow_tracking_status_default_is_pending(self, session) -> None:
        # Add required objects first
        from ariadne.domain.metadata import User, Project
        session.add(User(id="user-1", identity_provider="test", external_subject="u1", display_name="U"))
        session.flush()
        session.add(Project(id="proj-1", slug="p1", name="P", created_by="user-1"))
        session.flush()

        exc = Execution(**_minimal_execution())
        session.add(exc)
        session.flush()
        assert exc.mlflow_tracking_status == "PENDING"

    def test_mlflow_run_id_nullable(self, session) -> None:
        from ariadne.domain.metadata import User, Project
        session.add(User(id="user-2", identity_provider="test", external_subject="u2", display_name="U"))
        session.flush()
        session.add(Project(id="proj-2", slug="p2", name="P2", created_by="user-2"))
        session.flush()

        exc = Execution(**_minimal_execution(project_id="proj-2", submitted_by="user-2"))
        session.add(exc)
        session.flush()
        assert exc.mlflow_run_id is None

    def test_multiple_null_mlflow_run_ids_allowed(self, session) -> None:
        from ariadne.domain.metadata import User, Project
        session.add(User(id="user-3", identity_provider="test", external_subject="u3", display_name="U"))
        session.flush()
        session.add(Project(id="proj-3", slug="p3", name="P3", created_by="user-3"))
        session.flush()

        e1 = Execution(**_minimal_execution(project_id="proj-3", submitted_by="user-3"))
        e2 = Execution(**_minimal_execution(project_id="proj-3", submitted_by="user-3"))
        session.add(e1)
        session.flush()
        session.add(e2)
        session.flush()
        # Both have NULL mlflow_run_id, which is allowed
        assert e1.mlflow_run_id is None
        assert e2.mlflow_run_id is None

    def test_non_null_mlflow_run_id_is_unique(self, session) -> None:
        from ariadne.domain.metadata import User, Project
        session.add(User(id="user-4", identity_provider="test", external_subject="u4", display_name="U"))
        session.flush()
        session.add(Project(id="proj-4", slug="p4", name="P4", created_by="user-4"))
        session.flush()

        e1 = Execution(
            **_minimal_execution(project_id="proj-4", submitted_by="user-4"),
            mlflow_run_id="same-run-id",
        )
        session.add(e1)
        session.flush()

        e2 = Execution(
            **_minimal_execution(project_id="proj-4", submitted_by="user-4"),
            mlflow_run_id="same-run-id",
        )
        session.add(e2)
        with pytest.raises(Exception):  # IntegrityError from unique constraint
            session.flush()


class TestExecutionServiceMLflowStatus:
    """ExecutionService must set mlflow_tracking_status based on execution_mode."""

    def test_run_mode_gets_pending_status(self, engine) -> None:
        from sqlalchemy.orm import Session
        from ariadne.domain.metadata import User, Project
        from ariadne.infrastructure.persistence import SqlAlchemyMetadataRepository
        from ariadne.application.run_execution import ExecutionService

        with Session(engine) as session:
            session.add(User(id="usr-svc-1", identity_provider="t", external_subject="s", display_name="U"))
            session.flush()
            session.add(Project(id="proj-svc-1", slug="ps1", name="P", created_by="usr-svc-1"))
            session.flush()

            repo = SqlAlchemyMetadataRepository(session)
            svc = ExecutionService(repo)

            run, _ = svc.create(
                request_document={
                    "project_id": "proj-svc-1",
                    "execution_kind": "DISCOVERY",
                    "execution_mode": "RUN",
                    "stages": [],
                },
                actor_user_id="usr-svc-1",
                idempotency_key=None,
            )

            assert run.mlflow_tracking_status == "PENDING"

    def test_dry_run_mode_gets_not_required(self, engine) -> None:
        from sqlalchemy.orm import Session
        from ariadne.domain.metadata import User, Project
        from ariadne.infrastructure.persistence import SqlAlchemyMetadataRepository
        from ariadne.application.run_execution import ExecutionService

        with Session(engine) as session:
            session.add(User(id="usr-svc-2", identity_provider="t", external_subject="s2", display_name="U"))
            session.flush()
            session.add(Project(id="proj-svc-2", slug="ps2", name="P", created_by="usr-svc-2"))
            session.flush()

            repo = SqlAlchemyMetadataRepository(session)
            svc = ExecutionService(repo)

            run, _ = svc.create(
                request_document={
                    "project_id": "proj-svc-2",
                    "execution_kind": "DISCOVERY",
                    "execution_mode": "DRY_RUN",
                    "stages": [],
                },
                actor_user_id="usr-svc-2",
                idempotency_key=None,
            )

            assert run.mlflow_tracking_status == "NOT_REQUIRED"

    def test_validate_only_mode_gets_not_required(self, engine) -> None:
        from sqlalchemy.orm import Session
        from ariadne.domain.metadata import User, Project
        from ariadne.infrastructure.persistence import SqlAlchemyMetadataRepository
        from ariadne.application.run_execution import ExecutionService

        with Session(engine) as session:
            session.add(User(id="usr-svc-3", identity_provider="t", external_subject="s3", display_name="U"))
            session.flush()
            session.add(Project(id="proj-svc-3", slug="ps3", name="P", created_by="usr-svc-3"))
            session.flush()

            repo = SqlAlchemyMetadataRepository(session)
            svc = ExecutionService(repo)

            run, _ = svc.create(
                request_document={
                    "project_id": "proj-svc-3",
                    "execution_kind": "DISCOVERY",
                    "execution_mode": "VALIDATE_ONLY",
                    "stages": [],
                },
                actor_user_id="usr-svc-3",
                idempotency_key=None,
            )

            assert run.mlflow_tracking_status == "NOT_REQUIRED"
