"""ENH-E1 scientific validity foundation.

Revision ID: 20260806_product_0002
Revises: 20260805_product_0001
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260806_product_0002"
down_revision = "20260805_product_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "product_execution",
        sa.Column("input_result_id", sa.String(36), nullable=True),
    )
    op.add_column(
        "product_execution",
        sa.Column(
            "snapshot_schema_version",
            sa.String(100),
            nullable=False,
            server_default="causal-analysis-spec/2",
        ),
    )
    # Every row present while this migration runs was created under the v1
    # contract, which had no input_result_id and no identification-first gate.
    # Preserve that fact instead of fabricating an upstream Result reference.
    # The server default remains v2, so all executions created after the
    # migration are governed by the strict current constraint below.
    op.execute(
        "UPDATE product_execution "
        "SET snapshot_schema_version='legacy-product-snapshot/1'"
    )
    op.create_foreign_key(
        "fk_product_execution_input_result_id",
        "product_execution",
        "product_result",
        ["input_result_id"],
        ["result_id"],
        ondelete="RESTRICT",
    )
    op.create_index(
        "ix_product_execution_input_result_id", "product_execution", ["input_result_id"]
    )
    op.drop_constraint(
        "ck_product_execution_graph_by_operation", "product_execution", type_="check"
    )
    op.drop_constraint(
        "ck_product_execution_operation", "product_execution", type_="check"
    )
    op.create_check_constraint(
        "ck_product_execution_operation",
        "product_execution",
        "operation IN ('DISCOVERY','IDENTIFICATION','ESTIMATION','REFUTATION','SENSITIVITY')",
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

    op.drop_constraint("ck_product_result_type", "product_result", type_="check")
    op.drop_constraint("ck_product_result_scientific_status", "product_result", type_="check")
    op.execute("UPDATE product_result SET scientific_status='GENERATED' WHERE result_type='DISCOVERY_GRAPH_RESULT' AND scientific_status='VALID'")
    op.execute("UPDATE product_result SET scientific_status='ESTIMATED' WHERE result_type='TREATMENT_EFFECT_RESULT' AND scientific_status='VALID'")
    op.create_check_constraint(
        "ck_product_result_type",
        "product_result",
        "result_type IN ('DISCOVERY_GRAPH_RESULT','IDENTIFICATION_RESULT','DATA_ELIGIBILITY_RESULT','TREATMENT_EFFECT_RESULT','DIAGNOSTICS_RESULT','REFUTATION_RESULT','SENSITIVITY_RESULT')",
    )
    op.create_check_constraint(
        "ck_product_result_scientific_status",
        "product_result",
        "scientific_status IN ('GENERATED','GENERATED_WITH_WARNINGS','UNRELIABLE','IDENTIFIED','NOT_IDENTIFIED','PARTIALLY_IDENTIFIED','REQUIRES_REVIEW','PASS','WARN','FAIL','ESTIMATED','INSUFFICIENT_OVERLAP','INSUFFICIENT_SAMPLE','ESTIMATION_UNRELIABLE','NO_FAILURE_DETECTED','FAILURE_DETECTED','INCONCLUSIVE','ROBUST','FRAGILE')",
    )
    op.create_check_constraint(
        "ck_product_result_status_matrix",
        "product_result",
        "(result_type = 'DISCOVERY_GRAPH_RESULT' AND scientific_status IN ('GENERATED','GENERATED_WITH_WARNINGS','UNRELIABLE')) OR "
        "(result_type = 'IDENTIFICATION_RESULT' AND scientific_status IN ('IDENTIFIED','NOT_IDENTIFIED','PARTIALLY_IDENTIFIED','REQUIRES_REVIEW')) OR "
        "(result_type IN ('DATA_ELIGIBILITY_RESULT','DIAGNOSTICS_RESULT') AND scientific_status IN ('PASS','WARN','FAIL')) OR "
        "(result_type = 'TREATMENT_EFFECT_RESULT' AND scientific_status IN ('ESTIMATED','INSUFFICIENT_OVERLAP','INSUFFICIENT_SAMPLE','ESTIMATION_UNRELIABLE','REQUIRES_REVIEW')) OR "
        "(result_type = 'REFUTATION_RESULT' AND scientific_status IN ('NO_FAILURE_DETECTED','FAILURE_DETECTED','INCONCLUSIVE')) OR "
        "(result_type = 'SENSITIVITY_RESULT' AND scientific_status IN ('ROBUST','FRAGILE','INCONCLUSIVE'))",
    )

    op.add_column(
        "product_graph_version",
        sa.Column("graph_origin", sa.String(40), nullable=False, server_default="DISCOVERED"),
    )
    op.add_column(
        "product_graph_version",
        sa.Column("provenance_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
    )
    op.alter_column("product_graph_version", "source_result_id", nullable=True)
    op.create_check_constraint(
        "ck_product_graph_origin",
        "product_graph_version",
        "graph_origin IN ('DISCOVERED','CONSTRAINT_ADJUSTED','USER_DEFINED','IMPORTED','USER_EDITED')",
    )
    op.create_check_constraint(
        "ck_product_graph_origin_references",
        "product_graph_version",
        "(graph_origin = 'DISCOVERED' AND source_result_id IS NOT NULL) OR "
        "(graph_origin = 'CONSTRAINT_ADJUSTED' AND (source_result_id IS NOT NULL OR parent_graph_version_id IS NOT NULL)) OR "
        "(graph_origin IN ('USER_DEFINED','IMPORTED') AND source_result_id IS NULL AND parent_graph_version_id IS NULL) OR "
        "(graph_origin = 'USER_EDITED' AND source_result_id IS NULL AND parent_graph_version_id IS NOT NULL)",
    )

    op.drop_constraint("ck_product_artifact_type", "product_artifact", type_="check")
    op.create_check_constraint(
        "ck_product_artifact_type",
        "product_artifact",
        "artifact_type IN ('DATASET_FILE','GRAPH_JSON','GRAPH_IMAGE','EFFECT_TABLE','DIAGNOSTICS_TABLE','MANIFEST','CONFIG_SNAPSHOT','LOG','SCIENTIFIC_RESULT_JSON','SCIENTIFIC_REPORT')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_product_artifact_type", "product_artifact", type_="check")
    op.create_check_constraint(
        "ck_product_artifact_type",
        "product_artifact",
        "artifact_type IN ('DATASET_FILE','GRAPH_JSON','GRAPH_IMAGE','EFFECT_TABLE','DIAGNOSTICS_TABLE','MANIFEST','CONFIG_SNAPSHOT','LOG')",
    )
    op.drop_constraint("ck_product_graph_origin_references", "product_graph_version", type_="check")
    op.drop_constraint("ck_product_graph_origin", "product_graph_version", type_="check")
    op.alter_column("product_graph_version", "source_result_id", nullable=False)
    op.drop_column("product_graph_version", "provenance_json")
    op.drop_column("product_graph_version", "graph_origin")
    op.drop_constraint("ck_product_result_status_matrix", "product_result", type_="check")
    op.drop_constraint("ck_product_result_scientific_status", "product_result", type_="check")
    op.drop_constraint("ck_product_result_type", "product_result", type_="check")
    op.create_check_constraint(
        "ck_product_result_type",
        "product_result",
        "result_type IN ('DISCOVERY_GRAPH_RESULT','IDENTIFICATION_RESULT','TREATMENT_EFFECT_RESULT')",
    )
    op.create_check_constraint(
        "ck_product_result_scientific_status",
        "product_result",
        "scientific_status IN ('VALID','NOT_IDENTIFIED','INSUFFICIENT_OVERLAP','INSUFFICIENT_SAMPLE','ESTIMATION_UNRELIABLE')",
    )
    op.drop_constraint("ck_product_execution_input_by_operation", "product_execution", type_="check")
    op.drop_constraint("ck_product_execution_operation", "product_execution", type_="check")
    op.create_check_constraint(
        "ck_product_execution_operation", "product_execution", "operation IN ('DISCOVERY','ESTIMATION')"
    )
    op.create_check_constraint(
        "ck_product_execution_graph_by_operation",
        "product_execution",
        "(operation = 'DISCOVERY' AND input_graph_version_id IS NULL) OR (operation = 'ESTIMATION' AND input_graph_version_id IS NOT NULL)",
    )
    op.drop_index("ix_product_execution_input_result_id", table_name="product_execution")
    op.drop_constraint("fk_product_execution_input_result_id", "product_execution", type_="foreignkey")
    op.drop_column("product_execution", "snapshot_schema_version")
    op.drop_column("product_execution", "input_result_id")
