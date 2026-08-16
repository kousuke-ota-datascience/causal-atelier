"""Focused ENH-E7 G01 P07 coverage for project integration and browser regression."""

import subprocess
from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_project_route_restore_preserves_legacy_analytical_route_compatibility() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "LEGACY_PROJECT_WORKSPACES=Object.freeze" in app
    assert "(context|data|explore|causal|predictive|results)" in app
    assert "await activateWorkspace(LEGACY_PROJECT_WORKSPACES[workspace],{push:false});" in app
    assert "source:'legacy-analytical-shortcut'" not in app


def test_frontend_navigation_scripts_are_syntactically_valid_javascript() -> None:
    for source in ("frontend/app.js", "frontend/project_navigation.js"):
        subprocess.run(["node", "--check", source], cwd=REPOSITORY, check=True)


def test_browser_runner_covers_create_project_routes_history_reload_and_analysis_launcher() -> None:
    runner = (REPOSITORY / "tests/browser_e2e/run_enh_e7_project_integration.py").read_text(encoding="utf-8")
    dockerfile = (REPOSITORY / "Dockerfile.browser-e2e").read_text(encoding="utf-8")
    ignored = (REPOSITORY / ".dockerignore").read_text(encoding="utf-8")

    assert "run_enh_e7_project_integration.py" in dockerfile
    assert "!tests/browser_e2e/run_enh_e7_project_integration.py" in ignored
    assert "create-to-overview" in runner
    assert "project-routes-reload-history" in runner
    assert "page.reload" in runner and "page.go_back" in runner and "page.go_forward" in runner
    assert "project-analysis-launcher" in runner
