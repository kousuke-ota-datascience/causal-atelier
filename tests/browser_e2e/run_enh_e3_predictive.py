"""Real Chromium acceptance for the G5 Predictive workspace."""

from __future__ import annotations

import json
import os
import platform
import time
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from playwright.sync_api import Page, sync_playwright


WEB = os.getenv("ARIADNE_E2E_WEB_URL", "http://127.0.0.1:8080")
API = os.getenv("ARIADNE_E2E_API_URL", "http://127.0.0.1:8000/api/v1")
ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(os.getenv("ARIADNE_E2E_OUTPUT_DIR", ROOT / "test-results/browser_e2e"))


def _request(
    method: str,
    path: str,
    *,
    payload: dict[str, Any] | None = None,
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    body = data
    request_headers = dict(headers or {})
    if payload is not None:
        body = json.dumps(payload).encode()
        request_headers["Content-Type"] = "application/json"
    request = urllib.request.Request(
        f"{API}{path}", data=body, headers=request_headers, method=method
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def _get(path: str) -> dict[str, Any]:
    return _request("GET", path)


def _post(path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return _request("POST", path, payload=payload)


def _upload_dataset(project_id: str, content: bytes) -> dict[str, Any]:
    boundary = f"ariadne-{uuid.uuid4().hex}"
    chunks: list[bytes] = []
    for name, value in {
        "dataset_key": "g5_predictive",
        "version_label": "v1",
        "name": "G5 Predictive Browser",
        "source_note": "deterministic G5 browser fixture",
    }.items():
        chunks.extend([
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
            str(value).encode(),
            b"\r\n",
        ])
    chunks.extend([
        f"--{boundary}\r\n".encode(),
        b'Content-Disposition: form-data; name="file"; filename="predictive.csv"\r\n',
        b"Content-Type: text/csv\r\n\r\n",
        content,
        b"\r\n",
        f"--{boundary}--\r\n".encode(),
    ])
    return _request(
        "POST",
        f"/projects/{project_id}/dataset-versions",
        data=b"".join(chunks),
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Idempotency-Key": f"g5-browser-{uuid.uuid4().hex}",
        },
    )


def _wait(predicate: Callable[[], Any], timeout: float = 120) -> Any:
    deadline = time.monotonic() + timeout
    last: Any = None
    while time.monotonic() < deadline:
        try:
            last = predicate()
            if last:
                return last
        except Exception as exc:  # pragma: no cover - retained as failure evidence
            last = exc
        time.sleep(0.5)
    raise AssertionError(f"Timed out; last observation: {last!r}")


def _prepare_workspace() -> tuple[str, str, str]:
    project = _post("/projects", {
        "name": f"G5 Predictive Browser {int(time.time())}",
        "topic": "conversion prediction",
        "objective": "evaluate and explain a predictive model",
        "memo": "G5 browser acceptance",
    })
    project_id = project["project_id"]
    rows = ["score,converted"]
    rows.extend(f"{score},{int(score >= 0)}" for score in range(-60, 60))
    dataset = _upload_dataset(project_id, ("\n".join(rows) + "\n").encode())
    context = _post(f"/projects/{project_id}/research-contexts", {
        "context_key": "conversion_prediction",
        "problem_statement": "Predict conversion before outreach.",
        "research_questions": ["Who is likely to convert?"],
        "significance": "Allocate outreach capacity.",
        "hypotheses": [],
        "decision_context": {"action": "prioritize outreach"},
        "relations": [],
    })
    context_id = context["research_context_version_id"]
    fixed = _post(f"/projects/{project_id}/research-contexts/{context_id}/fix")
    assert fixed["status"] == "FIXED"
    return project_id, dataset["dataset_version_id"], context_id


def _latest_predictive_execution(project_id: str) -> dict[str, Any] | None:
    values = [
        item
        for item in _get(f"/projects/{project_id}/executions")["items"]
        if item.get("analysis_family") == "PREDICTIVE"
        and item.get("analysis_specification_id")
    ]
    return values[0] if values else None


def _select(page: Page, selector: str, value: str) -> None:
    page.locator(selector).select_option(value)


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    evidence_path = OUTPUT / "predictive-evidence.json"
    project_id, dataset_id, context_id = _prepare_workspace()
    evidence: dict[str, Any] = {
        "command": (
            "docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a "
            "--profile e2e run --build --rm --entrypoint python browser-e2e "
            "tests/browser_e2e/run_enh_e3_predictive.py"
        ),
        "start_time": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "project_id": project_id,
        "dataset_version_id": dataset_id,
        "research_context_version_id": context_id,
        "scenarios": {},
    }
    outcome = "FAIL"
    console: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        evidence["browser"] = f"Chromium {browser.version}"
        context = browser.new_context(record_video_dir=OUTPUT / "predictive-video")
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        page.on("console", lambda message: console.append(
            f"{message.type}: {message.text}"
        ))
        try:
            predictive_url = f"{WEB}/projects/{project_id}/predictive"
            page.goto(predictive_url, wait_until="networkidle")
            page.locator("#health").filter(has_text="API READY").wait_for(timeout=30_000)
            page.locator("#predictive.workspace.active").wait_for()
            assert page.url.endswith(f"/projects/{project_id}/predictive")
            assert page.locator("#project-select").input_value() == project_id
            page.locator(".predictive-terminology").filter(
                has_text="Predictive Explanation ≠ Causal Explanation ≠ Treatment Effect"
            ).wait_for()
            evidence["scenarios"]["predictive-deep-link"] = {"status": "PASS"}

            _select(page, "#predictive-context", context_id)
            _select(
                page,
                '#predictive-form select[name="dataset_version_id"]',
                dataset_id,
            )
            page.locator(
                '#predictive-form input[name="explanation_sample_size"]'
            ).fill("5")
            run = page.locator("#run-predictive")
            _wait(lambda: run.is_enabled())
            run.click()
            page.locator("#notice").filter(
                has_text="Evaluation、Predictive Explanation、Model Cardを保存しました"
            ).wait_for(timeout=120_000)

            for result_type in (
                "EVALUATION_RESULT",
                "ERROR_ANALYSIS_RESULT",
                "PREDICTIVE_EXPLANATION_RESULT",
                "MODEL_CARD_RESULT",
            ):
                page.locator(
                    f'#predictive-results [data-result-type="{result_type}"]'
                ).wait_for()
            page.locator("#predictive-results").filter(
                has_text="Predictive Explanation is not a Causal Explanation or Treatment Effect."
            ).wait_for()
            page.locator("#predictive-artifacts").filter(
                has_text="PREDICTIVE_EXPLANATION"
            ).wait_for()
            page.locator("#predictive-artifacts").filter(
                has_text="MODEL_CARD"
            ).wait_for()
            execution = _wait(lambda: _latest_predictive_execution(project_id))
            assert execution["status"] == "SUCCEEDED"
            results = _get(
                f"/projects/{project_id}/executions/{execution['execution_id']}/results"
            )["items"]
            by_type = {item["result_type"]: item for item in results}
            assert by_type["PREDICTIVE_EXPLANATION_RESULT"]["analytical_status"] == "GENERATED"
            assert by_type["MODEL_CARD_RESULT"]["analytical_status"] == "GENERATED"
            page.screenshot(
                path=OUTPUT / "G5-predictive-workspace.png", full_page=True
            )
            evidence["scenarios"]["predictive-full-workflow"] = {
                "status": "PASS",
                "execution_id": execution["execution_id"],
                "result_ids": [item["result_id"] for item in results],
            }

            target_input = page.locator(
                '#predictive-form input[name="target"]'
            )
            target_input.fill("missing_target")
            run.click()
            rendered_error = page.locator("#notice.show").filter(
                has_text="UNKNOWN_PREDICTIVE_COLUMN"
            )
            rendered_error.wait_for(timeout=30_000)
            assert "missing_target" in rendered_error.text_content()
            assert _latest_predictive_execution(project_id)["execution_id"] == (
                execution["execution_id"]
            )
            page.screenshot(
                path=OUTPUT / "G5-predictive-error-rendering.png", full_page=True
            )
            evidence["scenarios"]["predictive-error-rendering"] = {
                "status": "PASS",
                "induced_error": "UNKNOWN_PREDICTIVE_COLUMN",
                "rendered_message": rendered_error.text_content(),
            }
            target_input.fill("converted")

            page.locator('nav button[data-route="data"]').click()
            page.wait_for_url(f"**/projects/{project_id}/data")
            page.locator('nav button[data-workspace="predictive"]').click()
            page.wait_for_url(f"**/projects/{project_id}/predictive")
            page.go_back(wait_until="networkidle")
            page.locator("#data.workspace.active").wait_for()
            page.go_forward(wait_until="networkidle")
            page.locator("#predictive.workspace.active").wait_for()
            page.reload(wait_until="networkidle")
            page.locator("#predictive.workspace.active").wait_for()
            page.locator(
                '#predictive-results [data-result-type="MODEL_CARD_RESULT"]'
            ).wait_for()
            evidence["scenarios"]["predictive-routing"] = {
                "status": "PASS",
                "deep_link": True,
                "browser_back": True,
                "reload": True,
            }
            outcome = "PASS"
        except Exception:
            page.screenshot(
                path=OUTPUT / "G5-predictive-failure.png", full_page=True
            )
            raise
        finally:
            context.tracing.stop(path=OUTPUT / "predictive-trace.zip")
            context.close()
            browser.close()
            evidence["console"] = console
            evidence["end_time"] = datetime.now(timezone.utc).isoformat()
            evidence["status"] = outcome
            evidence_path.write_text(
                json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8"
            )
    print(json.dumps({"status": outcome, "evidence": str(evidence_path)}, sort_keys=True))
    return 0 if outcome == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
