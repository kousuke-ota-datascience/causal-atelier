# E4-G07 Trial01 Implementation Completion Report

## Identification

| Field | Value |
|---|---|
| Gate / Trial | E4-G07 / 01 |
| P04 Entry SHA | `8e4d7cd6119bc995fca7ea44183bfc7d13ed3445` |
| P01 checkpoint | `e10a6e3d1305cf31d61d669f6e6d41a1b41e8ce1` |
| P02 checkpoint | `102d0c1539eee8a1d605a709c599a21e99e3ab15` |
| P03 checkpoint | `8e4d7cd6119bc995fca7ea44183bfc7d13ed3445` |
| Fixed Implementation/Test Candidate SHA | `8e4d7cd6119bc995fca7ea44183bfc7d13ed3445` |
| Product Migration Head | `20260809_product_0010` |
| TD-005 | CLOSURE_CANDIDATE |
| Gate | READY_FOR_TEST |

This is a Coding Agent completion report, not an Independent Test decision. It does not declare E4-G07 PASS or TD-005 CLOSED.

## Package Chain

| Package | Status | Primary evidence |
|---|---|---|
| P01 | COMPLETE | Product/API/worker/shared-science transitive legacy reachability guard and deployment boundary contracts. |
| P02 | COMPLETE | Product-only Alembic/bootstrap guard and fresh PostgreSQL version/schema evidence. |
| P03 | COMPLETE | Closed analysis-CLI classification, no-persistence reachability guard, local manifest boundary. |
| P04 | COMPLETE | Final-state rerun, candidate freeze, residual inventory, and Independent Test handoff. |

## G07 Acceptance Matrix

| Gate AC | Result | Final-state evidence |
|---|---|---|
| AC-001 Runtime legacy independence | PASS | `test_architecture.py` + P01 AST transitive graph; Product/API/worker → `ariadne.legacy` = 0. |
| AC-002 Deployment legacy independence | PASS | P01 deployment contracts for package scripts, wheel/Docker exclusion, Docker API, and compose worker; legacy invocation = 0. |
| AC-003 Shared scientific preservation | PASS | P01 retained-root graph plus import smoke for worker, `ScientificCoreAdapter`, causal, preprocessing, shared. |
| AC-004 Product-only bootstrap | PASS | P02 guard; fresh PostgreSQL reset/upgrade/current; Product version table at repository head; root version/schema absent. |
| AC-005 CLI lifecycle / compatibility | PASS | P03 closed CLI inventory, no legacy/persistence reachability, local manifests without Product IDs, and terminology inventory. |

## Gate-wide Verification

### Static / local

```text
15 passed, 1 skipped (P02 PostgreSQL-only node)
```

Executed: `tests/product/test_architecture.py`, G07 P01/P02/P03 guard tests, and `tests/product/test_cli_contract.py`. The P02 skip is covered by the fresh PostgreSQL run below.

### Migration graph

`uv run alembic -c alembic_product.ini heads` returned one head: `20260809_product_0010`. History is the Product chain from `20260805_product_0001` to that head; no root-chain splice was observed.

### Fresh PostgreSQL

Runner evidence:

```text
/tmp/ariadne-g07-p04-pg-evidence/run-20260809T231004Z.txt
/tmp/ariadne-g07-p04-pg-evidence/run-20260809T231004Z.metadata.txt
```

Fresh reset, Product migration upgrade, `current`, and pytest all exited 0; 25 tests passed. The DB revision equals `20260809_product_0010`; `alembic_version_product` exists; root `alembic_version` and root-only `app_user` are absent.

### Protected regressions / hygiene

- G02–G06 local authority selection: 42 passed.
- Representative G03–G05 PostgreSQL persistence selection is included in the 25-pass fresh runner.
- `compileall -q src/ariadne tests/product`: PASS.
- `git diff --check`: PASS; the candidate worktree was clean when frozen.

## Final Residual Legacy Inventory

| Path / surface | Classification | Runtime reachable? | Deployment reachable? | Bootstrap reachable? | Persistent authority? | Shared capability required? | G07 final action | G08 residual | Evidence |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| `src/ariadne/legacy/` | RETIRED_UNREACHABLE | no | no | no | no | no | Retain; no speculative deletion. | Optional physical archive/source cleanup. | P01 AST guard; wheel/Docker exclusion. |
| Product/API/worker roots | ACTIVE_PRODUCT_DEPENDENCY (canonical) | yes | yes | no | yes | no | Preserve canonical authority. | none | P01 guard + protected regressions. |
| `pyproject.toml`, Dockerfile, `.dockerignore`, compose API/worker | ACTIVE_PRODUCT_DEPENDENCY (boundary control) | yes | yes | no | yes | no | Preserve canonical registrations/exclusions. | none | P01 deployment contracts. |
| `ariadne.causal`, `ariadne.preprocessing`, `ariadne.shared`, `ariadne.scientific` | RETAIN_SHARED_CAPABILITY | yes | indirectly | no | no | yes | Preserve unchanged. | none | P01 graph + import smoke. |
| `alembic_product.ini` / `product_migrations` | ACTIVE_PRODUCT_DEPENDENCY (canonical) | no | yes | yes | yes | no | Preserve sole Product migration chain. | none | P02 guard + final fresh PostgreSQL. |
| Root `alembic.ini` / `migrations` | HISTORY_ONLY | no | no | no | no | no | Retain without rewrite/deletion. | Optional archive cleanup. | P02 guard + root version/schema absence. |
| Standalone scientific CLI / manifests | LOW_LEVEL_UTILITY | yes | no | no | no | yes | Preserve local scientific/file boundary. | Future auditable CLI requires explicit classification. | P03 graph + local runtime contracts. |
| `legacy-product-snapshot/1` and read-only legacy projection terms | COMPATIBILITY_DATA_CONTRACT | Product domain only | no | no | no | no | Retain compatibility validation/projection names. | Bounded contract retirement decision. | P03 consumer inventory. |

No retired legacy runtime or root legacy migration has `ACTIVE_PRODUCT_DEPENDENCY` status.

## Facts, Interpretation, Unknowns

### Facts

- Final candidate evidence proves runtime/deployment legacy reachability is zero, Product bootstrap selects only `product_migrations`, and low-level CLIs do not own persistence.
- Shared scientific modules remain importable without legacy orchestration.
- Physical legacy source and root migration history remain, explicitly non-authoritative.

### Interpretation

The seven TD-005 closure-candidate conditions in P04 §10 are satisfied. Therefore TD-005 is a **CLOSURE_CANDIDATE**, not closed.

### Unknowns / limits

- Independent Test has not yet independently reproduced the gate evidence; Gate PASS and TD-005 CLOSED are therefore unknown/not established.
- A future auditable CLI does not exist in the current inventory; its required canonical submission behavior is a forward boundary, not runtime evidence for a present feature.

## G08 Residuals

- Physical legacy source/archive cleanup, if desired.
- Bounded compatibility terminology/read-contract retirement after an explicit product data-contract decision.
- Final whole-architecture zero-debt audit (TD-006 scope).

These residuals are non-authoritative and do not reactivate Product runtime, deployment, bootstrap, or persistent lifecycle ownership.

## Handoff

```text
Coding Agent P04: COMPLETE
Gate: READY_FOR_TEST
Fixed Candidate: 8e4d7cd6119bc995fca7ea44183bfc7d13ed3445
Independent Test Contract: READY
TD-005: CLOSURE_CANDIDATE
```

Independent Test input is the pre-authored [G07 test instruction](../../../10_enhance_instruction/G07/07_Ariadne_ENH-E4_G07_テスト指示書.md), this completion report, the fixed candidate, and current repository. Its decision must be written to `30_test_report/G07/Trial01/E4-G07_01_999_gate_decision.md`.
