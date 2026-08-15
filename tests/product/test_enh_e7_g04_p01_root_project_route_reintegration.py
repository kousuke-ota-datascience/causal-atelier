"""Focused ENH-E7 G04 P01 coverage for root and Project route reintegration."""

import subprocess
from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def _route_result() -> str:
    script = """
const fs = require('fs');
globalThis.window = globalThis;
eval(fs.readFileSync('frontend/project_navigation.js', 'utf8'));
eval(fs.readFileSync('frontend/navigation_state.js', 'utf8'));
eval(fs.readFileSync('frontend/top_level_surface_activation.js', 'utf8'));
const catalog = {families:[{slug:'causal', default_stage_id:'setup', stages:[{slug:'setup'}]}]};
const routes = [
  ['/projects', 'projects'],
  ['/projects/new', 'projects'],
  ['/projects/p1', 'project-management'],
  ['/projects/p1/overview', 'project-management'],
];
for (const [pathname, expectedSurface] of routes) {
  const actualSurface = TopLevelSurfaceActivation.classifyRoute(pathname, catalog);
  if (actualSurface !== expectedSurface) throw Error(`${pathname}: ${actualSurface}`);
}
const shortRoute = ProjectNavigation.parse('/projects/p1');
if (ProjectNavigation.serialize(shortRoute) !== '/projects/p1/overview') throw Error('short route did not canonicalize');
console.log(JSON.stringify({shortRoute:ProjectNavigation.serialize(shortRoute)}));
"""
    result = subprocess.run(
        ["node", "-e", script], cwd=REPOSITORY, text=True, capture_output=True, check=False
    )
    assert result.returncode == 0, result.stderr or result.stdout
    return result.stdout.strip()


def test_project_routes_activate_only_their_expected_top_level_surface() -> None:
    assert _route_result() == '{"shortRoute":"/projects/p1/overview"}'


def test_root_load_replaces_root_with_project_collection_without_legacy_workspace() -> None:
    source = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    root_restore = """if(location.pathname==='/'||location.pathname===''){
    synchronizeProjectHistory({kind:'collection'},'REPLACE');
    state.project=null;fillProject();await loadProjects();
    await activateWorkspace('projects',{push:false});
    return true;
  }"""
    assert root_restore in source


def test_create_success_replaces_with_new_project_overview() -> None:
    source = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "synchronizeProjectHistory(ProjectNavigation.overview(state.project.project_id),'REPLACE');await activateWorkspace('management',{push:false});" in source
