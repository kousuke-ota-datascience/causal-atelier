"""TRAIN-only fitted preprocessing for predictive stages."""

from __future__ import annotations

from typing import Any

import pandas as pd

from ariadne.product.domain.errors import InvalidSchema, PredictiveValidationError
from ariadne.product.domain.schemas import canonical_hash, reject_unknown


def fit_preprocessor(
    train: pd.DataFrame,
    feature_columns: list[str],
    definition: dict[str, Any],
) -> dict[str, Any]:
    reject_unknown(
        definition,
        {"fit_partition", "numeric_imputation", "scale_numeric", "categorical_encoding"},
        name="preprocessing_spec",
    )
    if definition.get("fit_partition", "TRAIN") != "TRAIN":
        raise PredictiveValidationError(
            "PREPROCESSING_LEAKAGE_DETECTED",
            "Preprocessing may only be fitted on TRAIN",
            path="preprocessing_spec.fit_partition",
        )
    if definition.get("numeric_imputation", "MEAN") != "MEAN":
        raise InvalidSchema("Only deterministic MEAN numeric imputation is supported")
    if definition.get("categorical_encoding", "ONE_HOT") != "ONE_HOT":
        raise InvalidSchema("Only deterministic ONE_HOT categorical encoding is supported")
    scale = definition.get("scale_numeric", True)
    if not isinstance(scale, bool):
        raise InvalidSchema("preprocessing_spec.scale_numeric must be boolean")
    columns: list[dict[str, Any]] = []
    output_features: list[str] = []
    for name in feature_columns:
        series = train[name]
        if pd.api.types.is_numeric_dtype(series):
            numeric = pd.to_numeric(series, errors="coerce")
            mean = float(numeric.mean())
            if pd.isna(mean):
                raise PredictiveValidationError(
                    "UNUSABLE_TRAIN_FEATURE",
                    f"Numeric feature {name!r} has no TRAIN values",
                    path=f"feature_spec.feature_columns.{name}",
                )
            std = float(numeric.std(ddof=0)) if scale else 1.0
            if not std or pd.isna(std):
                std = 1.0
            columns.append({"name": name, "kind": "NUMERIC", "mean": mean, "scale": std})
            output_features.append(name)
        else:
            categories = sorted({
                "__MISSING__" if pd.isna(value) else str(value)
                for value in series.tolist()
            })
            columns.append({"name": name, "kind": "CATEGORICAL", "categories": categories})
            output_features.extend(f"{name}={category}" for category in categories)
    state = {
        "schema_version": "fitted-preprocessor/1",
        "fit_partition": "TRAIN",
        "columns": columns,
        "output_features": output_features,
    }
    state["canonical_hash"] = canonical_hash(state)
    return state


def transform_frame(frame: pd.DataFrame, state: dict[str, Any]) -> list[list[float]]:
    result: list[list[float]] = []
    for _, row in frame.iterrows():
        transformed: list[float] = []
        for column in state["columns"]:
            value = row[column["name"]]
            if column["kind"] == "NUMERIC":
                numeric = column["mean"] if pd.isna(value) else float(value)
                transformed.append((numeric - column["mean"]) / column["scale"])
            else:
                category = "__MISSING__" if pd.isna(value) else str(value)
                transformed.extend(
                    1.0 if category == expected else 0.0
                    for expected in column["categories"]
                )
        result.append(transformed)
    return result
