"""Real Chromium coverage for ENH-E8 G01 Project List return navigation."""

from __future__ import annotations

import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, sync_playwright


WEB = os.getenv("ARIADNE_E2E_WEB_URL", "http://127.0.0.1:8080")
API = os.getenv("ARIADNE_E2E_API_URL", "http://127.0.0.1:8000/api/v1")
ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(os.getenv("ARIADNE_E2E_OUTPUT_DIR", ROOT / "test-results/browser_e2e"))
COMMAND = (
    "docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a "
    "--profile e2e run --build --rm --entrypoint python browser-e2e "
    "tests/browser_e2e/run_enh_e8_g01_project_return.py"
)
SECTIONS = (("overview", "management"), ("context", "context"), ("data", "data"), ("results", "results"))


def _request(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        f"{API}{path}", data=data,
        headers={"Content-Type": "application/json"} if data is not None else {}, method=method,
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def _active(page: Page, workspace: str) -> None:
    page.locator(f"#{workspace}.workspace.active").wait_for(timeout=30_000)
    page.wait_for_function(
        """() => [...document.querySelectorAll('[data-top-level-surface-root]')]
          .filter(root => !root.hidden).map(root => root.dataset.topLevelSurfaceRoot)
          .join(',') === 'project-management'""",
        timeout=30_000,
    )


def _project_return(page: Page, project_id: str, section: str, workspace: str) -> dict[str, str]:
    project_path = f"/projects/{project_id}/{section}"
    page.goto(f"{WEB}{project_path}", wait_until="networkidle")
    page.locator("#health").filter(has_text="API READY").wait_for(timeout=30_000)
    _active(page, workspace)
    action = page.get_by_role("button", name="Project Listへ戻る")
    assert action.count() == 1 and action.is_visible() and action.is_enabled()
    action.focus()
    page.keyboard.press("Enter")
    page.wait_for_function("() => window.location.pathname === '/projects'", timeout=30_000)
    page.locator("#projects.workspace.active").wait_for(timeout=30_000)
    page.go_back(wait_until="networkidle")
    page.wait_for_function("expected => window.location.pathname === expected", arg=project_path, timeout=30_000)
    _active(page, workspace)
    page.go_forward(wait_until="networkidle")
    page.wait_for_function("() => window.location.pathname === '/projects'", timeout=30_000)
    page.locator("#projects.workspace.active").wait_for(timeout=30_000)
    return {"direct_entry": project_path, "return_target": "/projects"}


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    evidence_path = OUTPUT / "enh-e8-g01-project-return-evidence.json"
    project = _request("POST", "/projects", {
        "name": f"ENH-E8 G01 Return {int(time.time())}", "topic": "Project return navigation",
        "objective": "Verify deterministic Project List navigation in Chromium", "memo": "ENH-E8 G01 fixture",
    })
    evidence: dict[str, Any] = {
        "schema_version": "enh-e8-g01-browser-evidence/1", "command": COMMAND,
        "start_time": datetime.now(timezone.utc).isoformat(), "project_id": project["project_id"], "scenarios": {},
    }
    outcome = "FAIL"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context()
        page = context.new_page()
        page_errors: list[str] = []
        page.on("pageerror", lambda error: page_errors.append(str(error)))
        try:
            for section, workspace in SECTIONS:
                evidence["scenarios"][f"direct-entry-{section}-return-back-forward"] = {
                    "status": "PASS", **_project_return(page, project["project_id"], section, workspace),
                }
            assert not page_errors, page_errors
            page.screenshot(path=OUTPUT / "enh-e8-g01-project-return.png", full_page=True)
            outcome = "PASS"
        except Exception as error:
            evidence["failure"] = repr(error)
            page.screenshot(path=OUTPUT / "enh-e8-g01-project-return-failure.png", full_page=True)
            raise
        finally:
            evidence["page_errors"] = page_errors
            evidence["end_time"] = datetime.now(timezone.utc).isoformat()
            evidence["status"] = outcome
            evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")
            context.close()
            browser.close()
    print(json.dumps({"status": outcome, "evidence": str(evidence_path)}, sort_keys=True))
    return 0 if outcome == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
