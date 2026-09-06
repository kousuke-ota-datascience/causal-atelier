# Post-Migration Verification

**Status:** `NOT_STARTED`  
**Purpose:** closure checklist for Test Architecture Migration

## 1. Structural verification

- [ ] target directories exist as designed
- [ ] active tests have no ambiguous ownership between `regression` and `enhancement`
- [ ] current ENH-E9 tests are under `tests/enhancement/enh_e9/...`
- [ ] permanent regression filenames no longer depend on historical Enhancement identity unless explicitly justified
- [ ] `tests/legacy_archive/` remains excluded from normal pytest collection
- [ ] scientific benchmarks remain separately identifiable

## 2. Pytest collection / fixture verification

- [ ] default pytest collection succeeds
- [ ] expected active test count is reconciled against pre-migration baseline
- [ ] no tests are silently dropped by path changes
- [ ] no legacy tests are accidentally reintroduced
- [ ] shared fixtures resolve from intended scopes
- [ ] PostgreSQL-dependent tests retain explicit skip/marker behavior
- [ ] custom markers remain registered and meaningful

## 3. Regression verification

- [ ] unit regression suite passes
- [ ] contract regression suite passes
- [ ] integration regression suite passes
- [ ] frontend regression suite passes
- [ ] scientific deterministic regression suite passes
- [ ] benchmark suite can be invoked separately from default blocking regression as intended

## 4. Enhancement verification

- [ ] ENH-E9 G01/G02 test paths are executable independently
- [ ] G02 focused frontend tests retain their original acceptance semantics
- [ ] enhancement-specific tests are not accidentally required as historical permanent regression without disposition

## 5. Browser E2E verification

- [ ] canonical `run_project_lifecycle.py` executes the current Project lifecycle
- [ ] canonical `run_analysis_navigation.py` executes current family/stage navigation and history behavior
- [ ] canonical `run_causal_critical_journey.py` executes Discovery -> candidate -> comparison -> adopt/fix connectivity
- [ ] canonical `run_predictive_critical_journey.py` executes current predictive connectivity
- [ ] no canonical runner imports historical Enhancement runner modules
- [ ] Browser runner assertions target semantic observable state / canonical routes rather than obsolete internal DOM where avoidable
- [ ] traces/screenshots/logs/evidence are still produced on failure

## 6. Docker / CI / command-reference verification

- [ ] `Dockerfile.browser-e2e` references current canonical runner paths
- [ ] `.dockerignore` includes required test files/directories
- [ ] Compose/browser execution commands use current paths
- [ ] CI/workflow scripts use current paths
- [ ] documentation/operator prompts do not invoke archived runner paths
- [ ] repository search finds no unintended stale references to migrated paths

## 7. Semantic non-regression audit

For each `SPLIT`, `MERGE`, `RETIRE`, or `ARCHIVE` action:

- [ ] durable current invariant has an identified replacement test, or
- [ ] explicit rationale confirms the behavior is no longer authoritative.

No assertion may disappear solely because it was inconvenient to migrate.

## 8. G02 provenance protection

- [ ] G02 Trial01 Fixed Candidate identity remains unchanged by test architecture migration
- [ ] G02 frozen `07` remains unchanged
- [ ] Browser harness repair/migration commits are distinguishable from product candidate commits
- [ ] G02 Independent Verification is rerun under the same Trial after the test-side blocker is resolved

## 9. Closure record

Complete only after migration execution.

```text
Final migration commit(s):
Pre-migration baseline SHA:
Post-migration verification SHA:
Regression result:
Enhancement result:
Browser result:
Known residual risks:
Final status: PASS | BLOCKED | FAIL
```
