# Target Test Architecture

**Status:** `PROPOSED_BASELINE`  
**Scope:** filesystem organization and test lifecycle policy

## 1. Target filesystem

```text
tests/
├── regression/
│   ├── unit/
│   │   ├── causal/
│   │   ├── predictive/
│   │   └── scientific/
│   ├── contract/
│   │   ├── architecture/
│   │   ├── causal/
│   │   ├── predictive/
│   │   └── scientific/
│   ├── integration/
│   │   ├── api/
│   │   ├── worker/
│   │   ├── persistence/
│   │   └── execution/
│   ├── frontend/
│   │   ├── project/
│   │   ├── navigation/
│   │   ├── causal/
│   │   └── predictive/
│   └── browser_e2e/
│       ├── run_project_lifecycle.py
│       ├── run_analysis_navigation.py
│       ├── run_causal_critical_journey.py
│       └── run_predictive_critical_journey.py
│
├── enhancement/
│   └── enh_e9/
│       ├── g01/
│       ├── g02/
│       │   ├── unit/
│       │   ├── contract/
│       │   ├── integration/
│       │   ├── frontend/
│       │   └── browser_e2e/
│       └── ...
│
├── characterization/
│   └── scientific/
│
├── benchmarks/
│   └── scientific/
│
├── support/
│   ├── fixtures/
│   ├── factories/
│   └── helpers/
│
└── legacy_archive/
```

## 2. Orthogonal classification axes

### Lifecycle / authority axis

- `regression` — current authoritative product behavior that must continue to hold
- `enhancement` — active Enhancement delta under development/verification
- `characterization` — observational/scientific characterization that is not a hard regression contract
- `benchmarks` — repeated scientific/statistical acceptance benchmarks
- `support` — fixtures/factories/helpers, not independent assertions
- `legacy_archive` — retired historical tests excluded from normal collection

### Verification-layer axis

- `unit`
- `contract`
- `integration`
- `frontend`
- `browser_e2e`

These axes are intentionally orthogonal. A test must first have a lifecycle/authority role, then a verification layer.

## 3. Regression definition

`tests/regression/` is not a historical archive of all previously passing tests.

A regression test must represent **current authoritative behavior**. If an intentional Enhancement changes navigation, API shape, or internal architecture while preserving product semantics, the regression suite is re-authored to express the new current contract.

Regression expectations must not be weakened merely to make a failing test pass. Each drift must be classified:

| Drift type | Required action |
|---|---|
| Intended specification change | update regression to the newly approved current contract |
| Product violates existing contract | fix product; do not weaken regression |
| Implementation/DOM/navigation changes but semantics remain | update harness/locator/route expression |
| Old specification retired | explicitly replace/remove old regression with recorded decision |

## 4. Enhancement test lifecycle

New or changed behavior begins under:

```text
tests/enhancement/<enhancement>/<gate>/<layer>/
```

After Gate/Enhancement stabilization, each test receives a disposition:

```text
PROMOTE      -> move current invariant into regression
REWRITE      -> preserve semantics while replacing historical/temporary structure
MERGE        -> combine overlapping assertions into canonical regression
SPLIT        -> separate current invariant from migration/history-only assertions
RETIRE       -> remove no-longer-needed temporary assertion
ARCHIVE      -> preserve historical evidence outside active regression
```

Promotion is semantic, not necessarily a file move. Enhancement-specific tests may be distilled into fewer canonical regression tests.

## 5. Browser E2E policy in target architecture

Browser E2E is restricted to critical cross-layer user journeys. Detailed correctness remains primarily in lower deterministic layers.

Initial canonical Browser regression candidates:

1. `run_project_lifecycle.py`
   - Project List -> New Project -> overview/context/data/results -> return/history
2. `run_analysis_navigation.py`
   - Project -> analysis family/stage navigation -> direct entry/reload/back-forward
3. `run_causal_critical_journey.py`
   - dataset/fixture -> Discovery -> candidate -> comparison -> adopt/fix -> persisted observable result
4. `run_predictive_critical_journey.py`
   - dataset/fixture -> predictive setup/run -> result -> persisted observable result

Historical Enhancement acceptance runners are sources for scenario extraction, not permanent authorities.

## 6. ENH-E9 initial placement

Current G02 focused tests should stage under:

```text
tests/enhancement/enh_e9/g02/frontend/
├── test_discovery_copy_help_overflow.py
├── test_selection_comparison_clarity.py
└── test_adoption_feedback_export.py
```

A dedicated G02 Browser connectivity runner may stage under:

```text
tests/enhancement/enh_e9/g02/browser_e2e/
```

until its durable behavior is distilled into the canonical causal critical journey.

## 7. Migration invariants

The migration must preserve the following:

- no product semantic change solely for filesystem cleanup;
- no weakening/removal of current authoritative assertions without recorded disposition;
- no mutation of G02 Fixed Trial Candidate as part of test architecture work;
- legacy archive remains excluded from default pytest collection;
- scientific benchmark execution remains separately identifiable;
- fixture resolution and pytest markers remain valid;
- Docker/CI/browser runner paths are updated atomically when files move.
