"""因果探索が出力した edge table を読み込む。"""

from __future__ import annotations

from collections.abc import Collection
from pathlib import Path
import warnings

import pandas as pd


EDGE_COLUMNS = ["source", "target", "endpoint_source", "endpoint_target", "edge"]


def load_discovery_edges(
    discovery_dir: Path,
    algorithms: Collection[str],
    required: bool,
) -> pd.DataFrame:
    """因果探索 step が生成した directed edge を読み込む。

    Args:
        discovery_dir: Directory containing causal discovery outputs.
        algorithms: Algorithms whose edge files should be loaded.
        required: Whether missing edge files should raise an error.

    Returns:
        Data frame containing edge rows with an ``algorithm`` column.

    Raises:
        FileNotFoundError: If an edge file is required but missing.
        ValueError: If an edge file has an invalid schema.
    """
    records = []
    for algorithm in algorithms:
        edge_path = discovery_dir / algorithm / "edges.csv"
        if not edge_path.exists():
            if required:
                raise FileNotFoundError(f"missing graph edge file: {edge_path}")
            warnings.warn(f"missing graph edge file: {edge_path}", stacklevel=2)
            continue
        edges = pd.read_csv(edge_path)
        missing = {"source", "target", "edge"}.difference(edges.columns)
        if missing:
            raise ValueError(f"{edge_path} is missing required columns: {sorted(missing)}")
        copied = edges.copy()
        copied["algorithm"] = algorithm
        records.append(copied)
    if not records:
        return pd.DataFrame(columns=[*EDGE_COLUMNS, "algorithm"])
    return pd.concat(records, ignore_index=True)
