"""Create the v1 metadata, lineage, result, and visualization schema.

Schema frozen at revision 20260719_0001.  No ORM imports — all DDL is
explicit so that future ORM changes cannot alter the result of applying this
revision against an empty database.

Run-era table/column names are used exactly as they existed when this
revision was authored.  Revision 0002 adds the analysis-ready and causal-graph
tables; revision 0003 renames Run→Execution.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260719_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── Identity & access ────────────────────────────────────────────────────
    op.create_table(
        "app_user",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("identity_provider", sa.String(64), nullable=False),
        sa.Column("external_subject", sa.String(255), nullable=False),
        sa.Column("email", sa.String(320)),
        sa.Column("display_name", sa.String(255), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("identity_provider", "external_subject",
                            name="uq_app_user_provider_subject"),
    )
    op.create_table(
        "role",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("code", sa.String(64), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("system_managed", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.UniqueConstraint("code", name="uq_role_code"),
    )
    op.create_table(
        "project",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("slug", sa.String(255), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("status", sa.String(32), nullable=False, server_default="ACTIVE"),
        sa.Column("created_by", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_project_created_by"),
                  nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("slug", name="uq_project_slug"),
    )
    op.create_table(
        "project_member",
        sa.Column("project_id", sa.String(36),
                  sa.ForeignKey("project.id", name="fk_project_member_project"),
                  primary_key=True),
        sa.Column("user_id", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_project_member_user"),
                  primary_key=True),
        sa.Column("role_id", sa.String(36),
                  sa.ForeignKey("role.id", name="fk_project_member_role"),
                  nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # ── Storage ──────────────────────────────────────────────────────────────
    op.create_table(
        "stored_object",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("backend", sa.String(32), nullable=False, server_default="LOCAL"),
        sa.Column("bucket", sa.String(255)),
        sa.Column("object_key", sa.Text, nullable=False),
        sa.Column("object_version", sa.String(255), nullable=False, server_default=""),
        sa.Column("media_type", sa.String(255)),
        sa.Column("format", sa.String(32)),
        sa.Column("size_bytes", sa.BigInteger),
        sa.Column("checksum_algorithm", sa.String(32), nullable=False,
                  server_default="SHA256"),
        sa.Column("checksum", sa.String(255), nullable=False),
        sa.Column("encryption_metadata", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("status", sa.String(32), nullable=False, server_default="AVAILABLE"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("backend", "bucket", "object_key", "object_version",
                            name="uq_stored_object_location"),
    )

    # ── Dataset ──────────────────────────────────────────────────────────────
    op.create_table(
        "dataset",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36),
                  sa.ForeignKey("project.id", name="fk_dataset_project"),
                  nullable=False),
        sa.Column("slug", sa.String(255), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("dataset_kind", sa.String(32), nullable=False),
        sa.Column("created_by", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_dataset_created_by"),
                  nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("project_id", "slug", name="uq_dataset_project_slug"),
    )
    op.create_index("ix_dataset_project_id", "dataset", ["project_id"])

    # origin_stage_run_id FK is deferred (use_alter) — added after stage_run.
    op.create_table(
        "dataset_version",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("dataset_id", sa.String(36),
                  sa.ForeignKey("dataset.id", name="fk_dataset_version_dataset"),
                  nullable=False),
        sa.Column("version_number", sa.Integer, nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="REGISTERING"),
        sa.Column("source_type", sa.String(32), nullable=False),
        sa.Column("source_metadata", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("schema_hash", sa.String(255)),
        sa.Column("content_hash", sa.String(255)),
        sa.Column("table_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("origin_stage_run_id", sa.String(36)),
        sa.Column("created_by", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_dataset_version_created_by"),
                  nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ready_at", sa.DateTime(timezone=True)),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("dataset_id", "version_number",
                            name="uq_dataset_version_dataset_number"),
    )
    op.create_index("ix_dataset_version_dataset_id", "dataset_version", ["dataset_id"])

    op.create_table(
        "dataset_table_version",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("dataset_version_id", sa.String(36),
                  sa.ForeignKey("dataset_version.id",
                                name="fk_dtv_dataset_version"),
                  nullable=False),
        sa.Column("logical_name", sa.String(255), nullable=False),
        sa.Column("stored_object_id", sa.String(36),
                  sa.ForeignKey("stored_object.id", name="fk_dtv_stored_object"),
                  nullable=False),
        sa.Column("ordinal", sa.Integer, nullable=False),
        sa.Column("file_format", sa.String(32), nullable=False),
        sa.Column("row_count", sa.BigInteger),
        sa.Column("column_count", sa.Integer),
        sa.Column("schema_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("schema_hash", sa.String(255)),
        sa.Column("content_hash", sa.String(255), nullable=False),
        sa.Column("partition_values", sa.JSON),
        sa.Column("source_entry_name", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("dataset_version_id", "logical_name", name="uq_dtv_version_name"),
        sa.UniqueConstraint("dataset_version_id", "ordinal", name="uq_dtv_version_ordinal"),
    )
    op.create_index("ix_dtv_dataset_version_id",
                    "dataset_table_version", ["dataset_version_id"])

    op.create_table(
        "dataset_column",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("dataset_table_version_id", sa.String(36),
                  sa.ForeignKey("dataset_table_version.id",
                                name="fk_dataset_column_dtv"),
                  nullable=False),
        sa.Column("ordinal", sa.Integer, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("physical_type", sa.String(128), nullable=False),
        sa.Column("logical_type", sa.String(128)),
        sa.Column("nullable", sa.Boolean, nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("semantic_tags", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.UniqueConstraint("dataset_table_version_id", "name",
                            name="uq_dataset_column_dtv_name"),
        sa.UniqueConstraint("dataset_table_version_id", "ordinal",
                            name="uq_dataset_column_dtv_ordinal"),
    )
    op.create_index("ix_dataset_column_dtv", "dataset_column", ["dataset_table_version_id"])

    op.create_table(
        "dataset_column_policy",
        sa.Column("dataset_column_id", sa.String(36),
                  sa.ForeignKey("dataset_column.id",
                                name="fk_dataset_column_policy_column"),
                  primary_key=True),
        sa.Column("classification", sa.String(32), nullable=False,
                  server_default="INTERNAL"),
        sa.Column("preview_allowed", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("analysis_allowed", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("download_allowed", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("mask_rule", sa.String(64)),
        sa.Column("minimum_group_count", sa.Integer),
        sa.Column("updated_by", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_dcp_updated_by"),
                  nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # data_profile.artifact_id FK deferred — added after artifact table.
    op.create_table(
        "data_profile",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("dataset_table_version_id", sa.String(36),
                  sa.ForeignKey("dataset_table_version.id",
                                name="fk_data_profile_dtv"),
                  nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="PENDING"),
        sa.Column("profiler_name", sa.String(128), nullable=False,
                  server_default="ariadne"),
        sa.Column("profiler_version", sa.String(64), nullable=False, server_default="1"),
        sa.Column("sampled", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("sample_size", sa.BigInteger),
        sa.Column("summary_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("artifact_id", sa.String(36)),
        sa.Column("error_summary", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_data_profile_dtv",
                    "data_profile", ["dataset_table_version_id"])

    op.create_table(
        "column_profile",
        sa.Column("data_profile_id", sa.String(36),
                  sa.ForeignKey("data_profile.id",
                                name="fk_column_profile_data_profile"),
                  primary_key=True),
        sa.Column("dataset_column_id", sa.String(36),
                  sa.ForeignKey("dataset_column.id",
                                name="fk_column_profile_dataset_column"),
                  primary_key=True),
        sa.Column("null_count", sa.BigInteger),
        sa.Column("distinct_count", sa.BigInteger),
        sa.Column("min_value", sa.Text),
        sa.Column("max_value", sa.Text),
        sa.Column("statistics_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
    )

    # ── Configuration ─────────────────────────────────────────────────────────
    op.create_table(
        "configuration",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36),
                  sa.ForeignKey("project.id", name="fk_configuration_project"),
                  nullable=False),
        sa.Column("configuration_type", sa.String(64), nullable=False),
        sa.Column("slug", sa.String(255), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("created_by", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_configuration_created_by"),
                  nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("project_id", "configuration_type", "slug",
                            name="uq_configuration_project_type_slug"),
    )
    op.create_index("ix_configuration_project_id", "configuration", ["project_id"])

    op.create_table(
        "configuration_version",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("configuration_id", sa.String(36),
                  sa.ForeignKey("configuration.id",
                                name="fk_cv_configuration"),
                  nullable=False),
        sa.Column("version_number", sa.Integer, nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="DRAFT"),
        sa.Column("schema_version", sa.String(64), nullable=False, server_default="1"),
        sa.Column("canonical_json", sa.JSON, nullable=False),
        sa.Column("original_format", sa.String(16), nullable=False, server_default="YAML"),
        sa.Column("original_text", sa.Text),
        sa.Column("content_hash", sa.String(255), nullable=False),
        sa.Column("validation_status", sa.String(32), nullable=False,
                  server_default="UNKNOWN"),
        sa.Column("validation_summary", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("supersedes_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id", name="fk_cv_supersedes")),
        sa.Column("created_by", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_cv_created_by"),
                  nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("published_by", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_cv_published_by")),
        sa.Column("published_at", sa.DateTime(timezone=True)),
        sa.Column("lock_version", sa.Integer, nullable=False, server_default="1"),
        sa.UniqueConstraint("configuration_id", "version_number",
                            name="uq_cv_configuration_number"),
        sa.UniqueConstraint("configuration_id", "content_hash",
                            name="uq_cv_configuration_hash"),
    )
    op.create_index("ix_cv_configuration_id",
                    "configuration_version", ["configuration_id"])

    op.create_table(
        "configuration_dependency",
        sa.Column("source_configuration_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id", name="fk_cd_source"),
                  primary_key=True),
        sa.Column("dependency_name", sa.String(255), primary_key=True),
        sa.Column("target_configuration_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id", name="fk_cd_target"),
                  nullable=False),
        sa.Column("dependency_type", sa.String(32), nullable=False),
    )
    op.create_table(
        "feature_semantics_projection",
        sa.Column("configuration_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id", name="fk_fsp_cv"),
                  primary_key=True),
        sa.Column("default_unit_id", sa.String(255)),
        sa.Column("feature_count", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # v1 feature_semantic_item — without dataset_column_id, categorical,
    # allowed_for_discovery, time_metadata_json, description (added in 0002).
    op.create_table(
        "feature_semantic_item",
        sa.Column("feature_semantics_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id", name="fk_fsi_cv"),
                  primary_key=True),
        sa.Column("name", sa.String(255), primary_key=True),
        sa.Column("role", sa.String(32), nullable=False),
        sa.Column("source_table", sa.String(255), nullable=False),
        sa.Column("source_column", sa.String(255)),
        sa.Column("unit_id", sa.String(255), nullable=False),
        sa.Column("aggregation", sa.String(64)),
        sa.Column("transform", sa.String(128)),
        sa.Column("dtype", sa.String(128)),
        sa.Column("allowed_for_adjustment", sa.Boolean, nullable=False,
                  server_default=sa.false()),
        sa.Column("post_treatment", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("metadata_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
    )

    # v1 causal_design_projection — without dataset_version_id,
    # causal_graph_version_id, target_population, adjustment_strategy,
    # adjustment_set_json, analyst_note (added in 0002).
    op.create_table(
        "causal_design_projection",
        sa.Column("configuration_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id", name="fk_cdp_cv"),
                  primary_key=True),
        sa.Column("feature_semantics_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id",
                                name="fk_cdp_feature_semantics_cv")),
        sa.Column("estimand", sa.String(16), nullable=False),
        sa.Column("treatment_name", sa.String(255), nullable=False),
        sa.Column("treatment_time", sa.String(255)),
        sa.Column("treatment_levels", sa.JSON, nullable=False,
                  server_default=sa.text("'[]'")),
        sa.Column("outcome_name", sa.String(255), nullable=False),
        sa.Column("outcome_window", sa.JSON),
        sa.Column("unit", sa.String(255), nullable=False),
        sa.Column("time_zero", sa.String(255)),
        sa.Column("adjustment_set_name", sa.String(255)),
    )
    op.create_table(
        "causal_assumption",
        sa.Column("causal_design_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id",
                                name="fk_causal_assumption_cv"),
                  primary_key=True),
        sa.Column("assumption_code", sa.String(128), primary_key=True),
        sa.Column("statement", sa.Text),
        sa.Column("declaration_status", sa.String(32), nullable=False),
        sa.Column("evidence", sa.Text),
        sa.Column("ordinal", sa.Integer, nullable=False),
    )

    # ── Experiment & pipeline ─────────────────────────────────────────────────
    op.create_table(
        "experiment",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36),
                  sa.ForeignKey("project.id", name="fk_experiment_project"),
                  nullable=False),
        sa.Column("slug", sa.String(255), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("objective", sa.Text),
        sa.Column("hypothesis", sa.Text),
        sa.Column("notes", sa.Text),
        sa.Column("source_repository", sa.Text),
        sa.Column("source_commit", sa.String(128)),
        sa.Column("notebook_reference", sa.Text),
        sa.Column("tags", sa.JSON, nullable=False, server_default=sa.text("'[]'")),
        sa.Column("created_by", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_experiment_created_by"),
                  nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("archived_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("project_id", "slug", name="uq_experiment_project_slug"),
    )
    op.create_index("ix_experiment_project_id", "experiment", ["project_id"])

    op.create_table(
        "pipeline_definition",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36),
                  sa.ForeignKey("project.id", name="fk_pipeline_definition_project"),
                  nullable=False),
        sa.Column("slug", sa.String(255), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("created_by", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_pipeline_definition_created_by"),
                  nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("project_id", "slug",
                            name="uq_pipeline_definition_project_slug"),
    )
    op.create_index("ix_pipeline_definition_project_id",
                    "pipeline_definition", ["project_id"])

    op.create_table(
        "pipeline_definition_version",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("pipeline_definition_id", sa.String(36),
                  sa.ForeignKey("pipeline_definition.id", name="fk_pdv_definition"),
                  nullable=False),
        sa.Column("version_number", sa.Integer, nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="DRAFT"),
        sa.Column("random_seed_default", sa.BigInteger),
        sa.Column("fail_fast", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("canonical_json", sa.JSON, nullable=False),
        sa.Column("content_hash", sa.String(255), nullable=False),
        sa.Column("created_by", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_pdv_created_by"),
                  nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("pipeline_definition_id", "version_number",
                            name="uq_pdv_definition_number"),
        sa.UniqueConstraint("pipeline_definition_id", "content_hash",
                            name="uq_pdv_definition_hash"),
    )
    op.create_index("ix_pdv_pipeline_definition_id",
                    "pipeline_definition_version", ["pipeline_definition_id"])

    # v1 pipeline_stage_definition — without input_mode (added in 0002).
    op.create_table(
        "pipeline_stage_definition",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("pipeline_definition_version_id", sa.String(36),
                  sa.ForeignKey("pipeline_definition_version.id", name="fk_psd_pdv"),
                  nullable=False),
        sa.Column("stage_key", sa.String(255), nullable=False),
        sa.Column("stage_type", sa.String(32), nullable=False),
        sa.Column("analysis_mode", sa.String(32)),
        sa.Column("ordinal", sa.Integer, nullable=False),
        sa.Column("enabled_by_default", sa.Boolean, nullable=False,
                  server_default=sa.true()),
        sa.Column("runner_name", sa.String(128), nullable=False),
        sa.Column("timeout_seconds", sa.Integer),
        sa.Column("retry_policy_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("resource_requirements_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("metadata_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.UniqueConstraint("pipeline_definition_version_id", "stage_key",
                            name="uq_psd_pdv_stage_key"),
        sa.UniqueConstraint("pipeline_definition_version_id", "ordinal",
                            name="uq_psd_pdv_ordinal"),
    )
    op.create_index("ix_psd_pdv_id", "pipeline_stage_definition",
                    ["pipeline_definition_version_id"])

    op.create_table(
        "pipeline_stage_dependency",
        sa.Column("stage_definition_id", sa.String(36),
                  sa.ForeignKey("pipeline_stage_definition.id",
                                name="fk_pstdep_stage"),
                  primary_key=True),
        sa.Column("depends_on_stage_definition_id", sa.String(36),
                  sa.ForeignKey("pipeline_stage_definition.id",
                                name="fk_pstdep_depends_on"),
                  primary_key=True),
    )
    op.create_table(
        "pipeline_stage_config_binding",
        sa.Column("stage_definition_id", sa.String(36),
                  sa.ForeignKey("pipeline_stage_definition.id", name="fk_pscb_stage"),
                  primary_key=True),
        sa.Column("binding_name", sa.String(255), primary_key=True),
        sa.Column("configuration_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id", name="fk_pscb_cv"),
                  nullable=False),
        sa.Column("required", sa.Boolean, nullable=False, server_default=sa.true()),
    )
    op.create_table(
        "pipeline_stage_output_declaration",
        sa.Column("stage_definition_id", sa.String(36),
                  sa.ForeignKey("pipeline_stage_definition.id", name="fk_psod_stage"),
                  primary_key=True),
        sa.Column("output_name", sa.String(255), primary_key=True),
        sa.Column("artifact_kind", sa.String(64), nullable=False),
        sa.Column("required", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("register_as_dataset", sa.Boolean, nullable=False,
                  server_default=sa.false()),
    )

    # ── Execution (Run-era names) ─────────────────────────────────────────────
    # Table renamed run→execution by revision 0003.
    # Columns run_kind→execution_kind, retry_of_run_id→retry_of_execution_id by 0003.
    op.create_table(
        "run",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36),
                  sa.ForeignKey("project.id", name="fk_run_project"),
                  nullable=False),
        sa.Column("experiment_id", sa.String(36),
                  sa.ForeignKey("experiment.id", name="fk_run_experiment")),
        sa.Column("pipeline_definition_version_id", sa.String(36),
                  sa.ForeignKey("pipeline_definition_version.id", name="fk_run_pdv")),
        sa.Column("run_kind", sa.String(32), nullable=False),
        sa.Column("execution_mode", sa.String(32), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="SUBMITTED"),
        sa.Column("submitted_by", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_run_submitted_by"),
                  nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("queued_at", sa.DateTime(timezone=True)),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column("cancel_requested_at", sa.DateTime(timezone=True)),
        sa.Column("idempotency_key", sa.String(255)),
        sa.Column("request_hash", sa.String(255), nullable=False),
        sa.Column("random_seed", sa.BigInteger),
        sa.Column("code_commit", sa.String(128)),
        sa.Column("package_version", sa.String(64)),
        sa.Column("dependency_lock_hash", sa.String(255)),
        sa.Column("container_image_digest", sa.String(255)),
        sa.Column("priority", sa.Integer, nullable=False, server_default="0"),
        sa.Column("retry_of_run_id", sa.String(36),
                  sa.ForeignKey("run.id", name="fk_run_retry_of")),
        sa.Column("error_code", sa.String(128)),
        sa.Column("error_summary", sa.Text),
        sa.Column("metadata_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
    )
    op.create_index("ix_run_project_id", "run", ["project_id"])
    op.create_index(
        "uq_run_project_idempotency",
        "run",
        ["project_id", "idempotency_key"],
        unique=True,
        postgresql_where=sa.text("idempotency_key IS NOT NULL"),
        sqlite_where=sa.text("idempotency_key IS NOT NULL"),
    )
    op.create_index(
        "idx_run_project_status_submitted",
        "run",
        ["project_id", "status", "submitted_at"],
    )

    # Column renamed run_id→execution_id by 0003.
    op.create_table(
        "execution_plan",
        sa.Column("run_id", sa.String(36),
                  sa.ForeignKey("run.id", name="fk_execution_plan_run"),
                  primary_key=True),
        sa.Column("schema_version", sa.String(64), nullable=False, server_default="2"),
        sa.Column("canonical_json", sa.JSON, nullable=False),
        sa.Column("plan_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # Table renamed stage_run→stage_execution by 0003.
    # run_id→execution_id, reused_from_stage_run_id→reused_from_stage_execution_id by 0003.
    # input_mode added by 0002.
    op.create_table(
        "stage_run",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("run_id", sa.String(36),
                  sa.ForeignKey("run.id", name="fk_stage_run_run"),
                  nullable=False),
        sa.Column("stage_key", sa.String(255), nullable=False),
        sa.Column("stage_type", sa.String(32), nullable=False),
        sa.Column("analysis_mode", sa.String(32)),
        sa.Column("ordinal", sa.Integer, nullable=False),
        sa.Column("runner_name", sa.String(128), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="SUBMITTED"),
        sa.Column("current_attempt_number", sa.Integer, nullable=False,
                  server_default="0"),
        sa.Column("selected_attempt_id", sa.String(36)),
        sa.Column("cache_hit", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("reused_from_stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id", name="fk_stage_run_reused_from")),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column("error_code", sa.String(128)),
        sa.Column("error_summary", sa.Text),
        sa.UniqueConstraint("run_id", "stage_key", name="uq_stage_run_run_stage_key"),
        sa.UniqueConstraint("run_id", "ordinal", name="uq_stage_run_run_ordinal"),
    )
    op.create_index("ix_stage_run_run_id", "stage_run", ["run_id"])

    # Deferred FK: dataset_version.origin_stage_run_id → stage_run.id
    if op.get_bind().dialect.name == "postgresql":
        op.create_foreign_key(
            "fk_dataset_version_origin_stage_run",
            "dataset_version", "stage_run",
            ["origin_stage_run_id"], ["id"],
        )

    # Table renamed stage_run_dependency→stage_execution_dependency by 0003.
    op.create_table(
        "stage_run_dependency",
        sa.Column("stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id", name="fk_srd_stage_run"),
                  primary_key=True),
        sa.Column("depends_on_stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id", name="fk_srd_depends_on"),
                  primary_key=True),
    )
    op.create_table(
        "stage_run_dataset_input",
        sa.Column("stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id", name="fk_srdi_stage_run"),
                  primary_key=True),
        sa.Column("input_name", sa.String(255), primary_key=True),
        sa.Column("dataset_version_id", sa.String(36),
                  sa.ForeignKey("dataset_version.id", name="fk_srdi_dataset_version"),
                  nullable=False),
    )
    op.create_table(
        "stage_run_config_input",
        sa.Column("stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id", name="fk_srci_stage_run"),
                  primary_key=True),
        sa.Column("input_name", sa.String(255), primary_key=True),
        sa.Column("configuration_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id", name="fk_srci_cv"),
                  nullable=False),
        sa.Column("content_hash_snapshot", sa.String(255), nullable=False),
    )
    op.create_table(
        "stage_run_parameter",
        sa.Column("stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id", name="fk_srp_stage_run"),
                  primary_key=True),
        sa.Column("parameter_name", sa.String(255), primary_key=True),
        sa.Column("value_json", sa.JSON, nullable=False),
        sa.Column("source", sa.String(32), nullable=False),
    )

    # Column stage_run_id→stage_execution_id renamed by 0003.
    op.create_table(
        "stage_attempt",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id", name="fk_stage_attempt_stage_run"),
                  nullable=False),
        sa.Column("attempt_number", sa.Integer, nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="CREATED"),
        sa.Column("queue_message_id", sa.String(255)),
        sa.Column("worker_id", sa.String(255)),
        sa.Column("workspace_ref", sa.Text),
        sa.Column("queued_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("leased_at", sa.DateTime(timezone=True)),
        sa.Column("lease_expires_at", sa.DateTime(timezone=True)),
        sa.Column("heartbeat_at", sa.DateTime(timezone=True)),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column("exit_code", sa.Integer),
        sa.Column("error_class", sa.String(255)),
        sa.Column("error_code", sa.String(128)),
        sa.Column("error_message", sa.Text),
        sa.Column("error_detail_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("runtime_metadata_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("resource_usage_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.UniqueConstraint("stage_run_id", "attempt_number",
                            name="uq_stage_attempt_run_number"),
    )
    op.create_index("ix_stage_attempt_stage_run_id", "stage_attempt", ["stage_run_id"])

    # Table renamed stage_run_input_preparation→stage_execution_input_preparation by 0003.
    # Column stage_run_id→stage_execution_id renamed by 0003.
    op.create_table(
        "stage_run_input_preparation",
        sa.Column("stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id", name="fk_srip_stage_run"),
                  primary_key=True),
        sa.Column("input_mode", sa.String(32), nullable=False),
        sa.Column("input_dataset_version_id", sa.String(36),
                  sa.ForeignKey("dataset_version.id", name="fk_srip_dataset_version"),
                  nullable=False),
        sa.Column("input_table_version_id", sa.String(36),
                  sa.ForeignKey("dataset_table_version.id", name="fk_srip_dtv")),
        sa.Column("input_schema_hash", sa.String(255), nullable=False),
        sa.Column("feature_semantics_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id",
                                name="fk_srip_feature_semantics_cv")),
        sa.Column("requested_columns_json", sa.JSON, nullable=False,
                  server_default=sa.text("'[]'")),
        sa.Column("conditioning_spec_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("configured_feature_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id",
                                name="fk_srip_configured_feature_cv")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # ── Artifact ──────────────────────────────────────────────────────────────
    op.create_table(
        "artifact",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36),
                  sa.ForeignKey("project.id", name="fk_artifact_project"),
                  nullable=False),
        sa.Column("artifact_kind", sa.String(64), nullable=False),
        sa.Column("logical_name", sa.String(255), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="PENDING"),
        sa.Column("stored_object_id", sa.String(36),
                  sa.ForeignKey("stored_object.id",
                                name="fk_artifact_stored_object")),
        sa.Column("produced_by_attempt_id", sa.String(36),
                  sa.ForeignKey("stage_attempt.id",
                                name="fk_artifact_produced_by_attempt")),
        sa.Column("media_type", sa.String(255)),
        sa.Column("schema_name", sa.String(128)),
        sa.Column("schema_version", sa.String(64)),
        sa.Column("content_hash", sa.String(255), nullable=False),
        sa.Column("metadata_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_artifact_project_id", "artifact", ["project_id"])
    op.create_index(
        "idx_artifact_project_kind_created",
        "artifact",
        ["project_id", "artifact_kind", "created_at"],
    )

    # Deferred FK: data_profile.artifact_id → artifact.id
    if op.get_bind().dialect.name == "postgresql":
        op.create_foreign_key(
            "fk_data_profile_artifact",
            "data_profile", "artifact",
            ["artifact_id"], ["id"],
        )

    op.create_table(
        "stage_run_artifact_input",
        sa.Column("stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id", name="fk_srai_stage_run"),
                  primary_key=True),
        sa.Column("input_name", sa.String(255), primary_key=True),
        sa.Column("artifact_id", sa.String(36),
                  sa.ForeignKey("artifact.id", name="fk_srai_artifact"),
                  nullable=False),
    )
    op.create_table(
        "stage_run_artifact_output",
        sa.Column("stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id", name="fk_srao_stage_run"),
                  primary_key=True),
        sa.Column("output_name", sa.String(255), primary_key=True),
        sa.Column("artifact_id", sa.String(36),
                  sa.ForeignKey("artifact.id", name="fk_srao_artifact"),
                  nullable=False),
        sa.Column("required", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.UniqueConstraint("artifact_id", name="uq_srao_artifact"),
    )

    # stage_attempt_input_preparation — table name unchanged.
    # Column stage_run_id→stage_execution_id renamed by 0003.
    op.create_table(
        "stage_attempt_input_preparation",
        sa.Column("stage_attempt_id", sa.String(36),
                  sa.ForeignKey("stage_attempt.id", name="fk_saip_stage_attempt"),
                  primary_key=True),
        sa.Column("stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id", name="fk_saip_stage_run"),
                  nullable=False),
        sa.Column("input_mode", sa.String(32), nullable=False),
        sa.Column("actual_selected_columns_json", sa.JSON, nullable=False,
                  server_default=sa.text("'[]'")),
        sa.Column("excluded_columns_json", sa.JSON, nullable=False,
                  server_default=sa.text("'[]'")),
        sa.Column("resolved_conditioning_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("feature_frame_artifact_id", sa.String(36),
                  sa.ForeignKey("artifact.id",
                                name="fk_saip_feature_frame_artifact")),
        sa.Column("resolved_preparation_artifact_id", sa.String(36),
                  sa.ForeignKey("artifact.id",
                                name="fk_saip_resolved_preparation_artifact")),
        sa.Column("status", sa.String(32), nullable=False, server_default="RUNNING"),
        sa.Column("error_summary", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_saip_stage_run_id",
                    "stage_attempt_input_preparation", ["stage_run_id"])

    op.create_table(
        "artifact_lineage",
        sa.Column("downstream_artifact_id", sa.String(36),
                  sa.ForeignKey("artifact.id", name="fk_al_downstream"),
                  primary_key=True),
        sa.Column("upstream_artifact_id", sa.String(36),
                  sa.ForeignKey("artifact.id", name="fk_al_upstream"),
                  primary_key=True),
        sa.Column("relationship_type", sa.String(32), primary_key=True),
    )

    # ── Manifest & validation ─────────────────────────────────────────────────
    op.create_table(
        "manifest_record",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("run_id", sa.String(36),
                  sa.ForeignKey("run.id", name="fk_manifest_run"),
                  nullable=False),
        sa.Column("stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id", name="fk_manifest_stage_run")),
        sa.Column("scope", sa.String(16), nullable=False),
        sa.Column("artifact_id", sa.String(36),
                  sa.ForeignKey("artifact.id", name="fk_manifest_artifact"),
                  nullable=False),
        sa.Column("schema_version", sa.String(64), nullable=False),
        sa.Column("content_hash", sa.String(255), nullable=False),
        sa.Column("projection_json", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_manifest_record_run_id", "manifest_record", ["run_id"])

    # Table renamed validation_run→validation_execution by 0003.
    op.create_table(
        "validation_run",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("run_id", sa.String(36),
                  sa.ForeignKey("run.id", name="fk_validation_run_run"),
                  nullable=False),
        sa.Column("stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id",
                                name="fk_validation_run_stage_run")),
        sa.Column("validator_name", sa.String(128), nullable=False),
        sa.Column("validator_version", sa.String(64)),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_validation_run_run_id", "validation_run", ["run_id"])

    op.create_table(
        "validation_issue",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("validation_run_id", sa.String(36),
                  sa.ForeignKey("validation_run.id",
                                name="fk_validation_issue_validation_run"),
                  nullable=False),
        sa.Column("severity", sa.String(16), nullable=False),
        sa.Column("code", sa.String(128), nullable=False),
        sa.Column("message", sa.Text, nullable=False),
        sa.Column("location", sa.Text),
        sa.Column("payload_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("ordinal", sa.Integer, nullable=False),
    )
    op.create_index("ix_validation_issue_validation_run_id",
                    "validation_issue", ["validation_run_id"])

    # Table renamed run_event→execution_event by 0003.
    op.create_table(
        "run_event",
        sa.Column("id",
                  sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
                  primary_key=True, autoincrement=True),
        sa.Column("run_id", sa.String(36),
                  sa.ForeignKey("run.id", name="fk_run_event_run"),
                  nullable=False),
        sa.Column("stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id", name="fk_run_event_stage_run")),
        sa.Column("stage_attempt_id", sa.String(36),
                  sa.ForeignKey("stage_attempt.id",
                                name="fk_run_event_stage_attempt")),
        sa.Column("sequence_number", sa.BigInteger, nullable=False),
        sa.Column("event_type", sa.String(128), nullable=False),
        sa.Column("payload_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("run_id", "sequence_number",
                            name="uq_run_event_run_sequence"),
    )
    op.create_index("ix_run_event_run_id", "run_event", ["run_id"])

    # ── Outbox & audit ────────────────────────────────────────────────────────
    op.create_table(
        "outbox_event",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("aggregate_type", sa.String(64), nullable=False),
        sa.Column("aggregate_id", sa.String(36), nullable=False),
        sa.Column("event_type", sa.String(128), nullable=False),
        sa.Column("payload_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True)),
        sa.Column("claimed_at", sa.DateTime(timezone=True)),
        sa.Column("claimed_by", sa.String(255)),
        sa.Column("publish_attempts", sa.Integer, nullable=False, server_default="0"),
        sa.Column("last_error", sa.Text),
    )
    op.create_index("ix_outbox_event_aggregate_id", "outbox_event", ["aggregate_id"])
    op.create_index("ix_outbox_event_event_type", "outbox_event", ["event_type"])
    op.create_index("ix_outbox_event_published_at", "outbox_event", ["published_at"])
    op.create_index("ix_outbox_event_claimed_at", "outbox_event", ["claimed_at"])

    op.create_table(
        "audit_event",
        sa.Column("id",
                  sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
                  primary_key=True, autoincrement=True),
        sa.Column("project_id", sa.String(36),
                  sa.ForeignKey("project.id", name="fk_audit_event_project")),
        sa.Column("actor_user_id", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_audit_event_actor")),
        sa.Column("action", sa.String(128), nullable=False),
        sa.Column("resource_type", sa.String(64), nullable=False),
        sa.Column("resource_id", sa.String(36)),
        sa.Column("request_id", sa.String(255)),
        sa.Column("before_json", sa.JSON),
        sa.Column("after_json", sa.JSON),
        sa.Column("source_ip", sa.String(64)),
        sa.Column("user_agent", sa.Text),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_audit_event_project_id", "audit_event", ["project_id"])

    # ── Visualization ─────────────────────────────────────────────────────────
    op.create_table(
        "visualization_specification",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36),
                  sa.ForeignKey("project.id", name="fk_vis_spec_project"),
                  nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("dataset_table_version_id", sa.String(36),
                  sa.ForeignKey("dataset_table_version.id",
                                name="fk_vis_spec_dtv")),
        sa.Column("logical_table_name", sa.String(255)),
        sa.Column("specification_json", sa.JSON, nullable=False),
        sa.Column("specification_hash", sa.String(255), nullable=False),
        sa.Column("created_by", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_vis_spec_created_by"),
                  nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_vis_spec_project_id",
                    "visualization_specification", ["project_id"])

    op.create_table(
        "visualization_query",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36),
                  sa.ForeignKey("project.id", name="fk_vis_query_project"),
                  nullable=False),
        sa.Column("dataset_table_version_id", sa.String(36),
                  sa.ForeignKey("dataset_table_version.id", name="fk_vis_query_dtv"),
                  nullable=False),
        sa.Column("visualization_specification_id", sa.String(36),
                  sa.ForeignKey("visualization_specification.id",
                                name="fk_vis_query_vis_spec")),
        sa.Column("status", sa.String(32), nullable=False, server_default="SUBMITTED"),
        sa.Column("query_json", sa.JSON, nullable=False),
        sa.Column("query_hash", sa.String(255), nullable=False),
        sa.Column("query_engine_version", sa.String(64), nullable=False,
                  server_default="pyarrow-1"),
        sa.Column("result_json", sa.JSON),
        sa.Column("result_artifact_id", sa.String(36),
                  sa.ForeignKey("artifact.id",
                                name="fk_vis_query_result_artifact")),
        sa.Column("cache_hit", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("sampled", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("sample_size", sa.BigInteger),
        sa.Column("sampling_method", sa.String(64)),
        sa.Column("random_seed", sa.BigInteger),
        sa.Column("scanned_bytes", sa.BigInteger),
        sa.Column("result_row_count", sa.BigInteger),
        sa.Column("duration_ms", sa.BigInteger),
        sa.Column("error_summary", sa.Text),
        sa.Column("created_by", sa.String(36),
                  sa.ForeignKey("app_user.id", name="fk_vis_query_created_by"),
                  nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_vis_query_project_id", "visualization_query", ["project_id"])
    op.create_index("ix_vis_query_query_hash", "visualization_query", ["query_hash"])
    op.create_index(
        "idx_visualization_query_cache",
        "visualization_query",
        ["dataset_table_version_id", "query_hash", "query_engine_version", "status"],
    )

    # ── Results ───────────────────────────────────────────────────────────────
    # discovery_feature_version_id is NOT NULL in v1; made nullable in 0002.
    # input_mode, feature_semantics_version_id, input_preparation_attempt_id,
    # resolved_semantics_artifact_id are added by 0002.
    op.create_table(
        "discovery_result",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id",
                                name="fk_discovery_result_stage_run"),
                  nullable=False),
        sa.Column("dataset_version_id", sa.String(36),
                  sa.ForeignKey("dataset_version.id",
                                name="fk_discovery_result_dataset_version"),
                  nullable=False),
        sa.Column("discovery_analysis_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id",
                                name="fk_discovery_result_analysis_cv"),
                  nullable=False),
        sa.Column("discovery_feature_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id",
                                name="fk_discovery_result_feature_cv"),
                  nullable=False),
        sa.Column("algorithm_count", sa.Integer, nullable=False),
        sa.Column("node_count", sa.Integer),
        sa.Column("edge_count", sa.Integer),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("summary_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("stage_run_id", name="uq_discovery_result_stage_run"),
    )

    op.create_table(
        "discovery_algorithm_result",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("discovery_result_id", sa.String(36),
                  sa.ForeignKey("discovery_result.id", name="fk_dar_discovery_result"),
                  nullable=False),
        sa.Column("algorithm", sa.String(64), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("message", sa.Text),
        sa.Column("edge_artifact_id", sa.String(36),
                  sa.ForeignKey("artifact.id", name="fk_dar_edge_artifact")),
        sa.Column("graph_artifact_id", sa.String(36),
                  sa.ForeignKey("artifact.id", name="fk_dar_graph_artifact")),
        sa.Column("diagnostic_artifact_id", sa.String(36),
                  sa.ForeignKey("artifact.id", name="fk_dar_diagnostic_artifact")),
        sa.Column("metadata_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.UniqueConstraint("discovery_result_id", "algorithm",
                            name="uq_dar_result_algorithm"),
    )
    op.create_index("ix_dar_discovery_result_id",
                    "discovery_algorithm_result", ["discovery_result_id"])

    op.create_table(
        "discovery_edge",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("discovery_algorithm_result_id", sa.String(36),
                  sa.ForeignKey("discovery_algorithm_result.id", name="fk_de_dar"),
                  nullable=False),
        sa.Column("source", sa.String(255), nullable=False),
        sa.Column("target", sa.String(255), nullable=False),
        sa.Column("edge_type", sa.String(64)),
        sa.Column("orientation", sa.String(64)),
        sa.Column("score", sa.Float),
        sa.Column("stability", sa.Float),
        sa.Column("selected", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("payload_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
    )
    op.create_index("ix_de_dar_id",
                    "discovery_edge", ["discovery_algorithm_result_id"])

    # inference_feature_version_id is NOT NULL in v1; made nullable in 0002.
    # input_mode, feature_semantics_version_id, causal_graph_version_id,
    # input_preparation_attempt_id are added by 0002.
    op.create_table(
        "edge_weight_result",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id",
                                name="fk_edge_weight_result_stage_run"),
                  nullable=False),
        sa.Column("discovery_result_id", sa.String(36),
                  sa.ForeignKey("discovery_result.id",
                                name="fk_ewr_discovery_result")),
        sa.Column("dataset_version_id", sa.String(36),
                  sa.ForeignKey("dataset_version.id",
                                name="fk_ewr_dataset_version"),
                  nullable=False),
        sa.Column("inference_analysis_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id",
                                name="fk_ewr_inference_analysis_cv"),
                  nullable=False),
        sa.Column("inference_feature_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id",
                                name="fk_ewr_inference_feature_cv"),
                  nullable=False),
        sa.Column("result_artifact_id", sa.String(36),
                  sa.ForeignKey("artifact.id", name="fk_ewr_result_artifact"),
                  nullable=False),
        sa.Column("report_artifact_id", sa.String(36),
                  sa.ForeignKey("artifact.id", name="fk_ewr_report_artifact")),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("summary_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("stage_run_id", name="uq_ewr_stage_run"),
    )

    op.create_table(
        "edge_weight_estimate",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("edge_weight_result_id", sa.String(36),
                  sa.ForeignKey("edge_weight_result.id", name="fk_ewe_ewr"),
                  nullable=False),
        sa.Column("algorithm", sa.String(64), nullable=False),
        sa.Column("source", sa.String(255), nullable=False),
        sa.Column("target", sa.String(255), nullable=False),
        sa.Column("coefficient", sa.Float),
        sa.Column("standard_error", sa.Float),
        sa.Column("statistic", sa.Float),
        sa.Column("p_value", sa.Float),
        sa.Column("adjusted_p_value", sa.Float),
        sa.Column("ci_lower", sa.Float),
        sa.Column("ci_upper", sa.Float),
        sa.Column("sample_count", sa.BigInteger),
        sa.Column("robust_se", sa.String(16)),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("warning", sa.Text),
        sa.Column("interpretation_level", sa.String(64), nullable=False,
                  server_default="EXPLORATORY_EDGE_COEFFICIENT"),
        sa.Column("payload_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
    )
    op.create_index("ix_ewe_ewr_id",
                    "edge_weight_estimate", ["edge_weight_result_id"])

    # inference_feature_version_id is NOT NULL in v1; made nullable in 0002.
    # input_mode, causal_graph_version_id, input_preparation_attempt_id added by 0002.
    op.create_table(
        "treatment_effect_result",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id",
                                name="fk_treatment_effect_result_stage_run"),
                  nullable=False),
        sa.Column("dataset_version_id", sa.String(36),
                  sa.ForeignKey("dataset_version.id",
                                name="fk_ter_dataset_version"),
                  nullable=False),
        sa.Column("inference_analysis_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id",
                                name="fk_ter_inference_analysis_cv"),
                  nullable=False),
        sa.Column("inference_feature_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id",
                                name="fk_ter_inference_feature_cv"),
                  nullable=False),
        sa.Column("feature_semantics_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id",
                                name="fk_ter_feature_semantics_cv"),
                  nullable=False),
        sa.Column("causal_design_version_id", sa.String(36),
                  sa.ForeignKey("configuration_version.id",
                                name="fk_ter_causal_design_cv"),
                  nullable=False),
        sa.Column("discovery_result_id", sa.String(36),
                  sa.ForeignKey("discovery_result.id",
                                name="fk_ter_discovery_result")),
        sa.Column("treatment_name", sa.String(255), nullable=False),
        sa.Column("outcome_name", sa.String(255), nullable=False),
        sa.Column("estimand", sa.String(16), nullable=False),
        sa.Column("adjustment_strategy", sa.String(64), nullable=False),
        sa.Column("result_artifact_id", sa.String(36),
                  sa.ForeignKey("artifact.id", name="fk_ter_result_artifact"),
                  nullable=False),
        sa.Column("report_artifact_id", sa.String(36),
                  sa.ForeignKey("artifact.id", name="fk_ter_report_artifact")),
        sa.Column("diagnostic_status", sa.String(32), nullable=False),
        sa.Column("summary_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("stage_run_id", name="uq_ter_stage_run"),
    )

    op.create_table(
        "treatment_effect_estimate",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("treatment_effect_result_id", sa.String(36),
                  sa.ForeignKey("treatment_effect_result.id", name="fk_tee_ter"),
                  nullable=False),
        sa.Column("method", sa.String(64), nullable=False),
        sa.Column("estimand", sa.String(16), nullable=False),
        sa.Column("estimate", sa.Float),
        sa.Column("standard_error", sa.Float),
        sa.Column("ci_lower", sa.Float),
        sa.Column("ci_upper", sa.Float),
        sa.Column("p_value", sa.Float),
        sa.Column("adjusted_p_value", sa.Float),
        sa.Column("sample_count", sa.BigInteger),
        sa.Column("effective_sample_size", sa.Float),
        sa.Column("robust_se", sa.String(16)),
        sa.Column("adjustment_method", sa.String(64)),
        sa.Column("diagnostic_status", sa.String(32), nullable=False),
        sa.Column("interpretation_level", sa.String(64), nullable=False,
                  server_default="ESTIMATED_TREATMENT_EFFECT"),
        sa.Column("notes", sa.Text),
        sa.Column("warnings", sa.Text),
        sa.Column("payload_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
        sa.UniqueConstraint("treatment_effect_result_id", "method", "estimand",
                            name="uq_tee_result_method_estimand"),
    )
    op.create_index("ix_tee_ter_id",
                    "treatment_effect_estimate", ["treatment_effect_result_id"])

    op.create_table(
        "selected_adjustment_variable",
        sa.Column("treatment_effect_result_id", sa.String(36),
                  sa.ForeignKey("treatment_effect_result.id", name="fk_sav_ter"),
                  primary_key=True),
        sa.Column("feature_name", sa.String(255), primary_key=True),
        sa.Column("ordinal", sa.Integer, nullable=False),
        sa.Column("selection_source", sa.String(32), nullable=False),
    )
    op.create_table(
        "excluded_adjustment_candidate",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("treatment_effect_result_id", sa.String(36),
                  sa.ForeignKey("treatment_effect_result.id", name="fk_eac_ter"),
                  nullable=False),
        sa.Column("feature_name", sa.String(255), nullable=False),
        sa.Column("reason_code", sa.String(128), nullable=False),
        sa.Column("reason_detail", sa.Text),
        sa.Column("payload_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
    )
    op.create_index("ix_eac_ter_id",
                    "excluded_adjustment_candidate", ["treatment_effect_result_id"])

    op.create_table(
        "diagnostic_summary",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("stage_run_id", sa.String(36),
                  sa.ForeignKey("stage_run.id",
                                name="fk_diagnostic_summary_stage_run"),
                  nullable=False),
        sa.Column("diagnostic_type", sa.String(64), nullable=False),
        sa.Column("metric_name", sa.String(128), nullable=False),
        sa.Column("metric_value_number", sa.Float),
        sa.Column("metric_value_text", sa.Text),
        sa.Column("severity", sa.String(16)),
        sa.Column("status", sa.String(32)),
        sa.Column("artifact_id", sa.String(36),
                  sa.ForeignKey("artifact.id",
                                name="fk_diagnostic_summary_artifact")),
        sa.Column("payload_json", sa.JSON, nullable=False,
                  server_default=sa.text("'{}'")),
    )
    op.create_index("ix_diagnostic_summary_stage_run_id",
                    "diagnostic_summary", ["stage_run_id"])

    # ── PostgreSQL: immutability & append-only triggers ───────────────────────
    if op.get_bind().dialect.name == "postgresql":
        op.execute(
            """
            CREATE FUNCTION ariadne_protect_immutable() RETURNS trigger AS $$
            BEGIN
              IF TG_TABLE_NAME = 'configuration_version'
                 AND OLD.status IN ('PUBLISHED', 'DEPRECATED')
                 AND (NEW.canonical_json, NEW.content_hash, NEW.schema_version,
                      NEW.original_format, NEW.original_text,
                      NEW.configuration_id, NEW.version_number)
                     IS DISTINCT FROM
                     (OLD.canonical_json, OLD.content_hash, OLD.schema_version,
                      OLD.original_format, OLD.original_text,
                      OLD.configuration_id, OLD.version_number) THEN
                RAISE EXCEPTION 'published configuration content is immutable';
              ELSIF TG_TABLE_NAME = 'dataset_version'
                 AND OLD.status = 'READY'
                 AND (NEW.dataset_id, NEW.version_number, NEW.source_type,
                      NEW.source_metadata, NEW.schema_hash, NEW.content_hash,
                      NEW.table_count)
                     IS DISTINCT FROM
                     (OLD.dataset_id, OLD.version_number, OLD.source_type,
                      OLD.source_metadata, OLD.schema_hash, OLD.content_hash,
                      OLD.table_count) THEN
                RAISE EXCEPTION 'ready dataset version content is immutable';
              ELSIF TG_TABLE_NAME = 'pipeline_definition_version'
                 AND OLD.status IN ('PUBLISHED', 'DEPRECATED')
                 AND (NEW.pipeline_definition_id, NEW.version_number,
                      NEW.random_seed_default, NEW.fail_fast,
                      NEW.canonical_json, NEW.content_hash)
                     IS DISTINCT FROM
                     (OLD.pipeline_definition_id, OLD.version_number,
                      OLD.random_seed_default, OLD.fail_fast,
                      OLD.canonical_json, OLD.content_hash) THEN
                RAISE EXCEPTION 'published pipeline definition version is immutable';
              ELSIF TG_TABLE_NAME = 'dataset_table_version'
                 AND (NEW.dataset_version_id, NEW.logical_name, NEW.stored_object_id,
                      NEW.ordinal, NEW.file_format, NEW.schema_json,
                      NEW.schema_hash, NEW.content_hash, NEW.partition_values)
                     IS DISTINCT FROM
                     (OLD.dataset_version_id, OLD.logical_name, OLD.stored_object_id,
                      OLD.ordinal, OLD.file_format, OLD.schema_json,
                      OLD.schema_hash, OLD.content_hash, OLD.partition_values) THEN
                RAISE EXCEPTION 'dataset table content is immutable';
              ELSIF TG_TABLE_NAME = 'artifact'
                 AND OLD.status = 'AVAILABLE'
                 AND (NEW.stored_object_id, NEW.content_hash,
                      NEW.schema_name, NEW.schema_version)
                     IS DISTINCT FROM
                     (OLD.stored_object_id, OLD.content_hash,
                      OLD.schema_name, OLD.schema_version) THEN
                RAISE EXCEPTION 'available artifact content is immutable';
              END IF;
              RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER trg_configuration_version_immutable
              BEFORE UPDATE ON configuration_version
              FOR EACH ROW EXECUTE FUNCTION ariadne_protect_immutable();
            CREATE TRIGGER trg_dataset_version_immutable
              BEFORE UPDATE ON dataset_version
              FOR EACH ROW EXECUTE FUNCTION ariadne_protect_immutable();
            CREATE TRIGGER trg_pipeline_definition_version_immutable
              BEFORE UPDATE ON pipeline_definition_version
              FOR EACH ROW EXECUTE FUNCTION ariadne_protect_immutable();
            CREATE TRIGGER trg_dataset_table_immutable
              BEFORE UPDATE ON dataset_table_version
              FOR EACH ROW EXECUTE FUNCTION ariadne_protect_immutable();
            CREATE TRIGGER trg_artifact_immutable
              BEFORE UPDATE ON artifact
              FOR EACH ROW EXECUTE FUNCTION ariadne_protect_immutable();

            CREATE FUNCTION ariadne_append_only() RETURNS trigger AS $$
            BEGIN
              RAISE EXCEPTION '% is append-only', TG_TABLE_NAME;
            END;
            $$ LANGUAGE plpgsql;
            CREATE TRIGGER trg_run_event_append_only
              BEFORE UPDATE OR DELETE ON run_event
              FOR EACH ROW EXECUTE FUNCTION ariadne_append_only();
            CREATE TRIGGER trg_audit_event_append_only
              BEFORE UPDATE OR DELETE ON audit_event
              FOR EACH ROW EXECUTE FUNCTION ariadne_append_only();
            """
        )


def downgrade() -> None:
    bind = op.get_bind()
    is_pg = bind.dialect.name == "postgresql"

    if is_pg:
        op.execute("DROP TRIGGER IF EXISTS trg_audit_event_append_only ON audit_event")
        op.execute("DROP TRIGGER IF EXISTS trg_run_event_append_only ON run_event")
        op.execute("DROP TRIGGER IF EXISTS trg_artifact_immutable ON artifact")
        op.execute(
            "DROP TRIGGER IF EXISTS trg_dataset_table_immutable ON dataset_table_version"
        )
        op.execute(
            "DROP TRIGGER IF EXISTS trg_pipeline_definition_version_immutable"
            " ON pipeline_definition_version"
        )
        op.execute(
            "DROP TRIGGER IF EXISTS trg_dataset_version_immutable ON dataset_version"
        )
        op.execute(
            "DROP TRIGGER IF EXISTS trg_configuration_version_immutable"
            " ON configuration_version"
        )
        op.execute("DROP FUNCTION IF EXISTS ariadne_append_only() CASCADE")
        op.execute("DROP FUNCTION IF EXISTS ariadne_protect_immutable() CASCADE")

    op.drop_table("diagnostic_summary")
    op.drop_table("excluded_adjustment_candidate")
    op.drop_table("selected_adjustment_variable")
    op.drop_table("treatment_effect_estimate")
    op.drop_table("treatment_effect_result")
    op.drop_table("edge_weight_estimate")
    op.drop_table("edge_weight_result")
    op.drop_table("discovery_edge")
    op.drop_table("discovery_algorithm_result")
    op.drop_table("discovery_result")
    op.drop_table("visualization_query")
    op.drop_table("visualization_specification")
    op.drop_table("audit_event")
    op.drop_table("outbox_event")
    op.drop_table("run_event")
    op.drop_table("validation_issue")
    op.drop_table("validation_run")
    op.drop_table("manifest_record")
    op.drop_table("artifact_lineage")
    op.drop_table("stage_attempt_input_preparation")
    op.drop_table("stage_run_artifact_output")
    op.drop_table("stage_run_artifact_input")

    if is_pg:
        op.drop_constraint(
            "fk_data_profile_artifact", "data_profile", type_="foreignkey"
        )

    op.drop_table("artifact")
    op.drop_table("stage_run_input_preparation")
    op.drop_table("stage_attempt")
    op.drop_table("stage_run_parameter")
    op.drop_table("stage_run_config_input")
    op.drop_table("stage_run_dataset_input")
    op.drop_table("stage_run_dependency")

    if is_pg:
        op.drop_constraint(
            "fk_dataset_version_origin_stage_run", "dataset_version",
            type_="foreignkey",
        )

    op.drop_table("stage_run")
    op.drop_table("execution_plan")
    op.drop_table("run")
    op.drop_table("pipeline_stage_output_declaration")
    op.drop_table("pipeline_stage_config_binding")
    op.drop_table("pipeline_stage_dependency")
    op.drop_table("pipeline_stage_definition")
    op.drop_table("pipeline_definition_version")
    op.drop_table("pipeline_definition")
    op.drop_table("experiment")
    op.drop_table("causal_assumption")
    op.drop_table("causal_design_projection")
    op.drop_table("feature_semantic_item")
    op.drop_table("feature_semantics_projection")
    op.drop_table("configuration_dependency")
    op.drop_table("configuration_version")
    op.drop_table("configuration")
    op.drop_table("column_profile")
    op.drop_table("data_profile")
    op.drop_table("dataset_column_policy")
    op.drop_table("dataset_column")
    op.drop_table("dataset_table_version")
    op.drop_table("dataset_version")
    op.drop_table("dataset")
    op.drop_table("stored_object")
    op.drop_table("project_member")
    op.drop_table("project")
    op.drop_table("role")
    op.drop_table("app_user")
