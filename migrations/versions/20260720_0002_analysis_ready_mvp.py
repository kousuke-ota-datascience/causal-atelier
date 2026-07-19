"""Add the analysis-ready Web MVP metadata and saved graph resources."""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

from causal_atelier.domain import metadata as m


revision = "20260720_0002"
down_revision = "20260719_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    for model in (
        m.AnalysisDatasetBinding,
        m.FeatureSemanticsDatasetBinding,
        m.StageRunInputPreparation,
        m.StageAttemptInputPreparation,
        m.CausalGraph,
        m.CausalGraphVersion,
        m.CausalGraphNode,
        m.CausalGraphEdge,
        m.StageRunGraphInput,
    ):
        model.__table__.create(bind=bind, checkfirst=True)

    _add("pipeline_stage_definition", sa.Column("input_mode", sa.String(32)))
    _add(
        "stage_run",
        sa.Column(
            "input_mode",
            sa.String(32),
            nullable=False,
            server_default="CONFIGURED_FEATURE_BUILD",
        ),
    )
    for column in (
        sa.Column("dataset_column_id", sa.String(36)),
        sa.Column("categorical", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column(
            "allowed_for_discovery", sa.Boolean(), nullable=False, server_default=sa.true()
        ),
        sa.Column(
            "time_metadata_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")
        ),
        sa.Column("description", sa.Text()),
    ):
        _add("feature_semantic_item", column)
    for column in (
        sa.Column("dataset_version_id", sa.String(36)),
        sa.Column("causal_graph_version_id", sa.String(36)),
        sa.Column("target_population", sa.Text()),
        sa.Column("adjustment_strategy", sa.String(64)),
        sa.Column(
            "adjustment_set_json", sa.JSON(), nullable=False, server_default=sa.text("'[]'")
        ),
        sa.Column("analyst_note", sa.Text()),
    ):
        _add("causal_design_projection", column)
    for table in ("discovery_result", "edge_weight_result", "treatment_effect_result"):
        _add(
            table,
            sa.Column(
                "input_mode",
                sa.String(32),
                nullable=False,
                server_default="CONFIGURED_FEATURE_BUILD",
            ),
        )
        _add(table, sa.Column("input_preparation_attempt_id", sa.String(36)))
    _add("discovery_result", sa.Column("feature_semantics_version_id", sa.String(36)))
    _add("edge_weight_result", sa.Column("feature_semantics_version_id", sa.String(36)))
    _add("edge_weight_result", sa.Column("causal_graph_version_id", sa.String(36)))
    _add("treatment_effect_result", sa.Column("causal_graph_version_id", sa.String(36)))

    # The initial migration imports current metadata. These guards make a fresh
    # install and an upgrade from the v1 schema converge on the same result.
    if bind.dialect.name == "postgresql":
        op.alter_column("discovery_result", "discovery_feature_version_id", nullable=True)
        op.alter_column("edge_weight_result", "inference_feature_version_id", nullable=True)
        op.alter_column(
            "treatment_effect_result", "inference_feature_version_id", nullable=True
        )
        op.execute(
            """
            CREATE OR REPLACE FUNCTION causal_atelier_protect_published_graph()
            RETURNS trigger AS $$
            BEGIN
              IF OLD.status IN ('PUBLISHED', 'DEPRECATED') AND
                 (NEW.canonical_json, NEW.content_hash, NEW.causal_graph_id,
                  NEW.version_number, NEW.dataset_version_id,
                  NEW.feature_semantics_version_id) IS DISTINCT FROM
                 (OLD.canonical_json, OLD.content_hash, OLD.causal_graph_id,
                  OLD.version_number, OLD.dataset_version_id,
                  OLD.feature_semantics_version_id) THEN
                RAISE EXCEPTION 'published causal graph version is immutable';
              END IF;
              RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            DROP TRIGGER IF EXISTS trg_causal_graph_version_immutable
              ON causal_graph_version;
            CREATE TRIGGER trg_causal_graph_version_immutable
              BEFORE UPDATE ON causal_graph_version
              FOR EACH ROW EXECUTE FUNCTION causal_atelier_protect_published_graph();
            """
        )


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute(
            "DROP FUNCTION IF EXISTS causal_atelier_protect_published_graph() CASCADE"
        )
    for table in (
        "stage_run_graph_input",
        "causal_graph_edge",
        "causal_graph_node",
        "causal_graph_version",
        "causal_graph",
        "stage_attempt_input_preparation",
        "stage_run_input_preparation",
        "feature_semantics_dataset_binding",
        "analysis_dataset_binding",
    ):
        if table in inspect(bind).get_table_names():
            op.drop_table(table)


def _add(table_name: str, column: sa.Column) -> None:
    columns = {item["name"] for item in inspect(op.get_bind()).get_columns(table_name)}
    if column.name not in columns:
        op.add_column(table_name, column)

