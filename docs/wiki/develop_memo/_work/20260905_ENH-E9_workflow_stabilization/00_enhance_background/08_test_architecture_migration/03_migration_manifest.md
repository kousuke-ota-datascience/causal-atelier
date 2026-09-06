# Test Migration Manifest

**Status:** `DRAFT`  
**Purpose:** source-to-target migration authority for test architecture restructuring

## 1. Manifest rules

Each migration item must record:

- source path;
- target path or target test family;
- action;
- rationale;
- dependency notes;
- verification required after migration.

Allowed action vocabulary:

```text
KEEP
MOVE
RENAME
PROMOTE
REWRITE
MERGE
SPLIT
ARCHIVE
RETIRE
REVIEW_SUPERSEDED
```

No file is physically moved until its manifest row is approved enough to avoid ambiguous ownership.

## 2. Initial high-confidence mappings

| Source | Target | Action | Notes |
|---|---|---|---|
| `tests/browser_e2e/run_enh_e7_project_integration.py` | `tests/regression/browser_e2e/run_project_lifecycle.py` | `PROMOTE + REWRITE` | current Project lifecycle source |
| `tests/browser_e2e/run_enh_e8_g01_project_return.py` | `tests/regression/browser_e2e/run_project_lifecycle.py` | `MERGE` | merge return/history scenarios into canonical project journey |
| `tests/browser_e2e/run_enh_e6_family_stage_navigation.py` | `tests/regression/browser_e2e/run_analysis_navigation.py` | `PROMOTE + REWRITE` | remove Enhancement identity; retain current family/stage navigation |
| `tests/browser_e2e/run_enh_e3_predictive.py` | `tests/regression/browser_e2e/run_predictive_critical_journey.py` | `PROMOTE + REWRITE` | distill current predictive journey |
| `tests/browser_e2e/run_enh_e1a.py` | historical archive + causal scenario source | `ARCHIVE + SPLIT` | do not repair wholesale as canonical regression |
| `tests/browser_e2e/run_enh_e3.py` | historical archive + scenario source | `ARCHIVE + SPLIT` | depends on historical runner behavior; distill current invariants only |
| `tests/product/test_enh_e9_g02_p01_discovery_copy_help_overflow.py` | `tests/enhancement/enh_e9/g02/frontend/test_discovery_copy_help_overflow.py` | `MOVE + RENAME` | active G02 delta |
| `tests/product/test_enh_e9_g02_p02_selection_comparison_clarity.py` | `tests/enhancement/enh_e9/g02/frontend/test_selection_comparison_clarity.py` | `MOVE + RENAME` | active G02 delta |
| `tests/product/test_enh_e9_g02_p03_adoption_feedback_export.py` | `tests/enhancement/enh_e9/g02/frontend/test_adoption_feedback_export.py` | `MOVE + RENAME` | active G02 delta |
| `tests/scientific_benchmarks/` | `tests/benchmarks/scientific/` | `MOVE + REWRITE_NAMES_AS_NEEDED` | preserve benchmark marker/semantics |
| `tests/legacy_archive/` | unchanged | `KEEP` | remain excluded from default collection |

## 3. Generic product tests

Initial target families:

| Source pattern | Target family | Action |
|---|---|---|
| `tests/product/test_architecture.py` | `tests/regression/contract/architecture/` | `PROMOTE` |
| `tests/product/test_cli_contract.py` | `tests/regression/contract/` | `PROMOTE` |
| `tests/product/test_domain_and_snapshot.py` | `tests/regression/unit/` | `PROMOTE` |
| `tests/product/test_frontend_contract.py` | `tests/regression/frontend/` | `PROMOTE` |
| `tests/product/test_postgres_contract.py` | `tests/regression/integration/persistence/` | `PROMOTE` |
| `tests/product/test_api_worker_e2e.py` | `tests/regression/integration/` | `PROMOTE_REVIEW_LAYER` |
| `tests/product/compose_golden_path_smoke.py` | `tests/regression/integration/` | `PROMOTE_REVIEW_LAYER` |

Exact filenames are pending semantic review.

## 4. Enhancement-family review groups

### E1-E3

Action: `PROMOTE + REWRITE + DEDUPE` for still-current behavior.

Remove historical Enhancement identity from permanent regression filenames unless provenance itself is a requirement.

### E4

Action: `SPLIT`.

- canonical execution/result/artifact/lineage invariants -> regression
- migration/cutover procedure assertions -> archive or retire after extraction

### E5

Action:

- navigation/history -> `REVIEW_SUPERSEDED` against E6/E7
- causal/predictive/exploratory semantics -> `PROMOTE + MERGE`

### E6-E8

Action: primarily `PROMOTE + MERGE`, with migration/runner-specific assertions rewritten into current generic contracts.

### E9

Action: `ACTIVE_ENH` until Gate/Enhancement completion. Promotion occurs only after explicit disposition review.

## 5. Support migration

`tests/conftest.py` and `tests/product/conftest.py` are not mechanically moved in the first batch.

Before migration, record:

- fixture consumers;
- pytest discovery scope;
- environment variables;
- import/path assumptions;
- Docker/CI references.

Potential future targets:

```text
tests/support/fixtures/
tests/support/factories/
tests/support/helpers/
```

but conftest placement may remain structural rather than fully centralized.

## 6. Manifest completion condition

Physical migration may start only when:

1. all active test files have a disposition;
2. all `SPLIT` / `MERGE` rows identify destination invariants;
3. Browser/CI/Docker path references are inventoried;
4. pytest fixture scope impact is understood;
5. active ENH-E9 tests are separated from permanent regression candidates.
