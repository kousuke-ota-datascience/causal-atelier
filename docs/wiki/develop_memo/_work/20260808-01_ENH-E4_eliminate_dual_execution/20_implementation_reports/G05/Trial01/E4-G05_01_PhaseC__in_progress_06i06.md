# E4-G05 Trial 01 Phase C In-Progress Status Report 06i06

- Gate / Trial / Phase: `E4-G05` / `01` / `C`
- Work package: `C1 — canonical Predictive Golden Path`
- Status: `IN_PROGRESS`

## 1. 最新の standard PostgreSQL E2E 結果

実行対象:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_predictive_api_worker_e2e_e3.py::test_predictive_execution_plan_async_worker_results_artifacts_and_lineage
```

canonical Predictive Execution、StageExecution、typed Results、Artifact ownership/media type/schema version、input/output lineage の確認を進めている。

今回の failure は次の canonical derivation edge だった。

```text
PREDICTION --DERIVED_FROM--> FITTED_MODEL
```

## 2. 原因

canonical worker は同じ `ArtifactType` の Artifact を複数保存し得る。以前の実装は ArtifactType ごとに辞書で一件だけを選び、`DERIVED_FROM` edge を保存していた。

一方 E2E の API projection は created-at/order により別の同型 Artifact ID を返し得る。そのため、response で選ばれた `PREDICTION` / `FITTED_MODEL` の組に edge がない場合があった。

## 3. 追加済み修正（未検証）

Artifact derivation lineage persistence を以下へ変更した。

- `FITTED_PREPROCESSOR` の全 Artifact × `PARTITION_INDEX` の全 Artifact
- `FITTED_MODEL` の全 Artifact × `FITTED_PREPROCESSOR` の全 Artifact
- `PREDICTION` の全 Artifact × `FITTED_MODEL` の全 Artifact

各組に canonical `DERIVED_FROM` edge を保存する。これにより API projection がどの同型 Artifact ID を返しても、C1 E2E contract の lineage edge を満たす。

## 4. 残作業

1. 同一 standard PostgreSQL E2E を再実行する。
2. PASS後、`git diff --check` を確認する。
3. C1 production source/test のみを checkpoint commit する。

retry、rerun、revise、full old Family row-count negative、Phase C final checkpoint/report、Phase D/E は対象外であり未着手である。
