"""Focused ENH-E7 G02 P01 coverage for the Analysis shell and context restore."""

from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_analysis_shell_exposes_catalog_selected_stage_contents() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert 'id="analysis-family-tabs"' in html
    assert 'id="analysis-stage-sidebar"' in html
    assert 'id="analysis-stage-contents"' in html
    assert "const currentStage=current.stages.find(item=>item.slug===context.stageSlug);" in app
    assert "<h2>Stage Contents</h2>" in app
    assert "aria-selected=" in app
    assert "aria-current=" in app


def test_context_header_has_read_only_project_and_restores_only_saved_selection() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "Current Project (read-only)" in html
    assert '<output id="analysis-context-project-name">' in html
    assert 'id="common-context"' in html
    assert 'id="common-dataset"' in html
    assert 'id="common-view"' in html
    assert "const contextValue=workspace?.research_context_version_id||'';" in app
    assert "const datasetValue=workspace?.dataset_version_id||'';" in app
    assert "const viewValue=workspace?.analysis_view_id||'';" in app
    assert "select.value=available?value:'';" in app
    assert "保存済み選択を復元できません" in app


def test_context_selection_updates_do_not_navigate_or_create_resources() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    handlers = app[app.index("function saveCommonWorkspaceSelection(") : app.index("$('#project-register-form').onsubmit")]

    assert "saveWorkspaceState" in handlers
    assert "loadWorkspaceState" in handlers
    assert "synchronizeAnalysisHistory" not in handlers
    assert "history.pushState" not in handlers
    assert "/executions" not in handlers
    assert "/analysis-views`,{method:'POST'" not in handlers
