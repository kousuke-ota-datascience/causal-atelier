"""DB-free adapter for causal discovery algorithms."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from ariadne.product.domain.enums import GraphType, ScientificStatus
from ariadne.product.domain.errors import (
    InvalidAnalysisSpec,
    ScientificCoreExecutionError,
    UnsupportedAlgorithm,
)
from ariadne.product.domain.graph_semantics import canonical_graph
from ariadne.product.ports.scientific_core import DiscoveryInput, DiscoveryOutput

_GRAPH_TYPES = {"pc": GraphType.CPDAG, "ges": GraphType.CPDAG, "lingam": GraphType.DAG, "notears": GraphType.DAG}
_PARAMETERS = {
    "pc": {"alpha", "pc_indep_test", "bootstrap_samples"},
    "ges": {"ges_max_p", "ges_score_func"},
    "lingam": set(),
    "notears": {"notears_threshold"},
}
_SPEC_FIELDS = {"feature_columns", "constraints", "expected_graph_type"}


class DiscoveryAdapter:
    def run(self, input_: DiscoveryInput, output_dir: Path) -> DiscoveryOutput:
        algorithm = input_.algorithm.lower()
        if algorithm not in _GRAPH_TYPES:
            raise UnsupportedAlgorithm(input_.algorithm)
        unknown = set(input_.parameters) - _PARAMETERS[algorithm]
        if unknown:
            raise InvalidAnalysisSpec(f"Unknown {algorithm} parameters: {sorted(unknown)}")
        unknown_spec = set(input_.analysis_spec) - _SPEC_FIELDS
        if unknown_spec:
            raise InvalidAnalysisSpec(f"Unknown discovery analysis fields: {sorted(unknown_spec)}")

        frame = _load_dataset(input_.dataset_path)
        columns = input_.analysis_spec.get("feature_columns")
        if not isinstance(columns, list) or not columns:
            raise InvalidAnalysisSpec("analysis_spec.feature_columns must be a non-empty list")
        if len(columns) != len(set(columns)):
            raise InvalidAnalysisSpec("feature_columns must be unique")
        missing = [column for column in columns if column not in frame.columns]
        if missing:
            raise InvalidAnalysisSpec(f"feature columns are missing: {missing}")
        frame = frame.loc[:, columns]
        if frame.empty:
            raise InvalidAnalysisSpec("discovery dataset must contain at least one row")

        params = input_.parameters
        try:
            from ariadne.causal.discovery.algorithms import CausalDiscovery

            runner = CausalDiscovery(
                alpha=float(params.get("alpha", 0.05)),
                use_background_knowledge=False,
                algorithms=(algorithm,),
                random_seed=input_.random_seed if input_.random_seed is not None else 42,
                pc_indep_test=str(params.get("pc_indep_test", "fisherz")),
                bootstrap_samples=int(params.get("bootstrap_samples", 0)),
                notears_threshold=float(params.get("notears_threshold", 0.3)),
                ges_max_p=params.get("ges_max_p"),
                ges_score_func=str(params.get("ges_score_func", "local_score_BIC")),
            )
            result = runner.run_all(frame)[algorithm]
        except (InvalidAnalysisSpec, UnsupportedAlgorithm):
            raise
        except Exception as exc:
            raise ScientificCoreExecutionError(
                f"{algorithm} discovery failed: {type(exc).__name__}: {exc}"
            ) from exc
        if result.status != "ok":
            raise ScientificCoreExecutionError(
                f"{algorithm} discovery failed: {result.message or result.status}"
            )

        graph_type = _GRAPH_TYPES[algorithm]
        expected_graph_type = input_.analysis_spec.get("expected_graph_type")
        if expected_graph_type is not None and expected_graph_type != graph_type.value:
            raise InvalidAnalysisSpec(
                f"expected_graph_type={expected_graph_type!r} does not match {graph_type.value!r}"
            )
        graph = _edges_to_graph_json(result.edges, graph_type, columns)
        graph, constraint_warnings = _apply_constraints(
            graph, input_.analysis_spec.get("constraints", {})
        )
        graph = canonical_graph(graph_type, graph)

        output_dir.mkdir(parents=True, exist_ok=True)
        graph_path = output_dir / f"{algorithm}_graph.json"
        graph_path.write_text(json.dumps(graph, sort_keys=True, indent=2), encoding="utf-8")
        edges_path = output_dir / f"{algorithm}_edges.csv"
        pd.DataFrame(graph["edges"]).to_csv(edges_path, index=False)
        warnings = list(constraint_warnings)
        if not graph["edges"]:
            warnings.append("No edges were discovered under the specified conditions.")
        return DiscoveryOutput(
            scientific_status=ScientificStatus.VALID,
            graph_type=graph_type.value,
            graph_json=graph,
            summary={"algorithm": algorithm.upper(), "node_count": len(columns), "edge_count": len(graph["edges"])},
            diagnostics={"feature_columns": columns, "constraints_applied": bool(input_.analysis_spec.get("constraints"))},
            warnings=warnings,
            artifacts=[graph_path, edges_path],
        )


def _load_dataset(path: Path) -> pd.DataFrame:
    try:
        if path.suffix.lower() == ".parquet":
            return pd.read_parquet(path)
        if path.suffix.lower() == ".csv":
            return pd.read_csv(path)
    except Exception as exc:
        raise ScientificCoreExecutionError(f"Unable to read dataset: {exc}") from exc
    raise InvalidAnalysisSpec(f"Unsupported dataset format: {path.suffix!r}")


def _edges_to_graph_json(edges: pd.DataFrame, graph_type: GraphType, nodes: list[str]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for row in edges.to_dict(orient="records"):
        record = {
            "source": str(row["source"]),
            "target": str(row["target"]),
            "endpoint_source": str(row.get("endpoint_source", "tail")).upper(),
            "endpoint_target": str(row.get("endpoint_target", "arrow")).upper(),
        }
        if "weight" in row and pd.notna(row["weight"]):
            record["weight"] = float(row["weight"])
        records.append(record)
    return {"graph_type": graph_type.value, "nodes": list(nodes), "edges": records}


def _edge_from_constraint(value: Any) -> tuple[str, str]:
    if isinstance(value, dict) and set(value) >= {"source", "target"}:
        return str(value["source"]), str(value["target"])
    if isinstance(value, (list, tuple)) and len(value) == 2:
        return str(value[0]), str(value[1])
    raise InvalidAnalysisSpec("edge constraints must contain source and target")


def _apply_constraints(graph: dict[str, Any], constraints: Any) -> tuple[dict[str, Any], list[str]]:
    if constraints in (None, {}):
        return graph, []
    if not isinstance(constraints, dict):
        raise InvalidAnalysisSpec("constraints must be an object")
    unknown = set(constraints) - {"required_edges", "forbidden_edges", "temporal_tiers"}
    if unknown:
        raise InvalidAnalysisSpec(f"Unknown graph constraints: {sorted(unknown)}")
    nodes = set(graph["nodes"])
    forbidden = {_edge_from_constraint(value) for value in constraints.get("forbidden_edges", [])}
    required = {_edge_from_constraint(value) for value in constraints.get("required_edges", [])}
    if any(a not in nodes or b not in nodes or a == b for a, b in forbidden | required):
        raise InvalidAnalysisSpec("graph constraints must reference distinct feature columns")
    edges = [edge for edge in graph["edges"] if (edge["source"], edge["target"]) not in forbidden]
    present = {(edge["source"], edge["target"]) for edge in edges}
    for source, target in sorted(required - present):
        edges.append({"source": source, "target": target, "endpoint_source": "TAIL", "endpoint_target": "ARROW"})

    tiers = constraints.get("temporal_tiers", [])
    if tiers:
        if not isinstance(tiers, list) or not all(isinstance(tier, list) for tier in tiers):
            raise InvalidAnalysisSpec("temporal_tiers must be a list of node lists")
        tier_by_node: dict[str, int] = {}
        for index, tier in enumerate(tiers):
            for node in tier:
                if node not in nodes or node in tier_by_node:
                    raise InvalidAnalysisSpec("temporal tiers contain an unknown or duplicate node")
                tier_by_node[node] = index
        constrained: list[dict[str, Any]] = []
        for edge in edges:
            left = tier_by_node.get(edge["source"])
            right = tier_by_node.get(edge["target"])
            if left is not None and right is not None and left > right:
                continue
            constrained.append(edge)
        edges = constrained
    return {**graph, "edges": edges}, ["Graph constraints were explicitly applied."]


__all__ = ["DiscoveryAdapter", "_edges_to_graph_json"]
