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
        CheckConstraint("operation IN ('DISCOVERY', 'ESTIMATION')", name="ck_product_execution_operation"),
        CheckConstraint(
            "status IN ('QUEUED', 'RUNNING', 'SUCCEEDED', 'FAILED', 'CANCELLED')",
            name="ck_product_execution_status",
        ),
        CheckConstraint("retry_count >= 0", name="ck_product_execution_retry_count"),
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


class GraphVersionOrm(ProductBase):
    __tablename__ = "product_graph_version"

    graph_version_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False, index=True)
    source_result_id: Mapped[str] = mapped_column(ForeignKey("product_result.result_id", ondelete="RESTRICT"), nullable=False, index=True)
    parent_graph_version_id: Mapped[str | None] = mapped_column(ForeignKey("product_graph_version.graph_version_id", ondelete="RESTRICT"), index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    graph_type: Mapped[str] = mapped_column(String(40), nullable=False)
    graph_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    content_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    edit_rationale: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="DRAFT")
    created_by: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    __table_args__ = (
        CheckConstraint("status IN ('DRAFT', 'FIXED')", name="ck_product_graph_version_status"),
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
