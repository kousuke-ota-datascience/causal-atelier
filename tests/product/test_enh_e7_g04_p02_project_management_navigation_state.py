"""Focused ENH-E7 G04 P02 coverage for Project Management navigation state."""

import subprocess
from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def _surface_result() -> str:
    script = """
const fs = require('fs');
globalThis.window = globalThis;
eval(fs.readFileSync('frontend/project_navigation.js', 'utf8'));
eval(fs.readFileSync('frontend/navigation_state.js', 'utf8'));
eval(fs.readFileSync('frontend/top_level_surface_activation.js', 'utf8'));
const catalog = {families:[{slug:'causal', default_stage_id:'setup', stages:[{slug:'setup'}]}]};
const routes = ['overview', 'context', 'data', 'results'];
for (const section of routes) {
  const pathname = `/projects/p1/${section}`;
  const parsed = ProjectNavigation.parse(pathname);
  if (parsed.section !== section) throw Error(`${pathname}: section ${parsed.section}`);
  if (TopLevelSurfaceActivation.classifyRoute(pathname, catalog) !== 'project-management') throw Error(`${pathname}: wrong surface`);
}
const roots = ['projects', 'project-management', 'analysis'].map(kind => ({
  dataset:{topLevelSurfaceRoot:kind}, hidden:false,
  setAttribute(){}, classList:{toggle(name, value){this.active=value;}},
}));
globalThis.document = {querySelectorAll(selector){
  if (selector === '[data-top-level-surface-root]') return roots;
  throw Error(selector);
}};
TopLevelSurfaceActivation.activateForWorkspace('results');
const visible = roots.filter(root => !root.hidden).map(root => root.dataset.topLevelSurfaceRoot);
if (JSON.stringify(visible) !== JSON.stringify(['project-management'])) throw Error(`visible roots: ${visible}`);
console.log(JSON.stringify({visible}));
"""
    result = subprocess.run(
        ["node", "-e", script], cwd=REPOSITORY, text=True, capture_output=True, check=False
    )
    assert result.returncode == 0, result.stderr or result.stdout
    return result.stdout.strip()


def test_pm_routes_map_to_their_section_and_only_pm_surface_is_visible() -> None:
    assert _surface_result() == '{"visible":["project-management"]}'


def test_pm_navigation_selected_state_is_derived_from_workspace_without_local_state() -> None:
    source = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "$$('#project-management-navigation [data-workspace]').forEach(item=>{" in source
    assert "const current=item.dataset.workspace===workspace;" in source
    assert "item.classList.toggle('active',current);" in source
    assert "item.setAttribute('aria-current',current?'page':'false');" in source
    assert "TopLevelSurfaceActivation.activateForWorkspace(workspace);" in source
    assert "if(!retainAnalysisShell)clearAnalysisNavigationShell();" in source


def test_overview_data_and_results_ownership_remains_in_their_existing_sections() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")

    assert 'id="archive-project"' in html
    assert 'id="analysis-view-form"' in html
    assert 'id="result-summary"' in html
