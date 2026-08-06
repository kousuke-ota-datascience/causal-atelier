from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from ariadne.adapters.local_artifact_store import LocalArtifactStore
from ariadne.interfaces.web_api import dependencies
from ariadne.interfaces.worker.execution_processor import ExecutionProcessor
from ariadne.product.domain.enums import ResultType, ScientificStatus
from ariadne.product.domain.enums import ExecutionOperation
from ariadne.product.application.execution_service import _post_selection_inference_warnings
from ariadne.product.ports.scientific_core import ScientificResultBatch, ScientificResultDescriptor
from ariadne.scientific.core_adapter import ScientificCoreAdapter


GRAPH = {"graph_type": "DAG", "nodes": ["customer_id", "x", "treatment", "outcome"], "edges": [
    {"source": "x", "target": "treatment", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
    {"source": "x", "target": "outcome", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
    {"source": "treatment", "target": "outcome", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
]}


class FakeScientificCore:
    def run_discovery(self, _input, _output):  # type: ignore[no-untyped-def]
        return ScientificResultBatch([ScientificResultDescriptor(
            ResultType.DISCOVERY_GRAPH_RESULT, ScientificStatus.GENERATED,
            {"edge_count": 3}, GRAPH,
        )])

    def run_identification(self, _input, _output):  # type: ignore[no-untyped-def]
        return ScientificResultBatch([
            ScientificResultDescriptor(
                ResultType.IDENTIFICATION_RESULT, ScientificStatus.IDENTIFIED,
                {"strategy": "BACKDOOR"},
                {"strategy": "BACKDOOR", "causal_question_hash": "fake", "selected_adjustment_set": ["x"]},
            ),
            ScientificResultDescriptor(
                ResultType.DATA_ELIGIBILITY_RESULT, ScientificStatus.PASS,
                {"status": "PASS"}, {"status": "PASS", "checks": [
                    {"check_code": "LIMITED_OVERLAP", "status": "PASS", "evidence": {}},
                ], "inferred_types": {
                    "treatment": {"type": "BINARY", "evidence": {}},
                    "outcome": {"type": "CONTINUOUS", "evidence": {}},
                }},
            ),
        ])

    def run_estimation(self, input_, _output):  # type: ignore[no-untyped-def]
        return ScientificResultBatch([
            ScientificResultDescriptor(
                ResultType.TREATMENT_EFFECT_RESULT, ScientificStatus.ESTIMATED,
                {"estimate": 2.0},
                {"estimator": input_.estimator, "estimand": "ATE", "estimate": 2.0,
                 "standard_error": .2, "confidence_interval": [1.6, 2.4]},
            ),
            ScientificResultDescriptor(
                ResultType.DIAGNOSTICS_RESULT, ScientificStatus.PASS,
                {"status": "PASS"}, {"sample_size": 40},
            ),
        ])

    def run_refutation(self, _input, _output):  # type: ignore[no-untyped-def]
        return ScientificResultBatch([ScientificResultDescriptor(
            ResultType.REFUTATION_RESULT, ScientificStatus.NO_FAILURE_DETECTED,
            {"method": "PLACEBO_TREATMENT"},
            {"interpretation": "No specified failure was detected; assumptions are not proven."},
        )])

    def run_sensitivity(self, _input, _output):  # type: ignore[no-untyped-def]
        return ScientificResultBatch([ScientificResultDescriptor(
            ResultType.SENSITIVITY_RESULT, ScientificStatus.ROBUST,
            {"dimension": "PROPENSITY_CLIPPING"},
            {"sign_reversal": False, "decision_reversal": False},
        )])


class NonIdentifiedCore(FakeScientificCore):
    def run_identification(self, _input, _output):  # type: ignore[no-untyped-def]
        return ScientificResultBatch([
            ScientificResultDescriptor(
                ResultType.IDENTIFICATION_RESULT, ScientificStatus.NOT_IDENTIFIED,
                {"reason_count": 1}, {"non_identification_reasons": [{"code": "OPEN_BACKDOOR_PATH"}]},
            ),
            ScientificResultDescriptor(
                ResultType.DATA_ELIGIBILITY_RESULT, ScientificStatus.PASS,
                {"status": "PASS"}, {"status": "PASS", "checks": [], "inferred_types": {
                    "treatment": {"type": "BINARY", "evidence": {}},
                    "outcome": {"type": "CONTINUOUS", "evidence": {}},
                }},
            ),
        ])


def test_post_selection_warning_has_exact_scope_and_deterministic_sources() -> None:
    executions = [
        SimpleNamespace(execution_id="discovery-z", operation=ExecutionOperation.DISCOVERY,
                        dataset_version_id="dataset-a"),
        SimpleNamespace(execution_id="discovery-a", operation=ExecutionOperation.DISCOVERY,
                        dataset_version_id="dataset-a"),
        SimpleNamespace(execution_id="other-dataset", operation=ExecutionOperation.DISCOVERY,
                        dataset_version_id="dataset-b"),
        SimpleNamespace(execution_id="not-discovery", operation=ExecutionOperation.IDENTIFICATION,
                        dataset_version_id="dataset-a"),
    ]
    repository = SimpleNamespace(list_by_project=lambda project_id: executions)
    uow = SimpleNamespace(executions=repository)

    assert _post_selection_inference_warnings(
        uow=uow, project_id="project", dataset_version_id="dataset-a",
        operation=ExecutionOperation.ESTIMATION, analysis_mode="EXPLORATORY",
    ) == []
    assert _post_selection_inference_warnings(
        uow=uow, project_id="project", dataset_version_id="dataset-b-missing",
        operation=ExecutionOperation.ESTIMATION, analysis_mode="CONFIRMATORY",
    ) == []
    warning = _post_selection_inference_warnings(
        uow=uow, project_id="project", dataset_version_id="dataset-a",
        operation=ExecutionOperation.ESTIMATION, analysis_mode="CONFIRMATORY",
    )
    assert warning == [{
        "warning_code": "POST_SELECTION_INFERENCE_RISK",
        "message": (
            "Confirmatory estimation follows graph discovery on the same Dataset Version; "
            "post-selection inference may invalidate nominal uncertainty."
        ),
        "source_discovery_execution_ids": ["discovery-a", "discovery-z"],
        "dataset_version_id": "dataset-a",
        "rationale": (
            "A prior DISCOVERY Execution used the same immutable Dataset Version in this Project."
        ),
    }]


def process_next(tmp_path: Path, core=None) -> None:  # type: ignore[no-untyped-def]
    with dependencies._uow_context() as uow:
        execution = uow.executions.claim_next("test-worker"); uow.commit()
    assert execution is not None
    ExecutionProcessor(
        dependencies._uow_context, core or FakeScientificCore(),
        LocalArtifactStore(tmp_path / "objects"),
    ).process(execution)


def common_spec(*, question=True, operation_spec=None, strategy="BACKDOOR"):  # type: ignore[no-untyped-def]
    return {
        "schema_version": "causal-analysis-spec/2", "analysis_mode": "EXPLORATORY",
        "research_context": {},
        "causal_question": ({
            "population": "eligible rows", "treatment": "treatment", "comparator": "untreated",
            "outcome": "outcome", "analysis_unit": "customer_id", "treatment_time": "t0",
            "outcome_window": "30d", "estimand": "ATE",
        } if question else {}),
        "causal_design": {
            "identification_strategy": strategy, "adjustment_set": ["x"], "assumptions": ["exchangeability"],
        },
        "operation_spec": operation_spec or {}, "validation_override": None,
    }


async def submit(client, project_id, body, key):  # type: ignore[no-untyped-def]
    return await client.post(
        f"/api/v1/projects/{project_id}/execution-batches", json=body,
        headers={"Idempotency-Key": key},
    )


@pytest.mark.anyio
async def test_execution_batch_validation_error_exposes_actionable_field_details(client) -> None:  # type: ignore[no-untyped-def]
    response = await submit(client, "not-used", {
        "operation": "DISCOVERY", "dataset_version_id": "not-used",
        "input_graph_version_id": None, "input_result_id": None,
        "objective": "validation regression", "rationale": "no variants",
        "analysis_spec": common_spec(
            question=False,
            operation_spec={
                "feature_columns": ["x"], "constraints": {},
                "expected_graph_type": None,
            },
        ),
        "variants": [], "code_version": "test", "runtime_versions": {},
    }, "invalid-empty-variants")

    assert response.status_code == 400
    error = response.json()["error"]
    assert error["code"] == "INVALID_REQUEST"
    assert any(
        item["loc"] == ["body", "variants"] and item["type"] == "too_short"
        for item in error["details"]["errors"]
    )


async def _create_identification_fixture(client, *, name: str, content: bytes):  # type: ignore[no-untyped-def]
    project_id = (await client.post("/api/v1/projects", json={"name": name})).json()["project_id"]
    dataset_id = (await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={"file": ("data.csv", content, "text/csv")},
        data={"dataset_key": "d", "version_label": "v1", "name": "d"},
        headers={"Idempotency-Key": f"{name}-dataset"},
    )).json()["dataset_version_id"]
    graph_id = (await client.post(
        f"/api/v1/projects/{project_id}/graph-versions",
        json={"source_result_id": None, "parent_graph_version_id": None,
              "graph_origin": "USER_DEFINED", "name": "domain graph", "graph_type": "DAG",
              "graph": GRAPH, "provenance": {"source_note": "test"},
              "edit_rationale": None, "fix_immediately": True},
        headers={"Idempotency-Key": f"{name}-graph"},
    )).json()["graph_version_id"]
    response = await submit(client, project_id, {
        "operation": "IDENTIFICATION", "dataset_version_id": dataset_id,
        "input_graph_version_id": graph_id, "input_result_id": None,
        "objective": "eligibility edge case", "rationale": "FR-064",
        "analysis_spec": common_spec(operation_spec={"allow_partial_identification": False}),
        "variants": [{"algorithm_or_estimator": "GRAPHICAL_IDENTIFICATION", "parameters": {}, "random_seed": 42}],
        "code_version": "test", "runtime_versions": {},
    }, f"{name}-identification")
    assert response.status_code == 201
    return project_id, dataset_id, response.json()["executions"][0]["execution_id"]


@pytest.mark.anyio
@pytest.mark.requirement("FR-050", "FR-064", "FR-065")
@pytest.mark.parametrize(
    ("name", "content", "expected_status"),
    [
        ("string-treatment", b"customer_id,x,treatment,outcome\n" + b"1,0,control,1\n2,1,treated,3\n" * 12, "FAIL"),
        ("string-outcome", b"customer_id,x,treatment,outcome\n" + b"1,0,0,low\n2,1,1,high\n" * 12, "FAIL"),
        ("missing-outcome", b"customer_id,x,treatment\n" + b"1,0,0\n2,1,1\n" * 12, "FAIL"),
        ("one-arm", b"customer_id,x,treatment,outcome\n" + b"1,0,0,1\n2,1,0,3\n" * 12, "FAIL"),
        ("small-sample", b"customer_id,x,treatment,outcome\n" + b"1,0,0,1\n2,1,1,3\n" * 4, "FAIL"),
        ("propensity-failure", b"customer_id,x,treatment,outcome\n" + b"1,,0,1\n2,,1,3\n" * 60, "FAIL"),
    ],
)
async def test_real_worker_persists_negative_eligibility_without_technical_failure(
    client, product_env, name: str, content: bytes, expected_status: str,
) -> None:  # type: ignore[no-untyped-def]
    _, tmp_path = product_env
    _, _, execution_id = await _create_identification_fixture(client, name=name, content=content)
    process_next(tmp_path, ScientificCoreAdapter())
    execution = (await client.get(f"/api/v1/executions/{execution_id}")).json()
    results = (await client.get(f"/api/v1/executions/{execution_id}/results")).json()["items"]
    eligibility = next(item for item in results if item["result_type"] == "DATA_ELIGIBILITY_RESULT")
    assert execution["status"] == "SUCCEEDED"
    assert eligibility["scientific_status"] == expected_status


@pytest.mark.anyio
@pytest.mark.requirement("FR-064")
async def test_worker_marks_unreadable_dataset_artifact_as_technical_failure(
    client, product_env,
) -> None:  # type: ignore[no-untyped-def]
    _, tmp_path = product_env
    _, dataset_id, execution_id = await _create_identification_fixture(
        client,
        name="unreadable-artifact",
        content=b"customer_id,x,treatment,outcome\n" + b"1,0,0,1\n2,1,1,3\n" * 12,
    )
    with dependencies._uow_context() as uow:
        dataset = uow.dataset_versions.get(dataset_id)
        assert dataset is not None
        artifact = uow.artifacts.get(dataset.source_artifact_id)
        assert artifact is not None
    (tmp_path / "objects" / artifact.object_key).unlink()
    process_next(tmp_path, ScientificCoreAdapter())
    execution = (await client.get(f"/api/v1/executions/{execution_id}")).json()
    results = (await client.get(f"/api/v1/executions/{execution_id}/results")).json()["items"]
    assert execution["status"] == "FAILED"
    assert results == []


@pytest.mark.anyio
async def test_enh_e1_identification_first_nonidentification_and_lineage(client, product_env):  # type: ignore[no-untyped-def]
    _, tmp_path = product_env
    project = (await client.post("/api/v1/projects", json={"name": "ENH-E1"})).json()
    project_id = project["project_id"]
    content = b"customer_id,x,treatment,outcome\n" + b"1,0,0,1\n2,1,1,3\n" * 20
    dataset = await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={"file": ("data.csv", content, "text/csv")},
        data={"dataset_key": "d", "version_label": "v1", "name": "d", "source_note": "synthetic"},
        headers={"Idempotency-Key": "dataset"},
    )
    dataset_id = dataset.json()["dataset_version_id"]
    assert set(dataset.json()["schema"].values()) <= {
        "BOOLEAN", "INTEGER", "REAL", "DATETIME", "TEXT", "OTHER",
    }

    discovery = await submit(client, project_id, {
        "operation": "DISCOVERY", "dataset_version_id": dataset_id,
        "input_graph_version_id": None, "input_result_id": None,
        "objective": "discover provenance source", "rationale": "E2E-06",
        "analysis_spec": common_spec(
            question=False,
            operation_spec={"feature_columns": ["x", "treatment", "outcome"],
                            "constraints": {}, "expected_graph_type": "DAG"},
        ),
        "variants": [{"algorithm_or_estimator": "PC", "parameters": {}, "random_seed": 42}],
        "code_version": "test", "runtime_versions": {},
    }, "discover")
    assert discovery.status_code == 201
    discovery_execution = discovery.json()["executions"][0]["execution_id"]
    process_next(tmp_path)
    discovery_results = (await client.get(
        f"/api/v1/executions/{discovery_execution}/results"
    )).json()["items"]
    discovery_result_id = discovery_results[0]["result_id"]

    discovered = (await client.post(
        f"/api/v1/projects/{project_id}/graph-versions",
        json={"source_result_id": discovery_result_id, "parent_graph_version_id": None,
              "graph_origin": "DISCOVERED", "name": "algorithm output", "graph_type": "DAG",
              "graph": GRAPH, "provenance": {"backend": "fake-core"},
              "edit_rationale": None, "fix_immediately": True},
        headers={"Idempotency-Key": "discovered-graph"},
    )).json()
    constrained_graph = {**GRAPH, "edges": GRAPH["edges"][:-1]}
    constrained = (await client.post(
        f"/api/v1/projects/{project_id}/graph-versions",
        json={"source_result_id": None, "parent_graph_version_id": discovered["graph_version_id"],
              "graph_origin": "CONSTRAINT_ADJUSTED", "name": "post-hoc constraint",
              "graph_type": "DAG", "graph": constrained_graph,
              "provenance": {"constraint_mode": "POST_HOC", "reason": "domain exclusion"},
              "edit_rationale": None, "fix_immediately": True},
        headers={"Idempotency-Key": "constrained-graph"},
    )).json()
    edited = (await client.post(
        f"/api/v1/projects/{project_id}/graph-versions",
        json={"source_result_id": None, "parent_graph_version_id": constrained["graph_version_id"],
              "graph_origin": "USER_EDITED", "name": "reviewed graph", "graph_type": "DAG",
              "graph": GRAPH, "provenance": {"editor": "analyst"},
              "edit_rationale": "restore treatment effect edge", "fix_immediately": True},
        headers={"Idempotency-Key": "edited-graph"},
    )).json()
    assert [discovered["graph_origin"], constrained["graph_origin"], edited["graph_origin"]] == [
        "DISCOVERED", "CONSTRAINT_ADJUSTED", "USER_EDITED",
    ]
    assert constrained["parent_graph_version_id"] == discovered["graph_version_id"]
    assert edited["parent_graph_version_id"] == constrained["graph_version_id"]
    assert discovered["content_hash"] != constrained["content_hash"]

    graph = await client.post(
        f"/api/v1/projects/{project_id}/graph-versions",
        json={"source_result_id": None, "parent_graph_version_id": None,
              "graph_origin": "USER_DEFINED", "name": "domain DAG", "graph_type": "DAG",
              "graph": GRAPH, "provenance": {"source_note": "domain knowledge"},
              "edit_rationale": None, "fix_immediately": True},
        headers={"Idempotency-Key": "graph"},
    )
    assert graph.status_code == 201 and graph.json()["graph_origin"] == "USER_DEFINED"
    graph_id = graph.json()["graph_version_id"]

    identification = await submit(client, project_id, {
        "operation": "IDENTIFICATION", "dataset_version_id": dataset_id,
        "input_graph_version_id": graph_id, "input_result_id": None,
        "objective": "identify", "rationale": "gate",
        "analysis_spec": common_spec(operation_spec={"allow_partial_identification": False}),
        "variants": [{"algorithm_or_estimator": "GRAPHICAL_IDENTIFICATION", "parameters": {}, "random_seed": 42}],
        "code_version": "test", "runtime_versions": {},
    }, "identify")
    assert identification.status_code == 201
    identification_execution = identification.json()["executions"][0]["execution_id"]
    process_next(tmp_path)
    results = (await client.get(f"/api/v1/executions/{identification_execution}/results")).json()["items"]
    assert {result["result_type"] for result in results} == {
        "IDENTIFICATION_RESULT", "DATA_ELIGIBILITY_RESULT",
    }
    identification_result = next(result for result in results if result["result_type"] == "IDENTIFICATION_RESULT")

    estimation_spec = common_spec(operation_spec={"inference_options": {}})
    estimation = await submit(client, project_id, {
        "operation": "ESTIMATION", "dataset_version_id": dataset_id,
        "input_graph_version_id": graph_id, "input_result_id": identification_result["result_id"],
        "objective": "estimate", "rationale": "compare",
        "analysis_spec": estimation_spec,
        "variants": [{"algorithm_or_estimator": "ols", "parameters": {}, "random_seed": 42},
                     {"algorithm_or_estimator": "ipw", "parameters": {}, "random_seed": 42}],
        "code_version": "test", "runtime_versions": {},
    }, "estimate")
    assert estimation.status_code == 201
    for _ in range(2):
        process_next(tmp_path)
    effect_results = []
    for item in estimation.json()["executions"]:
        current = (await client.get(f"/api/v1/executions/{item['execution_id']}/results")).json()["items"]
        assert {value["result_type"] for value in current} == {"TREATMENT_EFFECT_RESULT", "DIAGNOSTICS_RESULT"}
        effect_results.append(next(value for value in current if value["result_type"] == "TREATMENT_EFFECT_RESULT"))
    comparison = await client.post("/api/v1/comparisons/query", json={
        "project_id": project_id, "result_ids": [value["result_id"] for value in effect_results],
    })
    assert comparison.status_code == 200
    annotation = await client.post(f"/api/v1/projects/{project_id}/annotations", json={
        "target_result_id": effect_results[0]["result_id"], "target_graph_version_id": None,
        "statement": "retain OLS estimate", "rationale": "estimator agreement",
        "assumptions": ["exchangeability", "positivity"],
        "limitations": ["synthetic acceptance data"],
    })
    assert annotation.status_code == 201
    lineage = (await client.get(f"/api/v1/results/{effect_results[0]['result_id']}/lineage")).json()
    assert sum(node["node_type"] == "Result" for node in lineage["nodes"]) >= 2
    assert any(node["node_type"] == "Annotation" for node in lineage["nodes"])

    for operation, operation_spec, method, expected_type in [
        ("REFUTATION", {"method": "PLACEBO_TREATMENT", "repetitions": 10},
         "PLACEBO_TREATMENT", "REFUTATION_RESULT"),
        ("SENSITIVITY", {"dimension": "PROPENSITY_CLIPPING", "values": [.01, .05]},
         "PROPENSITY_CLIPPING", "SENSITIVITY_RESULT"),
    ]:
        followup_spec = common_spec(question=False, operation_spec=operation_spec)
        followup = await submit(client, project_id, {
            "operation": operation, "dataset_version_id": dataset_id,
            "input_graph_version_id": graph_id, "input_result_id": effect_results[0]["result_id"],
            "objective": operation.lower(), "rationale": "ENH-E1 follow-up",
            "analysis_spec": followup_spec,
            "variants": [{"algorithm_or_estimator": method, "parameters": {}, "random_seed": 42}],
            "code_version": "test", "runtime_versions": {},
        }, operation.lower())
        assert followup.status_code == 201
        followup_execution = followup.json()["executions"][0]["execution_id"]
        process_next(tmp_path)
        followup_results = (await client.get(
            f"/api/v1/executions/{followup_execution}/results"
        )).json()["items"]
        assert followup_results[0]["result_type"] == expected_type

    negative = await submit(client, project_id, {
        "operation": "IDENTIFICATION", "dataset_version_id": dataset_id,
        "input_graph_version_id": graph_id, "input_result_id": None,
        "objective": "negative", "rationale": "test",
        "analysis_spec": common_spec(operation_spec={"allow_partial_identification": False}),
        "variants": [{"algorithm_or_estimator": "GRAPHICAL_IDENTIFICATION", "parameters": {}, "random_seed": 7}],
        "code_version": "test", "runtime_versions": {},
    }, "negative")
    negative_execution = negative.json()["executions"][0]["execution_id"]
    process_next(tmp_path, NonIdentifiedCore())
    negative_results = (await client.get(f"/api/v1/executions/{negative_execution}/results")).json()["items"]
    negative_id = next(value["result_id"] for value in negative_results if value["result_type"] == "IDENTIFICATION_RESULT")
    rejected = await submit(client, project_id, {
        "operation": "ESTIMATION", "dataset_version_id": dataset_id,
        "input_graph_version_id": graph_id, "input_result_id": negative_id,
        "objective": "must reject", "rationale": "gate", "analysis_spec": estimation_spec,
        "variants": [{"algorithm_or_estimator": "ols", "parameters": {}, "random_seed": 42}],
        "code_version": "test", "runtime_versions": {},
    }, "reject")
    assert rejected.status_code == 422 and rejected.json()["error"]["code"] == "IDENTIFICATION_NOT_ACCEPTABLE"


@pytest.mark.anyio
@pytest.mark.requirement("FR-060", "FR-062", "FR-063")
async def test_confirmatory_warning_and_revised_execution_are_persisted(
    client, product_env,
) -> None:  # type: ignore[no-untyped-def]
    _, tmp_path = product_env
    project_id = (await client.post("/api/v1/projects", json={"name": "E1a"})).json()["project_id"]
    content = b"customer_id,x,treatment,outcome\n" + b"1,0,0,1\n2,1,1,3\n" * 20
    dataset_id = (await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={"file": ("data.csv", content, "text/csv")},
        data={"dataset_key": "d", "version_label": "v1", "name": "d"},
        headers={"Idempotency-Key": "e1a-dataset"},
    )).json()["dataset_version_id"]

    discovery = await submit(client, project_id, {
        "operation": "DISCOVERY", "dataset_version_id": dataset_id,
        "input_graph_version_id": None, "input_result_id": None,
        "objective": "prior exploration", "rationale": "FR-063",
        "analysis_spec": common_spec(
            question=False,
            operation_spec={"feature_columns": ["x", "treatment", "outcome"],
                            "constraints": {}, "expected_graph_type": "DAG"},
        ),
        "variants": [{"algorithm_or_estimator": "PC", "parameters": {}, "random_seed": 42}],
        "code_version": "test", "runtime_versions": {},
    }, "e1a-discovery")
    discovery_execution_id = discovery.json()["executions"][0]["execution_id"]
    process_next(tmp_path)

    graph_id = (await client.post(
        f"/api/v1/projects/{project_id}/graph-versions",
        json={"source_result_id": None, "parent_graph_version_id": None,
              "graph_origin": "USER_DEFINED", "name": "fixed", "graph_type": "DAG",
              "graph": GRAPH, "provenance": {"source_note": "domain"},
              "edit_rationale": None, "fix_immediately": True},
        headers={"Idempotency-Key": "e1a-graph"},
    )).json()["graph_version_id"]
    identification = await submit(client, project_id, {
        "operation": "IDENTIFICATION", "dataset_version_id": dataset_id,
        "input_graph_version_id": graph_id, "input_result_id": None,
        "objective": "identify", "rationale": "gate",
        "analysis_spec": common_spec(operation_spec={"allow_partial_identification": False}),
        "variants": [{"algorithm_or_estimator": "GRAPHICAL_IDENTIFICATION", "parameters": {}, "random_seed": 42}],
        "code_version": "test", "runtime_versions": {},
    }, "e1a-identification")
    identification_execution_id = identification.json()["executions"][0]["execution_id"]
    process_next(tmp_path)
    identification_result_id = next(
        item["result_id"] for item in (await client.get(
            f"/api/v1/executions/{identification_execution_id}/results"
        )).json()["items"] if item["result_type"] == "IDENTIFICATION_RESULT"
    )

    confirmatory_spec = {
        **common_spec(operation_spec={"inference_options": {}}),
        "analysis_mode": "CONFIRMATORY",
    }
    base_body = {
        "operation": "ESTIMATION", "dataset_version_id": dataset_id,
        "input_graph_version_id": graph_id, "input_result_id": identification_result_id,
        "objective": "confirm", "rationale": "estimate after exploration",
        "analysis_spec": confirmatory_spec,
        "variants": [{"algorithm_or_estimator": "ols", "parameters": {}, "random_seed": 42}],
        "code_version": "test", "runtime_versions": {},
    }
    base = await submit(client, project_id, base_body, "e1a-base")
    assert base.status_code == 201
    base_execution_id = base.json()["executions"][0]["execution_id"]
    warning = base.json()["executions"][0]["scientific_warnings"][0]
    assert warning["warning_code"] == "POST_SELECTION_INFERENCE_RISK"
    assert warning["source_discovery_execution_ids"] == [discovery_execution_id]

    missing_reason = await submit(client, project_id, {
        **base_body,
        "base_execution_id": base_execution_id,
        "variants": [{"algorithm_or_estimator": "ipw", "parameters": {}, "random_seed": 42}],
    }, "e1a-missing-reason")
    assert missing_reason.status_code == 422
    assert missing_reason.json()["error"]["code"] == "EXECUTION_CHANGE_REASON_REQUIRED"

    rerun = await submit(client, project_id, {
        **base_body,
        "base_execution_id": base_execution_id,
    }, "e1a-rerun")
    assert rerun.status_code == 201
    rerun_id = rerun.json()["executions"][0]["execution_id"]
    rerun_execution = (await client.get(f"/api/v1/executions/{rerun_id}")).json()
    assert rerun_execution["revision_context"]["revision_kind"] == "RERUN"
    assert rerun_execution["revision_context"]["changed_dimensions"] == []

    revised = await submit(client, project_id, {
        **base_body,
        "base_execution_id": base_execution_id,
        "change_reason": "triangulate with a propensity estimator",
        "variants": [{"algorithm_or_estimator": "ipw", "parameters": {}, "random_seed": 42}],
    }, "e1a-revised")
    assert revised.status_code == 201
    revised_id = revised.json()["executions"][0]["execution_id"]
    revised_execution = (await client.get(f"/api/v1/executions/{revised_id}")).json()
    revision = revised_execution["revision_context"]
    assert revision["revision_kind"] == "REVISED"
    assert revision["base_execution_id"] == base_execution_id
    assert revision["change_reason"] == "triangulate with a propensity estimator"
    assert "algorithm_or_estimator" in revision["changed_dimensions"]

    for _ in range(3):
        process_next(tmp_path)
    revised_result = next(
        item for item in (await client.get(f"/api/v1/executions/{revised_id}/results")).json()["items"]
        if item["result_type"] == "TREATMENT_EFFECT_RESULT"
    )
    assert any(
        item.get("warning_code") == "POST_SELECTION_INFERENCE_RISK"
        for item in revised_result["warnings"]
        if isinstance(item, dict)
    )
    lineage = (await client.get(f"/api/v1/results/{revised_result['result_id']}/lineage")).json()
    assert any(
        edge["relation_type"] == "REVISED_FROM"
        and edge["from_id"] == base_execution_id
        and edge["to_id"] == revised_id
        for edge in lineage["edges"]
    )
