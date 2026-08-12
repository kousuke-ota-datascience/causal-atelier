"""Read-only, family-local navigation metadata for analysis clients."""

from __future__ import annotations

from dataclasses import dataclass

from ariadne.product.domain.enums import AnalysisFamily


@dataclass(frozen=True)
class NavigationStage:
    stage_id: str
    slug: str
    label: str
    order: int


@dataclass(frozen=True)
class FamilyNavigation:
    family: AnalysisFamily
    slug: str
    label: str
    default_stage_id: str
    stages: tuple[NavigationStage, ...]


def validate_navigation_catalog(catalog: tuple[FamilyNavigation, ...]) -> None:
    """Validate the dedicated navigation metadata contract."""
    expected_families = set(AnalysisFamily)
    families = [item.family for item in catalog]
    if len(families) != len(expected_families) or set(families) != expected_families:
        raise ValueError("catalog must contain each AnalysisFamily exactly once")

    family_slugs = [item.slug for item in catalog]
    if any(not slug for slug in family_slugs) or len(set(family_slugs)) != len(family_slugs):
        raise ValueError("family slugs must be non-blank and globally unique")

    for family in catalog:
        if not family.stages:
            raise ValueError("family navigation must contain at least one stage")
        stage_ids = [stage.stage_id for stage in family.stages]
        stage_slugs = [stage.slug for stage in family.stages]
        if any(not identifier for identifier in stage_ids + stage_slugs):
            raise ValueError("stage IDs and slugs must be non-blank")
        if len(set(stage_ids)) != len(stage_ids) or len(set(stage_slugs)) != len(stage_slugs):
            raise ValueError("stage IDs and slugs must be unique within a family")
        if family.default_stage_id not in stage_ids:
            raise ValueError("default stage ID must belong to its family")
        if [stage.order for stage in family.stages] != list(range(len(family.stages))):
            raise ValueError("stage order must be deterministic and consecutive")
        if any(stage.stage_id != stage.slug for stage in family.stages):
            raise ValueError("canonical stage ID must equal slug")


def _stages(*stage_ids: str) -> tuple[NavigationStage, ...]:
    return tuple(
        NavigationStage(
            stage_id=stage_id,
            slug=stage_id,
            label=stage_id.replace("-", " ").title(),
            order=order,
        )
        for order, stage_id in enumerate(stage_ids)
    )


CATALOG = (
    FamilyNavigation(
        family=AnalysisFamily.EXPLORATORY,
        slug="exploratory",
        label="Exploratory",
        default_stage_id="profile",
        stages=_stages("profile", "data-quality", "distribution", "relationships", "comparison", "findings"),
    ),
    FamilyNavigation(
        family=AnalysisFamily.PREDICTIVE,
        slug="predictive",
        label="Predictive",
        default_stage_id="setup",
        stages=_stages("setup", "train", "predict", "metrics", "explainability", "model-management"),
    ),
    FamilyNavigation(
        family=AnalysisFamily.CAUSAL,
        slug="causal",
        label="Causal",
        default_stage_id="setup",
        stages=_stages("setup", "discovery", "identification", "estimation", "effects", "diagnostics", "sensitivity"),
    ),
)

validate_navigation_catalog(CATALOG)
