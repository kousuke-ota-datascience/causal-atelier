"""20260805_0001_product_domain_baseline

Revision ID: 20260805_product_0001
Revises:
Create Date: 2026-08-05

Baseline migration for the product domain – creates the 7 core entities.
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260805_product_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "product_idempotency",
        sa.Column("idempotency_id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), nullable=False),
        sa.Column("scope", sa.String(100), nullable=False),
        sa.Column("idempotency_key", sa.String(200), nullable=False),
        sa.Column("request_hash", sa.String(64), nullable=False),
        sa.Column("response_json", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("project_id", "scope", "idempotency_key", name="uq_product_idempotency_key"),
    )
    op.create_table(
        "product_project",
        sa.Column("project_id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("topic", sa.Text),
        sa.Column("objective", sa.Text),
        sa.Column("memo", sa.Text),
        sa.Column("status", sa.String(20), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("status IN ('ACTIVE', 'ARCHIVED')", name="ck_product_project_status"),
    )

    op.create_table(
        "product_execution",
        sa.Column("execution_id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("dataset_version_id", sa.String(36), nullable=False),
        sa.Column("input_graph_version_id", sa.String(36)),
        sa.Column("batch_key", sa.String(36), nullable=False),
        sa.Column("operation", sa.String(20), nullable=False),
        sa.Column("objective_snapshot", sa.Text),
        sa.Column("rationale_snapshot", sa.Text),
        sa.Column("analysis_spec_json", sa.JSON, nullable=False, server_default="{}"),
        sa.Column("algorithm_or_estimator", sa.String(100), nullable=False),
        sa.Column("parameter_json", sa.JSON, nullable=False, server_default="{}"),
        sa.Column("random_seed", sa.BigInteger),
        sa.Column("code_version", sa.String(200), nullable=False),
        sa.Column("runtime_version_json", sa.JSON, nullable=False, server_default="{}"),
        sa.Column("snapshot_hash", sa.String(128), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="QUEUED"),
        sa.Column("retry_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("last_error_summary", sa.Text),
        sa.Column("requested_by", sa.String(200), nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column("worker_token", sa.String(36)),
        sa.CheckConstraint("operation IN ('DISCOVERY', 'ESTIMATION')", name="ck_product_execution_operation"),
        sa.CheckConstraint(
            "status IN ('QUEUED', 'RUNNING', 'SUCCEEDED', 'FAILED', 'CANCELLED')",
            name="ck_product_execution_status",
        ),
        sa.CheckConstraint("retry_count >= 0", name="ck_product_execution_retry_count"),
        sa.CheckConstraint(
            "(operation = 'DISCOVERY' AND input_graph_version_id IS NULL) OR (operation = 'ESTIMATION' AND input_graph_version_id IS NOT NULL)",
            name="ck_product_execution_graph_by_operation",
        ),
    )
    op.create_index("ix_product_execution_project_id", "product_execution", ["project_id"])
    op.create_index("ix_product_execution_dataset_version_id", "product_execution", ["dataset_version_id"])
    op.create_index("ix_product_execution_input_graph_version_id", "product_execution", ["input_graph_version_id"])
    op.create_index("ix_product_execution_batch_key", "product_execution", ["batch_key"])
    op.create_index("ix_product_execution_status", "product_execution", ["status"])

    op.create_table(
        "product_result",
        sa.Column("result_id", sa.String(36), primary_key=True),
        sa.Column("execution_id", sa.String(36), sa.ForeignKey("product_execution.execution_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("result_type", sa.String(40), nullable=False),
        sa.Column("scientific_status", sa.String(40), nullable=False),
        sa.Column("summary_json", sa.JSON, nullable=False, server_default="{}"),
        sa.Column("payload_json", sa.JSON, nullable=False, server_default="{}"),
        sa.Column("diagnostics_json", sa.JSON, nullable=False, server_default="{}"),
        sa.Column("warning_json", sa.JSON, nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("result_type IN ('DISCOVERY_GRAPH_RESULT','IDENTIFICATION_RESULT','TREATMENT_EFFECT_RESULT')", name="ck_product_result_type"),
        sa.CheckConstraint("scientific_status IN ('VALID','NOT_IDENTIFIED','INSUFFICIENT_OVERLAP','INSUFFICIENT_SAMPLE','ESTIMATION_UNRELIABLE')", name="ck_product_result_scientific_status"),
    )
    op.create_index("ix_product_result_execution_id", "product_result", ["execution_id"])

    op.create_table(
        "product_graph_version",
        sa.Column("graph_version_id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("source_result_id", sa.String(36), sa.ForeignKey("product_result.result_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("parent_graph_version_id", sa.String(36), sa.ForeignKey("product_graph_version.graph_version_id", ondelete="RESTRICT")),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("graph_type", sa.String(40), nullable=False),
        sa.Column("graph_json", sa.JSON, nullable=False, server_default="{}"),
        sa.Column("content_hash", sa.String(128), nullable=False),
        sa.Column("edit_rationale", sa.Text),
        sa.Column("status", sa.String(20), nullable=False, server_default="DRAFT"),
        sa.Column("created_by", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("status IN ('DRAFT', 'FIXED')", name="ck_product_graph_version_status"),
        sa.CheckConstraint("graph_type IN ('DAG','CPDAG','PAG')", name="ck_product_graph_version_type"),
    )
    op.create_index("ix_product_graph_version_project_id", "product_graph_version", ["project_id"])
    op.create_index("ix_product_graph_version_source_result_id", "product_graph_version", ["source_result_id"])
    op.create_index("ix_product_graph_version_parent_id", "product_graph_version", ["parent_graph_version_id"])

    op.create_table(
        "product_artifact",
        sa.Column("artifact_id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("execution_id", sa.String(36), sa.ForeignKey("product_execution.execution_id", ondelete="RESTRICT")),
        sa.Column("result_id", sa.String(36), sa.ForeignKey("product_result.result_id", ondelete="RESTRICT")),
        sa.Column("artifact_type", sa.String(40), nullable=False),
        sa.Column("object_key", sa.Text, nullable=False, unique=True),
        sa.Column("content_hash", sa.String(128), nullable=False),
        sa.Column("media_type", sa.String(100), nullable=False),
        sa.Column("size_bytes", sa.BigInteger, nullable=False),
        sa.Column("metadata_json", sa.JSON, nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("size_bytes >= 0", name="ck_product_artifact_size_bytes"),
        sa.CheckConstraint("artifact_type IN ('DATASET_FILE','GRAPH_JSON','GRAPH_IMAGE','EFFECT_TABLE','DIAGNOSTICS_TABLE','MANIFEST','CONFIG_SNAPSHOT','LOG')", name="ck_product_artifact_type"),
    )
    op.create_index("ix_product_artifact_project_id", "product_artifact", ["project_id"])
    op.create_index("ix_product_artifact_execution_id", "product_artifact", ["execution_id"])
    op.create_index("ix_product_artifact_result_id", "product_artifact", ["result_id"])

    op.create_table(
        "product_dataset_version",
        sa.Column("dataset_version_id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("source_artifact_id", sa.String(36), sa.ForeignKey("product_artifact.artifact_id", ondelete="RESTRICT"), nullable=False, unique=True),
        sa.Column("dataset_key", sa.String(100), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("version_label", sa.String(100), nullable=False),
        sa.Column("content_hash", sa.String(128), nullable=False),
        sa.Column("schema_json", sa.JSON, nullable=False, server_default="{}"),
        sa.Column("profile_summary_json", sa.JSON, nullable=False, server_default="{}"),
        sa.Column("row_count", sa.BigInteger, nullable=False),
        sa.Column("column_count", sa.Integer, nullable=False),
        sa.Column("source_note", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("project_id", "dataset_key", "version_label", name="uq_product_dsv_version_label"),
        sa.UniqueConstraint("project_id", "dataset_key", "content_hash", name="uq_product_dsv_content_hash"),
        sa.CheckConstraint("row_count >= 0", name="ck_product_dsv_row_count"),
        sa.CheckConstraint("column_count >= 0", name="ck_product_dsv_column_count"),
    )
    op.create_index("ix_product_dataset_version_project_id", "product_dataset_version", ["project_id"])
    op.create_index("ix_product_dataset_version_dataset_key", "product_dataset_version", ["dataset_key"])

    # Add FK constraint from execution to dataset_version (deferred to after both tables exist)
    op.create_foreign_key(
        "fk_product_execution_dataset_version_id",
        "product_execution", "product_dataset_version",
        ["dataset_version_id"], ["dataset_version_id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_product_execution_input_graph_version_id",
        "product_execution", "product_graph_version",
        ["input_graph_version_id"], ["graph_version_id"],
        ondelete="RESTRICT",
    )

    op.create_table(
        "product_annotation",
        sa.Column("annotation_id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("target_result_id", sa.String(36), sa.ForeignKey("product_result.result_id", ondelete="RESTRICT")),
        sa.Column("target_graph_version_id", sa.String(36), sa.ForeignKey("product_graph_version.graph_version_id", ondelete="RESTRICT")),
        sa.Column("statement", sa.Text, nullable=False),
        sa.Column("rationale", sa.Text),
        sa.Column("assumptions_json", sa.JSON, nullable=False, server_default="[]"),
        sa.Column("limitations_json", sa.JSON, nullable=False, server_default="[]"),
        sa.Column("created_by", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "(target_result_id IS NOT NULL) != (target_graph_version_id IS NOT NULL)",
            name="ck_product_annotation_target_xor",
        ),
    )
    op.create_index("ix_product_annotation_project_id", "product_annotation", ["project_id"])
    op.create_index("ix_product_annotation_target_result_id", "product_annotation", ["target_result_id"])
    op.create_index("ix_product_annotation_target_gv_id", "product_annotation", ["target_graph_version_id"])


def downgrade() -> None:
    op.drop_table("product_annotation")
    op.drop_constraint("fk_product_execution_input_graph_version_id", "product_execution", type_="foreignkey")
    op.drop_constraint("fk_product_execution_dataset_version_id", "product_execution", type_="foreignkey")
    op.drop_table("product_dataset_version")
    op.drop_table("product_artifact")
    op.drop_table("product_graph_version")
    op.drop_table("product_result")
    op.drop_table("product_execution")
    op.drop_table("product_idempotency")
    op.drop_table("product_project")
