from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest

from ariadne.interfaces.web_api import dependencies
from ariadne.product.persistence.orm_models import (
    AnalysisSpecificationOrm,
    ExecutionOrm,
    ExecutionPlanOrm,
    FamilyArtifactOrm,
    FamilyExecutionOrm,
    FamilyResultOrm,
    FamilyStageExecutionOrm,
)


async def _project_dataset(client, name: str, key: str) -> tuple[str, str]:  # type: ignore[no-untyped-def]
    project = await client.post("/api/v1/projects", json={"name": name})
    assert project.status_code == 201
    project_id = project.json()["project_id"]
    dataset = await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={"file": ("data.csv", b"x,y\n1,0\n2,1\n", "text/csv")},
        data={"dataset_key": key, "version_label": "v1", "name": name},
        headers={"Idempotency-Key": f"g6-{key}"},
    )
    assert dataset.status_code == 201
    return project_id, dataset.json()["dataset_version_id"]


async def _context_view(
    client, project_id: str, dataset_id: str,
) -> tuple[str, str]:  # type: ignore[no-untyped-def]
    context = await client.post(
        f"/api/v1/projects/{project_id}/research-contexts",
        json={
            "context_key": "g6-lineage", "problem_statement": "Trace the full analysis lifecycle.",
            "research_questions": ["Which follow-up analysis is justified?"],
            "significance": "Preserve cross-analysis provenance.", "hypotheses": [],
            "decision_context": {"action": "review"}, "relations": [],
        },
    )
    context_id = context.json()["research_context_version_id"]
    assert (await client.post(
        f"/api/v1/projects/{project_id}/research-contexts/{context_id}/fix"
    )).status_code == 200
    view = await client.post(
        f"/api/v1/projects/{project_id}/analysis-views",
        json={
            "view_key": "g6-lineage", "name": "G6 lineage view",
            "spec": {
                "schema_version": "analysis-view/1",
                "source_dataset_version_id": dataset_id,
                "row_filter": [], "selected_columns": ["x", "y"],
                "derived_columns": [],
                "missing_value_policy": {"default": "KEEP", "columns": {}},
                "time_cutoff": None, "sampling": None,
            },
        },
    )
    view_id = view.json()["analysis_view_id"]
    assert (await client.post(
        f"/api/v1/projects/{project_id}/analysis-views/{view_id}/validate"
    )).status_code == 200
    assert (await client.post(
        f"/api/v1/projects/{project_id}/analysis-views/{view_id}/fix"
    )).status_code == 200
    selected = await client.put(
        f"/api/v1/projects/{project_id}/workspace-state",
        json={
            "research_context_version_id": context_id,
            "dataset_version_id": dataset_id,
            "analysis_view_id": view_id,
        },
    )
    assert selected.status_code == 200
    return context_id, view_id


def _analysis_specification(
    project_id: str, dataset_id: str, context_id: str, view_id: str,
) -> str:
    specification_id = str(uuid.uuid4())
    factory = dependencies._get_session_factory()
    with factory() as session:
        session.add(AnalysisSpecificationOrm(
            analysis_specification_id=specification_id, project_id=project_id,
            specification_key="g6-predictive-draft", version_number=1, status="DRAFT",
            schema_version="analysis-specification/1", analysis_family="PREDICTIVE",
            research_context_version_id=context_id, dataset_version_id=dataset_id,
            analysis_view_id=view_id, analysis_mode="EXPLORATORY",
            family_spec_schema_version="g6-lineage-fixture/1", family_spec_json={},
            revision_context_json=None, warnings_json=[], canonical_hash=None,
            created_by="g6-test", created_at=datetime.now(timezone.utc), fixed_at=None,
        ))
        session.commit()
    return specification_id


def _family_result(
    project_id: str, dataset_id: str, family: str, result_type: str, *,
    context_id: str | None = None, view_id: str | None = None,
    specification_id: str | None = None,
) -> dict[str, str]:
    now = datetime.now(timezone.utc)
    execution_id, stage_id, result_id, plan_id, artifact_id = (
        str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()),
        str(uuid.uuid4()),
    )
    factory = dependencies._get_session_factory()
    with factory() as session:
        session.add(ExecutionPlanOrm(
            execution_plan_id=plan_id, project_id=project_id,
            analysis_specification_id=specification_id or f"g6-{family.lower()}-{result_id}",
            analysis_family=family, plan_schema_version="execution-plan/1",
            planner_id="g6.fixture", planner_version="1",
            stages_json=[], dependencies_json=[], plan_hash=uuid.uuid4().hex,
            created_at=now,
        ))
        session.flush()
        session.add(FamilyExecutionOrm(
            execution_id=execution_id, project_id=project_id,
            dataset_version_id=dataset_id, analysis_view_id=view_id,
            research_context_version_id=context_id,
            analysis_specification_id=specification_id,
            execution_plan_id=plan_id, analysis_family=family,
            specification_schema_version="g6-fixture/1",
            specification_snapshot_json={}, snapshot_json={},
            snapshot_hash=uuid.uuid4().hex, status="SUCCEEDED", retry_count=0,
            last_error_json=None, requested_by="g6-test", requested_at=now,
            started_at=now, finished_at=now,
        ))
        session.flush()
        session.add(FamilyStageExecutionOrm(
            stage_execution_id=stage_id, execution_id=execution_id,
            stage_key="g6", stage_type_json={"namespace": "g6", "name": "fixture", "version": "1"},
            ordinal=0, status="SUCCEEDED", attempt_history_json=[{"attempt": 1}],
            input_binding_json={}, output_binding_json={}, started_at=now, finished_at=now,
        ))
        session.flush()
        session.add(FamilyResultOrm(
            result_id=result_id, project_id=project_id, execution_id=execution_id,
            stage_execution_id=stage_id, analysis_family=family,
            result_type=result_type, schema_version="g6-result/1",
            analytical_status="GENERATED", summary_json={"value": 1},
            payload_json={}, diagnostics_json={}, warning_json=[], created_at=now,
        ))
        session.flush()
        session.add(FamilyArtifactOrm(
            artifact_id=artifact_id, project_id=project_id, execution_id=execution_id,
            stage_execution_id=stage_id, result_id=result_id, family=family,
            artifact_type="G6_LINEAGE_FIXTURE", schema_version="g6-artifact/1",
            media_type="application/json", object_key=f"g6/{artifact_id}.json",
            content_hash="0" * 64, size_bytes=0, metadata_json={}, created_at=now,
        ))
        session.commit()
    return {
        "execution_id": execution_id, "result_id": result_id,
        "artifact_id": artifact_id,
    }


def _causal_execution(
    project_id: str, dataset_id: str, *, base_id: str | None = None,
    revision_kind: str | None = None,
) -> str:
    execution_id = str(uuid.uuid4())
    revision_context = None if base_id is None else {
        "base_execution_id": base_id, "revision_kind": revision_kind,
        "changed_dimensions": [] if revision_kind == "RERUN" else ["parameters"],
        "change_reason": None if revision_kind == "RERUN" else "Revise assumptions",
    }
    with dependencies._get_session_factory()() as session:
        session.add(ExecutionOrm(
            execution_id=execution_id, project_id=project_id,
            dataset_version_id=dataset_id, input_graph_version_id=None,
            input_result_id=None, batch_key=str(uuid.uuid4()), operation="DISCOVERY",
            objective_snapshot="G6 causal draft", rationale_snapshot="Cross-analysis follow-up",
            analysis_spec_json={"revision_context": revision_context},
            algorithm_or_estimator="pc", parameter_json={}, random_seed=42,
            code_version="g6-test", runtime_version_json={}, snapshot_hash=uuid.uuid4().hex,
            snapshot_schema_version="causal-analysis-spec/2", status="QUEUED",
            retry_count=0, last_error_summary=None, requested_by="g6-test",
            requested_at=datetime.now(timezone.utc), started_at=None, finished_at=None,
        ))
        session.commit()
    return execution_id


@pytest.mark.anyio
@pytest.mark.requirement("G6-CROSS-ANALYSIS-LINEAGE")
async def test_project_lineage_combines_families_and_explicit_relations(client) -> None:  # type: ignore[no-untyped-def]
    project_id, dataset_id = await _project_dataset(client, "G6 lineage", "g6-lineage")
    context_id, view_id = await _context_view(client, project_id, dataset_id)
    specification_id = _analysis_specification(
        project_id, dataset_id, context_id, view_id,
    )
    explore = _family_result(
        project_id, dataset_id, "EXPLORATORY", "CHART_RESULT",
        context_id=context_id, view_id=view_id,
    )
    predictive = _family_result(
        project_id, dataset_id, "PREDICTIVE", "EVALUATION_RESULT",
        context_id=context_id, view_id=view_id, specification_id=specification_id,
    )
    causal_base_id = _causal_execution(project_id, dataset_id)
    rerun_id = _causal_execution(
        project_id, dataset_id, base_id=causal_base_id, revision_kind="RERUN"
    )
    revised_id = _causal_execution(
        project_id, dataset_id, base_id=causal_base_id, revision_kind="REVISED"
    )

    for target_type, target_id, statement in (
        ("Execution", causal_base_id, "Exploration motivated a causal draft."),
        ("AnalysisSpecification", specification_id, "Exploration motivated a predictive draft."),
    ):
        linked = await client.post(
            f"/api/v1/projects/{project_id}/lineage-links",
            json={
                "source_type": "Result", "source_id": explore["result_id"],
                "relation_type": "MOTIVATED", "target_type": target_type,
                "target_id": target_id, "evidence": {"statement": statement},
            },
        )
        assert linked.status_code == 201
    annotation = await client.post(
        f"/api/v1/projects/{project_id}/workspace-annotations",
        json={
            "target_type": "Result", "target_id": explore["result_id"],
            "statement": "Retain as hypothesis-generating evidence.",
            "rationale": "Cross-analysis lineage test", "assumptions": [],
            "limitations": ["Not causal"], "decision": "SELECTED",
            "next_actions": ["Review predictive and causal drafts"],
        },
    )
    assert annotation.status_code == 201
    annotation_id = annotation.json()["annotation_id"]

    response = await client.get(f"/api/v1/projects/{project_id}/lineage")
    assert response.status_code == 200
    graph = response.json()
    assert graph["schema_version"] == "project-lineage/1"
    node_keys = {(item["node_type"], item["entity_id"]) for item in graph["nodes"]}
    assert ("Result", explore["result_id"]) in node_keys
    assert ("Result", predictive["result_id"]) in node_keys
    edges = {
        (item["source_type"], item["source_id"], item["relation_type"],
         item["target_type"], item["target_id"], item["explicit"])
        for item in graph["edges"]
    }
    assert (
        "ResearchContextVersion", context_id, "USED_INPUT",
        "DatasetVersion", dataset_id, False,
    ) in edges
    assert ("DatasetVersion", dataset_id, "DERIVED_FROM", "AnalysisView", view_id, False) in edges
    assert (
        "DatasetVersion", dataset_id, "USED_INPUT",
        "Execution", explore["execution_id"], False,
    ) in edges
    assert (
        "Execution", predictive["execution_id"], "GENERATED",
        "Result", predictive["result_id"], False,
    ) in edges
    assert (
        "Result", predictive["result_id"], "GENERATED",
        "Artifact", predictive["artifact_id"], False,
    ) in edges
    assert (
        "Result", explore["result_id"], "MOTIVATED",
        "Execution", causal_base_id, True,
    ) in edges
    assert (
        "Result", explore["result_id"], "MOTIVATED",
        "AnalysisSpecification", specification_id, True,
    ) in edges
    assert (
        "Result", explore["result_id"], "SUPPORTED_BY",
        "Annotation", annotation_id, False,
    ) in edges
    revision_edges = [
        item for item in graph["edges"]
        if item["source_id"] == causal_base_id
        and item["relation_type"] == "REVISED_FROM"
    ]
    assert {item["target_id"] for item in revision_edges} == {rerun_id, revised_id}
    assert {
        item["evidence"]["revision_context"]["revision_kind"]
        for item in revision_edges
    } == {"RERUN", "REVISED"}

    result_graph = await client.get(
        f"/api/v1/projects/{project_id}/results/{predictive['result_id']}/lineage"
    )
    assert result_graph.status_code == 200
    assert result_graph.json()["root_result_id"] == predictive["result_id"]
    assert explore["result_id"] in {item["entity_id"] for item in result_graph.json()["nodes"]}


@pytest.mark.anyio
@pytest.mark.requirement("G6-PROJECT-BOUNDARY")
async def test_explicit_lineage_link_rejects_cross_project_resources(client) -> None:  # type: ignore[no-untyped-def]
    first_project, first_dataset = await _project_dataset(client, "first", "g6-first")
    second_project, second_dataset = await _project_dataset(client, "second", "g6-second")
    first_result = _family_result(
        first_project, first_dataset, "EXPLORATORY", "PROFILE_RESULT"
    )["result_id"]
    second_result = _family_result(
        second_project, second_dataset, "PREDICTIVE", "EVALUATION_RESULT"
    )["result_id"]

    response = await client.post(
        f"/api/v1/projects/{first_project}/lineage-links",
        json={
            "source_type": "Result", "source_id": first_result,
            "relation_type": "MOTIVATED",
            "target_type": "Result", "target_id": second_result,
            "evidence": {},
        },
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "PROJECT_BOUNDARY_VIOLATION"
