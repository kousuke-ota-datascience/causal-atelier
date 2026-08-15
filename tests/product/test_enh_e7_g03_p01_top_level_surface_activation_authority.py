"""Focused ENH-E7 G03 P01 coverage for top-level presentation activation."""

import subprocess
from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def _authority_result() -> str:
    script = """
const fs = require('fs');
globalThis.window = globalThis;
eval(fs.readFileSync('frontend/project_navigation.js', 'utf8'));
eval(fs.readFileSync('frontend/navigation_state.js', 'utf8'));
eval(fs.readFileSync('frontend/top_level_surface_activation.js', 'utf8'));
const catalog = {families:[
  {slug:'exploratory', default_stage_id:'profile', stages:[{slug:'profile'}]},
  {slug:'causal', default_stage_id:'setup', stages:[{slug:'setup'}]},
]};
const fixtures = {
  '/projects':'projects',
  '/projects/new':'projects',
  '/projects/p1/overview':'project-management',
  '/projects/p1/context':'project-management',
  '/projects/p1/data':'project-management',
  '/projects/p1/results':'project-management',
  '/projects/p1/analysis/exploratory/profile':'analysis',
  '/projects/p1/analysis/causal/setup/resource/graph-version/g1':'analysis',
};
for (const [pathname, expected] of Object.entries(fixtures)) {
  const actual = TopLevelSurfaceActivation.classifyRoute(pathname, catalog);
  if (actual !== expected) throw Error(`${pathname}: ${actual}`);
}
const roots = ['projects', 'project-management', 'analysis'].map(kind => ({
  dataset:{topLevelSurfaceRoot:kind}, hidden:false, attributes:{},
  setAttribute(name, value){this.attributes[name]=value;},
  classList:{toggle(name, value){this.active=value;}},
}));
globalThis.document = {querySelectorAll(selector){
  if (selector === '[data-top-level-surface-root]') return roots;
  if (selector === '[data-hidden-on-projects-surface]') return [];
  throw Error(selector);
}};
TopLevelSurfaceActivation.activate('analysis');
const visible = roots.filter(root => !root.hidden).map(root => root.dataset.topLevelSurfaceRoot);
if (visible.length !== 1 || visible[0] !== 'analysis') throw Error(`visible roots: ${visible}`);
console.log(JSON.stringify({context:TopLevelSurfaceActivation.surfaceForWorkspace('context'), data:TopLevelSurfaceActivation.surfaceForWorkspace('data'), visible}));
"""
    result = subprocess.run(
        ["node", "-e", script], cwd=REPOSITORY, text=True, capture_output=True, check=False
    )
    assert result.returncode == 0, result.stderr or result.stdout
    return result.stdout.strip()


def test_route_fixtures_have_one_expected_top_level_surface_kind() -> None:
    assert _authority_result() == (
        '{"context":"project-management","data":"project-management","visible":["analysis"]}'
    )


def test_top_level_surface_roots_are_exclusive_and_owned_by_one_authority() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    authority = (REPOSITORY / "frontend" / "top_level_surface_activation.js").read_text(encoding="utf-8")

    assert html.count("data-top-level-surface-root=") == 3
    assert 'data-top-level-surface-root="projects"' in html
    assert 'data-top-level-surface-root="project-management"' in html
    assert 'data-top-level-surface-root="analysis"' in html
    assert "root.hidden=!active" in authority
    assert "root.setAttribute('aria-hidden',String(!active))" in authority
    assert "TopLevelSurfaceActivation.activateForWorkspace(workspace);" in app


def test_project_internal_section_switching_keeps_its_top_level_surface_kind() -> None:
    authority = (REPOSITORY / "frontend" / "top_level_surface_activation.js").read_text(encoding="utf-8")

    for workspace in ("management", "context", "data", "results"):
        assert f"{workspace}:SURFACE_KINDS.PROJECT_MANAGEMENT" in authority
