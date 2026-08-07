"""Exploratory Stage Runners; outputs are explicitly non-causal Results."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

import pandas as pd

from ariadne.product.domain.execution_plan import StageType
from ariadne.product.workflow.contracts import (
    ArtifactDraft,
    ResultDraft,
    StageContext,
    StageRunResult,
)
from ariadne.product.workflow.runner_registry import StageRunnerRegistry

_RESULT_TYPES = {
    "PROFILE": ("DATA_PROFILE_RESULT", "exploratory-data-profile-result/1"),
    "DISTRIBUTION": ("DISTRIBUTION_RESULT", "exploratory-distribution-result/1"),
    "ASSOCIATION": ("ASSOCIATION_RESULT", "exploratory-association-result/1"),
    "GROUP_SUMMARY": ("GROUP_SUMMARY_RESULT", "exploratory-group-summary-result/1"),
    "TIME_TREND": ("GROUP_SUMMARY_RESULT", "exploratory-time-trend-result/1"),
    "CHART": ("CHART_RESULT", "exploratory-chart-result/1"),
}
_STAGE_NAMES = {
    "PROFILE": "profile", "DISTRIBUTION": "distribution", "ASSOCIATION": "association",
    "GROUP_SUMMARY": "aggregate", "TIME_TREND": "time_trend", "CHART": "chart",
}


@dataclass
class ExploratoryStageRunner:
    operation: str

    @property
    def stage_type(self) -> StageType:
        return StageType("exploratory", _STAGE_NAMES[self.operation], "1")

    def validate(self, context: StageContext) -> None:
        if not isinstance(context.inputs.get("frame"), pd.DataFrame):
            raise ValueError("Exploratory Runner requires a pandas analysis frame")
        if context.inputs["frame"].empty:
            raise ValueError("Exploratory Runner cannot process an empty frame")

    def run(self, context: StageContext) -> StageRunResult:
        frame: pd.DataFrame = context.inputs["frame"]
        spec = context.stage.parameters
        payload, warnings = self._calculate(frame, spec)
        result_type, schema_version = _RESULT_TYPES[self.operation]
        status = "GENERATED_WITH_WARNINGS" if warnings else "GENERATED"
        result = ResultDraft(
            result_type=result_type,
            schema_version=schema_version,
            analytical_status=status,
            summary={
                "analysis_label": "EXPLORATORY",
                "row_count": len(frame),
                "columns": list(frame.columns),
            },
            payload=payload,
            warnings=tuple({"code": "EXPLORATORY_WARNING", "message": value} for value in warnings),
        )
        artifacts: tuple[ArtifactDraft, ...] = ()
        if self.operation == "CHART":
            content = json.dumps(payload["chart_spec"], sort_keys=True, separators=(",", ":")).encode()
            artifacts = (ArtifactDraft(
                artifact_type="CHART_SPECIFICATION",
                schema_version="exploratory-chart-artifact/1",
                media_type="application/vnd.vegalite.v5+json",
                content=content,
                metadata={"analysis_label": "EXPLORATORY"},
            ),)
        return StageRunResult(
            output_bindings={"exploration_result": payload}, results=(result,), artifacts=artifacts
        )

    def _calculate(self, frame: pd.DataFrame, spec: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
        columns = spec.get("columns") or list(frame.columns)
        unknown = sorted(set(columns) - set(frame.columns))
        if unknown:
            raise ValueError(f"Unknown exploratory columns: {unknown}")
        warnings: list[str] = []
        if self.operation == "PROFILE":
            values = []
            for column in columns:
                series = frame[column]
                item: dict[str, Any] = {
                    "column": column, "dtype": str(series.dtype),
                    "missing_count": int(series.isna().sum()),
                    "missing_rate": float(series.isna().mean()),
                    "cardinality": int(series.nunique(dropna=True)),
                }
                if pd.api.types.is_numeric_dtype(series):
                    described = series.describe()
                    item["numeric_summary"] = {
                        key: _json_number(described[key]) for key in ("mean", "std", "min", "25%", "50%", "75%", "max")
                        if key in described
                    }
                values.append(item)
            return {"profile": values}, warnings
        if self.operation == "DISTRIBUTION":
            if len(columns) != 1: raise ValueError("DISTRIBUTION requires exactly one column")
            series = frame[columns[0]].dropna()
            if pd.api.types.is_numeric_dtype(series):
                counts, boundaries = __import__("numpy").histogram(series.to_numpy(), bins=min(10, max(1, int(len(series) ** .5))))
                distribution = {"kind": "HISTOGRAM", "counts": counts.tolist(), "bin_edges": boundaries.tolist()}
            else:
                distribution = {"kind": "CATEGORY_COUNTS", "values": [
                    {"value": str(key), "count": int(count)}
                    for key, count in series.value_counts(dropna=False).head(50).items()
                ]}
            return {"column": columns[0], "distribution": distribution}, warnings
        if self.operation == "ASSOCIATION":
            if len(columns) != 2: raise ValueError("ASSOCIATION requires exactly two columns")
            left, right = frame[columns[0]], frame[columns[1]]
            if pd.api.types.is_numeric_dtype(left) and pd.api.types.is_numeric_dtype(right):
                joined = pd.concat([left, right], axis=1).dropna()
                value = float(joined.iloc[:, 0].corr(joined.iloc[:, 1]))
                return {"columns": columns, "method": "PEARSON", "value": _json_number(value), "sample_count": len(joined)}, warnings
            table = pd.crosstab(left, right)
            if table.empty: return {"columns": columns, "method": "CRAMERS_V", "value": None, "sample_count": 0}, ["Insufficient non-missing pairs"]
            import numpy as np
            observed = table.to_numpy(dtype=float); total = observed.sum()
            expected = observed.sum(1)[:, None] * observed.sum(0)[None, :] / total
            chi2 = float(np.divide((observed - expected) ** 2, expected, out=np.zeros_like(observed), where=expected != 0).sum())
            denominator = max(1, min(observed.shape) - 1)
            return {"columns": columns, "method": "CRAMERS_V", "value": float((chi2 / total / denominator) ** .5), "sample_count": int(total)}, warnings
        grouping = spec.get("grouping") or []
        aggregation = spec.get("aggregation") or {}
        if self.operation in {"GROUP_SUMMARY", "TIME_TREND"}:
            if isinstance(grouping, str): grouping = [grouping]
            if not grouping or set(grouping) - set(frame.columns): raise ValueError("Valid grouping columns are required")
            target = aggregation.get("column")
            method = aggregation.get("method", "COUNT")
            if method == "COUNT": grouped = frame.groupby(grouping, dropna=False).size().rename("value").reset_index()
            elif method in {"MEAN", "SUM", "MIN", "MAX", "MEDIAN"} and target in frame:
                grouped = getattr(frame.groupby(grouping, dropna=False)[target], method.lower())().rename("value").reset_index()
            else: raise ValueError("Aggregation is incompatible with the selected column")
            records = _records(grouped)
            return {"grouping": grouping, "aggregation": aggregation, "values": records}, warnings
        if self.operation == "CHART":
            encoding = spec.get("chart_encoding") or {}
            if not isinstance(encoding, dict) or not encoding.get("x"):
                raise ValueError("CHART requires x encoding")
            fields = [value for key, value in encoding.items() if key in {"x", "y", "color", "facet"} and value]
            if set(fields) - set(frame.columns): raise ValueError("Chart encoding references an unknown column")
            max_rows = min(len(frame), int((spec.get("sampling") or {}).get("size", 1000)))
            chart_data = _records(frame[fields].head(max_rows))
            mark = encoding.get("mark", "point")
            chart_spec = {
                "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
                "description": "EXPLORATORY visualization; not a causal conclusion",
                "mark": mark,
                "encoding": {key: {"field": value} for key, value in encoding.items() if key in {"x", "y", "color", "facet"} and value},
                "data": {"values": chart_data},
            }
            return {"chart_spec": chart_spec, "sampling": {"displayed_rows": max_rows, "source_rows": len(frame)}}, warnings
        raise AssertionError(self.operation)


def register_exploratory_runners(registry: StageRunnerRegistry) -> None:
    for operation in _RESULT_TYPES:
        registry.register(ExploratoryStageRunner(operation))


def _json_number(value: Any) -> float | int | None:
    import math
    if pd.isna(value) or not math.isfinite(float(value)): return None
    result = float(value)
    return int(result) if result.is_integer() else result


def _records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    value = frame.astype(object).where(frame.notna(), None)
    return [{key: _json_value(item) for key, item in row.items()} for row in value.to_dict(orient="records")]


def _json_value(value: Any) -> Any:
    if isinstance(value, (int, float)): return _json_number(value)
    if isinstance(value, (pd.Timestamp, datetime, date)):
        return value.isoformat()
    return value
