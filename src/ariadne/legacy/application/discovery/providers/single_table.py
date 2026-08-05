"""SingleTable input provider for causal discovery."""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Any

import pandas as pd

from ariadne.application.discovery.dto import (
    DiscoveryRequest,
    PreparedDiscoveryInput,
)
from ariadne.preprocessing.common import drop_collinear_columns


def _load_table(table_path: Path) -> pd.DataFrame:
    """Load a CSV or Parquet file.

    Args:
        table_path: Path to the file.

    Returns:
        Loaded DataFrame.

    Raises:
        ValueError: If the file format is unsupported.
    """
    suffix = table_path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(table_path)
    if suffix in (".parquet", ".pq"):
        return pd.read_parquet(table_path)
    raise ValueError(
        f"Unsupported file format: {suffix!r}. "
        "SingleTableDiscoveryInputProvider supports .csv and .parquet."
    )


def _apply_missing_value_policy(frame: pd.DataFrame, policy: str) -> pd.DataFrame:
    """Apply missing-value policy to a frame.

    Args:
        frame: Input frame.
        policy: ``"fail"`` to raise on missing values; ``"drop"`` to drop rows.

    Returns:
        Frame with policy applied.

    Raises:
        ValueError: If policy is ``"fail"`` and missing values are present.
    """
    if not frame.isnull().any().any():
        return frame
    if policy == "fail":
        missing_cols = frame.columns[frame.isnull().any()].tolist()
        raise ValueError(
            f"Missing values found in columns {missing_cols}. "
            "Use missing_values='drop' to drop rows with missing values."
        )
    if policy == "drop":
        return frame.dropna()
    raise ValueError(f"Unknown missing_values policy: {policy!r}. Use 'fail' or 'drop'.")


def _build_simple_variable_metadata(columns: list[str]) -> pd.DataFrame:
    """Build a minimal variable metadata frame for single-table input."""
    return pd.DataFrame(
        {
            "variable": columns,
            "role": "covariate",
            "data_type": "continuous",
            "transform": "identity",
            "background_tier": None,
            "used_in_discovery": True,
            "fisherz_caution": False,
            "source_table": "single_table",
            "source_column": columns,
            "window": None,
            "aggregation": None,
        }
    )


def _standardize_zscore(frame: pd.DataFrame) -> pd.DataFrame:
    """Apply z-score standardisation column-wise."""
    std = frame.std()
    zero_std = std[std == 0].index.tolist()
    if zero_std:
        warnings.warn(
            f"Constant columns dropped during z-score standardisation: {zero_std}",
            stacklevel=2,
        )
        frame = frame.drop(columns=zero_std)
        std = std.drop(zero_std)
    mean = frame.mean()
    return (frame - mean) / std


class SingleTableDiscoveryInputProvider:
    """Prepares a single analysis-ready table for causal discovery.

    Reads one CSV or Parquet file where each row is one analysis unit.
    Does not require campaign IDs, pre-treatment weeks, or any Complete
    Journey tables.

    Provider options (``request.input_specification.options``):

    - ``table_path`` (str, required): Path to the CSV or Parquet file.
    - ``columns`` (list[str], optional): Columns to select; all numeric columns
      if omitted.
    - ``unit_id`` (str, optional): ID column to drop before analysis (default: none).
    - ``missing_values`` (str, optional): ``"fail"`` (default) or ``"drop"``.
    - ``standardization`` (str | None, optional): ``"zscore"`` or ``None`` (default).
    - ``collinearity_threshold`` (float, optional): Drop collinear columns above
      this absolute correlation threshold; None to skip (default: None).

    Args:
        request: Discovery request.
    """

    def __init__(self, request: DiscoveryRequest) -> None:
        self._request = request

    def prepare(self, request: DiscoveryRequest) -> PreparedDiscoveryInput:
        """Load, validate, and normalise a single analysis table.

        Args:
            request: Discovery request.

        Returns:
            Normalised discovery input.

        Raises:
            ValueError: If table_path is missing, columns are not found, or
                validation fails.
        """
        opts: dict[str, Any] = dict(request.input_specification.options)

        table_path_raw = opts.get("table_path")
        if table_path_raw is None:
            raise ValueError(
                "SingleTableDiscoveryInputProvider requires 'table_path' in provider options."
            )
        table_path = request.project_root / Path(str(table_path_raw))
        if not table_path.exists():
            raise ValueError(f"table_path does not exist: {table_path}")

        raw = _load_table(table_path)

        unit_id: str | None = opts.get("unit_id")
        if unit_id is not None and unit_id in raw.columns:
            raw = raw.drop(columns=[unit_id])

        columns: list[str] | None = opts.get("columns")
        if columns:
            missing = [c for c in columns if c not in raw.columns]
            if missing:
                raise ValueError(f"Requested columns not found in table: {missing}")
            raw = raw[columns]
        else:
            # Select only numeric columns
            raw = raw.select_dtypes(include="number")

        # Numeric compatibility check
        non_numeric = [c for c in raw.columns if not pd.api.types.is_numeric_dtype(raw[c])]
        if non_numeric:
            raise ValueError(
                f"Non-numeric columns cannot be used for discovery: {non_numeric}"
            )

        missing_policy = str(opts.get("missing_values", "fail"))
        frame = _apply_missing_value_policy(raw, missing_policy)

        # Detect and warn about constant columns
        constant_cols = [c for c in frame.columns if frame[c].nunique() <= 1]
        if constant_cols:
            warnings.warn(
                f"Constant columns dropped from single-table discovery input: {constant_cols}",
                stacklevel=2,
            )
            frame = frame.drop(columns=constant_cols)

        raw_frame = frame.copy()

        collinearity_threshold: float | None = opts.get("collinearity_threshold")
        if collinearity_threshold is not None:
            frame = drop_collinear_columns(frame, threshold=float(collinearity_threshold))

        standardization = opts.get("standardization")
        if standardization == "zscore":
            analysis_frame = _standardize_zscore(frame)
        elif standardization is None:
            analysis_frame = frame
        else:
            raise ValueError(
                f"Unknown standardization: {standardization!r}. Use 'zscore' or None."
            )

        variable_metadata = _build_simple_variable_metadata(
            list(analysis_frame.columns)
        )

        return PreparedDiscoveryInput(
            analysis_frame=analysis_frame,
            raw_frame=raw_frame,
            transformed_frame=frame,
            variable_metadata=variable_metadata,
            background_knowledge=None,
            metadata={"table_path": str(table_path)},
        )


__all__ = ["SingleTableDiscoveryInputProvider"]
