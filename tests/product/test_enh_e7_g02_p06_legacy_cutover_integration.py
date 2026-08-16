"""Focused ENH-E7 G02 P06 coverage for legacy cutover and integration."""

import subprocess
from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_sidebar_removes_parallel_analytical_shortcuts_but_keeps_project_surfaces() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "data-navigation-family=" not in html
    assert "data-navigation-stage=" not in html
    assert "legacy-analytical-shortcut" not in app
    for route in ("overview", "context", "data", "results"):
        assert f'data-route="{route}"' in html
    assert 'id="analysis-workspace-launcher"' in html


def test_legacy_urls_resource_routes_and_history_authority_remain_available() -> None:
    script = """
const fs = require('fs'); const vm = require('vm');
vm.runInThisContext(fs.readFileSync('frontend/navigation_state.js', 'utf8'));
const catalog = {families:[
  {slug:'exploratory',default_stage_id:'profile',stages:[{slug:'profile'}]},
  {slug:'predictive',default_stage_id:'setup',stages:[{slug:'setup'}]},
  {slug:'causal',default_stage_id:'setup',stages:[{slug:'setup'},{slug:'discovery'}]},
]};
const n = globalThis.AnalysisNavigation;
const legacy = n.legacyContext(catalog, 'p1', n.parse('/projects/p1/explore', catalog).legacy);
if (n.serialize(legacy) !== '/projects/p1/analysis/exploratory/profile') throw Error('legacy URL normalization');
const resource = n.parse('/projects/p1/analysis/causal/discovery/resource/result/r1', catalog);
if (n.serialize(resource) !== '/projects/p1/analysis/causal/discovery/resource/result/r1') throw Error('resource route');
"""
    subprocess.run(["node", "-e", script], cwd=REPOSITORY, check=True)

    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    assert "source:'legacy-route-normalization'" in app
    assert "AnalysisNavigation.contextForResource" in app
    assert "window.addEventListener('popstate',()=>restoreProjectRoute()" in app
    assert "activateWorkspace('management')" in app
    assert "activateWorkspace('results')" in app


def test_browser_runner_exercises_project_launcher_and_history_reload() -> None:
    runner = (REPOSITORY / "tests/browser_e2e/run_enh_e7_project_integration.py").read_text(encoding="utf-8")

    assert "project-analysis-launcher" in runner
    assert "data-open-analysis-family=\"exploratory\"" in runner
    assert "page.reload" in runner and "page.go_back" in runner and "page.go_forward" in runner
