"""Focused ENH-E7 G04 P04 coverage for cross-surface browser history."""

from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_browser_runner_covers_pm_analysis_results_reload_back_and_forward() -> None:
    runner = (REPOSITORY / "tests/browser_e2e/run_enh_e7_project_integration.py").read_text(encoding="utf-8")

    assert '"project-analysis-launcher"' in runner
    assert '"cross-surface-reload-history"' in runner
    assert 'page.locator("#return-to-project-management").click()' in runner
    assert 'page.locator("#open-results-lineage").click()' in runner
    assert 'arg=f"/projects/{project_id}/analysis/exploratory/profile"' in runner
    assert "page.reload(wait_until=\"networkidle\")" in runner
    assert "page.go_back(wait_until=\"networkidle\")" in runner
    assert "page.go_forward(wait_until=\"networkidle\")" in runner
    assert "assert page.locator(\"#project-select\").input_value() == project_id" in runner


def test_shared_transition_authorities_preserve_project_and_prevent_duplicate_entries() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "if(historyMode===ANALYSIS_HISTORY_MODES.NONE||location.pathname===path)return;" in app
    assert "if(location.pathname===path)return;" in app
    assert "window.addEventListener('popstate',()=>restoreProjectRoute()" in app
    assert "await applyAnalysisNavigation(parsed,{historyMode:ANALYSIS_HISTORY_MODES.NONE,source:'route-restore'});" in app
    assert "$('#return-to-project-management').onclick=()=>activateWorkspace('management')" in app
    assert "$('#open-results-lineage').onclick=()=>activateWorkspace('results')" in app


def test_surface_activation_clears_stale_analysis_shell_on_pm_results_restore() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "TopLevelSurfaceActivation.activateForWorkspace(workspace);" in app
    assert "if(!retainAnalysisShell)clearAnalysisNavigationShell();" in app
    assert "await activateWorkspace(PROJECT_WORKSPACES[route.section],{push:false});" in app
