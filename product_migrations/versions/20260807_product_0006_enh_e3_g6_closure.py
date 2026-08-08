"""ENH-E3 G6 workspace closure, annotations, access, and export bundles.

Revision ID: 20260807_product_0006
Revises: 20260807_product_0005
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260807_product_0006"
down_revision = "20260807_product_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "product_project_membership",
        sa.Column("membership_id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("user_id", sa.String(200), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("project_id", "user_id", name="uq_product_project_membership"),
        sa.CheckConstraint("role IN ('OWNER','EDITOR','VIEWER')", name="ck_product_project_membership_role"),
    )
    op.create_index("ix_product_project_membership_project_id", "product_project_membership", ["project_id"])
    op.execute(
        "INSERT INTO product_project_membership "
        "(membership_id, project_id, user_id, role, created_at) "
        "SELECT project_id, project_id, 'anonymous', 'OWNER', created_at FROM product_project"
    )

    op.create_table(
        "product_workspace_selection",
        sa.Column("workspace_selection_id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("user_id", sa.String(200), nullable=False),
        sa.Column("research_context_version_id", sa.String(36), sa.ForeignKey("product_research_context_version.research_context_version_id", ondelete="RESTRICT")),
        sa.Column("dataset_version_id", sa.String(36), sa.ForeignKey("product_dataset_version.dataset_version_id", ondelete="RESTRICT")),
        sa.Column("analysis_view_id", sa.String(36), sa.ForeignKey("product_analysis_view.analysis_view_id", ondelete="RESTRICT")),
        sa.Column("unsaved_draft", sa.Boolean(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("project_id", "user_id", name="uq_product_workspace_selection"),
    )
    op.create_index("ix_product_workspace_selection_project_id", "product_workspace_selection", ["project_id"])

    op.create_table(
        "product_workspace_annotation",
        sa.Column("annotation_id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("target_type", sa.String(100), nullable=False),
        sa.Column("target_id", sa.String(100), nullable=False),
        sa.Column("statement", sa.Text(), nullable=False),
        sa.Column("rationale", sa.Text()),
        sa.Column("assumptions_json", sa.JSON(), nullable=False),
        sa.Column("limitations_json", sa.JSON(), nullable=False),
        sa.Column("decision", sa.String(20)),
        sa.Column("next_actions_json", sa.JSON(), nullable=False),
        sa.Column("revision_history_json", sa.JSON(), nullable=False),
        sa.Column("created_by", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "target_type IN ('Project','ResearchContextVersion','AnalysisView','AnalysisSpecification','Execution','Result','GraphVersion')",
            name="ck_product_workspace_annotation_target_type",
        ),
        sa.CheckConstraint("decision IS NULL OR decision IN ('SELECTED','REJECTED','DEFERRED')", name="ck_product_workspace_annotation_decision"),
    )
    op.create_index("ix_product_workspace_annotation_project_id", "product_workspace_annotation", ["project_id"])
    op.create_index("ix_product_workspace_annotation_target_id", "product_workspace_annotation", ["target_id"])

    op.create_table(
        "product_export_bundle",
        sa.Column("export_id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("schema_version", sa.String(100), nullable=False),
        sa.Column("result_ids_json", sa.JSON(), nullable=False),
        sa.Column("object_key", sa.Text(), nullable=False, unique=True),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("media_type", sa.String(100), nullable=False),
        sa.Column("size_bytes", sa.BigInteger(), nullable=False),
        sa.Column("manifest_summary_json", sa.JSON(), nullable=False),
        sa.Column("created_by", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("size_bytes >= 0", name="ck_product_export_bundle_size"),
    )
    op.create_index("ix_product_export_bundle_project_id", "product_export_bundle", ["project_id"])


def downgrade() -> None:
    op.drop_table("product_export_bundle")
    op.drop_table("product_workspace_annotation")
    op.drop_table("product_workspace_selection")
    op.drop_table("product_project_membership")
