"""Standalone discovery CLI; it never creates Web/API Execution IDs."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

import yaml
from pydantic import ValidationError

from ariadne.interfaces.cli.config_schema import DiscoveryCliConfig
from ariadne.interfaces.cli.manifest import CliManifest


def _hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="ariadne-discover")
    parser.add_argument("--config", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        raw = yaml.safe_load(args.config.read_text(encoding="utf-8"))
        config = DiscoveryCliConfig.model_validate(raw)
    except (OSError, yaml.YAMLError, ValidationError, TypeError) as exc:
        print(f"ERROR: invalid config: {exc}", file=sys.stderr)
        return 2
    dataset = config.dataset.resolve()
    if not dataset.is_file():
        print(f"ERROR: dataset not found: {dataset}", file=sys.stderr)
        return 3
    dataset_hash = _hash(dataset)
    if config.dataset_hash and config.dataset_hash != dataset_hash:
        print("ERROR: dataset hash mismatch", file=sys.stderr)
        return 3
    try:
        from ariadne.product.domain.errors import InvalidAnalysisSpec, UnsupportedAlgorithm
        from ariadne.product.ports.scientific_core import DiscoveryInput
        from ariadne.scientific.core_adapter import ScientificCoreAdapter
        output = ScientificCoreAdapter().run_discovery(DiscoveryInput(
            dataset_path=dataset, algorithm=config.algorithm, parameters=config.parameters,
            random_seed=config.random_seed, analysis_spec=config.analysis_spec,
        ), config.output_dir)
    except (InvalidAnalysisSpec, UnsupportedAlgorithm) as exc:
        print(f"ERROR: invalid config: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"ERROR: scientific core technical failure: {exc}", file=sys.stderr)
        return 4
    try:
        artifacts = [{"location": str(path), "content_hash": _hash(path)} for path in output.artifacts]
        manifest = CliManifest(
            manifest_version="1.0", operation="DISCOVERY",
            dataset={"content_hash": dataset_hash, "location": str(dataset)}, graph=None,
            algorithm_or_estimator=config.algorithm, parameters=config.parameters,
            analysis_spec=config.analysis_spec, random_seed=config.random_seed,
            code_version=_version(), runtime_versions={"python": platform.python_version()},
            scientific_status=output.scientific_status.value, result_summary=output.summary,
            artifacts=artifacts, warnings=output.warnings,
        )
        config.output_dir.mkdir(parents=True, exist_ok=True)
        (config.output_dir / "manifest.json").write_text(
            json.dumps(manifest.to_dict(), sort_keys=True, indent=2), encoding="utf-8"
        )
    except OSError as exc:
        print(f"ERROR: output write failure: {exc}", file=sys.stderr)
        return 5
    return 0


def _version() -> str:
    import ariadne
    return getattr(ariadne, "__version__", "0.1.0")


if __name__ == "__main__":
    raise SystemExit(main())
