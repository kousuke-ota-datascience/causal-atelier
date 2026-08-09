# E4-G05 Trial 01 Phase C In-Progress Status Report 06i10

- Gate / Trial / Phase: `E4-G05` / `01` / `C`
- Work package: `C2 — Predictive canonical retry`
- Status: `PHASE_C_C2_COMPLETE`
- C2 checkpoint SHA: `3cea6711803904e0009fc55a013c2e8003b45f13`

## 実装結果

Product-facing `PredictiveWorkflowService.retry()` の canonical 分岐は、
`ExecutionService.retry_execution()` に委譲する。canonical `Execution.increment_retry()` は
FAILED Execution を同一 ID の QUEUED Execution へ遷移させ、`retry_count` を加算する。
既存の `StageExecution`、`StageAttempt`、`Result`、`Artifact` を削除・再作成しない。

retry 後、canonical claim authority が同一 Execution を claim し、G03 の
`StageExecution.start_attempt()` により FAILED StageExecution に attempt 2 を追記できる。
したがって StageExecution ID は不変であり、attempt history は `[1, 2]` として保存される。
この lifecycle は family service に複製していない。

## C2 PostgreSQL 検証

対象テスト: `tests/product/test_enh_e4_g05_phase_c_retry_postgres.py`

標準 runner により real PostgreSQL で PASS した。

```text
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g05_phase_c_retry_postgres.py

1 passed in 0.61s
pytest_exit_code=0
```

検証した事実は次のとおり。

- Execution ID は retry 前後で同一。
- StageExecution ID set は不変。
- `retry_count` は canonical rule に従って増加。
- 初回失敗 attempt を保持し、再 claim 後の attempt は番号 2 として追記。
- `PREDICTIVE` family、analysis specification、execution plan、dataset、seed、family snapshot を保持。
- canonical Result / Artifact の execution / result ownership を保持。
- legacy sentinel を用い、`FamilyExecution`、`FamilyStageExecution`、`FamilyResult`、`FamilyArtifact` の行数が retry 前後で不変であることを確認。
- cross-project、non-PREDICTIVE、retry-ineligible、unknown execution ID を拒否し、legacy Family authority への fallback がないことを確認。

## C1 回帰

以下も標準 runner で再実行し PASS した。

```text
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_predictive_api_worker_e2e_e3.py::test_predictive_execution_plan_async_worker_results_artifacts_and_lineage

1 passed in 1.83s
pytest_exit_code=0
```

この回帰で canonical Predictive Execution / StageExecution、typed Result / Artifact、
artifact cardinality 4、`PARTITION_INDEX`・`FITTED_PREPROCESSOR`・`FITTED_MODEL`・`PREDICTION`、
および provenance chain が維持されることを確認した。

## チェックリスト

- [x] actual G03 retry / attempt contract identified
- [x] Predictive retry delegates canonical lifecycle
- [x] canonical retry permits the G03 next attempt on the existing StageExecution
- [x] Execution identity / StageExecution identity / attempt history / numbering preserved
- [x] Predictive immutable snapshot preserved
- [x] four required negative cases PASS
- [x] Family write / destructive reset negative PASS
- [x] C2 PostgreSQL test PASS
- [x] C1 Golden Path regression PASS
- [x] `git diff --check` PASS
- [x] C2 checkpoint commit created

## 範囲外

C3（rerun / revise）、C4、Phase C final report、Phase D、Phase Eには進んでいない。
