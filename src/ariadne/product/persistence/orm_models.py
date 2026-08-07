"""SQLAlchemy ORM models for the product domain (new schema)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def _new_id() -> str:
    return str(uuid.uuid4())


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ProductBase(DeclarativeBase):
    pass


class IdempotencyRecordOrm(ProductBase):
    """Technical table; not a business entity."""

    __tablename__ = "product_idempotency"
    idempotency_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    project_id: Mapped[str] = mapped_column(String(36), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(200), nullable=False)
    request_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    response_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    __table_args__ = (
        UniqueConstraint("project_id", "scope", "idempotency_key", name="uq_product_idempotency_key"),
    )


class ProjectOrm(ProductBase):
    __tablename__ = "product_project"

    project_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    topic: Mapped[str | None] = mapped_column(Text)
    objective: Mapped[str | None] = mapped_column(Text)
    memo: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow)

    __table_args__ = (
        CheckConstraint("status IN ('ACTIVE', 'ARCHIVED')", name="ck_product_project_status"),
    )


class ArtifactOrm(ProductBase):
    __tablename__ = "product_artifact"

    artifact_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False, index=True)
    execution_id: Mapped[str | None] = mapped_column(ForeignKey("product_execution.execution_id", ondelete="RESTRICT"), index=True)
    result_id: Mapped[str | None] = mapped_column(ForeignKey("product_result.result_id", ondelete="RESTRICT"), index=True)
    artifact_type: Mapped[str] = mapped_column(String(40), nullable=False)
    object_key: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    content_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    media_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    __table_args__ = (
        CheckConstraint("size_bytes >= 0", name="ck_product_artifact_size_bytes"),
        CheckConstraint(
            "artifact_type IN ('DATASET_FILE','GRAPH_JSON','GRAPH_IMAGE','EFFECT_TABLE','DIAGNOSTICS_TABLE','MANIFEST','CONFIG_SNAPSHOT','LOG','SCIENTIFIC_RESULT_JSON','SCIENTIFIC_REPORT')",
            name="ck_product_artifact_type",
        ),
    )


class DatasetVersionOrm(ProductBase):
    __tablename__ = "product_dataset_version"

    dataset_version_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False, index=True)
    source_artifact_id: Mapped[str] = mapped_column(ForeignKey("product_artifact.artifact_id", ondelete="RESTRICT"), nullable=False, unique=True)
    dataset_key: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    version_label: Mapped[str] = mapped_column(String(100), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    schema_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    profile_summary_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    row_count: Mapped[int] = mapped_column(BigInteger, nullable=False)
    column_count: Mapped[int] = mapped_column(Integer, nullable=False)
    source_note: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    __table_args__ = (
        UniqueConstraint("project_id", "dataset_key", "version_label", name="uq_product_dsv_version_label"),
        UniqueConstraint("project_id", "dataset_key", "content_hash", name="uq_product_dsv_content_hash"),
        CheckConstraint("row_count >= 0", name="ck_product_dsv_row_count"),
        CheckConstraint("column_count >= 0", name="ck_product_dsv_column_count"),
    )


class ExecutionOrm(ProductBase):
    __tablename__ = "product_execution"

    execution_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False, index=True)
    dataset_version_id: Mapped[str] = mapped_column(ForeignKey("product_dataset_version.dataset_version_id", ondelete="RESTRICT"), nullable=False, index=True)
    input_graph_version_id: Mapped[str | None] = mapped_column(ForeignKey("product_graph_version.graph_version_id", ondelete="RESTRICT"), index=True)
    input_result_id: Mapped[str | None] = mapped_column(ForeignKey("product_result.result_id", ondelete="RESTRICT"), index=True)
    batch_key: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    operation: Mapped[str] = mapped_column(String(20), nullable=False)
    objective_snapshot: Mapped[str | None] = mapped_column(Text)
    rationale_snapshot: Mapped[str | None] = mapped_column(Text)
    analysis_spec_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    algorithm_or_estimator: Mapped[str] = mapped_column(String(100), nullable=False)
    parameter_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    random_seed: Mapped[int | None] = mapped_column(BigInteger)
    code_version: Mapped[str] = mapped_column(String(200), nullable=False)
    runtime_version_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    snapshot_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    snapshot_schema_version: Mapped[str] = mapped_column(
        String(100), nullable=False, default="causal-analysis-spec/2"
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="QUEUED")
    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_error_summary: Mapped[str | None] = mapped_column(Text)
    requested_by: Mapped[str] = mapped_column(String(200), nullable=False)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_utcnow)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    # internal worker token - not exposed as domain attribute
    _worker_token: Mapped[str | None] = mapped_column("worker_token", String(36))

    __table_args__ = (
        CheckConstraint(
            "operation IN ('DISCOVERY','IDENTIFICATION','ESTIMATION','REFUTATION','SENSITIVITY')",
            name="ck_product_execution_operation",
        ),
        CheckConstraint(
            "status IN ('QUEUED', 'RUNNING', 'SUCCEEDED', 'FAILED', 'CANCELLED')",
            name="ck_product_execution_status",
        ),
        CheckConstraint("retry_count >= 0", name="ck_product_execution_retry_count"),
        CheckConstraint(
            "(operation = 'DISCOVERY' AND input_graph_version_id IS NULL AND input_result_id IS NULL) OR "
            "(operation = 'IDENTIFICATION' AND input_graph_version_id IS NOT NULL AND input_result_id IS NULL) OR "
            "(operation = 'ESTIMATION' AND input_graph_version_id IS NOT NULL AND "
            "(input_result_id IS NOT NULL OR snapshot_schema_version = 'legacy-product-snapshot/1')) OR "
            "(operation IN ('REFUTATION','SENSITIVITY') AND input_graph_version_id IS NOT NULL AND input_result_id IS NOT NULL)",
            name="ck_product_execution_input_by_operation",
        ),
    )


class ResultOrm(ProductBase):
    __tablename__ = "product_result"

    result_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    execution_id: Mapped[str] = mapped_column(ForeignKey("product_execution.execution_id", ondelete="RESTRICT"), nullable=False, index=True)
    result_type: Mapped[str] = mapped_column(String(40), nullable=False)
    scientific_status: Mapped[str] = mapped_column(String(40), nullable=False)
    summary_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    diagnostics_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    warning_json: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    __table_args__ = (
        CheckConstraint(
            "result_type IN ('DISCOVERY_GRAPH_RESULT','IDENTIFICATION_RESULT','DATA_ELIGIBILITY_RESULT','TREATMENT_EFFECT_RESULT','DIAGNOSTICS_RESULT','REFUTATION_RESULT','SENSITIVITY_RESULT')",
            name="ck_product_result_type",
        ),
        CheckConstraint(
            "scientific_status IN ('GENERATED','GENERATED_WITH_WARNINGS','UNRELIABLE','IDENTIFIED','NOT_IDENTIFIED','PARTIALLY_IDENTIFIED','REQUIRES_REVIEW','PASS','WARN','FAIL','ESTIMATED','INSUFFICIENT_OVERLAP','INSUFFICIENT_SAMPLE','ESTIMATION_UNRELIABLE','NO_FAILURE_DETECTED','FAILURE_DETECTED','INCONCLUSIVE','ROBUST','FRAGILE')",
            name="ck_product_result_scientific_status",
        ),
        CheckConstraint(
            "(result_type = 'DISCOVERY_GRAPH_RESULT' AND scientific_status IN ('GENERATED','GENERATED_WITH_WARNINGS','UNRELIABLE')) OR "
            "(result_type = 'IDENTIFICATION_RESULT' AND scientific_status IN ('IDENTIFIED','NOT_IDENTIFIED','PARTIALLY_IDENTIFIED','REQUIRES_REVIEW')) OR "
            "(result_type IN ('DATA_ELIGIBILITY_RESULT','DIAGNOSTICS_RESULT') AND scientific_status IN ('PASS','WARN','FAIL')) OR "
            "(result_type = 'TREATMENT_EFFECT_RESULT' AND scientific_status IN ('ESTIMATED','INSUFFICIENT_OVERLAP','INSUFFICIENT_SAMPLE','ESTIMATION_UNRELIABLE','REQUIRES_REVIEW')) OR "
            "(result_type = 'REFUTATION_RESULT' AND scientific_status IN ('NO_FAILURE_DETECTED','FAILURE_DETECTED','INCONCLUSIVE')) OR "
            "(result_type = 'SENSITIVITY_RESULT' AND scientific_status IN ('ROBUST','FRAGILE','INCONCLUSIVE'))",
            name="ck_product_result_status_matrix",
        ),
    )


class GraphVersionOrm(ProductBase):
    __tablename__ = "product_graph_version"

    graph_version_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False, index=True)
    source_result_id: Mapped[str | None] = mapped_column(ForeignKey("product_result.result_id", ondelete="RESTRICT"), index=True)
    parent_graph_version_id: Mapped[str | None] = mapped_column(ForeignKey("product_graph_version.graph_version_id", ondelete="RESTRICT"), index=True)
    designated_outcome_node: Mapped[str | None] = mapped_column(String(200), index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    graph_type: Mapped[str] = mapped_column(String(40), nullable=False)
    graph_origin: Mapped[str] = mapped_column(String(40), nullable=False)
    provenance_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    graph_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    content_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    edit_rationale: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="DRAFT")
    created_by: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    __table_args__ = (
        CheckConstraint("status IN ('DRAFT', 'FIXED')", name="ck_product_graph_version_status"),
        CheckConstraint("graph_type IN ('DAG','CPDAG','PAG')", name="ck_product_graph_version_type"),
        CheckConstraint(
            "graph_origin IN ('DISCOVERED','CONSTRAINT_ADJUSTED','USER_DEFINED','IMPORTED','USER_EDITED')",
            name="ck_product_graph_origin",
        ),
        CheckConstraint(
            "(graph_origin = 'DISCOVERED' AND source_result_id IS NOT NULL) OR "
            "(graph_origin = 'CONSTRAINT_ADJUSTED' AND (source_result_id IS NOT NULL OR parent_graph_version_id IS NOT NULL)) OR "
            "(graph_origin IN ('USER_DEFINED','IMPORTED') AND source_result_id IS NULL AND parent_graph_version_id IS NULL) OR "
            "(graph_origin = 'USER_EDITED' AND source_result_id IS NULL AND parent_graph_version_id IS NOT NULL)",
            name="ck_product_graph_origin_references",
        ),
    )


class AnnotationOrm(ProductBase):
    __tablename__ = "product_annotation"

    annotation_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False, index=True)
    target_result_id: Mapped[str | None] = mapped_column(ForeignKey("product_result.result_id", ondelete="RESTRICT"), index=True)
    target_graph_version_id: Mapped[str | None] = mapped_column(ForeignKey("product_graph_version.graph_version_id", ondelete="RESTRICT"), index=True)
    statement: Mapped[str] = mapped_column(Text, nullable=False)
    rationale: Mapped[str | None] = mapped_column(Text)
    assumptions_json: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
    limitations_json: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
    created_by: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow)

    __table_args__ = (
        CheckConstraint(
            "(target_result_id IS NOT NULL) != (target_graph_version_id IS NOT NULL)",
            name="ck_product_annotation_target_xor",
        ),
    )


# ENH-E3 versioned workspace resources.  These tables are additive so the
# existing causal product rows and their strict status constraints remain
# readable without a destructive rewrite.


class AnalysisViewOrm(ProductBase):
    __tablename__ = "product_analysis_view"

    analysis_view_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False, index=True)
    source_dataset_version_id: Mapped[str] = mapped_column(ForeignKey("product_dataset_version.dataset_version_id", ondelete="RESTRICT"), nullable=False, index=True)
    view_key: Mapped[str] = mapped_column(String(100), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="DRAFT")
    schema_version: Mapped[str] = mapped_column(String(100), nullable=False, default="analysis-view/1")
    spec_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    content_hash: Mapped[str | None] = mapped_column(String(64))
    manifest_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_by: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    fixed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("project_id", "view_key", "version_number", name="uq_product_analysis_view_version"),
        CheckConstraint("status IN ('DRAFT','FIXED')", name="ck_product_analysis_view_status"),
        CheckConstraint("version_number > 0", name="ck_product_analysis_view_version"),
    )


class ExecutionPlanOrm(ProductBase):
    __tablename__ = "product_execution_plan"

    execution_plan_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False, index=True)
    analysis_specification_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    analysis_family: Mapped[str] = mapped_column(String(20), nullable=False)
    plan_schema_version: Mapped[str] = mapped_column(String(100), nullable=False)
    planner_id: Mapped[str] = mapped_column(String(100), nullable=False)
    planner_version: Mapped[str] = mapped_column(String(40), nullable=False)
    stages_json: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    dependencies_json: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    plan_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    __table_args__ = (
        CheckConstraint("analysis_family IN ('EXPLORATORY','CAUSAL','PREDICTIVE')", name="ck_product_execution_plan_family"),
    )


class FamilyExecutionOrm(ProductBase):
    __tablename__ = "product_family_execution"

    execution_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False, index=True)
    dataset_version_id: Mapped[str] = mapped_column(ForeignKey("product_dataset_version.dataset_version_id", ondelete="RESTRICT"), nullable=False, index=True)
    analysis_view_id: Mapped[str | None] = mapped_column(ForeignKey("product_analysis_view.analysis_view_id", ondelete="RESTRICT"), index=True)
    execution_plan_id: Mapped[str] = mapped_column(ForeignKey("product_execution_plan.execution_plan_id", ondelete="RESTRICT"), nullable=False, index=True)
    analysis_family: Mapped[str] = mapped_column(String(20), nullable=False)
    specification_schema_version: Mapped[str] = mapped_column(String(100), nullable=False)
    specification_snapshot_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    snapshot_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    snapshot_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="QUEUED")
    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_error_json: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    requested_by: Mapped[str] = mapped_column(String(200), nullable=False)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    worker_token: Mapped[str | None] = mapped_column(String(36))
    worker_id: Mapped[str | None] = mapped_column(String(200))
    lease_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint("analysis_family IN ('EXPLORATORY','CAUSAL','PREDICTIVE')", name="ck_product_family_execution_family"),
        CheckConstraint("status IN ('QUEUED','RUNNING','SUCCEEDED','FAILED','CANCELLED')", name="ck_product_family_execution_status"),
        CheckConstraint("retry_count >= 0", name="ck_product_family_execution_retry"),
    )


class FamilyStageExecutionOrm(ProductBase):
    __tablename__ = "product_family_stage_execution"

    stage_execution_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    execution_id: Mapped[str] = mapped_column(ForeignKey("product_family_execution.execution_id", ondelete="RESTRICT"), nullable=False, index=True)
    stage_key: Mapped[str] = mapped_column(String(100), nullable=False)
    stage_type_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    ordinal: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="PENDING")
    attempt_history_json: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
    input_binding_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    output_binding_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    last_error_json: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("execution_id", "stage_key", name="uq_product_family_stage_key"),
        CheckConstraint("status IN ('PENDING','READY','RUNNING','SUCCEEDED','FAILED','SKIPPED_DUE_TO_PREREQUISITE')", name="ck_product_family_stage_status"),
    )


class FamilyResultOrm(ProductBase):
    __tablename__ = "product_family_result"

    result_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False, index=True)
    execution_id: Mapped[str] = mapped_column(ForeignKey("product_family_execution.execution_id", ondelete="RESTRICT"), nullable=False, index=True)
    stage_execution_id: Mapped[str] = mapped_column(ForeignKey("product_family_stage_execution.stage_execution_id", ondelete="RESTRICT"), nullable=False, index=True)
    analysis_family: Mapped[str] = mapped_column(String(20), nullable=False)
    result_type: Mapped[str] = mapped_column(String(100), nullable=False)
    schema_version: Mapped[str] = mapped_column(String(100), nullable=False)
    analytical_status: Mapped[str] = mapped_column(String(60), nullable=False)
    summary_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    diagnostics_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    warning_json: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    __table_args__ = (
        CheckConstraint("analysis_family IN ('EXPLORATORY','CAUSAL','PREDICTIVE')", name="ck_product_family_result_family"),
    )


class FamilyArtifactOrm(ProductBase):
    __tablename__ = "product_family_artifact"

    artifact_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False, index=True)
    execution_id: Mapped[str] = mapped_column(ForeignKey("product_family_execution.execution_id", ondelete="RESTRICT"), nullable=False, index=True)
    stage_execution_id: Mapped[str] = mapped_column(ForeignKey("product_family_stage_execution.stage_execution_id", ondelete="RESTRICT"), nullable=False, index=True)
    result_id: Mapped[str | None] = mapped_column(ForeignKey("product_family_result.result_id", ondelete="RESTRICT"), index=True)
    family: Mapped[str] = mapped_column(String(20), nullable=False)
    artifact_type: Mapped[str] = mapped_column(String(100), nullable=False)
    schema_version: Mapped[str] = mapped_column(String(100), nullable=False)
    media_type: Mapped[str] = mapped_column(String(100), nullable=False)
    object_key: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    __table_args__ = (
        CheckConstraint("family IN ('EXPLORATORY','CAUSAL','PREDICTIVE')", name="ck_product_family_artifact_family"),
        CheckConstraint("size_bytes >= 0", name="ck_product_family_artifact_size"),
    )


class LineageEdgeOrm(ProductBase):
    __tablename__ = "product_lineage_edge"

    lineage_edge_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(100), nullable=False)
    source_id: Mapped[str] = mapped_column(String(100), nullable=False)
    relation_type: Mapped[str] = mapped_column(String(100), nullable=False)
    target_type: Mapped[str] = mapped_column(String(100), nullable=False)
    target_id: Mapped[str] = mapped_column(String(100), nullable=False)
    evidence_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_by: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    __table_args__ = (
        UniqueConstraint("source_type", "source_id", "relation_type", "target_type", "target_id", name="uq_product_lineage_edge"),
    )
