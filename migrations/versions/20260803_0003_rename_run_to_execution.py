"""Rename the Run execution-management domain to Execution.

The initial migration builds its schema from ``Base.metadata`` (which now uses
the Execution names), so a *fresh* database is already correct and this
migration is a guarded no-op for it. An existing v1/v2 database still carries
the legacy ``run`` / ``stage_run`` / ``run_event`` names, so this migration
renames those tables and their columns in place, preserving all data.
"""

from __future__ import annotations

from alembic import op
from sqlalchemy import inspect

revision = "20260803_0003"
down_revision = "20260720_0002"
branch_labels = None
depends_on = None


# (old_table, new_table)
TABLE_RENAMES: list[tuple[str, str]] = [
    ("run", "execution"),
    ("stage_run", "stage_execution"),
    ("stage_run_dependency", "stage_execution_dependency"),
    ("stage_run_dataset_input", "stage_execution_dataset_input"),
    ("stage_run_config_input", "stage_execution_config_input"),
    ("stage_run_artifact_input", "stage_execution_artifact_input"),
    ("stage_run_input_preparation", "stage_execution_input_preparation"),
    ("stage_run_parameter", "stage_execution_parameter"),
    ("stage_run_artifact_output", "stage_execution_artifact_output"),
    ("stage_run_graph_input", "stage_execution_graph_input"),
    ("run_event", "execution_event"),
    ("validation_run", "validation_execution"),
]

# (new_table, old_column, new_column) — applied after tables are renamed.
COLUMN_RENAMES: list[tuple[str, str, str]] = [
    ("execution", "run_kind", "execution_kind"),
    ("execution", "retry_of_run_id", "retry_of_execution_id"),
    ("execution_plan", "run_id", "execution_id"),
    ("stage_execution", "run_id", "execution_id"),
    ("stage_execution", "reused_from_stage_run_id", "reused_from_stage_execution_id"),
    ("stage_execution_dependency", "stage_run_id", "stage_execution_id"),
    (
        "stage_execution_dependency",
        "depends_on_stage_run_id",
        "depends_on_stage_execution_id",
    ),
    ("stage_attempt", "stage_run_id", "stage_execution_id"),
    ("stage_execution_dataset_input", "stage_run_id", "stage_execution_id"),
    ("stage_execution_config_input", "stage_run_id", "stage_execution_id"),
    ("stage_execution_artifact_input", "stage_run_id", "stage_execution_id"),
    ("stage_execution_input_preparation", "stage_run_id", "stage_execution_id"),
    ("stage_attempt_input_preparation", "stage_run_id", "stage_execution_id"),
    ("stage_execution_parameter", "stage_run_id", "stage_execution_id"),
    ("stage_execution_artifact_output", "stage_run_id", "stage_execution_id"),
    ("stage_execution_graph_input", "stage_run_id", "stage_execution_id"),
    ("manifest_record", "run_id", "execution_id"),
    ("manifest_record", "stage_run_id", "stage_execution_id"),
    ("validation_execution", "run_id", "execution_id"),
    ("validation_execution", "stage_run_id", "stage_execution_id"),
    ("validation_issue", "validation_run_id", "validation_execution_id"),
    ("execution_event", "run_id", "execution_id"),
    ("execution_event", "stage_run_id", "stage_execution_id"),
    ("dataset_version", "origin_stage_run_id", "origin_stage_execution_id"),
    ("discovery_result", "stage_run_id", "stage_execution_id"),
    ("edge_weight_result", "stage_run_id", "stage_execution_id"),
    ("treatment_effect_result", "stage_run_id", "stage_execution_id"),
    ("diagnostic_summary", "stage_run_id", "stage_execution_id"),
]

# (table, old_index, new_index)
INDEX_RENAMES: list[tuple[str, str, str]] = [
    ("execution", "uq_run_project_idempotency", "uq_execution_project_idempotency"),
    (
        "execution",
        "idx_run_project_status_submitted",
        "idx_execution_project_status_submitted",
    ),
]


def _tables() -> set[str]:
    return set(inspect(op.get_bind()).get_table_names())


def _columns(table: str) -> set[str]:
    return {col["name"] for col in inspect(op.get_bind()).get_columns(table)}


def _indexes(table: str) -> set[str]:
    return {ix["name"] for ix in inspect(op.get_bind()).get_indexes(table)}


def _apply(table_map: list[tuple[str, str]], column_map: list[tuple[str, str, str]],
           index_map: list[tuple[str, str, str]]) -> None:
    tables = _tables()
    for old_table, new_table in table_map:
        if old_table in tables and new_table not in tables:
            op.rename_table(old_table, new_table)
    for table, old_col, new_col in column_map:
        if table not in _tables():
            continue
        columns = _columns(table)
        if old_col in columns and new_col not in columns:
            with op.batch_alter_table(table) as batch:
                batch.alter_column(old_col, new_column_name=new_col)
    is_postgres = op.get_bind().dialect.name == "postgresql"
    for table, old_index, new_index in index_map:
        if not is_postgres or table not in _tables():
            continue
        if old_index in _indexes(table) and new_index not in _indexes(table):
            op.execute(f'ALTER INDEX "{old_index}" RENAME TO "{new_index}"')


def upgrade() -> None:
    _apply(TABLE_RENAMES, COLUMN_RENAMES, INDEX_RENAMES)


def downgrade() -> None:
    new_to_old = {new: old for old, new in TABLE_RENAMES}
    _apply(
        [(new, old) for old, new in TABLE_RENAMES],
        [
            (new_to_old.get(table, table), new_col, old_col)
            for table, old_col, new_col in COLUMN_RENAMES
        ],
        [(new_to_old.get(table, table), new, old) for table, old, new in INDEX_RENAMES],
    )
