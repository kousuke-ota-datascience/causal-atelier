# ENH-E5 G04 Trial 01 — Test Item 004: Browser regression

- Result: `FAIL`
- Test target: `5123961d466354b4bf8158d67a770d61b8574fd2`
- Verification purpose: Frozen Gate 07 verification architecture の browser/regression と current Explore behavior を実 Chromium で確認する。

## Command

```text
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a \
  --profile e2e run --build --rm --entrypoint python browser-e2e \
  tests/browser_e2e/run_enh_e3.py
```

## Raw evidence

The command created the browser container and its evidence output.  The runner's emitted `test-results/browser_e2e/evidence.json` recorded:

```json
{
  "browser": "Chromium 151.0.7922.34",
  "end_time": "2026-08-13T00:16:49.080709+00:00",
  "project_id": "48e547ec-686f-4f59-a4bd-fb1f7d76bdf2",
  "scenarios": {},
  "start_time": "2026-08-13T00:16:07.027870+00:00",
  "status": "FAIL"
}
```

Generated local failure evidence:

```text
test-results/browser_e2e/failure.png
test-results/browser_e2e/trace.zip
test-results/browser_e2e/video/page@ea808eb5b688ba630047ad9050429fd7.webm
```

The runner also recorded one browser-console error: HTTP `422 Unprocessable Entity`.

## Decision rationale

The frozen 07 contract requires browser/regression verification of current Explore behavior.  The canonical real-Chromium runner produced its own `status: FAIL`; no scenario passed.  This is a protected-regression failure.  The Test Agent did not change candidate implementation, test code, or acceptance criteria.
