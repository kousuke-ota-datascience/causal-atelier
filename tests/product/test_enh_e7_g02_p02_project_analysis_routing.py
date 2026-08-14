"""Focused ENH-E7 G02 P02 coverage for Project/Analysis/Results routing."""

from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_project_launches_each_catalog_family_at_its_catalog_default_stage() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert 'id="analysis-workspace-launcher"' in html
    assert "function renderAnalysisWorkspaceLauncher()" in app
    assert "catalog.families.map(family=>" in app
    assert "AnalysisNavigation.defaultContext(catalog,project.project_id,button.dataset.openAnalysisFamily)" in app
    assert "source:'project-analysis-launch'" in app
    assert "default_stage_id" not in app[app.index("function renderAnalysisWorkspaceLauncher()") : app.index("function renderAnalysisNavigation()")]


def test_analysis_routing_uses_existing_transition_authority_for_project_and_results() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    routing = app[app.index("const routing=$('#analysis-routing-actions');") : app.index("$$('#analysis-family-tabs button')")]

    assert 'id="analysis-routing-actions"' in html
    assert "return-to-project-management" in routing
    assert "open-results-lineage" in routing
    assert "activateWorkspace('management')" in routing
    assert "activateWorkspace('results')" in routing
    assert "history.pushState" not in routing
    assert "synchronizeAnalysisHistory" not in routing


def test_routing_does_not_change_backend_execution_or_persistence_semantics() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    routing = app[app.index("function renderAnalysisWorkspaceLauncher()") : app.index("function activateAnalysisPresentation(")]

    assert "/execution-plans" not in routing
    assert "/executions" not in routing
    assert "workspace-state`,{method:'PUT'" not in routing
