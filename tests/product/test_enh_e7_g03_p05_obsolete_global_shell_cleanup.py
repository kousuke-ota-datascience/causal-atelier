"""Focused ENH-E7 G03 P05 coverage for obsolete global shell removal."""

from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_obsolete_global_sidebar_and_common_header_are_absent_from_production_sources() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    authority = (REPOSITORY / "frontend" / "top_level_surface_activation.js").read_text(encoding="utf-8")
    css = (REPOSITORY / "frontend" / "styles.css").read_text(encoding="utf-8")

    for obsolete in ("<aside", "selected-project-shell", "common-workspace-header", "data-hidden-on-projects-surface"):
        assert obsolete not in html
    assert "renderCommonWorkspaceHeader" not in app
    assert "data-hidden-on-projects-surface" not in authority
    assert "aside" not in css
    assert 'id="analysis-context-header"' in html
    assert "renderAnalysisContext" in app


def test_analysis_context_has_one_production_owner_and_no_duplicate_navigation_controls() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    authority = (REPOSITORY / "frontend" / "top_level_surface_activation.js").read_text(encoding="utf-8")

    assert html.count('id="project-management-navigation"') == 1
    assert html.count('id="analysis-routing-actions"') == 1
    assert authority.count("analysis-context-header") == 1
    assert "analysis-context-region" in authority
