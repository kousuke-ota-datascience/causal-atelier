from __future__ import annotations

import ast
from pathlib import Path

import pytest

from ariadne.product.application.navigation_catalog import (
    CATALOG,
    FamilyNavigation,
    NavigationStage,
    validate_navigation_catalog,
)
from ariadne.product.domain.enums import AnalysisFamily


@pytest.mark.anyio
async def test_analysis_navigation_api_returns_the_canonical_catalog(client):
    response = await client.get("/api/v1/navigation/analysis")

    assert response.status_code == 200
    assert response.json() == {
        "schema_version": "analysis-navigation/1",
        "families": [
            {"family": "EXPLORATORY", "slug": "exploratory", "label": "Exploratory", "default_stage_id": "profile", "stages": [
                {"stage_id": "profile", "slug": "profile", "label": "Profile", "order": 0},
                {"stage_id": "data-quality", "slug": "data-quality", "label": "Data Quality", "order": 1},
                {"stage_id": "distribution", "slug": "distribution", "label": "Distribution", "order": 2},
                {"stage_id": "relationships", "slug": "relationships", "label": "Relationships", "order": 3},
                {"stage_id": "comparison", "slug": "comparison", "label": "Comparison", "order": 4},
                {"stage_id": "findings", "slug": "findings", "label": "Findings", "order": 5},
            ]},
            {"family": "PREDICTIVE", "slug": "predictive", "label": "Predictive", "default_stage_id": "setup", "stages": [
                {"stage_id": "setup", "slug": "setup", "label": "Setup", "order": 0},
                {"stage_id": "train", "slug": "train", "label": "Train", "order": 1},
                {"stage_id": "predict", "slug": "predict", "label": "Predict", "order": 2},
                {"stage_id": "metrics", "slug": "metrics", "label": "Metrics", "order": 3},
                {"stage_id": "explainability", "slug": "explainability", "label": "Explainability", "order": 4},
                {"stage_id": "model-management", "slug": "model-management", "label": "Model Management", "order": 5},
            ]},
            {"family": "CAUSAL", "slug": "causal", "label": "Causal", "default_stage_id": "setup", "stages": [
                {"stage_id": "setup", "slug": "setup", "label": "Setup", "order": 0},
                {"stage_id": "discovery", "slug": "discovery", "label": "Discovery", "order": 1},
                {"stage_id": "identification", "slug": "identification", "label": "Identification", "order": 2},
                {"stage_id": "estimation", "slug": "estimation", "label": "Estimation", "order": 3},
                {"stage_id": "effects", "slug": "effects", "label": "Effects", "order": 4},
                {"stage_id": "diagnostics", "slug": "diagnostics", "label": "Diagnostics", "order": 5},
                {"stage_id": "sensitivity", "slug": "sensitivity", "label": "Sensitivity", "order": 6},
            ]},
        ],
    }


@pytest.mark.parametrize("catalog", [
    (CATALOG[0], CATALOG[0], CATALOG[2]),
    (CATALOG[0], FamilyNavigation(AnalysisFamily.PREDICTIVE, "", "Predictive", "setup", CATALOG[1].stages), CATALOG[2]),
    (CATALOG[0], FamilyNavigation(AnalysisFamily.PREDICTIVE, "predictive", "Predictive", "missing", CATALOG[1].stages), CATALOG[2]),
    (CATALOG[0], FamilyNavigation(AnalysisFamily.PREDICTIVE, "predictive", "Predictive", "setup", ()), CATALOG[2]),
    (CATALOG[0], FamilyNavigation(AnalysisFamily.PREDICTIVE, "predictive", "Predictive", "setup", (NavigationStage("setup", "setup", "Setup", 0), NavigationStage("setup", "second", "Second", 1))), CATALOG[2]),
])
def test_catalog_validation_rejects_invalid_catalogs(catalog):
    with pytest.raises(ValueError):
        validate_navigation_catalog(catalog)


def test_navigation_catalog_has_no_execution_runtime_dependency_or_persistence_registration():
    repository = Path(__file__).parents[2]
    catalog_path = repository / "src/ariadne/product/application/navigation_catalog.py"
    tree = ast.parse(catalog_path.read_text(encoding="utf-8"))
    imported_modules = [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module]
    assert not any("execution_plan" in module or "stage_execution" in module for module in imported_modules)
    assert not any(module.startswith("ariadne.product.persistence") for module in imported_modules)
    assert "analysis-navigation/1" not in (repository / "src/ariadne/product/domain/schemas.py").read_text(encoding="utf-8")
