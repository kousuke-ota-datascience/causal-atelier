"""Standalone estimation CLI; scientific negative outcomes exit zero."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

import yaml
from pydantic import ValidationError

from ariadne.interfaces.cli.config_schema import EstimationCliConfig
from ariadne.interfaces.cli.manifest import CliManifest


def _hash(path: Path) -> str:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="ariadne-estimate")
    parser.add_argument("--config", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        config = EstimationCliConfig.model_validate(yaml.safe_load(args.config.read_text(encoding="utf-8")))
    except (OSError, yaml.YAMLError, ValidationError, TypeError) as exc:
        print(f"ERROR: invalid config: {exc}", file=sys.stderr)
        return 2
    dataset, graph = config.dataset.resolve(), config.graph.resolve()
    if not dataset.is_file() or not graph.is_file():
        print("ERROR: dataset or graph not found", file=sys.stderr)
        return 3
    dataset_hash, graph_hash = _hash(dataset), _hash(graph)
    if (config.dataset_hash and config.dataset_hash != dataset_hash) or (config.graph_hash and config.graph_hash != graph_hash):
        print("ERROR: input hash mismatch", file=sys.stderr)
        return 3
    try:
        from ariadne.product.domain.errors import InvalidAnalysisSpec, UnsupportedEstimator
        from ariadne.product.ports.scientific_core import EstimationInput
        from ariadne.scientific.core_adapter import ScientificCoreAdapter
        output = ScientificCoreAdapter().run_estimation(EstimationInput(
            dataset_path=dataset, graph_path=graph, estimator=config.estimator,
            parameters=config.parameters, random_seed=config.random_seed,
            analysis_spec=config.analysis_spec,
        ), config.output_dir)
    except (InvalidAnalysisSpec, UnsupportedEstimator) as exc:
        print(f"ERROR: invalid config: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"ERROR: scientific core technical failure: {exc}", file=sys.stderr)
        return 4
    try:
        import ariadne
        manifest = CliManifest(
            manifest_version="1.0", operation="ESTIMATION",
            dataset={"content_hash": dataset_hash, "location": str(dataset)},
            graph={"content_hash": graph_hash, "location": str(graph)},
            algorithm_or_estimator=config.estimator, parameters=config.parameters,
            analysis_spec=config.analysis_spec, random_seed=config.random_seed,
            code_version=getattr(ariadne, "__version__", "0.1.0"),
            runtime_versions={"python": platform.python_version()},
            scientific_status=output.scientific_status.value, result_summary=output.summary,
            artifacts=[{"location": str(path), "content_hash": _hash(path)} for path in output.artifacts],
            warnings=output.warnings,
        )
        config.output_dir.mkdir(parents=True, exist_ok=True)
        (config.output_dir / "manifest.json").write_text(
            json.dumps(manifest.to_dict(), sort_keys=True, indent=2), encoding="utf-8"
        )
    except OSError as exc:
        print(f"ERROR: output write failure: {exc}", file=sys.stderr)
        return 5
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
