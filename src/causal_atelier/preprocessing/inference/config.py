"""特徴量設定の dataclass と validation。"""

from __future__ import annotations

from dataclasses import dataclass
from os import PathLike, fsdecode
from pathlib import Path
from typing import Any, Mapping

from causal_atelier.infrastructure.config import (
    ensure_mapping as _mapping,
    ensure_tuple as _tuple,
    load_yaml_mapping,
)


@dataclass(frozen=True)
class DatasetSpec:
    """dataset level の特徴量設定。

    Attributes:
        name: Dataset name.
        analysis_unit: Unit of analysis.
        unit_key: Column identifying the analysis unit.
        time_key: Column identifying transaction time periods.
    """

    name: str
    analysis_unit: str
    unit_key: str
    time_key: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "DatasetSpec":
        """Build dataset specification from YAML.

        Args:
            value: Mapping under the ``dataset`` key.

        Returns:
            Parsed dataset specification.
        """
        data = _mapping(value, "dataset")
        return cls(
            name=str(data["name"]),
            analysis_unit=str(data["analysis_unit"]),
            unit_key=str(data["unit_key"]),
            time_key=str(data["time_key"]),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the dataset specification.

        Returns:
            YAML-compatible dictionary.
        """
        return {
            "name": self.name,
            "analysis_unit": self.analysis_unit,
            "unit_key": self.unit_key,
            "time_key": self.time_key,
        }


@dataclass(frozen=True)
class TableSpec:
    """logical source table の仕様。

    Attributes:
        name: Dataset registry entry name.
        required_columns: Columns required after loading the table.
        household_key: Household key column.
        campaign_id: Campaign identifier column.
        start_day: Campaign start-day column.
        end_day: Campaign end-day column.
        week: Transaction week column.
        transaction_timestamp: Transaction timestamp column.
    """

    name: str
    required_columns: tuple[str, ...]
    household_key: str | None = None
    campaign_id: str | None = None
    start_day: str | None = None
    end_day: str | None = None
    week: str | None = None
    transaction_timestamp: str | None = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TableSpec":
        """Build a table specification from YAML.

        Args:
            value: Table mapping.

        Returns:
            Parsed table specification.
        """
        data = _mapping(value, "tables.*")
        return cls(
            name=str(data["name"]),
            required_columns=tuple(str(item) for item in _tuple(data.get("required_columns"), "required_columns")),
            household_key=None if data.get("household_key") is None else str(data["household_key"]),
            campaign_id=None if data.get("campaign_id") is None else str(data["campaign_id"]),
            start_day=None if data.get("start_day") is None else str(data["start_day"]),
            end_day=None if data.get("end_day") is None else str(data["end_day"]),
            week=None if data.get("week") is None else str(data["week"]),
            transaction_timestamp=None
            if data.get("transaction_timestamp") is None
            else str(data["transaction_timestamp"]),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the table specification.

        Returns:
            YAML-compatible dictionary.
        """
        return {
            "name": self.name,
            "required_columns": list(self.required_columns),
            "household_key": self.household_key,
            "campaign_id": self.campaign_id,
            "start_day": self.start_day,
            "end_day": self.end_day,
            "week": self.week,
            "transaction_timestamp": self.transaction_timestamp,
        }


@dataclass(frozen=True)
class MetricSpec:
    """集約 metric の仕様。

    Attributes:
        column: Source column. ``None`` is allowed for row-count metrics.
        agg: Aggregation method.
    """

    column: str | None
    agg: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "MetricSpec":
        """Build an aggregation metric from YAML.

        Args:
            value: Metric mapping.

        Returns:
            Parsed metric specification.
        """
        data = _mapping(value, "metrics.*")
        return cls(
            column=None if data.get("column") is None else str(data["column"]),
            agg=str(data["agg"]),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the metric specification.

        Returns:
            YAML-compatible dictionary.
        """
        return {"column": self.column, "agg": self.agg}


@dataclass(frozen=True)
class AggregationBlockSpec:
    """設定済みの分析単位 aggregation block。

    Attributes:
        source_table: Logical source table name.
        prefix: Prefix added to output feature names.
        group_by: Columns used as aggregation keys.
        window: Named time window used for filtering.
        metrics: Metrics keyed by output metric name.
    """

    source_table: str
    prefix: str
    group_by: tuple[str, ...]
    window: str
    metrics: dict[str, MetricSpec]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "AggregationBlockSpec":
        """Build an aggregation block from YAML.

        Args:
            value: Aggregation block mapping.

        Returns:
            Parsed aggregation block.
        """
        data = _mapping(value, "aggregations.*")
        metrics_data = _mapping(data.get("metrics", {}), "aggregations.*.metrics")
        return cls(
            source_table=str(data["source_table"]),
            prefix=str(data["prefix"]),
            group_by=tuple(str(item) for item in _tuple(data.get("group_by"), "group_by")),
            window=str(_mapping(data.get("filters", {}), "filters").get("window", data.get("window"))),
            metrics={
                str(name): MetricSpec.from_mapping(metric)
                for name, metric in metrics_data.items()
            },
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the aggregation block.

        Returns:
            YAML-compatible dictionary.
        """
        return {
            "source_table": self.source_table,
            "prefix": self.prefix,
            "group_by": list(self.group_by),
            "filters": {"window": self.window},
            "metrics": {
                name: metric.to_dict()
                for name, metric in self.metrics.items()
            },
        }


@dataclass(frozen=True)
class EncodingSpec:
    """列 encoding の仕様。

    Attributes:
        input_column: Source categorical or numeric column.
        type: Encoding method.
        output: Primary output column for one-column encodings.
        map: Category-to-number mapping for ordinal encodings.
        unknown_value: Value used when an ordinal or numeric encoding is
            unknown.
        unknown_values: Values treated as unknown for unknown-indicator
            encodings.
        positive_values: Values treated as positive for binary encodings.
        output_positive: Positive indicator column.
        output_unknown: Unknown indicator column.
        aliases: Backward-compatible aliases keyed by alias column.
    """

    input_column: str
    type: str
    output: str | None = None
    map: dict[str, float] | None = None
    unknown_value: float | None = None
    unknown_values: tuple[str | None, ...] = ()
    positive_values: tuple[str, ...] = ()
    output_positive: str | None = None
    output_unknown: str | None = None
    aliases: dict[str, str] | None = None

    @classmethod
    def from_mapping(cls, name: str, value: Mapping[str, Any]) -> "EncodingSpec":
        """Build an encoding specification from YAML.

        Args:
            name: Encoding mapping key.
            value: Encoding mapping.

        Returns:
            Parsed encoding specification.
        """
        data = _mapping(value, f"encodings.{name}")
        numeric_map = None
        if data.get("map") is not None:
            numeric_map = {
                str(key): float(child)
                for key, child in _mapping(data["map"], f"encodings.{name}.map").items()
            }
        aliases = None
        if data.get("aliases") is not None:
            aliases = {
                str(key): str(child)
                for key, child in _mapping(data["aliases"], f"encodings.{name}.aliases").items()
            }
        return cls(
            input_column=str(data.get("input_column", name)),
            type=str(data["type"]),
            output=None if data.get("output") is None else str(data["output"]),
            map=numeric_map,
            unknown_value=None
            if data.get("unknown_value") is None
            else float(data["unknown_value"]),
            unknown_values=tuple(
                None if item is None else str(item)
                for item in _tuple(data.get("unknown_values"), "unknown_values")
            ),
            positive_values=tuple(
                str(item)
                for item in _tuple(data.get("positive_values"), "positive_values")
            ),
            output_positive=None
            if data.get("output_positive") is None
            else str(data["output_positive"]),
            output_unknown=None
            if data.get("output_unknown") is None
            else str(data["output_unknown"]),
            aliases=aliases,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the encoding specification.

        Returns:
            YAML-compatible dictionary.
        """
        return {
            "type": self.type,
            "output": self.output,
            "map": self.map,
            "unknown_value": self.unknown_value,
            "unknown_values": list(self.unknown_values),
            "positive_values": list(self.positive_values),
            "output_positive": self.output_positive,
            "output_unknown": self.output_unknown,
            "aliases": self.aliases,
        }


@dataclass(frozen=True)
class AdjustmentSetSpec:
    """adjustment set を構築するためのルール。

    Attributes:
        include: Explicit covariate names, normalized from ``include`` or
            ``variables``.
        include_patterns: Regular expressions whose matching columns are
            appended.
        forbidden_roles: Feature roles that are not allowed in this set.
        reviewer_status: Review status metadata.
        description: Human-readable description.
    """

    include: tuple[str, ...]
    include_patterns: tuple[str, ...] = ()
    forbidden_roles: tuple[str, ...] = ()
    reviewer_status: str | None = None
    description: str = ""

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "AdjustmentSetSpec":
        """Build adjustment-set rules from YAML.

        Args:
            value: Adjustment-set mapping.

        Returns:
            Parsed adjustment-set specification.
        """
        data = _mapping(value, "adjustment_sets.*")
        variables = data.get("include", data.get("variables"))
        return cls(
            include=tuple(str(item) for item in _tuple(variables, "variables")),
            include_patterns=tuple(
                str(item)
                for item in _tuple(data.get("include_patterns"), "include_patterns")
            ),
            forbidden_roles=tuple(
                str(item)
                for item in _tuple(data.get("forbidden_roles"), "forbidden_roles")
            ),
            reviewer_status=None
            if data.get("reviewer_status") is None
            else str(data["reviewer_status"]),
            description=str(data.get("description", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the adjustment-set specification.

        Returns:
            YAML-compatible dictionary.
        """
        return {
            "description": self.description,
            "variables": list(self.include),
            "include_patterns": list(self.include_patterns),
            "forbidden_roles": list(self.forbidden_roles),
            "reviewer_status": self.reviewer_status,
        }


@dataclass(frozen=True)
class FeatureValidationSpec:
    """特徴量生成の validation と互換性 policy。

    Attributes:
        drop_constant_columns: Whether standardization drops constant columns.
        drop_all_missing_columns: Whether standardization drops all-missing
            columns.
        fail_on_missing_required_columns: Whether data loading validates table
            schemas.
        fail_on_unknown_aggregation: Whether unknown aggregations raise.
        dropped_column_notes: Configured compatibility notes added to dropped
            column output.
    """

    drop_constant_columns: bool = True
    drop_all_missing_columns: bool = True
    fail_on_missing_required_columns: bool = True
    fail_on_unknown_aggregation: bool = True
    dropped_column_notes: tuple[dict[str, str], ...] = ()

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "FeatureValidationSpec":
        """Build validation policy from YAML.

        Args:
            value: Mapping under ``feature_validation``.

        Returns:
            Parsed validation policy.
        """
        data = _mapping(value or {}, "feature_validation")
        notes = tuple(
            {"column": str(item["column"]), "reason": str(item["reason"])}
            for item in _tuple(data.get("dropped_column_notes"), "dropped_column_notes")
        )
        return cls(
            drop_constant_columns=bool(data.get("drop_constant_columns", cls.drop_constant_columns)),
            drop_all_missing_columns=bool(data.get("drop_all_missing_columns", cls.drop_all_missing_columns)),
            fail_on_missing_required_columns=bool(
                data.get(
                    "fail_on_missing_required_columns",
                    cls.fail_on_missing_required_columns,
                )
            ),
            fail_on_unknown_aggregation=bool(
                data.get("fail_on_unknown_aggregation", cls.fail_on_unknown_aggregation)
            ),
            dropped_column_notes=notes,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize validation policy.

        Returns:
            YAML-compatible dictionary.
        """
        return {
            "drop_constant_columns": self.drop_constant_columns,
            "drop_all_missing_columns": self.drop_all_missing_columns,
            "fail_on_missing_required_columns": self.fail_on_missing_required_columns,
            "fail_on_unknown_aggregation": self.fail_on_unknown_aggregation,
            "dropped_column_notes": list(self.dropped_column_notes),
        }


@dataclass(frozen=True)
class FeatureConfig:
    """解決済みの特徴量生成設定。

    Attributes:
        dataset: Dataset-level specification.
        tables: Logical table specifications.
        windows: Window specification mappings.
        treatment: Treatment definition mapping.
        aggregations: Aggregation blocks keyed by block name.
        encodings: Encoding specifications keyed by source column.
        adjustment_sets: Adjustment-set rules keyed by strategy.
        exclude_patterns: Regular expressions excluded from automatic
            adjustment sets.
        validation: Feature validation policy.
        raw_data: Original YAML mapping used for snapshot output.
    """

    dataset: DatasetSpec
    tables: dict[str, TableSpec]
    windows: dict[str, Any]
    treatment: dict[str, Any]
    aggregations: dict[str, AggregationBlockSpec]
    encodings: dict[str, EncodingSpec]
    adjustment_sets: dict[str, AdjustmentSetSpec]
    exclude_patterns: tuple[str, ...]
    validation: FeatureValidationSpec
    raw_data: dict[str, Any]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "FeatureConfig":
        """Build feature configuration from parsed YAML.

        Args:
            value: Parsed feature YAML mapping.

        Returns:
            Validated feature configuration.
        """
        data = dict(_mapping(value, "feature_config"))
        tables = {
            str(name): TableSpec.from_mapping(child)
            for name, child in _mapping(data.get("tables", {}), "tables").items()
        }
        aggregations = {
            str(name): AggregationBlockSpec.from_mapping(child)
            for name, child in _mapping(data.get("aggregations", {}), "aggregations").items()
        }
        encodings = {
            str(name): EncodingSpec.from_mapping(str(name), child)
            for name, child in _mapping(data.get("encodings", {}), "encodings").items()
        }
        adjustment_data = _mapping(data.get("adjustment_sets", {}), "adjustment_sets")
        adjustment_sets = {
            str(name): AdjustmentSetSpec.from_mapping(child)
            for name, child in adjustment_data.items()
            if name != "exclude_patterns"
        }
        exclude_patterns = tuple(
            str(item)
            for item in _tuple(
                adjustment_data.get("exclude_patterns", ()),
                "adjustment_sets.exclude_patterns",
            )
        )
        return cls(
            dataset=DatasetSpec.from_mapping(data["dataset"]),
            tables=tables,
            windows=dict(_mapping(data.get("windows", {}), "windows")),
            treatment=dict(_mapping(data.get("treatment", {}), "treatment")),
            aggregations=aggregations,
            encodings=encodings,
            adjustment_sets=adjustment_sets,
            exclude_patterns=exclude_patterns,
            validation=FeatureValidationSpec.from_mapping(data.get("feature_validation")),
            raw_data=data,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the feature configuration.

        Returns:
            YAML-compatible dictionary.
        """
        return self.raw_data


def load_feature_config(path: str | bytes | PathLike[str]) -> FeatureConfig:
    """特徴量設定 YAML を読み込む。

    Args:
        path: YAML ファイルパス。

    Returns:
        validation 済み特徴量設定。

    Raises:
        ValueError: YAML root が mapping でない場合。
    """
    return FeatureConfig.from_mapping(load_yaml_mapping(Path(fsdecode(path))))
