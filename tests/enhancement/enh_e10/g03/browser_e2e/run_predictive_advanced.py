"""Hermetic Chromium journeys for ENH-E10 G03 predictive advanced flows."""

from __future__ import annotations

import json
import os
import tempfile
import time
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from playwright.sync_api import Page, sync_playwright


WEB = os.getenv("ARIADNE_E2E_WEB_URL", "http://127.0.0.1:8080")
API = os.getenv("ARIADNE_E2E_API_URL", "http://127.0.0.1:8000/api/v1")
OUTPUT = Path(os.getenv("ARIADNE_E2E_OUTPUT_DIR", "test-results/browser_e2e")) / "enh_e10"


def _request(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(f"{API}{path}", data=data, method=method)
    if data is not None:
        request.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def _wait(predicate: Callable[[], Any], timeout: float = 150) -> Any:
    deadline, last = time.monotonic() + timeout, None
    while time.monotonic() < deadline:
        try:
            last = predicate()
            if last:
                return last
        except Exception as error:  # retained in failure evidence
            last = error
        time.sleep(0.5)
    raise AssertionError(f"timed out; last observation: {last!r}")


def _post_dataset(project_id: str, rows: str) -> str:
    boundary = f"e10-{uuid.uuid4().hex}"
    parts: list[bytes] = []
    for name, value in {"dataset_key": "e10", "version_label": "v1", "name": "E10 browser"}.items():
        parts.extend([f"--{boundary}\r\n".encode(), f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(), value.encode(), b"\r\n"])
    parts.extend([f"--{boundary}\r\n".encode(), b'Content-Disposition: form-data; name="file"; filename="e10.csv"\r\nContent-Type: text/csv\r\n\r\n', rows.encode(), b"\r\n", f"--{boundary}--\r\n".encode()])
    request = urllib.request.Request(f"{API}/projects/{project_id}/dataset-versions", data=b"".join(parts), method="POST", headers={"Content-Type": f"multipart/form-data; boundary={boundary}", "Idempotency-Key": uuid.uuid4().hex})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["dataset_version_id"]


def _workspace(regression: bool) -> tuple[str, str, str]:
    project = _request("POST", "/projects", {"name": f"E10 G03 {time.time_ns()}", "topic": "predictive", "objective": "advanced browser"})
    project_id = project["project_id"]
    rows = ["score,converted"] + [f"{value},{float(3 * value - 2) if regression else int(value >= 0)}" for value in range(-80, 80)]
    dataset_id = _post_dataset(project_id, "\n".join(rows) + "\n")
    context = _request("POST", f"/projects/{project_id}/research-contexts", {"context_key": "e10", "problem_statement": "predict", "research_questions": ["predict"], "significance": None, "hypotheses": [], "decision_context": {"action": "prioritize"}, "relations": []})
    context_id = context["research_context_version_id"]
    _request("POST", f"/projects/{project_id}/research-contexts/{context_id}/fix")
    return project_id, dataset_id, context_id


def _terminal_execution(project_id: str) -> dict[str, Any] | None:
    items = _request("GET", f"/projects/{project_id}/executions")["items"]
    return next((item for item in items if item.get("analysis_family") == "PREDICTIVE" and item["status"] in {"SUCCEEDED", "FAILED"}), None)


def _stage_failure_evidence(project_id: str, execution_id: str) -> list[dict[str, Any]]:
    stages = _request("GET", f"/projects/{project_id}/executions/{execution_id}/stages")["items"]
    return [
        {
            "stage_key": stage["stage_key"],
            "status": stage["status"],
            "last_error": stage.get("last_error"),
            "attempt_history": stage.get("attempt_history", []),
        }
        for stage in stages
    ]


def _stage(page: Page, stage: str) -> None:
    page.locator(f'#analysis-stage-sidebar button[data-stage="{stage}"]').click()
    page.locator(f'[data-predictive-stage-surface~="{stage}"]:visible').first.wait_for(timeout=30_000)


def _journey(page: Page, *, regression: bool, evidence: dict[str, Any]) -> None:
    project_id, dataset_id, context_id = _workspace(regression)
    page.goto(f"{WEB}/projects/{project_id}/analysis/predictive/setup", wait_until="networkidle")
    page.locator("#health").filter(has_text="API READY").wait_for(timeout=30_000)
    page.locator("#predictive-context").select_option(context_id)
    page.locator('#predictive-form select[name="dataset_version_id"]').select_option(dataset_id)
    if regression:
        page.locator('#predictive-form select[name="task_type"]').select_option("REGRESSION")
    _stage(page, "train")
    page.locator('#predictive-form select[name="model_id"]:visible').select_option(
        "lightgbm_regressor.v1" if regression else "lightgbm_classifier.v1"
    )
    _stage(page, "explainability")
    page.locator('#predictive-form select[name="explanation_method"]:visible').select_option(
        "LIME_TABULAR" if regression else "SHAP_TREE"
    )
    _stage(page, "train")
    page.locator('#run-predictive:visible').click()
    execution = _wait(lambda: _terminal_execution(project_id))
    scenario = "110" if regression else "100"
    stages = _stage_failure_evidence(project_id, execution["execution_id"])
    evidence["scenarios"][scenario] = {
        "status": execution["status"],
        "execution_id": execution["execution_id"],
        "stages": stages,
    }
    assert execution["status"] == "SUCCEEDED", {
        "terminal_error": execution.get("last_error_summary"),
        "stages": stages,
    }
    page.locator("#notice").filter(has_text="Model Cardを保存しました").wait_for(timeout=30_000)
    results = _request("GET", f"/projects/{project_id}/executions/{execution['execution_id']}/results")["items"]
    artifacts = _request("GET", f"/projects/{project_id}/executions/{execution['execution_id']}/artifacts")["items"]
    by_type = {item["result_type"]: item for item in results}
    assert by_type["PREDICTIVE_EXPLANATION_RESULT"]["analytical_status"] == "GENERATED"
    assert by_type["MODEL_CARD_RESULT"]["payload"].get("model_descriptor", {}).get("model_id")
    assert {"PREDICTIVE_EXPLANATION", "MODEL_CARD", "FITTED_MODEL"} <= {item["artifact_type"] for item in artifacts}
    assert "Predictive Explanation ≠ Causal Explanation" in page.locator(".predictive-terminology").inner_text()
    evidence["scenarios"][scenario].update({
        "status": "PASS",
        "result_types": list(by_type),
        "artifact_types": [item["artifact_type"] for item in artifacts],
    })


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    evidence: dict[str, Any] = {"schema_version": "enh-e10-g03-browser-evidence/1", "command": "python tests/enhancement/enh_e10/g03/browser_e2e/run_predictive_advanced.py", "started_at": datetime.now(timezone.utc).isoformat(), "status": "FAIL", "scenarios": {}}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(record_video_dir=OUTPUT / "video")
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        try:
            _journey(page, regression=False, evidence=evidence)
            _journey(page, regression=True, evidence=evidence)
            evidence["status"] = "PASS"
        except Exception as error:
            evidence["failure"] = {"type": type(error).__name__, "message": str(error), "url": page.url}
            page.screenshot(path=OUTPUT / "failure.png", full_page=True)
            raise
        finally:
            context.tracing.stop(path=OUTPUT / "trace.zip")
            context.close(); browser.close()
            (OUTPUT / "evidence.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
