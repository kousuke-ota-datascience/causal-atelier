# 背景

`06c_Ariadne_ENH-E4_G05_実装指示書_中断後再開.md` の Phase A 完遂優先指示に従い、E4-G05 Trial 01 を現在の未コミット working tree から継続した。以下は再開時点の actual diff と、その後に行った Phase A の追加実装を含む状況報告である。

## Working tree classification

### VALID_AND_KEEP

- `src/ariadne/interfaces/web_api/dependencies.py`: Exploratory / Predictive service への canonical `ExecutionService` injection。
- `src/ariadne/interfaces/web_api/routers/exploration.py`: canonical `Execution` の Exploratory execution response projection。
- `src/ariadne/interfaces/worker/runner.py`: canonical `uow.executions.claim_next()` を唯一の worker claim entrypoint とする変更。
- `src/ariadne/interfaces/worker/execution_processor.py`: Causal / Exploratory / Predictive runner dispatch の追加。
- `src/ariadne/product/application/execution_service.py`: non-causal family submission と canonical cancellation 時の StageExecution cancellation。
- `src/ariadne/product/application/exploratory_service.py`: Exploratory canonical submit と canonical execution read の一部。
- `src/ariadne/product/application/predictive_workflow_service.py`: Predictive canonical submission の一部。
- `tests/product/test_enh_e4_g05_submission_convergence.py`: Exploratory submit が canonical Execution / StageExecution を作り、`FamilyExecutionOrm` を作らないことの coverage。

### NEEDS_COMPLETION

- `src/ariadne/product/domain/enums.py`: family-specific Result / ScientificStatus / ArtifactType を追加済みだが、Phase A の開始点にすぎない。
- `src/ariadne/product/domain/result.py`: 追加 ResultType と ScientificStatus の domain validation を追加済み。
- `src/ariadne/product/persistence/orm_models.py`: Result / Artifact value constraint の追加を開始済み。ただし result status matrix は追加型をまだ表現していない。
- `product_migrations/versions/20260809_product_0010_enh_e4_g05_family_output_types.py`: `20260809_product_0009` の direct child として作成済み。ただし ORM status matrix と完全一致するかを verification していない。downgrade も implementation contract に照らして要確認である。
- canonical worker の family output は現状 `DIAGNOSTICS_RESULT` / `PASS` envelope を使用しており、追加した typed Result / Artifact semantics へ未接続である。
- Exploratory / Predictive read projection、Predictive mutation delegation、old family write authority shutdown、Phase E tests は未実装である。

### NEEDS_CORRECTION

- `src/ariadne/interfaces/worker/execution_processor.py` の `_family_descriptors()` は family result type / status を typed canonical `ResultType` / `ScientificStatus` に変換せず、generic envelope に圧縮している。Phase A の payload preservation 要件に不適合であり、typed conversion と canonical StageResult ownershipへ置換が必要である。
- `src/ariadne/product/persistence/orm_models.py` の `ck_product_result_status_matrix` は追加 ResultType を許容するよう未更新である。SQLite metadata と PostgreSQL migration の schema contract を一致させる必要がある。
- `20260809_product_0010` の migration は check constraint 更新を実装したが、domain/ORM/migration の status matrix を単一の型集合として同期させる test がない。

### UNRELATED_DO_NOT_TOUCH

- `deploy/.nfs000000000076202f00000088` の削除。
- `docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/00_ENH-E4_Current_Architecture_Control_Sheet.md` の編集。
- G05 instruction directory 内の既存 instruction files。これらは G05 Trial 01 の入力・経過記録であり、implementation source ではない。

## Phase A inventory facts

既存 family runner は、canonical schema の従前 enum/check constraint には存在しない以下の output semantics を生成する。

- Exploratory Result: `DATA_PROFILE_RESULT`、`DISTRIBUTION_RESULT`、`ASSOCIATION_RESULT`、`GROUP_SUMMARY_RESULT`、`CHART_RESULT`。
- Predictive Result: `SPLIT_RESULT`、`TRAINING_RESULT`、`EVALUATION_RESULT`、`ERROR_ANALYSIS_RESULT`、`PREDICTIVE_EXPLANATION_RESULT`、`MODEL_CARD_RESULT`。
- Predictive ScientificStatus: `TRAINED`、`TRAINED_WITH_WARNINGS`、`EVALUATED`、`INSUFFICIENT_TEST_SAMPLE`、`NOT_APPLICABLE`。
- family ArtifactType: `CHART_SPECIFICATION`、`PARTITION_INDEX`、`FITTED_PREPROCESSOR`、`FITTED_MODEL`、`PREDICTION`、`PREDICTIVE_EXPLANATION`、`MODEL_CARD`。

これらを generic `DIAGNOSTICS_RESULT` / `PASS` に圧縮すると、typed result/status semantics が canonical metadata から失われる。G05 06 が許容する minimal typed extension と Product migration により解消可能であり、`DESIGN_BLOCKED` の根拠ではない。

## 検証事実

- `git diff --check` は、直近確認時点で exit `0`。
- Phase A enum 追加前に `compileall` は exit `0`。
- `tests/product/test_enh_e4_g05_submission_convergence.py` は `1 passed`。
- `tests/product/test_enh_e4_g03_generic_executor_boundary.py` と `tests/product/test_enh_e4_g04_result_artifact_contract.py` は合計 `12 passed`。
- Phase A enum / validation / ORM / migration 追加後の compile、unit test、repository round-trip test、standard PostgreSQL runner は未実行。

## 継続判断

Trial 01 は未完了である。次の実装順序は変更しない。

1. Phase A を閉じる。domain validation、serialization/deserialization、ORM status matrix、migration、canonical Result/Artifact writer、repository/PostgreSQL round-trip test を整合させる。
2. generic envelope を family typed canonical Result / Artifact persistence に置換する。
3. その後に限り Phase B/C の read projection と lifecycle delegation、Phase D の旧 authority shutdown、Phase E の real PostgreSQL verification へ進む。
4. 全 completion condition が `DONE` になるまで fixed commit、completion report、ledger、`READY_FOR_TEST` は作成しない。

# 指示

```
06d に記録された NEEDS_COMPLETION / NEEDS_CORRECTION を全て閉じ、Phase A→B→C→D→Eを継続し、READY_FOR_TESTまで停止せず完遂せよ
```