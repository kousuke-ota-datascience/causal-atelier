from __future__ import annotations

import pytest


GRAPH = {
    "graph_type": "DAG",
    "nodes": ["x", "treatment", "outcome"],
    "edges": [
        {"source": "x", "target": "treatment", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
        {"source": "x", "target": "outcome", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
        {"source": "treatment", "target": "outcome", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
    ],
}


async def _project_and_dataset(client, name: str = "ENH-E2"):  # type: ignore[no-untyped-def]
    project = (await client.post("/api/v1/projects", json={"name": name})).json()
    response = await client.post(
        f"/api/v1/projects/{project['project_id']}/dataset-versions",
        files={"file": ("data.csv", b"x,treatment,outcome\n0,0,1\n1,1,3\n", "text/csv")},
        data={"dataset_key": "d", "version_label": "v1", "name": "d"},
        headers={"Idempotency-Key": f"{name}-dataset"},
    )
    assert response.status_code == 201
    return project, response.json()


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("filename", "content"),
    [
        ("empty.csv", b""),
        ("broken.csv", b"\xff\xfe\x00\x00"),
        ("data.txt", b"x,y\n1,2\n"),
    ],
)
async def test_invalid_dataset_upload_is_actionable_client_error(
    client, filename: str, content: bytes,
) -> None:  # type: ignore[no-untyped-def]
    project = (await client.post("/api/v1/projects", json={"name": filename})).json()
    response = await client.post(
        f"/api/v1/projects/{project['project_id']}/dataset-versions",
        files={"file": (filename, content, "application/octet-stream")},
        data={"dataset_key": "d", "version_label": "v1", "name": "d"},
        headers={"Idempotency-Key": f"invalid-{filename}"},
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_DATASET_FILE"


@pytest.mark.anyio
async def test_long_dataset_key_is_metadata_error_instead_of_filesystem_500(client) -> None:  # type: ignore[no-untyped-def]
    project = (await client.post("/api/v1/projects", json={"name": "long-key"})).json()
    column_names_mistaken_for_key = ", ".join(f"feature_{index}" for index in range(30))
    assert len(column_names_mistaken_for_key) > 255

    response = await client.post(
        f"/api/v1/projects/{project['project_id']}/dataset-versions",
        files={"file": ("data.csv", b"x,y\n1,2\n", "text/csv")},
        data={
            "dataset_key": column_names_mistaken_for_key,
            "version_label": "v1",
            "name": "long-key dataset",
        },
        headers={"Idempotency-Key": "long-dataset-key"},
    )

    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "INVALID_DATASET_METADATA"
    assert error["message"] == (
        f"dataset_key must be at most 100 characters "
        f"(received {len(column_names_mistaken_for_key)})"
    )
    listed = await client.get(
        f"/api/v1/projects/{project['project_id']}/dataset-versions"
    )
    assert listed.json()["items"] == []


@pytest.mark.anyio
async def test_dataset_artifact_path_uses_internal_ids_not_dataset_metadata(client) -> None:  # type: ignore[no-untyped-def]
    project = (await client.post("/api/v1/projects", json={"name": "safe-key"})).json()
    project_id = project["project_id"]
    response = await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={"file": ("data.csv", b"x,y\n1,2\n", "text/csv")},
        data={
            "dataset_key": "segment/../sales",
            "version_label": "v1",
            "name": "safe storage path",
        },
        headers={"Idempotency-Key": "safe-dataset-key"},
    )

    assert response.status_code == 201
    dataset = response.json()
    artifact_id = dataset["source_artifact_id"]
    artifact = (await client.get(f"/api/v1/artifacts/{artifact_id}")).json()
    assert artifact["object_key"] == (
        f"projects/{project_id}/datasets/{artifact_id}/source.csv"
    )
    assert "segment" not in artifact["object_key"]
    download = await client.get(f"/api/v1/artifacts/{artifact_id}/download")
    assert download.status_code == 200
    assert download.content == b"x,y\n1,2\n"


def _graph_body(*, outcome: str | None = "outcome", fixed: bool = True) -> dict:
    return {
        "source_result_id": None,
        "parent_graph_version_id": None,
        "graph_origin": "USER_DEFINED",
        "name": "domain graph",
        "graph_type": "DAG",
        "graph": GRAPH,
        "designated_outcome_node": outcome,
        "provenance": {"source_note": "domain"},
        "edit_rationale": None,
        "fix_immediately": fixed,
    }


def _identification_body(dataset_id: str, graph_id: str, outcome: str) -> dict:
    return {
        "operation": "IDENTIFICATION",
        "dataset_version_id": dataset_id,
        "input_graph_version_id": graph_id,
        "input_result_id": None,
        "objective": "identify",
        "rationale": "ENH-E2 outcome gate",
        "analysis_spec": {
            "schema_version": "causal-analysis-spec/2",
            "analysis_mode": "EXPLORATORY",
            "research_context": {},
            "causal_question": {
                "population": "rows", "treatment": "treatment", "comparator": "untreated",
                "outcome": outcome, "analysis_unit": "row", "treatment_time": "t0",
                "outcome_window": "t1", "estimand": "ATE",
            },
            "causal_design": {
                "identification_strategy": "BACKDOOR", "adjustment_set": ["x"],
                "assumptions": ["exchangeability"],
            },
            "operation_spec": {"allow_partial_identification": False},
            "validation_override": None,
        },
        "variants": [{
            "algorithm_or_estimator": "GRAPHICAL_IDENTIFICATION",
            "parameters": {}, "random_seed": 42,
        }],
        "code_version": "test-enh-e2",
        "runtime_versions": {},
    }


@pytest.mark.anyio
@pytest.mark.requirement("FR-071", "FR-072", "FR-073", "FR-074", "NFR-018")
async def test_project_delete_is_idempotent_archive_and_all_new_writes_are_guarded(
    client,
) -> None:  # type: ignore[no-untyped-def]
    project, dataset = await _project_and_dataset(client, "archive")
    project_id = project["project_id"]
    execution_response = await client.post(
        f"/api/v1/projects/{project_id}/execution-batches",
        json={
            "operation": "DISCOVERY",
            "dataset_version_id": dataset["dataset_version_id"],
            "analysis_spec": {
                "schema_version": "causal-analysis-spec/2",
                "analysis_mode": "EXPLORATORY",
                "research_context": {},
                "causal_question": {},
                "causal_design": {"adjustment_set": [], "assumptions": []},
                "operation_spec": {
                    "feature_columns": ["x", "treatment", "outcome"],
                    "designated_outcome_node": "outcome",
                    "constraints": {
                        "required_edges": [], "forbidden_edges": [], "temporal_tiers": [],
                    },
                    "expected_graph_type": None,
                },
                "validation_override": None,
            },
            "variants": [{
                "algorithm_or_estimator": "pc",
                "parameters": {"alpha": 0.05},
                "random_seed": 42,
            }],
            "code_version": "test-enh-e2",
            "runtime_versions": {},
        },
    )
    assert execution_response.status_code == 202
    execution_id = execution_response.json()["executions"][0]["execution_id"]

    assert (await client.delete(f"/api/v1/projects/{project_id}")).status_code == 204
    assert (await client.delete(f"/api/v1/projects/{project_id}")).status_code == 204
    assert (await client.get(f"/api/v1/projects/{project_id}")).json()["status"] == "ARCHIVED"
    assert project_id not in {
        item["project_id"] for item in (await client.get("/api/v1/projects")).json()["items"]
    }
    # Existing immutable lineage remains readable.
    assert (await client.get(
        f"/api/v1/projects/{project_id}/dataset-versions"
    )).json()["items"][0]["dataset_version_id"] == dataset["dataset_version_id"]

    update = await client.patch(f"/api/v1/projects/{project_id}", json={"memo": "forbidden"})
    assert update.status_code == 409 and update.json()["error"]["code"] == "PROJECT_ARCHIVED"
    graph = await client.post(
        f"/api/v1/projects/{project_id}/graph-versions",
        json=_graph_body(),
        headers={"Idempotency-Key": "archived-graph"},
    )
    assert graph.status_code == 409 and graph.json()["error"]["code"] == "PROJECT_ARCHIVED"
    second_upload = await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={"file": ("next.csv", b"x,treatment,outcome\n2,0,4\n", "text/csv")},
        data={"dataset_key": "d", "version_label": "v2", "name": "d"},
        headers={"Idempotency-Key": "archived-dataset-v2"},
    )
    assert second_upload.status_code == 409
    assert second_upload.json()["error"]["code"] == "PROJECT_ARCHIVED"
    for action in ("cancel", "retry"):
        response = await client.post(f"/api/v1/executions/{execution_id}/{action}")
        assert response.status_code == 409
        assert response.json()["error"]["code"] == "PROJECT_ARCHIVED"


@pytest.mark.anyio
@pytest.mark.requirement("FR-080", "FR-083", "FR-084", "FR-086", "FR-094")
async def test_graph_candidate_lifecycle_and_comparison_are_state_derived(client) -> None:  # type: ignore[no-untyped-def]
    project, _ = await _project_and_dataset(client, "graphs")
    project_id = project["project_id"]
    draft = (await client.post(
        f"/api/v1/projects/{project_id}/graph-versions",
        json=_graph_body(fixed=False),
        headers={"Idempotency-Key": "draft-root"},
    )).json()

    invalid_parent = await client.post(
        f"/api/v1/projects/{project_id}/graph-versions",
        json={
            **_graph_body(fixed=False),
            "parent_graph_version_id": draft["graph_version_id"],
            "graph_origin": "USER_EDITED",
            "edit_rationale": "invalid parent state",
        },
        headers={"Idempotency-Key": "invalid-parent"},
    )
    assert invalid_parent.status_code == 409
    assert invalid_parent.json()["error"]["code"] == "GRAPH_PARENT_NOT_FIXED"

    fixed = (await client.post(
        f"/api/v1/projects/{project_id}/graph-versions/{draft['graph_version_id']}/fix"
    )).json()
    child = (await client.post(
        f"/api/v1/projects/{project_id}/graph-edit-drafts",
        json={
            "base_candidate_kind": "GRAPH_VERSION",
            "base_candidate_id": fixed["graph_version_id"],
            "change_kind": "USER_EDITED",
            "name": "edited child",
            "edit_rationale": "remove implausible direct effect",
        },
        headers={"Idempotency-Key": "child"},
    )).json()
    assert child["status"] == "DRAFT"
    assert child["parent_graph_version_id"] == fixed["graph_version_id"]
    assert child["designated_outcome_node"] == "outcome"

    changed_graph = {**GRAPH, "edges": GRAPH["edges"][:-1]}
    child = (await client.patch(
        f"/api/v1/projects/{project_id}/graph-versions/{child['graph_version_id']}",
        json={
            "graph": changed_graph,
            "designated_outcome_node": "outcome",
            "edit_rationale": "remove implausible direct effect",
        },
    )).json()
    child = (await client.post(
        f"/api/v1/projects/{project_id}/graph-versions/{child['graph_version_id']}/fix"
    )).json()
    immutable = await client.patch(
        f"/api/v1/projects/{project_id}/graph-versions/{child['graph_version_id']}",
        json={"graph": GRAPH, "edit_rationale": "must create another child"},
    )
    assert immutable.status_code == 409
    assert immutable.json()["error"]["code"] == "GRAPH_FIXED_IMMUTABLE"

    candidates = (await client.get(
        f"/api/v1/projects/{project_id}/graph-candidates"
    )).json()["items"]
    assert len(candidates) == 2
    assert candidates[0]["allowed_actions"]["can_create_child"] is True
    assert candidates[1]["allowed_actions"]["can_use_for_inference"] is True
    comparison = await client.post(
        f"/api/v1/projects/{project_id}/graph-candidate-comparisons/query",
        json={"candidate_refs": [
            {"candidate_kind": "GRAPH_VERSION", "candidate_id": fixed["graph_version_id"]},
            {"candidate_kind": "GRAPH_VERSION", "candidate_id": child["graph_version_id"]},
        ]},
    )
    assert comparison.status_code == 200
    assert comparison.json()["compatibility"]["compatible"] is True
    assert comparison.json()["differences"][0]["removed_edges"]


@pytest.mark.anyio
@pytest.mark.requirement("FR-078", "FR-089", "FR-090", "FR-091")
async def test_inference_rejects_missing_or_tampered_graph_outcome(client) -> None:  # type: ignore[no-untyped-def]
    project, dataset = await _project_and_dataset(client, "outcome")
    project_id = project["project_id"]
    fixed = (await client.post(
        f"/api/v1/projects/{project_id}/graph-versions",
        json=_graph_body(),
        headers={"Idempotency-Key": "fixed-outcome"},
    )).json()
    mismatch = await client.post(
        f"/api/v1/projects/{project_id}/execution-batches",
        json=_identification_body(dataset["dataset_version_id"], fixed["graph_version_id"], "x"),
    )
    assert mismatch.status_code == 409
    assert mismatch.json()["error"]["code"] == "GRAPH_OUTCOME_MISMATCH"

    missing = (await client.post(
        f"/api/v1/projects/{project_id}/graph-versions",
        json=_graph_body(outcome=None),
        headers={"Idempotency-Key": "fixed-missing"},
    )).json()
    required = await client.post(
        f"/api/v1/projects/{project_id}/execution-batches",
        json=_identification_body(dataset["dataset_version_id"], missing["graph_version_id"], "outcome"),
    )
    assert required.status_code == 422
    assert required.json()["error"]["code"] == "GRAPH_OUTCOME_REQUIRED"

    accepted = await client.post(
        f"/api/v1/projects/{project_id}/execution-batches",
        json=_identification_body(
            dataset["dataset_version_id"], fixed["graph_version_id"], "outcome"
        ),
    )
    assert accepted.status_code == 202
