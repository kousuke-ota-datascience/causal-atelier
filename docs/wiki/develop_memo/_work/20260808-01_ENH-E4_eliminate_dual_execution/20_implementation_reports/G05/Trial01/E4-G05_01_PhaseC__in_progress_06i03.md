# E4-G05 Trial 01 Phase C In-Progress Status Report 06i03

- Gate: `E4-G05`
- Trial: `01`
- Phase: `C` / internal work package `C1`
- Status: `IN_PROGRESS`

## 1. 事実

- C1 は canonical Predictive Golden Path に限定して継続中である。
- `FITTED_PREPROCESSOR` の欠落は解消した。原因は、prepare stage が ArtifactDraft のみを返し、従来の canonical descriptor 変換が ResultDraft のない stage の Artifact を破棄していたことだった。
- canonical Artifact の schema version、output ownership、StageExecution association を保持する変更を追加した。
- LocalArtifactStore は media type を自動推定せず、デフォルトで `application/octet-stream` を返す実装である。`.json` 拡張子への変更だけでは不十分だったため、family Artifact を保存する際に `application/json` を明示して渡す修正を追加した。

## 2. 最新の PostgreSQL E2E 結果

実行コマンド:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_predictive_api_worker_e2e_e3.py::test_predictive_execution_plan_async_worker_results_artifacts_and_lineage
```

確認済み:

- canonical Predictive Execution と StageExecution が作成される。
- canonical worker は `SUCCEEDED` に到達する。
- typed Predictive Result が作成される。
- Artifact type は `PARTITION_INDEX`、`FITTED_PREPROCESSOR`、`FITTED_MODEL`、`PREDICTION` の4種を満たす。
- Artifact schema version と `application/json` media type の assertion を通過した。

未達:

- lineage endpoint は空配列を返し、既存 E2E の `ResearchContextVersion` input lineage assertion で失敗した。

## 3. 原因と追加済み修正

原因は canonical Predictive submission が `ExecutionService.create_family_execution()` に委譲した後、旧 Family submit が持っていた input lineage edge を生成していなかったことである。

`PredictiveWorkflowService._canonical_submission()` に、canonical Execution ID を target とする以下の `USED_INPUT` lineage edge を保存する修正を追加した。

- ResearchContextVersion
- DatasetVersion
- AnalysisSpecification
- ExecutionPlan

この修正は G06 の lineage authority 統合ではなく、現行 endpoint が canonical owned Execution を前提として読めるようにする Phase C C1 の最小互換修正である。

## 4. 次の作業

1. 上記 lineage 修正を含めて同じ standard PostgreSQL E2E を再実行する。
2. PASS 後、`git diff --check` を確認する。
3. C1 production source/test のみを checkpoint commit する。

retry、rerun、revise、full old-table negative、Phase C complete/report には進んでいない。
