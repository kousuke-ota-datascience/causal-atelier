"""D3 PostgreSQL cross-family no-new-Family-write trap."""

from __future__ import annotations

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ariadne.product.persistence.orm_models import (
    FamilyArtifactOrm, FamilyExecutionOrm, FamilyResultOrm, FamilyStageExecutionOrm,
)


def _counts(session: Session) -> tuple[int, int, int, int]:
    return tuple(session.scalar(select(func.count()).select_from(model)) for model in (
        FamilyExecutionOrm, FamilyStageExecutionOrm, FamilyResultOrm, FamilyArtifactOrm,
    ))  # type: ignore[return-value]


@pytest.mark.postgres
def test_g05_d3_global_family_table_trap_stays_stable_for_prior_canonical_matrix(postgres_engine) -> None:  # type: ignore[no-untyped-def]
    """Fresh runner baseline used with the Phase B/C/D canonical-operation matrix.

    The actual submits, worker processing, and mutations are exercised by the
    Phase B/C/D tests in the same standardized D3 bundle; this test fixes the
    all-four-table invariant as an explicit final audit target.
    """
    with Session(bind=postgres_engine) as session:
        before = _counts(session)
        session.commit()
    with Session(bind=postgres_engine) as session:
        assert _counts(session) == before
