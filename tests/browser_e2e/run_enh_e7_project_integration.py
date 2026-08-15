"""Real Chromium regression coverage for ENH-E7 G01 Project surfaces."""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import Page, sync_playwright


WEB = os.getenv("ARIADNE_E2E_WEB_URL", "http://127.0.0.1:8080")
ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(os.getenv("ARIADNE_E2E_OUTPUT_DIR", ROOT / "test-results/browser_e2e"))
COMMAND = (
    "docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a "
    "--profile e2e run --build --rm --entrypoint python browser-e2e "
    "tests/browser_e2e/run_enh_e7_project_integration.py"
)


def _active(page: Page, workspace: str) -> None:
    page.locator(f"#{workspace}.workspace.active").wait_for(timeout=30_000)


def _route(page: Page, project_id: str, section: str, workspace: str) -> None:
    page.wait_for_function(
        "expected => window.location.pathname === expected", arg=f"/projects/{project_id}/{section}", timeout=30_000
    )
    _active(page, workspace)
    assert page.locator("#project-select").input_value() == project_id


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    evidence_path = OUTPUT / "enh-e7-project-integration-evidence.json"
    evidence: dict[str, object] = {
        "schema_version": "enh-e7-browser-evidence/1", "command": COMMAND,
        "start_time": datetime.now(timezone.utc).isoformat(), "scenarios": {},
    }
    outcome = "FAIL"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto(f"{WEB}/projects", wait_until="networkidle")
            page.locator("#health").filter(has_text="API READY").wait_for(timeout=30_000)
            _active(page, "projects")
            page.screenshot(path=OUTPUT / "enh-e7-g03-p06-projects.png", full_page=True)
            page.locator("#new-project").click()
            page.wait_for_function("() => window.location.pathname === '/projects/new'", timeout=30_000)
            _active(page, "project-new")
            project_name = f"ENH-E7 Project Browser {int(time.time())}"
            form = page.locator("#project-register-form")
            form.locator('[name="name"]').fill(project_name)
            form.locator('[name="topic"]').fill("Project surface integration")
            form.locator('[name="objective"]').fill("Verify project routes in Chromium")
            form.locator("button:not([type])").click()
            page.wait_for_function(
                "() => /^\\/projects\\/[^/]+\\/overview$/.test(window.location.pathname)", timeout=30_000
            )
            _active(page, "management")
            page.screenshot(path=OUTPUT / "enh-e7-g03-p06-project-management.png", full_page=True)
            project_id = page.locator("#project-select").input_value()
            assert project_id
            evidence["scenarios"] = {"create-to-overview": {"status": "PASS", "project_id": project_id}}

            for section, workspace in (("context", "context"), ("data", "data"), ("results", "results")):
                page.locator(f'nav button[data-route="{section}"]').click()
                _route(page, project_id, section, workspace)
            page.reload(wait_until="networkidle")
            _route(page, project_id, "results", "results")
            page.go_back(wait_until="networkidle")
            _route(page, project_id, "data", "data")
            page.go_forward(wait_until="networkidle")
            _route(page, project_id, "results", "results")
            evidence["scenarios"]["project-routes-reload-history"] = {"status": "PASS"}

            page.locator('nav button[data-route="overview"]').click()
            _route(page, project_id, "overview", "management")
            page.locator('[data-open-analysis-family="exploratory"]').click()
            page.wait_for_function(
                "expected => window.location.pathname === expected",
                arg=f"/projects/{project_id}/analysis/exploratory/profile", timeout=30_000,
            )
            _active(page, "explore")
            page.screenshot(path=OUTPUT / "enh-e7-g03-p06-analysis.png", full_page=True)
            evidence["scenarios"]["project-analysis-launcher"] = {"status": "PASS"}
            outcome = "PASS"
        except Exception as error:
            evidence["failure"] = repr(error)
            page.screenshot(path=OUTPUT / "enh-e7-project-integration-failure.png", full_page=True)
            raise
        finally:
            evidence["end_time"] = datetime.now(timezone.utc).isoformat()
            evidence["status"] = outcome
            evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")
            context.close(); browser.close()
    print(json.dumps({"status": outcome, "evidence": str(evidence_path)}, sort_keys=True))
    return 0 if outcome == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
