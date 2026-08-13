# ENH-E6 G01 P03 — Browser Regression and Test Strengthening

**Document class:** Primary Execution Contract — Work Package  
**Self-containment:** MUST.

- Enhancement: `ENH-E6`
- Gate: `G01`
- Package: `P03`
- Status: `APPROVED / WAITING_FOR_REQUIRED_P01_P02_CHECKPOINTS`
- Target branch: `bugfix/ariadne_mvp_e6`

## 1. Purpose

Build the ENH-E6 regression evidence that directly prevents recurrence of `ANOM-E5-001`: a real Chromium runner must enter Analysis normally and operate actual Family/Stage elements, while product/static tests provide focused lower-layer protection. Existing source-string checks remain supplemental, not observable acceptance substitutes.

## 2. Effective Gate constraints applicable to this package

- real browser = existing Playwright Python / Chromium `browser-e2e` infrastructure.
- runner waits for frontend health `API READY` and creates/selects deterministic Project context through supported UI/API setup consistent with existing harness.
- first normal-entry Family assertion occurs without forced reload or direct renderer invocation.
- test operates actual Family tabs and Stage controls.
- Browser E2E proves critical cross-layer journeys; detailed resolver/state correctness remains lower-layer responsibility.
- test must not weaken/delete existing assertions or fabricate DOM state.
- canonical docs and historical ENH-E5 evidence remain protected.

## 3. In scope

Create:

- `tests/browser_e2e/run_enh_e6_family_stage_navigation.py`

Update as required so the runner is executable in the canonical image:

- `Dockerfile.browser-e2e`
- `.dockerignore`

Add/adjust affected product/frontend/static tests where needed to encode lower-layer architecture/regression without replacing browser proof.

Evidence output should follow existing `test-results/browser_e2e` convention and capture actionable failure data.

## 4. Explicitly out of scope

- change production navigation behavior to make tests pass except a clearly isolated P03-owned testability defect explicitly permitted by this contract (none currently specified)
- reimplement P01 transition authority or P02 mapping
- redefine expected routes/mappings
- broad browser test framework replacement
- introduce Selenium/Cypress/new framework
- skip/xfail/weaken tests
- direct-test invocation of renderer to bypass actual user journey
- full scientific workflow E2E unrelated to Family/Stage navigation

If a product defect in P01/P02 behavior is exposed, record evidence and stop rather than opportunistically fix other package scope.

## 5. Entry criteria / required evidence

- repository preflight passes
- required P01/P02 package checkpoints are present in current candidate line
- actual implementation exposes expected Family/Stage controls and legacy shortcuts
- existing `browser-e2e` infrastructure files exist
- assigned P03 resolves exactly once

Existing harness facts embedded in this contract:

- Playwright Python / Chromium
- `Dockerfile.browser-e2e` uses `mcr.microsoft.com/playwright/python:v1.62.0-noble`
- compose service sets `ARIADNE_E2E_WEB_URL=http://frontend`, API URL, evidence volume, depends on frontend/worker
- existing canonical invocation uses `docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --build --rm --entrypoint python browser-e2e <runner>`
- past defect: `.dockerignore` excluded a newly added runner; P03 must verify current runner is in build context/image.

## 6. Required implementation

### 6.1 Canonical ENH-E6 runner

Implement `tests/browser_e2e/run_enh_e6_family_stage_navigation.py` with evidence structure consistent with existing runners where practical (scenario results, console capture, screenshot/trace/video on failure or run).

Canonical command to make executable:

```bash
docker compose \
  -f compose.yaml \
  -f compose.e1a.yaml \
  -p ariadne-e1a \
  --profile e2e \
  run --build --rm \
  --entrypoint python \
  browser-e2e \
  tests/browser_e2e/run_enh_e6_family_stage_navigation.py
```

Runner must ensure current source image inclusion. Update Dockerfile/.dockerignore so `git check-ignore`/Docker build cannot silently omit the runner.

### 6.2 Browser journey B01 — Normal entry -> Family switching

1. launch fresh browser context; navigate frontend; wait `#health` contains `API READY`.
2. create or select deterministic Project context such that `/projects/<id>/data` or equivalent selected Project state is confirmed.
3. click actual normal/legacy Explore analytical entry; **do not reload**.
4. assert canonical URL ends `/analysis/exploratory/profile`.
5. assert exactly 3 visible/operable Family tabs in backend catalog order/labels, Exploratory selected.
6. assert current Exploratory Stage list is visible and current stage selected.
7. click actual Predictive Family tab.
8. assert canonical `/analysis/predictive/setup`, Predictive selected, Predictive-local stage list/default selected, Predictive presentation active.
9. click actual Causal Family tab.
10. assert canonical `/analysis/causal/setup`, Causal selected, Causal-local stages, causal setup presentation mapping active.

### 6.3 Browser journey B02 — Causal Discovery / Inference boundary

1. from selected Project, click actual `Causal Discovery` compatibility entry.
2. assert route `/analysis/causal/discovery`, Causal selected, discovery Stage selected, Discovery presentation active and Inference inactive.
3. click actual `Causal Inference` compatibility entry.
4. assert route `/analysis/causal/identification`, Causal selected, identification selected, Inference active and Discovery inactive.
5. click actual `estimation` Stage control.
6. assert Causal remains selected, URL `/analysis/causal/estimation`, estimation selected, Inference remains active.

### 6.4 Browser journey B03 — Direct/reload/history restore

1. open/establish `exploratory/profile` canonical state.
2. Family-switch to Predictive, then click a non-default Predictive Stage available from catalog.
3. record route/Family/Stage/presentation at each state.
4. browser Back through transitions and Forward again; after each event wait for deterministic UI state without arbitrary sleep where app signal/locator can be used.
5. reload an explicit canonical route and assert identical route/selected Family/Stage/presentation.

### 6.5 Failure evidence

On failure capture at least:

- current URL
- screenshot
- Family tab role/name/selected/visible state or outerHTML snapshot
- Stage sidebar equivalent
- active workspace/presentation identity
- console messages
- relevant failed network/status info if observable
- trace/video when existing harness supports it

## 7. Focused verification

P03 must run:

1. syntax/static check for new runner.
2. `git check-ignore` or equivalent proving runner is not excluded from Docker build context.
3. Docker image build/canonical runner command above.
4. all B01-B03 scenarios green on P03 package candidate.
5. relevant existing product/static/navigation regressions impacted by test-support changes.

The following are insufficient alone:

- string `analysis-family-tabs` exists in HTML
- string `catalog.families.map` exists in JS
- hidden element text exists
- direct call of transition/renderer from test
- assertion performed only after forced reload

## 8. Protected contract / Transition Debt constraints

- do not alter required production behavior to simplify automation.
- do not replace real browser proof with static/DOM-only tests.
- retain existing E3/E1a browser harness functionality; additive runner integration must not break current image.
- ANOM-E5-001 remains OPEN until independent G01 PASS, even if P03 browser self-check is green.

## 9. Checkpoint / reporting rule

After all focused verification passes, create P03 checkpoint/evidence/report per operator workflow. Report exact browser command, browser version if available, scenarios/results, evidence paths, changed Docker/.dockerignore state, `START_SHA`/checkpoint/evidence SHAs. Do not assemble Fixed Candidate unless separately assigned.

## 10. Package completion criteria

`PACKAGE_READY` only when:

- ENH-E6 runner exists and is included/executable in browser image;
- canonical command builds current source and passes B01-B03;
- actual Family/Stage elements are clicked;
- clean normal entry is asserted before reload;
- failure evidence behavior is implemented/usable;
- relevant regressions remain green;
- package checkpoint/report/evidence recorded;
- no P01/P02 product scope or forbidden expectation weakening is included.

## 11. External reference policy

Assigned P03 is the only normative implementation contract. Coding Agent must not read Gate06, Gate07, P00, other Pxx, 00-30, ADR, prior ENH, issues, Web for required behavior. Current repository code/test/compose/Docker files may be inspected as implementation substrate. If expected behavior is ambiguous, stop `BLOCKED_CONTRACT_AMBIGUITY` rather than opening forbidden contracts.

## 12. Stop rule

Stop if B01-B03 reveal P01/P02 product defect requiring other package change, canonical browser infrastructure cannot support this runner without broad framework migration, protected existing browser suites require unrelated modification, repository/contract is ambiguous, or required verification cannot complete within P03 scope.
