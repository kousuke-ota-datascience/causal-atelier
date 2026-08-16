# 009 history_reload_console_browser

- Result: PASS
- Fixed Trial Candidate full SHA: `d2d5a9a7f6df352d787c8d561fce937012eef854`
- Tested Repository State full SHA: `9e85e4a6a2365869b48e5bc6c0b0ac6845698869`
- Exact command / method: `docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --build --rm --entrypoint python browser-e2e tests/browser_e2e/run_enh_e7_project_integration.py`
- Exit code: 0

## AC mapping

AC-G04-01, AC-G04-09, AC-G04-14.

## Direct assertion / predicate mapping

The runner asserts root replacement normalization, PM route reload, Back/Forward between Data and Results, cross-surface Back/Forward between Analysis and Results, exactly one visible root at every assertion point, selected Project continuity, and zero `console` type `error` / `pageerror` events.

## Raw relevant evidence

`project-routes-reload-history=PASS`; `cross-surface-reload-history=PASS`; evidence `status=PASS`; no captured error entries.

## Facts

Reload/history and browser runtime-error predicates all passed.

## Interpretation

No duplicate-history, stale-shell, console, or page-error violation was observed in the specified browser journey.

## Protected contract relation

G02 history authority and G03 stale-shell/duplicate-global-binding protection.

## Reproduction procedure

Run the command above.

## Browser evidence

`test-results/browser_e2e/enh-e7-project-integration-evidence.json`; the runner stores failure screenshot `enh-e7-project-integration-failure.png` only on failure, and it was not produced.
