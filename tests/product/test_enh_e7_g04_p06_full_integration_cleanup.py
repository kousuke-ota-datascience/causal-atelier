"""Focused ENH-E7 G04 P06 coverage for the complete browser journey and cleanup audit."""

from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_browser_runner_covers_root_to_pm_analysis_family_stage_results_and_pm_without_errors() -> None:
    runner = (REPOSITORY / "tests/browser_e2e/run_enh_e7_project_integration.py").read_text(encoding="utf-8")

    assert 'page.goto(f"{WEB}/", wait_until="networkidle")' in runner
    assert "window.location.pathname === '/projects'" in runner
    assert 'button[data-family="causal"]' in runner
    assert 'button[data-stage="discovery"]' in runner
    assert 'page.locator("#open-results-lineage").click()' in runner
    assert "full-g04-root-pm-analysis-results-pm" in runner
    assert "page.on(\"pageerror\"" in runner
    assert "message.type == \"error\"" in runner
    assert "assert not page_errors, page_errors" in runner


def test_browser_runner_asserts_one_visible_surface_root_for_every_workspace() -> None:
    runner = (REPOSITORY / "tests/browser_e2e/run_enh_e7_project_integration.py").read_text(encoding="utf-8")

    assert "SURFACE_BY_WORKSPACE" in runner
    assert "[data-top-level-surface-root]" in runner
    assert "visible.length === 1 && visible[0] === expected" in runner
    assert "_active(page, \"projects\")" in runner
    assert "_active(page, \"management\")" in runner
    assert "_active(page, \"explore\")" in runner
    assert '_route(page, project_id, "results", "results")' in runner


def test_history_and_event_authorities_have_no_duplicate_global_binding_or_temporary_fallback() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert app.count("window.addEventListener('popstate'") == 1
    assert app.count("function synchronizeProjectHistory(") == 1
    assert app.count("function synchronizeAnalysisHistory(") == 1
    assert "temporary routing shim" not in app.lower()
    assert "fallback route" not in app.lower()
