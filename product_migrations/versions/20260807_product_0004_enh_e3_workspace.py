"""ENH-E3 generic workspace and exploratory persistence.

Revision ID: 20260807_product_0004
Revises: 20260806_product_0003
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260807_product_0004"
down_revision = "20260806_product_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "product_analysis_view",
        sa.Column("analysis_view_id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("source_dataset_version_id", sa.String(36), sa.ForeignKey("product_dataset_version.dataset_version_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("view_key", sa.String(100), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("schema_version", sa.String(100), nullable=False),
        sa.Column("spec_json", sa.JSON(), nullable=False),
        sa.Column("content_hash", sa.String(64)),
        sa.Column("manifest_json", sa.JSON(), nullable=False),
        sa.Column("created_by", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("fixed_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("project_id", "view_key", "version_number", name="uq_product_analysis_view_version"),
        sa.CheckConstraint("status IN ('DRAFT','FIXED')", name="ck_product_analysis_view_status"),
        sa.CheckConstraint("version_number > 0", name="ck_product_analysis_view_version"),
    )
    op.create_index("ix_product_analysis_view_project_id", "product_analysis_view", ["project_id"])
    op.create_index("ix_product_analysis_view_source_dataset_version_id", "product_analysis_view", ["source_dataset_version_id"])

    op.create_table(
        "product_execution_plan",
        sa.Column("execution_plan_id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("analysis_specification_id", sa.String(100), nullable=False),
        sa.Column("analysis_family", sa.String(20), nullable=False),
        sa.Column("plan_schema_version", sa.String(100), nullable=False),
        sa.Column("planner_id", sa.String(100), nullable=False),
        sa.Column("planner_version", sa.String(40), nullable=False),
        sa.Column("stages_json", sa.JSON(), nullable=False),
        sa.Column("dependencies_json", sa.JSON(), nullable=False),
        sa.Column("plan_hash", sa.String(64), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("analysis_family IN ('EXPLORATORY','CAUSAL','PREDICTIVE')", name="ck_product_execution_plan_family"),
    )
    op.create_index("ix_product_execution_plan_project_id", "product_execution_plan", ["project_id"])
    op.create_index("ix_product_execution_plan_analysis_specification_id", "product_execution_plan", ["analysis_specification_id"])

    op.create_table(
        "product_family_execution",
        sa.Column("execution_id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("dataset_version_id", sa.String(36), sa.ForeignKey("product_dataset_version.dataset_version_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("analysis_view_id", sa.String(36), sa.ForeignKey("product_analysis_view.analysis_view_id", ondelete="RESTRICT")),
        sa.Column("execution_plan_id", sa.String(36), sa.ForeignKey("product_execution_plan.execution_plan_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("analysis_family", sa.String(20), nullable=False),
        sa.Column("specification_schema_version", sa.String(100), nullable=False),
        sa.Column("specification_snapshot_json", sa.JSON(), nullable=False),
        sa.Column("snapshot_json", sa.JSON(), nullable=False),
        sa.Column("snapshot_hash", sa.String(64), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("retry_count", sa.Integer(), nullable=False),
        sa.Column("last_error_json", sa.JSON()),
        sa.Column("requested_by", sa.String(200), nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column("worker_token", sa.String(36)),
        sa.Column("worker_id", sa.String(200)),
        sa.Column("lease_expires_at", sa.DateTime(timezone=True)),
        sa.CheckConstraint("analysis_family IN ('EXPLORATORY','CAUSAL','PREDICTIVE')", name="ck_product_family_execution_family"),
        sa.CheckConstraint("status IN ('QUEUED','RUNNING','SUCCEEDED','FAILED','CANCELLED')", name="ck_product_family_execution_status"),
        sa.CheckConstraint("retry_count >= 0", name="ck_product_family_execution_retry"),
    )
    for column in ("project_id", "dataset_version_id", "analysis_view_id", "execution_plan_id"):
        op.create_index(f"ix_product_family_execution_{column}", "product_family_execution", [column])

    op.create_table(
        "product_family_stage_execution",
        sa.Column("stage_execution_id", sa.String(36), primary_key=True),
        sa.Column("execution_id", sa.String(36), sa.ForeignKey("product_family_execution.execution_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("stage_key", sa.String(100), nullable=False),
        sa.Column("stage_type_json", sa.JSON(), nullable=False),
        sa.Column("ordinal", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(40), nullable=False),
        sa.Column("attempt_history_json", sa.JSON(), nullable=False),
        sa.Column("input_binding_json", sa.JSON(), nullable=False),
        sa.Column("output_binding_json", sa.JSON(), nullable=False),
        sa.Column("last_error_json", sa.JSON()),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("execution_id", "stage_key", name="uq_product_family_stage_key"),
        sa.CheckConstraint("status IN ('PENDING','READY','RUNNING','SUCCEEDED','FAILED','SKIPPED_DUE_TO_PREREQUISITE')", name="ck_product_family_stage_status"),
    )
    op.create_index("ix_product_family_stage_execution_execution_id", "product_family_stage_execution", ["execution_id"])

    op.create_table(
        "product_family_result",
        sa.Column("result_id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("execution_id", sa.String(36), sa.ForeignKey("product_family_execution.execution_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("stage_execution_id", sa.String(36), sa.ForeignKey("product_family_stage_execution.stage_execution_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("analysis_family", sa.String(20), nullable=False),
        sa.Column("result_type", sa.String(100), nullable=False),
        sa.Column("schema_version", sa.String(100), nullable=False),
        sa.Column("analytical_status", sa.String(60), nullable=False),
        sa.Column("summary_json", sa.JSON(), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=False),
        sa.Column("diagnostics_json", sa.JSON(), nullable=False),
        sa.Column("warning_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("analysis_family IN ('EXPLORATORY','CAUSAL','PREDICTIVE')", name="ck_product_family_result_family"),
    )
    for column in ("project_id", "execution_id", "stage_execution_id"):
        op.create_index(f"ix_product_family_result_{column}", "product_family_result", [column])

    op.create_table(
        "product_family_artifact",
        sa.Column("artifact_id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("execution_id", sa.String(36), sa.ForeignKey("product_family_execution.execution_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("stage_execution_id", sa.String(36), sa.ForeignKey("product_family_stage_execution.stage_execution_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("result_id", sa.String(36), sa.ForeignKey("product_family_result.result_id", ondelete="RESTRICT")),
        sa.Column("family", sa.String(20), nullable=False),
        sa.Column("artifact_type", sa.String(100), nullable=False),
        sa.Column("schema_version", sa.String(100), nullable=False),
        sa.Column("media_type", sa.String(100), nullable=False),
        sa.Column("object_key", sa.Text(), nullable=False, unique=True),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("size_bytes", sa.BigInteger(), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("family IN ('EXPLORATORY','CAUSAL','PREDICTIVE')", name="ck_product_family_artifact_family"),
        sa.CheckConstraint("size_bytes >= 0", name="ck_product_family_artifact_size"),
    )
    for column in ("project_id", "execution_id", "stage_execution_id", "result_id"):
        op.create_index(f"ix_product_family_artifact_{column}", "product_family_artifact", [column])

    op.create_table(
        "product_lineage_edge",
        sa.Column("lineage_edge_id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("source_type", sa.String(100), nullable=False),
        sa.Column("source_id", sa.String(100), nullable=False),
        sa.Column("relation_type", sa.String(100), nullable=False),
        sa.Column("target_type", sa.String(100), nullable=False),
        sa.Column("target_id", sa.String(100), nullable=False),
        sa.Column("evidence_json", sa.JSON(), nullable=False),
        sa.Column("created_by", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("source_type", "source_id", "relation_type", "target_type", "target_id", name="uq_product_lineage_edge"),
    )
    op.create_index("ix_product_lineage_edge_project_id", "product_lineage_edge", ["project_id"])


def downgrade() -> None:
    for table in (
        "product_lineage_edge",
        "product_family_artifact",
        "product_family_result",
        "product_family_stage_execution",
        "product_family_execution",
        "product_execution_plan",
        "product_analysis_view",
    ):
        op.drop_table(table)
