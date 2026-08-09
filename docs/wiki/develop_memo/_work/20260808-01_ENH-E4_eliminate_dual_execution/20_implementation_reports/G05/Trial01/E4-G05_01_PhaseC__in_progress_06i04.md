# E4-G05 Trial 01 Phase C In-Progress Status Report 06i04

- Gate / Trial / Phase: `E4-G05` / `01` / `C`
- Internal work package: `C1 — canonical Predictive Golden Path`
- Status: `IN_PROGRESS`

## 1. 最新の確認結果

standard PostgreSQL runner で canonical Predictive E2E を再実行した。

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_predictive_api_worker_e2e_e3.py::test_predictive_execution_plan_async_worker_results_artifacts_and_lineage
```

以下は PASS した。

- canonical Predictive Execution / StageExecution の作成
- canonical worker による `SUCCEEDED` 到達
- typed Predictive Result の永続化
- `PARTITION_INDEX`、`FITTED_PREPROCESSOR`、`FITTED_MODEL`、`PREDICTION` の Artifact type
- Artifact schema version
- Artifact media type `application/json`
- canonical input lineage: ResearchContextVersion、DatasetVersion、AnalysisSpecification、ExecutionPlan

## 2. 新たに検出した C1 production defect

canonical worker は Result / Artifact を `product_result` / `product_artifact` に保存していたが、対応する lineage edge を保存していなかった。このため Predictive lineage endpoint が input edge だけを返し、E2E の以下の contract を満たさなかった。

- `Execution --GENERATED--> Result`
- `Result --GENERATED--> Artifact`（Result-owned Artifact）
- `Execution --GENERATED--> Artifact`（FITTED_PREPROCESSOR）
- Artifact chain の `DERIVED_FROM`
- evaluation Result に対する prediction Artifact の `EVIDENCE_FOR`

## 3. 追加済みの未検証修正

`ExecutionProcessor` の canonical Result/Artifact 永続化トランザクション内で、以下を追加した。

- 全 canonical Result の `Execution --GENERATED--> Result` edge
- canonical Artifact の `GENERATED` edge
- `PARTITION_INDEX → FITTED_PREPROCESSOR → FITTED_MODEL → PREDICTION` の Artifact derivation edge

修正は同じ canonical output transaction に含め、old Family Result/Artifact を lineage authority として使用しない。

## 4. 残作業

1. `PREDICTION --EVIDENCE_FOR--> EVALUATION_RESULT` edge が E2E contract どおり保存されるよう補完する。
2. 同一 PostgreSQL E2E を再実行し PASS させる。
3. `git diff --check` を PASS させる。
4. C1 production source/test のみを checkpoint commit する。

retry、rerun、revise、full old Family row-count negative、Phase C final checkpoint/report、Phase D/E は C1 scope 外であり未着手である。
