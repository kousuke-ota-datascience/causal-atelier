"""Pydantic schemas for the product web API."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ── Project ────────────────────────────────────────────────────────────────────

class ProjectCreate(BaseModel):
    name: str = Field(..., max_length=200)
    topic: str | None = None
    objective: str | None = None
    memo: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = Field(None, max_length=200)
    topic: str | None = None
    objective: str | None = None
    memo: str | None = None


class ProjectResponse(BaseModel):
    project_id: str
    name: str
    topic: str | None
    objective: str | None
    memo: str | None
    status: str
    created_at: datetime | None
    updated_at: datetime | None


# ── DatasetVersion ─────────────────────────────────────────────────────────────

class DatasetVersionResponse(BaseModel):
    dataset_version_id: str
    project_id: str
    source_artifact_id: str
    dataset_key: str
    name: str
    version_label: str
    content_hash: str
    column_schema: dict[str, Any]
    profile_summary: dict[str, Any]
    row_count: int
    column_count: int
    source_note: str | None
    created_at: datetime | None


class DatasetVersionListResponse(BaseModel):
    items: list[DatasetVersionResponse]
    next_cursor: str | None = None


# ── Execution ──────────────────────────────────────────────────────────────────

class ExecutionVariantSpecRequest(BaseModel):
    algorithm_or_estimator: str
    parameter_json: dict[str, Any] = Field(default_factory=dict)
    random_seed: int | None = None
    analysis_spec_json: dict[str, Any] = Field(default_factory=dict)
    objective_snapshot: str | None = None
    rationale_snapshot: str | None = None


class ExecutionBatchCreate(BaseModel):
    dataset_version_id: str
    operation: str  # DISCOVERY | ESTIMATION
    variants: list[ExecutionVariantSpecRequest]
    input_graph_version_id: str | None = None
    code_version: str = ""
    runtime_version_json: dict[str, Any] = Field(default_factory=dict)


class ExecutionBatchResponse(BaseModel):
    batch_key: str
    execution_ids: list[str]


class ExecutionResponse(BaseModel):
    execution_id: str
    project_id: str
    dataset_version_id: str
    input_graph_version_id: str | None
    batch_key: str
    operation: str
    algorithm_or_estimator: str
    status: str
    retry_count: int
    requested_by: str
    requested_at: datetime | None
    started_at: datetime | None
    finished_at: datetime | None
    last_error_summary: str | None


class ExecutionListResponse(BaseModel):
    items: list[ExecutionResponse]
    next_cursor: str | None = None


# ── Result ─────────────────────────────────────────────────────────────────────

class ResultResponse(BaseModel):
    result_id: str
    execution_id: str
    result_type: str
    scientific_status: str
    summary_json: dict[str, Any]
    payload_json: dict[str, Any]
    diagnostics_json: dict[str, Any]
    warning_json: list[Any]
    created_at: datetime | None


class ResultListResponse(BaseModel):
    items: list[ResultResponse]


# ── GraphVersion ───────────────────────────────────────────────────────────────

class GraphVersionCreate(BaseModel):
    source_result_id: str
    name: str = Field(..., max_length=200)
    graph_type: str
    graph_json: dict[str, Any]
    parent_graph_version_id: str | None = None
    edit_rationale: str | None = None


class GraphVersionUpdate(BaseModel):
    graph_json: dict[str, Any]
    edit_rationale: str | None = None


class GraphVersionResponse(BaseModel):
    graph_version_id: str
    project_id: str
    source_result_id: str
    parent_graph_version_id: str | None
    name: str
    graph_type: str
    graph_json: dict[str, Any]
    content_hash: str
    edit_rationale: str | None
    status: str
    created_by: str
    created_at: datetime | None


class GraphVersionListResponse(BaseModel):
    items: list[GraphVersionResponse]
    next_cursor: str | None = None


# ── Annotation ─────────────────────────────────────────────────────────────────

class AnnotationCreate(BaseModel):
    statement: str
    target_result_id: str | None = None
    target_graph_version_id: str | None = None
    rationale: str | None = None
    assumptions_json: list[Any] = Field(default_factory=list)
    limitations_json: list[Any] = Field(default_factory=list)


class AnnotationUpdate(BaseModel):
    statement: str | None = None
    rationale: str | None = None
    assumptions_json: list[Any] | None = None
    limitations_json: list[Any] | None = None


class AnnotationResponse(BaseModel):
    annotation_id: str
    project_id: str
    target_result_id: str | None
    target_graph_version_id: str | None
    statement: str
    rationale: str | None
    assumptions_json: list[Any]
    limitations_json: list[Any]
    created_by: str
    created_at: datetime | None
    updated_at: datetime | None


# ── Comparison / Lineage ────────────────────────────────────────────────────────

class ComparisonQueryRequest(BaseModel):
    result_ids: list[str] = Field(..., min_length=2, max_length=20)


class ComparisonResponse(BaseModel):
    common_conditions: dict[str, Any]
    changed_conditions: list[dict[str, Any]]
    result_differences: list[dict[str, Any]]
    warnings: list[str]
    lineage_summary: dict[str, Any]


class LineageNodeResponse(BaseModel):
    node_type: str
    entity_id: str
    label: str
    attributes: dict[str, Any]


class LineageResponse(BaseModel):
    nodes: list[LineageNodeResponse]
    edges: list[list[str]]  # [[from_id, to_id], ...]


# ── Error ──────────────────────────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    error_code: str
    message: str
    detail: dict[str, Any] | None = None
