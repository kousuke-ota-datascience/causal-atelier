# E4-G05 Trial 01 Phase C In-Progress Status Report

- 記録時刻: `2026-08-09T08:10:31Z`
- ブランチ: `refactor/ariadne_mvp_e4`
- 現在の HEAD: `e6c410de6ec4d928c6c3ec8b9647d6ff39a92008`
- Phase B implementation checkpoint: `b77e3febd9c6c48b553bc59cd8e5be29f2aba998`
- 状態: `IN_PROGRESS`

## 1. 事実

- Phase C 指示書 `06i01_Ariadne_ENH-E4_G05_PhaseC_実装指示書.md` を全読し、Phase C のみを対象としている。
- Phase B checkpoint は現在の HEAD の祖先である。
- Phase C 実装は未コミットである。Phase B report の手動修正、Phase C 指示書は既存の working-tree 変更として保持し、Phase C production commit へ混入させない。
- `PredictiveWorkflowService` は既に `execution_service` を受け取る constructor であり、DI provider もこれを注入している。Phase C では、この dependency を submit だけでなく Product-facing read/mutation にも実際に使用する実装へ拡張中である。

## 2. 実装済み（未コミット）

- Predictive canonical mode の `list_executions`、`get_execution`、`get_stages`、`list_results`、`list_artifacts`、`list_lineage` に canonical Product Execution/StageExecution/Result/Artifact を読む分岐を追加した。
- Predictive `cancel` と `retry` を canonical `ExecutionService` へ delegate する分岐を追加した。
- `rerun` / `revise` / `prefill` の canonical snapshot projection を追加中である。
- revise API request に `change_reason` を追加し、サービス側で理由を捏造しない方向へ変更した。
- canonical worker の Artifact に Execution output ownership と StageExecution association を設定し、artifact metadata に schema version を保持する変更を追加した。
- 旧 Family worker を直接 claim/process する既存 Predictive E2E を、canonical claim と `ExecutionProcessor` による処理へ置換し始めた。

## 3. 検証事実

- standard PostgreSQL runner を用いて canonical Predictive E2E node を複数回実行した。
- 初回は API route が submit request に存在しない `change_reason` を参照する実装不備で失敗した。route を修正した。
- 次に canonical worker の lease owner が claim 時の `worker_id` と一致しない test helper 不備で失敗した。helper の owner を一致させた。
- 次に canonical Artifact に `EXECUTION_OUTPUT` ownership が設定されていない production defect を検出した。Artifact scope を設定するよう修正した。
- 最新実行では canonical Predictive Execution、StageExecution、typed Result の生成と terminal `SUCCEEDED` まで到達した。
- ただし既存 E3 Predictive E2E は Artifact response に `FITTED_PREPROCESSOR` が含まれないため失敗している。期待値は `PARTITION_INDEX`、`FITTED_PREPROCESSOR`、`FITTED_MODEL`、`PREDICTION` の4種であり、actual は `FITTED_PREPROCESSOR` を欠く。

## 4. 未達と次の作業

- `FITTED_PREPROCESSOR` 欠落の原因を canonical family descriptor → Artifact persistence の対応で特定・修正する。
- Predictive retry の canonical StageExecution identity / attempt-history contract、rerun/revise の base relation と change reason、全 Product-facing operation の old Family row-count negative を追加検証する。
- 実 PostgreSQLの Phase C 専用 test、Phase A/B/G02/G03/G04 regression、checkpoint commit、Phase C report と metadata correction commit は未実施である。

## 5. 判定

`DESIGN_BLOCKED` ではない。

根拠は、現時点の失敗はいずれも adapter、test helper、canonical Artifact ownership/mapping の実装不備であり、06i01 が許可する Phase C の最小修正で解消可能だからである。Phase D/E には進んでいない。
