from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ariadne.product.domain.artifact import Artifact
from ariadne.product.domain.enums import (
    ArtifactScope, ArtifactType, ResultLevel, ResultType, ScientificStatus,
)
from ariadne.product.domain.errors import InvalidAnalysisSpec
from ariadne.product.domain.result import Result
from ariadne.product.domain.stage_execution import StageExecution
from ariadne.product.persistence.repositories import (
    SqlArtifactRepository, SqlResultRepository, SqlStageExecutionRepository,
)


_RESULTS = (
    (ResultType.DATA_PROFILE_RESULT, ScientificStatus.GENERATED),
    (ResultType.DISTRIBUTION_RESULT, ScientificStatus.GENERATED_WITH_WARNINGS),
    (ResultType.ASSOCIATION_RESULT, ScientificStatus.GENERATED),
    (ResultType.GROUP_SUMMARY_RESULT, ScientificStatus.GENERATED),
    (ResultType.CHART_RESULT, ScientificStatus.GENERATED),
    (ResultType.SPLIT_RESULT, ScientificStatus.PASS),
    (ResultType.TRAINING_RESULT, ScientificStatus.TRAINED),
    (ResultType.TRAINING_RESULT, ScientificStatus.TRAINED_WITH_WARNINGS),
    (ResultType.EVALUATION_RESULT, ScientificStatus.EVALUATED),
    (ResultType.EVALUATION_RESULT, ScientificStatus.INSUFFICIENT_TEST_SAMPLE),
    (ResultType.ERROR_ANALYSIS_RESULT, ScientificStatus.GENERATED_WITH_WARNINGS),
    (ResultType.PREDICTIVE_EXPLANATION_RESULT, ScientificStatus.NOT_APPLICABLE),
    (ResultType.MODEL_CARD_RESULT, ScientificStatus.GENERATED),
)
_ARTIFACTS = (
    ArtifactType.CHART_SPECIFICATION, ArtifactType.PARTITION_INDEX,
    ArtifactType.FITTED_PREPROCESSOR, ArtifactType.FITTED_MODEL,
    ArtifactType.PREDICTION, ArtifactType.PREDICTIVE_EXPLANATION,
    ArtifactType.MODEL_CARD,
)


def _ids() -> dict[str, str]:
    return {name: str(uuid.uuid4()) for name in ("project", "dataset", "source", "execution", "stage")}


def _seed(engine, ids: dict[str, str]) -> None:  # type: ignore[no-untyped-def]
    now = datetime.now(timezone.utc)
    with engine.begin() as c:
        c.execute(text("INSERT INTO product_project (project_id,name,status,created_at,updated_at) VALUES (:project,'g05','ACTIVE',:now,:now)"), {**ids, "now": now})
        c.execute(text("INSERT INTO product_artifact (artifact_id,project_id,artifact_type,object_key,content_hash,media_type,size_bytes,metadata_json,created_at) VALUES (:source,:project,'DATASET_FILE',:key,'hash','text/csv',1,'{}',:now)"), {**ids, "key": f"source/{ids['source']}", "now": now})
        c.execute(text("INSERT INTO product_dataset_version (dataset_version_id,project_id,source_artifact_id,dataset_key,name,version_label,content_hash,schema_json,profile_summary_json,row_count,column_count,created_at) VALUES (:dataset,:project,:source,'g05','g05','v1','hash','{}','{}',1,1,:now)"), {**ids, "now": now})
        c.execute(text("INSERT INTO product_execution (execution_id,project_id,dataset_version_id,batch_key,operation,analysis_family,analysis_spec_json,algorithm_or_estimator,parameter_json,code_version,runtime_version_json,snapshot_hash,status,retry_count,requested_by,requested_at) VALUES (:execution,:project,:dataset,:execution,'DISCOVERY','EXPLORATORY','{}','g05','{}','g05','{}','hash','QUEUED',0,'g05',:now)"), {**ids, "now": now})


def _cleanup(engine, ids: dict[str, str]) -> None:  # type: ignore[no-untyped-def]
    with engine.begin() as c:
        c.execute(text("DELETE FROM product_artifact WHERE execution_id=:execution"), ids)
        c.execute(text("DELETE FROM product_result WHERE execution_id=:execution"), ids)
        c.execute(text("DELETE FROM product_stage_execution WHERE execution_id=:execution"), ids)
        c.execute(text("DELETE FROM product_execution WHERE execution_id=:execution"), ids)
        c.execute(text("DELETE FROM product_dataset_version WHERE dataset_version_id=:dataset"), ids)
        c.execute(text("DELETE FROM product_artifact WHERE artifact_id=:source"), ids)
        c.execute(text("DELETE FROM product_project WHERE project_id=:project"), ids)


@pytest.mark.postgres
def test_g05_phase_a_family_output_types_round_trip(postgres_engine) -> None:  # type: ignore[no-untyped-def]
    ids = _ids(); _seed(postgres_engine, ids)
    try:
        stage = StageExecution(stage_execution_id=ids["stage"], execution_id=ids["execution"], stage_key="family")
        with Session(bind=postgres_engine) as session:
            SqlStageExecutionRepository(session).add(stage)
            session.flush()
            results = [Result(execution_id=ids["execution"], result_level=ResultLevel.STAGE_RESULT, stage_execution_id=ids["stage"], result_type=kind, scientific_status=status, summary_json={"schema_version": "family/1"}, payload_json={"typed": kind.value}, diagnostics_json={"status": status.value}, warning_json=[{"code": "kept"}]) for kind, status in _RESULTS]
            SqlResultRepository(session).add_many(results)
            artifacts = [Artifact(project_id=ids["project"], execution_id=ids["execution"], stage_execution_id=ids["stage"], result_id=results[index % len(results)].result_id, artifact_scope=ArtifactScope.EXECUTION_OUTPUT, artifact_type=kind, object_key=f"outputs/{ids['execution']}/{kind.value}", content_hash=kind.value, media_type="application/json", size_bytes=1, metadata_json={"schema_version": "artifact/1", "kind": kind.value}) for index, kind in enumerate(_ARTIFACTS)]
            SqlArtifactRepository(session).add_many(artifacts)
            session.commit()
        with Session(bind=postgres_engine) as session:
            loaded_results = SqlResultRepository(session).list_by_execution(ids["execution"])
            loaded_artifacts = SqlArtifactRepository(session).list_by_execution(ids["execution"])
        assert {(row.result_type, row.scientific_status) for row in loaded_results} == set(_RESULTS)
        assert all(row.result_level is ResultLevel.STAGE_RESULT and row.stage_execution_id == ids["stage"] for row in loaded_results)
        assert all(row.summary_json["schema_version"] == "family/1" and row.payload_json["typed"] == row.result_type.value and row.diagnostics_json["status"] == row.scientific_status.value and row.warning_json == [{"code": "kept"}] for row in loaded_results)
        assert {row.artifact_type for row in loaded_artifacts} == set(_ARTIFACTS)
        assert all(row.execution_id == ids["execution"] and row.stage_execution_id == ids["stage"] and row.result_id for row in loaded_artifacts)
        assert all(row.object_key != row.artifact_id and row.metadata_json["schema_version"] == "artifact/1" for row in loaded_artifacts)
    finally:
        _cleanup(postgres_engine, ids)


def test_g05_phase_a_domain_rejects_invalid_family_result_status() -> None:
    with pytest.raises(InvalidAnalysisSpec):
        Result(result_type=ResultType.TRAINING_RESULT, scientific_status=ScientificStatus.PASS)
    with pytest.raises(ValueError):
        ResultType("NOT_A_RESULT")
    with pytest.raises(ValueError):
        ArtifactType("NOT_AN_ARTIFACT")


@pytest.mark.postgres
def test_g05_phase_a_postgres_constraints_reject_invalid_typed_values(postgres_engine) -> None:  # type: ignore[no-untyped-def]
    ids = _ids(); _seed(postgres_engine, ids)
    try:
        stage = StageExecution(stage_execution_id=ids["stage"], execution_id=ids["execution"], stage_key="family")
        with Session(bind=postgres_engine) as session:
            SqlStageExecutionRepository(session).add(stage); session.commit()
        with pytest.raises(IntegrityError):
            with postgres_engine.begin() as c:
                c.execute(text("INSERT INTO product_result (result_id,execution_id,result_level,stage_execution_id,result_type,scientific_status,summary_json,payload_json,diagnostics_json,warning_json,created_at) VALUES (:id,:execution,'STAGE_RESULT',:stage,'TRAINING_RESULT','PASS','{}','{}','{}','[]',now())"), {**ids, "id": str(uuid.uuid4())})
        with pytest.raises(IntegrityError):
            with postgres_engine.begin() as c:
                c.execute(text("INSERT INTO product_artifact (artifact_id,project_id,artifact_type,object_key,content_hash,media_type,size_bytes,metadata_json,created_at) VALUES (:id,:project,'NOT_AN_ARTIFACT',:key,'hash','text/plain',1,'{}',now())"), {**ids, "id": str(uuid.uuid4()), "key": f"invalid/{uuid.uuid4()}"})
    finally:
        _cleanup(postgres_engine, ids)
