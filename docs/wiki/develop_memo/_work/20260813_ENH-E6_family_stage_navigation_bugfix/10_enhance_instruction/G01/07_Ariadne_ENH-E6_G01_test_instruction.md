# Ariadne ENH-E6 G01 テスト指示書 — Gate Verification Contract

**Document class:** Primary Execution Contract — Independent Verification  
**Self-containment:** MUST.  
**Contract state:** `APPROVED / FROZEN`  
**Information boundary:** this document is for Test/Audit Agent; **Work Package Coding Agents must not read it.**

## 1. Acceptance authority

This frozen 07 alone is G01 Acceptance Criteria authority. Coding self-check/package reports are evidence inputs only and cannot define PASS. No source-string existence or implementation claim can substitute for required observable proof.

## 2. Gate objective / acceptance claim

G01 PASS means supported Analysis entry/navigation paths consistently apply canonical Family/Stage Navigation Context and expose synchronized Family tabs, Family-local Stage sidebar, URL/history, selected state, and correct existing presentation surface. Legacy analytical left-nav behaves only as canonical compatibility entry. The defect reproduced as API READY + canonical route + Family button=0/Stage button=0 must no longer occur.

## 3. Effective verification context

Protected semantics:

- 3 Families: Exploratory/Predictive/Causal; catalog authority for labels/order/default/stages.
- canonical route `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`.
- Navigation Stage != Execution Stage; no navigation persistence.
- legacy targets: Explore/profile, Predictive/setup, Causal Discovery/discovery, Causal Inference/identification.
- presentation mapping:
  - `exploratory/* -> explore`
  - `predictive/* -> predictive`
  - `causal/setup -> discovery`
  - `causal/discovery -> discovery`
  - `causal/identification -> inference`
  - `causal/estimation -> inference`
  - `causal/effects -> inference`
  - `causal/diagnostics -> inference`
  - `causal/sensitivity -> inference`.
- invalid/missing binding fails closed.
- affected E5 route/catalog/history/operation-availability behavior protected.

Pre-fix negative control:

```text
HEALTH: API READY
AFTER_PROJECT_SELECT_URL: .../projects/<id>/data
AFTER_EXPLORE_URL: .../projects/<id>/analysis/exploratory/profile
FAMILY_TAB_CONTAINER_COUNT: 1
FAMILY_BUTTON_COUNT: 0
STAGE_BUTTON_COUNT: 0
```

## 4. Required verification inputs — evidence / observation targets

- Fixed Trial Candidate SHA and clean candidate identity
- implementation completion/Candidate Assembly record
- package checkpoint identities for P01-P03
- candidate changed-file/diff inventory
- current source/tests/config/compose/browser runner
- previous protected test baselines where relevant
- browser evidence outputs from candidate execution

Planning/code agent self-reports are not acceptance authority; they may be cross-checked as evidence.

## 5. Candidate identity audit — MUST FIRST

Before functional judgment:

1. record branch and candidate SHA.
2. verify working tree clean or explain exact allowed evidence-only state.
3. verify Fixed Trial Candidate matches Candidate Assembly record.
4. verify required package checkpoint ancestry/inclusion.
5. inspect diff scope for prohibited canonical docs/ENH-E5 evidence/unrelated changes.
6. verify browser runner executed from candidate/current-source image, not stale manual service/image.

Identity ambiguity that prevents trustworthy evaluation => `BLOCKED` until resolved; do not test an arbitrary candidate.

## 6. Acceptance Criteria

| AC | Mandatory PASS condition |
|---|---|
| AC-E6-G01-001 Initial observable shell | fresh Project Analysis normal entry, before reload: 3 visible/operable catalog Family tabs; exactly one selected; current-Family-only Stage list visible/selected |
| AC-E6-G01-002 Family click default Stage | actual Family click -> target Family catalog default canonical URL, selected Family/Stage, local stage list, correct presentation |
| AC-E6-G01-003 Stage click | actual non-default Stage click retains Family and synchronizes URL/selected Stage/presentation |
| AC-E6-G01-004 Deep link/reload/history | direct canonical route, reload, Back/Forward reproduce URL + Family + Stage + presentation coherently |
| AC-E6-G01-005 Single transition authority regression | code/behavior audit shows supported entry handlers do not maintain parallel full state+history+shell+presentation mutation paths |
| AC-E6-G01-006 Stage-aware Causal presentation | causal/discovery => Discovery only; causal/identification & estimation => Inference only; Causal Family retained |
| AC-E6-G01-007 Legacy compatibility boundary | four legacy analytical entries converge to exact canonical contexts and immediate shell observability without split-brain legacy state |
| AC-E6-G01-008 Causal Inference entry semantics | Causal Inference shortcut opens `causal/identification`, not automatic estimation skip |
| AC-E6-G01-009 Fail closed | unknown Family/Stage, missing current Family/catalog invariant, missing supported presentation binding do not silently fall back |
| AC-E6-G01-010 Blocking real-browser proof | mandatory runner clicks actual Family tab and Stage control; static source existence alone cannot pass |
| AC-E6-G01-011 Protected regression | affected E5 parse/serialize/legacy normalize/catalog authority/resource-route/availability/back-forward behavior remains green |

All 11 are mandatory unless Test Agent declares inability to evaluate a specific AC as `BLOCKED`; missing test evidence is not implicit PASS.

## 7. Test Item plan

Canonical Trial01 Test Item IDs planned:

| Test Item | Scope | Primary layer | AC coverage |
|---|---|---|---|
| `001_candidate_identity` | Fixed Candidate/diff/protected path audit | audit | prerequisite to all |
| `002_navigation_and_binding_lower_layers` | unit/DOM resolver/transition/history/fail-closed | unit/integration | 002,003,005,006,008,009,011 |
| `003_architecture_static_audit` | duplicate authority/catalog/persistence/protected doc audit | static/code audit | 005,009,011 |
| `004_browser_normal_family_switch` | B01 | real Chromium | 001,002,010 |
| `005_browser_causal_legacy_boundary` | B02 | real Chromium | 006,007,008,010 |
| `006_browser_history_restore` | B03 | real Chromium | 003,004,010 |
| `007_protected_regression` | affected E5/product/browser regression | regression | 011 + cross-check |

### 7.1 Test layer allocation

- unit/pure: route/context/default/history-mode and presentation resolver detailed correctness.
- DOM/integration: transition -> selected UI/presentation/fail-closed behavior.
- static/code audit: no parallel full transition authority, no full duplicated catalog, no Navigation->Execution persistence, protected paths unchanged.
- browser E2E: real cross-layer observable critical journeys.
- regression: inherited affected behavior.

Browser E2E does not replace lower-layer detailed correctness; lower-layer tests do not replace observable E2E.

### 7.2 Gate blocking Browser E2E — conditional

Applicable and blocking. Canonical runner:

`tests/browser_e2e/run_enh_e6_family_stage_navigation.py`

Canonical command:

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

Environment requirements:

- current-source build/recreate through canonical command
- API/worker/frontend ready; runner waits for `#health` `API READY`
- fresh browser context
- deterministic Project creation/selection
- evidence output under browser_e2e evidence volume
- runner included in Docker build context/image; `.dockerignore` exclusion is a blocking harness defect, not product PASS

Synchronization: prefer app/DOM/network readiness signals over arbitrary sleeps; history/reload assertions wait for observable selected state/presentation.

Blocking journeys:

**B01 Normal entry -> Family switching**: Project context -> click Explore -> before reload assert 3 tabs/local stages -> click Predictive -> `/predictive/setup` -> click Causal -> `/causal/setup` with correct selected UI/presentation.

**B02 Causal legacy boundary**: Causal Discovery -> `/causal/discovery` Discovery active; Causal Inference -> `/causal/identification` Inference active; click estimation -> Inference remains active/Causal selected.

**B03 History restore**: Exploratory -> Predictive -> non-default stage -> Back/Forward with URL/Family/Stage/presentation identity; explicit canonical route reload preserves identity.

## 8. Protected passed-Gate regression

Test Agent must verify no unauthorized modification/regression of:

- `docs/wiki/requirement_definition/**`
- ENH-E5 frozen evidence/contracts/reports/decisions
- backend catalog authority/current Family values
- canonical route parse/serialize/legacy normalization behavior
- Navigation Stage vs Execution Stage separation/non-persistence
- affected route-dependent operation availability
- existing non-analysis navigation behavior materially touched by shell lifecycle

## 9. Transition Debt audit

- `ANOM-E5-001` may close only on G01 PASS.
- legacy visual left-nav retention is acceptable if it is compatibility-only and all ACs pass.
- no new silent fallback/parallel authority debt may be accepted unless explicitly recorded/approved outside this Trial.

## 10. Test Agent prohibited work

- modify production code to make candidate pass
- modify frozen 06/07/Pxx or canonical requirements during verification
- weaken AC/expected value based on actual implementation
- use Coding Agent statement as PASS proof without observation
- skip required browser journey because source tests are green
- test a different candidate than audited Fixed Trial Candidate
- repair browser harness/product and continue as if same immutable candidate unless workflow explicitly produces a new candidate

## 11. Evidence requirements

Each Test Item records:

- candidate SHA
- exact command/method
- exit/result
- observed facts
- requirement/AC mapping
- PASS/FAIL/BLOCKED rationale
- relevant files/log/screenshot/trace/video paths

Browser failure evidence minimum: URL, screenshot, Family/Stage selected/visible snapshot, active presentation/workspace, console errors, relevant network failure.

## 12. Decision semantics

### PASS

All mandatory ACs supported by required Test Items; B01-B03 all pass; protected regression passes; candidate identity valid; no blocking unsupported/prohibited scope.

### FAIL

Candidate defect or prohibited regression causes one or more mandatory ACs to fail with sufficient evidence. Formal FAIL can create next Trial after contract validity check.

### BLOCKED

Candidate identity/environment/prerequisite/harness prevents reliable acceptance judgment and is not itself proven product candidate defect. BLOCKED is not PASS or FAIL and does not increment Trial automatically.

## 13. Remediation Trial handling

After formal FAIL:

1. preserve Trial01 evidence immutable.
2. determine whether 06/07 semantic contract remains valid.
3. if valid: create/freeze Trial02 remediation 08 using appropriate route.
4. if contract defect: Human-approved 09 amendment/re-baseline instead of AC relaxation.
5. do not send Coding Agent back to normal Pxx route while current remediation contract applies.

## 14. Required outputs

For Trial01 independent verification:

- `30_test_report/G01/Trial01/` Test Item reports for 001-007 as applicable
- failure/browser evidence paths
- `999` Gate Decision with PASS/FAIL/BLOCKED and AC summary
- exact Fixed Trial Candidate identity
- if PASS: recommendation to promote verified state/update TD; promotion is subsequent state-control action
- if FAIL/BLOCKED: explicit next workflow route without editing historical evidence
