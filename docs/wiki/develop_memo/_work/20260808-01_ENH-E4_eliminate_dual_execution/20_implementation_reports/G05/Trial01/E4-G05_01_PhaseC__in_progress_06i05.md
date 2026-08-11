# E4-G05 Trial 01 Phase C In-Progress Status Report 06i05

- Gate / Trial / Phase: `E4-G05` / `01` / `C`
- Work package: `C1 — canonical Predictive Golden Path`
- Status: `IN_PROGRESS`

## 最新の検証事実

standard PostgreSQL runner で canonical Predictive E2E を再実行した。

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_predictive_api_worker_e2e_e3.py::test_predictive_execution_plan_async_worker_results_artifacts_and_lineage
```

canonical Execution、StageExecution、typed Result、4種の Artifact、input lineage、Result/Artifact generated lineage、Artifact derivation lineage までは確認できている。

最新 failure は以下である。

```text
Result(EVALUATION_RESULT) --GENERATED--> Artifact(PREDICTION)
```

が存在しない。

## 原因

canonical descriptor 変換では stage の複数 Result が同一 Artifact list を共有する。Artifact persistence は descriptor traversal 中の Result ID をそのまま使うため、`PREDICTION` Artifact が `ERROR_ANALYSIS_RESULT` 側へ関連付く場合があった。

既存 Predictive E2E contract は Prediction を evaluation evidence として扱うため、canonical output lineage の source Result は `EVALUATION_RESULT` でなければならない。

## 追加済み修正（未検証）

worker の canonical lineage persistence に `result_by_type` projection を追加した。

- `PREDICTION` Artifact の `GENERATED` edge は、canonical `EVALUATION_RESULT` の Result ID を source とする。
- `PREDICTION --EVIDENCE_FOR--> EVALUATION_RESULT` edge は既に追加済みである。

これにより C1 が要求する以下の lineage contract を満たす予定である。

```text
Execution --GENERATED--> Result
Result/Execution --GENERATED--> Artifact
PARTITION_INDEX -> FITTED_PREPROCESSOR -> FITTED_MODEL -> PREDICTION
PREDICTION --EVIDENCE_FOR--> EVALUATION_RESULT
```

## 残作業

1. 同一 standard PostgreSQL E2E を再実行し PASS を確認する。
2. `git diff --check` を PASS させる。
3. C1 production source/test のみを checkpoint commit する。

retry、rerun、revise、全 old Family row-count negative、Phase C final report、Phase D/E は対象外であり未着手である。
