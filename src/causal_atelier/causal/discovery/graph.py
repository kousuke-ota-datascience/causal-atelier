"""因果探索 edge table の共通 schema utility。

探索側は causal-learn graph や重み付き隣接行列を ``edges.csv`` へ正規化し、
推論側はその ``edges.csv`` を読み込んで edge weight や graph-parent adjustment
に使う。この module は、その境界で使う edge 表現と report 補助処理を集約する。
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def endpoint_name(endpoint) -> str:
    """causal-learn endpoint を正規化した名前に変換する。

    Args:
        endpoint: causal-learn endpoint enum-like object.

    Returns:
        Lowercase endpoint name.
    """
    return endpoint.name.lower()


def edge_symbol(edge) -> str:
    """causal-learn の edge endpoint pair を text symbol に変換する。

    Args:
        edge: causal-learn graph edge.

    Returns:
        Symbol such as ``-->``, ``---``, ``<->``, ``o->``, or ``o-o``.
    """
    endpoint1 = edge.get_endpoint1().name
    endpoint2 = edge.get_endpoint2().name
    if endpoint1 == "TAIL" and endpoint2 == "ARROW":
        return "-->"
    if endpoint1 == "TAIL" and endpoint2 == "TAIL":
        return "---"
    if endpoint1 == "ARROW" and endpoint2 == "ARROW":
        return "<->"
    if endpoint1 == "CIRCLE" and endpoint2 == "ARROW":
        return "o->"
    if endpoint1 == "TAIL" and endpoint2 == "CIRCLE":
        return "--o"
    if endpoint1 == "CIRCLE" and endpoint2 == "CIRCLE":
        return "o-o"
    return f"{endpoint1}-{endpoint2}"


def graph_edge_records(graph) -> pd.DataFrame:
    """causal-learn graph を正規化済み edge record に変換する。

    Args:
        graph: causal-learn graph object exposing ``get_graph_edges``.

    Returns:
        Edge data frame with source, target, endpoints, and edge symbol.
    """
    records = []
    for edge in graph.get_graph_edges():
        records.append(
            {
                "source": edge.get_node1().get_name(),
                "target": edge.get_node2().get_name(),
                "endpoint_source": endpoint_name(edge.get_endpoint1()),
                "endpoint_target": endpoint_name(edge.get_endpoint2()),
                "edge": edge_symbol(edge),
            }
        )
    if not records:
        return pd.DataFrame(
            columns=["source", "target", "endpoint_source", "endpoint_target", "edge"]
        )
    return pd.DataFrame(records).sort_values(["source", "target"]).reset_index(drop=True)


def weight_matrix_edge_records(
    weight_matrix: np.ndarray,
    *,
    node_names: list[str],
    threshold: float,
) -> pd.DataFrame:
    """重み付き adjacency matrix を edge record に変換する。

    Args:
        weight_matrix: Matrix where rows are targets and columns are sources.
        node_names: Variable names in matrix order.
        threshold: Minimum absolute weight to include.

    Returns:
        Edge data frame including weights for selected matrix entries.
    """
    records = []
    for target_index, source_index in zip(*np.where(np.abs(weight_matrix) > threshold)):
        if source_index == target_index:
            continue
        records.append(
            {
                "source": node_names[source_index],
                "target": node_names[target_index],
                "endpoint_source": "tail",
                "endpoint_target": "arrow",
                "edge": "-->",
                "weight": float(weight_matrix[target_index, source_index]),
            }
        )
    columns = ["source", "target", "endpoint_source", "endpoint_target", "edge", "weight"]
    if not records:
        return pd.DataFrame(columns=columns)
    return pd.DataFrame(records).sort_values(["source", "target"]).reset_index(drop=True)


def adjacency_key(row: pd.Series) -> tuple[str, str]:
    """edge adjacency の順序不変 key を作る。

    Args:
        row: Edge record containing ``source`` and ``target``.

    Returns:
        Sorted ``(node_a, node_b)`` tuple.
    """
    source = str(row["source"])
    target = str(row["target"])
    return tuple(sorted((source, target)))


def mermaid_edge(row: pd.Series) -> str:
    """1 つの edge record を Mermaid flowchart edge として描画する。

    Args:
        row: Edge record containing ``source``, ``target``, and ``edge``.

    Returns:
        Mermaid edge line.
    """
    source = row["source"]
    target = row["target"]
    edge = row["edge"]
    if edge == "-->":
        return f"    {source}[{source}] --> {target}[{target}]"
    if edge == "---":
        return f"    {source}[{source}] --- {target}[{target}]"
    if edge == "<->":
        return f"    {source}[{source}] <--> {target}[{target}]"
    if edge == "o->":
        return f"    {source}[{source}] o--> {target}[{target}]"
    if edge == "--o":
        return f"    {source}[{source}] --o {target}[{target}]"
    return f"    {source}[{source}] -. {edge} .- {target}[{target}]"


def dataframe_to_markdown(frame: pd.DataFrame) -> str:
    """data frame を最小限の Markdown table として描画する。

    Args:
        frame: Data frame to render.

    Returns:
        Markdown table string, or a no-edge message for empty frames.
    """
    if frame.empty:
        return "_No edges discovered._"

    columns = list(frame.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for _, row in frame.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)
