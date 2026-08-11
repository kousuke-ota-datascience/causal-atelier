# E4-G05 Trial 01 Phase C — 06i13 実行状況報告

- Gate: E4-G05
- Trial: 01
- Phase: C
- 実装指示 ID: 06i13
- 状態: PHASE_C_COMPLETE
- ブランチ: `refactor/ariadne_mvp_e4`
- 実装チェックポイント: `9c58bffd5c5fb6be8565a1256222e678fb86c52a`
- Phase C 報告書初回コミット: `2ee00aa30572a1f7771488eb3953dcd5d0e7b65a`
- 報告書メタデータ補正コミット: `cd0d563cd7839cef2fe8307cc004e291e19e2ef6`

## 指示実行結果

### 結論

Phase C の C4 最終監査を完了し、Predictive の Product-facing flow は canonical Execution / StageExecution / Result / Artifact を authority として使用することを確認した。Phase C の完了条件は満たした。Phase D には進んでいない。

### 事実

- `StageExecution.prepare_retry()` を追加し、FAILED stage を同一 ID、attempt history、binding を保持したまま PENDING へ戻すようにした。これにより canonical retry 後の worker は READY → RUNNING → 新しい attempt を正常に実行する。
- C4 authority audit test を追加し、canonical Predictive ID の get/list、stage、result、artifact、lineage、prefill、cancel を検証した。unknown canonical ID は `EntityNotFound` となり、旧 Family table の fallback は成功しない。
- submit、read、cancel、retry、rerun、revise、canonical worker について、`FamilyExecutionOrm`、`FamilyStageExecutionOrm`、`FamilyResultOrm`、`FamilyArtifactOrm` の新規行が増えないことを C1〜C4 の PostgreSQL tests で確認した。
- canonical worker Golden Path は typed Result / Artifact と provenance を維持して成功する。対象 artifact の cardinality は PARTITION_INDEX、FITTED_PREPROCESSOR、FITTED_MODEL、PREDICTION が各 1 件である。
- retry は同一 Execution と同一 StageExecution を使用し、attempt history を保持する。rerun / revise は新しい canonical Execution と `base_execution_id` を使用する。same-condition revise は canonical comparison の結果に従い RERUN、condition 変更ありは明示的な理由付き REVISED となる。

### 検証結果

- 標準 PostgreSQL runner による C1/C2/C3a/C3b/C4、Phase A/B、G02/G04 bundle: 18 passed、exit 0。
  - Evidence: `test-results/postgres/run-20260809T092414Z.txt`
- 標準 PostgreSQL runner による G03 regression: 6 passed、exit 0。
  - Evidence: `test-results/postgres/run-20260809T092351Z.txt`
- API/worker regression: `.venv/bin/pytest -q tests/product/test_predictive_api_worker_e2e_e3.py` は 3 passed、exit 0。
- `git diff --check`: PASS。
- Product migration head: `20260809_product_0010` を PostgreSQL runner 内で確認した。

### 判断

最初の G03 を含む併走 bundle の 3 件の失敗は、先行 fixture がデータを残すことと G03 test が空の global queue を前提とすることの組合せによる fixture isolation の問題だった。G03 を標準 runner により独立 reset で再実行すると 6 passed であり、Phase C の Product semantic defect を示す証拠はない。

### 残作業

Phase D では全 family の legacy claim/process 到達性を停止し、global failure fallback を監査する。Phase E では G05 全体の Golden Path、transition debt、completion report、READY_FOR_TEST を扱う。本指示の範囲外であり、今回実装していない。

## 参照報告書

`docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G05/Trial01/E4-G05_01_PhaseC_implementation_checkpoint_report.md`

