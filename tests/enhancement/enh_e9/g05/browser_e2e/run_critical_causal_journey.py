"""Current-UI Chromium journey for the ENH-E9 G05 critical causal path.

This runner is deliberately not part of P01 verification.  G05 Independent
Verification runs it only after all blocking non-browser evidence has passed.
"""

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
EVIDENCE = OUTPUT / "enh-e9-g05-critical-causal-journey-evidence.json"
TRACE = OUTPUT / "enh-e9-g05-critical-causal-journey-trace.zip"
FAILURE = OUTPUT / "enh-e9-g05-critical-causal-journey-failure.png"


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


def _checkpoint(evidence: dict[str, Any], page: Page, name: str, stage: str) -> None:
    evidence["checkpoints"].append({"name": name, "route": page.url, "stage": stage})


def _executions(project_id: str) -> list[dict[str, Any]]:
    return _get(f"/projects/{project_id}/executions")["items"]


def _wait_new_executions(
    project_id: str, before: set[str], operation: str, count: int,
) -> list[dict[str, Any]]:
    def complete() -> list[dict[str, Any]] | None:
        items = [
            item for item in _executions(project_id)
            if item["execution_id"] not in before and item["operation"] == operation
        ]
        return items if len(items) == count and all(item["status"] == "SUCCEEDED" for item in items) else None

    return _wait(complete)


def _results(execution_id: str) -> list[dict[str, Any]]:
    return _get(f"/executions/{execution_id}/results")["items"]


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
        form.locator('input[name="dataset_key"]').fill("g05_browser")
        form.locator('input[name="version_label"]').fill("v1")
        form.locator('input[name="name"]').fill("G05 Browser Dataset")
        form.locator('textarea[name="source_note"]').fill("G05 critical causal journey fixture")
        form.locator("button:not([type])").click()
        page.locator("#notice").filter(has_text="Dataset Versionを登録しました").wait_for(timeout=30_000)
    finally:
        source.unlink(missing_ok=True)
    return _wait(lambda: next((
        item["dataset_version_id"]
        for item in _get(f"/projects/{project_id}/dataset-versions")["items"]
        if item["dataset_version_id"] not in before
    ), None))


def _run_discovery_and_adopt(page: Page, project_id: str, dataset_id: str) -> str:
    page.locator('#discovery-form select[name="dataset_version_id"]').select_option(dataset_id)
    page.locator("#open-feature-selector").click()
    page.locator("#feature-modal").wait_for(state="visible", timeout=30_000)
    for column in ("x", "treatment", "outcome"):
        page.locator(f'#feature-options input[value="{column}"]').check()
    page.locator("#confirm-features").click()
    page.locator('#discovery-form select[name="designated_outcome_node"]').select_option("outcome")
    page.locator('#discovery-form input[name="algorithms"][value="ges"]').uncheck()
    page.locator('#discovery-form input[name="alpha"]').fill("0.01,0.05")
    before = {item["execution_id"] for item in _executions(project_id)}
    page.locator("#discovery-form button:not([type])").click()
    page.locator("#notice").filter(has_text="2件のDiscoveryを受け付けました").wait_for(timeout=30_000)
    _wait_new_executions(project_id, before, "DISCOVERY", 2)
    page.locator("#refresh-discovery").click()
    page.wait_for_function("() => document.querySelector('#refresh-discovery').dataset.refreshStatus === 'done'", timeout=30_000)
    candidate = page.locator("#graph-candidates tr").filter(has_text="DISCOVERY_RESULT").first
    candidate.locator("button").click()
    page.locator("#graph-modal").wait_for(state="visible", timeout=30_000)
    page.locator("#graph-rationale").fill("Adopt selected Discovery candidate for G05 journey")
    page.locator("#adopt-graph").click()
    page.locator("#graph-modal-feedback").filter(has_text="採用済み:").wait_for(timeout=30_000)
    graph_id = _wait(lambda: next((
        item["graph_version_id"]
        for item in _get(f"/projects/{project_id}/graph-versions")["items"]
        if item["status"] == "FIXED" and item["designated_outcome_node"] == "outcome"
    ), None))
    page.locator("#close-graph-modal").click()
    return graph_id


def _fill_identification(page: Page, dataset_id: str, graph_id: str) -> None:
    form = page.locator("#inference-form")
    form.locator('select[name="dataset_version_id"]').select_option(dataset_id)
    form.locator('select[name="graph_version_id"]').select_option(graph_id)
    form.locator('select[name="analysis_mode"]').select_option("EXPLORATORY")
    for name, value in {
        "population": "eligible rows", "comparator": "untreated", "treatment": "treatment",
        "analysis_unit": "row", "treatment_time": "baseline", "outcome_window": "follow-up",
    }.items():
        form.locator(f'[name="{name}"]').fill(value)
    form.locator('select[name="estimand"]').select_option("ATE")
    form.locator('select[name="strategy"]').select_option("BACKDOOR")
    form.locator('input[name="adjustment"]').fill("x")
    form.locator('textarea[name="assumptions"]').fill("No unmeasured confounding")


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    evidence: dict[str, Any] = {
        "schema_version": "enh-e9-g05-browser-evidence/1",
        "command": "python tests/enhancement/enh_e9/g05/browser_e2e/run_critical_causal_journey.py",
        "start_time": datetime.now(timezone.utc).isoformat(),
        "checkpoints": [],
        "lineage": {},
        "status": "FAIL",
    }
    console: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(record_video_dir=OUTPUT / "enh-e9-g05-critical-causal-journey-video")
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        page.on("console", lambda message: console.append(f"{message.type}: {message.text}"))
        try:
            page.goto(f"{WEB}/", wait_until="networkidle")
            page.locator("#health").filter(has_text="API READY").wait_for(timeout=30_000)
            _route(page, "/projects", "projects")
            _checkpoint(evidence, page, "project-list", "projects")

            page.locator("#new-project").click()
            _route(page, "/projects/new", "project-new")
            register = page.locator("#project-register-form")
            register.locator('input[name="name"]').fill(f"ENH-E9 G05 Browser {int(time.time())}")
            register.locator('input[name="topic"]').fill("G05 critical causal journey")
            register.locator('textarea[name="objective"]').fill("Verify G01-G04 connected causal journey")
            register.locator('textarea[name="memo"]').fill("G05 Trial01 browser fixture")
            register.locator("button:not([type])").click()
            page.wait_for_function("() => /^\\/projects\\/[^/]+\\/overview$/.test(window.location.pathname)", timeout=30_000)
            project_id = page.locator("#project-select").input_value()
            assert project_id
            evidence["lineage"]["project_id"] = project_id
            _checkpoint(evidence, page, "project-created", "management")

            page.locator('nav button[data-route="data"]').click()
            _route(page, f"/projects/{project_id}/data", "data")
            dataset_id = _upload_dataset(page, project_id)
            evidence["lineage"]["dataset_version_id"] = dataset_id
            _checkpoint(evidence, page, "dataset-registered", "data")

            page.locator('nav button[data-route="overview"]').click()
            _route(page, f"/projects/{project_id}/overview", "management")
            page.locator('[data-open-analysis-family="causal"]').click()
            _route(page, f"/projects/{project_id}/analysis/causal/setup", "discovery")
            page.locator('#analysis-stage-sidebar button[data-stage="discovery"]').click()
            _route(page, f"/projects/{project_id}/analysis/causal/discovery", "discovery")
            graph_id = _run_discovery_and_adopt(page, project_id, dataset_id)
            evidence["lineage"]["graph_version_id"] = graph_id
            _checkpoint(evidence, page, "discovery-candidate-adopted-fixed", "discovery")

            page.locator('#analysis-stage-sidebar button[data-stage="identification"]').click()
            _route(page, f"/projects/{project_id}/analysis/causal/identification", "inference")
            _fill_identification(page, dataset_id, graph_id)
            assert page.locator("#inference-outcome").inner_text() == "outcome"
            before = {item["execution_id"] for item in _executions(project_id)}
            page.locator("#run-identification").click()
            page.locator("#notice").filter(has_text="Identificationを受け付けました").wait_for(timeout=30_000)
            identification_execution = _wait_new_executions(project_id, before, "IDENTIFICATION", 1)[0]
            identification_result = next(item for item in _results(identification_execution["execution_id"]) if item["result_type"] == "IDENTIFICATION_RESULT")
            page.locator("#refresh-inference").click()
            page.wait_for_function("() => document.querySelector('#refresh-inference').dataset.refreshStatus === 'done'", timeout=30_000)
            page.locator(f'#identification-results option[value="{identification_result["result_id"]}"]').wait_for(timeout=30_000)
            evidence["lineage"]["identification_execution_id"] = identification_execution["execution_id"]
            evidence["lineage"]["identification_result_id"] = identification_result["result_id"]
            _checkpoint(evidence, page, "identification-result-selected", "identification")

            page.locator('#analysis-stage-sidebar button[data-stage="estimation"]').click()
            _route(page, f"/projects/{project_id}/analysis/causal/estimation", "inference")
            page.locator("#identification-results").select_option(identification_result["result_id"])
            for estimator in ("difference_in_means", "ols", "ipw", "aipw"):
                page.locator(f'#inference-form input[name="estimators"][value="{estimator}"]').set_checked(estimator == "ipw")
            before = {item["execution_id"] for item in _executions(project_id)}
            page.locator("#run-estimation").click()
            page.locator("#notice").filter(has_text="1件のEstimationを受け付けました").wait_for(timeout=30_000)
            estimation_execution = _wait_new_executions(project_id, before, "ESTIMATION", 1)[0]
            results = _results(estimation_execution["execution_id"])
            effect = next(item for item in results if item["result_type"] == "TREATMENT_EFFECT_RESULT")
            diagnostics = next(item for item in results if item["result_type"] == "DIAGNOSTICS_RESULT")
            evidence["lineage"]["estimation_execution_id"] = estimation_execution["execution_id"]
            evidence["lineage"]["treatment_effect_result_id"] = effect["result_id"]
            evidence["lineage"]["diagnostics_result_id"] = diagnostics["result_id"]
            _checkpoint(evidence, page, "estimation-from-selected-identification-result", "estimation")

            page.locator('#analysis-stage-sidebar button[data-stage="effects"]').click()
            _route(page, f"/projects/{project_id}/analysis/causal/effects", "inference")
            page.locator("#refresh-effects").click()
            page.wait_for_function("() => document.querySelector('#refresh-effects').dataset.refreshStatus === 'done'", timeout=30_000)
            page.locator(f'#treatment-effect-results input[value="{effect["result_id"]}"]').wait_for(timeout=30_000)
            _checkpoint(evidence, page, "persisted-treatment-effect-presented", "effects")

            page.locator('#analysis-stage-sidebar button[data-stage="diagnostics"]').click()
            _route(page, f"/projects/{project_id}/analysis/causal/diagnostics", "inference")
            page.locator("#refresh-diagnostics").click()
            page.wait_for_function("() => document.querySelector('#refresh-diagnostics').dataset.refreshStatus === 'done'", timeout=30_000)
            page.locator(f'#diagnostics-results input[value="{diagnostics["result_id"]}"]').wait_for(timeout=30_000)
            _checkpoint(evidence, page, "persisted-diagnostics-presented", "diagnostics")
            assert not [value for value in console if value.startswith("error:")], console
            evidence["status"] = "PASS"
        except Exception as error:
            evidence["failure"] = {
                "error": repr(error), "route": page.url,
                "last_checkpoint": evidence["checkpoints"][-1] if evidence["checkpoints"] else None,
            }
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
