# E4-G05 Trial 01 Phase C In-Progress Status Report 06i02

- 記録時刻: `2026-08-09T08:18:44Z`
- Branch: `refactor/ariadne_mvp_e4`
- Current documentation checkpoint: `2ed9ea4663587b8747a20328dae5e9023777c854`
- Phase state: `IN_PROGRESS`
- Trial: `01`

## 1. 現在の working tree

### Phase C 実装差分（未コミット）

- `src/ariadne/product/application/predictive_workflow_service.py`
  - canonical `ExecutionService` を利用する Predictive submit/read/cancel/retry/rerun/revise/prefill の収束を実装中。
  - canonical `ExecutionOrm`、`StageExecutionOrm`、`ResultOrm`、`ArtifactOrm` の projection を追加中。
- `src/ariadne/interfaces/web_api/routers/predictive_workflow.py`
  - revise request に明示的な `change_reason` を追加中。
- `src/ariadne/interfaces/worker/execution_processor.py`
  - canonical Predictive Artifact の output ownership、StageExecution association、schema version metadata を追加中。
  - prepare stage のように Result を返さない stage の ArtifactDraft を後続 canonical Result descriptor へ保持する修正を追加中。
  - Artifact object の拡張子を `.json` に変更中。
- `tests/product/test_predictive_api_worker_e2e_e3.py`
  - obsolete な Family worker claim/process 前提を canonical claim + `ExecutionProcessor` に置換中。

### 保持している既存変更

- 既存進捗報告書は user 作業として `E4-G05_01_PhaseC__in_progress_06i01.md` へ rename staged されている。変更・巻き戻しを行っていない。
- `06i02_.md` instruction artifact は untracked の user 作業であり、Phase C production commit へ混入させない。

## 2. 実装・検証の事実

1. canonical Predictive submit は canonical Execution/StageExecution を生成し、worker で terminal `SUCCEEDED` に到達した。
2. 最初の canonical E2E 失敗は `FITTED_PREPROCESSOR` の欠落だった。
   - 原因: prepare stage は ArtifactDraft を返すが ResultDraft を返さない。従来の `_family_descriptors()` は ResultDraft がない stage の ArtifactDraft を descriptor に渡していなかった。
   - 修正: pending artifact として保持し、後続 Result descriptor へ引き継ぐ実装を追加した。
3. 上記修正後、Artifact type の4種（`PARTITION_INDEX`、`FITTED_PREPROCESSOR`、`FITTED_MODEL`、`PREDICTION`）は E2E assertion を通過した。
4. 次の失敗は Artifact media type である。
   - expected: `application/json`
   - actual: `application/octet-stream`
   - 原因: canonical artifact object の一時出力が `.bin` だったため LocalArtifactStore の media type 判定が binary になった。
   - 修正済み（未検証）: output filename を `.json` に変更した。

## 3. 最終実行済みコマンドと結果

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_predictive_api_worker_e2e_e3.py::test_predictive_execution_plan_async_worker_results_artifacts_and_lineage
```

- standard PostgreSQL runner を使用した。
- migration head は `20260809_product_0010`。
- 最新の失敗は Artifact media type assertion のみであり、exit code は `1`。
- raw evidence: `test-results/postgres/run-20260809T081439Z.txt` および同 metadata file。

## 4. 未達作業

- `.json` 出力修正後の canonical Predictive E2E を再実行し、PASSさせる。
- retry: same Execution ID、stable StageExecution ID、attempt history preservation、legacy row non-write を実装・検証する。
- rerun/revise: canonical base relation、new StageExecution set、explicit `change_reason`、cross-project/cross-family negative を実装・検証する。
- submit/read/cancel/retry/rerun/revise/prefill の FamilyExecution/FamilyStageExecution/FamilyResult/FamilyArtifact row-count negative を実 PostgreSQL testへ追加する。
- Phase C 専用 PostgreSQL test、Phase A/B/G02/G03/G04 regression、checkpoint commit、Phase C checkpoint report、report metadata correction commitを完了する。

## 5. 判定

`DESIGN_BLOCKED` ではない。

根拠: 現在の未達は canonical descriptor の artifact transfer と content media type の実装不備、および残る lifecycle adapter/test coverageである。いずれも 06i01 が許可する Phase C scope 内の最小修正で解消可能である。Phase D/Eには未着手である。
