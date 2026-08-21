"""Real Chromium candidate coverage for ENH-E8 G02 P03 Predictive Stage content."""

from __future__ import annotations

import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright


WEB = os.getenv("ARIADNE_E2E_WEB_URL", "http://127.0.0.1:8080")
API = os.getenv("ARIADNE_E2E_API_URL", "http://127.0.0.1:8000/api/v1")
ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(os.getenv("ARIADNE_E2E_OUTPUT_DIR", ROOT / "test-results/browser_e2e"))
STAGES = ("setup", "train", "predict", "metrics", "explainability", "model-management")


def _request(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(payload).encode() if payload else None
    request = urllib.request.Request(f"{API}{path}", data=data, method=method,
                                     headers={"Content-Type": "application/json"} if payload else {})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    evidence_path = OUTPUT / "enh-e8-g02-predictive-stage-content-evidence.json"
    project_id = _request("POST", "/projects", {"name": f"ENH-E8 P03 {int(time.time())}", "topic": "Predictive Stage", "objective": "Chromium presentation check", "memo": "P03"})["project_id"]
    catalog = _request("GET", "/navigation/analysis")
    predictive = next(family for family in catalog["families"] if family["slug"] == "predictive")
    labels = {stage["slug"]: stage["label"] for stage in predictive["stages"]}
    evidence: dict[str, Any] = {"project_id": project_id, "started": datetime.now(timezone.utc).isoformat(), "stages": {}}
    outcome = "FAIL"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto(f"{WEB}/projects/{project_id}/analysis/predictive/setup", wait_until="networkidle")
            page.locator("#health").filter(has_text="API READY").wait_for(timeout=30_000)
            assert page.locator("#open-predictive-feature-selector").is_disabled()
            assert "利用できません" in page.locator("#predictive-feature-selector-status").inner_text()
            for stage in STAGES:
                page.wait_for_function("expected => location.pathname === expected", arg=f"/projects/{project_id}/analysis/predictive/{stage}")
                page.wait_for_function(
                    "expected => document.querySelector('#analysis-stage-contents .analysis-stage-heading')?.textContent === expected",
                    arg=labels[stage], timeout=30_000,
                )
                assert page.locator("#analysis-stage-contents .analysis-stage-heading").inner_text() == labels[stage]
                evidence["stages"][stage] = {"route": page.url, "status": "PASS"}
                if stage != STAGES[-1]:
                    next_stage = STAGES[STAGES.index(stage) + 1]
                    page.locator(f'#analysis-stage-sidebar button[data-stage="{next_stage}"]').click()
            page.go_back(wait_until="networkidle")
            assert page.url.endswith("/predictive/explainability")
            page.go_forward(wait_until="networkidle")
            assert page.url.endswith("/predictive/model-management")
            outcome = "PASS"
        finally:
            evidence["status"] = outcome
            evidence["ended"] = datetime.now(timezone.utc).isoformat()
            evidence_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
            context.close(); browser.close()
    print(json.dumps({"status": outcome, "evidence": str(evidence_path)}))
    return 0 if outcome == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
