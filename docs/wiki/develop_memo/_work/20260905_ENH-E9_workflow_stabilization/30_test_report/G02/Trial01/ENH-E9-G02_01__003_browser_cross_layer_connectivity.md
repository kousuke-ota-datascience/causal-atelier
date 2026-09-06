# ENH-E9 G02 Trial 01 Test Item 003 — Browser cross-layer connectivity

> **Document class:** Evidence Artifact

- Project / Enhancement / Gate / Trial: Ariadne / ENH-E9 / G02 / 01
- Status / Primary layer: BLOCKED / BROWSER_E2E
- Fixed Trial Candidate SHA: `8cf70523093efa53b59a7de2c655f9755dbceb8d`
- Tested Repository State: `6355ce9252a896c5907ac465b102e959c5b481f7`
- Completion report: `20_implementation_reports/G02/Trial01/ENH-E9-G02_01__implementation_completion.md`
- 07 Contract: `10_enhance_instruction/G02/07_Ariadne_ENH-E9_G02_test_instruction.md` (FROZEN)
- Applicable 08: NONE
- Timestamp: 2026-09-06T01:13:54Z

## Purpose / acceptance mapping

- Covers mandatory final cross-layer connectivity for AC1–AC8: Discovery → candidate review/comparison → adopt/fix.
- Candidate identity audit NO (item 001); non-browser prerequisites PASS (item 002).

## Exact command

```bash
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e9-g02-verify --profile e2e run --rm --no-deps --entrypoint python browser-e2e tests/browser_e2e/run_enh_e1a.py
```

Exit code: `1` (runner failure). The pre-running isolated API was healthy, with frontend/database/worker available. The equivalent isolated project was used because the canonical Compose project's host port `15432` was occupied.

## Browser diagnostic evidence

```text
test-results/browser_e2e/evidence.json
browser: Chromium 151.0.7922.34
console: []
scenarios: {}
start: 2026-09-06T01:08:22.562201+00:00
end:   2026-09-06T01:08:56.493312+00:00
status: FAIL
```

- Trace: `test-results/browser_e2e/trace.zip`
- Screenshot: `test-results/browser_e2e/failure.png`
- Video: `test-results/browser_e2e/video/page@6cbfb144e7c2bd2e2f2fee4c3e945321.webm`
- API/worker logs: N/A; no product workflow reached.
- Failure classification: `TEST_IMPLEMENTATION_DEFECT`.

## Facts and interpretation

The runner passed Chromium launch and application health, then stopped at `page.locator('nav button[data-workspace="management"]').click()`. The current rendered Project List page provides `#new-project` and no matching navigation selector. No project was registered and the evidence contains zero scenarios, so Discovery, comparison, adoption, and fix were not exercised.

This is not a verified product integration violation; it is a stale test locator before a G02 product assertion. It also cannot establish product correctness. Frozen 07 and the test-agent rule therefore require BLOCKED rather than FAIL.

| Criterion | Expected | Observed | Result |
|---|---|---|---|
| Mandatory Browser E2E | Complete cross-layer scenario | 0 scenarios; stopped before project registration | BLOCKED |
| Product judgment | Fail only on verified product violation | Test implementation failed first | BLOCKED |

## Mutation audit / reproduction / rationale

- Production, automated test, migration, dependency changes by Test Agent: NONE.
- Reproduce with the exact Compose command and inspect the listed evidence.
- Required action: align/provide the authoritative E2E runner for current Project List → New Project navigation, then rerun the required scenario in the same Trial.
