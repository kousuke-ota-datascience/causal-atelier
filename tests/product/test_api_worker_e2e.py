from __future__ import annotations

import json
from pathlib import Path

from ariadne.adapters.local_artifact_store import LocalArtifactStore
from ariadne.interfaces.web_api import dependencies
from ariadne.interfaces.worker.execution_processor import ExecutionProcessor
from ariadne.product.domain.enums import ScientificStatus
from ariadne.product.ports.scientific_core import DiscoveryOutput, EstimationOutput


class FakeScientificCore:
    def run_discovery(self, input_, output_dir):  # type: ignore[no-untyped-def]
        graph={"graph_type":"CPDAG","nodes":["coupon","past_sales","sales"],"edges":[
            {"source":"past_sales","target":"coupon","endpoint_source":"TAIL","endpoint_target":"ARROW"},
            {"source":"past_sales","target":"sales","endpoint_source":"TAIL","endpoint_target":"ARROW"},
            {"source":"coupon","target":"sales","endpoint_source":"TAIL","endpoint_target":"ARROW"},
        ]}
        path=output_dir/"graph.json";path.write_text(json.dumps(graph),encoding="utf-8")
        return DiscoveryOutput(ScientificStatus.VALID,"CPDAG",graph,{"edge_count":3},{},[],[path])

    def run_estimation(self, input_, output_dir):  # type: ignore[no-untyped-def]
        path=output_dir/"effect.json";path.write_text('{"estimate": 2.0}',encoding="utf-8")
        return EstimationOutput(
            scientific_status=ScientificStatus.VALID,
            payload={"estimate":2.0,"standard_error":.2,"confidence_interval":[1.6,2.4]},
            summary={"estimate":2.0,"standard_error":.2,"confidence_interval":[1.6,2.4]},
            diagnostics={"sample_size":{"n_complete":40},"overlap":{"ps_min":.2,"ps_max":.8}},
            warnings=[],artifacts=[path],
        )


class NegativeScientificCore(FakeScientificCore):
    def run_estimation(self, input_, output_dir):  # type: ignore[no-untyped-def]
        return EstimationOutput(
            scientific_status=ScientificStatus.NOT_IDENTIFIED,
            payload={"estimate":None},summary={"estimate":None},diagnostics={},
            warnings=["not identified"],artifacts=[],
        )


class FailingScientificCore(FakeScientificCore):
    def run_estimation(self, input_, output_dir):  # type: ignore[no-untyped-def]
        raise RuntimeError("technical failure sentinel")


def process_next(tmp_path: Path, core=None):  # type: ignore[no-untyped-def]
    with dependencies._uow_context() as uow:
        execution=uow.executions.claim_next("test-worker")
        uow.commit()
    assert execution is not None
    ExecutionProcessor(
        dependencies._uow_context,core or FakeScientificCore(),LocalArtifactStore(tmp_path/"objects")
    ).process(execution)


import pytest


@pytest.mark.anyio
async def test_api_worker_golden_path_and_contracts(client, product_env):  # type: ignore[no-untyped-def]
    _,tmp_path=product_env
    bad=await client.post('/api/v1/projects',json={"name":"x","unknown":1})
    assert bad.status_code==400 and bad.json()["error"]["code"]=="INVALID_REQUEST"
    project=(await client.post('/api/v1/projects',json={"name":"Sales","topic":"Coupon","objective":"ATE","memo":None})).json()
    project_id=project["project_id"]
    assert (await client.get('/api/v1/projects')).json()["items"][0]["project_id"]==project_id
    content=b"coupon,past_sales,sales\n"+b"0,1,3\n1,2,6\n"*20
    headers={"Idempotency-Key":"dataset-1"}
    files={"file":("sales.csv",content,"text/csv")}
    data={"dataset_key":"sales","version_label":"v1","name":"Sales data","source_note":"synthetic"}
    first=await client.post(f'/api/v1/projects/{project_id}/dataset-versions',files=files,data=data,headers=headers)
    assert first.status_code==201
    second=await client.post(f'/api/v1/projects/{project_id}/dataset-versions',files=files,data=data,headers=headers)
    assert second.status_code==201 and second.json()==first.json()
    dataset_id=first.json()["dataset_version_id"]
    assert (await client.get(f'/api/v1/dataset-versions/{dataset_id}/preview')).json()["rows"]

    discovery_body={"operation":"DISCOVERY","dataset_version_id":dataset_id,"input_graph_version_id":None,
        "objective":"Discover","rationale":"Compare","analysis_spec":{"feature_columns":["coupon","past_sales","sales"],"constraints":{}},
        "variants":[{"algorithm_or_estimator":"pc","parameters":{"alpha":.01},"random_seed":42},
                    {"algorithm_or_estimator":"pc","parameters":{"alpha":.05},"random_seed":42},
                    {"algorithm_or_estimator":"ges","parameters":{},"random_seed":42}],
        "code_version":"test","runtime_versions":{"python":"test"}}
    accepted=await client.post(f'/api/v1/projects/{project_id}/execution-batches',json=discovery_body,headers={"Idempotency-Key":"disc-1"})
    assert accepted.status_code==201 and len(accepted.json()["executions"])==3
    for _ in range(3):process_next(tmp_path)
    executions=(await client.get(f'/api/v1/projects/{project_id}/executions')).json()["items"]
    assert all(item["status"]=="SUCCEEDED" for item in executions)
    discovery_results=[]
    for execution in executions:
        discovery_results.extend((await client.get(f'/api/v1/executions/{execution["execution_id"]}/results')).json()["items"])
    comparison=await client.post('/api/v1/comparisons/query',json={"project_id":project_id,"result_ids":[r["result_id"] for r in discovery_results]})
    assert comparison.status_code==200 and comparison.json()["operation"]=="DISCOVERY"
    source=discovery_results[0]
    graph=await client.post(f'/api/v1/projects/{project_id}/graph-versions',headers={"Idempotency-Key":"graph-1"},json={
        "source_result_id":source["result_id"],"parent_graph_version_id":None,"name":"Selected",
        "graph_type":"CPDAG","graph":source["payload"],"edit_rationale":"Stable across runs","fix_immediately":True,
    })
    assert graph.status_code==201 and graph.json()["status"]=="FIXED"
    fixed_update=await client.patch(
        f'/api/v1/graph-versions/{graph.json()["graph_version_id"]}',
        json={"graph":source["payload"],"edit_rationale":"must fail"},
    )
    assert fixed_update.status_code==409 and fixed_update.json()["error"]["code"]=="GRAPH_ALREADY_FIXED"
    other_project=(await client.post('/api/v1/projects',json={"name":"Other"})).json()
    cross_graph=await client.post(
        f'/api/v1/projects/{other_project["project_id"]}/graph-versions',
        headers={"Idempotency-Key":"cross-graph"},json={
            "source_result_id":source["result_id"],"parent_graph_version_id":None,"name":"Invalid",
            "graph_type":"CPDAG","graph":source["payload"],"edit_rationale":None,"fix_immediately":False,
        },
    )
    assert cross_graph.status_code==422 and cross_graph.json()["error"]["code"]=="PROJECT_BOUNDARY_VIOLATION"
    cross_annotation=await client.post(
        f'/api/v1/projects/{other_project["project_id"]}/annotations',json={
            "target_result_id":source["result_id"],"target_graph_version_id":None,
            "statement":"Invalid project","rationale":None,"assumptions":[],"limitations":[],
        },
    )
    assert cross_annotation.status_code==422

    draft=(await client.post(
        f'/api/v1/projects/{project_id}/graph-versions',headers={"Idempotency-Key":"draft-1"},json={
            "source_result_id":source["result_id"],"parent_graph_version_id":None,"name":"Draft",
            "graph_type":"CPDAG","graph":source["payload"],"edit_rationale":None,"fix_immediately":False,
        },
    )).json()

    estimation={"operation":"ESTIMATION","dataset_version_id":dataset_id,"input_graph_version_id":graph.json()["graph_version_id"],
        "objective":"Estimate","rationale":"Compare estimators","analysis_spec":{"treatment":"coupon","outcome":"sales","estimand":"ATE","target_population":None,"adjustment_set":["past_sales"],"assumptions":["exchangeability"],"inference_options":{}},
        "variants":[{"algorithm_or_estimator":"ols","parameters":{},"random_seed":42},{"algorithm_or_estimator":"ipw","parameters":{},"random_seed":42}],
        "code_version":"test","runtime_versions":{"python":"test"}}
    draft_rejected=await client.post(
        f'/api/v1/projects/{project_id}/execution-batches',
        json={**estimation,"input_graph_version_id":draft["graph_version_id"]},
        headers={"Idempotency-Key":"draft-estimation"},
    )
    assert draft_rejected.status_code==422
    response=await client.post(f'/api/v1/projects/{project_id}/execution-batches',json=estimation,headers={"Idempotency-Key":"est-1"})
    assert response.status_code==201
    process_next(tmp_path);process_next(tmp_path)
    est_ids=[item["execution_id"] for item in response.json()["executions"]]
    est_results=[(await client.get(f'/api/v1/executions/{value}/results')).json()["items"][0] for value in est_ids]
    assert all(value["scientific_status"]=="VALID" for value in est_results)
    assert all(value["artifact_ids"] for value in est_results)
    target=est_results[0]["result_id"]
    annotation=await client.post(f'/api/v1/projects/{project_id}/annotations',json={
        "target_result_id":target,"target_graph_version_id":None,"statement":"Adopt OLS",
        "rationale":"Stable","assumptions":["exchangeability"],"limitations":["synthetic"],
    })
    assert annotation.status_code==201
    lineage=(await client.get(f'/api/v1/results/{target}/lineage')).json()
    assert {node["node_type"] for node in lineage["nodes"]}>={"Result","Execution","DatasetVersion","GraphVersion","Artifact","Annotation"}
    artifact_id=next(node["entity_id"] for node in lineage["nodes"] if node["node_type"]=="Artifact")
    assert (await client.get(f'/api/v1/artifacts/{artifact_id}/download')).status_code==200
    export_headers={"Idempotency-Key":"export-1"}
    exported=await client.post(f'/api/v1/results/{target}/export',headers=export_headers)
    assert exported.json()["manifest_version"]=="1.0"
    assert (await client.post(f'/api/v1/results/{target}/export',headers=export_headers)).json()==exported.json()
    conflict=await client.post(
        f'/api/v1/results/{est_results[1]["result_id"]}/export',headers=export_headers
    )
    assert conflict.status_code==409 and conflict.json()["error"]["code"]=="IDEMPOTENCY_CONFLICT"

    single_variant={**estimation,"variants":[
        {"algorithm_or_estimator":"difference_in_means","parameters":{},"random_seed":42}
    ]}
    negative=await client.post(
        f'/api/v1/projects/{project_id}/execution-batches',json=single_variant,
        headers={"Idempotency-Key":"negative-1"},
    )
    negative_id=negative.json()["executions"][0]["execution_id"]
    process_next(tmp_path,NegativeScientificCore())
    negative_execution=(await client.get(f'/api/v1/executions/{negative_id}')).json()
    negative_result=(await client.get(f'/api/v1/executions/{negative_id}/results')).json()["items"][0]
    assert negative_execution["status"]=="SUCCEEDED"
    assert negative_result["scientific_status"]=="NOT_IDENTIFIED"

    failing=await client.post(
        f'/api/v1/projects/{project_id}/execution-batches',json={
            **estimation,"variants":[{"algorithm_or_estimator":"aipw","parameters":{},"random_seed":42}],
        },headers={"Idempotency-Key":"failure-1"},
    )
    failing_id=failing.json()["executions"][0]["execution_id"]
    with dependencies._uow_context() as uow:
        snapshot_before=uow.executions.get(failing_id).snapshot_hash
    process_next(tmp_path,FailingScientificCore())
    failed=(await client.get(f'/api/v1/executions/{failing_id}')).json()
    assert failed["status"]=="FAILED" and "technical failure sentinel" in failed["last_error_summary"]
    assert (await client.get(f'/api/v1/executions/{failing_id}/results')).json()["items"]==[]
    assert (await client.post(f'/api/v1/executions/{failing_id}/retry')).status_code==204
    with dependencies._uow_context() as uow:
        retried=uow.executions.get(failing_id)
        assert retried.status.value=="QUEUED" and retried.snapshot_hash==snapshot_before

    cancelled=await client.post(
        f'/api/v1/projects/{project_id}/execution-batches',json=single_variant,
        headers={"Idempotency-Key":"cancel-1"},
    )
    cancelled_id=cancelled.json()["executions"][0]["execution_id"]
    assert (await client.post(f'/api/v1/executions/{cancelled_id}/cancel')).status_code==204
    assert (await client.get(f'/api/v1/executions/{cancelled_id}')).json()["status"]=="CANCELLED"
