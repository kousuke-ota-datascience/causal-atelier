"""Typed, immutable analysis-view specification."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ariadne.product.domain.enums import VersionedResourceStatus
from ariadne.product.domain.errors import InvalidSchema, ResourceImmutable
from ariadne.product.domain.schemas import canonical_hash, reject_unknown

VIEW_SCHEMA_VERSION = "analysis-view/1"
_VIEW_FIELDS = {
    "schema_version", "source_dataset_version_id", "row_filter", "selected_columns",
    "derived_columns", "missing_value_policy", "time_cutoff", "sampling",
}


def validate_analysis_view_payload(payload: dict[str, Any]) -> dict[str, Any]:
    reject_unknown(payload, _VIEW_FIELDS, name="Analysis View")
    if set(payload) != _VIEW_FIELDS:
        raise InvalidSchema(f"Analysis View fields are required: {sorted(_VIEW_FIELDS - set(payload))}")
    if payload["schema_version"] != VIEW_SCHEMA_VERSION:
        raise InvalidSchema(f"schema_version must be {VIEW_SCHEMA_VERSION}")
    if not isinstance(payload["source_dataset_version_id"], str) or not payload["source_dataset_version_id"]:
        raise InvalidSchema("source_dataset_version_id is required")
    for name in ("row_filter", "selected_columns", "derived_columns"):
        if not isinstance(payload[name], list):
            raise InvalidSchema(f"{name} must be an array")
    if len(payload["selected_columns"]) != len(set(payload["selected_columns"])):
        raise InvalidSchema("selected_columns must be unique")
    if not isinstance(payload["missing_value_policy"], dict):
        raise InvalidSchema("missing_value_policy must be an object")
    derived_names = [item.get("name") for item in payload["derived_columns"] if isinstance(item, dict)]
    if len(derived_names) != len(payload["derived_columns"]) or len(derived_names) != len(set(derived_names)):
        raise InvalidSchema("derived column names must exist and be unique")
    return payload


@dataclass
class AnalysisView:
    analysis_view_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str = ""
    view_key: str = ""
    version_number: int = 1
    name: str = ""
    status: VersionedResourceStatus = VersionedResourceStatus.DRAFT
    view_spec: dict[str, Any] = field(default_factory=dict)
    canonical_hash: str | None = None
    created_by: str = ""
    created_at: datetime | None = None

    def update(self, view_spec: dict[str, Any], *, name: str | None = None) -> None:
        if self.status is VersionedResourceStatus.FIXED:
            raise ResourceImmutable("FIXED Analysis View cannot be updated")
        validate_analysis_view_payload(view_spec)
        self.view_spec = dict(view_spec)
        if name is not None:
            self.name = name

    def fix(self) -> None:
        if self.status is VersionedResourceStatus.FIXED:
            return
        validate_analysis_view_payload(self.view_spec)
        if not self.project_id or not self.view_key or self.version_number < 1:
            raise InvalidSchema("Analysis View identity is invalid")
        self.canonical_hash = canonical_hash(self.view_spec)
        self.status = VersionedResourceStatus.FIXED
