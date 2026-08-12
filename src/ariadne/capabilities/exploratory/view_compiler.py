"""Deterministic Analysis View compiler for tabular Dataset Versions."""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import pandas as pd

from ariadne.product.domain.analysis_view import validate_analysis_view_payload
from ariadne.product.domain.errors import FilterTypeMismatch, InvalidSchema
from ariadne.product.domain.schemas import canonical_hash

_FILTER_OPERATORS = {"EQ", "NE", "LT", "LTE", "GT", "GTE", "IN", "NOT_IN", "IS_NULL", "NOT_NULL"}
_OPERATORS_BY_LOGICAL_TYPE = {
    "BOOLEAN": {"EQ", "NE", "IN", "NOT_IN", "IS_NULL", "NOT_NULL"},
    "INTEGER": _FILTER_OPERATORS,
    "REAL": _FILTER_OPERATORS,
    "DATETIME": _FILTER_OPERATORS,
    "TEXT": {"EQ", "NE", "IN", "NOT_IN", "IS_NULL", "NOT_NULL"},
    "OTHER": {"IS_NULL", "NOT_NULL"},
}
_EXPRESSION_OPERATORS = {"ADD", "SUBTRACT", "MULTIPLY", "DIVIDE"}
_FUNCTIONS = {"ABS", "LOWER", "UPPER", "LOG", "YEAR", "MONTH", "DAY"}


@dataclass(frozen=True)
class CompiledAnalysisView:
    frame: pd.DataFrame
    manifest: dict[str, Any]
    materialized_hash: str


class AnalysisViewCompiler:
    compiler_version = "analysis-view-compiler/1"

    def validate(self, dataset_schema: dict[str, str], view_spec: dict[str, Any]) -> None:
        validate_analysis_view_payload(view_spec)
        source_columns = set(dataset_schema)
        derived_names: set[str] = set()
        for item in view_spec["derived_columns"]:
            if set(item) != {"name", "expression"} or not isinstance(item["name"], str):
                raise InvalidSchema("Each derived column requires name and expression")
            if item["name"] in source_columns or item["name"] in derived_names:
                raise InvalidSchema(f"Derived column name is duplicated: {item['name']}")
            self._validate_expression(item["expression"], source_columns | derived_names)
            derived_names.add(item["name"])
        available = source_columns | derived_names
        selected = view_spec["selected_columns"]
        if selected and (missing := sorted(set(selected) - available)):
            raise InvalidSchema(f"Analysis View references unknown selected columns: {missing}")
        for index, condition in enumerate(view_spec["row_filter"]):
            self._validate_filter(condition, available, dataset_schema, f"row_filter[{index}]")
        cutoff = view_spec["time_cutoff"]
        if cutoff is not None:
            self._validate_filter(cutoff, available, dataset_schema, "time_cutoff")
            if dataset_schema.get(cutoff["column"]) != "DATETIME" or cutoff["operator"] not in {"LT", "LTE"}:
                raise FilterTypeMismatch("FILTER_TYPE_MISMATCH: time_cutoff requires a DATETIME column and LT or LTE")
        policy = view_spec["missing_value_policy"]
        if set(policy) - {"default", "columns"}:
            raise InvalidSchema("Unknown missing_value_policy fields")
        if policy.get("default", "KEEP") not in {"KEEP", "DROP_ROW"}:
            raise InvalidSchema("missing_value_policy.default must be KEEP or DROP_ROW")
        columns = policy.get("columns", {})
        if not isinstance(columns, dict) or set(columns) - available:
            raise InvalidSchema("missing_value_policy references an unknown column")
        for column, rule in columns.items():
            if not isinstance(rule, dict) or rule.get("strategy") not in {
                "KEEP", "DROP_ROW", "FILL_VALUE", "FILL_MEAN", "FILL_MEDIAN", "FILL_MODE",
            }:
                raise InvalidSchema(f"Invalid missing-value rule for {column}")
            if rule["strategy"] == "FILL_VALUE" and "value" not in rule:
                raise InvalidSchema("FILL_VALUE requires value")
        sampling = view_spec["sampling"]
        if sampling is not None:
            if not isinstance(sampling, dict) or set(sampling) - {"method", "size", "seed"}:
                raise InvalidSchema("Invalid sampling specification")
            if sampling.get("method") not in {"HEAD", "RANDOM"}:
                raise InvalidSchema("sampling.method must be HEAD or RANDOM")
            if not isinstance(sampling.get("size"), int) or sampling["size"] < 1:
                raise InvalidSchema("sampling.size must be positive")
            if sampling["method"] == "RANDOM" and not isinstance(sampling.get("seed"), int):
                raise InvalidSchema("RANDOM sampling requires an integer seed")

    def compile(
        self,
        frame: pd.DataFrame,
        dataset_schema: dict[str, str],
        view_spec: dict[str, Any],
        *,
        source_dataset_content_hash: str,
    ) -> CompiledAnalysisView:
        self.validate(dataset_schema, view_spec)
        value = frame.copy(deep=True)
        source_rows = len(value)
        for item in view_spec["derived_columns"]:
            value[item["name"]] = self._evaluate_expression(item["expression"], value)
        for condition in view_spec["row_filter"]:
            value = value.loc[self._filter_mask(value, condition)]
        if view_spec["time_cutoff"] is not None:
            value = value.loc[self._filter_mask(value, view_spec["time_cutoff"])]
        value = self._apply_missing_policy(value, view_spec["missing_value_policy"])
        selected = view_spec["selected_columns"]
        if selected:
            value = value[[*selected]]
        sampling = view_spec["sampling"]
        if sampling is not None and len(value) > sampling["size"]:
            value = (
                value.head(sampling["size"])
                if sampling["method"] == "HEAD"
                else value.sample(n=sampling["size"], random_state=sampling["seed"])
            )
        value = value.reset_index(drop=True)
        if value.empty:
            raise InvalidSchema("ANALYSIS_VIEW_EMPTY: Analysis View produced no rows")
        materialized = value.to_json(
            orient="table", date_format="iso", date_unit="us", index=False, force_ascii=False
        ).encode("utf-8")
        materialized_hash = hashlib.sha256(materialized).hexdigest()
        manifest = {
            "schema_version": "analysis-view-manifest/1",
            "compiler_version": self.compiler_version,
            "source_dataset_content_hash": source_dataset_content_hash,
            "view_spec_hash": canonical_hash(view_spec),
            "materialized_hash": materialized_hash,
            "source_row_count": source_rows,
            "output_row_count": len(value),
            "output_columns": list(value.columns),
            "view_spec": view_spec,
        }
        return CompiledAnalysisView(value, manifest, materialized_hash)

    def _validate_filter(
        self, value: Any, available: set[str], dataset_schema: dict[str, str], path: str,
    ) -> None:
        if not isinstance(value, dict) or set(value) - {"column", "operator", "value"}:
            raise InvalidSchema(f"Invalid filter at {path}")
        if value.get("column") not in available:
            raise InvalidSchema(f"Unknown filter column at {path}")
        if value.get("operator") not in _FILTER_OPERATORS:
            raise InvalidSchema(f"Unknown filter operator at {path}")
        operator = value["operator"]
        expected_keys = {"column", "operator"} if operator in {"IS_NULL", "NOT_NULL"} else {"column", "operator", "value"}
        if set(value) != expected_keys:
            raise FilterTypeMismatch(f"FILTER_TYPE_MISMATCH: invalid value shape at {path}")
        logical_type = dataset_schema.get(value["column"])
        if logical_type not in _OPERATORS_BY_LOGICAL_TYPE or operator not in _OPERATORS_BY_LOGICAL_TYPE[logical_type]:
            raise FilterTypeMismatch(f"FILTER_TYPE_MISMATCH: {operator} is not allowed for {value['column']} at {path}")
        if operator in {"IS_NULL", "NOT_NULL"}:
            return
        raw_value = value["value"]
        if operator in {"IN", "NOT_IN"}:
            if not isinstance(raw_value, list) or not raw_value:
                raise FilterTypeMismatch(f"FILTER_TYPE_MISMATCH: {operator} requires a non-empty list at {path}")
            values = raw_value
        else:
            if isinstance(raw_value, list):
                raise FilterTypeMismatch(f"FILTER_TYPE_MISMATCH: scalar value required at {path}")
            values = [raw_value]
        if not all(self._value_matches_logical_type(item, logical_type) for item in values):
            raise FilterTypeMismatch(f"FILTER_TYPE_MISMATCH: invalid {logical_type} value at {path}")

    @staticmethod
    def _value_matches_logical_type(value: Any, logical_type: str) -> bool:
        if logical_type == "BOOLEAN":
            return isinstance(value, bool)
        if logical_type == "INTEGER":
            return type(value) is int
        if logical_type == "REAL":
            return type(value) in {int, float} and math.isfinite(value)
        if logical_type == "TEXT":
            return isinstance(value, str)
        if logical_type == "DATETIME" and isinstance(value, str):
            try:
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                return False
            return True
        return False

    def _validate_expression(self, value: Any, available: set[str]) -> None:
        if not isinstance(value, dict):
            raise InvalidSchema("Derived expression must be an object")
        if set(value) == {"column"}:
            if value["column"] not in available:
                raise InvalidSchema(f"Unknown expression column: {value['column']}")
            return
        if set(value) == {"literal"}:
            return
        if set(value) == {"operator", "left", "right"} and value["operator"] in _EXPRESSION_OPERATORS:
            self._validate_expression(value["left"], available)
            self._validate_expression(value["right"], available)
            return
        if set(value) == {"function", "args"} and value["function"] in _FUNCTIONS:
            if not isinstance(value["args"], list) or len(value["args"]) != 1:
                raise InvalidSchema("Allow-listed derived functions take one argument")
            self._validate_expression(value["args"][0], available)
            return
        raise InvalidSchema("Derived expression uses a non-deterministic or unsupported operation")

    def _evaluate_expression(self, expression: dict[str, Any], frame: pd.DataFrame) -> Any:
        if "column" in expression:
            return frame[expression["column"]]
        if "literal" in expression:
            return expression["literal"]
        if "operator" in expression:
            left = self._evaluate_expression(expression["left"], frame)
            right = self._evaluate_expression(expression["right"], frame)
            return {
                "ADD": lambda: left + right,
                "SUBTRACT": lambda: left - right,
                "MULTIPLY": lambda: left * right,
                "DIVIDE": lambda: left / right,
            }[expression["operator"]]()
        argument = self._evaluate_expression(expression["args"][0], frame)
        function = expression["function"]
        if function == "ABS":
            return argument.abs() if hasattr(argument, "abs") else abs(argument)
        if function in {"LOWER", "UPPER"}:
            values = argument.astype("string")
            return values.str.lower() if function == "LOWER" else values.str.upper()
        if function == "LOG":
            import numpy as np
            return np.log(argument)
        values = pd.to_datetime(argument, errors="raise")
        return {"YEAR": values.dt.year, "MONTH": values.dt.month, "DAY": values.dt.day}[function]

    @staticmethod
    def _filter_mask(frame: pd.DataFrame, condition: dict[str, Any]) -> pd.Series:
        series = frame[condition["column"]]
        operator = condition["operator"]
        if operator == "IS_NULL": return series.isna()
        if operator == "NOT_NULL": return series.notna()
        target = condition["value"]
        return {
            "EQ": lambda: series == target, "NE": lambda: series != target,
            "LT": lambda: series < target, "LTE": lambda: series <= target,
            "GT": lambda: series > target, "GTE": lambda: series >= target,
            "IN": lambda: series.isin(target), "NOT_IN": lambda: ~series.isin(target),
        }[operator]().fillna(False)

    @staticmethod
    def _apply_missing_policy(frame: pd.DataFrame, policy: dict[str, Any]) -> pd.DataFrame:
        value = frame.copy()
        if policy.get("default", "KEEP") == "DROP_ROW":
            value = value.dropna()
        for column, rule in policy.get("columns", {}).items():
            strategy = rule["strategy"]
            if strategy == "DROP_ROW": value = value.loc[value[column].notna()]
            elif strategy == "FILL_VALUE": value[column] = value[column].fillna(rule["value"])
            elif strategy == "FILL_MEAN": value[column] = value[column].fillna(value[column].mean())
            elif strategy == "FILL_MEDIAN": value[column] = value[column].fillna(value[column].median())
            elif strategy == "FILL_MODE":
                mode = value[column].mode(dropna=True)
                if mode.empty: raise InvalidSchema(f"Cannot calculate mode for {column}")
                value[column] = value[column].fillna(mode.iloc[0])
        return value
