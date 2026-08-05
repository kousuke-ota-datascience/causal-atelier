"""Add MLflow tracking columns to execution table.

This migration adds four columns to the ``execution`` table:

- ``mlflow_experiment_id``  – VARCHAR(255), nullable
- ``mlflow_run_id``         – VARCHAR(255), nullable, partial-unique (non-NULL)
- ``mlflow_tracking_status`` – VARCHAR(32), NOT NULL, CHECK constraint
- ``mlflow_tracking_error``  – TEXT, nullable

Existing rows are backfilled as follows:

- Executions with ``execution_mode`` in ``DRY_RUN`` or ``VALIDATE_ONLY`` receive
  ``mlflow_tracking_status = NOT_REQUIRED``.
- All other executions receive ``mlflow_tracking_status = PENDING``.  We do not
  attempt to recover or fabricate historical MLflow Run IDs.

DB constraint vs Application invariant split
--------------------------------------------
- ``CHECK mlflow_tracking_status IN (...)`` is enforced by the DB on every
  write.
- ``mlflow_run_id`` uniqueness is enforced by a partial unique index (NULL
  values are excluded, so multiple NULLs are allowed).
- The invariants "ACTIVE/FINISHED require mlflow_run_id" and "NOT_REQUIRED
  implies mlflow_run_id IS NULL" are enforced at the Application layer, not by
  a DB CHECK, to allow intermediate recovery states (e.g., ERROR after a crash
  between run creation and DB save).

Downgrade removes all four columns.
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "20260804_0004"
down_revision = "20260803_0003"
branch_labels = None
depends_on = None

_CHECK_NAME = "ck_execution_mlflow_tracking_status"
_CHECK_EXPR = "mlflow_tracking_status IN ('NOT_REQUIRED','PENDING','ACTIVE','FINISHED','ERROR')"
_INDEX_NAME = "uq_execution_mlflow_run_id"


def _columns(table: str) -> set[str]:
    return {col["name"] for col in inspect(op.get_bind()).get_columns(table)}


def upgrade() -> None:
    cols = _columns("execution")

    if "mlflow_experiment_id" not in cols:
        op.add_column(
            "execution",
            sa.Column("mlflow_experiment_id", sa.String(255), nullable=True),
        )
    if "mlflow_run_id" not in cols:
        op.add_column(
            "execution",
            sa.Column("mlflow_run_id", sa.String(255), nullable=True),
        )
    if "mlflow_tracking_error" not in cols:
        op.add_column(
            "execution",
            sa.Column("mlflow_tracking_error", sa.Text(), nullable=True),
        )

    if "mlflow_tracking_status" not in cols:
        # Add as nullable first so we can backfill before adding NOT NULL.
        op.add_column(
            "execution",
            sa.Column(
                "mlflow_tracking_status",
                sa.String(32),
                nullable=True,
            ),
        )

    # Backfill: DRY_RUN / VALIDATE_ONLY → NOT_REQUIRED; everything else → PENDING.
    op.execute(
        "UPDATE execution "
        "SET mlflow_tracking_status = 'NOT_REQUIRED' "
        "WHERE execution_mode IN ('DRY_RUN', 'VALIDATE_ONLY')"
    )
    op.execute(
        "UPDATE execution "
        "SET mlflow_tracking_status = 'PENDING' "
        "WHERE mlflow_tracking_status IS NULL"
    )

    # PostgreSQL: alter to NOT NULL after backfill.
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.alter_column("execution", "mlflow_tracking_status", nullable=False)

        # Partial unique index on non-NULL mlflow_run_id.
        op.execute(
            f"CREATE UNIQUE INDEX IF NOT EXISTS {_INDEX_NAME} "
            "ON execution (mlflow_run_id) "
            "WHERE mlflow_run_id IS NOT NULL"
        )
        # CHECK constraint.
        op.create_check_constraint(
            _CHECK_NAME,
            "execution",
            _CHECK_EXPR,
        )
    else:
        # SQLite does not support ALTER COLUMN; the column is effectively NOT NULL
        # due to the backfill.  Partial unique indexes and named CHECK constraints
        # are also limited on SQLite.
        try:
            op.execute(
                f"CREATE UNIQUE INDEX IF NOT EXISTS {_INDEX_NAME} "
                "ON execution (mlflow_run_id) "
                "WHERE mlflow_run_id IS NOT NULL"
            )
        except Exception:
            pass


def downgrade() -> None:
    bind = op.get_bind()

    # Drop the partial unique index for all dialects before dropping the column.
    if bind.dialect.name == "postgresql":
        try:
            op.drop_constraint(_CHECK_NAME, "execution", type_="check")
        except Exception:
            pass
        try:
            op.drop_index(_INDEX_NAME, table_name="execution")
        except Exception:
            pass
    else:
        # SQLite: drop the index via raw SQL before dropping the column.
        try:
            op.execute(f"DROP INDEX IF EXISTS {_INDEX_NAME}")
        except Exception:
            pass

    cols = _columns("execution")
    for col in ("mlflow_tracking_status", "mlflow_tracking_error",
                "mlflow_run_id", "mlflow_experiment_id"):
        if col in cols:
            op.drop_column("execution", col)
