"""Current-UI Chromium journey required by ENH-E9 G02 frozen verification."""

from __future__ import annotations

import json
import os
import tempfile
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from playwright.sync_api import Page, sync_playwright


WEB = os.getenv("ARIADNE_E2E_WEB_URL", "http://127.0.0.1:8080")
API = os.getenv("ARIADNE_E2E_API_URL", "http://127.0.0.1:8000/api/v1")
ROOT = next(
    (parent for parent in Path(__file__).resolve().parents if (parent / "pyproject.toml").is_file()),
    Path("/workspace"),
)
OUTPUT = Path(os.getenv("ARIADNE_E2E_OUTPUT_DIR", ROOT / "test-results/browser_e2e"))
EVIDENCE = OUTPUT / "enh-e9-g02-discovery-candidate-adoption-evidence.json"
TRACE = OUTPUT / "enh-e9-g02-discovery-candidate-adoption-trace.zip"
FAILURE = OUTPUT / "enh-e9-g02-discovery-candidate-adoption-failure.png"


def _get(path: str) -> dict[str, Any]:
    with urllib.request.urlopen(f"{API}{path}", timeout=20) as response:
        return json.load(response)


def _wait(predicate: Callable[[], Any], timeout: float = 120) -> Any:
    deadline = time.monotonic() + timeout
    last: Any = None
    while time.monotonic() < deadline:
        try:
            last = predicate()
            if last:
                return last
        except Exception as error:  # pragma: no cover - retained in failure evidence
            last = error
        time.sleep(0.5)
    raise AssertionError(f"timed out; last observation: {last!r}")


def _route(page: Page, expected: str, workspace: str) -> None:
    page.wait_for_function("expected => window.location.pathname === expected", arg=expected, timeout=30_000)
    page.locator(f"#{workspace}.workspace.active").wait_for(timeout=30_000)


def _upload_dataset(page: Page, project_id: str) -> str:
    before = {item["dataset_version_id"] for item in _get(f"/projects/{project_id}/dataset-versions")["items"]}
    rows = ["x,treatment,outcome"]
    rows.extend(f"{index % 7},{index % 2},{2 * (index % 2) + (index % 7) / 10}" for index in range(1, 181))
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as handle:
        handle.write("\n".join(rows) + "\n")
        source = Path(handle.name)
    try:
        form = page.locator("#dataset-form")
        form.locator('input[name="file"]').set_input_files(source)
        form.locator('input[name="dataset_key"]').fill("g02_browser")
        form.locator('input[name="version_label"]').fill("v1")
        form.locator('input[name="name"]').fill("G02 Browser Dataset")
        form.locator('textarea[name="source_note"]').fill("Current UI G02 browser fixture")
        form.locator("button:not([type])").click()
        page.locator("#notice").filter(has_text="Dataset Versionを登録しました").wait_for(timeout=30_000)
    finally:
        source.unlink(missing_ok=True)
    return _wait(lambda: next((
        item["dataset_version_id"]
        for item in _get(f"/projects/{project_id}/dataset-versions")["items"]
        if item["dataset_version_id"] not in before
    ), None))


def _wait_discovery(project_id: str, before: set[str]) -> list[dict[str, Any]]:
    def complete() -> list[dict[str, Any]] | None:
        executions = [
            item for item in _get(f"/projects/{project_id}/executions")["items"]
            if item["execution_id"] not in before and item["operation"] == "DISCOVERY"
        ]
        return executions if len(executions) == 2 and all(item["status"] == "SUCCEEDED" for item in executions) else None

    return _wait(complete)


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    evidence: dict[str, Any] = {
        "schema_version": "enh-e9-g02-browser-evidence/1",
        "command": "python tests/enhancement/enh_e9/g02/browser_e2e/run_discovery_candidate_adoption.py",
        "start_time": datetime.now(timezone.utc).isoformat(),
        "checkpoints": [],
        "scenarios": {},
        "status": "FAIL",
    }
    console: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(record_video_dir=OUTPUT / "enh-e9-g02-discovery-candidate-adoption-video")
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        page.on("console", lambda message: console.append(f"{message.type}: {message.text}"))
        try:
            page.goto(f"{WEB}/", wait_until="networkidle")
            page.locator("#health").filter(has_text="API READY").wait_for(timeout=30_000)
            _route(page, "/projects", "projects")
            evidence["checkpoints"].append("project-list")

            page.locator("#new-project").click()
            _route(page, "/projects/new", "project-new")
            project_name = f"ENH-E9 G02 Browser {int(time.time())}"
            register = page.locator("#project-register-form")
            register.locator('input[name="name"]').fill(project_name)
            register.locator('input[name="topic"]').fill("G02 current-browser repair")
            register.locator('textarea[name="objective"]').fill("Verify discovery candidate adoption connectivity")
            register.locator('textarea[name="memo"]').fill("G02 Trial01 test-only browser fixture")
            register.locator("button:not([type])").click()
            page.wait_for_function("() => /^\\/projects\\/[^/]+\\/overview$/.test(window.location.pathname)", timeout=30_000)
            page.locator("#management.workspace.active").wait_for(timeout=30_000)
            project_id = page.locator("#project-select").input_value()
            assert project_id
            evidence["project_id"] = project_id
            evidence["checkpoints"].append("project-created")

            page.locator('nav button[data-route="data"]').click()
            _route(page, f"/projects/{project_id}/data", "data")
            dataset_id = _upload_dataset(page, project_id)
            evidence["dataset_version_id"] = dataset_id
            evidence["checkpoints"].append("dataset-registered")

            page.locator('nav button[data-route="overview"]').click()
            _route(page, f"/projects/{project_id}/overview", "management")
            page.locator('[data-open-analysis-family="causal"]').click()
            _route(page, f"/projects/{project_id}/analysis/causal/setup", "discovery")
            page.locator('#analysis-stage-sidebar button[data-stage="discovery"]').click()
            _route(page, f"/projects/{project_id}/analysis/causal/discovery", "discovery")
            evidence["checkpoints"].append("current-analysis-discovery-route")

            page.wait_for_function(
                """datasetId => [...document.querySelector('#discovery-form select[name="dataset_version_id"]').options]
                    .some(option => option.value === datasetId)""",
                arg=dataset_id,
                timeout=30_000,
            )
            page.locator('#discovery-form select[name="dataset_version_id"]').select_option(dataset_id)
            page.locator("#open-feature-selector").click()
            page.locator("#feature-modal").wait_for(state="visible", timeout=30_000)
            for column in ("x", "treatment", "outcome"):
                page.locator(f'#feature-options input[value="{column}"]').check()
            page.locator("#confirm-features").click()
            page.locator('#discovery-form select[name="designated_outcome_node"]').select_option("outcome")
            page.locator('#discovery-form input[name="algorithms"][value="ges"]').uncheck()
            page.locator('#discovery-form input[name="alpha"]').fill("0.01,0.05")
            before = {item["execution_id"] for item in _get(f"/projects/{project_id}/executions")["items"]}
            page.locator("#discovery-form button:not([type])").click()
            page.locator("#notice").filter(has_text="2件のDiscoveryを受け付けました").wait_for(timeout=30_000)
            executions = _wait_discovery(project_id, before)
            page.locator("#refresh-discovery").click()
            page.wait_for_function("() => document.querySelector('#refresh-discovery').dataset.refreshStatus === 'done'", timeout=30_000)
            page.locator("#graph-candidates .candidate-check").nth(1).wait_for(timeout=30_000)
            evidence["scenarios"]["discovery-execution"] = {"status": "PASS", "execution_ids": [item["execution_id"] for item in executions]}
            evidence["checkpoints"].append("discovery-results-and-candidates")

            checks = page.locator("#graph-candidates .candidate-check")
            checks.nth(0).check()
            checks.nth(1).check()
            page.locator("#compare-discovery").click()
            page.locator("#graph-comparison-modal").wait_for(state="visible", timeout=30_000)
            assert page.locator("#comparison-tabs button").count() == 2
            page.locator("#comparison-summary").get_by_text("Current comparison candidate", exact=False).wait_for(timeout=30_000)
            evidence["scenarios"]["graph-comparison"] = {"status": "PASS", "candidate_count": 2}
            page.locator("#close-comparison-modal").click()
            evidence["checkpoints"].append("graph-comparison")

            page.locator("#graph-candidates tr").filter(has_text="DISCOVERY_RESULT").first.locator("button").click()
            page.locator("#graph-modal").wait_for(state="visible", timeout=30_000)
            page.locator("#graph-rationale").fill("Adopt current Discovery output without changing graph semantics")
            page.locator("#adopt-graph").click()
            page.locator("#graph-modal-feedback").filter(has_text="採用済み:").wait_for(timeout=30_000)
            feedback = page.locator("#graph-modal-feedback").inner_text()
            assert "FIXED" in feedback
            page.screenshot(path=OUTPUT / "enh-e9-g02-discovery-candidate-adoption.png", full_page=True)
            evidence["scenarios"]["adopt-fixed-graph"] = {"status": "PASS", "feedback": feedback}
            evidence["checkpoints"].append("adopted-fixed-graph")
            assert not [value for value in console if value.startswith("error:")], console
            evidence["status"] = "PASS"
        except Exception as error:
            evidence["failure"] = repr(error)
            page.screenshot(path=FAILURE, full_page=True)
            raise
        finally:
            context.tracing.stop(path=TRACE)
            context.close()
            browser.close()
            evidence["console"] = console
            evidence["end_time"] = datetime.now(timezone.utc).isoformat()
            EVIDENCE.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"status": evidence["status"], "evidence": str(EVIDENCE)}, sort_keys=True))
    return 0 if evidence["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
