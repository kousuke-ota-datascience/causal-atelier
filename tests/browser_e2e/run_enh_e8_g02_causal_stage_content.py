"""Real Chromium candidate coverage for ENH-E8 G02 P02 Causal Stage surfaces."""

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
    "tests/browser_e2e/run_enh_e8_g02_causal_stage_content.py"
)
STAGES = ("identification", "estimation", "effects", "diagnostics", "sensitivity")
WRONG_STAGE_PRIMARY = {
    "identification": ("#estimation-inputs", "#refutation-form", "#sensitivity-form"),
    "estimation": ("#identification-inputs", "#refutation-form", "#sensitivity-form"),
    "effects": ("#identification-inputs", "#estimation-inputs", "#refutation-form", "#sensitivity-form"),
    "diagnostics": ("#identification-inputs", "#estimation-inputs", "#treatment-effect-results", "#refutation-form"),
    "sensitivity": ("#identification-inputs", "#estimation-inputs", "#treatment-effect-results", "#diagnostics-results"),
}


def _request(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        f"{API}{path}", data=data,
        headers={"Content-Type": "application/json"} if payload is not None else {}, method=method,
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def _assert_stage(page: Page, project_id: str, stage: str, labels: dict[str, str]) -> None:
    expected_path = f"/projects/{project_id}/analysis/causal/{stage}"
    page.wait_for_function("expected => location.pathname === expected", arg=expected_path, timeout=30_000)
    page.wait_for_function(
        "expected => document.querySelector('#analysis-stage-contents .analysis-stage-heading')?.textContent === expected",
        arg=labels[stage], timeout=30_000,
    )
    assert page.locator("#analysis-stage-contents .analysis-stage-heading").inner_text() == labels[stage]
    assert page.locator(f'#analysis-stage-sidebar button[data-stage="{stage}"][aria-current="page"]').is_visible()
    for selector in WRONG_STAGE_PRIMARY[stage]:
        assert not page.locator(selector).is_visible(), f"{stage} exposed {selector}"


def _assert_estimation_submit_bypasses_hidden_identification_validation(page: Page) -> dict[str, Any]:
    button = page.locator("#run-estimation")
    button.wait_for(state="visible", timeout=30_000)
    invalid = page.evaluate("""() => [...document.querySelectorAll('#inference-form :invalid')].map(el => ({
        name: el.name,
        required: el.required,
        hiddenByStage: Boolean(el.closest('[hidden]')),
    }))""")
    hidden_invalid = {item["name"] for item in invalid if item["hiddenByStage"]}
    assert {"dataset_version_id", "graph_version_id"}.issubset(hidden_invalid), invalid
    assert page.locator("#run-estimation").get_attribute("type") == "button"

    button.click()
    page.locator("#notice").filter(has_text="Identification Resultを選択してください").wait_for(
        timeout=10_000
    )
    return {"status": "PASS", "hidden_invalid_controls": sorted(hidden_invalid)}


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    evidence_path = OUTPUT / "enh-e8-g02-causal-stage-content-evidence.json"
    project = _request("POST", "/projects", {
        "name": f"ENH-E8 G02 Causal Stage {int(time.time())}", "topic": "Causal stage surfaces",
        "objective": "Verify stage-specific Causal presentation in Chromium", "memo": "P02 browser candidate",
    })
    project_id = project["project_id"]
    catalog = _request("GET", "/navigation/analysis")
    causal = next(family for family in catalog["families"] if family["slug"] == "causal")
    labels = {stage["slug"]: stage["label"] for stage in causal["stages"]}
    evidence: dict[str, Any] = {"schema_version": "enh-e8-g02-browser-evidence/1", "command": COMMAND,
                                "project_id": project_id, "start_time": datetime.now(timezone.utc).isoformat(), "stages": {}}
    outcome = "FAIL"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto(f"{WEB}/projects/{project_id}/analysis/causal/{STAGES[0]}", wait_until="networkidle")
            page.locator("#health").filter(has_text="API READY").wait_for(timeout=30_000)
            for stage in STAGES:
                _assert_stage(page, project_id, stage, labels)
                evidence["stages"][stage] = {"status": "PASS", "route": page.url}
                if stage == "estimation":
                    evidence["estimation_submit_regression"] = (
                        _assert_estimation_submit_bypasses_hidden_identification_validation(page)
                    )
                if stage != STAGES[-1]:
                    next_stage = STAGES[STAGES.index(stage) + 1]
                    page.locator(f'#analysis-stage-sidebar button[data-stage="{next_stage}"]').click()
            page.go_back(wait_until="networkidle")
            _assert_stage(page, project_id, "diagnostics", labels)
            page.go_forward(wait_until="networkidle")
            _assert_stage(page, project_id, "sensitivity", labels)
            page.screenshot(path=OUTPUT / "enh-e8-g02-causal-stage-content.png", full_page=True)
            outcome = "PASS"
        except Exception as error:
            evidence["failure"] = repr(error)
            page.screenshot(path=OUTPUT / "enh-e8-g02-causal-stage-content-failure.png", full_page=True)
            raise
        finally:
            evidence["status"] = outcome
            evidence["end_time"] = datetime.now(timezone.utc).isoformat()
            evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")
            context.close()
            browser.close()
    print(json.dumps({"status": outcome, "evidence": str(evidence_path)}, sort_keys=True))
    return 0 if outcome == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
