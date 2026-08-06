from __future__ import annotations

import json
from pathlib import Path

import yaml

from ariadne.interfaces.cli.discovery import main as discovery_main
from ariadne.interfaces.cli.estimation import main as estimation_main
from ariadne.product.domain.enums import ScientificStatus
from ariadne.product.ports.scientific_core import DiscoveryOutput, EstimationOutput
from ariadne.scientific.core_adapter import ScientificCoreAdapter


def test_discovery_cli_writes_portable_manifest_without_web_identity(
    tmp_path: Path, monkeypatch,
) -> None:  # type: ignore[no-untyped-def]
    dataset = tmp_path / "data.csv"
    dataset.write_text("x,y\n1,2\n2,3\n", encoding="utf-8")
    output_dir = tmp_path / "output"

    def run(_self, _input, destination):  # type: ignore[no-untyped-def]
        artifact = destination / "pc_graph.json"
        destination.mkdir(parents=True)
        artifact.write_text('{"graph_type":"CPDAG","nodes":[],"edges":[]}', encoding="utf-8")
        return DiscoveryOutput(
            scientific_status=ScientificStatus.GENERATED,
            graph_type="CPDAG",
            graph_json={"graph_type": "CPDAG", "nodes": [], "edges": []},
            summary={"edge_count": 0}, diagnostics={}, warnings=["empty graph"],
            artifacts=[artifact],
        )

    monkeypatch.setattr(ScientificCoreAdapter, "run_discovery", run)
    config = tmp_path / "discovery.yaml"
    config.write_text(yaml.safe_dump({
            "config_version": "2.0", "dataset": str(dataset), "algorithm": "pc",
        "parameters": {"alpha": 0.05},
            "analysis_spec": {"schema_version":"causal-analysis-spec/2","analysis_mode":"EXPLORATORY","research_context":{},"causal_question":{},"causal_design":{"adjustment_set":[],"assumptions":[]},"operation_spec":{"feature_columns":["x","y"],"constraints":{},"expected_graph_type":None},"validation_override":None},
        "random_seed": 42, "output_dir": str(output_dir),
    }), encoding="utf-8")

    assert discovery_main(["--config", str(config)]) == 0
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["manifest_version"] == "2.0"
    assert manifest["scientific_status"] == "GENERATED"
    assert manifest["dataset"]["content_hash"]
    assert manifest["artifacts"][0]["content_hash"]
    assert "execution_id" not in manifest


def test_estimation_cli_scientific_negative_result_exits_zero(
    tmp_path: Path, monkeypatch,
) -> None:  # type: ignore[no-untyped-def]
    dataset = tmp_path / "data.csv"
    dataset.write_text("t,y\n0,1\n1,2\n", encoding="utf-8")
    graph = tmp_path / "graph.json"
    graph.write_text('{"graph_type":"DAG","nodes":["t","y"],"edges":[]}', encoding="utf-8")
    output_dir = tmp_path / "output"
    identification = tmp_path / "identification.json"
    identification.write_text(json.dumps({
        "identification_status": "IDENTIFIED", "eligibility_status": "PASS",
        "analysis_spec": {
            "causal_design": {"identification_strategy": "RANDOMIZED", "adjustment_set": []},
        },
        "result_summary": {"results": [
            {"result_type": "IDENTIFICATION_RESULT", "payload": {
                "strategy": "RANDOMIZED", "selected_adjustment_set": [],
            }},
            {"result_type": "DATA_ELIGIBILITY_RESULT", "payload": {
                "status": "PASS", "checks": [
                    {"check_code": "TREATMENT_PREVALENCE", "status": "PASS"},
                ],
                "inferred_types": {
                    "treatment": {"type": "BINARY", "evidence": {}},
                    "outcome": {"type": "CONTINUOUS", "evidence": {}},
                },
            }},
        ]},
    }), encoding="utf-8")

    def run(_self, _input, _destination):  # type: ignore[no-untyped-def]
        return EstimationOutput(
            scientific_status=ScientificStatus.REQUIRES_REVIEW,
            payload={"estimate": None}, summary={"estimate": None}, diagnostics={},
            warnings=["not identified"], artifacts=[],
        )

    monkeypatch.setattr(ScientificCoreAdapter, "run_estimation", run)
    config = tmp_path / "estimation.yaml"
    config.write_text(yaml.safe_dump({
        "config_version": "2.0", "dataset": str(dataset), "graph": str(graph),
        "graph_origin": "USER_DEFINED", "identification_manifest": str(identification),
        "estimator": "ols", "parameters": {},
        "analysis_spec": {"schema_version":"causal-analysis-spec/2","analysis_mode":"EXPLORATORY","research_context":{},"causal_question":{"population":"rows","treatment":"t","comparator":"0","outcome":"y","analysis_unit":"row","treatment_time":"t0","outcome_window":"t1","estimand":"ATE"},"causal_design":{"identification_strategy":"RANDOMIZED","adjustment_set":[],"assumptions":[]},"operation_spec":{"estimator":"ols","inference_options":{}},"validation_override":None},
        "random_seed": 42, "output_dir": str(output_dir),
    }), encoding="utf-8")

    assert estimation_main(["--config", str(config)]) == 0
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["scientific_status"] == "REQUIRES_REVIEW"
    assert manifest["graph"]["content_hash"]
    assert manifest["result_summary"] == {"estimate": None}
    assert manifest["scientific_warnings"] == []


def test_estimation_cli_uses_api_compatible_type_error_code(
    tmp_path: Path, capsys,
) -> None:  # type: ignore[no-untyped-def]
    dataset = tmp_path / "data.csv"
    dataset.write_text("t,y\n0,0\n1,1\n", encoding="utf-8")
    graph = tmp_path / "graph.json"
    graph.write_text('{"graph_type":"DAG","nodes":["t","y"],"edges":[]}', encoding="utf-8")
    identification = tmp_path / "identification.json"
    identification.write_text(json.dumps({
        "identification_status": "IDENTIFIED", "eligibility_status": "PASS",
        "analysis_spec": {"causal_design": {"identification_strategy": "RANDOMIZED"}},
        "result_summary": {"results": [
            {"result_type": "IDENTIFICATION_RESULT", "payload": {
                "strategy": "RANDOMIZED", "selected_adjustment_set": [],
            }},
            {"result_type": "DATA_ELIGIBILITY_RESULT", "payload": {
                "checks": [],
                "inferred_types": {
                    "treatment": {"type": "BINARY", "evidence": {}},
                    "outcome": {"type": "BINARY", "evidence": {}},
                },
            }},
        ]},
    }), encoding="utf-8")
    config = tmp_path / "estimation.yaml"
    config.write_text(yaml.safe_dump({
        "config_version": "2.0", "dataset": str(dataset), "graph": str(graph),
        "graph_origin": "USER_DEFINED", "identification_manifest": str(identification),
        "estimator": "ols", "parameters": {},
        "analysis_spec": {"schema_version":"causal-analysis-spec/2","analysis_mode":"EXPLORATORY","research_context":{},"causal_question":{"population":"rows","treatment":"t","comparator":"0","outcome":"y","analysis_unit":"row","treatment_time":"t0","outcome_window":"t1","estimand":"ATE"},"causal_design":{"identification_strategy":"RANDOMIZED","adjustment_set":[],"assumptions":[]},"operation_spec":{"estimator":"ols","inference_options":{}},"validation_override":None},
        "random_seed": 42, "output_dir": str(tmp_path / "output"),
    }), encoding="utf-8")

    assert estimation_main(["--config", str(config)]) == 2
    assert "ESTIMATOR_OUTCOME_TYPE_INCOMPATIBLE" in capsys.readouterr().err


def test_cli_rejects_unknown_config_field(tmp_path: Path) -> None:
    config = tmp_path / "invalid.yaml"
    config.write_text(yaml.safe_dump({
        "config_version": "2.0", "dataset": "missing.csv", "algorithm": "pc",
        "analysis_spec": {}, "output_dir": "out", "unknown": True,
    }), encoding="utf-8")
    assert discovery_main(["--config", str(config)]) == 2
