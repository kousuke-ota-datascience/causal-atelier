"""探索済み edge の条件付き係数を推定する。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from ..constants import SUPPORTED_ROBUST_SE
from .inference import records_to_frame
from .linear_model import (
    confidence_interval,
    fit_linear_regression,
    none_to_nan,
    normal_p_value,
    numeric_matrix,
)


@dataclass(frozen=True)
class EdgeEffectResult:
    """1 つの directed edge に対する条件付き係数の推定結果。

    Attributes:
        algorithm: Discovery algorithm that produced the edge.
        source: Source node.
        target: Target node.
        adjustment_set: Other parents of the target included in the regression.
        coefficient_standardized: Source coefficient on standardized data.
        coefficient_original_scale: Source coefficient on original-scale data.
        standard_error_standardized: Standard error on standardized data.
        standard_error_original_scale: Standard error on original-scale data.
        t_value: Original-scale coefficient divided by its standard error.
        ci_low_standardized: Lower CI bound on standardized data.
        ci_high_standardized: Upper CI bound on standardized data.
        ci_low_original_scale: Lower CI bound on original-scale data.
        ci_high_original_scale: Upper CI bound on original-scale data.
        p_value: Normal-approximation p-value.
        n_samples: Complete-case sample size.
        r_squared: Original-scale regression R-squared.
        condition_number: Original-scale design condition number.
    """

    algorithm: str
    source: str
    target: str
    adjustment_set: tuple[str, ...]
    coefficient_standardized: float
    coefficient_original_scale: float
    standard_error_standardized: float
    standard_error_original_scale: float
    t_value: float
    ci_low_standardized: float
    ci_high_standardized: float
    ci_low_original_scale: float
    ci_high_original_scale: float
    p_value: float
    n_samples: int
    r_squared: float
    condition_number: float


class EdgeWeightEstimator:
    """探索 graph の edge に対して条件付き線形係数を推定する。

    This estimator runs a local linear regression for each directed edge using
    the target node as outcome, the source node as focal regressor, and other
    parents of the target as adjustment variables. The estimated coefficient is
    an edge weight, not an ATE or ATT. It is causally interpretable only under
    strong structural assumptions about graph correctness, no unobserved
    confounding, linearity, and measurement.

    Args:
        standardized_frame: Analysis frame after z-scoring.
        original_frame: Analysis frame on the original scale.
        discovery_dir: Directory containing discovery ``edges.csv`` files.
        output_dir: Root output directory.
        algorithms: Discovery algorithms whose edges should be estimated.
        dropped_columns: Columns dropped from the standardized frame.
        robust_se: Robust standard error type for edge regressions.
        min_samples: Minimum complete-case sample size for an edge model.
    """

    def __init__(
        self,
        *,
        standardized_frame: pd.DataFrame,
        original_frame: pd.DataFrame,
        discovery_dir: Path,
        output_dir: Path,
        algorithms: tuple[str, ...],
        dropped_columns: pd.DataFrame,
        robust_se: str = "none",
        min_samples: int = 30,
    ) -> None:
        """estimator を初期化する。

        Args:
            standardized_frame: Z-scored analysis frame.
            original_frame: Original-scale analysis frame.
            discovery_dir: Discovery output directory.
            output_dir: Inference output directory.
            algorithms: Algorithms to read.
            dropped_columns: Dropped standardized columns.
            robust_se: Robust standard error type.
            min_samples: Minimum complete-case sample size.

        Raises:
            ValueError: If robust SE type or minimum sample size is invalid.
        """
        if robust_se not in SUPPORTED_ROBUST_SE:
            raise ValueError(f"robust_se must be one of {SUPPORTED_ROBUST_SE}: {robust_se}")
        if min_samples < 1:
            raise ValueError("min_samples must be positive")
        self.standardized_frame = standardized_frame
        self.original_frame = original_frame
        self.discovery_dir = discovery_dir
        self.output_dir = output_dir
        self.algorithms = algorithms
        self.dropped_columns = dropped_columns
        self.robust_se = robust_se
        self.min_samples = min_samples

    @property
    def edge_output_dir(self) -> Path:
        """mode 固有の出力ディレクトリを返す。

        Returns:
            Edge-weight output directory.
        """
        return self.output_dir / "edge_weight"

    def load_edges(self, algorithm: str) -> pd.DataFrame | None:
        """1 アルゴリズム分の edge table を読み込む。

        Args:
            algorithm: Discovery algorithm name.

        Returns:
            Edge table, or ``None`` when the file is absent.

        Raises:
            ValueError: If the edge table schema is invalid.
        """
        edge_path = self.discovery_dir / algorithm / "edges.csv"
        if not edge_path.exists():
            return None
        edges = pd.read_csv(edge_path)
        required = {"source", "target", "edge"}
        missing = required.difference(edges.columns)
        if missing:
            raise ValueError(f"{edge_path} is missing required columns: {sorted(missing)}")
        return edges

    def directed_edges(self, edges: pd.DataFrame) -> pd.DataFrame:
        """edge table から directed ``-->`` edge だけを抽出する。

        Args:
            edges: Edge table.

        Returns:
            Directed edge rows.
        """
        if edges.empty:
            return edges.copy()
        return edges.loc[edges["edge"].eq("-->")].copy()

    def parents_by_target(self, directed_edges: pd.DataFrame) -> dict[str, set[str]]:
        """各 target node を directed parent set に対応づける。

        Args:
            directed_edges: Directed edge table.

        Returns:
            Mapping from target to parent-node set.
        """
        parents: dict[str, set[str]] = {}
        for _, row in directed_edges.iterrows():
            source = str(row["source"])
            target = str(row["target"])
            parents.setdefault(target, set()).add(source)
        return parents

    def estimate_all_edge_coefficients(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """設定された全探索 edge の係数を推定する。

        Returns:
            Pair of effect table and skipped-edge table.

        Raises:
            FileNotFoundError: If no configured algorithm has an edge file.
        """
        records = []
        skipped_records = []
        found_edge_files = 0
        for algorithm in self.algorithms:
            loaded_edges = self.load_edges(algorithm)
            if loaded_edges is None:
                skipped_records.append(
                    {
                        "algorithm": algorithm,
                        "source": "",
                        "target": "",
                        "reason": "missing_edges_file",
                    }
                )
                continue
            found_edge_files += 1
            edges = self.directed_edges(loaded_edges)
            parents = self.parents_by_target(edges)
            for _, edge in edges.iterrows():
                source = str(edge["source"])
                target = str(edge["target"])
                missing_source = source not in self.standardized_frame.columns
                missing_target = target not in self.standardized_frame.columns
                if missing_source or missing_target:
                    if missing_source and missing_target:
                        reason = "missing_source_and_target"
                    elif missing_source:
                        reason = "missing_source"
                    else:
                        reason = "missing_target"
                    skipped_records.append(
                        {
                            "algorithm": algorithm,
                            "source": source,
                            "target": target,
                            "reason": reason,
                        }
                    )
                    continue

                adjustment_set = tuple(
                    sorted(
                        parent
                        for parent in parents.get(target, set()).difference({source})
                        if parent in self.standardized_frame.columns
                        and parent in self.original_frame.columns
                    )
                )
                result, skipped_reason = self.estimate_edge_coefficient(
                    algorithm=algorithm,
                    source=source,
                    target=target,
                    adjustment_set=adjustment_set,
                )
                if result is None:
                    skipped_records.append(
                        {
                            "algorithm": algorithm,
                            "source": source,
                            "target": target,
                            "reason": skipped_reason,
                        }
                    )
                else:
                    records.append(result.__dict__)

        if found_edge_files == 0:
            raise FileNotFoundError(
                f"No edges.csv files found under {self.discovery_dir} for algorithms: "
                f"{', '.join(self.algorithms)}"
            )

        columns = [
            "algorithm",
            "source",
            "target",
            "adjustment_set",
            "coefficient_standardized",
            "coefficient_original_scale",
            "standard_error_standardized",
            "standard_error_original_scale",
            "t_value",
            "ci_low_standardized",
            "ci_high_standardized",
            "ci_low_original_scale",
            "ci_high_original_scale",
            "p_value",
            "n_samples",
            "r_squared",
            "condition_number",
        ]
        effects = records_to_frame(records, columns)
        if not effects.empty:
            effects = effects.sort_values(["algorithm", "target", "source"]).reset_index(drop=True)
        skipped = records_to_frame(
            skipped_records,
            ["algorithm", "source", "target", "reason"],
        )
        return effects, skipped

    def estimate_all(self) -> pd.DataFrame:
        """全 edge coefficient を推定し、skip 状態を保持する。

        Returns:
            Edge-effect table.
        """
        effects, skipped_edges = self.estimate_all_edge_coefficients()
        self._last_skipped_edges = skipped_edges
        return effects

    def estimate_edge_coefficient(
        self,
        *,
        algorithm: str,
        source: str,
        target: str,
        adjustment_set: tuple[str, ...],
    ) -> tuple[EdgeEffectResult | None, str]:
        """1 つの local edge coefficient を推定する。

        Args:
            algorithm: Discovery algorithm name.
            source: Source node.
            target: Target node.
            adjustment_set: Additional target parents.

        Returns:
            Pair of result and skipped reason. The result is ``None`` when the
            edge cannot be estimated.
        """
        regressors = [source, *adjustment_set]
        used_columns = [target, *regressors]
        standardized = self.standardized_frame.loc[:, used_columns].dropna()
        original = self.original_frame.loc[:, used_columns].dropna()
        common_index = standardized.index.intersection(original.index)
        standardized = standardized.loc[common_index]
        original = original.loc[common_index]
        parameter_count = len(regressors) + 1
        if len(common_index) <= parameter_count or len(common_index) < self.min_samples:
            return None, "insufficient_sample_size"

        y_standardized = standardized[target].to_numpy(dtype=float)
        x_standardized = numeric_matrix(standardized, regressors)
        y_original = original[target].to_numpy(dtype=float)
        x_original = numeric_matrix(original, regressors)
        standardized_fit = fit_linear_regression(
            y_standardized,
            x_standardized,
            robust_se=self.robust_se,
        )
        original_fit = fit_linear_regression(
            y_original,
            x_original,
            robust_se=self.robust_se,
        )
        if standardized_fit.rank < parameter_count or original_fit.rank < parameter_count:
            return None, "rank_deficient"

        source_index = 1
        coefficient_standardized = float(standardized_fit.coefficients[source_index])
        standard_error_standardized = float(standardized_fit.standard_errors[source_index])
        coefficient_original = float(original_fit.coefficients[source_index])
        standard_error_original = float(original_fit.standard_errors[source_index])
        t_value = (
            coefficient_original / standard_error_original
            if standard_error_original > 0
            else np.nan
        )
        p_value = normal_p_value(float(t_value))
        ci_low_standardized, ci_high_standardized = confidence_interval(
            coefficient_standardized,
            standard_error_standardized,
        )
        ci_low_original, ci_high_original = confidence_interval(
            coefficient_original,
            standard_error_original,
        )

        return (
            EdgeEffectResult(
                algorithm=algorithm,
                source=source,
                target=target,
                adjustment_set=adjustment_set,
                coefficient_standardized=coefficient_standardized,
                coefficient_original_scale=coefficient_original,
                standard_error_standardized=standard_error_standardized,
                standard_error_original_scale=standard_error_original,
                t_value=float(t_value),
                ci_low_standardized=none_to_nan(ci_low_standardized),
                ci_high_standardized=none_to_nan(ci_high_standardized),
                ci_low_original_scale=none_to_nan(ci_low_original),
                ci_high_original_scale=none_to_nan(ci_high_original),
                p_value=p_value,
                n_samples=len(common_index),
                r_squared=original_fit.r_squared,
                condition_number=original_fit.condition_number,
            ),
            "",
        )


class CausalInference(EdgeWeightEstimator):
    """後方互換用の :class:`EdgeWeightEstimator` alias。

    Args:
        frame: Optional standardized frame retained for legacy callers.
        standardized_frame: Standardized frame.
        original_frame: Original-scale frame.
        discovery_dir: Discovery output directory.
        output_dir: Inference output directory.
        algorithms: Discovery algorithms to read.
        dropped_columns: Dropped standardized columns.
    """

    def __init__(
        self,
        *,
        frame: pd.DataFrame | None = None,
        standardized_frame: pd.DataFrame | None = None,
        original_frame: pd.DataFrame | None = None,
        discovery_dir: Path,
        output_dir: Path,
        algorithms: tuple[str, ...],
        dropped_columns: pd.DataFrame | None = None,
    ) -> None:
        """後方互換の edge-weight estimator を初期化する。

        Args:
            frame: Optional frame used as standardized data.
            standardized_frame: Standardized data.
            original_frame: Original-scale data.
            discovery_dir: Discovery output directory.
            output_dir: Inference output directory.
            algorithms: Algorithms to read.
            dropped_columns: Dropped-column table.

        Raises:
            ValueError: If neither ``frame`` nor ``standardized_frame`` is
                supplied.
        """
        if standardized_frame is None:
            if frame is None:
                raise ValueError("Either frame or standardized_frame must be provided.")
            standardized_frame = frame
        if original_frame is None:
            original_frame = standardized_frame
        if dropped_columns is None:
            dropped_columns = pd.DataFrame(columns=["column", "reason"])
        super().__init__(
            standardized_frame=standardized_frame,
            original_frame=original_frame,
            discovery_dir=discovery_dir,
            output_dir=output_dir,
            algorithms=algorithms,
            dropped_columns=dropped_columns,
        )
