"""Trial 02 real-PostgreSQL acceptance evidence for E4-G03."""

from __future__ import annotations

import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from ariadne.product.application.execution_service import (
    CreateExecutionBatchCommand, ExecutionService, ExecutionVariantSpec,
)
from ariadne.product.domain.enums import AnalysisFamily, ExecutionOperation, ExecutionStatus, StageExecutionStatus
from ariadne.product.domain.errors import InvalidExecutionPlan, InvalidStateTransition
from ariadne.product.domain.execution_plan import ExecutionPlan, StageBinding, StageDefinition, StageType
from ariadne.product.persistence.repositories import SqlExecutionRepository, SqlStageExecutionRepository
from ariadne.product.persistence.unit_of_work import SqlUnitOfWork


def _ids() -> dict[str, str]:
    return {key: str(uuid.uuid4()) for key in ("project", "dataset", "artifact")}


def _seed_project_and_dataset(engine, ids: dict[str, str]) -> None:  # type: ignore[no-untyped-def]
    now = datetime.now(timezone.utc)
    with engine.begin() as connection:
        connection.execute(text(
            "INSERT INTO product_project (project_id,name,status,created_at,updated_at) "
            "VALUES (:project,:project,'ACTIVE',:now,:now)"
        ), {**ids, "now": now})
        connection.execute(text(
            "INSERT INTO product_artifact (artifact_id,project_id,artifact_type,object_key,content_hash,media_type,size_bytes,metadata_json,created_at) "
            "VALUES (:artifact,:project,'DATASET_FILE',:object_key,'hash','text/csv',1,'{}',:now)"
        ), {**ids, "object_key": f"g03/{ids['artifact']}", "now": now})
        connection.execute(text(
            "INSERT INTO product_dataset_version (dataset_version_id,project_id,source_artifact_id,dataset_key,name,version_label,content_hash,schema_json,profile_summary_json,row_count,column_count,created_at) "
            "VALUES (:dataset,:project,:artifact,:dataset,'g03','v1','hash','{\"columns\":[\"feature\"]}','{}',1,1,:now)"
        ), {**ids, "now": now})


def _delete_seed(engine, ids: dict[str, str]) -> None:  # type: ignore[no-untyped-def]
    with engine.begin() as connection:
        connection.execute(text("DELETE FROM product_stage_attempt WHERE stage_execution_id IN (SELECT stage_execution_id FROM product_stage_execution WHERE execution_id IN (SELECT execution_id FROM product_execution WHERE project_id=:project))"), ids)
        connection.execute(text("DELETE FROM product_stage_execution WHERE execution_id IN (SELECT execution_id FROM product_execution WHERE project_id=:project)"), ids)
        connection.execute(text("DELETE FROM product_execution WHERE project_id=:project"), ids)
        connection.execute(text("DELETE FROM product_dataset_version WHERE project_id=:project"), ids)
        connection.execute(text("DELETE FROM product_artifact WHERE project_id=:project"), ids)
        connection.execute(text("DELETE FROM product_project WHERE project_id=:project"), ids)


def _plan(family: AnalysisFamily, *, empty: bool = False) -> ExecutionPlan:
    stages = () if empty else (
        StageDefinition("prepare", StageType("core", "prepare", "1")),
        StageDefinition("analyze", StageType("core", "analyze", "1")),
    )
    bindings = () if empty else (StageBinding("prepare", "payload", "analyze", "payload"),)
    return ExecutionPlan.build(
        project_id="acceptance", analysis_specification_id="acceptance", analysis_family=family,
        planner_id="g03.acceptance", planner_version="1", stages=stages, dependencies=bindings,
    )


def _service(engine, plan_provider):  # type: ignore[no-untyped-def]
    @contextmanager
    def factory():
        session = Session(bind=engine)
        try:
            with SqlUnitOfWork(session) as uow:
                yield uow
        finally:
            session.close()

    service = ExecutionService(factory, plan_provider=plan_provider)
    service._validation.validate_submission = lambda **kwargs: None  # type: ignore[method-assign]
    return service


def _submit(engine, ids: dict[str, str], family: AnalysisFamily, plan_provider=None) -> str:  # type: ignore[no-untyped-def]
    service = _service(engine, plan_provider or (lambda execution: _plan(execution.analysis_family)))
    result = service.create_execution_batch(CreateExecutionBatchCommand(
        project_id=ids["project"], dataset_version_id=ids["dataset"],
        operation=ExecutionOperation.DISCOVERY, analysis_family=family,
        variants=[ExecutionVariantSpec("acceptance", analysis_spec_json={"operation_spec": {}})],
    ))
    return result.execution_ids[0]


@pytest.mark.postgres
@pytest.mark.parametrize("family", list(AnalysisFamily))
def test_g03_ac001_canonical_application_path_persists_and_reloads_each_family(postgres_engine, family: AnalysisFamily) -> None:  # type: ignore[no-untyped-def]
    ids = _ids(); _seed_project_and_dataset(postgres_engine, ids)
    try:
        execution_id = _submit(postgres_engine, ids, family)
        session = Session(bind=postgres_engine)
        try:
            stages = SqlStageExecutionRepository(session).list_for_execution(execution_id)
            assert len(stages) == 2
            assert {stage.execution_id for stage in stages} == {execution_id}
            assert [stage.stage_key for stage in stages] == ["prepare", "analyze"]
        finally:
            session.close()
    finally:
        _delete_seed(postgres_engine, ids)


@pytest.mark.postgres
def test_g03_ac002_persistent_round_trip_lists_bindings_timestamps_and_retry_history(postgres_engine) -> None:  # type: ignore[no-untyped-def]
    ids = _ids(); _seed_project_and_dataset(postgres_engine, ids)
    now = datetime.now(timezone.utc)
    try:
        execution_id = _submit(postgres_engine, ids, AnalysisFamily.CAUSAL)
        session = Session(bind=postgres_engine); executions = SqlExecutionRepository(session); stages = SqlStageExecutionRepository(session)
        claimed = executions.claim_next("token", worker_id="owner"); assert claimed and claimed.execution_id == execution_id
        session.commit()
        prepare = stages.list_for_execution(execution_id)[0]
        prepare.mark_ready(); stages.update(prepare, owner="owner")
        stages.start_attempt(prepare, owner="owner", worker_id="owner", at=now)
        prepare.input_binding = {"input": "binding"}; prepare.fail({"code": "TEMP"}, now + timedelta(seconds=1))
        stages.update(prepare, owner="owner"); session.commit(); stage_id = prepare.stage_execution_id
        session.close()

        session = Session(bind=postgres_engine); stages = SqlStageExecutionRepository(session)
        reloaded = stages.get(stage_id); assert reloaded is not None
        assert stages.list_for_execution(execution_id)[0].dependencies == ()
        assert reloaded.input_binding == {"input": "binding"}
        assert reloaded.last_error == {"code": "TEMP"}
        assert reloaded.started_at is not None and reloaded.finished_at is not None
        stages.start_attempt(reloaded, owner="owner", worker_id="owner", at=now + timedelta(seconds=2))
        reloaded.succeed({"output": "binding"}, now + timedelta(seconds=3)); stages.update(reloaded, owner="owner"); session.commit(); session.close()

        session = Session(bind=postgres_engine); reloaded = SqlStageExecutionRepository(session).get(stage_id); assert reloaded is not None
        assert reloaded.output_binding == {"output": "binding"}
        assert [attempt.attempt_number for attempt in reloaded.attempts] == [1, 2]
        assert reloaded.attempts[0].error == {"code": "TEMP"} and reloaded.attempts[1].error is None
        session.close()
    finally:
        _delete_seed(postgres_engine, ids)


@pytest.mark.postgres
def test_g03_ac005_persistent_failure_retry_cancellation_owner_and_invalid_success(postgres_engine) -> None:  # type: ignore[no-untyped-def]
    ids = _ids(); _seed_project_and_dataset(postgres_engine, ids); now = datetime.now(timezone.utc); session = None
    try:
        execution_id = _submit(postgres_engine, ids, AnalysisFamily.CAUSAL)
        session = Session(bind=postgres_engine); executions = SqlExecutionRepository(session); stages = SqlStageExecutionRepository(session)
        execution = executions.claim_next("token", worker_id="owner"); assert execution and execution.execution_id == execution_id; session.commit()
        first, second = stages.list_for_execution(execution_id)
        first.mark_ready(); stages.update(first, owner="owner"); stages.start_attempt(first, owner="owner", worker_id="owner", at=now)
        first.fail({"code": "FAIL"}, now); stages.update(first, owner="owner")
        execution.mark_failed(now, "FAIL"); executions.complete(execution, "owner"); session.commit(); session.close()

        session = Session(bind=postgres_engine); executions = SqlExecutionRepository(session); stages = SqlStageExecutionRepository(session)
        failed = executions.get(execution_id); assert failed and failed.status is ExecutionStatus.FAILED
        failed.increment_retry(); failed.clear_lease(); executions.update(failed, owner="owner"); session.commit()
        retried = executions.claim_next("retry-token", worker_id="retry-owner"); assert retried and retried.execution_id == execution_id
        first = stages.list_for_execution(execution_id)[0]; stable_stage_id = first.stage_execution_id
        stages.start_attempt(first, owner="retry-owner", worker_id="retry-owner", at=now + timedelta(seconds=1)); first.succeed({"ok": True}, now + timedelta(seconds=2)); stages.update(first, owner="retry-owner")
        second.cancel(now + timedelta(seconds=2)); stages.update(second, owner="retry-owner")
        retried.request_cancel(); executions.complete(retried, "retry-owner"); session.commit(); session.close()

        session = Session(bind=postgres_engine); executions = SqlExecutionRepository(session); stages = SqlStageExecutionRepository(session)
        parent = executions.get(execution_id); loaded = stages.get(stable_stage_id); assert parent and loaded
        assert parent.status is ExecutionStatus.CANCELLED and loaded.status is StageExecutionStatus.SUCCEEDED
        assert [item.attempt_number for item in loaded.attempts] == [1, 2]
        cancelled = stages.list_for_execution(execution_id)[1]; assert cancelled.status is StageExecutionStatus.CANCELLED
        with pytest.raises(InvalidStateTransition):
            cancelled.start_attempt("retry-owner", now)
        with pytest.raises(PermissionError):
            stages.update(loaded, owner="wrong-owner")
        session.rollback(); session.close()

        stale_id = _submit(postgres_engine, ids, AnalysisFamily.CAUSAL)
        session = Session(bind=postgres_engine); executions = SqlExecutionRepository(session); stages = SqlStageExecutionRepository(session)
        stale = executions.claim_next("stale-token", worker_id="stale-owner"); assert stale and stale.execution_id == stale_id; session.commit()
        session.execute(text("UPDATE product_execution SET lease_expires_at=:expired WHERE execution_id=:execution"), {"expired": now - timedelta(seconds=1), "execution": stale_id}); session.commit()
        session.expire_all()
        stale_stage = stages.list_for_execution(stale_id)[0]; stale_stage.mark_ready()
        with pytest.raises(PermissionError):
            stages.update(stale_stage, owner="stale-owner")
        session.rollback(); session.close()
        session = Session(bind=postgres_engine); unchanged = SqlStageExecutionRepository(session).list_for_execution(stale_id)[0]
        assert unchanged.status is StageExecutionStatus.PENDING
        session.execute(text("UPDATE product_execution SET status='CANCELLED', lease_owner=NULL, lease_expires_at=NULL WHERE execution_id=:execution"), {"execution": stale_id})
        session.commit(); session.close()

        invalid_id = _submit(postgres_engine, ids, AnalysisFamily.CAUSAL)
        session = Session(bind=postgres_engine); executions = SqlExecutionRepository(session)
        invalid = executions.claim_next("invalid-token", worker_id="invalid-owner"); assert invalid and invalid.execution_id == invalid_id
        invalid.mark_succeeded(now)
        with pytest.raises(InvalidStateTransition):
            executions.complete(invalid, "invalid-owner")
        session.rollback(); session.close()
    finally:
        if session is not None:
            session.rollback()
            session.close()
        _delete_seed(postgres_engine, ids)


@pytest.mark.postgres
def test_g03_ac004_ac007_materialization_failure_rolls_back_without_orphans_or_zero_stage_execution(postgres_engine) -> None:  # type: ignore[no-untyped-def]
    ids = _ids(); _seed_project_and_dataset(postgres_engine, ids)
    try:
        empty_service = _service(postgres_engine, lambda execution: _plan(execution.analysis_family, empty=True))
        command = CreateExecutionBatchCommand(project_id=ids["project"], dataset_version_id=ids["dataset"], operation=ExecutionOperation.DISCOVERY, variants=[ExecutionVariantSpec("acceptance")])
        with pytest.raises(InvalidExecutionPlan, match="Canonical execution requires a stage"):
            empty_service.create_execution_batch(command)
        with postgres_engine.connect() as connection:
            assert connection.scalar(text("SELECT count(*) FROM product_execution WHERE project_id=:project"), ids) == 0

        @contextmanager
        def failing_stage_write_uow():
            session = Session(bind=postgres_engine)
            delegate = SqlUnitOfWork(session)

            class FailingStages:
                def add_many(self, stages) -> None:  # type: ignore[no-untyped-def]
                    raise RuntimeError("injected stage persistence failure")

            class Uow:
                projects = delegate.projects
                dataset_versions = delegate.dataset_versions
                executions = delegate.executions
                graph_versions = delegate.graph_versions
                stage_executions = FailingStages()

                def commit(self) -> None:
                    delegate.commit()

                def __enter__(self):  # type: ignore[no-untyped-def]
                    return self

                def __exit__(self, exc_type, *args) -> None:  # type: ignore[no-untyped-def]
                    session.rollback() if exc_type else session.commit()

            try:
                yield Uow()
            finally:
                session.close()

        persistence_failure = ExecutionService(failing_stage_write_uow, plan_provider=lambda execution: _plan(execution.analysis_family))
        persistence_failure._validation.validate_submission = lambda **kwargs: None  # type: ignore[method-assign]
        with pytest.raises(RuntimeError, match="injected stage persistence failure"):
            persistence_failure.create_execution_batch(command)
        with postgres_engine.connect() as connection:
            assert connection.scalar(text("SELECT count(*) FROM product_execution WHERE project_id=:project"), ids) == 0
            assert connection.scalar(text("SELECT count(*) FROM product_stage_execution")) == 0

        def failing_plan(execution):  # type: ignore[no-untyped-def]
            raise RuntimeError("injected materialization failure")
        with pytest.raises(RuntimeError, match="injected materialization failure"):
            _submit(postgres_engine, ids, AnalysisFamily.CAUSAL, failing_plan)
        with postgres_engine.connect() as connection:
            assert connection.scalar(text("SELECT count(*) FROM product_execution WHERE project_id=:project"), ids) == 0
            assert connection.scalar(text("SELECT count(*) FROM product_stage_execution")) == 0

        execution_id = _submit(postgres_engine, ids, AnalysisFamily.CAUSAL)
        with postgres_engine.connect() as connection:
            assert connection.scalar(text("SELECT count(*) FROM product_stage_execution WHERE execution_id=:execution"), {"execution": execution_id}) == 2
            assert connection.scalar(text("SELECT count(*) FROM product_stage_execution WHERE execution_id=:execution AND stage_key='prepare'"), {"execution": execution_id}) == 1
    finally:
        _delete_seed(postgres_engine, ids)
