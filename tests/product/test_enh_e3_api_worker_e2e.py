from __future__ import annotations

from pathlib import Path

import pytest

from ariadne.interfaces.web_api import dependencies
from ariadne.interfaces.worker.execution_processor import ExecutionProcessor
from ariadne.product.domain.enums import ResultType, ScientificStatus
from ariadne.product.ports.scientific_core import ScientificResultDescriptor
from ariadne.scientific.core_adapter import ScientificCoreAdapter


class FinalE2ECausalCore:
    def run_discovery(self, input_, output_dir: Path):  # type: ignore[no-untyped-def]
        return [ScientificResultDescriptor(
            result_type=ResultType.DISCOVERY_GRAPH_RESULT,
            scientific_status=ScientificStatus.GENERATED,
            summary={"node_count": 2, "edge_count": 1},
            payload={
                "graph_type": "DAG", "nodes": ["score", "converted"],
                "edges": [{
                    "source": "score", "target": "converted",
                    "endpoint_source": "TAIL", "endpoint_target": "ARROW",
                }],
            },
        )]


def _process_canonical(execution_id: str, worker_id: str, core) -> None:  # type: ignore[no-untyped-def]
    with dependencies._uow_context() as uow:
        claimed = uow.executions.claim_next(worker_id, worker_id=worker_id)
        uow.commit()
    assert claimed is not None and claimed.execution_id == execution_id
    ExecutionProcessor(
        dependencies._uow_context, core, dependencies._get_artifact_store(),
        owner_token=worker_id,
    ).process(claimed)


def _predictive_spec(factory) -> dict:  # type: ignore[no-untyped-def]
    spec = factory()
    spec["split_spec"].update({"strategy": "STRATIFIED", "stratify": True})
    spec["preprocessing_spec"] = {
        "fit_partition": "TRAIN", "numeric_imputation": "MEAN",
        "scale_numeric": True, "categorical_encoding": "ONE_HOT",
    }
    spec["model_spec"] = {
        "model_id": "logistic_regression.v1",
        "parameters": {"iterations": 800, "learning_rate": .1, "l2": .001},
    }
    spec["tuning_spec"] = {"selection_partitions": ["TRAIN", "VALIDATION"]}
    spec["explanation_spec"] = {
        "method": "LINEAR_COEFFICIENT_CONTRIBUTION", "dataset": "TEST",
        "sampling": {"strategy": "FIRST_N", "size": 5, "seed": 17},
        "local_explanations": True,
    }
    return spec


@pytest.mark.anyio
@pytest.mark.requirement("G6-FULL-PRODUCT-E2E")
async def test_research_context_to_cross_family_results_lineage_annotation_and_export(
    client, predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    project = await client.post("/api/v1/projects", json={
        "name": "ENH-E3 final", "topic": "conversion and intervention",
        "objective": "Explore, predict, and generate a causal hypothesis",
        "memo": "G6 final product E2E",
    })
    assert project.status_code == 201
    project_id = project.json()["project_id"]
    rows = ["score,converted"] + [f"{score},{int(score >= 0)}" for score in range(-60, 60)]
    dataset = await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={"file": ("final.csv", ("\n".join(rows) + "\n").encode(), "text/csv")},
        data={"dataset_key": "final", "version_label": "v1", "name": "Final E2E"},
        headers={"Idempotency-Key": "g6-final-dataset"},
    )
    assert dataset.status_code == 201
    dataset_id = dataset.json()["dataset_version_id"]

    context = await client.post(
        f"/api/v1/projects/{project_id}/research-contexts",
        json={
            "context_key": "conversion", "problem_statement": "Predict conversion before action.",
            "research_questions": ["Who is likely to convert?", "What intervention merits causal study?"],
            "significance": "Allocate outreach while preserving causal uncertainty.",
            "hypotheses": ["Score predicts conversion."],
            "decision_context": {"action": "prioritize and design a causal follow-up"},
            "relations": [],
        },
    )
    context_id = context.json()["research_context_version_id"]
    fixed_context = await client.post(
        f"/api/v1/projects/{project_id}/research-contexts/{context_id}/fix"
    )
    assert fixed_context.status_code == 200
    immutable = await client.patch(
        f"/api/v1/projects/{project_id}/research-contexts/{context_id}",
        json={"problem_statement": "overwrite"},
    )
    assert immutable.status_code == 409
    assert immutable.json()["error"]["code"] == "RESOURCE_IMMUTABLE"

    view_spec = {
        "schema_version": "analysis-view/1", "source_dataset_version_id": dataset_id,
        "row_filter": [], "selected_columns": ["score", "converted"],
        "derived_columns": [], "missing_value_policy": {"default": "KEEP", "columns": {}},
        "time_cutoff": None, "sampling": None,
    }
    view = await client.post(
        f"/api/v1/projects/{project_id}/analysis-views",
        json={"view_key": "final", "name": "Final population", "spec": view_spec},
    )
    view_id = view.json()["analysis_view_id"]
    assert (await client.post(
        f"/api/v1/projects/{project_id}/analysis-views/{view_id}/validate"
    )).status_code == 200
    assert (await client.post(
        f"/api/v1/projects/{project_id}/analysis-views/{view_id}/fix"
    )).json()["status"] == "FIXED"
    workspace = await client.put(
        f"/api/v1/projects/{project_id}/workspace-state",
        json={
            "research_context_version_id": context_id,
            "dataset_version_id": dataset_id, "analysis_view_id": view_id,
            "unsaved_draft": False,
        },
    )
    assert workspace.json()["current_role"] == "OWNER"

    exploration_request = {
        "dataset_version_id": dataset_id, "analysis_view_id": view_id,
        "family_spec": {
            "schema_version": "exploratory-analysis-spec/1", "operation": "ASSOCIATION",
            "columns": ["score", "converted"], "grouping": [],
            "aggregation": {"method": "COUNT", "column": None},
            "chart_encoding": {"mark": "point", "x": "score", "y": "converted"},
            "filter": None, "sampling": None, "expected_output_type": None,
        },
    }
    submitted_explore = await client.post(
        f"/api/v1/projects/{project_id}/exploration/executions",
        json=exploration_request,
    )
    explore_execution_id = submitted_explore.json()["execution_id"]
    _process_canonical(explore_execution_id, "g6-explore", ScientificCoreAdapter())
    explore_result = (await client.get(
        f"/api/v1/projects/{project_id}/exploration/results"
    )).json()["items"][0]
    assert explore_result["analysis_family"] == "EXPLORATORY"

    family_spec = _predictive_spec(predictive_spec_factory)
    specification = await client.post(
        f"/api/v1/projects/{project_id}/analysis-specifications",
        json={
            "schema_version": "analysis-specification/1",
            "specification_key": "final-predictive", "analysis_family": "PREDICTIVE",
            "research_context_version_id": context_id, "dataset_version_id": dataset_id,
            "analysis_view_id": view_id, "analysis_mode": "CONFIRMATORY",
            "family_spec_schema_version": "predictive-analysis-spec/1",
            "family_spec": family_spec, "warnings": [],
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
    predictive_execution = await client.post(
        f"/api/v1/projects/{project_id}/executions",
        json={
            "analysis_specification_id": specification_id,
            "execution_plan_id": plan.json()["execution_plan_id"], "seed": 17,
        },
        headers={"Idempotency-Key": "g6-predictive"},
    )
    predictive_execution_id = predictive_execution.json()["execution_id"]
    _process_canonical(predictive_execution_id, "g6-predictive", ScientificCoreAdapter())
    predictive_results = (await client.get(
        f"/api/v1/projects/{project_id}/executions/{predictive_execution_id}/results"
    )).json()["items"]
    predictive_by_type = {item["result_type"]: item for item in predictive_results}
    assert {"EVALUATION_RESULT", "PREDICTIVE_EXPLANATION_RESULT", "MODEL_CARD_RESULT"} <= set(predictive_by_type)
    evaluation_result_id = predictive_by_type["EVALUATION_RESULT"]["result_id"]

    causal_spec = {
        "schema_version": "causal-analysis-spec/2", "analysis_mode": "EXPLORATORY",
        "research_context": {"problem_statement": "Generated from predictive follow-up."},
        "causal_question": {}, "causal_design": {"adjustment_set": [], "assumptions": []},
        "operation_spec": {
            "feature_columns": ["score", "converted"], "designated_outcome_node": "converted",
            "constraints": {"required_edges": [], "forbidden_edges": [], "temporal_tiers": []},
            "expected_graph_type": None,
        }, "validation_override": None,
    }
    causal = await client.post(
        f"/api/v1/projects/{project_id}/execution-batches",
        json={
            "operation": "DISCOVERY", "dataset_version_id": dataset_id,
            "input_graph_version_id": None, "input_result_id": None,
            "objective": "Generate a causal hypothesis", "rationale": "Predictive follow-up",
            "analysis_spec": causal_spec,
            "variants": [{"algorithm_or_estimator": "pc", "parameters": {"alpha": .05}, "random_seed": 42}],
            "code_version": "g6-e2e", "runtime_versions": {"test": "g6"},
        },
        headers={"Idempotency-Key": "g6-causal"},
    )
    assert causal.status_code == 202
    causal_execution_id = causal.json()["executions"][0]["execution_id"]
    with dependencies._uow_context() as uow:
        claimed = uow.executions.claim_next("g6-causal-worker")
        uow.commit()
    assert claimed is not None and claimed.execution_id == causal_execution_id
    ExecutionProcessor(
        dependencies._uow_context, FinalE2ECausalCore(), dependencies._get_artifact_store()
    ).process(claimed)
    causal_results = (await client.get(
        f"/api/v1/executions/{causal_execution_id}/results"
    )).json()["items"]
    causal_result_id = causal_results[0]["result_id"]

    for source_id, target_type, target_id, statement in (
        (explore_result["result_id"], "AnalysisSpecification", specification_id, "Exploration motivated prediction."),
        (evaluation_result_id, "Execution", causal_execution_id, "Prediction generated a causal hypothesis."),
    ):
        link = await client.post(
            f"/api/v1/projects/{project_id}/lineage-links",
            json={
                "source_type": "Result", "source_id": source_id,
                "relation_type": "MOTIVATED", "target_type": target_type,
                "target_id": target_id, "evidence": {"statement": statement},
            },
        )
        assert link.status_code == 201

    unified = (await client.get(
        f"/api/v1/projects/{project_id}/results"
    )).json()["items"]
    assert {item["analysis_family"] for item in unified} == {
        "EXPLORATORY", "PREDICTIVE", "CAUSAL"
    }
    annotation = await client.post(
        f"/api/v1/projects/{project_id}/workspace-annotations",
        json={
            "target_type": "Result", "target_id": evaluation_result_id,
            "statement": "Use prediction for prioritization, not causal claims.",
            "rationale": "Held-out evaluation passed.", "assumptions": [],
            "limitations": ["Predictive Explanation is not a Causal Explanation."],
            "decision": "SELECTED", "next_actions": ["Review causal hypothesis"],
        },
        headers={"Idempotency-Key": "g6-workspace-annotation"},
    )
    assert annotation.status_code == 201
    exported = await client.post(
        f"/api/v1/projects/{project_id}/exports",
        json={"result_ids": [explore_result["result_id"], evaluation_result_id, causal_result_id]},
        headers={"Idempotency-Key": "g6-export"},
    )
    assert exported.status_code == 201
    assert exported.json()["manifest_summary"]["result_count"] == 3
    lineage = (await client.get(
        f"/api/v1/projects/{project_id}/lineage"
    )).json()
    explicit_motivations = [
        item for item in lineage["edges"]
        if item["relation_type"] == "MOTIVATED" and item["explicit"]
    ]
    assert len(explicit_motivations) == 2


def test_g6_frontend_closes_context_common_selectors_results_and_canonical_analysis_routes() -> None:
    root = Path(__file__).parents[2]
    html = (root / "frontend" / "index.html").read_text(encoding="utf-8")
    javascript = (root / "frontend" / "app.js").read_text(encoding="utf-8")
    navigation = (root / "frontend" / "navigation_state.js").read_text(encoding="utf-8")
    assert 'data-top-level-surface-root="analysis"' in html
    assert 'id="analysis-family-tabs"' in html
    assert 'id="analysis-stage-sidebar"' in html
    for route in ("explore", "causal", "predictive"):
        assert f'data-route="{route}"' not in html
    for legacy, family in (("explore", "exploratory"), ("causal", "causal"), ("predictive", "predictive")):
        assert f'{legacy}: ["{family}",' in navigation
    assert "function serialize(context)" in navigation
    for field in (
        'id="analysis-context-project-name"', 'id="common-context"', 'id="common-dataset"',
        'id="common-view"', 'id="common-role"', 'id="common-selection-status"',
        'id="research-context-form"', 'id="research-context-history"',
        'id="result-family-filter"', 'id="compare-results"',
        'id="show-project-lineage"', 'id="annotation-form"',
    ):
        assert field in html
    for contract in (
        "/workspace-state", "/workspace-annotations", "/results/summary",
        "/comparisons", "/lineage", "/exports",
        "Cross-family metrics are not normalized or ranked",
        "window.addEventListener('popstate'",
    ):
        assert contract in javascript or contract in (root / "src" / "ariadne" / "product" / "application" / "product_closure_service.py").read_text(encoding="utf-8")
