from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest
from sqlalchemy import text

from ariadne.product.domain.enums import AnalysisFamily
from ariadne.product.domain.execution import Execution
from ariadne.product.domain.execution_plan import ExecutionPlan, StageDefinition, StageType
from ariadne.product.persistence.repositories import SqlStageExecutionRepository
from ariadne.product.workflow.stage_materialization import StagePlanMaterializer


def _ids() -> dict[str, str]:
    return {key: str(uuid.uuid4()) for key in ("project", "dataset", "artifact", "execution")}


@pytest.mark.postgres
def test_g03_ac001_ac002_persistent_stage_round_trip(postgres_engine) -> None:  # type: ignore[no-untyped-def]
    ids = _ids()
    now = datetime.now(timezone.utc)
    with postgres_engine.begin() as connection:
        connection.execute(text(
            "INSERT INTO product_project (project_id,name,status,created_at,updated_at) "
            "VALUES (:project,'g03-stage','ACTIVE',:now,:now)"
        ), {**ids, "now": now})
        connection.execute(text(
            "INSERT INTO product_artifact (artifact_id,project_id,artifact_type,object_key,content_hash,media_type,size_bytes,metadata_json,created_at) "
            "VALUES (:artifact,:project,'DATASET_FILE',:key,'g03-hash','text/csv',1,'{}',:now)"
        ), {**ids, "key": f"g03/{ids['artifact']}", "now": now})
        connection.execute(text(
            "INSERT INTO product_dataset_version (dataset_version_id,project_id,source_artifact_id,dataset_key,name,version_label,content_hash,schema_json,profile_summary_json,row_count,column_count,created_at) "
            "VALUES (:dataset,:project,:artifact,'g03','g03','v1','g03-hash','{}','{}',1,1,:now)"
        ), {**ids, "now": now})
        connection.execute(text(
            "INSERT INTO product_execution (execution_id,project_id,dataset_version_id,batch_key,operation,analysis_spec_json,algorithm_or_estimator,parameter_json,code_version,runtime_version_json,snapshot_hash,status,retry_count,requested_by,requested_at,lease_owner) "
            "VALUES (:execution,:project,:dataset,:execution,'DISCOVERY','{}','pc','{}','test','{}','g03-hash','QUEUED',0,'g03',:now,NULL)"
        ), {**ids, "now": now})

    execution = Execution(execution_id=ids["execution"], project_id=ids["project"],
                          dataset_version_id=ids["dataset"], analysis_family=AnalysisFamily.CAUSAL)
    plan = ExecutionPlan.build(
        project_id=ids["project"], analysis_specification_id="g03",
        analysis_family=AnalysisFamily.CAUSAL, planner_id="g03", planner_version="1",
        stages=(StageDefinition("prepare", StageType("core", "prepare", "1")),),
    )
    stage = StagePlanMaterializer.materialize(execution, plan)[0]
    from sqlalchemy.orm import Session
    session = Session(bind=postgres_engine)
    repository = SqlStageExecutionRepository(session)
    repository.add(stage)
    session.commit()
    session.execute(text(
        "UPDATE product_execution SET status='RUNNING', lease_owner='worker' WHERE execution_id=:execution"
    ), ids)
    session.commit()
    loaded = repository.get(stage.stage_execution_id)
    assert loaded is not None
    loaded.mark_ready()
    repository.update(loaded, owner="worker")
    repository.start_attempt(loaded, owner="worker", worker_id="worker", at=now)
    loaded.input_binding = {"input": "binding/1"}
    loaded.fail({"code": "TEST", "message": "failure"}, now)
    repository.update(loaded, owner="worker")
    session.commit()
    round_tripped = repository.get(stage.stage_execution_id)
    assert round_tripped is not None
    assert round_tripped.execution_id == ids["execution"]
    assert round_tripped.input_binding == {"input": "binding/1"}
    assert round_tripped.last_error == {"code": "TEST", "message": "failure"}
    assert [attempt.attempt_number for attempt in round_tripped.attempts] == [1]
    assert round_tripped.attempts[0].error == {"code": "TEST", "message": "failure"}
    session.close()

    with postgres_engine.begin() as connection:
        connection.execute(text("DELETE FROM product_stage_attempt WHERE stage_execution_id=:stage"), {"stage": stage.stage_execution_id})
        connection.execute(text("DELETE FROM product_stage_execution WHERE stage_execution_id=:stage"), {"stage": stage.stage_execution_id})
        connection.execute(text("DELETE FROM product_execution WHERE execution_id=:execution"), ids)
        connection.execute(text("DELETE FROM product_dataset_version WHERE dataset_version_id=:dataset"), ids)
        connection.execute(text("DELETE FROM product_artifact WHERE artifact_id=:artifact"), ids)
        connection.execute(text("DELETE FROM product_project WHERE project_id=:project"), ids)
