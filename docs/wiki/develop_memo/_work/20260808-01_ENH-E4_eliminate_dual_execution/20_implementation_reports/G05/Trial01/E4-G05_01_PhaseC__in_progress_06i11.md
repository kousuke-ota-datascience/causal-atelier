# E4-G05 Trial 01 Phase C In-Progress Status Report 06i11

- Gate / Trial / Phase: `E4-G05` / `01` / `C`
- Work package: `C3a — Predictive canonical rerun`
- Status: `PHASE_C_C3A_COMPLETE`
- C3a checkpoint SHA: `daedd9244bf73f586b77ff6da11a1c4de91db55c`

## 実装結果

Product-facing `PredictiveWorkflowService.rerun()` の canonical 分岐は、base を
canonical `ExecutionService` から取得し、同じ固定 Predictive specification / plan / seed で
`submit_execution()` を呼ぶ。結果として `ExecutionService.create_family_execution()` が新しい
canonical Execution と新しい persistent StageExecution set を作成する。

base Execution は参照専用であり、rerun により reset・削除・更新されない。`revision_context` は
scientific condition の変更ではなく、base identity / snapshot hash / RERUN を記録する provenance
として新 Execution の snapshot に追加される。

## C3a PostgreSQL 検証

対象テスト: `tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py`

標準 runner により real PostgreSQL で PASS した。

```text
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py

1 passed in 0.66s
pytest_exit_code=0
```

確認した事実:

- rerun は base と異なる canonical Execution ID を作成する。
- new `base_execution_id` は base Execution ID と一致する。
- `analysis_family=PREDICTIVE`、`revision_kind=RERUN`、`change_reason=None` を保持する。
- dataset、analysis specification、execution plan、algorithm、parameters、seed、runtime family snapshot を保持する。
- new StageExecution set は存在し、すべての ID は base set と異なる。一方、stage key/type/dependencies/ordinal は等価である。
- base の status、retry_count、StageExecution IDs、Result IDs、Artifact IDs は rerun 前後で不変である。
- `FamilyExecution`、`FamilyStageExecution`、`FamilyResult`、`FamilyArtifact` の row count は rerun 前後で不変である。
- cross-project、non-PREDICTIVE、unknown ID、QUEUED lifecycle state を拒否し、legacy Family authority への fallback はない。

## 回帰

以下を standard PostgreSQL runner で再実行し PASS した。

```text
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g05_phase_c_retry_postgres.py

1 passed in 0.62s
pytest_exit_code=0

scripts/test/run_product_postgres_tests.sh \
  tests/product/test_predictive_api_worker_e2e_e3.py::test_predictive_execution_plan_async_worker_results_artifacts_and_lineage

run_exit_code=0
```

C2 の same-Execution retry、stable StageExecution identity、attempt history、legacy write-negative、
および C1 の canonical Predictive Golden Path、typed Result / Artifact、artifact cardinality 4、
provenance を維持した。

## チェックリスト

- [x] actual rerun implementation inspected
- [x] Product-facing rerun uses canonical base authority
- [x] new canonical Execution / `base_execution_id` / `RERUN` semantics
- [x] Predictive scientific conditions preserved
- [x] new StageExecution set and distinct identities
- [x] base is not destructively mutated
- [x] four negative cases PASS
- [x] all four legacy Family write negatives PASS
- [x] C3a PostgreSQL test PASS
- [x] C2 retry regression PASS
- [x] C1 Golden Path regression PASS
- [x] `git diff --check` PASS
- [x] C3a checkpoint commit created

## 範囲外

C3b（Predictive revise）、C4、Phase C final report、`PHASE_C_COMPLETE`、Phase D、Phase Eには進んでいない。
