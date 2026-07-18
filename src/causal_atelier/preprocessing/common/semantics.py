"""Feature semantics shared by discovery, inference, and runtime validation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class FeatureRole(str, Enum):
    """Causal role assigned to a feature."""

    TREATMENT = "treatment"
    OUTCOME = "outcome"
    COVARIATE = "covariate"
    MEDIATOR = "mediator"
    COLLIDER = "collider"
    POST_TREATMENT = "post_treatment"


_ROLE_ALIASES = {
    "baseline": FeatureRole.COVARIATE,
    "pre_treatment_behavior": FeatureRole.COVARIATE,
    "pre_treatment_covariate": FeatureRole.COVARIATE,
}


@dataclass(frozen=True)
class FeatureSemanticSpec:
    """Semantic contract for one feature."""

    name: str
    role: FeatureRole
    source_table: str
    source_column: str | None
    unit_id: str
    aggregation: str | None = None
    transform: str | None = None
    dtype: str | None = None
    allowed_for_adjustment: bool = False
    post_treatment: bool = False
    metadata: dict[str, Any] | None = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any], *, default_unit_id: str = "household_id") -> "FeatureSemanticSpec":
        """Build a semantic spec from a YAML mapping."""

        raw_role = str(value.get("role", "covariate"))
        role = _ROLE_ALIASES[raw_role] if raw_role in _ROLE_ALIASES else FeatureRole(raw_role)
        return cls(
            name=str(value["name"]),
            role=role,
            source_table=str(value.get("source_table", "")),
            source_column=None if value.get("source_column") is None else str(value["source_column"]),
            unit_id=str(value.get("unit_id", default_unit_id)),
            aggregation=None if value.get("aggregation") is None else str(value["aggregation"]),
            transform=None if value.get("transform") is None else str(value["transform"]),
            dtype=None if value.get("dtype", value.get("data_type")) is None else str(value.get("dtype", value.get("data_type"))),
            allowed_for_adjustment=bool(
                value.get("allowed_for_adjustment", role == FeatureRole.COVARIATE)
            ),
            post_treatment=bool(value.get("post_treatment", role == FeatureRole.POST_TREATMENT)),
            metadata=dict(value),
        )

    def comparable_fields(self) -> dict[str, Any]:
        """Return fields used for cross-stage semantic comparison."""

        return {
            "role": self.role.value,
            "source_table": self.source_table,
            "source_column": self.source_column,
            "unit_id": self.unit_id,
            "aggregation": self.aggregation,
            "transform": self.transform,
            "dtype": self.dtype,
            "allowed_for_adjustment": self.allowed_for_adjustment,
            "post_treatment": self.post_treatment,
        }

    def to_dict(self) -> dict[str, Any]:
        """Serialize the spec."""

        return {
            "name": self.name,
            **self.comparable_fields(),
        }


@dataclass(frozen=True)
class FeatureSemanticsCatalog:
    """Named collection of feature semantics."""

    features: tuple[FeatureSemanticSpec, ...]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "FeatureSemanticsCatalog":
        """Build a catalog from ``features: [...]`` YAML data."""

        features = value.get("features", [])
        default_unit = str(value.get("unit_id", "household_id"))
        return cls(
            tuple(
                FeatureSemanticSpec.from_mapping(item, default_unit_id=default_unit)
                for item in features
            )
        )

    @classmethod
    def from_feature_config_mapping(cls, value: Mapping[str, Any]) -> "FeatureSemanticsCatalog":
        """Build semantics from the existing discovery/inference feature config shape."""

        unit_id = str(value.get("dataset", {}).get("unit_key", value.get("metadata", {}).get("entity_id", "household_id")))
        records: list[FeatureSemanticSpec] = []
        raw_features = value.get("features")
        if isinstance(raw_features, Mapping):
            for group in raw_features.values():
                for item in group or []:
                    records.append(FeatureSemanticSpec.from_mapping(item, default_unit_id=unit_id))
        if value.get("treatment"):
            treatment = dict(value["treatment"])
            treatment.setdefault("name", treatment.get("name", "treated"))
            treatment.setdefault("role", "treatment")
            treatment.setdefault("unit_id", unit_id)
            records.append(FeatureSemanticSpec.from_mapping(treatment, default_unit_id=unit_id))
        for block_name, block in dict(value.get("aggregations", {})).items():
            prefix = str(block.get("prefix", block_name))
            source_table = str(block.get("source_table", ""))
            window = str(dict(block.get("filters", {})).get("window", block.get("window", "")))
            role = FeatureRole.OUTCOME if window == "outcome" else FeatureRole.COVARIATE
            for metric_name, metric in dict(block.get("metrics", {})).items():
                records.append(
                    FeatureSemanticSpec(
                        name=f"{prefix}_{metric_name}",
                        role=role,
                        source_table=source_table,
                        source_column=None if metric.get("column") is None else str(metric.get("column")),
                        unit_id=unit_id,
                        aggregation=str(metric.get("agg")),
                        transform=None,
                        dtype=None,
                        allowed_for_adjustment=role == FeatureRole.COVARIATE,
                        post_treatment=role == FeatureRole.OUTCOME,
                    )
                )
        for name, encoding in dict(value.get("encodings", {})).items():
            output_names = _encoding_output_names(str(name), dict(encoding))
            for output_name in output_names:
                records.append(
                    FeatureSemanticSpec(
                        name=output_name,
                        role=FeatureRole.COVARIATE,
                        source_table="demographics",
                        source_column=str(encoding.get("input_column", name)),
                        unit_id=unit_id,
                        transform=str(encoding.get("type", "identity")),
                        dtype=None,
                        allowed_for_adjustment=True,
                    )
                )
        deduped = {item.name: item for item in records}
        return cls(tuple(deduped[name] for name in sorted(deduped)))

    def by_name(self) -> dict[str, FeatureSemanticSpec]:
        """Return specs keyed by feature name."""

        return {feature.name: feature for feature in self.features}

    def to_dict(self) -> dict[str, Any]:
        """Serialize the catalog."""

        return {"features": [feature.to_dict() for feature in self.features]}


def _encoding_output_names(name: str, encoding: Mapping[str, Any]) -> list[str]:
    if encoding.get("type") == "binary_with_unknown":
        names = []
        aliases = dict(encoding.get("aliases") or {})
        names.extend(str(alias) for alias in aliases)
        if encoding.get("output_positive") is not None:
            names.append(str(encoding["output_positive"]))
        if encoding.get("output_unknown") is not None:
            names.append(str(encoding["output_unknown"]))
        return names
    if encoding.get("type") == "one_hot" and encoding.get("output") is not None:
        return [str(encoding["output"])]
    return [str(encoding.get("output", name))]


def compare_feature_semantics(
    left: FeatureSemanticsCatalog,
    right: FeatureSemanticsCatalog,
) -> list[str]:
    """Return human-readable semantic mismatches."""

    left_by_name = left.by_name()
    right_by_name = right.by_name()
    issues: list[str] = []
    for name in sorted(set(left_by_name).difference(right_by_name)):
        issues.append(f"feature missing from right catalog: {name}")
    for name in sorted(set(right_by_name).difference(left_by_name)):
        issues.append(f"feature missing from left catalog: {name}")
    for name in sorted(set(left_by_name).intersection(right_by_name)):
        left_fields = left_by_name[name].comparable_fields()
        right_fields = right_by_name[name].comparable_fields()
        for field, left_value in left_fields.items():
            right_value = right_fields[field]
            if left_value != right_value:
                issues.append(
                    f"feature semantics mismatch for {name}.{field}: {left_value!r} != {right_value!r}"
                )
    return issues


__all__ = [
    "FeatureRole",
    "FeatureSemanticSpec",
    "FeatureSemanticsCatalog",
    "compare_feature_semantics",
]
