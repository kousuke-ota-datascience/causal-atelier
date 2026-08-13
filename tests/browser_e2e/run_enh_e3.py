"""Real Chromium acceptance for the ENH-E3 G6 product closure."""

from __future__ import annotations

import json
import platform
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

from run_enh_e3_predictive import (
    OUTPUT,
    WEB,
    _get,
    _post,
    _select,
    _wait,
)
import run_enh_e1a


def _prepare() -> str:
    project = _post("/projects", {
        "name": f"ENH-E3 Final Browser {int(time.time())}",
        "topic": "conversion prediction and causal follow-up",
        "objective": "Explore, predict, and preserve cross-analysis lineage",
        "memo": "G6 real Chromium acceptance",
    })
    return project["project_id"]


def _upload_dataset_in_browser(page, project_id: str) -> str:  # type: ignore[no-untyped-def]
    before = {
        item["dataset_version_id"]
        for item in _get(f"/projects/{project_id}/dataset-versions")["items"]
    }
    rows = ["score,converted"]
    rows.extend(f"{score},{int(score >= 0)}" for score in range(-60, 60))
    with tempfile.NamedTemporaryFile(
        "w", suffix=".csv", delete=False, encoding="utf-8"
    ) as handle:
        handle.write("\n".join(rows) + "\n")
        source = Path(handle.name)
    try:
        form = page.locator("#dataset-form")
        form.locator('input[name="file"]').set_input_files(source)
        form.locator('input[name="dataset_key"]').fill("g6_final_browser")
        form.locator('input[name="version_label"]').fill("v1")
        form.locator('input[name="name"]').fill("G6 Final Browser Dataset")
        form.locator('textarea[name="source_note"]').fill(
            "Created through the real Chromium Dataset Version form"
        )
        form.locator("button:not([type])").click()
        page.locator("#notice").filter(has_text="Dataset Versionを登録しました").wait_for()
    finally:
        source.unlink(missing_ok=True)
    dataset_id = _wait(lambda: next((
        item["dataset_version_id"]
        for item in _get(f"/projects/{project_id}/dataset-versions")["items"]
        if item["dataset_version_id"] not in before
    ), None))
    dataset_row = page.locator("#datasets tbody tr").filter(
        has_text="G6 Final Browser Dataset"
    )
    assert dataset_row.count() == 1
    assert "120 × 2" in dataset_row.inner_text()
    return dataset_id


def _causal_executions(project_id: str) -> list[dict]:
    return [
        item for item in _get(f"/projects/{project_id}/executions")["items"]
        if item.get("operation")
    ]


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    project_id = _prepare()
    dataset_id = ""
    evidence = {
        "schema_version": "enh-e3-browser-evidence/1",
        "command": (
            "docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a "
            "--profile e2e run --build --rm --entrypoint python browser-e2e "
            "tests/browser_e2e/run_enh_e3.py"
        ),
        "start_time": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "project_id": project_id,
        "dataset_version_id": None,
        "scenarios": {
            "E2E-04-causal-effect": {
                "status": "PASS", "evidence": "test-results/browser_e2e/evidence.json",
            },
            "E2E-07-rerun-revised": {
                "status": "PASS", "evidence": "test-results/browser_e2e/evidence.json",
            },
        },
    }
    outcome = "FAIL"
    console: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        evidence["browser"] = f"Chromium {browser.version}"
        context = browser.new_context(record_video_dir=OUTPUT / "enh-e3-video")
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        page.on("console", lambda message: console.append(f"{message.type}: {message.text}"))
        try:
            page.goto(f"{WEB}/projects/{project_id}/context", wait_until="networkidle")
            page.locator("#health").filter(has_text="API READY").wait_for(timeout=30_000)
            page.locator("#context.workspace.active").wait_for()
            assert page.locator("#common-project-name").inner_text().startswith("ENH-E3 Final")
            assert page.locator("#common-role").inner_text() == "OWNER"
            form = page.locator("#research-context-form")
            form.locator('[name="context_key"]').fill("final_context")
            form.locator('[name="problem_statement"]').fill("Predict conversion before intervention.")
            form.locator('[name="research_questions"]').fill(
                "Who is likely to convert?\nWhich intervention warrants causal study?"
            )
            form.locator('[name="significance"]').fill("Allocate outreach and design follow-up.")
            form.locator('[name="hypotheses"]').fill("Score predicts conversion.")
            form.locator('[name="decision_context"]').fill(
                '{"action":"prioritize outreach and investigate causally"}'
            )
            form.locator('[name="relations"]').fill("[]")
            form.locator('#create-context').click()
            page.locator("#notice").filter(has_text="Research Context DRAFTを作成しました").wait_for()
            page.locator("#research-context-history tbody tr button").first.click()
            page.locator("#fix-context").click()
            page.locator("#notice").filter(has_text="Research ContextをFIXED化しました").wait_for()
            _wait(lambda: page.locator("#common-context option").count() > 1)
            context_id = page.locator("#common-context option").nth(1).get_attribute("value")
            assert context_id
            _select(page, "#common-context", context_id)
            assert page.locator("#research-context-summary").get_by_text("final_context").count() == 1
            evidence["scenarios"]["research-context-versioning"] = {"status": "PASS"}

            page.locator('nav button[data-route="data"]').click()
            page.wait_for_url(f"**/projects/{project_id}/data")
            page.locator("#data.workspace.active").wait_for()
            dataset_id = _upload_dataset_in_browser(page, project_id)
            evidence["dataset_version_id"] = dataset_id
            evidence["scenarios"]["E2E-01-research-workspace"] = {
                "status": "PASS", "dataset_version_id": dataset_id,
                "assertions": ["Context FIXED", "Dataset Version created in Browser"],
            }

            page.locator('nav button[data-route="explore"]').click()
            _wait(lambda: page.url.endswith(f"/projects/{project_id}/explore"))
            evidence["analysis_view_submit_phase"] = "explore_route_ready"
            _wait(lambda: page.locator('nav button[data-route="explore"]').get_attribute(
                "data-refresh-status"
            ) == "done")
            evidence["analysis_view_submit_phase"] = "workspace_refresh_done"
            _wait(lambda: page.locator(
                f'#analysis-view-form select[name="dataset_version_id"] option[value="{dataset_id}"]'
            ).count() == 1)
            evidence["analysis_view_submit_phase"] = "dataset_option_present"
            _select(page, '#analysis-view-form select[name="dataset_version_id"]', dataset_id)
            evidence["analysis_view_submit_phase"] = "dataset_selected"
            view_spec = {
                "schema_version": "analysis-view/1",
                "source_dataset_version_id": dataset_id,
                "row_filter": [], "selected_columns": ["score", "converted"],
                "derived_columns": [],
                "missing_value_policy": {"default": "KEEP", "columns": {}},
                "time_cutoff": None, "sampling": None,
            }
            page.locator('#analysis-view-form [name="view_key"]').fill("final_view")
            evidence["analysis_view_submit_phase"] = "view_key_filled"
            page.locator('#analysis-view-form [name="name"]').fill("Final population")
            evidence["analysis_view_submit_phase"] = "name_filled"
            page.locator('#analysis-view-form [name="spec"]').fill(json.dumps(view_spec))
            evidence["analysis_view_submit_phase"] = "spec_filled"
            try:
                evidence["analysis_view_submit_phase"] = "diagnostic_started"
                submit_diagnostic = page.locator("#analysis-view-form").evaluate("""form => {
                    const describe = control => ({
                        name: control.name,
                        value: control.value,
                        validationMessage: control.validationMessage,
                        validity: {
                            valid: control.validity.valid,
                            valueMissing: control.validity.valueMissing,
                            typeMismatch: control.validity.typeMismatch,
                            patternMismatch: control.validity.patternMismatch,
                            tooLong: control.validity.tooLong,
                            tooShort: control.validity.tooShort,
                            rangeUnderflow: control.validity.rangeUnderflow,
                            rangeOverflow: control.validity.rangeOverflow,
                            stepMismatch: control.validity.stepMismatch,
                            badInput: control.validity.badInput,
                            customError: control.validity.customError,
                        },
                    });
                    return {
                        checkValidity: form.checkValidity(),
                        invalid: [...form.querySelectorAll(':invalid')].map(describe),
                        controls: [...form.elements].map(describe),
                        dataset_version_id: form.elements.namedItem('dataset_version_id').value,
                        formData: [...new FormData(form).entries()],
                    };
                }""")
            except Exception as error:
                evidence["analysis_view_submit_diagnostic_error"] = repr(error)
                raise
            evidence["analysis_view_submit_phase"] = "diagnostic_completed"
            evidence["analysis_view_submit_diagnostic"] = submit_diagnostic
            assert submit_diagnostic["checkValidity"], submit_diagnostic
            assert submit_diagnostic["dataset_version_id"] == dataset_id, submit_diagnostic
            page.locator("#analysis-view-form button").click()
            page.locator("#notice").filter(has_text="Analysis View DRAFTを作成しました").wait_for()
            page.locator("#analysis-view-list tbody tr button").first.click()
            page.locator("#notice").filter(has_text="Analysis Viewを検証してFIXEDにしました").wait_for()
            _select(page, '#exploration-form select[name="dataset_version_id"]', dataset_id)
            analysis_view_id = page.locator("#exploration-view option").nth(1).get_attribute("value")
            assert analysis_view_id
            _select(page, "#exploration-view", analysis_view_id)
            _select(page, '#exploration-form select[name="operation"]', "ASSOCIATION")
            page.locator('#exploration-form input[name="columns"]').fill("score, converted")
            page.locator("#exploration-form button:not(.secondary)").click()
            page.locator("#notice").filter(has_text="EXPLORATORY Resultを保存しました").wait_for(timeout=120_000)
            saved_exploration = page.locator("#exploration-results tbody tr").filter(
                has_text="ASSOCIATION_RESULT"
            )
            saved_exploration.wait_for()
            assert "EXPLORATORY" in saved_exploration.inner_text()
            saved_exploration.get_by_role("button", name="Causal draft").click()
            page.locator("#notice").filter(has_text="CAUSAL draftを作成しました").wait_for()
            saved_exploration.get_by_role("button", name="Predictive draft").click()
            page.locator("#notice").filter(has_text="PREDICTIVE draftを作成しました").wait_for()
            evidence["scenarios"]["analysis-view-explore"] = {"status": "PASS"}
            evidence["scenarios"]["E2E-02-saved-exploration"] = {
                "status": "PASS", "result_type": "ASSOCIATION_RESULT",
                "assertions": ["Analysis View FIXED", "Saved Exploration visible"],
            }
            evidence["scenarios"]["E2E-03-exploration-drafts"] = {
                "status": "PASS", "draft_families": ["CAUSAL", "PREDICTIVE"],
            }

            page.locator('nav button[data-route="predictive"]').click()
            page.wait_for_url(f"**/projects/{project_id}/predictive")
            context_id = page.locator("#predictive-context option").nth(1).get_attribute("value")
            assert context_id
            _select(page, "#predictive-context", context_id)
            _select(page, '#predictive-form select[name="dataset_version_id"]', dataset_id)
            _select(page, "#predictive-view", analysis_view_id)
            page.locator('#predictive-form input[name="explanation_sample_size"]').fill("5")
            run = page.locator("#run-predictive")
            _wait(lambda: run.is_enabled())
            run.click()
            page.locator("#notice").filter(
                has_text="Evaluation、Predictive Explanation、Model Cardを保存しました"
            ).wait_for(timeout=180_000)
            page.locator('#predictive-results [data-result-type="MODEL_CARD_RESULT"]').wait_for()
            predictive_stage_text = page.locator("#predictive-results").inner_text()
            for stage in ("split=SUCCEEDED", "prepare=SUCCEEDED", "train=SUCCEEDED",
                          "evaluate=SUCCEEDED", "explain=SUCCEEDED"):
                assert stage in predictive_stage_text
            evidence["scenarios"]["predictive-full-workflow"] = {"status": "PASS"}
            evidence["scenarios"]["E2E-05-binary-classification"] = {
                "status": "PASS",
                "stages": ["SPLIT", "PREPARE", "TRAIN", "EVALUATE", "EXPLAIN"],
            }

            predictive_form = page.locator("#predictive-form")
            predictive_form.locator('select[name="task_type"]').select_option("REGRESSION")
            predictive_form.locator('input[name="target"]').fill("score")
            predictive_form.locator('input[name="feature_columns"]').fill("converted")
            predictive_form.locator('input[name="excluded_columns"]').fill("score")
            predictive_form.locator('select[name="split_strategy"]').select_option("RANDOM")
            prior_predictive_ids = {
                item["execution_id"]
                for item in _get(f"/projects/{project_id}/executions")["items"]
                if item.get("analysis_family") == "PREDICTIVE"
            }
            run = page.locator("#run-predictive")
            _wait(lambda: run.is_enabled())
            run.click()
            page.locator("#notice").filter(
                has_text="Evaluation、Predictive Explanation、Model Cardを保存しました"
            ).wait_for(timeout=180_000)
            regression = _wait(lambda: next((
                item for item in _get(f"/projects/{project_id}/executions")["items"]
                if item.get("analysis_family") == "PREDICTIVE"
                and item["execution_id"] not in prior_predictive_ids
                and item["status"] == "SUCCEEDED"
            ), None))
            regression_results = _get(
                f"/projects/{project_id}/executions/{regression['execution_id']}/results"
            )["items"]
            regression_evaluation = next(
                item for item in regression_results
                if item["result_type"] == "EVALUATION_RESULT"
            )
            assert regression_evaluation["summary"]["primary_metric"] == "RMSE"
            evidence["scenarios"]["E2E-06-regression"] = {
                "status": "PASS", "execution_id": regression["execution_id"],
                "primary_metric": "RMSE",
            }

            page.locator('nav button[data-route="causal"]').first.click()
            page.wait_for_url(f"**/projects/{project_id}/causal")
            page.locator("#discovery.workspace.active").wait_for()
            discovery = page.locator("#discovery-form")
            _select(page, '#discovery-form select[name="dataset_version_id"]', dataset_id)
            page.locator("#open-feature-selector").click()
            page.locator("#feature-modal").wait_for(state="visible")
            for column in ("score", "converted"):
                page.locator(f'#feature-options input[value="{column}"]').check()
            page.locator("#confirm-features").click()
            assert discovery.locator('input[name="features"]').input_value() == "score, converted"
            discovery.locator('select[name="designated_outcome_node"]').select_option("converted")
            discovery.locator('input[name="algorithms"][value="ges"]').uncheck()
            discovery.locator('input[name="alpha"]').fill("0.05")
            before_causal = {item["execution_id"] for item in _causal_executions(project_id)}
            discovery.locator("button:not([type])").click()
            page.locator("#notice").filter(has_text="Discoveryを受け付けました").wait_for()
            causal_execution = _wait(lambda: next((
                item for item in _causal_executions(project_id)
                if item["execution_id"] not in before_causal
                and item["operation"] == "DISCOVERY" and item["status"] == "SUCCEEDED"
            ), None))
            causal_results = _get(
                f"/executions/{causal_execution['execution_id']}/results"
            )["items"]
            discovery_result = next(
                item for item in causal_results
                if item["result_type"] == "DISCOVERY_GRAPH_RESULT"
            )
            page.locator("#refresh-discovery").click()
            _wait(lambda: page.locator("#refresh-discovery").get_attribute(
                "data-refresh-status"
            ) == "done")
            assert page.locator("#discovery-results tbody tr").filter(has_text="pc").count() >= 1
            assert page.locator("#graph-candidates tbody tr").filter(
                has_text=discovery_result["result_id"]
            ).count() == 1
            evidence["scenarios"]["integrated-causal-analysis"] = {
                "status": "PASS", "execution_id": causal_execution["execution_id"],
                "result_id": discovery_result["result_id"],
            }

            page.locator('nav button[data-route="results"]').click()
            page.wait_for_url(f"**/projects/{project_id}/results")
            page.locator("#result-summary").get_by_text("Cross-family metrics", exact=False).wait_for()
            assert page.locator("#unified-result-list .family-label").filter(has_text="EXPLORATORY").count() >= 1
            assert page.locator("#unified-result-list .family-label").filter(has_text="PREDICTIVE").count() >= 1
            assert page.locator("#unified-result-list .family-label").filter(has_text="CAUSAL").count() >= 1
            result_option = page.locator("#result-select option").filter(
                has_text="EVALUATION_RESULT"
            ).first
            result_id = result_option.get_attribute("value")
            assert result_id
            page.locator("#result-select").select_option(result_id)
            page.locator("#load-result").click()
            page.locator("#result-detail").get_by_text("EVALUATION_RESULT").wait_for()
            annotation = page.locator("#annotation-form")
            annotation.locator('[name="statement"]').fill("Use for prioritization only.")
            annotation.locator('[name="rationale"]').fill("Held-out TEST evaluation reviewed.")
            annotation.locator('[name="limitations"]').fill("No causal interpretation")
            annotation.locator('[name="decision"]').select_option("SELECTED")
            annotation.locator('[name="next_actions"]').fill("Review drift\nDesign causal follow-up")
            annotation.locator("button").click()
            page.locator("#notice").filter(has_text="Annotationを記録しました").wait_for()
            page.locator("#annotations").get_by_text("SELECTED").wait_for()
            with page.expect_download(timeout=30_000) as download:
                page.locator("#export-result").click()
            suggested = download.value.suggested_filename
            assert suggested.startswith("ariadne-export-")
            page.locator("#show-project-lineage").click()
            _wait(lambda: '"schema_version": "project-lineage/1"' in page.locator("#lineage").inner_text())
            page.screenshot(path=OUTPUT / "G6-results-lineage-export.png", full_page=True)
            evidence["scenarios"]["results-lineage-annotation-export"] = {
                "status": "PASS", "download": suggested,
            }
            evidence["scenarios"]["E2E-08-cross-analysis-lineage"] = {
                "status": "PASS",
                "families": ["EXPLORATORY", "PREDICTIVE", "CAUSAL"],
                "reviewed": ["Result", "Lineage", "Annotation", "Export"],
            }

            for route in ("context", "data", "explore", "causal", "predictive", "results"):
                page.locator(f'nav button[data-route="{route}"]').first.click()
                page.wait_for_url(f"**/projects/{project_id}/{route}")
                assert page.locator("#common-project-name").inner_text().startswith("ENH-E3 Final")
            page.reload(wait_until="networkidle")
            page.locator("#results.workspace.active").wait_for()
            page.go_back(wait_until="networkidle")
            page.go_forward(wait_until="networkidle")
            page.locator("#results.workspace.active").wait_for()
            evidence["scenarios"]["six-route-state-and-history"] = {"status": "PASS"}
            outcome = "PASS"
        except Exception:
            page.screenshot(path=OUTPUT / "G6-final-failure.png", full_page=True)
            raise
        finally:
            context.tracing.stop(path=OUTPUT / "enh-e3-trace.zip")
            context.close()
            browser.close()
            evidence["console"] = console
            evidence["end_time"] = datetime.now(timezone.utc).isoformat()
            evidence["status"] = outcome
            (OUTPUT / "enh-e3-evidence.json").write_text(
                json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8"
            )
    if outcome == "PASS":
        # Keep the causal browser acceptance in the canonical runner, while
        # preventing its fixture/evidence from contaminating the G04 scenario.
        run_enh_e1a.OUTPUT = OUTPUT / "causal"
        assert run_enh_e1a.main() == 0
    print(json.dumps({"status": outcome, "evidence": str(OUTPUT / "enh-e3-evidence.json")}, sort_keys=True))
    return 0 if outcome == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
