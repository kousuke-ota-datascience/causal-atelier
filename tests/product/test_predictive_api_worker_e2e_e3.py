from __future__ import annotations

import uuid

import pytest
from sqlalchemy import select

from ariadne.interfaces.web_api import dependencies
from ariadne.product.application.predictive_workflow_service import PredictiveWorkflowService
from ariadne.product.persistence.orm_models import (
    FamilyExecutionOrm,
    FamilyStageExecutionOrm,
)


async def _workspace(client, predictive_spec_factory):  # type: ignore[no-untyped-def]
    project = await client.post("/api/v1/projects", json={"name": "G4 Predictive E2E"})
    assert project.status_code == 201
    project_id = project.json()["project_id"]
    rows = ["score,converted"] + [
        f"{score},{int(score >= 0)}" for score in range(-60, 60)
    ]
    dataset = await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={
            "file": (
                "predictive.csv",
                ("\n".join(rows) + "\n").encode(),
                "text/csv",
            )
        },
        data={
            "dataset_key": "predictive-e2e",
            "version_label": "v1",
            "name": "Predictive E2E",
        },
        headers={"Idempotency-Key": "g4-predictive-e2e"},
    )
    assert dataset.status_code == 201
    dataset_id = dataset.json()["dataset_version_id"]
    context = await client.post(
        f"/api/v1/projects/{project_id}/research-contexts",
        json={
            "context_key": "conversion",
            "problem_statement": "Predict conversion before intervention.",
            "research_questions": ["Who is likely to convert?"],
            "decision_context": {"action": "prioritize outreach"},
        },
    )
    assert context.status_code == 201
    context_id = context.json()["research_context_version_id"]
    fixed_context = await client.post(
        f"/api/v1/projects/{project_id}/research-contexts/{context_id}/fix"
    )
    assert fixed_context.status_code == 200

    family_spec = predictive_spec_factory()
    family_spec["split_spec"].update({"strategy": "STRATIFIED", "stratify": True})
    family_spec["preprocessing_spec"] = {
        "fit_partition": "TRAIN",
        "numeric_imputation": "MEAN",
        "scale_numeric": True,
        "categorical_encoding": "ONE_HOT",
    }
    family_spec["model_spec"] = {
        "model_id": "logistic_regression.v1",
        "parameters": {"iterations": 800, "learning_rate": 0.1, "l2": 0.001},
    }
    family_spec["tuning_spec"] = {
        "selection_partitions": ["TRAIN", "VALIDATION"]
    }
    specification = await client.post(
        f"/api/v1/projects/{project_id}/analysis-specifications",
        json={
            "schema_version": "analysis-specification/1",
            "specification_key": "conversion-model",
            "analysis_family": "PREDICTIVE",
            "research_context_version_id": context_id,
            "dataset_version_id": dataset_id,
            "analysis_view_id": None,
            "analysis_mode": "CONFIRMATORY",
            "family_spec_schema_version": "predictive-analysis-spec/1",
            "family_spec": family_spec,
            "warnings": [],
        },
    )
    assert specification.status_code == 201
    specification_id = specification.json()["analysis_specification_id"]
    fixed_specification = await client.post(
        f"/api/v1/projects/{project_id}/analysis-specifications/"
        f"{specification_id}/fix"
    )
    assert fixed_specification.status_code == 200
    return project_id, specification_id, family_spec


@pytest.mark.anyio
@pytest.mark.requirement("G4-PREDICTIVE-API-WORKER-E2E")
async def test_predictive_execution_plan_async_worker_results_artifacts_and_lineage(
    client, predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    project_id, specification_id, family_spec = await _workspace(
        client, predictive_spec_factory
    )
    capabilities = await client.get(
        f"/api/v1/projects/{project_id}/predictive/capabilities"
    )
    assert capabilities.status_code == 200
    assert capabilities.json()["training_available"] is True
    assert capabilities.json()["evaluation_available"] is True
    assert capabilities.json()["explanation_available"] is True
    assert capabilities.json()["model_card_available"] is True

    plan = await client.post(
        f"/api/v1/projects/{project_id}/execution-plans",
        json={"analysis_specification_id": specification_id},
    )
    assert plan.status_code == 201
    plan_body = plan.json()
    assert [stage["stage_key"] for stage in plan_body["stages"]] == [
        "split", "prepare", "train", "evaluate",
    ]
    assert "evaluation_bundle" not in plan_body["stages"][2]["input_contract"]
    plan_id = plan_body["execution_plan_id"]
    validation = await client.post(
        f"/api/v1/projects/{project_id}/execution-plans/{plan_id}/validate"
    )
    assert validation.status_code == 200
    assert validation.json()["execution_order"] == [
        "split", "prepare", "train", "evaluate",
    ]

    submitted = await client.post(
        f"/api/v1/projects/{project_id}/executions",
        json={
            "analysis_specification_id": specification_id,
            "execution_plan_id": plan_id,
            "seed": family_spec["split_spec"]["seed"],
        },
        headers={"X-User-Id": "g4-test"},
    )
    assert submitted.status_code == 202
    assert submitted.json()["status"] == "QUEUED"
    execution_id = submitted.json()["execution_id"]

    listed = await client.get(f"/api/v1/projects/{project_id}/executions")
    assert execution_id in {item["execution_id"] for item in listed.json()["items"]}
    worker = PredictiveWorkflowService(
        dependencies._get_session_factory(), dependencies._get_artifact_store()
    )
    token = str(uuid.uuid4())
    assert worker.claim_next(token, worker_id="g4-test-worker") == execution_id
    running = await client.get(
        f"/api/v1/projects/{project_id}/executions/{execution_id}"
    )
    assert running.json()["status"] == "RUNNING"
    worker.process_execution(execution_id, worker_token=token)

    completed = await client.get(
        f"/api/v1/projects/{project_id}/executions/{execution_id}"
    )
    assert completed.status_code == 200
    completed_body = completed.json()
    assert completed_body["status"] == "SUCCEEDED"
    stages = (await client.get(
        f"/api/v1/projects/{project_id}/executions/{execution_id}/stages"
    )).json()["items"]
    assert [stage["stage_key"] for stage in stages] == [
        "split", "prepare", "train", "evaluate",
    ]
    assert {stage["status"] for stage in stages} == {"SUCCEEDED"}
    assert all(stage["attempt_history"] for stage in stages)

    results = (await client.get(
        f"/api/v1/projects/{project_id}/executions/{execution_id}/results"
    )).json()["items"]
    by_type = {item["result_type"]: item for item in results}
    assert set(by_type) == {
        "SPLIT_RESULT", "TRAINING_RESULT", "EVALUATION_RESULT", "ERROR_ANALYSIS_RESULT",
    }
    assert by_type["TRAINING_RESULT"]["analytical_status"] in {
        "TRAINED", "TRAINED_WITH_WARNINGS",
    }
    assert by_type["EVALUATION_RESULT"]["analytical_status"] == "EVALUATED"
    metrics = by_type["EVALUATION_RESULT"]["payload"]["metrics"]
    assert {"roc_auc", "pr_auc", "log_loss", "brier", "calibration"} <= set(metrics)

    artifacts = (await client.get(
        f"/api/v1/projects/{project_id}/executions/{execution_id}/artifacts"
    )).json()["items"]
    artifacts_by_type = {item["artifact_type"]: item for item in artifacts}
    assert set(artifacts_by_type) == {
        "PARTITION_INDEX",
        "FITTED_PREPROCESSOR",
        "FITTED_MODEL",
        "PREDICTION",
    }
    artifact_schema_versions = {
        "PARTITION_INDEX": "partition-artifact/1",
        "FITTED_PREPROCESSOR": "fitted-preprocessor/1",
        "FITTED_MODEL": "fitted-model/1",
        "PREDICTION": "prediction-artifact/1",
    }
    for artifact_type, artifact in artifacts_by_type.items():
        assert artifact["analysis_family"] == "PREDICTIVE"
        assert artifact["family"] == "PREDICTIVE"
        assert artifact["artifact_type"] == artifact_type
        assert artifact["schema_version"] == artifact_schema_versions[artifact_type]
        assert artifact["media_type"] == "application/json"
        assert len(artifact["content_hash"]) == 64
        assert artifact["size_bytes"] > 0

    lineage = (await client.get(
        f"/api/v1/projects/{project_id}/executions/{execution_id}/lineage"
    )).json()["items"]
    lineage_edges = {
        (
            item["source_type"],
            item["source_id"],
            item["relation_type"],
            item["target_type"],
            item["target_id"],
        )
        for item in lineage
    }
    lineage_node_types = {
        node_type
        for edge in lineage_edges
        for node_type in (edge[0], edge[3])
    }
    assert "ResearchContextVersion" in lineage_node_types
    assert "DatasetVersion" in lineage_node_types
    assert "AnalysisView" not in lineage_node_types
    assert "ExecutionPlan" in lineage_node_types
    assert "Result" in lineage_node_types
    snapshot = completed_body["snapshot"]
    assert (
        "ResearchContextVersion",
        snapshot["research_context"]["id"],
        "USED_INPUT",
        "Execution",
        execution_id,
    ) in lineage_edges
    assert (
        "DatasetVersion",
        snapshot["dataset_version"]["id"],
        "USED_INPUT",
        "Execution",
        execution_id,
    ) in lineage_edges
    assert snapshot["analysis_view"]["id"] is None
    assert (
        "AnalysisSpecification",
        specification_id,
        "USED_INPUT",
        "Execution",
        execution_id,
    ) in lineage_edges
    assert (
        "ExecutionPlan",
        plan_id,
        "USED_INPUT",
        "Execution",
        execution_id,
    ) in lineage_edges

    split_result_id = by_type["SPLIT_RESULT"]["result_id"]
    training_result_id = by_type["TRAINING_RESULT"]["result_id"]
    evaluation_result_id = by_type["EVALUATION_RESULT"]["result_id"]
    error_result_id = by_type["ERROR_ANALYSIS_RESULT"]["result_id"]
    partition_artifact_id = artifacts_by_type["PARTITION_INDEX"]["artifact_id"]
    preprocessor_artifact_id = artifacts_by_type["FITTED_PREPROCESSOR"]["artifact_id"]
    model_artifact_id = artifacts_by_type["FITTED_MODEL"]["artifact_id"]
    prediction_artifact_id = artifacts_by_type["PREDICTION"]["artifact_id"]
    for result_id in (
        split_result_id,
        training_result_id,
        evaluation_result_id,
        error_result_id,
    ):
        assert (
            "Execution",
            execution_id,
            "GENERATED",
            "Result",
            result_id,
        ) in lineage_edges
    assert (
        "Result",
        split_result_id,
        "GENERATED",
        "Artifact",
        partition_artifact_id,
    ) in lineage_edges
    assert (
        "Execution",
        execution_id,
        "GENERATED",
        "Artifact",
        preprocessor_artifact_id,
    ) in lineage_edges
    assert (
        "Result",
        training_result_id,
        "GENERATED",
        "Artifact",
        model_artifact_id,
    ) in lineage_edges
    assert (
        "Result",
        evaluation_result_id,
        "GENERATED",
        "Artifact",
        prediction_artifact_id,
    ) in lineage_edges
    assert (
        "Artifact",
        preprocessor_artifact_id,
        "DERIVED_FROM",
        "Artifact",
        partition_artifact_id,
    ) in lineage_edges
    assert (
        "Artifact",
        model_artifact_id,
        "DERIVED_FROM",
        "Artifact",
        preprocessor_artifact_id,
    ) in lineage_edges
    assert (
        "Artifact",
        prediction_artifact_id,
        "DERIVED_FROM",
        "Artifact",
        model_artifact_id,
    ) in lineage_edges
    assert (
        "Artifact",
        prediction_artifact_id,
        "EVIDENCE_FOR",
        "Result",
        evaluation_result_id,
    ) in lineage_edges

    prefill = await client.get(
        f"/api/v1/projects/{project_id}/executions/{execution_id}/prefill"
    )
    assert prefill.json()["analysis_specification_id"] == specification_id
    rerun = await client.post(
        f"/api/v1/projects/{project_id}/executions/{execution_id}/rerun"
    )
    assert rerun.status_code == 202
    assert rerun.json()["status"] == "QUEUED"
    cancelled = await client.post(
        f"/api/v1/projects/{project_id}/executions/"
        f"{rerun.json()['execution_id']}/cancel"
    )
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "CANCELLED"


@pytest.mark.anyio
@pytest.mark.requirement("G4-PREDICTIVE-RETRY-CONTRACT")
async def test_failed_predictive_execution_retry_resets_and_can_succeed(
    client, predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    project_id, specification_id, family_spec = await _workspace(
        client, predictive_spec_factory
    )
    plan = await client.post(
        f"/api/v1/projects/{project_id}/execution-plans",
        json={"analysis_specification_id": specification_id},
    )
    assert plan.status_code == 201
    submitted = await client.post(
        f"/api/v1/projects/{project_id}/executions",
        json={
            "analysis_specification_id": specification_id,
            "execution_plan_id": plan.json()["execution_plan_id"],
            "seed": family_spec["split_spec"]["seed"],
        },
    )
    assert submitted.status_code == 202
    execution_id = submitted.json()["execution_id"]

    factory = dependencies._get_session_factory()
    with factory() as session:
        execution = session.get(FamilyExecutionOrm, execution_id)
        assert execution is not None
        execution.status = "FAILED"
        execution.last_error_json = {
            "type": "SyntheticFailure",
            "message": "retry contract fixture",
        }
        first_stage = session.scalar(
            select(FamilyStageExecutionOrm)
            .where(FamilyStageExecutionOrm.execution_id == execution_id)
            .order_by(FamilyStageExecutionOrm.ordinal)
        )
        assert first_stage is not None
        first_stage.status = "FAILED"
        first_stage.last_error_json = execution.last_error_json
        first_stage.attempt_history_json = [{"attempt_number": 1}]
        first_stage.input_binding_json = {"fixture": True}
        first_stage.output_binding_json = {"fixture": True}
        session.commit()

    retry = await client.post(
        f"/api/v1/projects/{project_id}/executions/{execution_id}/retry"
    )
    assert retry.status_code == 200
    assert retry.json()["execution_id"] == execution_id
    assert retry.json()["status"] == "QUEUED"
    assert retry.json()["retry_count"] == 1
    assert retry.json()["last_error"] is None
    reset_stages = (await client.get(
        f"/api/v1/projects/{project_id}/executions/{execution_id}/stages"
    )).json()["items"]
    assert {stage["status"] for stage in reset_stages} == {"PENDING"}
    assert all(stage["attempt_history"] == [] for stage in reset_stages)
    assert all(stage["input_binding"] == {} for stage in reset_stages)
    assert all(stage["output_binding"] == {} for stage in reset_stages)
    assert all(stage["last_error"] is None for stage in reset_stages)

    worker = PredictiveWorkflowService(
        dependencies._get_session_factory(), dependencies._get_artifact_store()
    )
    token = str(uuid.uuid4())
    assert worker.claim_next(token, worker_id="g4-retry-worker") == execution_id
    worker.process_execution(execution_id, worker_token=token)
    completed = await client.get(
        f"/api/v1/projects/{project_id}/executions/{execution_id}"
    )
    assert completed.status_code == 200
    assert completed.json()["status"] == "SUCCEEDED"
    assert completed.json()["retry_count"] == 1


@pytest.mark.anyio
@pytest.mark.requirement("G4-PREDICTIVE-SNAPSHOT-CONTRACT")
async def test_execution_rejects_seed_different_from_fixed_specification(
    client, predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    project_id, specification_id, family_spec = await _workspace(
        client, predictive_spec_factory
    )
    plan = await client.post(
        f"/api/v1/projects/{project_id}/execution-plans",
        json={"analysis_specification_id": specification_id},
    )
    response = await client.post(
        f"/api/v1/projects/{project_id}/executions",
        json={
            "analysis_specification_id": specification_id,
            "execution_plan_id": plan.json()["execution_plan_id"],
            "seed": family_spec["split_spec"]["seed"] + 1,
        },
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "SEED_SPECIFICATION_MISMATCH"
