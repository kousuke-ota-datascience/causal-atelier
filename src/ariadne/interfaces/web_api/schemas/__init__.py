"""Strict request/response contracts for API v1."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class ProjectCreate(StrictModel):
    name: str = Field(min_length=1, max_length=200)
    topic: str | None = Field(default=None, max_length=4000)
    objective: str | None = Field(default=None, max_length=4000)
    memo: str | None = Field(default=None, max_length=8000)


class ProjectUpdate(StrictModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    topic: str | None = Field(default=None, max_length=4000)
    objective: str | None = Field(default=None, max_length=4000)
    memo: str | None = Field(default=None, max_length=8000)


class ProjectResponse(StrictModel):
    project_id: str; name: str; topic: str | None; objective: str | None; memo: str | None
    status: str; created_at: datetime | None; updated_at: datetime | None


class ProjectListResponse(StrictModel):
    items: list[ProjectResponse]; next_cursor: str | None = None


class DatasetVersionResponse(StrictModel):
    dataset_version_id: str; project_id: str; source_artifact_id: str; dataset_key: str
    name: str; version_label: str; content_hash: str
    column_schema: dict[str, Any] = Field(alias="schema")
    profile_summary: dict[str, Any]; row_count: int; column_count: int
    source_note: str | None; created_at: datetime | None


class DatasetVersionListResponse(StrictModel):
    items: list[DatasetVersionResponse]; next_cursor: str | None = None


class DatasetPreviewResponse(StrictModel):
    dataset_version_id: str; columns: list[str]; rows: list[dict[str, Any]]; limit: int


class ExecutionVariantRequest(StrictModel):
    algorithm_or_estimator: str = Field(min_length=1, max_length=100)
    parameters: dict[str, Any] = Field(default_factory=dict)
    random_seed: int | None = None


class ExecutionBatchCreate(StrictModel):
    operation: Literal["DISCOVERY", "IDENTIFICATION", "ESTIMATION", "REFUTATION", "SENSITIVITY"]
    dataset_version_id: str
    input_graph_version_id: str | None = None
    input_result_id: str | None = None
    objective: str | None = Field(default=None, max_length=4000)
    rationale: str | None = Field(default=None, max_length=8000)
    analysis_spec: dict[str, Any]
    variants: list[ExecutionVariantRequest] = Field(min_length=1, max_length=20)
    code_version: str = Field(min_length=1, max_length=200)
    runtime_versions: dict[str, Any]
    base_execution_id: str | None = None
    change_reason: str | None = Field(default=None, max_length=8000)

    @model_validator(mode="after")
    def graph_matches_operation(self) -> "ExecutionBatchCreate":
        graph_required = self.operation != "DISCOVERY"
        upstream_required = self.operation in {"ESTIMATION", "REFUTATION", "SENSITIVITY"}
        if (self.input_graph_version_id is not None) != graph_required:
            raise ValueError("input_graph_version_id does not match operation")
        if (self.input_result_id is not None) != upstream_required:
            raise ValueError("input_result_id does not match operation")
        from ariadne.product.domain.analysis_spec import validate_analysis_spec
        from ariadne.product.domain.enums import ExecutionOperation
        from ariadne.product.domain.errors import InvalidAnalysisSpec
        try:
            if self.operation == "ESTIMATION":
                for variant in self.variants:
                    value = {
                        **self.analysis_spec,
                        "operation_spec": {
                            **self.analysis_spec.get("operation_spec", {}),
                            "estimator": variant.algorithm_or_estimator,
                        },
                    }
                    validate_analysis_spec(ExecutionOperation.ESTIMATION, value)
            else:
                validate_analysis_spec(ExecutionOperation(self.operation), self.analysis_spec)
        except InvalidAnalysisSpec as exc:
            raise ValueError(str(exc)) from exc
        return self


class ExecutionAccepted(StrictModel):
    execution_id: str; status: str
    scientific_warnings: list[dict[str, Any]] = Field(default_factory=list)


class ExecutionBatchResponse(StrictModel):
    batch_key: str; executions: list[ExecutionAccepted]


class ExecutionResponse(StrictModel):
    execution_id: str; project_id: str; dataset_version_id: str
    input_graph_version_id: str | None; input_result_id: str | None
    snapshot_schema_version: str; batch_key: str; operation: str
    algorithm_or_estimator: str; status: str; retry_count: int; requested_by: str
    requested_at: datetime | None; started_at: datetime | None; finished_at: datetime | None
    last_error_summary: str | None
    analysis_mode: str | None = None
    scientific_warnings: list[dict[str, Any]] = Field(default_factory=list)
    revision_context: dict[str, Any] | None = None


class ExecutionListResponse(StrictModel):
    items: list[ExecutionResponse]; next_cursor: str | None = None


class ExecutionPrefillResponse(StrictModel):
    operation: str; dataset_version_id: str; input_graph_version_id: str | None; input_result_id: str | None
    objective: str | None; rationale: str | None; analysis_spec: dict[str, Any]
    algorithm_or_estimator: str; parameters: dict[str, Any]; random_seed: int | None


class ResultResponse(StrictModel):
    result_id: str; execution_id: str; result_type: str; scientific_status: str
    summary: dict[str, Any]; payload: dict[str, Any]; diagnostics: dict[str, Any]
    warnings: list[Any]; artifact_ids: list[str] = Field(default_factory=list)
    created_at: datetime | None


class ResultListResponse(StrictModel): items: list[ResultResponse]


class GraphVersionCreate(StrictModel):
    source_result_id: str | None = None; parent_graph_version_id: str | None = None
    graph_origin: Literal["DISCOVERED", "CONSTRAINT_ADJUSTED", "USER_DEFINED", "IMPORTED", "USER_EDITED"]
    name: str = Field(min_length=1, max_length=200); graph_type: Literal["DAG", "CPDAG", "PAG"]
    graph: dict[str, Any]; provenance: dict[str, Any]
    edit_rationale: str | None = None; fix_immediately: bool = False


class GraphVersionUpdate(StrictModel):
    graph: dict[str, Any]; edit_rationale: str | None = None


class GraphVersionResponse(StrictModel):
    graph_version_id: str; project_id: str; source_result_id: str | None
    parent_graph_version_id: str | None; name: str; graph_type: str; graph: dict[str, Any]
    graph_origin: str; provenance: dict[str, Any]
    content_hash: str; edit_rationale: str | None; status: str; created_by: str
    created_at: datetime | None


class GraphVersionListResponse(StrictModel):
    items: list[GraphVersionResponse]; next_cursor: str | None = None


class AnnotationCreate(StrictModel):
    target_result_id: str | None = None; target_graph_version_id: str | None = None
    statement: str = Field(min_length=1, max_length=8000); rationale: str | None = None
    assumptions: list[Any] = Field(default_factory=list); limitations: list[Any] = Field(default_factory=list)


class AnnotationUpdate(StrictModel):
    statement: str | None = Field(default=None, min_length=1, max_length=8000)
    rationale: str | None = None; assumptions: list[Any] | None = None
    limitations: list[Any] | None = None


class AnnotationResponse(StrictModel):
    annotation_id: str; project_id: str; target_result_id: str | None
    target_graph_version_id: str | None; statement: str; rationale: str | None
    assumptions: list[Any]; limitations: list[Any]; created_by: str
    created_at: datetime | None; updated_at: datetime | None


class ComparisonQueryRequest(StrictModel):
    project_id: str; result_ids: list[str] = Field(min_length=2, max_length=20)


class ComparisonResponse(StrictModel):
    operation: str; common_conditions: dict[str, Any]; changed_conditions: list[dict[str, Any]]
    result_differences: list[dict[str, Any]]; warnings: list[str]
    lineage_summary: dict[str, Any]


class LineageNodeResponse(StrictModel):
    node_type: str; entity_id: str; label: str; attributes: dict[str, Any]


class LineageEdgeResponse(StrictModel):
    relation_type: str; from_id: str; to_id: str


class LineageResponse(StrictModel):
    root_result_id: str; nodes: list[LineageNodeResponse]; edges: list[LineageEdgeResponse]


class ArtifactResponse(StrictModel):
    artifact_id: str; project_id: str; execution_id: str | None; result_id: str | None
    artifact_type: str; object_key: str; content_hash: str; media_type: str
    size_bytes: int; metadata: dict[str, Any]; created_at: datetime | None


class ErrorBody(StrictModel):
    code: str; message: str; details: dict[str, Any]; request_id: str


class ErrorResponse(StrictModel): error: ErrorBody
