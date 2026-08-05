"""ariadne-estimate CLI command."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ariadne-estimate",
        description="Estimate causal effects using a graph and dataset.",
    )
    parser.add_argument("--dataset", required=True, type=Path)
    parser.add_argument("--graph", required=True, type=Path, help="Path to graph JSON")
    parser.add_argument("--estimator", required=True, help="Estimator name (e.g. aipw, drl)")
    parser.add_argument("--treatment", required=True)
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--random-seed", type=int, default=None)
    parser.add_argument("--params", type=json.loads, default={}, metavar="JSON")
    parser.add_argument("--spec", type=json.loads, default={}, metavar="JSON", help="Additional analysis spec as JSON")
    args = parser.parse_args(argv)

    dataset_path: Path = args.dataset.resolve()
    graph_path: Path = args.graph.resolve()
    output_dir: Path = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not dataset_path.exists():
        print(f"ERROR: Dataset not found: {dataset_path}", file=sys.stderr)
        return 3
    if not graph_path.exists():
        print(f"ERROR: Graph not found: {graph_path}", file=sys.stderr)
        return 3

    dataset_hash = _sha256_file(dataset_path)
    graph_hash = _sha256_file(graph_path)

    analysis_spec = {
        "treatment": args.treatment,
        "outcome": args.outcome,
        **args.spec,
    }

    try:
        from ariadne.product.ports.scientific_core import EstimationInput
        from ariadne.scientific.core_adapter import ScientificCoreAdapter

        core = ScientificCoreAdapter()
        input_ = EstimationInput(
            dataset_path=dataset_path,
            graph_path=graph_path,
            estimator=args.estimator,
            parameters=args.params,
            random_seed=args.random_seed,
            analysis_spec=analysis_spec,
        )
        output = core.run_estimation(input_, output_dir)
    except Exception as exc:
        print(f"ERROR: Scientific core execution failed: {exc}", file=sys.stderr)
        return 4

    import ariadne
    version = getattr(ariadne, "__version__", "0.1.0")

    from ariadne.interfaces.cli.manifest import EstimationManifest
    manifest = EstimationManifest(
        manifest_version="1",
        ariadne_version=version,
        estimator=args.estimator,
        dataset_path=str(dataset_path),
        dataset_hash=dataset_hash,
        graph_path=str(graph_path),
        graph_hash=graph_hash,
        parameters=args.params,
        analysis_spec=analysis_spec,
        random_seed=args.random_seed,
        scientific_status=output.scientific_status.value,
        payload=output.payload,
        summary=output.summary,
        output_dir=str(output_dir),
        artifacts=[str(p) for p in output.artifacts],
        warnings=output.warnings,
    )

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest.__dict__, indent=2, default=str))

    print(f"Scientific status: {output.scientific_status.value}")
    print(f"Manifest written to: {manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
