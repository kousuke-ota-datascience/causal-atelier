"""ENH-E2 outcome inheritance for Graph Version.

Revision ID: 20260806_product_0003
Revises: 20260806_product_0002
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260806_product_0003"
down_revision = "20260806_product_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "product_graph_version",
        sa.Column("designated_outcome_node", sa.String(200), nullable=True),
    )
    op.create_index(
        "ix_product_graph_version_designated_outcome_node",
        "product_graph_version",
        ["designated_outcome_node"],
    )
    # Some long-lived ENH-E1 databases applied an early 0002 definition that
    # required input_result_id for every ESTIMATION.  Re-state the canonical
    # 0002 constraint so genuine pre-v2 rows remain readable while current v2
    # submissions still require an Identification Result.
    _replace_execution_input_constraint()


def downgrade() -> None:
    _replace_execution_input_constraint()
    op.drop_index(
        "ix_product_graph_version_designated_outcome_node",
        table_name="product_graph_version",
    )
    op.drop_column("product_graph_version", "designated_outcome_node")


def _replace_execution_input_constraint() -> None:
    op.drop_constraint(
        "ck_product_execution_input_by_operation",
        "product_execution",
        type_="check",
    )
    op.create_check_constraint(
        "ck_product_execution_input_by_operation",
        "product_execution",
        "(operation = 'DISCOVERY' AND input_graph_version_id IS NULL AND input_result_id IS NULL) OR "
        "(operation = 'IDENTIFICATION' AND input_graph_version_id IS NOT NULL AND input_result_id IS NULL) OR "
        "(operation = 'ESTIMATION' AND input_graph_version_id IS NOT NULL AND "
        "(input_result_id IS NOT NULL OR snapshot_schema_version = 'legacy-product-snapshot/1')) OR "
        "(operation IN ('REFUTATION','SENSITIVITY') AND input_graph_version_id IS NOT NULL AND input_result_id IS NOT NULL)",
    )
