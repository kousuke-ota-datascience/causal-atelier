# E4-G05 Trial 01 Phase C In-Progress Status Report 06i12

- Gate / Trial / Phase: `E4-G05` / `01` / `C`
- Work package: `C3b — Predictive canonical revise`
- Status: `PHASE_C_C3B_COMPLETE`
- C3b checkpoint SHA: `7870329192986bcd070935bf48fe814dda444a77`

## 実装結果

Product-facing `PredictiveWorkflowService.revise()` は canonical base Execution を取得し、正規の
fixed Predictive AnalysisSpecification / ExecutionPlan と explicit `change_reason` を用いて
canonical `ExecutionService.create_family_execution()` に委譲する。

実装中に、same-condition revise でも `change_reason` の有無だけで Execution ORM の
`revision_kind` が `REVISED` になる不整合を検出した。`_build_revision_context()` は既に
正しく condition comparison を行っていたため、Execution の `revision_kind` / `change_reason` を
その canonical revision context から設定するよう最小修正した。

これにより次が成立する。

- 実際の scientific condition 変更あり: `REVISED`、caller supplied non-empty `change_reason`。
- 条件差分なし: `RERUN`、`change_reason=None`。
- base Execution、base StageExecution、base Result / Artifact は revise により変更されない。

## C3b PostgreSQL 検証

対象テスト: `tests/product/test_enh_e4_g05_phase_c_revise_postgres.py`

```text
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g05_phase_c_revise_postgres.py

1 passed in 0.88s
pytest_exit_code=0
```

real PostgreSQL で、正規 Workspace lifecycle により base Specification を revise し、
`logistic_regression.v1` の `l2` を `0.25` へ変更した新 fixed Specification と Plan を作成した。
明示理由 `正則化強度を変更して予測安定性を検証するため` を渡して revise し、以下を確認した。

- new canonical Execution、`base_execution_id`、`analysis_family=PREDICTIVE`、`revision_kind=REVISED`。
- supplied `change_reason`、changed model parameter、revised Specification / Plan が canonical snapshot に保存される。
- dataset と seed は保持され、new persistent StageExecution set は base と異なる ID を持ち revised plan と整合する。
- base の status、retry_count、StageExecution / Result / Artifact ownership は不変。
- prefill は revised canonical Execution から Specification、Plan、seed、revision context を投影する。
- same-condition revise は canonical comparison により `RERUN` となる。
- missing / empty / whitespace reason、cross-project、non-PREDICTIVE、unknown ID、queued lifecycle、
  spec-plan mismatch、spec seed と異なる seed を拒否する。
- `FamilyExecution`、`FamilyStageExecution`、`FamilyResult`、`FamilyArtifact` に新規 write はない。

## 回帰

次の standard PostgreSQL verification を実行して PASS した。

```text
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py

1 passed in 0.69s
pytest_exit_code=0

scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g05_phase_c_retry_postgres.py

run_exit_code=0

scripts/test/run_product_postgres_tests.sh \
  tests/product/test_predictive_api_worker_e2e_e3.py::test_predictive_execution_plan_async_worker_results_artifacts_and_lineage

1 passed in 1.68s
pytest_exit_code=0
```

## チェックリスト

- [x] actual canonical revise contract inspected
- [x] canonical base authority と explicit change_reason request path
- [x] changed condition / unchanged condition の canonical comparison
- [x] changed revise は `REVISED`、same-condition revise は `RERUN`
- [x] new canonical Execution / base relation / new StageExecution identities
- [x] base non-destructive
- [x] required negative cases
- [x] all four legacy Family write negatives
- [x] C3b PostgreSQL test
- [x] C3a / C2 / C1 regressions
- [x] `git diff --check`
- [x] C3b checkpoint commit

## 範囲外

C4、Phase C final audit / report、`PHASE_C_COMPLETE`、Phase D、Phase Eには進んでいない。
