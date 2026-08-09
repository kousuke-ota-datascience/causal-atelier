# E4-G05 Trial 01 Phase C In-Progress Status Report 06i07

- Gate / Trial / Phase: `E4-G05` / `01` / `C`
- Work package: `C1 — canonical Predictive Golden Path`
- Status: `IN_PROGRESS`

## 1. 06i07 の semantic review 結果

06i06 時点の ArtifactType ごとの Cartesian-product `DERIVED_FROM` edge は、actual provenance を表さないため採用しない。

原因は lineage edge そのものではなく、canonical descriptor 変換が同一 stage の Artifact list をその stage の全 Result descriptor へ複製していたことである。この複製により同型 Artifact が複数保存され、ArtifactType だけでは正しい lineage source/target を一意に選べない状態になっていた。

## 2. 追加済み修正（未検証）

### Artifact cardinality

- stage が ResultDraft を複数返す場合、stage Artifact は最初の owning Result descriptor のみに関連付ける。
- ResultDraft を返さない prepare stage の Artifact は pending artifact として保持し、後続の最初の Result descriptor へ一度だけ引き継ぐ。
- これにより C1 Golden Path では、`PARTITION_INDEX`、`FITTED_PREPROCESSOR`、`FITTED_MODEL`、`PREDICTION` が各1件となる想定である。

### Provenance

- `DERIVED_FROM` は一意に保存された actual Artifact ID 間だけに保存する。
- chain は以下である。

```text
PARTITION_INDEX
  <- FITTED_PREPROCESSOR
  <- FITTED_MODEL
  <- PREDICTION
```

- `PREDICTION --EVIDENCE_FOR--> EVALUATION_RESULT` と、Prediction の `GENERATED` source を canonical `EVALUATION_RESULT` とする修正は維持している。

### Test hardening

既存 Predictive E2E に次を追加した。

```text
len(artifacts) == 4
len(artifacts_by_type) == 4
```

したがって、dict comprehension による duplicate collapse で cardinality defect を隠さない。

## 3. 未検証事項

この修正後の standard PostgreSQL E2E は未実行である。

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_predictive_api_worker_e2e_e3.py::test_predictive_execution_plan_async_worker_results_artifacts_and_lineage
```

PASS後に `git diff --check`、C1 production source/test の path-specific checkpoint commit を実施する必要がある。

## 4. Scope boundary

retry、rerun、revise、full old Family row-count negative、Phase C final checkpoint/report、Phase D/E は C1 の対象外であり未着手である。
