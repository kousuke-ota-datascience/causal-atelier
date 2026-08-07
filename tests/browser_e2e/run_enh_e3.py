"""Real Chromium acceptance for the ENH-E3 G6 product closure."""

from __future__ import annotations

import json
import platform
import time
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright

from run_enh_e3_predictive import (
    OUTPUT,
    WEB,
    _post,
    _select,
    _upload_dataset,
    _wait,
)


def _prepare() -> tuple[str, str]:
    project = _post("/projects", {
        "name": f"ENH-E3 Final Browser {int(time.time())}",
        "topic": "conversion prediction and causal follow-up",
        "objective": "Explore, predict, and preserve cross-analysis lineage",
        "memo": "G6 real Chromium acceptance",
    })
    rows = ["score,converted"]
    rows.extend(f"{score},{int(score >= 0)}" for score in range(-60, 60))
    dataset = _upload_dataset(project["project_id"], ("\n".join(rows) + "\n").encode())
    return project["project_id"], dataset["dataset_version_id"]


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    project_id, dataset_id = _prepare()
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
        "dataset_version_id": dataset_id,
        "scenarios": {},
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
            assert page.locator("#research-context-summary").get_by_text("final_context").count() == 1
            evidence["scenarios"]["research-context-versioning"] = {"status": "PASS"}

            page.locator('nav button[data-route="explore"]').click()
            page.wait_for_url(f"**/projects/{project_id}/explore")
            _select(page, '#analysis-view-form select[name="dataset_version_id"]', dataset_id)
            view_spec = {
                "schema_version": "analysis-view/1",
                "source_dataset_version_id": dataset_id,
                "row_filter": [], "selected_columns": ["score", "converted"],
                "derived_columns": [],
                "missing_value_policy": {"default": "KEEP", "columns": {}},
                "time_cutoff": None, "sampling": None,
            }
            page.locator('#analysis-view-form [name="view_key"]').fill("final_view")
            page.locator('#analysis-view-form [name="name"]').fill("Final population")
            page.locator('#analysis-view-form [name="spec"]').fill(json.dumps(view_spec))
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
            page.locator("#exploration-results").get_by_text("EXPLORATORY").wait_for()
            evidence["scenarios"]["analysis-view-explore"] = {"status": "PASS"}

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
            evidence["scenarios"]["predictive-full-workflow"] = {"status": "PASS"}

            page.locator('nav button[data-route="results"]').click()
            page.wait_for_url(f"**/projects/{project_id}/results")
            page.locator("#result-summary").get_by_text("Cross-family metrics", exact=False).wait_for()
            assert page.locator("#unified-result-list .family-label").filter(has_text="EXPLORATORY").count() >= 1
            assert page.locator("#unified-result-list .family-label").filter(has_text="PREDICTIVE").count() >= 1
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
    print(json.dumps({"status": outcome, "evidence": str(OUTPUT / "enh-e3-evidence.json")}, sort_keys=True))
    return 0 if outcome == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
