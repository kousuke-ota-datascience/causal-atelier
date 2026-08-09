# E4-G05 Trial 01 Phase A 実装チェックポイント報告書

- プロジェクト: Ariadne / causal-atelier
- 拡張: ENH-E4 eliminate dual execution
- ゲート: E4-G05
- 試行: 01
- チェックポイント状態: PHASE_A_COMPLETE
- ブランチ: `refactor/ariadne_mvp_e4`
- ベースラインコミット: `0bc9ce5f3ea66f862f088c2246082aedfd0d83e4`
- 開始コミット: `0bc9ce5f3ea66f862f088c2246082aedfd0d83e4`
- チェックポイントコミット: `b8a3f5502f82fcca8cb9634bd8368e3ebc9f0344`
- 報告書コミット: PENDING
- マイグレーションhead: `20260809_product_0010`
- 開始日時: UNKNOWN
- 終了日時: UNKNOWN

これは Phase A のチェックポイント記録であり、E4-G05完了報告書でもゲートの PASS/FAIL/BLOCKED 判定でもない。

## 1. 入力

- Phase A 実装指示書: `docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/10_enhance_instruction/G05/06g01_Ariadne_ENH-E4_G05_PhaseA_実装指示書.md`
- 直前のゲート判定報告書: `NONE`

## 2. 実装範囲

- Exploratory / Predictive の科学的出力に必要な canonical family `ResultType`、`ScientificStatus`、`ArtifactType` を追加した。
- domain の Result type/status validation、ORM の値・状態制約、Product migration `20260809_product_0010` を追加した。
- typed canonical family Result/Artifact persistence のため、real PostgreSQL を使う Phase A round-trip/negative test を追加した。
- チェックポイント test は、canonical `Execution` / `StageExecution` を経由した Result/Artifact ownership、fresh session での repository reload、schema-version payload metadata、diagnostics、warnings、artifact metadata、Result↔Artifact association を検証する。

## 3. 変更ファイル

### 追加

- `tests/product/test_enh_e4_g05_phase_a_postgres.py`

### 変更

- `src/ariadne/product/domain/enums.py` — Phase A の typed family output vocabulary。baseline checkpoint に含まれる。
- `src/ariadne/product/domain/result.py` — family `ResultType` / `ScientificStatus` compatibility。baseline checkpoint に含まれる。
- `src/ariadne/product/persistence/orm_models.py` — typed Result/Artifact constraints。baseline checkpoint に含まれる。
- `product_migrations/versions/20260809_product_0010_enh_e4_g05_family_output_types.py` — Product migration。baseline checkpoint に含まれる。
- `src/ariadne/interfaces/worker/execution_processor.py` — family typed output conversion。baseline checkpoint に含まれる。

### 削除

`NONE`

## 4. 実装詳細

family-specific type は canonical typed `ResultType`、`ScientificStatus`、`ArtifactType` として永続化される。generic `DIAGNOSTICS_RESULT` / `PASS` fallback への圧縮は行わない。

test対象の全 family Result は canonical `STAGE_RESULT` であり、canonical `stage_execution_id` を保持する。test は `summary_json` / `payload_json` 内の schema/version metadata、payload、diagnostics、warnings を fresh repository reload 後も保持することを確認する。Artifact は semantic `artifact_id`、physical `object_key`、canonical Result/StageExecution association、Execution ownership、metadata を保持する。

## 5. 追加・変更した自動テスト

| カバレッジ | 正確なテスト | 証拠 |
|---|---|---|
| family ResultType/ScientificStatus round-trip | `test_g05_phase_a_family_output_types_round_trip` | real PostgreSQL と fresh session による canonical repository reload |
| 不正な family typed value | `test_g05_phase_a_domain_rejects_invalid_family_result_status` | domain enum/type-status の negative test |
| PostgreSQL上の不正typed value | `test_g05_phase_a_postgres_constraints_reject_invalid_typed_values` | Result status matrix と ArtifactType check constraint の negative test |

## 6. マイグレーション

- 追加マイグレーション: `product_migrations/versions/20260809_product_0010_enh_e4_g05_family_output_types.py`
- 変更前head: `20260809_product_0009`
- 変更後head: `20260809_product_0010`
- 破壊的変更: `NONE`
- データマイグレーション: `NONE`

## 7. 既通過ゲートへの影響

G04 canonical Result/Artifact ownership regression は標準 PostgreSQL runner で実行し、PASSした。G02/G03 production contract は checkpoint commit `b8a3f55` で変更していない。G02/G03 の最終 G05 regression は、この Phase A-only checkpoint の対象外である。

## 8. 既知の制約・未解決項目

- Phase B Exploratory read convergence: NOT_RUN。
- Phase C Predictive read/mutation convergence: NOT_RUN。
- Phase D old family lifecycle shutdown: NOT_RUN。
- Phase E cross-family Golden Path、old-write negative、no-fallback negative、final G02/G03/G04 regression: NOT_RUN。
- E4-G05 final completion report、TD closure evidence、READY_FOR_TEST: NOT_RUN。

## 9. スコープ外作業

Phase B/C/D/E、G06 lineage consolidation、E4-G05 final implementation commit、final Gate handoff は `06g01` により明示的に対象外とされた。

## 10. Git証拠

- checkpoint後の `git rev-parse HEAD`: `b8a3f5502f82fcca8cb9634bd8368e3ebc9f0344`
- checkpoint後の `git status --short`: この報告書の作成前は未追跡の `06g01` instruction file のみ。
- checkpoint diff stat: `1 file changed, 119 insertions(+)`。
- checkpoint前の `git diff --check`: exit `0`。

## 11. テスト担当への引継ぎ

- テスト対象implementation commit: `b8a3f5502f82fcca8cb9634bd8368e3ebc9f0344`
- アクティブゲート: `E4-G05 Trial 01 Phase A`
- implementation report path: このファイル
- Coding Agent test execution: `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g05_phase_a_postgres.py tests/product/test_enh_e4_g04_result_artifact_postgres.py tests/product/test_postgres_contract.py` → `10 passed`、exit `0`、migration head `20260809_product_0010`。
- 独立テストの準備完了: Phase A checkpoint scope に限り `YES`。

## 12. 設計ブロック

- 矛盾: `NONE`
- 観測事実: family output type には canonical Product Result/Artifact constraint の minimal typed extension が必要だった。
- 影響: `20260809_product_0010` と canonical repository round-trip coverage により解消した。
- 最小選択肢: legacy table write を行わない enum/domain/ORM/migration alignment。
- 必要な判断: `NONE`

## 13. 補足実装証拠

- 初回 PostgreSQL run は test setupの順序不備を検出した。新しい StageExecution row を flushする前に Result persistence が flushされ、`fk_product_result_stage_execution` failure が発生した。testは StageExecution を先に flushするよう修正し、schema / migration の変更は不要だった。
- standard runner の migration output は `20260809_product_0010 (head)` を確認した。
- standard runner は 10 test（G05 Phase A 3件、G04 PostgreSQL ownership 3件、PostgreSQL contract 4件）を収集し、全件PASSした。
