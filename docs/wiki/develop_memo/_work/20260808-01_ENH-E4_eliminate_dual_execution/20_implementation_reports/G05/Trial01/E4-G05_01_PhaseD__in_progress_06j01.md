# E4-G05 Trial 01 Phase D — D1 実行状況報告（06j01）

- Gate: E4-G05
- Trial: 01
- Phase: D
- Work package: D1 — Legacy claim/process authority shutdown
- 実装指示 ID: 06j01
- 開始時 HEAD: `fc88d3a98b2d66d0318742a360538da12d36c3d8`
- D1 checkpoint: `e831e3f78d4791a2d4a0ef96f6ce80058c376fae`
- 状態: PHASE_D_D1_COMPLETE

## 指示実行結果

### 結論

D1 の完了条件を満たした。新 Product worker の claim authority は canonical `uow.executions.claim_next()` のみであり、Exploratory / Predictive に残す旧 Family claim/process facade は明示的 reject となった。Phase D の D2 / D3 は実施していない。

### 実装した変更

- `ExploratoryWorkspaceService.claim_next` / `process_execution` を `LegacyProductAuthorityDisabled` で明示 reject に変更した。
- `PredictiveWorkflowService.claim_next` / `process_execution` を同様に明示 reject に変更した。
- worker runner の call graph は `uow.executions.claim_next()` → `ExecutionProcessor.process()` の一経路であることを architecture/boundary test で固定した。family dispatch は canonical claim 後に `ExecutionProcessor` 内で行われる。
- 旧 E3 の Exploratory / Predictive worker 呼出しを canonical claim + `ExecutionProcessor` に置換した。
- canonical worker の実行で判明した以下の Product defect を最小修正した。
  - Predictive の Analysis View hash を immutable family snapshot から split runner へ渡す。
  - Predictive runtime metadata を scientific runner snapshot に保持する。
  - family Artifact の `result_type` を保持し、MODEL_CARD / PREDICTIVE_EXPLANATION を対応する canonical Result に関連付ける。
  - Predictive model-card / explanation lineage と Exploratory input lineage を canonical owner に保存する。
  - unified Product result projection が canonical Execution の `analysis_family` と family schema/context を使用する。

### Authority Inventory

| 対象 | 実態 | D1 disposition |
|---|---|---|
| Product worker runner | `uow.executions.claim_next` → `ExecutionProcessor` | canonical sole authority |
| Exploratory `claim_next` / `process_execution` | Family ORM を使う旧 body が source に残存 | EXPLICIT_REJECT |
| Predictive `claim_next` / `process_execution` | Family ORM を使う旧 body が source に残存 | EXPLICIT_REJECT |
| Causal family-specific claim/process | `src/ariadne/product/application/`、worker/web API/CLI を検索 | NOT_FOUND |
| `GenericExecutor` | scientific stage executor | non-authoritative（G03 boundary PASS） |

### No-fallback / old-table negative

PostgreSQL D1 test は Exploratory / Predictive の旧 Family trap row（Execution / StageExecution / Result / Artifact）を seed し、4つの旧 facade を直接呼んだ。すべて `LegacyProductAuthorityDisabled` で reject され、Family table の row count と status は不変だった。

同じ test で canonical Execution を claim 後に controlled processing failure を注入した。canonical Execution は FAILED となり、旧 Family table は不変だった。canonical failure から旧 claim/process authority への fallback は観測されない。

### 検証結果

- `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g05_phase_d_d1_legacy_claim_shutdown_postgres.py`
  - PASS: 2 passed、exit 0。
  - Evidence: `test-results/postgres/run-20260809T094611Z.txt`
- `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g05_phase_d_d1_legacy_claim_shutdown_postgres.py tests/product/test_predictive_api_worker_e2e_e3.py::test_predictive_execution_plan_async_worker_results_artifacts_and_lineage tests/product/test_enh_e4_g05_phase_c_retry_postgres.py tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py tests/product/test_enh_e4_g05_phase_c_revise_postgres.py tests/product/test_enh_e4_g05_phase_c_authority_audit_postgres.py tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g04_result_artifact_postgres.py`
  - PASS: 17 passed、exit 0。
  - Evidence: `test-results/postgres/run-20260809T094638Z.txt`
- `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_enh_e4_g03_generic_executor_boundary.py`
  - PASS: 12 passed、exit 0。
  - Evidence: `test-results/postgres/run-20260809T094704Z.txt`
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q tests/product/test_enh_e4_g05_phase_d_d1_legacy_claim_shutdown_postgres.py tests/product/test_exploratory_api_worker_e2e_e3.py tests/product/test_predictive_explanation_e3.py tests/product/test_enh_e3_api_worker_e2e.py`
  - PASS: 9 passed、1 skipped。skip は PostgreSQL fixture 未設定のためであり、D1 PostgreSQL runner で同 test は実行済み。
- Product migration head: `20260809_product_0010` を標準 PostgreSQL runner で確認。
- `git diff --check`: PASS（checkpoint commit 前）。

### D1 completion checklist

- [DONE] actual claim/process authority inventory
- [DONE] Product worker canonical sole claim authority
- [DONE] Exploratory old claim/process explicit reject
- [DONE] Predictive old claim/process explicit reject
- [DONE] Causal inventory（family-specific old method NOT_FOUND）
- [DONE] direct old method cannot mutate Family lifecycle/output
- [DONE] canonical failure → old authority fallback NONE
- [DONE] old Family `SELECT FOR UPDATE` は new Product claim path から unreachable
- [DONE] GenericExecutor non-authoritative
- [DONE] D1 behavior / PostgreSQL / Phase C / G02 / G03 / G04 regression
- [DONE] migration head / diff check / D1 checkpoint

### 残作業

D2 は Product composition の legacy submit / lifecycle mutation branch shutdown と bounded read compatibility を扱う。D3 は全 family の global reachability、failure fallback、old-table runtime negative matrix、Phase D final report を扱う。今回の D1 では実施していない。

