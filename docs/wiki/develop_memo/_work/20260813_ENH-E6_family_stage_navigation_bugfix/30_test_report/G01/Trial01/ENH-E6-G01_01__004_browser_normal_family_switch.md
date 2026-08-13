# Test Item 004 — B01 normal entry and Family switch

- Result: **PASS**
- Candidate: `575cdd139aea09d4f19b46ab6a6d38545f645c71`
- AC: 001, 002, 010

## Command

```text
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --build --rm --entrypoint python browser-e2e tests/browser_e2e/run_enh_e6_family_stage_navigation.py
```

## Raw evidence

`test-results/browser_e2e/enh-e6-family-stage-navigation-evidence.json` reports `status: PASS`, Chromium `151.0.7922.34`, and `B01-normal-entry-family-switching: PASS`. It creates/selects a project, waits for `#health` API READY, performs the real Explore click, then real Predictive and Causal Family-tab clicks.

The B01 final snapshot has canonical `/analysis/causal/setup`, 3 visible Family buttons with Causal solely selected, 7 Causal-local Stage buttons with Setup current, and active `discovery` presentation. The runner also asserted the initial Exploratory family-tab count is exactly 3 and the Stage count equals the catalog's current-Family stages before any reload.

Artifacts: `test-results/browser_e2e/enh-e6-family-stage-navigation.png`, trace zip, and video directory.
