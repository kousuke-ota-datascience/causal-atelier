# Test Classification Inventory

**Status:** `INITIAL_BASELINE`  
**Inventory date:** 2026-09-06  
**Repository branch:** `bugfix/ariadne_mvp_e9`

## 1. Classification vocabulary

| Classification / Action | Meaning |
|---|---|
| `PROMOTE` | Move current authoritative behavior into permanent regression coverage |
| `PROMOTE_REWRITE` | Preserve semantic coverage but rewrite/rename to remove historical Enhancement identity or obsolete structure |
| `MERGE` | Consolidate overlapping tests into a smaller current regression surface |
| `SPLIT` | Separate current invariant coverage from migration/history-only assertions |
| `ACTIVE_ENH` | Keep under the currently active Enhancement staging area |
| `BENCHMARK` | Keep as scientific/statistical benchmark, separate from normal regression |
| `ARCHIVE` | Preserve as historical evidence but remove from active regression execution |
| `REVIEW_SUPERSEDED` | Compare with newer tests and retain only unique current invariants |
| `KEEP` | Retain current placement/role |

## 2. Current top-level structure

Current repository test areas:

```text
tests/
├── browser_e2e/
├── integration/
├── legacy_archive/
├── product/
├── scientific/
└── scientific_benchmarks/
```

The current tree mixes lifecycle/authority and verification-layer concepts at the same directory level. `product` and `scientific` describe domain/purpose, while `integration` and `browser_e2e` describe verification layers.

## 3. Initial inventory by test family

### 3.1 Generic product tests

Examples:

- `tests/product/compose_golden_path_smoke.py`
- `tests/product/test_api_worker_e2e.py`
- `tests/product/test_architecture.py`
- `tests/product/test_cli_contract.py`
- `tests/product/test_domain_and_snapshot.py`
- `tests/product/test_frontend_contract.py`
- `tests/product/test_postgres_contract.py`

Initial disposition: **PROMOTE** into `tests/regression/<layer>/...` according to actual verification layer.

### 3.2 ENH-E1 / E2 / E3 product tests

Examples include analysis specification/view, causal workflow, predictive workflow, exploratory workflow, research context, lineage/export, estimator compatibility, and frontend contracts.

Initial disposition: **PROMOTE_REWRITE**. Historical suffixes such as `_e3` should not define permanent regression identity when the asserted behavior remains current.

### 3.3 ENH-E4 execution-authority tests

E4 contains both durable execution semantics and historical migration/cutover assertions.

Durable examples:

- rerun creates a new canonical execution;
- base execution remains immutable;
- stage semantics and revision lineage are preserved;
- canonical execution/result/artifact authority remains consistent.

Initial disposition: **SPLIT**.

- durable current invariants -> `PROMOTE_REWRITE`
- migration/cutover procedure/history -> `ARCHIVE` or retire after invariant extraction

### 3.4 ENH-E5 tests

Navigation tests are likely superseded by E6/E7 navigation architecture.

Initial disposition:

- old navigation/history shell tests -> `REVIEW_SUPERSEDED`
- predictive/causal/exploratory semantic tests -> `PROMOTE_REWRITE` / `MERGE`

### 3.5 ENH-E6 tests

Navigation and stage-presentation behavior remains relevant, but static tests that assert a specific historical Browser runner filename are too implementation-specific.

Initial disposition:

- navigation semantics -> `PROMOTE_REWRITE`
- specific runner integration assertions -> `SPLIT` and rewrite as generic Browser harness contract

### 3.6 ENH-E7 tests

E7 Project / Analysis routing and surface architecture are strong sources for current regression coverage. Migration/cutover/cleanup assertions are mixed in the same family.

Initial disposition:

- current Project / Analysis invariants -> `PROMOTE_REWRITE` / `MERGE`
- migration/cutover/history assertions -> `SPLIT` / `ARCHIVE`

### 3.7 ENH-E8 tests

Current causal/predictive stage-surface behavior is likely permanent regression behavior.

Initial disposition: **PROMOTE_REWRITE / MERGE**.

### 3.8 ENH-E9 tests

Current files include G01/G02 and causal-result/estimation-presentation guards.

Initial disposition: **ACTIVE_ENH**.

Proposed location pattern:

```text
tests/enhancement/enh_e9/<gate>/<layer>/...
```

Special case: `test_enh_e9_causal_result_presentation.py` mixes product presentation assertions with an assertion against an ENH-E9 work/handoff document. It requires **SPLIT** before permanent promotion.

## 4. Browser E2E inventory

| Existing runner | Initial disposition |
|---|---|
| `run_enh_e1a.py` | `ARCHIVE` + extract still-valid scenarios |
| `run_enh_e3.py` | `ARCHIVE` / `DISTILL` |
| `run_enh_e3_predictive.py` | `PROMOTE_REWRITE` into predictive critical journey |
| `run_enh_e6_family_stage_navigation.py` | `PROMOTE_REWRITE` into analysis navigation regression |
| `run_enh_e7_project_integration.py` | `PROMOTE_REWRITE` into project lifecycle regression |
| `run_enh_e8_g01_project_return.py` | `MERGE` into project lifecycle regression |
| `run_enh_e8_g02_causal_stage_content.py` | `MERGE` into causal/navigation regression |
| `run_enh_e8_g02_predictive_stage_content.py` | `MERGE` into predictive regression |

Important observation: historical Browser runners have dependency chains and stale navigation assumptions. They must not be treated as immutable regression authorities simply because they were once acceptance runners.

## 5. Scientific tests

### `tests/scientific/`

These tests contain deterministic scientific product semantics such as identification/eligibility behavior, discovery graph semantics, estimator recovery, overlap handling, and explicit requirement linkage.

Initial disposition: primarily **PROMOTE** into current scientific regression layers, not characterization-only storage.

### `tests/scientific_benchmarks/`

These tests evaluate repeated synthetic/semi-synthetic scenarios, bias/RMSE/coverage, and scientific acceptance thresholds.

Initial disposition: **BENCHMARK** under `tests/benchmarks/scientific/`.

## 6. Existing integration directory

### `tests/integration/test_core.py`

Contains mixed pure-unit, config, feature-semantic, and architecture-boundary assertions.

Initial disposition: **SPLIT** into unit/contract regression layers.

### `tests/integration/test_inference.py`

Contains estimator and fixed-seed scientific behavior that overlaps newer scientific tests.

Initial disposition: **PROMOTE_REWRITE / DEDUPE REVIEW**.

## 7. Legacy and support

### `tests/legacy_archive/`

Already isolated from normal pytest collection.

Initial disposition: **KEEP**.

### `conftest.py` / shared fixtures

Fixture placement affects pytest scope and discovery. Do not move these mechanically during the first migration batch.

Initial disposition: **SUPPORT REVIEW**, migrate only after dependency analysis.

## 8. Confidence and unresolved work

High-confidence conclusions:

- current ENH-E9 tests belong in enhancement staging;
- historical Browser runners must be distilled, not blindly repaired/promoted;
- scientific benchmarks remain separate from standard regression;
- legacy archive should remain excluded;
- migration/cutover history must not become permanent product regression merely because the tests still pass.

Pending before physical migration:

1. file-by-file duplicate/superseded comparison for E1-E8;
2. exact target verification layer per file;
3. final rename targets;
4. fixture/import/path dependency analysis;
5. CI / Docker / command reference inventory.
