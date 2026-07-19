"""Metadata entities shared by application and relational persistence.

The canonical documents remain JSON/YAML artifacts.  These tables contain the
identity, lifecycle, lineage, and searchable projections described by the data
model definition.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    event,
    inspect,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def new_id() -> str:
    return str(uuid.uuid4())


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "app_user"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    identity_provider: Mapped[str] = mapped_column(String(64))
    external_subject: Mapped[str] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(320))
    display_name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    __table_args__ = (UniqueConstraint("identity_provider", "external_subject"),)


class Project(Base):
    __tablename__ = "project"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE")
    created_by: Mapped[str] = mapped_column(ForeignKey("app_user.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Role(Base):
    __tablename__ = "role"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    code: Mapped[str] = mapped_column(String(64), unique=True)
    name: Mapped[str] = mapped_column(String(255))
    system_managed: Mapped[bool] = mapped_column(Boolean, default=True)


class ProjectMember(Base):
    __tablename__ = "project_member"
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("app_user.id"), primary_key=True)
    role_id: Mapped[str] = mapped_column(ForeignKey("role.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )


class StoredObject(Base):
    __tablename__ = "stored_object"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    backend: Mapped[str] = mapped_column(String(32), default="LOCAL")
    bucket: Mapped[str | None] = mapped_column(String(255))
    object_key: Mapped[str] = mapped_column(Text)
    object_version: Mapped[str] = mapped_column(String(255), default="")
    media_type: Mapped[str | None] = mapped_column(String(255))
    format: Mapped[str | None] = mapped_column(String(32))
    size_bytes: Mapped[int | None] = mapped_column(BigInteger)
    checksum_algorithm: Mapped[str] = mapped_column(String(32), default="SHA256")
    checksum: Mapped[str] = mapped_column(String(255))
    encryption_metadata: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(32), default="AVAILABLE")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (
        UniqueConstraint("backend", "bucket", "object_key", "object_version"),
    )


class Dataset(Base):
    __tablename__ = "dataset"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    slug: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    dataset_kind: Mapped[str] = mapped_column(String(32))
    created_by: Mapped[str] = mapped_column(ForeignKey("app_user.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (UniqueConstraint("project_id", "slug"),)


class DatasetVersion(Base):
    __tablename__ = "dataset_version"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    dataset_id: Mapped[str] = mapped_column(ForeignKey("dataset.id"), index=True)
    version_number: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(32), default="REGISTERING")
    source_type: Mapped[str] = mapped_column(String(32))
    source_metadata: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    schema_hash: Mapped[str | None] = mapped_column(String(255))
    content_hash: Mapped[str | None] = mapped_column(String(255))
    table_count: Mapped[int] = mapped_column(Integer, default=0)
    origin_stage_run_id: Mapped[str | None] = mapped_column(
        ForeignKey("stage_run.id", use_alter=True)
    )
    created_by: Mapped[str] = mapped_column(ForeignKey("app_user.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    ready_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (UniqueConstraint("dataset_id", "version_number"),)


class DatasetTableVersion(Base):
    __tablename__ = "dataset_table_version"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    dataset_version_id: Mapped[str] = mapped_column(
        ForeignKey("dataset_version.id"), index=True
    )
    logical_name: Mapped[str] = mapped_column(String(255))
    stored_object_id: Mapped[str] = mapped_column(ForeignKey("stored_object.id"))
    ordinal: Mapped[int] = mapped_column(Integer)
    file_format: Mapped[str] = mapped_column(String(32))
    row_count: Mapped[int | None] = mapped_column(BigInteger)
    column_count: Mapped[int | None] = mapped_column(Integer)
    schema_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    schema_hash: Mapped[str | None] = mapped_column(String(255))
    content_hash: Mapped[str] = mapped_column(String(255))
    partition_values: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    source_entry_name: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    __table_args__ = (
        UniqueConstraint("dataset_version_id", "logical_name"),
        UniqueConstraint("dataset_version_id", "ordinal"),
    )


class DatasetColumn(Base):
    __tablename__ = "dataset_column"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    dataset_table_version_id: Mapped[str] = mapped_column(
        ForeignKey("dataset_table_version.id"), index=True
    )
    ordinal: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(255))
    physical_type: Mapped[str] = mapped_column(String(128))
    logical_type: Mapped[str | None] = mapped_column(String(128))
    nullable: Mapped[bool] = mapped_column(Boolean)
    description: Mapped[str | None] = mapped_column(Text)
    semantic_tags: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    __table_args__ = (
        UniqueConstraint("dataset_table_version_id", "name"),
        UniqueConstraint("dataset_table_version_id", "ordinal"),
    )


class AnalysisDatasetBinding(Base):
    """Declares the single primary table used by the analysis-ready path."""

    __tablename__ = "analysis_dataset_binding"
    dataset_version_id: Mapped[str] = mapped_column(
        ForeignKey("dataset_version.id"), primary_key=True
    )
    primary_table_version_id: Mapped[str] = mapped_column(
        ForeignKey("dataset_table_version.id"), unique=True
    )
    analysis_unit_description: Mapped[str] = mapped_column(Text)
    unit_identifier_column_id: Mapped[str | None] = mapped_column(
        ForeignKey("dataset_column.id")
    )
    readiness_status: Mapped[str] = mapped_column(String(32), default="UNKNOWN")
    schema_hash_snapshot: Mapped[str] = mapped_column(String(255))
    validation_summary_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_by: Mapped[str] = mapped_column(ForeignKey("app_user.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class DatasetColumnPolicy(Base):
    __tablename__ = "dataset_column_policy"
    dataset_column_id: Mapped[str] = mapped_column(
        ForeignKey("dataset_column.id"), primary_key=True
    )
    classification: Mapped[str] = mapped_column(String(32), default="INTERNAL")
    preview_allowed: Mapped[bool] = mapped_column(Boolean, default=True)
    analysis_allowed: Mapped[bool] = mapped_column(Boolean, default=True)
    download_allowed: Mapped[bool] = mapped_column(Boolean, default=True)
    mask_rule: Mapped[str | None] = mapped_column(String(64))
    minimum_group_count: Mapped[int | None] = mapped_column(Integer)
    updated_by: Mapped[str] = mapped_column(ForeignKey("app_user.id"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )


class DataProfile(Base):
    __tablename__ = "data_profile"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    dataset_table_version_id: Mapped[str] = mapped_column(
        ForeignKey("dataset_table_version.id"), index=True
    )
    status: Mapped[str] = mapped_column(String(32), default="PENDING")
    profiler_name: Mapped[str] = mapped_column(String(128), default="causal-atelier")
    profiler_version: Mapped[str] = mapped_column(String(64), default="1")
    sampled: Mapped[bool] = mapped_column(Boolean, default=False)
    sample_size: Mapped[int | None] = mapped_column(BigInteger)
    summary_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    artifact_id: Mapped[str | None] = mapped_column(
        ForeignKey("artifact.id", use_alter=True)
    )
    error_summary: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )


class ColumnProfile(Base):
    __tablename__ = "column_profile"
    data_profile_id: Mapped[str] = mapped_column(
        ForeignKey("data_profile.id"), primary_key=True
    )
    dataset_column_id: Mapped[str] = mapped_column(
        ForeignKey("dataset_column.id"), primary_key=True
    )
    null_count: Mapped[int | None] = mapped_column(BigInteger)
    distinct_count: Mapped[int | None] = mapped_column(BigInteger)
    min_value: Mapped[str | None] = mapped_column(Text)
    max_value: Mapped[str | None] = mapped_column(Text)
    statistics_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


class Configuration(Base):
    __tablename__ = "configuration"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    configuration_type: Mapped[str] = mapped_column(String(64))
    slug: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    created_by: Mapped[str] = mapped_column(ForeignKey("app_user.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (UniqueConstraint("project_id", "configuration_type", "slug"),)


class ConfigurationVersion(Base):
    __tablename__ = "configuration_version"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    configuration_id: Mapped[str] = mapped_column(
        ForeignKey("configuration.id"), index=True
    )
    version_number: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(32), default="DRAFT")
    schema_version: Mapped[str] = mapped_column(String(64), default="1")
    canonical_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    original_format: Mapped[str] = mapped_column(String(16), default="YAML")
    original_text: Mapped[str | None] = mapped_column(Text)
    content_hash: Mapped[str] = mapped_column(String(255))
    validation_status: Mapped[str] = mapped_column(String(32), default="UNKNOWN")
    validation_summary: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    supersedes_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("configuration_version.id")
    )
    created_by: Mapped[str] = mapped_column(ForeignKey("app_user.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    published_by: Mapped[str | None] = mapped_column(ForeignKey("app_user.id"))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    lock_version: Mapped[int] = mapped_column(Integer, default=1)
    __table_args__ = (
        UniqueConstraint("configuration_id", "version_number"),
        UniqueConstraint("configuration_id", "content_hash"),
    )


class ConfigurationDependency(Base):
    __tablename__ = "configuration_dependency"
    source_configuration_version_id: Mapped[str] = mapped_column(
        ForeignKey("configuration_version.id"), primary_key=True
    )
    dependency_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    target_configuration_version_id: Mapped[str] = mapped_column(
        ForeignKey("configuration_version.id")
    )
    dependency_type: Mapped[str] = mapped_column(String(32))


class FeatureSemanticsProjection(Base):
    __tablename__ = "feature_semantics_projection"
    configuration_version_id: Mapped[str] = mapped_column(
        ForeignKey("configuration_version.id"), primary_key=True
    )
    default_unit_id: Mapped[str | None] = mapped_column(String(255))
    feature_count: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )


class FeatureSemanticsDatasetBinding(Base):
    __tablename__ = "feature_semantics_dataset_binding"
    configuration_version_id: Mapped[str] = mapped_column(
        ForeignKey("configuration_version.id"), primary_key=True
    )
    dataset_version_id: Mapped[str] = mapped_column(
        ForeignKey("dataset_version.id"), index=True
    )
    dataset_table_version_id: Mapped[str] = mapped_column(
        ForeignKey("dataset_table_version.id")
    )
    dataset_schema_hash_snapshot: Mapped[str] = mapped_column(String(255))
    binding_status: Mapped[str] = mapped_column(String(32), default="VALID")
    validation_summary_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class FeatureSemanticItem(Base):
    __tablename__ = "feature_semantic_item"
    feature_semantics_version_id: Mapped[str] = mapped_column(
        ForeignKey("configuration_version.id"), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(255), primary_key=True)
    role: Mapped[str] = mapped_column(String(32))
    source_table: Mapped[str] = mapped_column(String(255))
    source_column: Mapped[str | None] = mapped_column(String(255))
    unit_id: Mapped[str] = mapped_column(String(255))
    aggregation: Mapped[str | None] = mapped_column(String(64))
    transform: Mapped[str | None] = mapped_column(String(128))
    dtype: Mapped[str | None] = mapped_column(String(128))
    dataset_column_id: Mapped[str | None] = mapped_column(
        ForeignKey("dataset_column.id")
    )
    categorical: Mapped[bool] = mapped_column(Boolean, default=False)
    allowed_for_discovery: Mapped[bool] = mapped_column(Boolean, default=True)
    allowed_for_adjustment: Mapped[bool] = mapped_column(Boolean, default=False)
    post_treatment: Mapped[bool] = mapped_column(Boolean, default=False)
    time_metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    description: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


class CausalDesignProjection(Base):
    __tablename__ = "causal_design_projection"
    configuration_version_id: Mapped[str] = mapped_column(
        ForeignKey("configuration_version.id"), primary_key=True
    )
    feature_semantics_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("configuration_version.id")
    )
    dataset_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("dataset_version.id")
    )
    causal_graph_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("causal_graph_version.id")
    )
    estimand: Mapped[str] = mapped_column(String(16))
    treatment_name: Mapped[str] = mapped_column(String(255))
    treatment_time: Mapped[str | None] = mapped_column(String(255))
    treatment_levels: Mapped[list[Any]] = mapped_column(JSON, default=list)
    outcome_name: Mapped[str] = mapped_column(String(255))
    outcome_window: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    unit: Mapped[str] = mapped_column(String(255))
    time_zero: Mapped[str | None] = mapped_column(String(255))
    adjustment_set_name: Mapped[str | None] = mapped_column(String(255))
    target_population: Mapped[str | None] = mapped_column(Text)
    adjustment_strategy: Mapped[str | None] = mapped_column(String(64))
    adjustment_set_json: Mapped[list[Any]] = mapped_column(JSON, default=list)
    analyst_note: Mapped[str | None] = mapped_column(Text)


class CausalAssumption(Base):
    __tablename__ = "causal_assumption"
    causal_design_version_id: Mapped[str] = mapped_column(
        ForeignKey("configuration_version.id"), primary_key=True
    )
    assumption_code: Mapped[str] = mapped_column(String(128), primary_key=True)
    statement: Mapped[str | None] = mapped_column(Text)
    declaration_status: Mapped[str] = mapped_column(String(32))
    evidence: Mapped[str | None] = mapped_column(Text)
    ordinal: Mapped[int] = mapped_column(Integer)


class Experiment(Base):
    __tablename__ = "experiment"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    slug: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))
    objective: Mapped[str | None] = mapped_column(Text)
    hypothesis: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    source_repository: Mapped[str | None] = mapped_column(Text)
    source_commit: Mapped[str | None] = mapped_column(String(128))
    notebook_reference: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_by: Mapped[str] = mapped_column(ForeignKey("app_user.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    archived_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (UniqueConstraint("project_id", "slug"),)


class PipelineDefinition(Base):
    __tablename__ = "pipeline_definition"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    slug: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    created_by: Mapped[str] = mapped_column(ForeignKey("app_user.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (UniqueConstraint("project_id", "slug"),)


class PipelineDefinitionVersion(Base):
    __tablename__ = "pipeline_definition_version"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    pipeline_definition_id: Mapped[str] = mapped_column(
        ForeignKey("pipeline_definition.id"), index=True
    )
    version_number: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(32), default="DRAFT")
    random_seed_default: Mapped[int | None] = mapped_column(BigInteger)
    fail_fast: Mapped[bool] = mapped_column(Boolean, default=True)
    canonical_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    content_hash: Mapped[str] = mapped_column(String(255))
    created_by: Mapped[str] = mapped_column(ForeignKey("app_user.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (
        UniqueConstraint("pipeline_definition_id", "version_number"),
        UniqueConstraint("pipeline_definition_id", "content_hash"),
    )


class PipelineStageDefinition(Base):
    __tablename__ = "pipeline_stage_definition"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    pipeline_definition_version_id: Mapped[str] = mapped_column(
        ForeignKey("pipeline_definition_version.id"), index=True
    )
    stage_key: Mapped[str] = mapped_column(String(255))
    stage_type: Mapped[str] = mapped_column(String(32))
    analysis_mode: Mapped[str | None] = mapped_column(String(32))
    input_mode: Mapped[str | None] = mapped_column(String(32))
    ordinal: Mapped[int] = mapped_column(Integer)
    enabled_by_default: Mapped[bool] = mapped_column(Boolean, default=True)
    runner_name: Mapped[str] = mapped_column(String(128))
    timeout_seconds: Mapped[int | None] = mapped_column(Integer)
    retry_policy_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    resource_requirements_json: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict
    )
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    __table_args__ = (
        UniqueConstraint("pipeline_definition_version_id", "stage_key"),
        UniqueConstraint("pipeline_definition_version_id", "ordinal"),
    )


class PipelineStageDependency(Base):
    __tablename__ = "pipeline_stage_dependency"
    stage_definition_id: Mapped[str] = mapped_column(
        ForeignKey("pipeline_stage_definition.id"), primary_key=True
    )
    depends_on_stage_definition_id: Mapped[str] = mapped_column(
        ForeignKey("pipeline_stage_definition.id"), primary_key=True
    )


class PipelineStageConfigBinding(Base):
    __tablename__ = "pipeline_stage_config_binding"
    stage_definition_id: Mapped[str] = mapped_column(
        ForeignKey("pipeline_stage_definition.id"), primary_key=True
    )
    binding_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    configuration_version_id: Mapped[str] = mapped_column(
        ForeignKey("configuration_version.id")
    )
    required: Mapped[bool] = mapped_column(Boolean, default=True)


class PipelineStageOutputDeclaration(Base):
    __tablename__ = "pipeline_stage_output_declaration"
    stage_definition_id: Mapped[str] = mapped_column(
        ForeignKey("pipeline_stage_definition.id"), primary_key=True
    )
    output_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    artifact_kind: Mapped[str] = mapped_column(String(64))
    required: Mapped[bool] = mapped_column(Boolean, default=True)
    register_as_dataset: Mapped[bool] = mapped_column(Boolean, default=False)


class Run(Base):
    __tablename__ = "run"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    experiment_id: Mapped[str | None] = mapped_column(ForeignKey("experiment.id"))
    pipeline_definition_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("pipeline_definition_version.id")
    )
    run_kind: Mapped[str] = mapped_column(String(32))
    execution_mode: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32), default="SUBMITTED")
    submitted_by: Mapped[str] = mapped_column(ForeignKey("app_user.id"))
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    queued_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cancel_requested_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    idempotency_key: Mapped[str | None] = mapped_column(String(255))
    request_hash: Mapped[str] = mapped_column(String(255))
    random_seed: Mapped[int | None] = mapped_column(BigInteger)
    code_commit: Mapped[str | None] = mapped_column(String(128))
    package_version: Mapped[str | None] = mapped_column(String(64))
    dependency_lock_hash: Mapped[str | None] = mapped_column(String(255))
    container_image_digest: Mapped[str | None] = mapped_column(String(255))
    priority: Mapped[int] = mapped_column(Integer, default=0)
    retry_of_run_id: Mapped[str | None] = mapped_column(ForeignKey("run.id"))
    error_code: Mapped[str | None] = mapped_column(String(128))
    error_summary: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    __table_args__ = (
        Index(
            "uq_run_project_idempotency",
            "project_id",
            "idempotency_key",
            unique=True,
            postgresql_where=(idempotency_key.is_not(None)),
            sqlite_where=(idempotency_key.is_not(None)),
        ),
        Index(
            "idx_run_project_status_submitted", "project_id", "status", "submitted_at"
        ),
    )


class ExecutionPlanRecord(Base):
    __tablename__ = "execution_plan"
    run_id: Mapped[str] = mapped_column(ForeignKey("run.id"), primary_key=True)
    schema_version: Mapped[str] = mapped_column(String(64), default="2")
    canonical_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    plan_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )


class StageRun(Base):
    __tablename__ = "stage_run"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    run_id: Mapped[str] = mapped_column(ForeignKey("run.id"), index=True)
    stage_key: Mapped[str] = mapped_column(String(255))
    stage_type: Mapped[str] = mapped_column(String(32))
    analysis_mode: Mapped[str | None] = mapped_column(String(32))
    input_mode: Mapped[str] = mapped_column(
        String(32), default="CONFIGURED_FEATURE_BUILD", server_default="CONFIGURED_FEATURE_BUILD"
    )
    ordinal: Mapped[int] = mapped_column(Integer)
    runner_name: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(32), default="SUBMITTED")
    current_attempt_number: Mapped[int] = mapped_column(Integer, default=0)
    selected_attempt_id: Mapped[str | None] = mapped_column(String(36))
    cache_hit: Mapped[bool] = mapped_column(Boolean, default=False)
    reused_from_stage_run_id: Mapped[str | None] = mapped_column(
        ForeignKey("stage_run.id")
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    error_code: Mapped[str | None] = mapped_column(String(128))
    error_summary: Mapped[str | None] = mapped_column(Text)
    __table_args__ = (
        UniqueConstraint("run_id", "stage_key"),
        UniqueConstraint("run_id", "ordinal"),
    )


class StageRunDependency(Base):
    __tablename__ = "stage_run_dependency"
    stage_run_id: Mapped[str] = mapped_column(
        ForeignKey("stage_run.id"), primary_key=True
    )
    depends_on_stage_run_id: Mapped[str] = mapped_column(
        ForeignKey("stage_run.id"), primary_key=True
    )


class StageAttempt(Base):
    __tablename__ = "stage_attempt"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    stage_run_id: Mapped[str] = mapped_column(ForeignKey("stage_run.id"), index=True)
    attempt_number: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(32), default="CREATED")
    queue_message_id: Mapped[str | None] = mapped_column(String(255))
    worker_id: Mapped[str | None] = mapped_column(String(255))
    workspace_ref: Mapped[str | None] = mapped_column(Text)
    queued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    leased_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    lease_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    heartbeat_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    exit_code: Mapped[int | None] = mapped_column(Integer)
    error_class: Mapped[str | None] = mapped_column(String(255))
    error_code: Mapped[str | None] = mapped_column(String(128))
    error_message: Mapped[str | None] = mapped_column(Text)
    error_detail_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    runtime_metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    resource_usage_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    __table_args__ = (UniqueConstraint("stage_run_id", "attempt_number"),)


class StageRunDatasetInput(Base):
    __tablename__ = "stage_run_dataset_input"
    stage_run_id: Mapped[str] = mapped_column(
        ForeignKey("stage_run.id"), primary_key=True
    )
    input_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    dataset_version_id: Mapped[str] = mapped_column(ForeignKey("dataset_version.id"))


class StageRunConfigInput(Base):
    __tablename__ = "stage_run_config_input"
    stage_run_id: Mapped[str] = mapped_column(
        ForeignKey("stage_run.id"), primary_key=True
    )
    input_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    configuration_version_id: Mapped[str] = mapped_column(
        ForeignKey("configuration_version.id")
    )
    content_hash_snapshot: Mapped[str] = mapped_column(String(255))


class StageRunArtifactInput(Base):
    __tablename__ = "stage_run_artifact_input"
    stage_run_id: Mapped[str] = mapped_column(
        ForeignKey("stage_run.id"), primary_key=True
    )
    input_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    artifact_id: Mapped[str] = mapped_column(ForeignKey("artifact.id"))


class StageRunInputPreparation(Base):
    __tablename__ = "stage_run_input_preparation"
    stage_run_id: Mapped[str] = mapped_column(
        ForeignKey("stage_run.id"), primary_key=True
    )
    input_mode: Mapped[str] = mapped_column(String(32))
    input_dataset_version_id: Mapped[str] = mapped_column(
        ForeignKey("dataset_version.id")
    )
    input_table_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("dataset_table_version.id")
    )
    input_schema_hash: Mapped[str] = mapped_column(String(255))
    feature_semantics_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("configuration_version.id")
    )
    requested_columns_json: Mapped[list[Any]] = mapped_column(JSON, default=list)
    conditioning_spec_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    configured_feature_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("configuration_version.id")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )


class StageAttemptInputPreparation(Base):
    __tablename__ = "stage_attempt_input_preparation"
    stage_attempt_id: Mapped[str] = mapped_column(
        ForeignKey("stage_attempt.id"), primary_key=True
    )
    stage_run_id: Mapped[str] = mapped_column(ForeignKey("stage_run.id"), index=True)
    input_mode: Mapped[str] = mapped_column(String(32))
    actual_selected_columns_json: Mapped[list[Any]] = mapped_column(JSON, default=list)
    excluded_columns_json: Mapped[list[Any]] = mapped_column(JSON, default=list)
    resolved_conditioning_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    feature_frame_artifact_id: Mapped[str | None] = mapped_column(
        ForeignKey("artifact.id")
    )
    resolved_preparation_artifact_id: Mapped[str | None] = mapped_column(
        ForeignKey("artifact.id")
    )
    status: Mapped[str] = mapped_column(String(32), default="RUNNING")
    error_summary: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class StageRunParameter(Base):
    __tablename__ = "stage_run_parameter"
    stage_run_id: Mapped[str] = mapped_column(
        ForeignKey("stage_run.id"), primary_key=True
    )
    parameter_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    value_json: Mapped[Any] = mapped_column(JSON)
    source: Mapped[str] = mapped_column(String(32))


class Artifact(Base):
    __tablename__ = "artifact"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    artifact_kind: Mapped[str] = mapped_column(String(64))
    logical_name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), default="PENDING")
    stored_object_id: Mapped[str | None] = mapped_column(ForeignKey("stored_object.id"))
    produced_by_attempt_id: Mapped[str | None] = mapped_column(
        ForeignKey("stage_attempt.id")
    )
    media_type: Mapped[str | None] = mapped_column(String(255))
    schema_name: Mapped[str | None] = mapped_column(String(128))
    schema_version: Mapped[str | None] = mapped_column(String(64))
    content_hash: Mapped[str] = mapped_column(String(255))
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (
        Index(
            "idx_artifact_project_kind_created",
            "project_id",
            "artifact_kind",
            "created_at",
        ),
    )


class StageRunArtifactOutput(Base):
    __tablename__ = "stage_run_artifact_output"
    stage_run_id: Mapped[str] = mapped_column(
        ForeignKey("stage_run.id"), primary_key=True
    )
    output_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    artifact_id: Mapped[str] = mapped_column(ForeignKey("artifact.id"), unique=True)
    required: Mapped[bool] = mapped_column(Boolean, default=True)


class ArtifactLineage(Base):
    __tablename__ = "artifact_lineage"
    downstream_artifact_id: Mapped[str] = mapped_column(
        ForeignKey("artifact.id"), primary_key=True
    )
    upstream_artifact_id: Mapped[str] = mapped_column(
        ForeignKey("artifact.id"), primary_key=True
    )
    relationship_type: Mapped[str] = mapped_column(String(32), primary_key=True)


class ManifestRecord(Base):
    __tablename__ = "manifest_record"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    run_id: Mapped[str] = mapped_column(ForeignKey("run.id"), index=True)
    stage_run_id: Mapped[str | None] = mapped_column(ForeignKey("stage_run.id"))
    scope: Mapped[str] = mapped_column(String(16))
    artifact_id: Mapped[str] = mapped_column(ForeignKey("artifact.id"))
    schema_version: Mapped[str] = mapped_column(String(64))
    content_hash: Mapped[str] = mapped_column(String(255))
    projection_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )


class ValidationRun(Base):
    __tablename__ = "validation_run"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    run_id: Mapped[str] = mapped_column(ForeignKey("run.id"), index=True)
    stage_run_id: Mapped[str | None] = mapped_column(ForeignKey("stage_run.id"))
    validator_name: Mapped[str] = mapped_column(String(128))
    validator_version: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(16))
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    finished_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )


class ValidationIssueRecord(Base):
    __tablename__ = "validation_issue"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    validation_run_id: Mapped[str] = mapped_column(
        ForeignKey("validation_run.id"), index=True
    )
    severity: Mapped[str] = mapped_column(String(16))
    code: Mapped[str] = mapped_column(String(128))
    message: Mapped[str] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(Text)
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    ordinal: Mapped[int] = mapped_column(Integer)


class RunEvent(Base):
    __tablename__ = "run_event"
    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    run_id: Mapped[str] = mapped_column(ForeignKey("run.id"), index=True)
    stage_run_id: Mapped[str | None] = mapped_column(ForeignKey("stage_run.id"))
    stage_attempt_id: Mapped[str | None] = mapped_column(ForeignKey("stage_attempt.id"))
    sequence_number: Mapped[int] = mapped_column(BigInteger)
    event_type: Mapped[str] = mapped_column(String(128))
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    __table_args__ = (UniqueConstraint("run_id", "sequence_number"),)


class OutboxEvent(Base):
    __tablename__ = "outbox_event"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    aggregate_type: Mapped[str] = mapped_column(String(64))
    aggregate_id: Mapped[str] = mapped_column(String(36), index=True)
    event_type: Mapped[str] = mapped_column(String(128), index=True)
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), index=True
    )
    claimed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), index=True
    )
    claimed_by: Mapped[str | None] = mapped_column(String(255))
    publish_attempts: Mapped[int] = mapped_column(Integer, default=0)
    last_error: Mapped[str | None] = mapped_column(Text)


class AuditEvent(Base):
    __tablename__ = "audit_event"
    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    project_id: Mapped[str | None] = mapped_column(ForeignKey("project.id"), index=True)
    actor_user_id: Mapped[str | None] = mapped_column(ForeignKey("app_user.id"))
    action: Mapped[str] = mapped_column(String(128))
    resource_type: Mapped[str] = mapped_column(String(64))
    resource_id: Mapped[str | None] = mapped_column(String(36))
    request_id: Mapped[str | None] = mapped_column(String(255))
    before_json: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    after_json: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    source_ip: Mapped[str | None] = mapped_column(String(64))
    user_agent: Mapped[str | None] = mapped_column(Text)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )


class VisualizationSpecification(Base):
    __tablename__ = "visualization_specification"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    dataset_table_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("dataset_table_version.id")
    )
    logical_table_name: Mapped[str | None] = mapped_column(String(255))
    specification_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    specification_hash: Mapped[str] = mapped_column(String(255))
    created_by: Mapped[str] = mapped_column(ForeignKey("app_user.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )


class VisualizationQuery(Base):
    __tablename__ = "visualization_query"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    dataset_table_version_id: Mapped[str] = mapped_column(
        ForeignKey("dataset_table_version.id")
    )
    visualization_specification_id: Mapped[str | None] = mapped_column(
        ForeignKey("visualization_specification.id")
    )
    status: Mapped[str] = mapped_column(String(32), default="SUBMITTED")
    query_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    query_hash: Mapped[str] = mapped_column(String(255), index=True)
    query_engine_version: Mapped[str] = mapped_column(String(64), default="pyarrow-1")
    result_json: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    result_artifact_id: Mapped[str | None] = mapped_column(ForeignKey("artifact.id"))
    cache_hit: Mapped[bool] = mapped_column(Boolean, default=False)
    sampled: Mapped[bool] = mapped_column(Boolean, default=False)
    sample_size: Mapped[int | None] = mapped_column(BigInteger)
    sampling_method: Mapped[str | None] = mapped_column(String(64))
    random_seed: Mapped[int | None] = mapped_column(BigInteger)
    scanned_bytes: Mapped[int | None] = mapped_column(BigInteger)
    result_row_count: Mapped[int | None] = mapped_column(BigInteger)
    duration_ms: Mapped[int | None] = mapped_column(BigInteger)
    error_summary: Mapped[str | None] = mapped_column(Text)
    created_by: Mapped[str] = mapped_column(ForeignKey("app_user.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (
        Index(
            "idx_visualization_query_cache",
            "dataset_table_version_id",
            "query_hash",
            "query_engine_version",
            "status",
        ),
    )


class DiscoveryResult(Base):
    __tablename__ = "discovery_result"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    stage_run_id: Mapped[str] = mapped_column(ForeignKey("stage_run.id"), unique=True)
    dataset_version_id: Mapped[str] = mapped_column(ForeignKey("dataset_version.id"))
    discovery_analysis_version_id: Mapped[str] = mapped_column(
        ForeignKey("configuration_version.id")
    )
    discovery_feature_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("configuration_version.id")
    )
    input_mode: Mapped[str] = mapped_column(
        String(32), default="CONFIGURED_FEATURE_BUILD", server_default="CONFIGURED_FEATURE_BUILD"
    )
    feature_semantics_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("configuration_version.id")
    )
    input_preparation_attempt_id: Mapped[str | None] = mapped_column(
        ForeignKey("stage_attempt_input_preparation.stage_attempt_id")
    )
    resolved_semantics_artifact_id: Mapped[str | None] = mapped_column(
        ForeignKey("artifact.id")
    )
    algorithm_count: Mapped[int] = mapped_column(Integer)
    node_count: Mapped[int | None] = mapped_column(Integer)
    edge_count: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(32))
    summary_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )


class DiscoveryAlgorithmResult(Base):
    __tablename__ = "discovery_algorithm_result"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    discovery_result_id: Mapped[str] = mapped_column(
        ForeignKey("discovery_result.id"), index=True
    )
    algorithm: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32))
    message: Mapped[str | None] = mapped_column(Text)
    edge_artifact_id: Mapped[str | None] = mapped_column(ForeignKey("artifact.id"))
    graph_artifact_id: Mapped[str | None] = mapped_column(ForeignKey("artifact.id"))
    diagnostic_artifact_id: Mapped[str | None] = mapped_column(
        ForeignKey("artifact.id")
    )
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    __table_args__ = (UniqueConstraint("discovery_result_id", "algorithm"),)


class DiscoveryEdge(Base):
    __tablename__ = "discovery_edge"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    discovery_algorithm_result_id: Mapped[str] = mapped_column(
        ForeignKey("discovery_algorithm_result.id"), index=True
    )
    source: Mapped[str] = mapped_column(String(255))
    target: Mapped[str] = mapped_column(String(255))
    edge_type: Mapped[str | None] = mapped_column(String(64))
    orientation: Mapped[str | None] = mapped_column(String(64))
    score: Mapped[float | None] = mapped_column(Float)
    stability: Mapped[float | None] = mapped_column(Float)
    selected: Mapped[bool] = mapped_column(Boolean, default=True)
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


class CausalGraph(Base):
    __tablename__ = "causal_graph"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    slug: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    created_by: Mapped[str] = mapped_column(ForeignKey("app_user.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (UniqueConstraint("project_id", "slug"),)


class CausalGraphVersion(Base):
    __tablename__ = "causal_graph_version"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    causal_graph_id: Mapped[str] = mapped_column(ForeignKey("causal_graph.id"), index=True)
    version_number: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(32), default="DRAFT")
    source_discovery_algorithm_result_id: Mapped[str] = mapped_column(
        ForeignKey("discovery_algorithm_result.id")
    )
    dataset_version_id: Mapped[str] = mapped_column(ForeignKey("dataset_version.id"))
    feature_semantics_version_id: Mapped[str] = mapped_column(
        ForeignKey("configuration_version.id")
    )
    algorithm: Mapped[str] = mapped_column(String(64))
    algorithm_parameter_hash: Mapped[str | None] = mapped_column(String(255))
    node_count: Mapped[int] = mapped_column(Integer)
    edge_count: Mapped[int] = mapped_column(Integer)
    canonical_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    content_hash: Mapped[str] = mapped_column(String(255))
    graph_artifact_id: Mapped[str] = mapped_column(ForeignKey("artifact.id"))
    selection_note: Mapped[str | None] = mapped_column(Text)
    created_by: Mapped[str] = mapped_column(ForeignKey("app_user.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    published_by: Mapped[str | None] = mapped_column(ForeignKey("app_user.id"))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    supersedes_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("causal_graph_version.id")
    )
    __table_args__ = (
        UniqueConstraint("causal_graph_id", "version_number"),
        UniqueConstraint("causal_graph_id", "content_hash"),
        CheckConstraint("version_number >= 1", name="ck_graph_version_number"),
        CheckConstraint("node_count >= 0", name="ck_graph_node_count"),
        CheckConstraint("edge_count >= 0", name="ck_graph_edge_count"),
    )


class CausalGraphNode(Base):
    __tablename__ = "causal_graph_node"
    causal_graph_version_id: Mapped[str] = mapped_column(
        ForeignKey("causal_graph_version.id"), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(255), primary_key=True)
    ordinal: Mapped[int] = mapped_column(Integer)
    role_snapshot: Mapped[str | None] = mapped_column(String(32))
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    __table_args__ = (UniqueConstraint("causal_graph_version_id", "ordinal"),)


class CausalGraphEdge(Base):
    __tablename__ = "causal_graph_edge"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    causal_graph_version_id: Mapped[str] = mapped_column(
        ForeignKey("causal_graph_version.id"), index=True
    )
    node_a: Mapped[str] = mapped_column(String(255))
    node_b: Mapped[str] = mapped_column(String(255))
    endpoint_at_a: Mapped[str] = mapped_column(String(16))
    endpoint_at_b: Mapped[str] = mapped_column(String(16))
    score: Mapped[float | None] = mapped_column(Float)
    stability: Mapped[float | None] = mapped_column(Float)
    source_discovery_edge_id: Mapped[str | None] = mapped_column(
        ForeignKey("discovery_edge.id")
    )
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    __table_args__ = (
        UniqueConstraint("causal_graph_version_id", "node_a", "node_b"),
        CheckConstraint("node_a < node_b", name="ck_graph_edge_node_order"),
        CheckConstraint(
            "endpoint_at_a IN ('TAIL', 'ARROW', 'CIRCLE')",
            name="ck_graph_endpoint_a",
        ),
        CheckConstraint(
            "endpoint_at_b IN ('TAIL', 'ARROW', 'CIRCLE')",
            name="ck_graph_endpoint_b",
        ),
    )


class StageRunGraphInput(Base):
    __tablename__ = "stage_run_graph_input"
    stage_run_id: Mapped[str] = mapped_column(
        ForeignKey("stage_run.id"), primary_key=True
    )
    input_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    causal_graph_version_id: Mapped[str] = mapped_column(
        ForeignKey("causal_graph_version.id")
    )
    content_hash_snapshot: Mapped[str] = mapped_column(String(255))
    source: Mapped[str] = mapped_column(String(32), default="API_OVERRIDE")


class EdgeWeightResult(Base):
    __tablename__ = "edge_weight_result"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    stage_run_id: Mapped[str] = mapped_column(ForeignKey("stage_run.id"), unique=True)
    discovery_result_id: Mapped[str | None] = mapped_column(
        ForeignKey("discovery_result.id")
    )
    dataset_version_id: Mapped[str] = mapped_column(ForeignKey("dataset_version.id"))
    inference_analysis_version_id: Mapped[str] = mapped_column(
        ForeignKey("configuration_version.id")
    )
    inference_feature_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("configuration_version.id")
    )
    input_mode: Mapped[str] = mapped_column(
        String(32), default="CONFIGURED_FEATURE_BUILD", server_default="CONFIGURED_FEATURE_BUILD"
    )
    feature_semantics_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("configuration_version.id")
    )
    causal_graph_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("causal_graph_version.id"), index=True
    )
    input_preparation_attempt_id: Mapped[str | None] = mapped_column(
        ForeignKey("stage_attempt_input_preparation.stage_attempt_id")
    )
    result_artifact_id: Mapped[str] = mapped_column(ForeignKey("artifact.id"))
    report_artifact_id: Mapped[str | None] = mapped_column(ForeignKey("artifact.id"))
    status: Mapped[str] = mapped_column(String(32))
    summary_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )


class EdgeWeightEstimate(Base):
    __tablename__ = "edge_weight_estimate"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    edge_weight_result_id: Mapped[str] = mapped_column(
        ForeignKey("edge_weight_result.id"), index=True
    )
    algorithm: Mapped[str] = mapped_column(String(64))
    source: Mapped[str] = mapped_column(String(255))
    target: Mapped[str] = mapped_column(String(255))
    coefficient: Mapped[float | None] = mapped_column(Float)
    standard_error: Mapped[float | None] = mapped_column(Float)
    statistic: Mapped[float | None] = mapped_column(Float)
    p_value: Mapped[float | None] = mapped_column(Float)
    adjusted_p_value: Mapped[float | None] = mapped_column(Float)
    ci_lower: Mapped[float | None] = mapped_column(Float)
    ci_upper: Mapped[float | None] = mapped_column(Float)
    sample_count: Mapped[int | None] = mapped_column(BigInteger)
    robust_se: Mapped[str | None] = mapped_column(String(16))
    status: Mapped[str] = mapped_column(String(32))
    warning: Mapped[str | None] = mapped_column(Text)
    interpretation_level: Mapped[str] = mapped_column(
        String(64), default="EXPLORATORY_EDGE_COEFFICIENT"
    )
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


class TreatmentEffectResult(Base):
    __tablename__ = "treatment_effect_result"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    stage_run_id: Mapped[str] = mapped_column(ForeignKey("stage_run.id"), unique=True)
    dataset_version_id: Mapped[str] = mapped_column(ForeignKey("dataset_version.id"))
    inference_analysis_version_id: Mapped[str] = mapped_column(
        ForeignKey("configuration_version.id")
    )
    inference_feature_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("configuration_version.id")
    )
    feature_semantics_version_id: Mapped[str] = mapped_column(
        ForeignKey("configuration_version.id")
    )
    causal_design_version_id: Mapped[str] = mapped_column(
        ForeignKey("configuration_version.id")
    )
    discovery_result_id: Mapped[str | None] = mapped_column(
        ForeignKey("discovery_result.id")
    )
    input_mode: Mapped[str] = mapped_column(
        String(32), default="CONFIGURED_FEATURE_BUILD", server_default="CONFIGURED_FEATURE_BUILD"
    )
    causal_graph_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("causal_graph_version.id"), index=True
    )
    input_preparation_attempt_id: Mapped[str | None] = mapped_column(
        ForeignKey("stage_attempt_input_preparation.stage_attempt_id")
    )
    treatment_name: Mapped[str] = mapped_column(String(255))
    outcome_name: Mapped[str] = mapped_column(String(255))
    estimand: Mapped[str] = mapped_column(String(16))
    adjustment_strategy: Mapped[str] = mapped_column(String(64))
    result_artifact_id: Mapped[str] = mapped_column(ForeignKey("artifact.id"))
    report_artifact_id: Mapped[str | None] = mapped_column(ForeignKey("artifact.id"))
    diagnostic_status: Mapped[str] = mapped_column(String(32))
    summary_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )


class TreatmentEffectEstimate(Base):
    __tablename__ = "treatment_effect_estimate"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    treatment_effect_result_id: Mapped[str] = mapped_column(
        ForeignKey("treatment_effect_result.id"), index=True
    )
    method: Mapped[str] = mapped_column(String(64))
    estimand: Mapped[str] = mapped_column(String(16))
    estimate: Mapped[float | None] = mapped_column(Float)
    standard_error: Mapped[float | None] = mapped_column(Float)
    ci_lower: Mapped[float | None] = mapped_column(Float)
    ci_upper: Mapped[float | None] = mapped_column(Float)
    p_value: Mapped[float | None] = mapped_column(Float)
    adjusted_p_value: Mapped[float | None] = mapped_column(Float)
    sample_count: Mapped[int | None] = mapped_column(BigInteger)
    effective_sample_size: Mapped[float | None] = mapped_column(Float)
    robust_se: Mapped[str | None] = mapped_column(String(16))
    adjustment_method: Mapped[str | None] = mapped_column(String(64))
    diagnostic_status: Mapped[str] = mapped_column(String(32))
    interpretation_level: Mapped[str] = mapped_column(
        String(64), default="ESTIMATED_TREATMENT_EFFECT"
    )
    notes: Mapped[str | None] = mapped_column(Text)
    warnings: Mapped[str | None] = mapped_column(Text)
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    __table_args__ = (
        UniqueConstraint("treatment_effect_result_id", "method", "estimand"),
    )


class SelectedAdjustmentVariable(Base):
    __tablename__ = "selected_adjustment_variable"
    treatment_effect_result_id: Mapped[str] = mapped_column(
        ForeignKey("treatment_effect_result.id"), primary_key=True
    )
    feature_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    ordinal: Mapped[int] = mapped_column(Integer)
    selection_source: Mapped[str] = mapped_column(String(32))


class ExcludedAdjustmentCandidate(Base):
    __tablename__ = "excluded_adjustment_candidate"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    treatment_effect_result_id: Mapped[str] = mapped_column(
        ForeignKey("treatment_effect_result.id"), index=True
    )
    feature_name: Mapped[str] = mapped_column(String(255))
    reason_code: Mapped[str] = mapped_column(String(128))
    reason_detail: Mapped[str | None] = mapped_column(Text)
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


class DiagnosticSummary(Base):
    __tablename__ = "diagnostic_summary"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    stage_run_id: Mapped[str] = mapped_column(ForeignKey("stage_run.id"), index=True)
    diagnostic_type: Mapped[str] = mapped_column(String(64))
    metric_name: Mapped[str] = mapped_column(String(128))
    metric_value_number: Mapped[float | None] = mapped_column(Float)
    metric_value_text: Mapped[str | None] = mapped_column(Text)
    severity: Mapped[str | None] = mapped_column(String(16))
    status: Mapped[str | None] = mapped_column(String(32))
    artifact_id: Mapped[str | None] = mapped_column(ForeignKey("artifact.id"))
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


def _changed(target: Any, names: set[str]) -> bool:
    state = inspect(target)
    return any(state.attrs[name].history.has_changes() for name in names)


@event.listens_for(ConfigurationVersion, "before_update")
def _protect_published_configuration(
    _: Any, __: Any, target: ConfigurationVersion
) -> None:
    previous = inspect(target).attrs.status.history.deleted
    prior_status = previous[0] if previous else target.status
    if prior_status in {"PUBLISHED", "DEPRECATED"} and _changed(
        target,
        {
            "schema_version",
            "canonical_json",
            "original_format",
            "original_text",
            "content_hash",
            "configuration_id",
            "version_number",
        },
    ):
        raise ValueError("Published configuration content is immutable")


@event.listens_for(DatasetVersion, "before_update")
def _protect_ready_dataset(_: Any, __: Any, target: DatasetVersion) -> None:
    previous = inspect(target).attrs.status.history.deleted
    prior_status = previous[0] if previous else target.status
    if prior_status == "READY" and _changed(
        target,
        {
            "dataset_id",
            "version_number",
            "source_type",
            "source_metadata",
            "schema_hash",
            "content_hash",
            "table_count",
        },
    ):
        raise ValueError("Ready dataset version content is immutable")


@event.listens_for(PipelineDefinitionVersion, "before_update")
def _protect_published_pipeline(
    _: Any, __: Any, target: PipelineDefinitionVersion
) -> None:
    previous = inspect(target).attrs.status.history.deleted
    prior_status = previous[0] if previous else target.status
    if prior_status in {"PUBLISHED", "DEPRECATED"} and _changed(
        target,
        {
            "pipeline_definition_id",
            "version_number",
            "random_seed_default",
            "fail_fast",
            "canonical_json",
            "content_hash",
        },
    ):
        raise ValueError("Published pipeline definition version is immutable")


@event.listens_for(DatasetTableVersion, "before_update")
def _protect_dataset_table(_: Any, __: Any, target: DatasetTableVersion) -> None:
    if _changed(
        target,
        {
            "dataset_version_id",
            "logical_name",
            "stored_object_id",
            "ordinal",
            "file_format",
            "schema_json",
            "schema_hash",
            "content_hash",
            "partition_values",
        },
    ):
        raise ValueError("Dataset table content is immutable")


@event.listens_for(Artifact, "before_update")
def _protect_available_artifact(_: Any, __: Any, target: Artifact) -> None:
    previous = inspect(target).attrs.status.history.deleted
    prior_status = previous[0] if previous else target.status
    if prior_status == "AVAILABLE" and _changed(
        target,
        {"stored_object_id", "content_hash", "schema_name", "schema_version"},
    ):
        raise ValueError("Available artifact content is immutable")


@event.listens_for(CausalGraphVersion, "before_update")
def _protect_published_causal_graph(
    _: Any, __: Any, target: CausalGraphVersion
) -> None:
    previous = inspect(target).attrs.status.history.deleted
    prior_status = previous[0] if previous else target.status
    if prior_status in {"PUBLISHED", "DEPRECATED"} and _changed(
        target,
        {
            "causal_graph_id",
            "version_number",
            "source_discovery_algorithm_result_id",
            "dataset_version_id",
            "feature_semantics_version_id",
            "canonical_json",
            "content_hash",
            "node_count",
            "edge_count",
        },
    ):
        raise ValueError("Published causal graph content is immutable")


__all__ = [
    name
    for name, value in globals().items()
    if isinstance(value, type) and issubclass(value, Base)
]
