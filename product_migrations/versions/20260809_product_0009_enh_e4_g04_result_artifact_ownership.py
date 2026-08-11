"""ENH-E4 G04 canonical Result/Artifact ownership contract."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260809_product_0009"
down_revision = "20260809_product_0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_product_stage_execution_identity", "product_stage_execution",
        ["stage_execution_id", "execution_id"],
    )
    op.add_column("product_result", sa.Column("result_level", sa.String(30), nullable=False, server_default="EXECUTION_RESULT"))
    op.add_column("product_result", sa.Column("stage_execution_id", sa.String(36), nullable=True))
    op.create_unique_constraint("uq_product_result_execution_identity", "product_result", ["result_id", "execution_id"])
    op.create_check_constraint("ck_product_result_level", "product_result", "result_level IN ('EXECUTION_RESULT','STAGE_RESULT')")
    op.create_check_constraint(
        "ck_product_result_level_stage", "product_result",
        "(result_level = 'EXECUTION_RESULT' AND stage_execution_id IS NULL) OR "
        "(result_level = 'STAGE_RESULT' AND stage_execution_id IS NOT NULL)",
    )
    op.create_foreign_key(
        "fk_product_result_stage_execution", "product_result", "product_stage_execution",
        ["stage_execution_id", "execution_id"], ["stage_execution_id", "execution_id"], ondelete="RESTRICT",
    )
    op.create_index("ix_product_result_stage_execution_id", "product_result", ["stage_execution_id"])

    op.add_column("product_artifact", sa.Column("stage_execution_id", sa.String(36), nullable=True))
    op.add_column("product_artifact", sa.Column("artifact_scope", sa.String(30), nullable=False, server_default="SOURCE"))
    op.create_unique_constraint("uq_product_artifact_execution_identity", "product_artifact", ["artifact_id", "execution_id"])
    op.create_check_constraint("ck_product_artifact_scope", "product_artifact", "artifact_scope IN ('SOURCE','EXECUTION_OUTPUT')")
    op.create_check_constraint(
        "ck_product_artifact_scope_ownership", "product_artifact",
        "(artifact_scope = 'SOURCE' AND execution_id IS NULL AND stage_execution_id IS NULL AND result_id IS NULL) OR "
        "(artifact_scope = 'EXECUTION_OUTPUT' AND execution_id IS NOT NULL)",
    )
    op.create_foreign_key(
        "fk_product_artifact_stage_execution", "product_artifact", "product_stage_execution",
        ["stage_execution_id", "execution_id"], ["stage_execution_id", "execution_id"], ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_product_artifact_result_execution", "product_artifact", "product_result",
        ["result_id", "execution_id"], ["result_id", "execution_id"], ondelete="RESTRICT",
    )
    op.create_index("ix_product_artifact_stage_execution_id", "product_artifact", ["stage_execution_id"])


def downgrade() -> None:
    op.drop_index("ix_product_artifact_stage_execution_id", table_name="product_artifact")
    op.drop_constraint("fk_product_artifact_result_execution", "product_artifact", type_="foreignkey")
    op.drop_constraint("fk_product_artifact_stage_execution", "product_artifact", type_="foreignkey")
    op.drop_constraint("ck_product_artifact_scope_ownership", "product_artifact", type_="check")
    op.drop_constraint("ck_product_artifact_scope", "product_artifact", type_="check")
    op.drop_constraint("uq_product_artifact_execution_identity", "product_artifact", type_="unique")
    op.drop_column("product_artifact", "artifact_scope")
    op.drop_column("product_artifact", "stage_execution_id")
    op.drop_index("ix_product_result_stage_execution_id", table_name="product_result")
    op.drop_constraint("fk_product_result_stage_execution", "product_result", type_="foreignkey")
    op.drop_constraint("ck_product_result_level_stage", "product_result", type_="check")
    op.drop_constraint("ck_product_result_level", "product_result", type_="check")
    op.drop_constraint("uq_product_result_execution_identity", "product_result", type_="unique")
    op.drop_column("product_result", "stage_execution_id")
    op.drop_column("product_result", "result_level")
    op.drop_constraint("uq_product_stage_execution_identity", "product_stage_execution", type_="unique")
