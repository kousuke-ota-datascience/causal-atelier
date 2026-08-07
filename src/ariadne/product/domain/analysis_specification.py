"""Common envelope for exploratory, causal, and predictive specifications."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ariadne.product.domain.analysis_spec import validate_analysis_spec
from ariadne.product.domain.enums import (
    AnalysisFamily,
    AnalysisMode,
    ExecutionOperation,
    VersionedResourceStatus,
)
from ariadne.product.domain.errors import InvalidAnalysisSpec, InvalidSchema, ResourceImmutable
from ariadne.product.domain.schemas import SchemaRegistry, canonical_hash, reject_unknown

SPECIFICATION_SCHEMA_VERSION = "analysis-specification/1"
EXPLORATORY_SCHEMA_VERSION = "exploratory-analysis-spec/1"
PREDICTIVE_SCHEMA_VERSION = "predictive-analysis-spec/1"

_ENVELOPE_FIELDS = {
    "schema_version", "analysis_family", "research_context_version_id",
    "dataset_version_id", "analysis_view_id", "analysis_mode",
    "family_spec_schema_version", "family_spec", "revision_context", "warnings",
}
_EXPLORATORY_OPERATIONS = {
    "PROFILE", "DISTRIBUTION", "ASSOCIATION", "GROUP_SUMMARY", "TIME_TREND", "CHART",
}


def validate_exploratory_spec(payload: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "schema_version", "operation", "columns", "grouping", "aggregation",
        "chart_encoding", "filter", "sampling", "expected_output_type",
    }
    reject_unknown(payload, allowed, name="exploratory specification")
    if payload.get("schema_version") != EXPLORATORY_SCHEMA_VERSION:
        raise InvalidSchema(f"schema_version must be {EXPLORATORY_SCHEMA_VERSION}")
    if payload.get("operation") not in _EXPLORATORY_OPERATIONS:
        raise InvalidSchema("Unsupported exploratory operation")
    columns = payload.get("columns", [])
    if not isinstance(columns, list) or any(not isinstance(item, str) or not item for item in columns):
        raise InvalidSchema("columns must be a string array")
    return payload


def validate_predictive_spec(payload: dict[str, Any]) -> dict[str, Any]:
    from ariadne.capabilities.predictive.validation import validate_predictive_specification

    return validate_predictive_specification(payload)


def default_schema_registry() -> SchemaRegistry:
    registry = SchemaRegistry()
    registry.register(EXPLORATORY_SCHEMA_VERSION, validate_exploratory_spec)
    registry.register(PREDICTIVE_SCHEMA_VERSION, validate_predictive_spec)

    def causal(payload: dict[str, Any]) -> dict[str, Any]:
        operation = payload.get("operation")
        if operation is None:
            operation_spec = payload.get("operation_spec", {})
            operation = operation_spec.get("operation") if isinstance(operation_spec, dict) else None
        try:
            parsed_operation = ExecutionOperation(str(operation))
        except ValueError as exc:
            raise InvalidAnalysisSpec("Causal family_spec requires a valid operation") from exc
        causal_payload = dict(payload)
        causal_payload.pop("operation", None)
        if isinstance(causal_payload.get("operation_spec"), dict):
            causal_payload["operation_spec"] = dict(causal_payload["operation_spec"])
            causal_payload["operation_spec"].pop("operation", None)
        validate_analysis_spec(parsed_operation, causal_payload)
        return payload

    registry.register("causal-analysis-spec/2", causal)
    return registry


@dataclass
class AnalysisSpecification:
    analysis_specification_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str = ""
    specification_key: str = ""
    version_number: int = 1
    status: VersionedResourceStatus = VersionedResourceStatus.DRAFT
    analysis_family: AnalysisFamily = AnalysisFamily.EXPLORATORY
    research_context_version_id: str = ""
    dataset_version_id: str = ""
    analysis_view_id: str | None = None
    analysis_mode: AnalysisMode = AnalysisMode.EXPLORATORY
    family_spec_schema_version: str = EXPLORATORY_SCHEMA_VERSION
    family_spec: dict[str, Any] = field(default_factory=dict)
    revision_context: dict[str, Any] | None = None
    warnings: list[dict[str, Any]] = field(default_factory=list)
    canonical_hash: str | None = None
    created_by: str = ""
    created_at: datetime | None = None

    def update(self, **changes: Any) -> None:
        if self.status is VersionedResourceStatus.FIXED:
            raise ResourceImmutable("FIXED Analysis Specification cannot be updated")
        mutable = {
            "analysis_family", "research_context_version_id", "dataset_version_id",
            "analysis_view_id", "analysis_mode", "family_spec_schema_version", "family_spec",
            "revision_context", "warnings",
        }
        unknown = set(changes) - mutable
        if unknown:
            raise InvalidSchema(f"Unknown Analysis Specification fields: {sorted(unknown)}")
        for name, value in changes.items():
            setattr(self, name, value)

    def envelope(self) -> dict[str, Any]:
        return {
            "schema_version": SPECIFICATION_SCHEMA_VERSION,
            "analysis_family": self.analysis_family.value,
            "research_context_version_id": self.research_context_version_id,
            "dataset_version_id": self.dataset_version_id,
            "analysis_view_id": self.analysis_view_id,
            "analysis_mode": self.analysis_mode.value,
            "family_spec_schema_version": self.family_spec_schema_version,
            "family_spec": self.family_spec,
            "revision_context": self.revision_context,
            "warnings": self.warnings,
        }

    def validate(self, registry: SchemaRegistry | None = None) -> None:
        payload = self.envelope()
        reject_unknown(payload, _ENVELOPE_FIELDS, name="Analysis Specification")
        if not self.project_id or not self.specification_key or self.version_number < 1:
            raise InvalidSchema("Analysis Specification identity is invalid")
        if not self.research_context_version_id or not self.dataset_version_id:
            raise InvalidSchema("Context and Dataset references are required")
        expected = {
            AnalysisFamily.EXPLORATORY: EXPLORATORY_SCHEMA_VERSION,
            AnalysisFamily.CAUSAL: "causal-analysis-spec/2",
            AnalysisFamily.PREDICTIVE: PREDICTIVE_SCHEMA_VERSION,
        }[self.analysis_family]
        if self.family_spec_schema_version != expected:
            raise InvalidSchema(
                f"{self.analysis_family.value} requires family schema {expected}"
            )
        (registry or default_schema_registry()).validate(
            self.family_spec_schema_version, self.family_spec
        )

    def fix(self, registry: SchemaRegistry | None = None) -> None:
        if self.status is VersionedResourceStatus.FIXED:
            return
        self.validate(registry)
        self.canonical_hash = canonical_hash(self.envelope())
        self.status = VersionedResourceStatus.FIXED
