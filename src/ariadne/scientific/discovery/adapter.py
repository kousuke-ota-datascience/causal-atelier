"""Scientific Core adapter – wraps legacy causal discovery algorithms.

This adapter converts between the Product domain's ScientificCorePort interface
and the existing causal discovery implementation. It deliberately does not import
any Product repositories, ORM models, or Execution state.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from ariadne.product.domain.enums import ScientificStatus
from ariadne.product.ports.scientific_core import DiscoveryInput, DiscoveryOutput

# Supported single-algorithm discovery calls
_SINGLE_ALGO_ALGORITHMS = {"pc", "ges", "lingam", "notears"}


class DiscoveryAdapter:
    """Adapter from DiscoveryInput → DiscoveryOutput using legacy CausalDiscovery."""

    def run(self, input_: DiscoveryInput, output_dir: Path) -> DiscoveryOutput:
        output_dir.mkdir(parents=True, exist_ok=True)

        df = _load_dataset(input_.dataset_path)
        algorithm = input_.algorithm.lower()
        params = input_.parameters

        try:
            from ariadne.causal.discovery.algorithms import CausalDiscovery

            runner = CausalDiscovery(
                alpha=float(params.get("alpha", 0.05)),
                use_background_knowledge=bool(params.get("use_background_knowledge", False)),
                algorithms=(algorithm,),
                random_seed=input_.random_seed or 42,
            )
            results = runner.run_all(df)
        except Exception as exc:
            return DiscoveryOutput(
                scientific_status=ScientificStatus.SCIENTIFIC_ERROR,
                warnings=[str(exc)],
            )

        result = results.get(algorithm)
        if result is None or result.status == "failed":
            msg = result.message if result else f"Algorithm {algorithm!r} not found"
            return DiscoveryOutput(
                scientific_status=ScientificStatus.SCIENTIFIC_ERROR,
                warnings=[msg],
            )

        if result.status == "skipped":
            return DiscoveryOutput(
                scientific_status=ScientificStatus.SCIENTIFIC_ERROR,
                warnings=[result.message],
            )

        # Build graph JSON from edges DataFrame
        edges = result.edges
        graph_json = _edges_to_graph_json(edges, algorithm)

        if edges.empty:
            scientific_status = ScientificStatus.GRAPH_EMPTY
        else:
            scientific_status = ScientificStatus.GRAPH_PRODUCED

        # Save edges artifact
        artifact_paths: list[Path] = []
        edges_path = output_dir / f"{algorithm}_edges.csv"
        edges.to_csv(edges_path, index=False)
        artifact_paths.append(edges_path)

        # Save graph JSON artifact
        graph_path = output_dir / f"{algorithm}_graph.json"
        graph_path.write_text(json.dumps(graph_json, indent=2))
        artifact_paths.append(graph_path)

        summary = {
            "algorithm": algorithm,
            "edge_count": len(edges),
            "node_count": int(edges[["source", "target"]].stack().nunique()) if not edges.empty else 0,
        }

        return DiscoveryOutput(
            scientific_status=scientific_status,
            graph_json=graph_json,
            summary=summary,
            artifacts=artifact_paths,
        )


def _load_dataset(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported dataset format: {suffix!r}")


def _edges_to_graph_json(edges: pd.DataFrame, algorithm: str) -> dict[str, Any]:
    """Convert normalized edge DataFrame to graph JSON."""
    if edges.empty:
        return {"algorithm": algorithm, "nodes": [], "edges": []}

    nodes = sorted(set(edges["source"].tolist()) | set(edges["target"].tolist()))
    edge_list = []
    for _, row in edges.iterrows():
        edge_list.append({
            "source": row["source"],
            "target": row["target"],
            "edge_type": row.get("edge_type", "-->"),
        })

    return {
        "algorithm": algorithm,
        "nodes": nodes,
        "edges": edge_list,
    }
