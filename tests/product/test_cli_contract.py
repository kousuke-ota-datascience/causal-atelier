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
            scientific_status=ScientificStatus.VALID,
            graph_type="CPDAG",
            graph_json={"graph_type": "CPDAG", "nodes": [], "edges": []},
            summary={"edge_count": 0}, diagnostics={}, warnings=["empty graph"],
            artifacts=[artifact],
        )

    monkeypatch.setattr(ScientificCoreAdapter, "run_discovery", run)
    config = tmp_path / "discovery.yaml"
    config.write_text(yaml.safe_dump({
        "config_version": "1.0", "dataset": str(dataset), "algorithm": "pc",
        "parameters": {"alpha": 0.05},
        "analysis_spec": {"feature_columns": ["x", "y"], "constraints": {}},
        "random_seed": 42, "output_dir": str(output_dir),
    }), encoding="utf-8")

    assert discovery_main(["--config", str(config)]) == 0
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["manifest_version"] == "1.0"
    assert manifest["scientific_status"] == "VALID"
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

    def run(_self, _input, _destination):  # type: ignore[no-untyped-def]
        return EstimationOutput(
            scientific_status=ScientificStatus.NOT_IDENTIFIED,
            payload={"estimate": None}, summary={"estimate": None}, diagnostics={},
            warnings=["not identified"], artifacts=[],
        )

    monkeypatch.setattr(ScientificCoreAdapter, "run_estimation", run)
    config = tmp_path / "estimation.yaml"
    config.write_text(yaml.safe_dump({
        "config_version": "1.0", "dataset": str(dataset), "graph": str(graph),
        "estimator": "ols", "parameters": {},
        "analysis_spec": {
            "treatment": "t", "outcome": "y", "estimand": "ATE",
            "target_population": None, "adjustment_set": [], "assumptions": [],
            "inference_options": {},
        },
        "random_seed": 42, "output_dir": str(output_dir),
    }), encoding="utf-8")

    assert estimation_main(["--config", str(config)]) == 0
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["scientific_status"] == "NOT_IDENTIFIED"
    assert manifest["graph"]["content_hash"]
    assert manifest["result_summary"] == {"estimate": None}


def test_cli_rejects_unknown_config_field(tmp_path: Path) -> None:
    config = tmp_path / "invalid.yaml"
    config.write_text(yaml.safe_dump({
        "config_version": "1.0", "dataset": "missing.csv", "algorithm": "pc",
        "analysis_spec": {}, "output_dir": "out", "unknown": True,
    }), encoding="utf-8")
    assert discovery_main(["--config", str(config)]) == 2
