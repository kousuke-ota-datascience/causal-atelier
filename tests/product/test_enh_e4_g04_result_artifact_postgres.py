from __future__ import annotations

import uuid
from contextlib import contextmanager
from datetime import datetime, timezone

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from ariadne.product.application.output_ownership_service import OutputArtifact, OutputOwnershipService
from ariadne.product.domain.enums import AnalysisFamily, ArtifactScope, ArtifactType, ResultLevel, ResultType, ScientificStatus
from ariadne.product.domain.errors import OutputOwnershipError
from ariadne.product.domain.execution import Execution
from ariadne.product.domain.result import Result
from ariadne.product.domain.stage_execution import StageExecution
from ariadne.product.persistence.repositories import SqlStageExecutionRepository
from ariadne.product.persistence.unit_of_work import SqlUnitOfWork
from ariadne.product.workflow.output_contract import output_contract_for
from ariadne.adapters.local_artifact_store import LocalArtifactStore


def _ids() -> dict[str, str]:
    return {name: str(uuid.uuid4()) for name in ("project", "dataset", "artifact", "execution", "stage")}


def _seed(engine, ids: dict[str, str]) -> None:  # type: ignore[no-untyped-def]
    now = datetime.now(timezone.utc)
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO product_project (project_id,name,status,created_at,updated_at) VALUES (:project,'g04','ACTIVE',:now,:now)"), {**ids, "now": now})
        connection.execute(text("INSERT INTO product_artifact (artifact_id,project_id,artifact_type,object_key,content_hash,media_type,size_bytes,metadata_json,created_at) VALUES (:artifact,:project,'DATASET_FILE',:object_key,'source','text/csv',1,'{}',:now)"), {**ids, "object_key": f"source/{ids['artifact']}", "now": now})
        connection.execute(text("INSERT INTO product_dataset_version (dataset_version_id,project_id,source_artifact_id,dataset_key,name,version_label,content_hash,schema_json,profile_summary_json,row_count,column_count,created_at) VALUES (:dataset,:project,:artifact,:dataset,'g04','v1','source','{}','{}',1,1,:now)"), {**ids, "now": now})
        connection.execute(text("INSERT INTO product_execution (execution_id,project_id,dataset_version_id,batch_key,operation,analysis_family,analysis_spec_json,algorithm_or_estimator,parameter_json,code_version,runtime_version_json,snapshot_hash,status,retry_count,requested_by,requested_at) VALUES (:execution,:project,:dataset,:execution,'DISCOVERY','CAUSAL','{}','g04','{}','test','{}','g04','QUEUED',0,'g04',:now)"), {**ids, "now": now})


def _cleanup(engine, ids: dict[str, str]) -> None:  # type: ignore[no-untyped-def]
    with engine.begin() as connection:
        connection.execute(text("DELETE FROM product_artifact WHERE execution_id=:execution"), ids)
        connection.execute(text("DELETE FROM product_result WHERE execution_id=:execution"), ids)
        connection.execute(text("DELETE FROM product_stage_execution WHERE execution_id=:execution"), ids)
        connection.execute(text("DELETE FROM product_execution WHERE execution_id=:execution"), ids)
        connection.execute(text("DELETE FROM product_dataset_version WHERE dataset_version_id=:dataset"), ids)
        connection.execute(text("DELETE FROM product_artifact WHERE artifact_id=:artifact"), ids)
        connection.execute(text("DELETE FROM product_project WHERE project_id=:project"), ids)


def _service(engine, root):  # type: ignore[no-untyped-def]
    @contextmanager
    def factory():
        session = Session(bind=engine)
        try:
            with SqlUnitOfWork(session) as uow:
                yield uow
        finally:
            session.close()
    return OutputOwnershipService(factory, LocalArtifactStore(root))


@pytest.mark.postgres
def test_g04_ac001_ac002_postgres_round_trip_typed_result_and_artifact_ownership(postgres_engine, tmp_path) -> None:  # type: ignore[no-untyped-def]
    ids = _ids(); _seed(postgres_engine, ids)
    try:
        execution = Execution(execution_id=ids["execution"], project_id=ids["project"], analysis_family=AnalysisFamily.CAUSAL)
        stage = StageExecution(stage_execution_id=ids["stage"], execution_id=ids["execution"], stage_key="analysis")
        session = Session(bind=postgres_engine); repository = SqlStageExecutionRepository(session); repository.add(stage); session.commit(); session.close()
        result = Result(execution_id=ids["execution"], result_level=ResultLevel.STAGE_RESULT, stage_execution_id=ids["stage"], result_type=ResultType.DIAGNOSTICS_RESULT, scientific_status=ScientificStatus.PASS)
        service = _service(postgres_engine, tmp_path)
        _, artifacts = service.persist(
            execution, stage=stage, results=(result,),
            artifacts=(OutputArtifact(ArtifactType.LOG, b"canonical-bytes", "text/plain"),),
            contract=output_contract_for(AnalysisFamily.CAUSAL),
        )
        with postgres_engine.connect() as connection:
            row = connection.execute(text("SELECT result_level, execution_id, stage_execution_id FROM product_result WHERE result_id=:result"), {"result": result.result_id}).one()
            artifact = connection.execute(text("SELECT artifact_id, execution_id, stage_execution_id, result_id, artifact_scope, object_key FROM product_artifact WHERE artifact_id=:artifact"), {"artifact": artifacts[0].artifact_id}).one()
        assert row.result_level == "STAGE_RESULT" and row.execution_id == ids["execution"] and row.stage_execution_id == ids["stage"]
        assert artifact.execution_id == ids["execution"] and artifact.stage_execution_id == ids["stage"] and artifact.result_id == result.result_id
        assert artifact.artifact_scope == ArtifactScope.EXECUTION_OUTPUT.value and artifact.object_key != artifact.artifact_id

        wrong_stage = StageExecution(stage_execution_id=str(uuid.uuid4()), execution_id=str(uuid.uuid4()), stage_key="wrong")
        with pytest.raises(OutputOwnershipError):
            service.persist(execution, stage=wrong_stage, results=(result,), contract=output_contract_for(AnalysisFamily.CAUSAL))
        with pytest.raises(OutputOwnershipError):
            service.persist(execution, stage=stage, results=(Result(execution_id=str(uuid.uuid4()), result_level=ResultLevel.STAGE_RESULT, stage_execution_id=ids["stage"], result_type=ResultType.DIAGNOSTICS_RESULT, scientific_status=ScientificStatus.PASS),), contract=output_contract_for(AnalysisFamily.CAUSAL))
    finally:
        _cleanup(postgres_engine, ids)
