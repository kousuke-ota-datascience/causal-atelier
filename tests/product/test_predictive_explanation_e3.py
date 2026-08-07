from __future__ import annotations

import uuid

import pandas as pd
import pytest

from ariadne.capabilities.predictive import (
    PredictivePlanner,
    SUPPORTED_EXPLANATION_METHOD,
    register_predictive_explain_runner,
    register_predictive_split_runner,
    register_predictive_training_runners,
    validate_predictive_specification,
)
from ariadne.interfaces.web_api import dependencies
from ariadne.product.application.predictive_workflow_service import (
    PredictiveWorkflowService,
)
from ariadne.product.domain.errors import InvalidSchema, PredictiveValidationError
from ariadne.product.workflow.executor import GenericExecutor
from ariadne.product.workflow.plan_validator import PlanValidator
from ariadne.product.workflow.runner_registry import StageRunnerRegistry


def _registry() -> StageRunnerRegistry:
    registry = StageRunnerRegistry()
    register_predictive_split_runner(registry)
    register_predictive_training_runners(registry)
    register_predictive_explain_runner(registry)
    return registry


def _frame() -> pd.DataFrame:
    scores = list(range(-60, 60))
    return pd.DataFrame({
        "score": scores,
        "converted": [int(score >= 0) for score in scores],
    })


def _spec(predictive_spec_factory, method: str) -> dict:  # type: ignore[no-untyped-def,type-arg]
    spec = predictive_spec_factory()
    spec["split_spec"].update({"strategy": "STRATIFIED", "stratify": True})
    spec["preprocessing_spec"] = {
        "fit_partition": "TRAIN",
        "numeric_imputation": "MEAN",
        "scale_numeric": True,
        "categorical_encoding": "ONE_HOT",
    }
    spec["model_spec"] = {
        "model_id": "logistic_regression.v1",
        "parameters": {"iterations": 800, "learning_rate": 0.1, "l2": 0.001},
    }
    spec["tuning_spec"] = {"selection_partitions": ["TRAIN", "VALIDATION"]}
    spec["explanation_spec"] = {
        "method": method,
        "dataset": "TEST",
        "sampling": {"strategy": "FIRST_N", "size": 5, "seed": 17},
        "local_explanations": True,
    }
    return spec


def _execute(spec: dict) -> object:  # type: ignore[type-arg]
    plan = PredictivePlanner().build_full_plan(
        project_id="project",
        specification_id="fixed-specification",
        family_spec=spec,
    )
    PlanValidator(_registry()).validate(plan)
    return GenericExecutor(_registry()).execute(
        "execution",
        plan,
        external_inputs={
            "split": {
                "frame": _frame(),
                "source_snapshot": {
                    "schema_version": "predictive-source-snapshot/1",
                    "dataset_version_id": "dataset",
                    "dataset_content_hash": "a" * 64,
                    "analysis_view_id": None,
                    "analysis_view_hash": None,
                    "materialized_hash": "a" * 64,
                },
            },
            "prepare": {"frame": _frame()},
        },
        snapshots={
            "versions": {
                "code": "ariadne/0.1.0",
                "python": "3.12",
                "schemas": ["predictive-analysis-spec/1"],
            }
        },
    )


@pytest.mark.requirement("G5-PREDICTIVE-EXPLANATION-SPECIFICATION")
def test_explanation_specification_is_explicit_strict_and_test_only(
    predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    supported = _spec(predictive_spec_factory, SUPPORTED_EXPLANATION_METHOD)
    assert validate_predictive_specification(supported)["explanation_spec"] == (
        supported["explanation_spec"]
    )

    unknown = _spec(predictive_spec_factory, SUPPORTED_EXPLANATION_METHOD)
    unknown["explanation_spec"]["unknown"] = True
    with pytest.raises(InvalidSchema, match="Unknown explanation_spec fields"):
        validate_predictive_specification(unknown)

    validation = _spec(predictive_spec_factory, SUPPORTED_EXPLANATION_METHOD)
    validation["explanation_spec"]["dataset"] = "VALIDATION"
    with pytest.raises(PredictiveValidationError) as captured:
        validate_predictive_specification(validation)
    assert captured.value.code == "EXPLANATION_DATASET_UNSUPPORTED"
    assert captured.value.path == "explanation_spec.dataset"

    invalid_sampling = _spec(
        predictive_spec_factory, SUPPORTED_EXPLANATION_METHOD
    )
    invalid_sampling["explanation_spec"]["sampling"]["size"] = 0
    with pytest.raises(InvalidSchema, match="integer in"):
        validate_predictive_specification(invalid_sampling)


@pytest.mark.requirement("G5-PREDICTIVE-EXPLANATION")
def test_registered_explain_stage_generates_deterministic_global_and_local_explanations(
    predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    spec = _spec(predictive_spec_factory, SUPPORTED_EXPLANATION_METHOD)
    plan = PredictivePlanner().build_full_plan(
        project_id="project",
        specification_id="fixed-specification",
        family_spec=spec,
    )
    assert [stage.stage_key for stage in plan.stages] == [
        "split", "prepare", "train", "evaluate", "explain",
    ]
    explain = plan.stages[-1]
    assert explain.stage_type.as_dict() == {
        "namespace": "predictive", "name": "explain", "version": "1",
    }
    assert set(explain.input_contract) == {
        "frozen_model",
        "fitted_preprocessor",
        "explanation_dataset",
        "explanation_specification",
        "sampling_definition",
        "training_summary",
        "evaluation_summary",
        "partition_manifest",
    }

    first = _execute(spec)
    second = _execute(spec)
    assert first.status == "SUCCEEDED"
    by_type = {result.result_type: result for result in first.results}
    explanation = by_type["PREDICTIVE_EXPLANATION_RESULT"]
    assert explanation.analytical_status == "GENERATED"
    assert explanation.payload["explanation_method"] == SUPPORTED_EXPLANATION_METHOD
    assert explanation.payload["explanation_dataset_provenance"]["partition"] == "TEST"
    assert explanation.payload["sampling"] == {
        "strategy": "FIRST_N",
        "size": 5,
        "seed": 17,
        "available_sample_count": 24,
        "selected_sample_count": 5,
    }
    assert explanation.payload["background_reference_data"]["partition"] == "TRAIN"
    assert explanation.payload["background_reference_data"]["sample_count"] == 72
    assert explanation.payload["model_output_scale"] == "LOG_ODDS"
    assert explanation.payload["prediction_output_scale"] == "PROBABILITY"
    assert explanation.payload["global_explanation"][0]["feature"] == "score"
    assert len(explanation.payload["local_explanation"]) == 5
    local = explanation.payload["local_explanation"][0]
    assert local["linear_output"] == pytest.approx(
        local["base_value"]
        + sum(
            item["contribution_to_model_output"]
            for item in local["feature_contributions"]
        )
    )
    assert local["model_output"] == pytest.approx(local["linear_output"])
    assert 0.0 <= local["prediction"] <= 1.0
    assert explanation.diagnostics == {
        "predictive_not_causal": True,
        "selection_allowed": False,
    }
    assert (
        "Predictive Explanation is not a Causal Explanation or Treatment Effect."
        in explanation.payload["limitations"]
    )
    second_explanation = next(
        result
        for result in second.results
        if result.result_type == "PREDICTIVE_EXPLANATION_RESULT"
    )
    assert second_explanation.payload == explanation.payload


@pytest.mark.requirement("G5-PREDICTIVE-EXPLANATION-WARNINGS")
def test_local_explanation_sample_shortfall_is_explicit(
    predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    spec = _spec(predictive_spec_factory, SUPPORTED_EXPLANATION_METHOD)
    spec["explanation_spec"]["sampling"]["size"] = 1000
    outcome = _execute(spec)
    explanation = next(
        result
        for result in outcome.results
        if result.result_type == "PREDICTIVE_EXPLANATION_RESULT"
    )
    assert explanation.analytical_status == "GENERATED_WITH_WARNINGS"
    assert explanation.payload["sampling"]["selected_sample_count"] == 24
    assert explanation.warnings[0]["code"] == "EXPLANATION_SAMPLE_TRUNCATED"


@pytest.mark.requirement("G5-MODEL-CARD", "G5-EXPLANATION-NOT-APPLICABLE")
def test_model_card_is_complete_and_unsupported_method_returns_not_applicable(
    predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    outcome = _execute(_spec(predictive_spec_factory, "UNSUPPORTED_METHOD"))
    by_type = {result.result_type: result for result in outcome.results}
    explanation = by_type["PREDICTIVE_EXPLANATION_RESULT"]
    model_card = by_type["MODEL_CARD_RESULT"]
    assert explanation.analytical_status == "NOT_APPLICABLE"
    assert explanation.payload["global_explanation"] is None
    assert explanation.payload["local_explanation"] == []
    assert explanation.warnings[0]["code"] == "EXPLANATION_METHOD_NOT_APPLICABLE"
    assert model_card.analytical_status == "GENERATED_WITH_WARNINGS"
    assert set(model_card.payload) == {
        "schema_version",
        "intended_use",
        "deployment_population",
        "training_data",
        "feature_set",
        "split_strategy",
        "model_descriptor",
        "selected_hyperparameters",
        "validation_metrics",
        "test_metrics",
        "limitations",
        "warnings",
        "code_runtime_metadata",
    }
    assert model_card.payload["training_data"]["training_partition"] == "TRAIN"
    assert model_card.payload["split_strategy"]["strategy"] == "STRATIFIED"
    assert model_card.payload["selected_hyperparameters"]["iterations"] == 800
    assert model_card.payload["validation_metrics"]["sample_count"] == 24
    assert model_card.payload["test_metrics"]["sample_count"] == 24
    assert model_card.payload["code_runtime_metadata"]["code"] == "ariadne/0.1.0"
    assert (
        "Predictive Explanation is not a Causal Explanation or Treatment Effect."
        in model_card.payload["limitations"]
    )


@pytest.mark.anyio
@pytest.mark.requirement("G5-PREDICTIVE-EXPLANATION-PERSISTENCE-LINEAGE")
async def test_api_worker_persists_explanation_model_card_artifacts_and_lineage(
    client, predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    project = await client.post(
        "/api/v1/projects", json={"name": "G5 Predictive Explain"}
    )
    project_id = project.json()["project_id"]
    rows = ["score,converted"] + [
        f"{score},{int(score >= 0)}" for score in range(-60, 60)
    ]
    dataset = await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={"file": ("g5.csv", ("\n".join(rows) + "\n").encode(), "text/csv")},
        data={"dataset_key": "g5", "version_label": "v1", "name": "G5"},
        headers={"Idempotency-Key": "g5-explain"},
    )
    dataset_id = dataset.json()["dataset_version_id"]
    context = await client.post(
        f"/api/v1/projects/{project_id}/research-contexts",
        json={
            "context_key": "g5",
            "problem_statement": "Predict conversion.",
            "research_questions": ["Who is likely to convert?"],
            "decision_context": {"action": "prioritize outreach"},
        },
    )
    context_id = context.json()["research_context_version_id"]
    assert (await client.post(
        f"/api/v1/projects/{project_id}/research-contexts/{context_id}/fix"
    )).status_code == 200
    family_spec = _spec(predictive_spec_factory, SUPPORTED_EXPLANATION_METHOD)
    specification = await client.post(
        f"/api/v1/projects/{project_id}/analysis-specifications",
        json={
            "schema_version": "analysis-specification/1",
            "specification_key": "g5-model",
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
    specification_id = specification.json()["analysis_specification_id"]
    assert (await client.post(
        f"/api/v1/projects/{project_id}/analysis-specifications/{specification_id}/fix"
    )).status_code == 200
    plan = await client.post(
        f"/api/v1/projects/{project_id}/execution-plans",
        json={"analysis_specification_id": specification_id},
    )
    assert [stage["stage_key"] for stage in plan.json()["stages"]] == [
        "split", "prepare", "train", "evaluate", "explain",
    ]
    execution = await client.post(
        f"/api/v1/projects/{project_id}/executions",
        json={
            "analysis_specification_id": specification_id,
            "execution_plan_id": plan.json()["execution_plan_id"],
            "seed": family_spec["split_spec"]["seed"],
        },
    )
    execution_id = execution.json()["execution_id"]
    worker = PredictiveWorkflowService(
        dependencies._get_session_factory(), dependencies._get_artifact_store()
    )
    token = str(uuid.uuid4())
    assert worker.claim_next(token, worker_id="g5-test-worker") == execution_id
    worker.process_execution(execution_id, worker_token=token)
    assert (await client.get(
        f"/api/v1/projects/{project_id}/executions/{execution_id}"
    )).json()["status"] == "SUCCEEDED"

    results = (await client.get(
        f"/api/v1/projects/{project_id}/executions/{execution_id}/results"
    )).json()["items"]
    results_by_type = {result["result_type"]: result for result in results}
    assert results_by_type["PREDICTIVE_EXPLANATION_RESULT"]["analytical_status"] == "GENERATED"
    assert results_by_type["MODEL_CARD_RESULT"]["analytical_status"] == "GENERATED"
    artifacts = (await client.get(
        f"/api/v1/projects/{project_id}/executions/{execution_id}/artifacts"
    )).json()["items"]
    artifacts_by_type = {
        artifact["artifact_type"]: artifact for artifact in artifacts
    }
    assert artifacts_by_type["PREDICTIVE_EXPLANATION"]["result_id"] == (
        results_by_type["PREDICTIVE_EXPLANATION_RESULT"]["result_id"]
    )
    assert artifacts_by_type["MODEL_CARD"]["result_id"] == (
        results_by_type["MODEL_CARD_RESULT"]["result_id"]
    )
    lineage = (await client.get(
        f"/api/v1/projects/{project_id}/executions/{execution_id}/lineage"
    )).json()["items"]
    edges = {
        (
            item["source_type"],
            item["source_id"],
            item["relation_type"],
            item["target_type"],
            item["target_id"],
        )
        for item in lineage
    }
    model_card_id = results_by_type["MODEL_CARD_RESULT"]["result_id"]
    explanation_id = results_by_type["PREDICTIVE_EXPLANATION_RESULT"]["result_id"]
    assert (
        "Result", model_card_id, "DOCUMENTS", "AnalysisSpecification", specification_id,
    ) in edges
    assert (
        "Result", model_card_id, "DOCUMENTS", "DatasetVersion", dataset_id,
    ) in edges
    assert (
        "Result",
        model_card_id,
        "SUMMARIZES",
        "Result",
        results_by_type["EVALUATION_RESULT"]["result_id"],
    ) in edges
    assert (
        "Artifact",
        artifacts_by_type["FITTED_MODEL"]["artifact_id"],
        "USED_INPUT",
        "Result",
        explanation_id,
    ) in edges
    assert (
        "Artifact",
        artifacts_by_type["PREDICTIVE_EXPLANATION"]["artifact_id"],
        "EVIDENCE_FOR",
        "Result",
        explanation_id,
    ) in edges
