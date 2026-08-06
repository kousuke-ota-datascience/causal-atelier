"""Shared implementation for local identify/refute/sensitivity commands."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from ariadne.interfaces.cli.config_schema import (
    IdentificationCliConfig, RefutationCliConfig, SensitivityCliConfig,
)
from ariadne.interfaces.cli.manifest import CliManifest
from ariadne.product.domain.analysis_spec import causal_question_hash, validate_analysis_spec
from ariadne.product.domain.enums import ExecutionOperation
from ariadne.product.domain.errors import DomainError
from ariadne.product.ports.scientific_core import (
    IdentificationInput, RefutationInput, SensitivityInput,
)
from ariadne.scientific.core_adapter import ScientificCoreAdapter


def run_stage(operation: ExecutionOperation, argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=f"ariadne-{operation.value.lower()}")
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args(argv)
    model = {
        ExecutionOperation.IDENTIFICATION: IdentificationCliConfig,
        ExecutionOperation.REFUTATION: RefutationCliConfig,
        ExecutionOperation.SENSITIVITY: SensitivityCliConfig,
    }[operation]
    try:
        config = model.model_validate(yaml.safe_load(args.config.read_text(encoding="utf-8")))
        validate_analysis_spec(operation, config.analysis_spec)
    except (OSError, TypeError, yaml.YAMLError, ValidationError, DomainError, ValueError) as exc:
        print(f"ERROR: invalid config: {exc}", file=sys.stderr); return 2
    required = [config.dataset, config.graph]
    if hasattr(config, "upstream_result"):
        required.append(config.upstream_result)
    if not all(path.is_file() for path in required):
        print("ERROR: input artifact not found", file=sys.stderr); return 3
    try:
        core = ScientificCoreAdapter()
        if operation == ExecutionOperation.IDENTIFICATION:
            results = core.run_identification(IdentificationInput(
                dataset_path=config.dataset, graph_path=config.graph, method=config.method,
                parameters=config.parameters, random_seed=config.random_seed,
                analysis_spec=config.analysis_spec,
            ), config.output_dir)
            upstream_ref = None
        else:
            upstream = json.loads(config.upstream_result.read_text(encoding="utf-8"))
            if operation == ExecutionOperation.REFUTATION:
                results = core.run_refutation(RefutationInput(
                    dataset_path=config.dataset, graph_path=config.graph,
                    base_result=upstream, method=config.method, parameters=config.parameters,
                    random_seed=config.random_seed, analysis_spec=config.analysis_spec,
                ), config.output_dir)
            else:
                results = core.run_sensitivity(SensitivityInput(
                    dataset_path=config.dataset, graph_path=config.graph,
                    base_result=upstream, dimension=config.dimension, parameters=config.parameters,
                    random_seed=config.random_seed, analysis_spec=config.analysis_spec,
                ), config.output_dir)
            upstream_ref = f"sha256:{_hash(config.upstream_result)}"
    except ValueError as exc:
        print(f"ERROR: invalid scientific input: {exc}", file=sys.stderr); return 2
    except Exception as exc:
        print(f"ERROR: scientific core technical failure: {exc}", file=sys.stderr); return 4
    try:
        config.output_dir.mkdir(parents=True, exist_ok=True)
        artifacts = [
            {"location": str(artifact.path), "content_hash": _hash(artifact.path)}
            for result in results for artifact in result.artifacts
        ]
        manifest = CliManifest(
            manifest_version="2.0", operation=operation.value,
            dataset={"location": str(config.dataset), "content_hash": _hash(config.dataset)},
            graph={"location": str(config.graph), "content_hash": _hash(config.graph)},
            algorithm_or_estimator=getattr(config, "method", getattr(config, "dimension", "")),
            parameters=config.parameters, analysis_spec=config.analysis_spec,
            random_seed=config.random_seed, code_version="0.1.0",
            runtime_versions={"python": platform.python_version()},
            scientific_status=results[0].scientific_status.value,
            result_summary={"results": [
                {"result_type": result.result_type.value, "scientific_status": result.scientific_status.value,
                 "summary": result.summary, "payload": result.payload}
                for result in results
            ]}, artifacts=artifacts,
            warnings=[str(warning) for result in results for warning in result.warnings],
            analysis_mode=config.analysis_spec["analysis_mode"],
            causal_question_hash=causal_question_hash(config.analysis_spec),
            graph_origin=getattr(config, "graph_origin", None),
            upstream_result_reference=upstream_ref,
            identification_status=(results[0].scientific_status.value if operation == ExecutionOperation.IDENTIFICATION else None),
            eligibility_status=(results[1].scientific_status.value if operation == ExecutionOperation.IDENTIFICATION else None),
            backend_version="ariadne/0.1.0",
        )
        (config.output_dir / "manifest.json").write_text(
            json.dumps(manifest.to_dict(), sort_keys=True, indent=2), encoding="utf-8"
        )
    except OSError as exc:
        print(f"ERROR: output write failure: {exc}", file=sys.stderr); return 5
    return 0


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
