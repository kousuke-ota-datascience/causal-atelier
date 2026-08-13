"""ENH-E5 reproducibility metadata for append-only stage attempts."""

from alembic import op
import sqlalchemy as sa


revision = "20260813_product_0011"
down_revision = "20260809_product_0010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # NULL is the intentional backfill for deterministic attempts and for
    # historical rows whose effective seed was not recorded.
    op.add_column("product_stage_attempt", sa.Column("effective_random_seed", sa.Integer(), nullable=True))


def downgrade() -> None:
    raise NotImplementedError("ENH-E5 reproducibility migration is forward-only")
