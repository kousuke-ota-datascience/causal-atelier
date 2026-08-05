"""Reproducible Golden Path against the running Docker Compose product stack.

Run from the repository root:
    python tests/product/compose_golden_path_smoke.py
"""

from __future__ import annotations

import csv
import io
import math
import random
import time
import uuid

import httpx


BASE_URL = "http://127.0.0.1:8000/api/v1"
TIMEOUT_SECONDS = 120


def _synthetic_csv() -> bytes:
    randomizer = random.Random(20260805)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["coupon", "past_sales", "sales"])
    for _ in range(240):
        past_sales = randomizer.gauss(0, 1)
        propensity = 1 / (1 + math.exp(-0.45 * past_sales))
        coupon = int(randomizer.random() < propensity)
        sales = 2.5 * coupon + 1.2 * past_sales + randomizer.gauss(0, 1)
        writer.writerow([coupon, past_sales, sales])
    return output.getvalue().encode()


def _require(response: httpx.Response) -> dict:  # type: ignore[type-arg]
    if not response.is_success:
        raise AssertionError(f"{response.request.method} {response.request.url}: "
                             f"{response.status_code} {response.text}")
    return response.json()


def _wait_for_executions(client: httpx.Client, execution_ids: list[str]) -> None:
    deadline = time.monotonic() + TIMEOUT_SECONDS
    pending = set(execution_ids)
    while pending and time.monotonic() < deadline:
        for execution_id in list(pending):
            execution = _require(client.get(f"/executions/{execution_id}"))
            if execution["status"] == "FAILED":
                raise AssertionError(f"execution failed: {execution}")
            if execution["status"] in {"SUCCEEDED", "CANCELLED"}:
                pending.remove(execution_id)
        if pending:
            time.sleep(0.5)
    if pending:
        raise TimeoutError(f"executions did not finish: {sorted(pending)}")


def main() -> None:
    run_key = uuid.uuid4().hex
    with httpx.Client(base_url=BASE_URL, timeout=30) as client:
        project = _require(client.post("/projects", json={
            "name": f"Golden Path {run_key[:8]}",
            "topic": "coupon effect",
            "objective": "discover a graph and estimate ATE",
            "memo": "reproducible Compose smoke test",
        }))
        project_id = project["project_id"]
        upload_headers = {"Idempotency-Key": f"dataset-{run_key}"}
        upload_data = {
            "dataset_key": "synthetic_sales", "name": "Synthetic sales",
            "version_label": run_key, "source_note": "seed=20260805",
        }
        dataset = _require(client.post(
            f"/projects/{project_id}/dataset-versions",
            headers=upload_headers,
            data=upload_data,
            files={"file": ("synthetic.csv", _synthetic_csv(), "text/csv")},
        ))
        repeated = _require(client.post(
            f"/projects/{project_id}/dataset-versions",
            headers=upload_headers,
            data=upload_data,
            files={"file": ("synthetic.csv", _synthetic_csv(), "text/csv")},
        ))
        assert repeated == dataset
        assert _require(client.get(
            f"/dataset-versions/{dataset['dataset_version_id']}/preview?limit=5"
        ))["rows"]

        discovery = _require(client.post(
            f"/projects/{project_id}/execution-batches",
            headers={"Idempotency-Key": f"discovery-{run_key}"},
            json={
                "operation": "DISCOVERY",
                "dataset_version_id": dataset["dataset_version_id"],
                "input_graph_version_id": None,
                "objective": "compare discovery sensitivity",
                "rationale": "PC alpha grid plus GES",
                "analysis_spec": {
                    "feature_columns": ["coupon", "past_sales", "sales"],
                    "constraints": {"required_edges": [["coupon", "sales"]]},
                },
                "variants": [
                    {"algorithm_or_estimator": "pc", "parameters": {"alpha": 0.01}, "random_seed": 42},
                    {"algorithm_or_estimator": "pc", "parameters": {"alpha": 0.05}, "random_seed": 42},
                    {"algorithm_or_estimator": "ges", "parameters": {}, "random_seed": 42},
                ],
                "code_version": "compose-smoke", "runtime_versions": {"python": "3.12"},
            },
        ))
        discovery_ids = [item["execution_id"] for item in discovery["executions"]]
        _wait_for_executions(client, discovery_ids)
        discovery_results = [
            _require(client.get(f"/executions/{execution_id}/results"))["items"][0]
            for execution_id in discovery_ids
        ]
        assert all(result["scientific_status"] == "VALID" for result in discovery_results)
        comparison = _require(client.post("/comparisons/query", json={
            "project_id": project_id,
            "result_ids": [result["result_id"] for result in discovery_results],
        }))
        assert comparison["operation"] == "DISCOVERY"

        source = discovery_results[0]
        graph = _require(client.post(
            f"/projects/{project_id}/graph-versions",
            headers={"Idempotency-Key": f"graph-{run_key}"},
            json={
                "source_result_id": source["result_id"], "parent_graph_version_id": None,
                "name": "fixed discovery graph", "graph_type": "CPDAG",
                "graph": source["payload"], "edit_rationale": "required edge plus sensitivity check",
                "fix_immediately": True,
            },
        ))
        assert graph["status"] == "FIXED"

        estimation = _require(client.post(
            f"/projects/{project_id}/execution-batches",
            headers={"Idempotency-Key": f"estimation-{run_key}"},
            json={
                "operation": "ESTIMATION", "dataset_version_id": dataset["dataset_version_id"],
                "input_graph_version_id": graph["graph_version_id"],
                "objective": "estimate coupon ATE", "rationale": "triangulate estimators",
                "analysis_spec": {
                    "treatment": "coupon", "outcome": "sales", "estimand": "ATE",
                    "target_population": None, "adjustment_set": ["past_sales"],
                    "assumptions": ["exchangeability", "positivity"], "inference_options": {},
                },
                "variants": [
                    {"algorithm_or_estimator": "ols", "parameters": {}, "random_seed": 42},
                    {"algorithm_or_estimator": "ipw", "parameters": {}, "random_seed": 42},
                    {"algorithm_or_estimator": "aipw", "parameters": {}, "random_seed": 42},
                ],
                "code_version": "compose-smoke", "runtime_versions": {"python": "3.12"},
            },
        ))
        estimation_ids = [item["execution_id"] for item in estimation["executions"]]
        _wait_for_executions(client, estimation_ids)
        estimation_results = [
            _require(client.get(f"/executions/{execution_id}/results"))["items"][0]
            for execution_id in estimation_ids
        ]
        assert all(result["scientific_status"] == "VALID" for result in estimation_results)
        assert all(result["artifact_ids"] for result in estimation_results)
        _require(client.post("/comparisons/query", json={
            "project_id": project_id,
            "result_ids": [result["result_id"] for result in estimation_results],
        }))

        selected = estimation_results[0]
        _require(client.post(f"/projects/{project_id}/annotations", json={
            "target_result_id": selected["result_id"], "target_graph_version_id": None,
            "statement": "retain the OLS estimate", "rationale": "estimator agreement",
            "assumptions": ["exchangeability", "positivity"],
            "limitations": ["synthetic data"],
        }))
        lineage = _require(client.get(f"/results/{selected['result_id']}/lineage"))
        assert {node["node_type"] for node in lineage["nodes"]} >= {
            "Project", "DatasetVersion", "Execution", "Result", "GraphVersion", "Artifact", "Annotation"
        }
        artifact_id = selected["artifact_ids"][0]
        assert client.get(f"/artifacts/{artifact_id}/download").is_success
        manifest = _require(client.post(f"/results/{selected['result_id']}/export"))
        assert manifest["manifest_version"] == "1.0"
        print({
            "project_id": project_id,
            "dataset_version_id": dataset["dataset_version_id"],
            "discovery_results": len(discovery_results),
            "estimation_results": len(estimation_results),
            "root_result_id": selected["result_id"],
            "status": "PASS",
        })


if __name__ == "__main__":
    main()
