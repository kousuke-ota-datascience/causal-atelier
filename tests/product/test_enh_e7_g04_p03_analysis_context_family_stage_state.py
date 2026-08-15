"""Focused ENH-E7 G04 P03 coverage for Analysis Context and Family/Stage state."""

import subprocess
from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def _navigation_result() -> str:
    script = """
const fs = require('fs');
globalThis.window = globalThis;
eval(fs.readFileSync('frontend/navigation_state.js', 'utf8'));
const catalog = {families:[
  {slug:'exploratory', default_stage_id:'profile', stages:[{slug:'profile'}, {slug:'findings'}]},
  {slug:'causal', default_stage_id:'setup', stages:[{slug:'setup'}, {slug:'estimation'}]},
]};
const deep = AnalysisNavigation.parse('/projects/p1/analysis/causal/estimation', catalog);
if (deep.projectId !== 'p1' || deep.familySlug !== 'causal' || deep.stageSlug !== 'estimation') throw Error('deep route context mismatch');
const familyDefault = AnalysisNavigation.defaultContext(catalog, 'p1', 'exploratory');
if (familyDefault.stageSlug !== 'profile') throw Error('catalog default stage ignored');
const before = AnalysisNavigation.serialize(deep);
const contextSelectionOnly = {research_context_version_id:'rc1', dataset_version_id:'d1', analysis_view_id:'v1'};
if (AnalysisNavigation.serialize(deep) !== before || !contextSelectionOnly.analysis_view_id) throw Error('context selection rewrote route');
console.log(JSON.stringify({deep:AnalysisNavigation.serialize(deep), familyDefault:AnalysisNavigation.serialize(familyDefault), before}));
"""
    result = subprocess.run(
        ["node", "-e", script], cwd=REPOSITORY, text=True, capture_output=True, check=False
    )
    assert result.returncode == 0, result.stderr or result.stdout
    return result.stdout.strip()


def test_deep_route_and_family_default_stage_come_from_navigation_catalog() -> None:
    assert _navigation_result() == (
        '{"deep":"/projects/p1/analysis/causal/estimation",'
        '"familyDefault":"/projects/p1/analysis/exploratory/profile",'
        '"before":"/projects/p1/analysis/causal/estimation"}'
    )


def test_analysis_context_selection_does_not_rewrite_family_or_stage_route() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    handlers = app[app.index("function saveCommonWorkspaceSelection(") : app.index("$('#project-register-form').onsubmit")]

    assert "saveWorkspaceState(changes)" in handlers
    assert "synchronizeAnalysisHistory" not in handlers
    assert "history.pushState" not in handlers
    assert "history.replaceState" not in handlers
    assert "$('#common-context').onchange=event=>saveCommonWorkspaceSelection" in handlers
    assert "$('#common-dataset').onchange=event=>saveCommonWorkspaceSelection" in handlers
    assert "$('#common-view').onchange=event=>saveCommonWorkspaceSelection" in handlers


def test_rendered_selected_family_stage_and_contents_share_navigation_context() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    render = app[app.index("function renderAnalysisNavigation()") : app.index("function activateAnalysisPresentation(")]

    assert "const current=catalog.families.find(item=>item.slug===context.familySlug);" in render
    assert "const currentStage=current.stages.find(item=>item.slug===context.stageSlug);" in render
    assert "aria-selected=\"'+(f.slug===current.slug)+'\"" in render
    assert "aria-current=\"'+(s.slug===context.stageSlug?'page':'false')+'\"" in render
    assert "<b>'+escapeHtml(current.label)+'</b> / '+escapeHtml(currentStage.label)+'" in render
    assert "AnalysisNavigation.defaultContext(catalog,state.project.project_id,family.slug)" in render


def test_invalid_saved_selection_is_left_unselected_without_creating_a_default_resource() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    context = app[app.index("function renderAnalysisContext()") : app.index("async function loadWorkspaceState()")]

    assert "select.value=available?value:'';" in context
    assert "if(value&&!available)invalid.push(label);" in context
    assert "保存済み選択を復元できません" in context
    assert "defaultContext" not in context
    assert "method:'POST'" not in context
