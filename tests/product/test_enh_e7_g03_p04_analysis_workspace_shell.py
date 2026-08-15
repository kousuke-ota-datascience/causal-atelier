"""Focused ENH-E7 G03 P04 coverage for the Analysis Workspace shell."""

import subprocess
from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_analysis_surface_owns_context_and_stage_contents_and_hides_other_roots() -> None:
    script = """
const fs = require('fs');
globalThis.window = globalThis;
eval(fs.readFileSync('frontend/top_level_surface_activation.js', 'utf8'));
function element(id, surface) {
  return {id, dataset:surface ? {topLevelSurfaceRoot:surface} : {}, hidden:false, attributes:{}, parent:null,
    append(child){child.parent=this;}, setAttribute(name, value){this.attributes[name]=value;},
    classList:{toggle(name, value){this.active=value;}}};
}
const roots = {projects:element('projects-surface', 'projects'), management:element('project-management-surface', 'project-management'), analysis:element('analysis-surface', 'analysis')};
const content = {};
for (const id of ['projects', 'project-new', 'analysis-context-header', 'management', 'context', 'data', 'results', 'explore', 'discovery', 'inference', 'predictive']) content[id]=element(id);
const managementContent=element('project-management-section-content');
const analysisContext=element('analysis-context-region');
const analysisMain=element('analysis-stage-main-area');
globalThis.document = {
  querySelector(selector) {const match=selector.match(/^\\[data-top-level-surface-root="(.+)"\\]$/); return match ? roots[match[1] === 'project-management' ? 'management' : match[1]] : null;},
  querySelectorAll(selector) {if(selector === '[data-top-level-surface-root]') return Object.values(roots); if(selector === '[data-hidden-on-projects-surface]') return []; throw Error(selector);},
  getElementById(id) {if(id === 'project-management-section-content') return managementContent; if(id === 'analysis-context-region') return analysisContext; if(id === 'analysis-stage-main-area') return analysisMain; return content[id];},
};
TopLevelSurfaceActivation.initialize();
TopLevelSurfaceActivation.activateForWorkspace('explore');
const visible=Object.values(roots).filter(root=>!root.hidden).map(root=>root.dataset.topLevelSurfaceRoot);
if (visible.length !== 1 || visible[0] !== 'analysis') throw Error(`visible roots: ${visible}`);
if (content['analysis-context-header'].parent !== analysisContext) throw Error('Analysis Context ownership');
for (const id of ['explore', 'discovery', 'inference', 'predictive']) if(content[id].parent !== analysisMain) throw Error(`missing Analysis main ownership: ${id}`);
console.log('PASS');
"""
    result = subprocess.run(["node", "-e", script], cwd=REPOSITORY, text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr or result.stdout
    assert result.stdout.strip() == "PASS"


def test_analysis_navigation_topology_has_context_return_family_stage_and_main_area() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    css = (REPOSITORY / "frontend" / "styles.css").read_text(encoding="utf-8")

    analysis_start = html.index('<section id="analysis-surface"')
    analysis_end = html.index('</section>', analysis_start)
    analysis = html[analysis_start:analysis_end]
    assert 'id="analysis-context-region"' in analysis
    assert 'id="analysis-routing-actions"' in analysis
    assert 'id="analysis-family-tabs"' in analysis
    assert 'id="analysis-stage-sidebar"' in analysis
    assert 'id="analysis-stage-main-area"' in analysis
    assert analysis.index('id="analysis-context-region"') < analysis.index('id="analysis-routing-actions"')
    assert '.analysis-workspace-top-region #analysis-context-project-name{font:500 22px Georgia,serif}' in css
    assert '#analysis-family-tabs{display:flex;flex-direction:row;' in css
    assert '#analysis-stage-sidebar{display:flex;flex-direction:column;' in css
    assert '#analysis-stage-layout{display:grid;grid-template-columns:' in css


def test_existing_family_stage_and_return_action_bindings_are_preserved() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "$('#analysis-family-tabs').innerHTML=" in app
    assert "$('#analysis-stage-sidebar').innerHTML=" in app
    assert "$('#return-to-project-management').onclick=()=>activateWorkspace('management')" in app
    assert "source:'family-tab-click'" in app
    assert "source:'stage-sidebar-click'" in app
