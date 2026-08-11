"""ENH-E4 G03 canonical persistent StageExecution and attempts."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260809_product_0008"
down_revision = "20260809_product_0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "product_stage_execution",
        sa.Column("stage_execution_id", sa.String(36), primary_key=True),
        sa.Column("execution_id", sa.String(36), sa.ForeignKey("product_execution.execution_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("stage_key", sa.String(100), nullable=False),
        sa.Column("stage_type_json", sa.JSON(), nullable=False),
        sa.Column("ordinal", sa.Integer(), nullable=False),
        sa.Column("dependencies_json", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(40), nullable=False),
        sa.Column("input_binding_json", sa.JSON(), nullable=False),
        sa.Column("output_binding_json", sa.JSON(), nullable=False),
        sa.Column("last_error_json", sa.JSON()),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("execution_id", "stage_key", name="uq_product_stage_execution_key"),
        sa.CheckConstraint("ordinal >= 0", name="ck_product_stage_execution_ordinal"),
        sa.CheckConstraint(
            "status IN ('PENDING','READY','RUNNING','SUCCEEDED','FAILED','SKIPPED_DUE_TO_PREREQUISITE','CANCELLED')",
            name="ck_product_stage_execution_status",
        ),
    )
    op.create_index("ix_product_stage_execution_execution_id", "product_stage_execution", ["execution_id"])
    op.create_table(
        "product_stage_attempt",
        sa.Column("stage_attempt_id", sa.String(36), primary_key=True),
        sa.Column("stage_execution_id", sa.String(36), sa.ForeignKey("product_stage_execution.stage_execution_id", ondelete="RESTRICT"), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("worker_id", sa.String(200), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column("error_json", sa.JSON()),
        sa.UniqueConstraint("stage_execution_id", "attempt_number", name="uq_product_stage_attempt_number"),
        sa.CheckConstraint("attempt_number > 0", name="ck_product_stage_attempt_number"),
    )
    op.create_index("ix_product_stage_attempt_stage_execution_id", "product_stage_attempt", ["stage_execution_id"])


def downgrade() -> None:
    op.drop_index("ix_product_stage_attempt_stage_execution_id", table_name="product_stage_attempt")
    op.drop_table("product_stage_attempt")
    op.drop_index("ix_product_stage_execution_execution_id", table_name="product_stage_execution")
    op.drop_table("product_stage_execution")
