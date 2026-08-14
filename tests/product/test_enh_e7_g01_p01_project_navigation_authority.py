"""Focused ENH-E7 G01 P01 coverage for Project navigation authority."""

import subprocess
from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def _navigation_result(pathname: str) -> str:
    script = f"""
const fs = require('fs');
globalThis.window = globalThis;
eval(fs.readFileSync('frontend/project_navigation.js', 'utf8'));
const route = ProjectNavigation.parse({pathname!r});
console.log(JSON.stringify({{route, serialized: ProjectNavigation.serialize(route)}}));
"""
    result = subprocess.run(
        ["node", "-e", script], cwd=REPOSITORY, check=True, text=True, capture_output=True
    )
    return result.stdout.strip()


def test_project_routes_parse_and_serialize_to_their_canonical_paths() -> None:
    assert _navigation_result("/projects/") == '{"route":{"kind":"collection"},"serialized":"/projects"}'
    assert _navigation_result("/projects/new/") == '{"route":{"kind":"new"},"serialized":"/projects/new"}'
    assert _navigation_result("/projects/p1") == (
        '{"route":{"kind":"project","projectId":"p1","section":"overview"},'
        '"serialized":"/projects/p1/overview"}'
    )
    assert _navigation_result("/projects/a%20project/overview/") == (
        '{"route":{"kind":"project","projectId":"a project","section":"overview"},'
        '"serialized":"/projects/a%20project/overview"}'
    )
    assert _navigation_result("/projects/p1/context") == (
        '{"route":{"kind":"project","projectId":"p1","section":"context"},'
        '"serialized":"/projects/p1/context"}'
    )
    assert _navigation_result("/projects/p1/data") == (
        '{"route":{"kind":"project","projectId":"p1","section":"data"},'
        '"serialized":"/projects/p1/data"}'
    )
    assert _navigation_result("/projects/p1/results") == (
        '{"route":{"kind":"project","projectId":"p1","section":"results"},'
        '"serialized":"/projects/p1/results"}'
    )


def test_app_uses_project_navigation_for_normalization_and_history() -> None:
    source = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")

    assert "function synchronizeProjectHistory(route,historyMode)" in source
    assert "ProjectNavigation.parse(location.pathname)" in source
    assert "ProjectNavigation.projectRoute(state.project.project_id,button.dataset.route)" in source
    assert "ProjectNavigation.overview(state.project.project_id),'REPLACE'" in source
    assert "synchronizeProjectHistory(route,'REPLACE');" in source
    assert "window.addEventListener('popstate',()=>restoreProjectRoute()" in source
    assert '<script src="/project_navigation.js"></script>' in html


def test_project_navigation_does_not_claim_analysis_route_ownership() -> None:
    source = (REPOSITORY / "frontend" / "project_navigation.js").read_text(encoding="utf-8")

    assert "/analysis/" not in source
    assert "AnalysisNavigation" not in source
