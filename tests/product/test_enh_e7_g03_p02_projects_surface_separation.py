"""Focused ENH-E7 G03 P02 coverage for Projects surface separation."""

import subprocess
from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_projects_root_owns_list_and_new_project_and_hides_incompatible_chrome() -> None:
    script = """
const fs = require('fs');
globalThis.window = globalThis;
eval(fs.readFileSync('frontend/top_level_surface_activation.js', 'utf8'));
function element(id, surface) {
  return {
    id, dataset:surface ? {topLevelSurfaceRoot:surface} : {}, hidden:false, attributes:{},
    children:[], parent:null,
    append(child){ this.children.push(child); child.parent=this; },
    setAttribute(name, value){ this.attributes[name]=value; },
    classList:{toggle(name, value){ this.active=value; }},
  };
}
const roots = {
  projects:element('projects-surface', 'projects'),
  management:element('project-management-surface', 'project-management'),
  analysis:element('analysis-surface', 'analysis'),
};
const content = {};
for (const [surface, ids] of Object.entries({
  projects:['projects', 'project-new'],
  management:['management', 'context', 'data', 'results'],
  analysis:['analysis-context-header', 'analysis-navigation-shell', 'explore', 'discovery', 'inference', 'predictive'],
})) for (const id of ids) content[id]=element(id);
globalThis.document = {
  querySelector(selector) {
    const match = selector.match(/^\\[data-top-level-surface-root="(.+)"\\]$/);
    return match ? roots[match[1] === 'project-management' ? 'management' : match[1]] : null;
  },
  querySelectorAll(selector) {
    if (selector === '[data-top-level-surface-root]') return Object.values(roots);
    throw Error(selector);
  },
  getElementById(id) { return content[id] || (id === 'project-management-section-content' ? roots.management : (id === 'analysis-context-region' || id === 'analysis-stage-main-area' ? roots.analysis : null)); },
};
TopLevelSurfaceActivation.initialize();
if (content.projects.parent !== roots.projects || content['project-new'].parent !== roots.projects) throw Error('Projects content ownership');
for (const workspace of ['projects', 'project-new']) {
  TopLevelSurfaceActivation.activateForWorkspace(workspace);
  const visibleRoots = Object.values(roots).filter(root => !root.hidden).map(root => root.dataset.topLevelSurfaceRoot);
  if (visibleRoots.length !== 1 || visibleRoots[0] !== 'projects') throw Error(`${workspace}: visible roots ${visibleRoots}`);
}
console.log('PASS');
"""
    result = subprocess.run(
        ["node", "-e", script], cwd=REPOSITORY, text=True, capture_output=True, check=False
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert result.stdout.strip() == "PASS"


def test_projects_markup_owns_project_actions_without_an_obsolete_sidebar() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")

    projects_start = html.index('<section id="projects-surface"')
    projects_end = html.index('</section>', projects_start)
    projects_root = html[projects_start:projects_end]
    assert 'id="projects-surface-chrome"' in projects_root
    assert 'id="project-select"' in projects_root
    assert 'id="new-project"' in projects_root
    assert '<aside' not in html


def test_existing_project_selection_and_create_bindings_are_preserved() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "$('#new-project').onclick=async()=>" in app
    assert "$('#project-select').onchange=async event=>" in app
    assert "$('#project-register-form').onsubmit=async event=>" in app
    assert "api('/projects',{method:'POST'" in app
