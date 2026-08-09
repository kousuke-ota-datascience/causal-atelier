"""Focused pure-policy contract tests for E4-G06 P01."""

from __future__ import annotations

import pytest

from ariadne.product.domain.errors import InvalidSchema
from ariadne.product.domain.lineage import (
    LineageAuthority,
    assert_generic_lineage_allowed,
    classify_lineage_authority,
)


@pytest.mark.parametrize(("source", "relation", "target"), (
    ("Execution", "GENERATED", "Result"),
    ("Result", "GENERATED", "Artifact"),
    ("DatasetVersion", "USED_INPUT", "Execution"),
    ("AnalysisView", "USED_INPUT", "Execution"),
    ("Result", "USED_INPUT", "Execution"),
    ("Execution", "REVISED_FROM", "Execution"),
    ("Execution", "DERIVED_FROM", "Execution"),
    ("Result", "DERIVED_FROM", "GraphVersion"),
    ("Artifact", "DERIVED_FROM", "DatasetVersion"),
))
def test_structural_tuples_are_typed_authority(
    source: str, relation: str, target: str,
) -> None:
    assert classify_lineage_authority(source, relation, target) is LineageAuthority.TYPED_STRUCTURAL
    with pytest.raises(InvalidSchema, match="typed structural"):
        assert_generic_lineage_allowed(source, relation, target)


@pytest.mark.parametrize(("source", "relation", "target"), (
    ("Artifact", "DERIVED_FROM", "Artifact"),
    ("Result", "SUMMARIZES", "Result"),
    ("Result", "SUMMARIZES", "Artifact"),
    ("Result", "DOCUMENTS", "AnalysisSpecification"),
    ("Result", "EVIDENCE_FOR", "AnalysisView"),
    ("Result", "MOTIVATED", "AnalysisSpecification"),
    ("Result", "MOTIVATED", "Execution"),
    ("Result", "SELECTED", "Annotation"),
    ("Result", "REJECTED", "Annotation"),
))
def test_approved_generic_only_tuples_are_admitted(
    source: str, relation: str, target: str,
) -> None:
    assert classify_lineage_authority(source, relation, target) is LineageAuthority.GENERIC_ONLY
    assert_generic_lineage_allowed(source, relation, target)


def test_derived_from_authority_depends_on_semantic_endpoints() -> None:
    assert classify_lineage_authority(
        "Execution", "DERIVED_FROM", "Execution",
    ) is LineageAuthority.TYPED_STRUCTURAL
    assert classify_lineage_authority(
        "Artifact", "DERIVED_FROM", "Artifact",
    ) is LineageAuthority.GENERIC_ONLY


@pytest.mark.parametrize(("source", "relation", "target"), (
    ("Artifact", "DERIVED_FROM", "Result"),
    ("Result", "GENERATED", "Result"),
    ("Result", "NOT_A_RELATION", "Artifact"),
))
def test_unknown_or_unapproved_tuple_is_closed_by_default(
    source: str, relation: str, target: str,
) -> None:
    assert classify_lineage_authority(source, relation, target) is None
    with pytest.raises(InvalidSchema, match="Unsupported generic lineage semantic relation"):
        assert_generic_lineage_allowed(source, relation, target)
