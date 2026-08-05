from __future__ import annotations

from collections import Counter

import numpy as np
import pandas as pd

from ..graph import adjacency_key

from ..algorithms import CausalDiscovery


class CausalDiscoveryDiagnostics:
    """PC ベース因果探索の事後 diagnostic を実行する。

    Args:
        causal_discovery: Configured discovery runner used for repeated PC runs.
    """

    def __init__(self, causal_discovery: CausalDiscovery) -> None:
        """diagnostics を初期化する。

        Args:
            causal_discovery: Configured discovery runner used for repeated PC
                runs.
        """
        self.causal_discovery = causal_discovery

    def run_pc_alpha_sensitivity(
        self,
        frame: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """設定された alpha grid で PC を繰り返し実行する。

        Args:
            frame: Standardized discovery input.

        Returns:
            Pair of summary data frame and edge-level data frame across alpha
            values.
        """
        summary_columns = ["alpha", "status", "edges", "message"]
        edge_columns = [
            "alpha",
            "source",
            "target",
            "endpoint_source",
            "endpoint_target",
            "edge",
        ]
        summary_records = []
        edge_records = []

        for alpha in self.causal_discovery.alpha_grid:
            try:
                _, edges = self.causal_discovery.run_pc(frame, alpha=alpha)
            except Exception as exc:
                summary_records.append(
                    {
                        "alpha": alpha,
                        "status": "failed",
                        "edges": 0,
                        "message": f"{type(exc).__name__}: {exc}",
                    }
                )
                continue

            summary_records.append(
                {
                    "alpha": alpha,
                    "status": "ok",
                    "edges": len(edges),
                    "message": "",
                }
            )
            for _, edge in edges.iterrows():
                record = {"alpha": alpha}
                record.update(edge.to_dict())
                edge_records.append(record)

        return (
            pd.DataFrame(summary_records, columns=summary_columns),
            pd.DataFrame(edge_records, columns=edge_columns),
        )

    def bootstrap_pc_edge_stability(
        self,
        frame: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """bootstrap resampling により PC edge stability を推定する。

        Args:
            frame: Standardized discovery input.

        Returns:
            Pair of edge-stability data frame and bootstrap-failure data frame.
        """
        stability_columns = [
            "source",
            "target",
            "selection_count",
            "successful_bootstrap_samples",
            "selection_probability",
            "example_edge",
        ]
        failure_columns = ["bootstrap_iteration", "message"]
        if self.causal_discovery.bootstrap_samples <= 0:
            return (
                pd.DataFrame(columns=stability_columns),
                pd.DataFrame(columns=failure_columns),
            )

        sample_size = max(
            2,
            int(round(len(frame) * self.causal_discovery.bootstrap_sample_fraction)),
        )
        rng = np.random.default_rng(self.causal_discovery.random_seed)
        edge_counts: Counter[tuple[str, str]] = Counter()
        example_edges: dict[tuple[str, str], str] = {}
        failure_records = []

        for bootstrap_iteration in range(self.causal_discovery.bootstrap_samples):
            sample_seed = int(rng.integers(0, np.iinfo(np.int32).max))
            sample = frame.sample(
                n=sample_size,
                replace=True,
                random_state=sample_seed,
            ).reset_index(drop=True)
            try:
                _, edges = self.causal_discovery.run_pc(
                    sample,
                    alpha=self.causal_discovery.alpha,
                )
            except Exception as exc:
                failure_records.append(
                    {
                        "bootstrap_iteration": bootstrap_iteration,
                        "message": f"{type(exc).__name__}: {exc}",
                    }
                )
                continue

            for _, edge in edges.iterrows():
                key = adjacency_key(edge)
                edge_counts[key] += 1
                example_edges.setdefault(key, str(edge["edge"]))

        successful_samples = self.causal_discovery.bootstrap_samples - len(failure_records)
        stability_records = []
        for (source, target), count in sorted(edge_counts.items()):
            stability_records.append(
                {
                    "source": source,
                    "target": target,
                    "selection_count": count,
                    "successful_bootstrap_samples": successful_samples,
                    "selection_probability": (
                        count / successful_samples if successful_samples else np.nan
                    ),
                    "example_edge": example_edges[(source, target)],
                }
            )

        return (
            pd.DataFrame(stability_records, columns=stability_columns),
            pd.DataFrame(failure_records, columns=failure_columns),
        )


def variable_diagnostics(
    frame: pd.DataFrame,
    variable_metadata: pd.DataFrame,
) -> pd.DataFrame:
    """単変量 diagnostic を計算し、変数 metadata に結合する。

    Args:
        frame: Discovery feature frame.
        variable_metadata: Metadata generated from the feature configuration.

    Returns:
        Metadata with mean, standard deviation, range, zero share, and number
        of unique values.
    """
    records = []
    for column in frame.columns:
        values = frame[column]
        records.append(
            {
                "variable": column,
                "mean": float(values.mean()),
                "std": float(values.std()),
                "min": float(values.min()),
                "max": float(values.max()),
                "zero_share": float(values.eq(0).mean()),
                "unique_values": int(values.nunique(dropna=True)),
            }
        )
    diagnostics = pd.DataFrame(records)
    return variable_metadata.merge(diagnostics, on="variable", how="left")
