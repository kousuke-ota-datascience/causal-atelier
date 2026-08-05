"""ariadne-discover CLI command."""

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
        prog="ariadne-discover",
        description="Run causal discovery on a pre-processed tabular dataset.",
    )
    parser.add_argument("--dataset", required=True, type=Path, help="Path to dataset (.parquet or .csv)")
    parser.add_argument("--algorithm", required=True, help="Discovery algorithm (pc, ges, lingam, notears)")
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory to write outputs")
    parser.add_argument("--alpha", type=float, default=0.05, help="Significance level for PC (default: 0.05)")
    parser.add_argument("--random-seed", type=int, default=None)
    parser.add_argument("--params", type=json.loads, default={}, metavar="JSON", help="Additional parameters as JSON")
    parser.add_argument("--no-background-knowledge", action="store_true")
    args = parser.parse_args(argv)

    dataset_path: Path = args.dataset.resolve()
    output_dir: Path = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not dataset_path.exists():
        print(f"ERROR: Dataset not found: {dataset_path}", file=sys.stderr)
        return 3

    dataset_hash = _sha256_file(dataset_path)
    params = {
        "alpha": args.alpha,
        "use_background_knowledge": not args.no_background_knowledge,
        **args.params,
    }

    try:
        from ariadne.product.ports.scientific_core import DiscoveryInput
        from ariadne.scientific.core_adapter import ScientificCoreAdapter

        core = ScientificCoreAdapter()
        input_ = DiscoveryInput(
            dataset_path=dataset_path,
            algorithm=args.algorithm,
            parameters=params,
            random_seed=args.random_seed,
        )
        output = core.run_discovery(input_, output_dir)
    except Exception as exc:
        print(f"ERROR: Scientific core execution failed: {exc}", file=sys.stderr)
        return 4

    # Build and write manifest
    import ariadne
    version = getattr(ariadne, "__version__", "0.1.0")

    from ariadne.interfaces.cli.manifest import DiscoveryManifest
    manifest = DiscoveryManifest(
        manifest_version="1",
        ariadne_version=version,
        algorithm=args.algorithm,
        dataset_path=str(dataset_path),
        dataset_hash=dataset_hash,
        parameters=params,
        random_seed=args.random_seed,
        scientific_status=output.scientific_status.value,
        graph_json=output.graph_json,
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
