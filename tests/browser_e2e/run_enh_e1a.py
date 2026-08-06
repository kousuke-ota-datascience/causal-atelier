"""Real Chromium acceptance runner for E2E-04, E2E-05, E2E-06, and E1a."""

from __future__ import annotations

import json
import os
import platform
import tempfile
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from playwright.sync_api import Page, sync_playwright


WEB = os.getenv("ARIADNE_E2E_WEB_URL", "http://127.0.0.1:8080")
API = os.getenv("ARIADNE_E2E_API_URL", "http://127.0.0.1:8000/api/v1")
ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(os.getenv("ARIADNE_E2E_OUTPUT_DIR", ROOT / "test-results/browser_e2e"))
DAG = {
    "graph_type": "DAG",
    "nodes": ["x", "treatment", "outcome"],
    "edges": [
        {"source": "x", "target": "treatment", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
        {"source": "x", "target": "outcome", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
        {"source": "treatment", "target": "outcome", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
    ],
}


def _get(path: str) -> dict[str, Any]:
    with urllib.request.urlopen(f"{API}{path}", timeout=10) as response:
        return json.load(response)


def _wait(predicate: Callable[[], Any], timeout: float = 60) -> Any:
    deadline = time.monotonic() + timeout
    last: Any = None
    while time.monotonic() < deadline:
        try:
            last = predicate()
            if last:
                return last
        except Exception as exc:  # pragma: no cover - failure evidence retains the exception
            last = exc
        time.sleep(0.5)
    raise AssertionError(f"Timed out; last observation: {last!r}")


def _executions(project_id: str) -> list[dict[str, Any]]:
    return _get(f"/projects/{project_id}/executions")["items"]


def _wait_new_executions(
    project_id: str, before: set[str], operation: str, count: int,
) -> list[dict[str, Any]]:
    def ready():  # type: ignore[no-untyped-def]
        values = [
            item for item in _executions(project_id)
            if item["execution_id"] not in before and item["operation"] == operation
        ]
        return values if len(values) == count and all(item["status"] == "SUCCEEDED" for item in values) else None
    return _wait(ready, timeout=120)


def _results(execution_id: str) -> list[dict[str, Any]]:
    return _get(f"/executions/{execution_id}/results")["items"]


def _nav(page: Page, workspace: str) -> None:
    button = page.locator(f'nav button[data-workspace="{workspace}"]')
    button.click()
    page.locator(f"#{workspace}.workspace.active").wait_for()
    _wait(lambda: button.get_attribute("data-refresh-status") in {"done", "failed"})
    assert button.get_attribute("data-refresh-status") == "done"


def _refresh(page: Page, selector: str) -> None:
    button = page.locator(selector)
    button.click()
    _wait(lambda: button.get_attribute("data-refresh-status") in {"done", "failed"})
    assert button.get_attribute("data-refresh-status") == "done"


def _upload(page: Page, project_id: str, name: str, content: str) -> str:
    _nav(page, "data")
    before = {item["dataset_version_id"] for item in _get(f"/projects/{project_id}/dataset-versions")["items"]}
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as handle:
        handle.write(content)
        source = Path(handle.name)
    try:
        form = page.locator("#dataset-form")
        form.locator('input[name="file"]').set_input_files(source)
        form.locator('input[name="dataset_key"]').fill(name)
        form.locator('input[name="version_label"]').fill("v1")
        form.locator('input[name="name"]').fill(name)
        form.locator('textarea[name="source_note"]').fill("ENH-E1a browser acceptance synthetic fixture")
        form.locator("button").click()
        page.locator("#notice").filter(has_text="Dataset Version").wait_for()
    finally:
        source.unlink(missing_ok=True)
    return _wait(lambda: next((
        item["dataset_version_id"]
        for item in _get(f"/projects/{project_id}/dataset-versions")["items"]
        if item["dataset_version_id"] not in before
    ), None))


def _fill_inference(
    page: Page,
    *,
    dataset_id: str,
    graph_id: str,
    strategy: str = "BACKDOOR",
    adjustment: str = "x",
    mode: str = "EXPLORATORY",
) -> None:
    _nav(page, "inference")
    form = page.locator("#inference-form")
    form.locator('select[name="dataset_version_id"]').select_option(dataset_id)
    form.locator('select[name="graph_version_id"]').select_option(graph_id)
    form.locator('select[name="analysis_mode"]').select_option(mode)
    for name, value in {
        "population": "eligible rows", "comparator": "untreated",
        "treatment": "treatment", "outcome": "outcome", "analysis_unit": "id",
        "treatment_time": "t0", "outcome_window": "t1",
    }.items():
        form.locator(f'[name="{name}"]').fill(value)
    form.locator('select[name="estimand"]').select_option("ATE")
    form.locator('select[name="strategy"]').select_option(strategy)
    form.locator('input[name="adjustment"]').fill(adjustment)
    form.locator('textarea[name="assumptions"]').fill("Declared scientific assumptions")
    form.locator('input[name="override_reason"]').fill("")
    form.locator('select[name="base_execution_id"]').select_option("")
    form.locator('input[name="change_reason"]').fill("")


def _run_identification(page: Page, project_id: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    before = {item["execution_id"] for item in _executions(project_id)}
    page.locator("#run-identification").click()
    page.locator("#notice").filter(has_text="Identification").wait_for()
    execution = _wait_new_executions(project_id, before, "IDENTIFICATION", 1)[0]
    values = _results(execution["execution_id"])
    identification = next(item for item in values if item["result_type"] == "IDENTIFICATION_RESULT")
    eligibility = next(item for item in values if item["result_type"] == "DATA_ELIGIBILITY_RESULT")
    _refresh(page, "#refresh-inference")
    _wait(lambda: page.locator(
        f'#identification-results option[value="{identification["result_id"]}"]'
    ).count() == 1)
    return execution, identification, eligibility


def _select_estimators(page: Page, names: set[str]) -> None:
    for value in ("difference_in_means", "ols", "ipw", "aipw"):
        locator = page.locator(f'#inference-form input[name="estimators"][value="{value}"]')
        if locator.is_disabled():
            continue
        locator.set_checked(value in names)


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc)
    console: list[str] = []
    evidence: dict[str, Any] = {
        "command": "docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --build --rm browser-e2e",
        "start_time": started.isoformat(),
        "platform": platform.platform(),
        "scenarios": {},
    }
    outcome = "FAIL"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        evidence["browser"] = f"Chromium {browser.version}"
        context = browser.new_context(record_video_dir=OUTPUT / "video")
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        page.on("console", lambda message: console.append(f"{message.type}: {message.text}"))
        try:
            page.goto(WEB, wait_until="networkidle")
            page.locator("#health").filter(has_text="API READY").wait_for(timeout=30_000)
            project_name = f"ENH-E1a Browser {int(time.time())}"
            page.locator('#project-form input[name="name"]').fill(project_name)
            page.locator('#project-form input[name="topic"]').fill("E2E-04 to E2E-06")
            page.locator('#project-form textarea[name="objective"]').fill("Browser acceptance")
            page.locator("#project-form button").click()
            page.locator("#notice").filter(has_text="Project").wait_for()
            project_id = _wait(lambda: next((
                item["project_id"] for item in _get("/projects")["items"]
                if item["name"] == project_name
            ), None))
            evidence["project_id"] = project_id

            rows = ["id,x,treatment,outcome"]
            rows.extend(f"{index},{(index % 9) - 4},{index % 2},{2 * (index % 2) + 0.7 * ((index % 9) - 4) + (index % 5) / 10}" for index in range(1, 181))
            dataset_id = _upload(page, project_id, "continuous", "\n".join(rows) + "\n")

            # E2E-06: discovery output -> constraint-adjusted -> user-edited.
            _nav(page, "discovery")
            discovery_form = page.locator("#discovery-form")
            discovery_form.locator('select[name="dataset_version_id"]').select_option(dataset_id)
            discovery_form.locator('input[name="features"]').fill("x,treatment,outcome")
            before = {item["execution_id"] for item in _executions(project_id)}
            discovery_form.locator("button").click()
            page.locator("#notice").filter(has_text="Discovery").wait_for()
            discoveries = _wait_new_executions(project_id, before, "DISCOVERY", 3)
            _refresh(page, "#refresh-discovery")
            _wait(lambda: page.locator("#graph-source option").count() > 1)
            source_values = page.locator("#graph-source option").evaluate_all(
                "options => options.slice(1).map(option => option.value)"
            )
            page.locator("#graph-source").select_option(source_values[-1])
            endpoint_display = page.locator("#graph-editor").inner_text()
            assert "Type: CPDAG" in endpoint_display and ("TAIL" in endpoint_display or "ARROW" in endpoint_display)
            page.locator("#graph-rationale").fill("Preserve algorithm output and endpoint semantics")
            page.locator("#save-graph").click()
            page.locator("#notice").filter(has_text="provenance").wait_for()
            discovered_graph = _wait(lambda: next((
                item for item in _get(f"/projects/{project_id}/graph-versions")["items"]
                if item["graph_origin"] == "DISCOVERED"
            ), None))

            page.locator("#graph-parent").select_option(discovered_graph["graph_version_id"])
            page.locator("#graph-transform").select_option("CONSTRAINT_ADJUSTED")
            if page.locator("#graph-editor .edge button").count():
                page.locator("#graph-editor .edge button").first.click()
            else:
                page.locator("#edge-source").fill("x")
                page.locator("#edge-target").fill("treatment")
                page.locator("#add-edge").click()
            page.locator("#graph-rationale").fill("Apply a documented post-hoc constraint")
            page.locator("#save-graph").click()
            constrained = _wait(lambda: next((
                item for item in _get(f"/projects/{project_id}/graph-versions")["items"]
                if item["graph_origin"] == "CONSTRAINT_ADJUSTED"
            ), None))
            page.locator("#graph-parent").select_option(constrained["graph_version_id"])
            page.locator("#graph-transform").select_option("USER_EDITED")
            if page.locator("#graph-editor .edge button").count():
                page.locator("#graph-editor .edge button").first.click()
            else:
                page.locator("#edge-source").fill("treatment")
                page.locator("#edge-target").fill("outcome")
                page.locator("#add-edge").click()
            page.locator("#graph-rationale").fill("Domain expert edit with explicit rationale")
            page.locator("#save-graph").click()
            edited = _wait(lambda: next((
                item for item in _get(f"/projects/{project_id}/graph-versions")["items"]
                if item["graph_origin"] == "USER_EDITED"
            ), None))
            assert constrained["parent_graph_version_id"] == discovered_graph["graph_version_id"]
            assert edited["parent_graph_version_id"] == constrained["graph_version_id"]
            assert discovered_graph["graph_type"] == "CPDAG"
            page.screenshot(path=OUTPUT / "E2E-06-graph-provenance.png", full_page=True)
            evidence["scenarios"]["E2E-06"] = {
                "status": "PASS", "execution_ids": [item["execution_id"] for item in discoveries],
                "graph_version_ids": [discovered_graph["graph_version_id"], constrained["graph_version_id"], edited["graph_version_id"]],
            }

            # Register an explicit DAG without converting CPDAG/PAG.
            page.locator("#direct-graph-json").fill(json.dumps(DAG))
            page.locator("#direct-graph-name").fill("Domain DAG for identification")
            page.locator("#direct-graph-note").fill("Declared domain knowledge; independent of discovery orientation")
            page.locator("#save-direct-graph").click()
            page.locator("#notice").filter(has_text="Direct Graph").wait_for()
            dag = _wait(lambda: next((
                item for item in _get(f"/projects/{project_id}/graph-versions")["items"]
                if item["graph_origin"] == "USER_DEFINED" and item["graph_type"] == "DAG"
            ), None))
            graph_id = dag["graph_version_id"]

            # E2E-04 identification-first, two estimators, follow-ups, annotation, lineage.
            _fill_inference(page, dataset_id=dataset_id, graph_id=graph_id)
            identification_execution, identification, eligibility = _run_identification(page, project_id)
            assert identification["scientific_status"] == "IDENTIFIED"
            assert eligibility["scientific_status"] in {"PASS", "WARN"}
            page.locator("#identification-results").select_option(identification["result_id"])
            _select_estimators(page, {"ols", "ipw"})
            before = {item["execution_id"] for item in _executions(project_id)}
            page.locator("#inference-form button:not([type])").click()
            estimates = _wait_new_executions(project_id, before, "ESTIMATION", 2)
            _refresh(page, "#refresh-inference")
            effect_results = [
                next(item for item in _results(execution["execution_id"])
                     if item["result_type"] == "TREATMENT_EFFECT_RESULT")
                for execution in estimates
            ]
            for result in effect_results:
                page.locator(f'#inference-results input[value="{result["result_id"]}"]').check()
            page.locator("#compare-inference").click()
            _wait(lambda: "result_differences" in page.locator("#inference-comparison").inner_text())

            effect_id = next(
                result["result_id"] for result in effect_results
                if result["payload"]["estimator"] == "ipw"
            )
            page.locator('#refutation-form select[name="result_id"]').select_option(effect_id)
            before = {item["execution_id"] for item in _executions(project_id)}
            page.locator("#refutation-form button").click()
            refutation = _wait_new_executions(project_id, before, "REFUTATION", 1)[0]
            page.locator('#sensitivity-form select[name="result_id"]').select_option(effect_id)
            before = {item["execution_id"] for item in _executions(project_id)}
            page.locator("#sensitivity-form button").click()
            sensitivity = _wait_new_executions(project_id, before, "SENSITIVITY", 1)[0]

            _nav(page, "results")
            _wait(lambda: any(
                "SENSITIVITY_RESULT" in label
                for label in page.locator("#result-select option").all_inner_texts()
            ))
            page.locator("#result-select").select_option(effect_id)
            page.locator("#load-result").click()
            _wait(lambda: "IDENTIFICATION_RESULT" in page.locator("#lineage").inner_text())
            annotation = page.locator("#annotation-form")
            annotation.locator('textarea[name="statement"]').fill("Retain triangulated estimate")
            annotation.locator('textarea[name="rationale"]').fill("OLS and IPW agreement")
            annotation.locator('textarea[name="assumptions"]').fill("Exchangeability\nPositivity")
            annotation.locator('textarea[name="limitations"]').fill("Synthetic acceptance data")
            page.locator("#result-select").select_option(effect_id)
            annotation.locator("button").click()
            page.locator("#notice").filter(has_text="Annotation").wait_for()
            page.screenshot(path=OUTPUT / "E2E-04-identification-first.png", full_page=True)
            evidence["scenarios"]["E2E-04"] = {
                "status": "PASS", "dataset_version_id": dataset_id, "graph_version_id": graph_id,
                "execution_ids": [identification_execution["execution_id"], *[item["execution_id"] for item in estimates], refutation["execution_id"], sensitivity["execution_id"]],
                "result_ids": [identification["result_id"], *[item["result_id"] for item in effect_results]],
            }

            # FR-063 and FR-062 through browser form.
            _fill_inference(
                page, dataset_id=dataset_id, graph_id=graph_id, mode="CONFIRMATORY",
            )
            page.locator("#identification-results").select_option(identification["result_id"])
            _select_estimators(page, {"ols"})
            before = {item["execution_id"] for item in _executions(project_id)}
            page.locator("#inference-form button:not([type])").click()
            page.locator("#scientific-warnings").filter(has_text="POST_SELECTION_INFERENCE_RISK").wait_for()
            confirmatory = _wait_new_executions(project_id, before, "ESTIMATION", 1)[0]
            _refresh(page, "#refresh-inference")
            page.locator("#identification-results").select_option(identification["result_id"])
            page.locator("#base-executions").select_option(confirmatory["execution_id"])
            _select_estimators(page, {"ipw"})
            page.locator('#inference-form input[name="change_reason"]').fill("")
            page.locator("#inference-form button:not([type])").click()
            page.locator("#notice").filter(has_text="EXECUTION_CHANGE_REASON_REQUIRED").wait_for()
            page.locator('#inference-form input[name="change_reason"]').fill("Compare propensity-based revision")
            before = {item["execution_id"] for item in _executions(project_id)}
            page.locator("#inference-form button:not([type])").click()
            revised = _wait_new_executions(project_id, before, "ESTIMATION", 1)[0]
            assert revised["revision_context"]["base_execution_id"] == confirmatory["execution_id"]

            # RANDOMIZED with a valid pre-treatment covariate must identify.
            _fill_inference(page, dataset_id=dataset_id, graph_id=graph_id, strategy="RANDOMIZED", adjustment="x")
            randomized_execution, randomized, _ = _run_identification(page, project_id)
            assert randomized["scientific_status"] == "IDENTIFIED"

            # E2E-05: a missing confounder is a successful technical Execution and blocks estimation.
            _fill_inference(page, dataset_id=dataset_id, graph_id=graph_id, strategy="BACKDOOR", adjustment="")
            negative_execution, negative, _ = _run_identification(page, project_id)
            assert negative_execution["status"] == "SUCCEEDED" and negative["scientific_status"] == "NOT_IDENTIFIED"
            page.locator("#identification-results").select_option(negative["result_id"])
            _select_estimators(page, {"ols"})
            page.locator("#inference-form button:not([type])").click()
            page.locator("#notice").filter(has_text="IDENTIFICATION_NOT_ACCEPTABLE").wait_for()
            page.screenshot(path=OUTPUT / "E2E-05-non-identification.png", full_page=True)
            evidence["scenarios"]["E2E-05"] = {
                "status": "PASS", "execution_ids": [negative_execution["execution_id"]],
                "result_ids": [negative["result_id"]],
            }

            # Estimator outcome-type mismatch is explicit at submission.
            binary_rows = ["id,x,treatment,outcome"]
            binary_rows.extend(f"{index},{(index % 7) - 3},{index % 2},{(index // 2) % 2}" for index in range(1, 181))
            binary_dataset = _upload(page, project_id, "binary-outcome", "\n".join(binary_rows) + "\n")
            _fill_inference(page, dataset_id=binary_dataset, graph_id=graph_id)
            binary_execution, binary_identification, binary_eligibility = _run_identification(page, project_id)
            assert binary_execution["status"] == "SUCCEEDED" and binary_eligibility["payload"]["inferred_types"]["outcome"]["type"] == "BINARY"
            page.locator("#identification-results").select_option(binary_identification["result_id"])
            _select_estimators(page, {"ols"})
            page.locator("#inference-form button:not([type])").click()
            page.locator("#notice").filter(has_text="ESTIMATOR_OUTCOME_TYPE_INCOMPATIBLE").wait_for()

            page.screenshot(path=OUTPUT / "E1a-additional-browser-behaviors.png", full_page=True)
            evidence["scenarios"]["E1a-additional"] = {
                "status": "PASS",
                "execution_ids": [confirmatory["execution_id"], revised["execution_id"], randomized_execution["execution_id"], binary_execution["execution_id"]],
                "warnings": confirmatory["scientific_warnings"],
            }
            outcome = "PASS"
        except Exception:
            page.screenshot(path=OUTPUT / "failure.png", full_page=True)
            raise
        finally:
            context.tracing.stop(path=OUTPUT / "trace.zip")
            context.close()
            browser.close()
            evidence["console"] = console
            evidence["end_time"] = datetime.now(timezone.utc).isoformat()
            evidence["status"] = outcome
            (OUTPUT / "evidence.json").write_text(
                json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8"
            )
    print(json.dumps({"status": outcome, "evidence": str(OUTPUT / "evidence.json")}, sort_keys=True))
    return 0 if outcome == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
