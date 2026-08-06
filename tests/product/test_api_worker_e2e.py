from __future__ import annotations

import json
from pathlib import Path

import pytest

from ariadne.adapters.local_artifact_store import LocalArtifactStore
from ariadne.interfaces.web_api import dependencies
from ariadne.interfaces.worker.execution_processor import ExecutionProcessor
from ariadne.product.domain.enums import ResultType, ScientificStatus
from ariadne.product.ports.scientific_core import ScientificResultBatch, ScientificResultDescriptor


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
                {"status": "PASS"}, {"status": "PASS", "checks": []},
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
                {"status": "PASS"}, {"status": "PASS", "checks": []},
            ),
        ])


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
