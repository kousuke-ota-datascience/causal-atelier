"""Read-only navigation metadata API."""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

from ariadne.product.application.navigation_catalog import CATALOG


router = APIRouter(tags=["navigation"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class NavigationStageResponse(StrictModel):
    stage_id: str
    slug: str
    label: str
    order: int


class FamilyNavigationResponse(StrictModel):
    family: str
    slug: str
    label: str
    default_stage_id: str
    stages: list[NavigationStageResponse]


class AnalysisNavigationResponse(StrictModel):
    schema_version: Literal["analysis-navigation/1"]
    families: list[FamilyNavigationResponse]


@router.get("/navigation/analysis", response_model=AnalysisNavigationResponse)
async def get_analysis_navigation() -> AnalysisNavigationResponse:
    return AnalysisNavigationResponse(
        schema_version="analysis-navigation/1",
        families=[
            FamilyNavigationResponse(
                family=family.family.value,
                slug=family.slug,
                label=family.label,
                default_stage_id=family.default_stage_id,
                stages=[
                    NavigationStageResponse(
                        stage_id=stage.stage_id,
                        slug=stage.slug,
                        label=stage.label,
                        order=stage.order,
                    )
                    for stage in family.stages
                ],
            )
            for family in CATALOG
        ],
    )
