from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from ariadne.infrastructure.config import (
    clean_none_values as _clean_dict,
    ensure_mapping as _as_mapping,
    ensure_tuple as _as_tuple,
    load_yaml_mapping,
)

from ariadne.causal.discovery.constants import ALLOWED_AGGREGATIONS, ALLOWED_TRANSFORMS


@dataclass(frozen=True)
class CategoryMidpoint:
    """1 つの順序カテゴリと numeric midpoint。

    Attributes:
        label: Category label as it appears in the source data.
        midpoint: Numeric midpoint used for ordinal approximation.
    """

    label: str
    midpoint: float

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "CategoryMidpoint":
        """Build a category midpoint from YAML data.

        Args:
            value: Mapping with ``label`` and ``midpoint`` keys.

        Returns:
            Parsed category midpoint.
        """
        data = _as_mapping(value, "category")
        return cls(label=str(data["label"]), midpoint=float(data["midpoint"]))

    def to_dict(self) -> dict[str, Any]:
        """Serialize the category midpoint to YAML-compatible data.

        Returns:
            Dictionary representation.
        """
        return {"label": self.label, "midpoint": self.midpoint}


@dataclass(frozen=True)
class CategoricalMapping:
    """順序カテゴリ値から numeric midpoint への mapping。

    Attributes:
        type: Mapping type, currently ``ordered_midpoint``.
        categories: Ordered categories and midpoint values.
        unknown_values: Source values treated as unknown.
        unit: Optional unit label for documentation.
    """

    type: str
    categories: tuple[CategoryMidpoint, ...]
    unknown_values: tuple[Any, ...] = ()
    unit: str | None = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "CategoricalMapping":
        """Build a categorical mapping from YAML data.

        Args:
            value: Mapping under a ``categorical_mappings`` entry.

        Returns:
            Parsed categorical mapping.
        """
        data = _as_mapping(value, "categorical_mapping")
        return cls(
            type=str(data.get("type", "ordered_midpoint")),
            categories=tuple(CategoryMidpoint.from_mapping(item) for item in data.get("categories", [])),
            unknown_values=_as_tuple(data.get("unknown_values"), "categorical_mapping.unknown_values"),
            unit=str(data["unit"]) if data.get("unit") is not None else None,
        )

    def midpoint_map(self) -> dict[str, float]:
        """Return category label to midpoint mapping.

        Returns:
            Dictionary mapping source labels to numeric midpoints.
        """
        return {category.label: category.midpoint for category in self.categories}

    def median_midpoint(self) -> float:
        """Return the median of configured midpoint values.

        Returns:
            Median midpoint used as an imputation value.

        Raises:
            ValueError: If no categories are configured.
        """
        if not self.categories:
            raise ValueError("ordered midpoint mapping must contain categories")
        values = sorted(category.midpoint for category in self.categories)
        middle = len(values) // 2
        if len(values) % 2:
            return values[middle]
        return (values[middle - 1] + values[middle]) / 2

    def to_dict(self) -> dict[str, Any]:
        """Serialize the categorical mapping to YAML-compatible data.

        Returns:
            Dictionary representation.
        """
        return _clean_dict(
            {
                "type": self.type,
                "unit": self.unit,
                "unknown_values": list(self.unknown_values),
                "categories": [category.to_dict() for category in self.categories],
            }
        )


@dataclass(frozen=True)
class TableSpec:
    """feature engineering で使う source table と column 名。

    Attributes:
        name: Dataset registry entry name.
        household_key: Household identifier column.
        campaign_id: Campaign identifier column.
        week: Transaction week column.
        start_day: Campaign start-day column.
        end_day: Campaign end-day column.
        transaction_timestamp: Transaction timestamp column.
    """

    name: str
    household_key: str | None = None
    campaign_id: str | None = None
    week: str | None = None
    start_day: str | None = None
    end_day: str | None = None
    transaction_timestamp: str | None = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TableSpec":
        """Build a table specification from YAML data.

        Args:
            value: Mapping under a ``tables`` entry.

        Returns:
            Parsed table specification.
        """
        data = _as_mapping(value, "table spec")
        return cls(
            name=str(data["name"]),
            household_key=str(data["household_key"]) if data.get("household_key") is not None else None,
            campaign_id=str(data["campaign_id"]) if data.get("campaign_id") is not None else None,
            week=str(data["week"]) if data.get("week") is not None else None,
            start_day=str(data["start_day"]) if data.get("start_day") is not None else None,
            end_day=str(data["end_day"]) if data.get("end_day") is not None else None,
            transaction_timestamp=(
                str(data["transaction_timestamp"]) if data.get("transaction_timestamp") is not None else None
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the table specification to YAML-compatible data.

        Returns:
            Dictionary representation.
        """
        return _clean_dict(
            {
                "name": self.name,
                "household_key": self.household_key,
                "campaign_id": self.campaign_id,
                "week": self.week,
                "start_day": self.start_day,
                "end_day": self.end_day,
                "transaction_timestamp": self.transaction_timestamp,
            }
        )


@dataclass(frozen=True)
class FeatureSpec:
    """生成される探索 feature 1 つ分の仕様。

    Attributes:
        name: Output feature name.
        source_table: Logical source table name.
        source_column: Source column name.
        transform: Allowlisted transform name.
        role: Analytical role, such as baseline, treatment, or outcome.
        data_type: Variable data type used for metadata.
        background_tier: Temporal tier for background knowledge.
        used_in_discovery: Whether the feature is included in discovery input.
        fisherz_caution: Whether Fisher-z assumptions need caution.
        mapping: Optional categorical mapping name.
        unknown_values: Values treated as unknown.
        value: Reference value for equality transforms.
        window: Transaction window name.
        aggregation: Household-level aggregation name.
        fill_value: Value used after household-level reindexing.
    """

    name: str
    source_table: str
    source_column: str
    transform: str = "identity"
    role: str | None = None
    data_type: str | None = None
    background_tier: str | None = None
    used_in_discovery: bool = True
    fisherz_caution: bool = False
    mapping: str | None = None
    unknown_values: tuple[Any, ...] = ()
    value: Any = None
    window: str | None = None
    aggregation: str | None = None
    fill_value: Any = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "FeatureSpec":
        """Build a feature specification from YAML data.

        Args:
            value: One feature mapping from ``features.yaml``.

        Returns:
            Parsed feature specification.

        Raises:
            ValueError: If transform, aggregation, or required metadata is
                invalid.
        """
        data = _as_mapping(value, "feature spec")
        transform = str(data.get("transform", "identity"))
        if transform not in ALLOWED_TRANSFORMS:
            raise ValueError(f"feature transform is not supported: {transform}")
        aggregation = str(data["aggregation"]) if data.get("aggregation") is not None else None
        if aggregation is not None and aggregation not in ALLOWED_AGGREGATIONS:
            raise ValueError(f"feature aggregation is not supported: {aggregation}")
        spec = cls(
            name=str(data["name"]),
            source_table=str(data["source_table"]),
            source_column=str(data["source_column"]),
            transform=transform,
            role=str(data["role"]) if data.get("role") is not None else None,
            data_type=str(data["data_type"]) if data.get("data_type") is not None else None,
            background_tier=str(data["background_tier"]) if data.get("background_tier") is not None else None,
            used_in_discovery=bool(data.get("used_in_discovery", True)),
            fisherz_caution=bool(data.get("fisherz_caution", False)),
            mapping=str(data["mapping"]) if data.get("mapping") is not None else None,
            unknown_values=_as_tuple(data.get("unknown_values"), "feature.unknown_values"),
            value=data.get("value"),
            window=str(data["window"]) if data.get("window") is not None else None,
            aggregation=aggregation,
            fill_value=data.get("fill_value"),
        )
        if spec.used_in_discovery and (not spec.role or not spec.data_type):
            raise ValueError(f"used feature must define role and data_type: {spec.name}")
        return spec

    def to_dict(self) -> dict[str, Any]:
        """Serialize the feature specification to YAML-compatible data.

        Returns:
            Dictionary representation.
        """
        return _clean_dict(
            {
                "name": self.name,
                "source_table": self.source_table,
                "source_column": self.source_column,
                "window": self.window,
                "aggregation": self.aggregation,
                "fill_value": self.fill_value,
                "transform": self.transform,
                "mapping": self.mapping,
                "unknown_values": list(self.unknown_values) if self.unknown_values else None,
                "value": self.value,
                "role": self.role,
                "data_type": self.data_type,
                "background_tier": self.background_tier,
                "used_in_discovery": self.used_in_discovery,
                "fisherz_caution": self.fisherz_caution,
            }
        )


@dataclass(frozen=True)
class BackgroundKnowledgeConfig:
    """``features.yaml`` の temporal background knowledge 設定。

    Attributes:
        tier_order: Ordered causal tiers from earlier to later.
        forbid_backward_edges: Whether backward edges should be disallowed by
            the downstream background-knowledge object.
        tiers: Optional explicit mapping from tier name to feature names.
    """

    tier_order: tuple[str, ...]
    forbid_backward_edges: bool = True
    tiers: dict[str, tuple[str, ...]] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "BackgroundKnowledgeConfig":
        """Build background knowledge configuration from YAML data.

        Args:
            value: Mapping under ``background_knowledge``.

        Returns:
            Parsed background knowledge configuration.
        """
        data = _as_mapping(value or {}, "background_knowledge")
        tiers = {
            str(tier): tuple(str(name) for name in names)
            for tier, names in _as_mapping(data.get("tiers", {}), "background_knowledge.tiers").items()
        }
        return cls(
            tier_order=tuple(str(item) for item in data.get("tier_order", ("baseline", "pre", "treatment", "outcome"))),
            forbid_backward_edges=bool(data.get("forbid_backward_edges", True)),
            tiers=tiers,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize background knowledge settings to YAML-compatible data.

        Returns:
            Dictionary representation.
        """
        data: dict[str, Any] = {
            "tier_order": list(self.tier_order),
            "forbid_backward_edges": self.forbid_backward_edges,
        }
        if self.tiers:
            data["tiers"] = {tier: list(names) for tier, names in self.tiers.items()}
        return data


@dataclass(frozen=True)
class FeatureConfig:
    """feature generation 設定の top-level object。

    Attributes:
        metadata: Global feature metadata such as entity and time columns.
        tables: Logical source table specifications.
        campaign_window: Campaign window calculation settings.
        categorical_mappings: Named categorical-to-numeric mappings.
        features: Feature specifications grouped by role or period.
        background_knowledge: Temporal tier configuration.
    """

    metadata: dict[str, Any]
    tables: dict[str, TableSpec]
    campaign_window: dict[str, Any]
    categorical_mappings: dict[str, CategoricalMapping]
    features: dict[str, tuple[FeatureSpec, ...]]
    background_knowledge: BackgroundKnowledgeConfig

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "FeatureConfig":
        """Build feature configuration from YAML data.

        Args:
            value: Parsed ``features.yaml`` mapping.

        Returns:
            Validated feature configuration.

        Raises:
            ValueError: If feature references, transforms, or tiers are invalid.
        """
        data = _as_mapping(value, "feature config")
        tables = {
            str(name): TableSpec.from_mapping(table)
            for name, table in _as_mapping(data.get("tables", {}), "tables").items()
        }
        mappings = {
            str(name): CategoricalMapping.from_mapping(mapping)
            for name, mapping in _as_mapping(data.get("categorical_mappings", {}), "categorical_mappings").items()
        }
        features = {
            str(group): tuple(FeatureSpec.from_mapping(item) for item in specs)
            for group, specs in _as_mapping(data.get("features", {}), "features").items()
        }
        config = cls(
            metadata=dict(_as_mapping(data.get("metadata", {}), "metadata")),
            tables=tables,
            campaign_window=dict(_as_mapping(data.get("campaign_window", {}), "campaign_window")),
            categorical_mappings=mappings,
            features=features,
            background_knowledge=BackgroundKnowledgeConfig.from_mapping(data.get("background_knowledge")),
        )
        config.validate()
        return config

    def all_features(self) -> tuple[FeatureSpec, ...]:
        """Return all configured feature specifications.

        Returns:
            Tuple of feature specifications in YAML group order.
        """
        return tuple(spec for specs in self.features.values() for spec in specs)

    def used_feature_specs(self) -> tuple[FeatureSpec, ...]:
        """Return features marked for discovery use.

        Returns:
            Tuple of feature specifications where ``used_in_discovery`` is true.
        """
        return tuple(spec for spec in self.all_features() if spec.used_in_discovery)

    def feature_by_name(self) -> dict[str, FeatureSpec]:
        """Index feature specifications by output name.

        Returns:
            Mapping from feature name to specification.
        """
        return {spec.name: spec for spec in self.all_features()}

    def features_for_source_table(self, source_table: str) -> tuple[FeatureSpec, ...]:
        """Select discovery features generated from one logical source table.

        Args:
            source_table: Logical table name from ``features.yaml``.

        Returns:
            Tuple of used feature specifications for that table.
        """
        return tuple(spec for spec in self.used_feature_specs() if spec.source_table == source_table)

    def background_tiers_for_nodes(self, node_names: list[str]) -> list[set[str]]:
        """Build tier assignments for retained discovery nodes.

        Args:
            node_names: Variables retained in the discovery input.

        Returns:
            List of node-name sets ordered by configured tier order.
        """
        node_set = set(node_names)
        feature_by_name = self.feature_by_name()
        tier_map: dict[str, set[str]] = {tier: set() for tier in self.background_knowledge.tier_order}

        for spec in feature_by_name.values():
            if spec.name in node_set and spec.background_tier in tier_map:
                tier_map[spec.background_tier].add(spec.name)

        for tier, names in self.background_knowledge.tiers.items():
            if tier not in tier_map:
                continue
            tier_map[tier].update(name for name in names if name in node_set)

        return [tier_map[tier] for tier in self.background_knowledge.tier_order]

    def validate(self) -> None:
        """Validate cross-field references in the feature configuration.

        Raises:
            ValueError: If feature names are duplicated, references point to
                unknown tables/mappings/tiers, or transaction features are
                incomplete.
        """
        names = [spec.name for spec in self.all_features()]
        duplicates = sorted({name for name in names if names.count(name) > 1})
        if duplicates:
            raise ValueError(f"features[*].name must be unique: {duplicates}")

        known_tables = set(self.tables)
        known_mappings = set(self.categorical_mappings)
        tier_order = set(self.background_knowledge.tier_order)
        feature_names = set(names)

        for spec in self.all_features():
            if spec.source_table not in known_tables:
                raise ValueError(f"feature source_table is unknown: {spec.name} -> {spec.source_table}")
            if spec.mapping is not None and spec.mapping not in known_mappings:
                raise ValueError(f"feature mapping is unknown: {spec.name} -> {spec.mapping}")
            if spec.background_tier is not None and spec.background_tier not in tier_order:
                raise ValueError(f"feature background_tier is unknown: {spec.name} -> {spec.background_tier}")
            if spec.source_table == "transactions" and (spec.window is None or spec.aggregation is None):
                raise ValueError(f"transaction feature must define window and aggregation: {spec.name}")

        for tier, tier_features in self.background_knowledge.tiers.items():
            if tier not in tier_order:
                raise ValueError(f"background_knowledge.tiers contains unknown tier: {tier}")
            unknown_features = set(tier_features).difference(feature_names)
            if unknown_features:
                raise ValueError(
                    f"background_knowledge.tiers.{tier} contains unknown features: {sorted(unknown_features)}"
                )

    def to_dict(self) -> dict[str, Any]:
        """Serialize feature configuration to YAML-compatible data.

        Returns:
            Dictionary representation.
        """
        return {
            "metadata": self.metadata,
            "tables": {name: table.to_dict() for name, table in self.tables.items()},
            "campaign_window": self.campaign_window,
            "categorical_mappings": {
                name: mapping.to_dict() for name, mapping in self.categorical_mappings.items()
            },
            "features": {
                group: [spec.to_dict() for spec in specs]
                for group, specs in self.features.items()
            },
            "background_knowledge": self.background_knowledge.to_dict(),
        }

def load_feature_config(path: Path) -> FeatureConfig:
    """feature 設定ファイルを読み込み validation する。

    Args:
        path: Path to ``features.yaml``.

    Returns:
        Validated feature configuration.
    """
    return FeatureConfig.from_mapping(load_yaml_mapping(path))
