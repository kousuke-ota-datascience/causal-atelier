"""Focused ENH-E6 G01 P01 coverage for the frontend transition authority."""

from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_analysis_navigation_entries_converge_on_one_transition_authority() -> None:
    source = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "async function applyAnalysisNavigation(" in source
    assert "function synchronizeAnalysisHistory(context,historyMode)" in source
    assert "function activateAnalysisPresentation(context)" in source
    assert "renderAnalysisNavigation();\n  activateAnalysisPresentation(next);\n  await renderOperationAvailability();" in source
    assert "source:'family-tab-click'" in source
    assert "source:'stage-sidebar-click'" in source
    assert "source:'route-restore'" in source
    assert "window.addEventListener('popstate',()=>restoreProjectRoute()" in source


def test_transition_history_modes_are_explicit_and_do_not_duplicate_same_target() -> None:
    source = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "ANALYSIS_HISTORY_MODES=Object.freeze({PUSH:'PUSH',REPLACE:'REPLACE',NONE:'NONE'})" in source
    assert "if(historyMode===ANALYSIS_HISTORY_MODES.NONE||location.pathname===path)return;" in source
    assert "history.pushState({project_id:context.projectId,navigation:context},'',path);" in source
    assert "history.replaceState({project_id:context.projectId,navigation:context},'',path);" in source
    assert "historyMode:ANALYSIS_HISTORY_MODES.REPLACE,source:'legacy-route-normalization'" in source


def test_shell_is_cleared_when_a_non_analysis_workspace_becomes_active() -> None:
    source = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "function clearAnalysisNavigationShell()" in source
    assert "if(!retainAnalysisShell)clearAnalysisNavigationShell();" in source
    assert "await activateWorkspace(presentation.workspace,{push:false,retainAnalysisShell:true});" in source
    assert "$('#analysis-family-tabs').replaceChildren();$('#analysis-stage-sidebar').replaceChildren();" in source
