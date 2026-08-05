"""Add the analysis-ready Web MVP metadata and saved causal-graph resources.

Schema frozen at revision 20260720_0002.  No ORM imports — all DDL is explicit.

Tables added:
  analysis_dataset_binding, feature_semantics_dataset_binding,
  causal_graph, causal_graph_version, causal_graph_node, causal_graph_edge,
  stage_run_graph_input (Run-era name; renamed stage_execution_graph_input by 0003).

Columns added to existing tables: see inline comments.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260720_0002"
down_revision = "20260719_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    is_pg = bind.dialect.name == "postgresql"

    # ── New tables ────────────────────────────────────────────────────────────
    op.create_table(
        "analysis_dataset_binding",
        sa.Column("dataset_version_id", sa.String(36),
                  sa.ForeignKey("dataset_version.id",
                                name="fk_adb_dataset_version"),
                  primary_key=True),
        sa.Column("primary_table_version_id", sa.String(36),
                  sa.ForeignKey("dataset_table_version.id",
                                name="fk_adb_primary_dtv"),
                  nullable=False),
        sa.Column("analysis_unit_description", sa.Text, nullable=False),
        sa.Column("unit_identifier_column_id", sa.String(36),
                  sa.ForeignKey("dataset_column.id",
                                name="fk_adb_unit_identifier_column")),
        sa.Column("readiness_status", sa.String(32), nullable=False,
                  server_default="UNKNOWN"),
        sa.Column("schema_hash_snapshot", sa.String(255), nullable=False),
        sa.Column("validation_summary_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'") ),
        sa.Column("created_by", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_adb_created_by"),
                  nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("validated_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("primary_table_version_id",
                            name="uq_adb_primary_dtv"),
    )

    op.create_table(
        "feature_semantics_dataset_binding",
        sa.Column("configuration_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id",
                                name="fk_fsdb_cv"),
                  primary_key=True),
        sa.Column("dataset_version_id", sa.String(36),
                  sa.ForeignKey("dataset_version.id",
                                name="fk_fsdb_dataset_version"),
                  nullable=False),
        sa.Column("dataset_table_version_id", sa.String(36),
                  sa.ForeignKey("dataset_table_version.id",
                                name="fk_fsdb_dtv"),
                  nullable=False),
        sa.Column("dataset_schema_hash_snapshot", sa.String(255), nullable=False),
        sa.Column("binding_status", sa.String(32), nullable=False,
                  server_default="VALID"),
        sa.Column("validation_summary_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'") ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("validated_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_fsdb_dataset_version_id",
                    "feature_semantics_dataset_binding", ["dataset_version_id"])

    op.create_table(
        "causal_graph",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36),
                  sa.ForeignKey("project.id", name="fk_causal_graph_project"),
                  nullable=False),
        sa.Column("slug", sa.String(255), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("created_by", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_causal_graph_created_by"),
                  nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("project_id", "slug",
                            name="uq_causal_graph_project_slug"),
    )
    op.create_index("ix_causal_graph_project_id", "causal_graph", ["project_id"])

    op.create_table(
        "causal_graph_version",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("causal_graph_id", sa.String(36),
                  sa.ForeignKey("causal_graph.id",
                                name="fk_causal_graph_version_graph"),
                  nullable=False),
        sa.Column("version_number", sa.Integer, nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="DRAFT"),
        sa.Column("source_discovery_algorithm_result_id", sa.String(36),
                  sa.ForeignKey("discovery_algorithm_result.id",
                                name="fk_cgv_source_dar"),
                  nullable=False),
        sa.Column("dataset_version_id", sa.String(36),
                  sa.ForeignKey("dataset_version.id",
                                name="fk_cgv_dataset_version"),
                  nullable=False),
        sa.Column("feature_semantics_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id",
                                name="fk_cgv_feature_semantics_cv"),
                  nullable=False),
        sa.Column("algorithm", sa.String(64), nullable=False),
        sa.Column("algorithm_parameter_hash", sa.String(255)),
        sa.Column("node_count", sa.Integer, nullable=False),
        sa.Column("edge_count", sa.Integer, nullable=False),
        sa.Column("canonical_json", sa.JSON, nullable=False),
        sa.Column("content_hash", sa.String(255), nullable=False),
        sa.Column("graph_artifact_id", sa.String(36),
                  sa.ForeignKey("artifact.id", name="fk_cgv_graph_artifact"),
                  nullable=False),
        sa.Column("selection_note", sa.Text),
        sa.Column("created_by", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_cgv_created_by"),
                  nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("validated_at", sa.DateTime(timezone=True)),
        sa.Column("published_by", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_cgv_published_by")),
        sa.Column("published_at", sa.DateTime(timezone=True)),
        sa.Column("supersedes_version_id", sa.String(36),
                  sa.ForeignKey("causal_graph_version.id",
                                name="fk_cgv_supersedes")),
        sa.UniqueConstraint("causal_graph_id", "version_number",
                            name="uq_cgv_graph_number"),
        sa.UniqueConstraint("causal_graph_id", "content_hash",
                            name="uq_cgv_graph_hash"),
        sa.CheckConstraint("version_number >= 1", name="ck_graph_version_number"),
        sa.CheckConstraint("node_count >= 0", name="ck_graph_node_count"),
        sa.CheckConstraint("edge_count >= 0", name="ck_graph_edge_count"),
    )
    op.create_index("ix_causal_graph_version_graph_id",
                    "causal_graph_version", ["causal_graph_id"])

    op.create_table(
        "causal_graph_node",
        sa.Column("causal_graph_version_id", sa.String(36),
                  sa.ForeignKey("causal_graph_version.id",
                                name="fk_causal_graph_node_version"),
                  primary_key=True),
        sa.Column("name", sa.String(255), primary_key=True),
        sa.Column("ordinal", sa.Integer, nullable=False),
        sa.Column("role_snapshot", sa.String(32)),
        sa.Column("metadata_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'") ),
        sa.UniqueConstraint("causal_graph_version_id", "ordinal",
                            name="uq_cgn_version_ordinal"),
    )

    op.create_table(
        "causal_graph_edge",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("causal_graph_version_id", sa.String(36),
                  sa.ForeignKey("causal_graph_version.id",
                                name="fk_causal_graph_edge_version"),
                  nullable=False),
        sa.Column("node_a", sa.String(255), nullable=False),
        sa.Column("node_b", sa.String(255), nullable=False),
        sa.Column("endpoint_at_a", sa.String(16), nullable=False),
        sa.Column("endpoint_at_b", sa.String(16), nullable=False),
        sa.Column("score", sa.Float),
        sa.Column("stability", sa.Float),
        sa.Column("source_discovery_edge_id", sa.String(36),
                  sa.ForeignKey("discovery_edge.id",
                                name="fk_causal_graph_edge_discovery_edge")),
        sa.Column("payload_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'") ),
        sa.UniqueConstraint("causal_graph_version_id", "node_a", "node_b",
                            name="uq_cge_version_nodes"),
        sa.CheckConstraint("node_a < node_b", name="ck_graph_edge_node_order"),
        sa.CheckConstraint(
            "endpoint_at_a IN ('TAIL', 'ARROW', 'CIRCLE')",
            name="ck_graph_endpoint_a",
        ),
        sa.CheckConstraint(
            "endpoint_at_b IN ('TAIL', 'ARROW', 'CIRCLE')",
            name="ck_graph_endpoint_b",
        ),
    )
    op.create_index("ix_causal_graph_edge_version_id",
                    "causal_graph_edge", ["causal_graph_version_id"])

    # Table renamed stage_run_graph_input→stage_execution_graph_input by 0003.
    # Column stage_run_id→stage_execution_id renamed by 0003.
    op.create_table(
        "stage_run_graph_input",
        sa.Column("stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id", name="fk_srgi_stage_run"),
                  primary_key=True),
        sa.Column("input_name", sa.String(255), primary_key=True),
        sa.Column("causal_graph_version_id", sa.String(36),
                  sa.ForeignKey("causal_graph_version.id",
                                name="fk_srgi_causal_graph_version"),
                  nullable=False),
        sa.Column("content_hash_snapshot", sa.String(255), nullable=False),
        sa.Column("source", sa.String(32), nullable=False,
                  server_default="API_OVERRIDE"),
    )

    # ── Columns added to existing tables ──────────────────────────────────────

    # pipeline_stage_definition: add input_mode
    op.add_column(
        "pipeline_stage_definition",
        sa.Column("input_mode", sa.String(32)),
    )

    # stage_run: add input_mode (NOT NULL with server_default for backfill)
    op.add_column(
        "stage_run",
        sa.Column("input_mode", sa.String(32), nullable=False,
                  server_default="CONFIGURED_FEATURE_BUILD"),
    )

    # feature_semantic_item: add 5 columns
    op.add_column(
        "feature_semantic_item",
        sa.Column("dataset_column_id", sa.String(36)),
    )
    op.add_column(
        "feature_semantic_item",
        sa.Column("categorical", sa.Boolean, nullable=False,
                  server_default=sa.false()),
    )
    op.add_column(
        "feature_semantic_item",
        sa.Column("allowed_for_discovery", sa.Boolean, nullable=False,
                  server_default=sa.true()),
    )
    op.add_column(
        "feature_semantic_item",
        sa.Column("time_metadata_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'") ),
    )
    op.add_column(
        "feature_semantic_item",
        sa.Column("description", sa.Text),
    )
    # Add FK for dataset_column_id
    if is_pg:
        op.create_foreign_key(
            "fk_fsi_dataset_column",
            "feature_semantic_item", "dataset_column",
            ["dataset_column_id"], ["id"],
        )

    # causal_design_projection: add 6 columns
    op.add_column(
        "causal_design_projection",
        sa.Column("dataset_version_id", sa.String(36)),
    )
    op.add_column(
        "causal_design_projection",
        sa.Column("causal_graph_version_id", sa.String(36)),
    )
    op.add_column(
        "causal_design_projection",
        sa.Column("target_population", sa.Text),
    )
    op.add_column(
        "causal_design_projection",
        sa.Column("adjustment_strategy", sa.String(64)),
    )
    op.add_column(
        "causal_design_projection",
        sa.Column("adjustment_set_json", sa.JSON, nullable=False,
                  server_default=sa.text("'[]'") ),
    )
    op.add_column(
        "causal_design_projection",
        sa.Column("analyst_note", sa.Text),
    )
    if is_pg:
        op.create_foreign_key(
            "fk_cdp_dataset_version",
            "causal_design_projection", "dataset_version",
            ["dataset_version_id"], ["id"],
        )
        op.create_foreign_key(
            "fk_cdp_causal_graph_version",
            "causal_design_projection", "causal_graph_version",
            ["causal_graph_version_id"], ["id"],
        )

    # discovery_result: add 4 columns + make discovery_feature_version_id nullable
    op.add_column(
        "discovery_result",
        sa.Column("input_mode", sa.String(32), nullable=False,
                  server_default="CONFIGURED_FEATURE_BUILD"),
    )
    op.add_column(
        "discovery_result",
        sa.Column("feature_semantics_version_id", sa.String(36)),
    )
    op.add_column(
        "discovery_result",
        sa.Column("input_preparation_attempt_id", sa.String(36)),
    )
    op.add_column(
        "discovery_result",
        sa.Column("resolved_semantics_artifact_id", sa.String(36)),
    )
    if is_pg:
        op.alter_column("discovery_result", "discovery_feature_version_id",
                        nullable=True)
        op.create_foreign_key(
            "fk_dr_feature_semantics_cv",
            "discovery_result", "configuration_version",
            ["feature_semantics_version_id"], ["id"],
        )
        op.create_foreign_key(
            "fk_dr_input_preparation_attempt",
            "discovery_result", "stage_attempt_input_preparation",
            ["input_preparation_attempt_id"], ["stage_attempt_id"],
        )
        op.create_foreign_key(
            "fk_dr_resolved_semantics_artifact",
            "discovery_result", "artifact",
            ["resolved_semantics_artifact_id"], ["id"],
        )

    # edge_weight_result: add 4 columns + make inference_feature_version_id nullable
    op.add_column(
        "edge_weight_result",
        sa.Column("input_mode", sa.String(32), nullable=False,
                  server_default="CONFIGURED_FEATURE_BUILD"),
    )
    op.add_column(
        "edge_weight_result",
        sa.Column("feature_semantics_version_id", sa.String(36)),
    )
    op.add_column(
        "edge_weight_result",
        sa.Column("causal_graph_version_id", sa.String(36)),
    )
    op.add_column(
        "edge_weight_result",
        sa.Column("input_preparation_attempt_id", sa.String(36)),
    )
    if is_pg:
        op.alter_column("edge_weight_result", "inference_feature_version_id",
                        nullable=True)
        op.create_index("ix_ewr_causal_graph_version_id",
                        "edge_weight_result", ["causal_graph_version_id"])
        op.create_foreign_key(
            "fk_ewr_feature_semantics_cv",
            "edge_weight_result", "configuration_version",
            ["feature_semantics_version_id"], ["id"],
        )
        op.create_foreign_key(
            "fk_ewr_causal_graph_version",
            "edge_weight_result", "causal_graph_version",
            ["causal_graph_version_id"], ["id"],
        )
        op.create_foreign_key(
            "fk_ewr_input_preparation_attempt",
            "edge_weight_result", "stage_attempt_input_preparation",
            ["input_preparation_attempt_id"], ["stage_attempt_id"],
        )

    # treatment_effect_result: add 3 columns + make inference_feature_version_id nullable
    op.add_column(
        "treatment_effect_result",
        sa.Column("input_mode", sa.String(32), nullable=False,
                  server_default="CONFIGURED_FEATURE_BUILD"),
    )
    op.add_column(
        "treatment_effect_result",
        sa.Column("causal_graph_version_id", sa.String(36)),
    )
    op.add_column(
        "treatment_effect_result",
        sa.Column("input_preparation_attempt_id", sa.String(36)),
    )
    if is_pg:
        op.alter_column("treatment_effect_result", "inference_feature_version_id",
                        nullable=True)
        op.create_index("ix_ter_causal_graph_version_id",
                        "treatment_effect_result", ["causal_graph_version_id"])
        op.create_foreign_key(
            "fk_ter_causal_graph_version",
            "treatment_effect_result", "causal_graph_version",
            ["causal_graph_version_id"], ["id"],
        )
        op.create_foreign_key(
            "fk_ter_input_preparation_attempt",
            "treatment_effect_result", "stage_attempt_input_preparation",
            ["input_preparation_attempt_id"], ["stage_attempt_id"],
        )

    # ── PostgreSQL: causal_graph_version immutability trigger ─────────────────
    if is_pg:
        op.execute(
            """
            CREATE OR REPLACE FUNCTION ariadne_protect_published_graph()
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
              FOR EACH ROW EXECUTE FUNCTION ariadne_protect_published_graph();
            """
        )


def downgrade() -> None:
    bind = op.get_bind()
    is_pg = bind.dialect.name == "postgresql"

    if is_pg:
        op.execute(
            "DROP TRIGGER IF EXISTS trg_causal_graph_version_immutable"
            " ON causal_graph_version"
        )
        op.execute(
            "DROP FUNCTION IF EXISTS ariadne_protect_published_graph() CASCADE"
        )

    # Remove FK constraints added in upgrade (PostgreSQL only)
    if is_pg:
        for constraint, table in [
            ("fk_ter_input_preparation_attempt", "treatment_effect_result"),
            ("fk_ter_causal_graph_version", "treatment_effect_result"),
            ("fk_ewr_input_preparation_attempt", "edge_weight_result"),
            ("fk_ewr_causal_graph_version", "edge_weight_result"),
            ("fk_ewr_feature_semantics_cv", "edge_weight_result"),
            ("fk_dr_resolved_semantics_artifact", "discovery_result"),
            ("fk_dr_input_preparation_attempt", "discovery_result"),
            ("fk_dr_feature_semantics_cv", "discovery_result"),
            ("fk_cdp_causal_graph_version", "causal_design_projection"),
            ("fk_cdp_dataset_version", "causal_design_projection"),
            ("fk_fsi_dataset_column", "feature_semantic_item"),
        ]:
            op.drop_constraint(constraint, table, type_="foreignkey")

        op.drop_index("ix_ter_causal_graph_version_id",
                      table_name="treatment_effect_result")
        op.drop_index("ix_ewr_causal_graph_version_id",
                      table_name="edge_weight_result")

        # Restore NOT NULL on columns that were made nullable in upgrade
        op.alter_column("treatment_effect_result", "inference_feature_version_id",
                        nullable=False)
        op.alter_column("edge_weight_result", "inference_feature_version_id",
                        nullable=False)
        op.alter_column("discovery_result", "discovery_feature_version_id",
                        nullable=False)

    # Drop added columns (use batch for SQLite compatibility)
    for col in ["input_preparation_attempt_id", "causal_graph_version_id",
                "input_mode"]:
        with op.batch_alter_table("treatment_effect_result") as batch:
            batch.drop_column(col)
    for col in ["input_preparation_attempt_id", "causal_graph_version_id",
                "feature_semantics_version_id", "input_mode"]:
        with op.batch_alter_table("edge_weight_result") as batch:
            batch.drop_column(col)
    for col in ["resolved_semantics_artifact_id", "input_preparation_attempt_id",
                "feature_semantics_version_id", "input_mode"]:
        with op.batch_alter_table("discovery_result") as batch:
            batch.drop_column(col)
    for col in ["analyst_note", "adjustment_set_json", "adjustment_strategy",
                "target_population", "causal_graph_version_id", "dataset_version_id"]:
        with op.batch_alter_table("causal_design_projection") as batch:
            batch.drop_column(col)
    for col in ["description", "time_metadata_json", "allowed_for_discovery",
                "categorical", "dataset_column_id"]:
        with op.batch_alter_table("feature_semantic_item") as batch:
            batch.drop_column(col)
    with op.batch_alter_table("stage_run") as batch:
        batch.drop_column("input_mode")
    with op.batch_alter_table("pipeline_stage_definition") as batch:
        batch.drop_column("input_mode")

    # Drop tables added in upgrade (children before parents)
    op.drop_table("stage_run_graph_input")
    op.drop_table("causal_graph_edge")
    op.drop_table("causal_graph_node")
    op.drop_table("causal_graph_version")
    op.drop_table("causal_graph")
    op.drop_table("feature_semantics_dataset_binding")
    op.drop_table("analysis_dataset_binding")
