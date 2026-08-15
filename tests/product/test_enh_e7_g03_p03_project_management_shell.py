"""Focused ENH-E7 G03 P03 coverage for the Project Management shell."""

import subprocess
from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_project_management_surface_owns_sections_and_hides_other_top_level_surfaces() -> None:
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
const sectionContainer=element('project-management-section-content');
const analysisStageMainArea=element('analysis-stage-main-area');
const analysisContextRegion=element('analysis-context-region');
globalThis.document = {
  querySelector(selector) {const match=selector.match(/^\\[data-top-level-surface-root="(.+)"\\]$/); return match ? roots[match[1] === 'project-management' ? 'management' : match[1]] : null;},
  querySelectorAll(selector) {if(selector === '[data-top-level-surface-root]') return Object.values(roots); if(selector === '[data-hidden-on-projects-surface]') return []; throw Error(selector);},
  getElementById(id) {if(id === 'project-management-section-content') return sectionContainer; if(id === 'analysis-stage-main-area') return analysisStageMainArea; if(id === 'analysis-context-region') return analysisContextRegion; return content[id];},
};
TopLevelSurfaceActivation.initialize();
TopLevelSurfaceActivation.activateForWorkspace('context');
const visible=Object.values(roots).filter(root=>!root.hidden).map(root=>root.dataset.topLevelSurfaceRoot);
if (visible.length !== 1 || visible[0] !== 'project-management') throw Error(`visible roots: ${visible}`);
for (const id of ['management', 'context', 'data', 'results']) if(content[id].parent !== sectionContainer) throw Error(`missing PM ownership: ${id}`);
console.log('PASS');
"""
    result = subprocess.run(["node", "-e", script], cwd=REPOSITORY, text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr or result.stdout
    assert result.stdout.strip() == "PASS"


def test_project_management_navigation_is_a_vertical_project_local_descendant() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    css = (REPOSITORY / "frontend" / "styles.css").read_text(encoding="utf-8")

    shell_start = html.index('<section id="project-management-surface"')
    shell_end = html.index('</section>', shell_start)
    shell = html[shell_start:shell_end]
    assert 'id="project-management-navigation"' in shell
    assert 'data-workspace="management"' in shell
    assert 'data-workspace="context"' in shell
    assert 'data-workspace="data"' in shell
    assert 'data-workspace="results"' in shell
    assert 'id="project-management-section-content"' in shell
    assert '.project-management-shell-chrome nav{display:flex;flex-direction:column;' in css
    assert 'id="analysis-navigation-shell"' not in shell


def test_existing_section_bindings_remain_workspace_based() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "$$('nav [data-workspace]').forEach(button=>button.onclick=" in app
    assert "PROJECT_WORKSPACES=Object.freeze({overview:'management',context:'context',data:'data',results:'results'})" in app
    assert "$('#project-management-project-name').textContent=state.project?.name||'Project未選択'" in app
