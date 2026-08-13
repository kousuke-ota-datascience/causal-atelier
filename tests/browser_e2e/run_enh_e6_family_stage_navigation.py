"""Real Chromium regression coverage for ENH-E6 family/stage navigation."""

from __future__ import annotations

import json
import os
import platform
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
    "tests/browser_e2e/run_enh_e6_family_stage_navigation.py"
)


def _request(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    request = urllib.request.Request(f"{API}{path}", data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def _create_project() -> str:
    project = _request("POST", "/projects", {
        "name": f"ENH-E6 Navigation Browser {int(time.time())}",
        "topic": "family and stage navigation",
        "objective": "exercise canonical analysis navigation in Chromium",
        "memo": "ENH-E6 G01 P03 browser fixture",
    })
    return project["project_id"]


def _catalog() -> dict[str, Any]:
    return _request("GET", "/navigation/analysis")


def _family(catalog: dict[str, Any], slug: str) -> dict[str, Any]:
    return next(item for item in catalog["families"] if item["slug"] == slug)


def _snapshot(page: Page) -> dict[str, Any]:
    def controls(selector: str) -> list[dict[str, Any]]:
        return page.locator(selector).evaluate_all("""
            nodes => nodes.map(node => ({
              text: node.textContent, visible: !!(node.offsetWidth || node.offsetHeight || node.getClientRects().length),
              selected: node.getAttribute('aria-selected'), current: node.getAttribute('aria-current'), html: node.outerHTML,
            }))
        """)
    active = page.locator(".workspace.active")
    return {
        "url": page.url,
        "family_tabs": controls("#analysis-family-tabs button"),
        "stage_controls": controls("#analysis-stage-sidebar button"),
        "active_workspace": active.get_attribute("id") if active.count() else None,
        "causal_presentation": page.locator("#causal-stage-presentation").inner_text(),
    }


def _assert_context(page: Page, project_id: str, family: str, stage: str, workspace: str) -> None:
    expected = f"/projects/{project_id}/analysis/{family}/{stage}"
    page.wait_for_url(f"**{expected}", timeout=30_000)
    assert page.url.endswith(expected), page.url
    selected = page.locator(f'#analysis-family-tabs button[data-family="{family}"][aria-selected="true"]')
    current = page.locator(f'#analysis-stage-sidebar button[data-stage="{stage}"][aria-current="page"]')
    assert selected.count() == 1 and selected.is_visible()
    assert current.count() == 1 and current.is_visible()
    page.locator(f"#{workspace}.workspace.active").wait_for(timeout=30_000)


def _click_family(page: Page, slug: str) -> None:
    page.locator(f'#analysis-family-tabs button[data-family="{slug}"]').click()


def _click_stage(page: Page, slug: str) -> None:
    page.locator(f'#analysis-stage-sidebar button[data-stage="{slug}"]').click()


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    evidence_path = OUTPUT / "enh-e6-family-stage-navigation-evidence.json"
    project_id = _create_project()
    catalog = _catalog()
    evidence: dict[str, Any] = {
        "schema_version": "enh-e6-browser-evidence/1", "command": COMMAND,
        "start_time": datetime.now(timezone.utc).isoformat(), "platform": platform.platform(),
        "project_id": project_id, "catalog": catalog, "scenarios": {},
    }
    console: list[str] = []
    outcome = "FAIL"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        evidence["browser"] = f"Chromium {browser.version}"
        context = browser.new_context(record_video_dir=OUTPUT / "enh-e6-navigation-video")
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        page.on("console", lambda message: console.append(f"{message.type}: {message.text}"))
        try:
            page.goto(f"{WEB}/projects/{project_id}/data", wait_until="networkidle")
            page.locator("#health").filter(has_text="API READY").wait_for(timeout=30_000)
            assert page.locator("#project-select").input_value() == project_id

            # B01: normal entry and real Family/Stage tab interactions, without reload.
            page.locator('nav button[data-workspace="explore"]').click()
            _assert_context(page, project_id, "exploratory", "profile", "explore")
            tabs = page.locator('#analysis-family-tabs button[role="tab"]')
            assert tabs.count() == 3
            assert tabs.all_inner_texts() == [item["label"] for item in catalog["families"]]
            exploratory = _family(catalog, "exploratory")
            assert page.locator("#analysis-stage-sidebar button").count() == len(exploratory["stages"])
            _click_family(page, "predictive")
            predictive = _family(catalog, "predictive")
            _assert_context(page, project_id, "predictive", predictive["default_stage_id"], "predictive")
            _click_family(page, "causal")
            causal = _family(catalog, "causal")
            _assert_context(page, project_id, "causal", causal["default_stage_id"], "discovery")
            evidence["scenarios"]["B01-normal-entry-family-switching"] = {"status": "PASS", "snapshot": _snapshot(page)}

            # B02: the two legacy causal entries are compatibility shortcuts, not parallel routes.
            page.locator('nav button[data-workspace="discovery"]').click()
            _assert_context(page, project_id, "causal", "discovery", "discovery")
            page.locator('nav button[data-workspace="inference"]').click()
            _assert_context(page, project_id, "causal", "identification", "inference")
            _click_stage(page, "estimation")
            _assert_context(page, project_id, "causal", "estimation", "inference")
            evidence["scenarios"]["B02-causal-discovery-inference-boundary"] = {"status": "PASS", "snapshot": _snapshot(page)}

            # B03: direct canonical state, history traversal, and reload preserve the same UI identity.
            page.locator('nav button[data-workspace="explore"]').click()
            _assert_context(page, project_id, "exploratory", "profile", "explore")
            exploratory_route = page.url
            _click_family(page, "predictive")
            _assert_context(page, project_id, "predictive", predictive["default_stage_id"], "predictive")
            predictive_default_route = page.url
            non_default = next(stage["slug"] for stage in predictive["stages"] if stage["slug"] != predictive["default_stage_id"])
            _click_stage(page, non_default)
            _assert_context(page, project_id, "predictive", non_default, "predictive")
            predictive_stage_route = page.url
            page.go_back(wait_until="networkidle")
            _assert_context(page, project_id, "predictive", predictive["default_stage_id"], "predictive")
            page.go_back(wait_until="networkidle")
            _assert_context(page, project_id, "exploratory", "profile", "explore")
            page.go_forward(wait_until="networkidle")
            _assert_context(page, project_id, "predictive", predictive["default_stage_id"], "predictive")
            page.go_forward(wait_until="networkidle")
            _assert_context(page, project_id, "predictive", non_default, "predictive")
            page.reload(wait_until="networkidle")
            _assert_context(page, project_id, "predictive", non_default, "predictive")
            evidence["scenarios"]["B03-direct-reload-history-restore"] = {
                "status": "PASS", "routes": [exploratory_route, predictive_default_route, predictive_stage_route],
                "snapshot": _snapshot(page),
            }
            page.screenshot(path=OUTPUT / "enh-e6-family-stage-navigation.png", full_page=True)
            outcome = "PASS"
        except Exception as error:
            evidence["failure"] = {"error": repr(error), "snapshot": _snapshot(page)}
            page.screenshot(path=OUTPUT / "enh-e6-family-stage-navigation-failure.png", full_page=True)
            raise
        finally:
            context.tracing.stop(path=OUTPUT / "enh-e6-family-stage-navigation-trace.zip")
            context.close(); browser.close()
            evidence["console"] = console
            evidence["end_time"] = datetime.now(timezone.utc).isoformat()
            evidence["status"] = outcome
            evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"status": outcome, "evidence": str(evidence_path)}, sort_keys=True))
    return 0 if outcome == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
