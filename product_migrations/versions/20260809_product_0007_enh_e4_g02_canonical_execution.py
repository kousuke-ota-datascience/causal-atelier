"""ENH-E4 G02 canonical Execution discriminator and lease contract."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260809_product_0007"
down_revision = "20260807_product_0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "product_execution",
        sa.Column("analysis_family", sa.String(20), nullable=False, server_default="CAUSAL"),
    )
    op.add_column(
        "product_execution",
        sa.Column("base_execution_id", sa.String(36), nullable=True),
    )
    op.add_column(
        "product_execution",
        sa.Column("revision_kind", sa.String(20), nullable=True),
    )
    op.add_column(
        "product_execution",
        sa.Column("change_reason", sa.Text(), nullable=True),
    )
    op.add_column(
        "product_execution",
        sa.Column("lease_owner", sa.String(200), nullable=True),
    )
    op.add_column(
        "product_execution",
        sa.Column("lease_expires_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_product_execution_base_execution",
        "product_execution",
        "product_execution",
        ["base_execution_id"],
        ["execution_id"],
        ondelete="RESTRICT",
    )
    op.create_index(
        "ix_product_execution_analysis_family_status",
        "product_execution",
        ["analysis_family", "status", "requested_at"],
    )
    op.create_check_constraint(
        "ck_product_execution_analysis_family",
        "product_execution",
        "analysis_family IN ('CAUSAL','EXPLORATORY','PREDICTIVE')",
    )
    op.create_check_constraint(
        "ck_product_execution_revision_kind",
        "product_execution",
        "revision_kind IS NULL OR revision_kind IN ('RERUN','REVISED')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_product_execution_revision_kind", "product_execution", type_="check")
    op.drop_constraint("ck_product_execution_analysis_family", "product_execution", type_="check")
    op.drop_index("ix_product_execution_analysis_family_status", table_name="product_execution")
    op.drop_constraint("fk_product_execution_base_execution", "product_execution", type_="foreignkey")
    op.drop_column("product_execution", "lease_expires_at")
    op.drop_column("product_execution", "lease_owner")
    op.drop_column("product_execution", "change_reason")
    op.drop_column("product_execution", "revision_kind")
    op.drop_column("product_execution", "base_execution_id")
    op.drop_column("product_execution", "analysis_family")
