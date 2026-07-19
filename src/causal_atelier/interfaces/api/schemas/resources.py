"""Pydantic schemas kept separate from persistence and analysis models."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, model_validator


class ApiModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")


class Page(ApiModel):
    items: list[dict[str, Any]]
    total: int
    page: int
    limit: int


class ProjectCreate(ApiModel):
    slug: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{1,62}$")
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None


class ProjectUpdate(ApiModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None


class MemberCreate(ApiModel):
    user_id: str
    role: Literal["VIEWER", "ANALYST", "MAINTAINER", "PROJECT_ADMIN"]


class DatasetCreate(ApiModel):
    project_id: str
    slug: str = Field(pattern=r"^[a-z0-9][a-z0-9-_]{1,126}$")
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    dataset_kind: Literal[
        "RAW", "INTERIM", "PROCESSED", "DISCOVERY_FEATURE", "INFERENCE_FEATURE"
    ]


class ObjectReference(ApiModel):
    backend: Literal["LOCAL", "S3", "AZURE_BLOB"] = "LOCAL"
    namespace: str | None = Field(
        default=None, validation_alias=AliasChoices("namespace", "bucket")
    )
    key: str = Field(validation_alias=AliasChoices("key", "object_key"))
    version: str | None = None
    media_type: str | None = None
    format: Literal["CSV", "PARQUET", "RDA", "RDS"]
    size_bytes: int | None = Field(default=None, ge=0)
    checksum: str


class DatasetTableCreate(ApiModel):
    logical_name: str = Field(min_length=1, max_length=255)
    object: ObjectReference
    source_entry_name: str | None = None
    partition_values: dict[str, Any] | None = None


class DatasetVersionCreate(ApiModel):
    source_type: Literal["UPLOAD", "OBJECT_REFERENCE", "ETL", "FEATURE_BUILD", "IMPORT"]
    source_metadata: dict[str, Any] = Field(default_factory=dict)
    tables: list[DatasetTableCreate] = Field(min_length=1)
    profile: bool = True


class DatasetRegistryImport(ApiModel):
    project_id: str
    slug: str
    name: str
    description: str | None = None
    dataset_kind: Literal["RAW", "INTERIM", "PROCESSED"] = "RAW"
    registry_yaml: str
    objects: dict[str, ObjectReference]
    profile: bool = True


class ConfigurationCreate(ApiModel):
    project_id: str
    configuration_type: Literal[
        "ETL_EXTRACT",
        "ETL_TRANSFORM",
        "ETL_LOAD",
        "DISCOVERY_ANALYSIS",
        "DISCOVERY_FEATURE",
        "INFERENCE_ANALYSIS",
        "INFERENCE_FEATURE",
        "FEATURE_SEMANTICS",
        "CAUSAL_DESIGN",
        "PIPELINE",
    ]
    slug: str
    name: str
    description: str | None = None


class ConfigurationVersionCreate(ApiModel):
    canonical_json: dict[str, Any] | None = None
    yaml_text: str | None = None
    schema_version: str = "1"

    @model_validator(mode="after")
    def exactly_one_document(self) -> "ConfigurationVersionCreate":
        if (self.canonical_json is None) == (self.yaml_text is None):
            raise ValueError("provide exactly one of canonical_json or yaml_text")
        return self


class ExperimentCreate(ApiModel):
    project_id: str
    slug: str
    title: str
    objective: str | None = None
    hypothesis: str | None = None
    notes: str | None = None
    source_repository: str | None = None
    source_commit: str | None = None
    notebook_reference: str | None = None
    tags: list[str] = Field(default_factory=list)


class PipelineStageCreate(ApiModel):
    stage_key: str
    stage_type: Literal["ETL", "DISCOVERY", "INFERENCE"]
    analysis_mode: Literal["EDGE_WEIGHT", "TREATMENT_EFFECT"] | None = None
    input_mode: Literal["CONFIGURED_FEATURE_BUILD", "ANALYSIS_READY"] | None = None
    runner_name: str | None = None
    enabled: bool = True
    depends_on: list[str] = Field(default_factory=list)
    dataset_inputs: dict[str, str] = Field(default_factory=dict)
    configuration_inputs: dict[str, str] = Field(default_factory=dict)
    artifact_inputs: dict[str, str] = Field(default_factory=dict)
    graph_inputs: dict[str, str] = Field(default_factory=dict)
    parameters: dict[str, Any] = Field(default_factory=dict)
    outputs: dict[str, str] = Field(default_factory=dict)

    @model_validator(mode="after")
    def valid_analysis_mode(self) -> "PipelineStageCreate":
        if self.stage_type == "INFERENCE" and self.analysis_mode is None:
            raise ValueError("INFERENCE requires analysis_mode")
        if self.stage_type != "INFERENCE" and self.analysis_mode is not None:
            raise ValueError("analysis_mode is only valid for INFERENCE")
        return self


class AnalysisDatasetBindingUpdate(ApiModel):
    analysis_unit_description: str = Field(min_length=1, max_length=2000)
    unit_identifier_column_id: str | None = None


class CausalGraphCreate(ApiModel):
    project_id: str
    slug: str = Field(pattern=r"^[a-z0-9][a-z0-9-_]{1,126}$")
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None


class CausalGraphVersionCreate(ApiModel):
    source_discovery_algorithm_result_id: str
    feature_semantics_version_id: str
    selection_note: str | None = None


class PipelineDefinitionCreate(ApiModel):
    project_id: str
    slug: str
    name: str
    description: str | None = None
    random_seed_default: int | None = None
    fail_fast: bool = True
    stages: list[PipelineStageCreate] = Field(min_length=1)
    publish: bool = True


class PipelineDefinitionVersionCreate(ApiModel):
    random_seed_default: int | None = None
    fail_fast: bool = True
    stages: list[PipelineStageCreate] = Field(min_length=1)
    publish: bool = True


class RunCreate(ApiModel):
    project_id: str
    run_kind: Literal["PIPELINE", "ETL", "DISCOVERY", "INFERENCE"] = "PIPELINE"
    execution_mode: Literal["DRY_RUN", "VALIDATE_ONLY", "RUN"] = "RUN"
    pipeline_definition_version_id: str | None = None
    experiment_id: str | None = None
    stages: list[PipelineStageCreate] | None = None
    random_seed: int | None = None
    priority: int = Field(default=0, ge=-100, le=100)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def plan_source(self) -> "RunCreate":
        if (self.pipeline_definition_version_id is None) == (self.stages is None):
            raise ValueError(
                "provide exactly one of pipeline_definition_version_id or stages"
            )
        return self


class FilterClause(ApiModel):
    column: str
    operator: Literal["eq", "ne", "lt", "lte", "gt", "gte", "in", "is_null", "not_null"]
    value: Any = None


class SamplingSpec(ApiModel):
    method: Literal["random", "head"] = "random"
    size: int = Field(default=5000, ge=1, le=50_000)
    seed: int = 42


class VisualizationQuerySpec(ApiModel):
    chart_type: Literal[
        "table", "bar", "line", "scatter", "pie", "histogram", "box"
    ] = "table"
    selected_columns: list[str] = Field(default_factory=list)
    filters: list[FilterClause] = Field(default_factory=list)
    group_by: list[str] = Field(default_factory=list, max_length=3)
    series_column: str | None = None
    aggregation_target: str | None = None
    aggregation: Literal["count", "distinct_count", "sum", "mean", "min", "max"] = (
        "count"
    )
    sort_by: str | None = None
    sort_direction: Literal["asc", "desc"] = "asc"
    limit: int = Field(default=1000, ge=1, le=10_000)
    bins: int = Field(default=20, ge=2, le=200)
    top_n: int = Field(default=20, ge=1, le=100)
    time_grain: Literal["hour", "day", "week", "month", "quarter", "year"] | None = None
    include_nulls: bool = False
    sampling: SamplingSpec | None = None


class VisualizationSpecificationCreate(ApiModel):
    project_id: str
    name: str
    description: str | None = None
    dataset_table_version_id: str | None = None
    logical_table_name: str | None = None
    specification: VisualizationQuerySpec


class VisualizationQueryCreate(ApiModel):
    specification: VisualizationQuerySpec
    force_async: bool = False


class ResourceResponse(ApiModel):
    id: str
    created_at: datetime | None = None


class ErrorDetail(ApiModel):
    code: str
    message: str
    request_id: str
    details: dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(ApiModel):
    error: ErrorDetail


__all__ = [
    name
    for name, value in globals().items()
    if isinstance(value, type) and issubclass(value, BaseModel)
]
