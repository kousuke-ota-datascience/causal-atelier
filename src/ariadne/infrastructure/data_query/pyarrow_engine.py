"""Bounded CSV/Parquet preview, profiling, and aggregation using PyArrow."""

from __future__ import annotations

import math
import random
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.dataset as ds


ENGINE_VERSION = f"pyarrow-{pa.__version__}"
PROFILE_VALUE_LIMIT = 250_000


@dataclass(frozen=True)
class QueryResult:
    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int
    scanned_bytes: int
    duration_ms: int
    sampled: bool = False
    sample_size: int | None = None
    sampling_method: str | None = None
    random_seed: int | None = None
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "columns": self.columns,
            "rows": self.rows,
            "row_count": self.row_count,
            "scanned_bytes": self.scanned_bytes,
            "duration_ms": self.duration_ms,
            "sampled": self.sampled,
            "sample_size": self.sample_size,
            "sampling_method": self.sampling_method,
            "random_seed": self.random_seed,
            "metadata": self.metadata or {},
        }


class PyArrowQueryEngine:
    version = ENGINE_VERSION

    def __init__(
        self, *, max_result_rows: int = 10_000, max_sample_rows: int = 50_000
    ) -> None:
        self.max_result_rows = max_result_rows
        self.max_sample_rows = max_sample_rows

    def schema(self, path: Path, file_format: str) -> list[dict[str, Any]]:
        schema = self._dataset(path, file_format).schema
        return [
            {
                "name": field.name,
                "physical_type": str(field.type),
                "logical_type": _logical_type(field.type),
                "nullable": field.nullable,
            }
            for field in schema
        ]

    def preview(
        self,
        path: Path,
        file_format: str,
        *,
        page: int,
        limit: int,
        columns: list[str] | None = None,
    ) -> QueryResult:
        started = time.perf_counter()
        dataset = self._dataset(path, file_format)
        selected = columns or dataset.schema.names
        _require_columns(dataset.schema.names, selected)
        offset = (page - 1) * limit
        table = dataset.head(offset + limit, columns=selected).slice(offset, limit)
        rows = [_json_row(row) for row in table.to_pylist()]
        return QueryResult(
            columns=selected,
            rows=rows,
            row_count=len(rows),
            scanned_bytes=path.stat().st_size,
            duration_ms=int((time.perf_counter() - started) * 1000),
            metadata={"page": page, "limit": limit, "exact": True},
        )

    def profile(
        self, path: Path, file_format: str, *, top_n: int = 20
    ) -> dict[str, Any]:
        started = time.perf_counter()
        dataset = self._dataset(path, file_format)
        names = dataset.schema.names
        nulls = Counter({name: 0 for name in names})
        distinct: dict[str, set[Any]] = {name: set() for name in names}
        numeric: dict[str, list[float]] = defaultdict(list)
        categories: dict[str, Counter[str]] = defaultdict(Counter)
        minima: dict[str, Any] = {}
        maxima: dict[str, Any] = {}
        approximate_columns: set[str] = set()
        row_count = 0
        for batch in dataset.scanner(batch_size=65_536).to_batches():
            row_count += batch.num_rows
            for index, field in enumerate(batch.schema):
                values = batch.column(index).to_pylist()
                non_null = [value for value in values if value is not None]
                nulls[field.name] += len(values) - len(non_null)
                remaining = PROFILE_VALUE_LIMIT - len(distinct[field.name])
                if remaining > 0:
                    distinct[field.name].update(
                        _hashable(value) for value in non_null[:remaining]
                    )
                if len(non_null) > remaining:
                    approximate_columns.add(field.name)
                if non_null:
                    batch_min = min(non_null)
                    batch_max = max(non_null)
                    minima[field.name] = min(
                        minima.get(field.name, batch_min), batch_min
                    )
                    maxima[field.name] = max(
                        maxima.get(field.name, batch_max), batch_max
                    )
                if (
                    pa.types.is_integer(field.type)
                    or pa.types.is_floating(field.type)
                    or pa.types.is_decimal(field.type)
                ):
                    numeric_remaining = PROFILE_VALUE_LIMIT - len(numeric[field.name])
                    if numeric_remaining > 0:
                        numeric[field.name].extend(
                            float(value)
                            for value in non_null[:numeric_remaining]
                            if _finite(value)
                        )
                    if len(non_null) > numeric_remaining:
                        approximate_columns.add(field.name)
                elif pa.types.is_string(field.type) or pa.types.is_boolean(field.type):
                    category_remaining = PROFILE_VALUE_LIMIT - sum(
                        categories[field.name].values()
                    )
                    if category_remaining > 0:
                        categories[field.name].update(
                            str(value) for value in non_null[:category_remaining]
                        )
                    if len(non_null) > category_remaining:
                        approximate_columns.add(field.name)
        column_profiles: list[dict[str, Any]] = []
        for field in dataset.schema:
            name = field.name
            stats: dict[str, Any] = {}
            if values := numeric.get(name):
                ordered = sorted(values)
                stats = {
                    "mean": sum(values) / len(values),
                    "quantiles": {
                        "0.25": _quantile(ordered, 0.25),
                        "0.5": _quantile(ordered, 0.5),
                        "0.75": _quantile(ordered, 0.75),
                    },
                }
            if name in categories:
                stats["top_values"] = [
                    {"value": value, "count": count}
                    for value, count in categories[name].most_common(top_n)
                ]
            column_profiles.append(
                {
                    "name": name,
                    "physical_type": str(field.type),
                    "logical_type": _logical_type(field.type),
                    "null_count": nulls[name],
                    "null_ratio": nulls[name] / row_count if row_count else 0.0,
                    "distinct_count": len(distinct[name]),
                    "distinct_count_is_approximate": name in approximate_columns,
                    "min": _json_value(minima.get(name)),
                    "max": _json_value(maxima.get(name)),
                    "statistics": stats,
                }
            )
        return {
            "row_count": row_count,
            "column_count": len(names),
            "columns": column_profiles,
            "sampled": bool(approximate_columns),
            "sample_size": PROFILE_VALUE_LIMIT if approximate_columns else row_count,
            "sampling_method": "bounded_head" if approximate_columns else None,
            "exact": not approximate_columns,
            "scanned_bytes": path.stat().st_size,
            "duration_ms": int((time.perf_counter() - started) * 1000),
            "query_engine_version": self.version,
        }

    def execute(
        self, path: Path, file_format: str, specification: dict[str, Any]
    ) -> QueryResult:
        started = time.perf_counter()
        dataset = self._dataset(path, file_format)
        available = dataset.schema.names
        selected = list(specification.get("selected_columns") or [])
        groups = list(specification.get("group_by") or [])
        target = specification.get("aggregation_target")
        filters = list(specification.get("filters") or [])
        required = set(selected + groups + ([target] if target else []))
        required.update(item["column"] for item in filters)
        _require_columns(available, list(required))
        expression = _filter_expression(filters)
        scanner = dataset.scanner(
            columns=list(required) or available,
            filter=expression,
            batch_size=65_536,
        )
        if groups or specification.get("chart_type") in {"histogram", "box"}:
            rows, metadata = self._aggregate(scanner, specification)
            rows = self._sort_limit(rows, specification)
            sampled = False
            sample_size = None
            sampling_method = None
            seed = None
        else:
            sampling = specification.get("sampling")
            size = min(
                int((sampling or {}).get("size", specification.get("limit", 1000))),
                self.max_sample_rows,
            )
            sampling_method = (sampling or {}).get("method", "head")
            seed = int((sampling or {}).get("seed", 42))
            rows = self._sample(scanner, size=size, method=sampling_method, seed=seed)
            metadata = {
                "exact": sampling is None,
                "chart_type": specification.get("chart_type", "table"),
            }
            if specification.get("chart_type") == "scatter" and len(selected) >= 2:
                metadata["correlation"] = _correlation(rows, selected[0], selected[1])
            sampled = sampling is not None
            sample_size = len(rows) if sampled else None
        columns = list(rows[0]) if rows else (groups or selected)
        return QueryResult(
            columns=columns,
            rows=rows,
            row_count=len(rows),
            scanned_bytes=path.stat().st_size,
            duration_ms=int((time.perf_counter() - started) * 1000),
            sampled=sampled,
            sample_size=sample_size,
            sampling_method=sampling_method,
            random_seed=seed,
            metadata={**metadata, "query_engine_version": self.version},
        )

    def _aggregate(
        self, scanner: ds.Scanner, specification: dict[str, Any]
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        chart = specification.get("chart_type", "table")
        if chart in {"histogram", "box"}:
            column = (
                specification.get("selected_columns")
                or [specification.get("aggregation_target")]
            )[0]
            values: list[float] = []
            for batch in scanner.to_batches():
                values.extend(
                    float(value)
                    for value in batch.column(
                        batch.schema.get_field_index(column)
                    ).to_pylist()
                    if value is not None and _finite(value)
                )
            ordered = sorted(values)
            if chart == "box":
                rows = [
                    {
                        "column": column,
                        "min": min(values) if values else None,
                        "q1": _quantile(ordered, 0.25),
                        "median": _quantile(ordered, 0.5),
                        "q3": _quantile(ordered, 0.75),
                        "max": max(values) if values else None,
                    }
                ]
            else:
                rows = _histogram(values, int(specification.get("bins", 20)))
            return rows, {"exact": True, "chart_type": chart, "excluded_nulls": True}

        groups = list(specification.get("group_by") or [])
        target = specification.get("aggregation_target")
        operation = specification.get("aggregation", "count")
        include_nulls = bool(specification.get("include_nulls", False))
        time_grain = specification.get("time_grain")
        accumulators: dict[tuple[Any, ...], dict[str, Any]] = {}
        for batch in scanner.to_batches():
            for raw in batch.to_pylist():
                key = tuple(_time_bucket(raw.get(name), time_grain) for name in groups)
                if not include_nulls and any(value is None for value in key):
                    continue
                if (
                    len(accumulators) >= self.max_result_rows
                    and key not in accumulators
                ):
                    raise ValueError("aggregation exceeded maximum group count")
                state = accumulators.setdefault(
                    key,
                    {
                        "count": 0,
                        "value_count": 0,
                        "sum": 0.0,
                        "values": set(),
                        "min": None,
                        "max": None,
                    },
                )
                value = raw.get(target) if target else None
                state["count"] += 1
                if value is not None:
                    state["value_count"] += 1
                    if (
                        operation == "distinct_count"
                        and len(state["values"]) >= 1_000_000
                    ):
                        raise ValueError(
                            "distinct aggregation exceeded the configured memory bound"
                        )
                    state["values"].add(_hashable(value))
                    if isinstance(value, (int, float, Decimal)):
                        state["sum"] += float(value)
                    state["min"] = (
                        value if state["min"] is None else min(state["min"], value)
                    )
                    state["max"] = (
                        value if state["max"] is None else max(state["max"], value)
                    )
        rows: list[dict[str, Any]] = []
        value_name = operation if not target else f"{operation}_{target}"
        for key, state in accumulators.items():
            row = {
                name: _json_value(value)
                for name, value in zip(groups, key, strict=True)
            }
            if operation == "count":
                result = state["count"]
            elif operation == "distinct_count":
                result = len(state["values"])
            elif operation == "sum":
                result = state["sum"]
            elif operation == "mean":
                result = (
                    state["sum"] / state["value_count"]
                    if state["value_count"]
                    else None
                )
            else:
                result = state[operation]
            row[value_name] = _json_value(result)
            row["__group_count"] = state["count"]
            rows.append(row)
        return rows, {
            "exact": True,
            "aggregation": operation,
            "aggregation_target": target,
            "group_by": groups,
            "excluded_nulls": not include_nulls,
        }

    def _sample(
        self, scanner: ds.Scanner, *, size: int, method: str, seed: int
    ) -> list[dict[str, Any]]:
        if method == "head":
            rows: list[dict[str, Any]] = []
            for batch in scanner.to_batches():
                rows.extend(
                    _json_row(row) for row in batch.to_pylist()[: size - len(rows)]
                )
                if len(rows) >= size:
                    break
            return rows
        rng = random.Random(seed)
        reservoir: list[dict[str, Any]] = []
        seen = 0
        for batch in scanner.to_batches():
            for row in batch.to_pylist():
                seen += 1
                converted = _json_row(row)
                if len(reservoir) < size:
                    reservoir.append(converted)
                else:
                    replacement = rng.randrange(seen)
                    if replacement < size:
                        reservoir[replacement] = converted
        return reservoir

    def _sort_limit(
        self, rows: list[dict[str, Any]], specification: dict[str, Any]
    ) -> list[dict[str, Any]]:
        sort_by = specification.get("sort_by")
        if sort_by and rows and sort_by in rows[0]:
            rows.sort(
                key=lambda row: (row.get(sort_by) is None, row.get(sort_by)),
                reverse=specification.get("sort_direction") == "desc",
            )
        limit = min(int(specification.get("limit", 1000)), self.max_result_rows)
        return rows[:limit]

    @staticmethod
    def _dataset(path: Path, file_format: str) -> ds.Dataset:
        normalized = file_format.lower()
        if normalized not in {"csv", "parquet"}:
            raise ValueError(f"unsupported dataset format: {file_format}")
        return ds.dataset(path, format=normalized)


def _filter_expression(filters: list[dict[str, Any]]) -> ds.Expression | None:
    expression: ds.Expression | None = None
    for clause in filters:
        field = ds.field(clause["column"])
        operator = clause["operator"]
        value = clause.get("value")
        current = {
            "eq": lambda: field == value,
            "ne": lambda: field != value,
            "lt": lambda: field < value,
            "lte": lambda: field <= value,
            "gt": lambda: field > value,
            "gte": lambda: field >= value,
            "in": lambda: field.isin(value),
            "is_null": field.is_null,
            "not_null": field.is_valid,
        }[operator]()
        expression = current if expression is None else expression & current
    return expression


def _require_columns(available: list[str], requested: list[str]) -> None:
    missing = sorted(set(requested) - set(available))
    if missing:
        raise ValueError(f"unknown columns: {', '.join(missing)}")


def _logical_type(data_type: pa.DataType) -> str:
    if (
        pa.types.is_integer(data_type)
        or pa.types.is_floating(data_type)
        or pa.types.is_decimal(data_type)
    ):
        return "numeric"
    if pa.types.is_boolean(data_type):
        return "boolean"
    if pa.types.is_date(data_type) or pa.types.is_timestamp(data_type):
        return "datetime"
    if pa.types.is_string(data_type) or pa.types.is_large_string(data_type):
        return "text"
    return "other"


def _hashable(value: Any) -> Any:
    if isinstance(value, (list, dict)):
        return repr(value)
    return value


def _finite(value: Any) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def _quantile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    position = (len(values) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return values[lower]
    return values[lower] * (upper - position) + values[upper] * (position - lower)


def _histogram(values: list[float], bins: int) -> list[dict[str, Any]]:
    if not values:
        return []
    minimum, maximum = min(values), max(values)
    width = (maximum - minimum) / bins if maximum != minimum else 1.0
    counts = [0] * bins
    for value in values:
        index = min(int((value - minimum) / width), bins - 1)
        counts[index] += 1
    return [
        {
            "bin_start": minimum + index * width,
            "bin_end": minimum + (index + 1) * width,
            "count": count,
        }
        for index, count in enumerate(counts)
    ]


def _json_value(value: Any) -> Any:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, bytes):
        return value.hex()
    return value


def _json_row(row: dict[str, Any]) -> dict[str, Any]:
    return {name: _json_value(value) for name, value in row.items()}


def _time_bucket(value: Any, grain: str | None) -> Any:
    if not grain or not isinstance(value, (datetime, date)):
        return value
    if isinstance(value, date) and not isinstance(value, datetime):
        value = datetime(value.year, value.month, value.day)
    if grain == "hour":
        return value.replace(minute=0, second=0, microsecond=0)
    if grain == "day":
        return value.replace(hour=0, minute=0, second=0, microsecond=0)
    if grain == "week":
        start = value.replace(hour=0, minute=0, second=0, microsecond=0)
        return start - timedelta(days=start.weekday())
    if grain == "month":
        return value.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if grain == "quarter":
        month = ((value.month - 1) // 3) * 3 + 1
        return value.replace(
            month=month, day=1, hour=0, minute=0, second=0, microsecond=0
        )
    if grain == "year":
        return value.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    return value


def _correlation(rows: list[dict[str, Any]], left: str, right: str) -> dict[str, Any]:
    pairs = [
        (float(row[left]), float(row[right]))
        for row in rows
        if isinstance(row.get(left), (int, float))
        and isinstance(row.get(right), (int, float))
        and _finite(row[left])
        and _finite(row[right])
    ]
    if len(pairs) < 2:
        return {"pearson": None, "sample_count": len(pairs)}
    left_mean = sum(item[0] for item in pairs) / len(pairs)
    right_mean = sum(item[1] for item in pairs) / len(pairs)
    covariance = sum((x - left_mean) * (y - right_mean) for x, y in pairs)
    left_scale = math.sqrt(sum((x - left_mean) ** 2 for x, _ in pairs))
    right_scale = math.sqrt(sum((y - right_mean) ** 2 for _, y in pairs))
    value = (
        covariance / (left_scale * right_scale) if left_scale and right_scale else None
    )
    return {"pearson": value, "sample_count": len(pairs)}


__all__ = ["ENGINE_VERSION", "PyArrowQueryEngine", "QueryResult"]
