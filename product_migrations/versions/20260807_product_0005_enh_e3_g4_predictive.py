"""ENH-E3 G4 Research Context, Analysis Specification, and predictive references.

Revision ID: 20260807_product_0005
Revises: 20260807_product_0004
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260807_product_0005"
down_revision = "20260807_product_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "product_research_context_version",
        sa.Column("research_context_version_id", sa.String(36), primary_key=True),
        sa.Column(
            "project_id",
            sa.String(36),
            sa.ForeignKey("product_project.project_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("context_key", sa.String(100), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("schema_version", sa.String(100), nullable=False),
        sa.Column("problem_statement", sa.Text(), nullable=False),
        sa.Column("research_questions_json", sa.JSON(), nullable=False),
        sa.Column("significance", sa.Text()),
        sa.Column("hypotheses_json", sa.JSON(), nullable=False),
        sa.Column("decision_context_json", sa.JSON(), nullable=False),
        sa.Column("relations_json", sa.JSON(), nullable=False),
        sa.Column("canonical_hash", sa.String(64)),
        sa.Column("created_by", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("fixed_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint(
            "project_id",
            "context_key",
            "version_number",
            name="uq_product_research_context_version",
        ),
        sa.CheckConstraint(
            "status IN ('DRAFT','FIXED')", name="ck_product_research_context_status"
        ),
        sa.CheckConstraint(
            "version_number > 0", name="ck_product_research_context_version_number"
        ),
    )
    op.create_index(
        "ix_product_research_context_version_project_id",
        "product_research_context_version",
        ["project_id"],
    )

    op.create_table(
        "product_analysis_specification",
        sa.Column("analysis_specification_id", sa.String(36), primary_key=True),
        sa.Column(
            "project_id",
            sa.String(36),
            sa.ForeignKey("product_project.project_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("specification_key", sa.String(100), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("schema_version", sa.String(100), nullable=False),
        sa.Column("analysis_family", sa.String(20), nullable=False),
        sa.Column(
            "research_context_version_id",
            sa.String(36),
            sa.ForeignKey(
                "product_research_context_version.research_context_version_id",
                ondelete="RESTRICT",
            ),
            nullable=False,
        ),
        sa.Column(
            "dataset_version_id",
            sa.String(36),
            sa.ForeignKey("product_dataset_version.dataset_version_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "analysis_view_id",
            sa.String(36),
            sa.ForeignKey("product_analysis_view.analysis_view_id", ondelete="RESTRICT"),
        ),
        sa.Column("analysis_mode", sa.String(20), nullable=False),
        sa.Column("family_spec_schema_version", sa.String(100), nullable=False),
        sa.Column("family_spec_json", sa.JSON(), nullable=False),
        sa.Column("revision_context_json", sa.JSON()),
        sa.Column("warnings_json", sa.JSON(), nullable=False),
        sa.Column("canonical_hash", sa.String(64)),
        sa.Column("created_by", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("fixed_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint(
            "project_id",
            "specification_key",
            "version_number",
            name="uq_product_analysis_specification_version",
        ),
        sa.CheckConstraint(
            "status IN ('DRAFT','FIXED')", name="ck_product_analysis_specification_status"
        ),
        sa.CheckConstraint(
            "analysis_family IN ('EXPLORATORY','CAUSAL','PREDICTIVE')",
            name="ck_product_analysis_specification_family",
        ),
        sa.CheckConstraint(
            "analysis_mode IN ('EXPLORATORY','CONFIRMATORY')",
            name="ck_product_analysis_specification_mode",
        ),
        sa.CheckConstraint(
            "version_number > 0", name="ck_product_analysis_specification_version_number"
        ),
    )
    for column in (
        "project_id",
        "research_context_version_id",
        "dataset_version_id",
        "analysis_view_id",
    ):
        op.create_index(
            f"ix_product_analysis_specification_{column}",
            "product_analysis_specification",
            [column],
        )

    op.add_column(
        "product_family_execution",
        sa.Column("research_context_version_id", sa.String(36)),
    )
    op.create_foreign_key(
        "fk_product_family_execution_research_context",
        "product_family_execution",
        "product_research_context_version",
        ["research_context_version_id"],
        ["research_context_version_id"],
        ondelete="RESTRICT",
    )
    op.create_index(
        "ix_product_family_execution_research_context_version_id",
        "product_family_execution",
        ["research_context_version_id"],
    )
    op.add_column(
        "product_family_execution",
        sa.Column("analysis_specification_id", sa.String(36)),
    )
    op.create_foreign_key(
        "fk_product_family_execution_analysis_specification",
        "product_family_execution",
        "product_analysis_specification",
        ["analysis_specification_id"],
        ["analysis_specification_id"],
        ondelete="RESTRICT",
    )
    op.create_index(
        "ix_product_family_execution_analysis_specification_id",
        "product_family_execution",
        ["analysis_specification_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_product_family_execution_analysis_specification_id",
        table_name="product_family_execution",
    )
    op.drop_constraint(
        "fk_product_family_execution_analysis_specification",
        "product_family_execution",
        type_="foreignkey",
    )
    op.drop_column("product_family_execution", "analysis_specification_id")
    op.drop_index(
        "ix_product_family_execution_research_context_version_id",
        table_name="product_family_execution",
    )
    op.drop_constraint(
        "fk_product_family_execution_research_context",
        "product_family_execution",
        type_="foreignkey",
    )
    op.drop_column("product_family_execution", "research_context_version_id")
    op.drop_table("product_analysis_specification")
    op.drop_table("product_research_context_version")
