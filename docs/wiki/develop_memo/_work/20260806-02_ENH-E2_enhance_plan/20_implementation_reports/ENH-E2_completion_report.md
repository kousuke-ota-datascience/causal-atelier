# ENH-E2 Completion Report

## 1. Final Decision

**COMPLETE**

事実: FR-068〜FR-095、NFR-017〜NFR-021を実装または正本文書で確認し、default test、PostgreSQL contract、migration往復、実API Golden Path、実Chromium E2E-04〜E2E-10、既存Scientific BenchmarkをPASSした。

判断根拠: Project archive、Graph Version状態遷移、Outcome継承とtampering拒否をFrontendだけへ依存させずDomain / Application / API / DBで強制した。Graph Candidateは永続Entityを追加せずQuery Modelとして生成し、FIXED Graphの直接更新経路を設けていない。

## 2. Baseline

- Branch: `prototype/ariadne_mvp`
- Start commit: `8b28a8792e4579fb29651a380be0db5351f1a911`
- End commit: `8b28a8792e4579fb29651a380be0db5351f1a911`（未commit working treeを検証対象としたため同一）
- Migration head: `20260806_product_0003`
- Canonical document hashes:
  - `00_プロダクトコンセプトメモ.md`: `b92e252c19dfb269eddc938243ea9d380bab276dd6dbc448331fdcb019d6a5a0`
  - `10_要件定義.md`: `a999e1c09a83e92341f2b2ecc939fb6fd7835db06a016832a4051d086b7faca6`
  - `21_論理データ設計.md`: `0954b5e6e9a56dd9b3123fa52d4e6bf1296c7572eb1ba5f4b8f6812c0b7328f1`
  - `22_プロダクト基本設計.md`: `15f1db88144da96572a6e4d8e59eddb5c8b7ea8127519324419486f607b223aa`
  - `23_API・インターフェース設計.md`: `e8465be0c4715b915c91a247a4fc9db761efec8a580eba85e0700c1d528e7570`
  - `30_詳細設計.md`: `c0249abef2110d2c384785f1415c0c3f0c1fc3e17eec5561cce49e6e8da8666b`

## 3. Requirements

- Implemented IDs: `FR-068`〜`FR-095`、`NFR-017`〜`NFR-021`
- Deferred IDs: なし

| 要件群 | 実装根拠 | Test証跡 |
|---|---|---|
| FR-068〜070, NFR-017 | 各workspace/sectionの説明、入力例、keyboard対応tooltip、用語統一 | Frontend contract、Chromium E2E |
| FR-071〜074 | 専用Project管理、idempotent logical archive、ACTIVE write guard、read lineage保持 | `test_project_delete_is_idempotent_archive_and_all_new_writes_are_guarded`、E2E-07 |
| FR-075〜079 | Dataset schema由来Feature selector、決定論的同期、Outcome選択、Snapshot/Result/Graph伝播、Outcome node配置 | API/worker E2E、E2E-08 |
| FR-080〜087, NFR-019 | Discovery Result + Graph Version Query Model、状態別操作、子DRAFT、modal編集、2件以上のSVG/構造差分比較 | `test_graph_candidate_lifecycle_and_comparison_are_state_derived`、E2E-09/10 |
| FR-088〜091 | Identification/Data Eligibility説明、Graph Outcome read-only継承、未指定/不一致拒否 | `test_inference_rejects_missing_or_tampered_graph_outcome`、E2E-10 |
| FR-092〜095, NFR-018 | Project/Graph状態機械、shared policy、machine-readable domain error、API側強制 | ENH-E2 contract 3件、API contract |
| NFR-020〜021 | 全主要画面の操作・状態表とE1a contractが指定された改訂版正本へ統合済み | 正本文書hash固定、document review |

## 4. Changed Files

- Domain / Application:
  - `domain/{project.py,graph_version.py,analysis_spec.py,errors.py}`
  - `application/{project_policy.py,project_data_service.py,graph_version_service.py,graph_candidate_query_service.py,execution_service.py,annotation_service.py,query_service.py}`
- Persistence / Migration:
  - `persistence/{orm_models.py,repositories.py}`
  - `product_migrations/versions/20260806_product_0003_enh_e2.py`
- Interfaces:
  - Project、Graph Version、Graph Candidate、Result router/schema/dependency/error/idempotency
  - WorkerのDiscovery Outcome Result伝播
- Scientific adapter:
  - `scientific/discovery/adapter.py`
- Frontend:
  - `frontend/{index.html,app.js,styles.css}`
- Tests:
  - `tests/product/test_enh_e2_contract.py`
  - API/worker E2E、Golden Path、実Chromium runnerの更新

## 5. State Transition Compliance

### Project

- `ACTIVE -> ARCHIVED`のみを許可し、DELETEは同じ最終状態へ収束する。
- ARCHIVED後はmetadata、Dataset、Graph、Execution、Annotationの新規writeを409 `PROJECT_ARCHIVED`で拒否する。
- 通常一覧はACTIVEのみ。明示status filterによるARCHIVED readと既存Result/Lineage readは維持する。

### Graph Version

- Discovery Resultは不変のAlgorithm Outputとして扱い、採用時に`DISCOVERED/FIXED` Graph Versionを生成する。
- `DRAFT`のみ同一Version更新可能。`FIXED`からの編集はparentを保持する子`DRAFT`を生成する。
- parentは同一Projectの`FIXED`に限定し、循環を拒否する。FIXEDの直接PATCHは409 `GRAPH_FIXED_IMMUTABLE`。
- `designated_outcome_node`は親/Resultから継承し、変更時はnode membershipと理由を検証する。

### Execution / Result

- Discovery受付時にFeature/OutcomeをDataset schemaへ照合し、不変Snapshotへ保存する。
- WorkerがOutcomeをDiscovery Result payload/summaryへ保存する。
- IDENTIFICATION/ESTIMATIONはFIXED Graphを要求し、Outcome未指定を422 `GRAPH_OUTCOME_REQUIRED`、Causal Questionとの不一致を409 `GRAPH_OUTCOME_MISMATCH`で拒否する。
- ResultとLineageはProject archive後もread可能である。

## 6. Data and API Compliance

- 追加永続列: nullable `product_graph_version.designated_outcome_node`とindex。nullableは既存Graph移行のためであり、新規Inference gateは非nullを要求する。
- Graph Candidate用table: なし。Result/Graph Versionからapplication Query Modelを生成する。
- Migration 0003は、長期稼働DBで確認された初期0002 constraint差異も正本定義へ正規化する。legacy snapshotのread互換を保ち、current v2 ESTIMATIONのIdentification Result必須条件は弱化しない。
- 主要追加API: Project archive/status filter、nested Graph GET/PATCH/fix、Graph edit draft、Graph Candidate list/detail/comparison。
- Dataset uploadの空ファイル、parse不能、未対応拡張子は422 `INVALID_DATASET_FILE`とし、内部障害の500と区別する。
- `dataset_key`、`version_label`、`name`、`source_note`はDB/API上限をapplication層でも検証する。特に100文字を超える`dataset_key`は422 `INVALID_DATASET_METADATA`を返す。
- Dataset Artifactの`object_key`はuser-controlled metadataを含めず、Project IDとArtifact IDから構成する。これにより長いkeyやpath文字をfilesystem pathへ伝播させない。
- Graph SVGは最大6列で折り返し、`viewBox`をcanvas幅へ追従させ、横scrollなしですべてのnodeを表示する。

## 7. Tests

| 区分 | Command / Scope | 結果 |
|---|---|---|
| Unit / API / Frontend / Benchmarkを含むdefault | `.venv/bin/pytest -q` | `115 passed, 4 skipped in 23.47s` |
| ENH-E2 behavior | `tests/product/test_enh_e2_contract.py` | default suite内で8件PASS |
| Live Dataset regression / PostgreSQL | 273文字key、正常key、Artifact read/download | 422、201、200/200（500なし） |
| PostgreSQL integration（0003適用済みCompose DB） | `... pytest -q tests/product/test_postgres_contract.py` | `4 passed in 1.33s` |
| Fresh migration DB PostgreSQL contract | 同上、`ariadne_enh_e2_recheck` | `4 passed in 2.91s` |
| Migration | fresh DB: empty→head→0002→head | PASS、final `20260806_product_0003 (head)` |
| Real API/worker/PostgreSQL Golden Path | `compose_golden_path_smoke.py` against `:18000/api/v1` | PASS、Discovery 3、Estimation 3 |
| Real Chromium | Playwright 1.62.0 / Chromium 151、invalid Dataset、tooltip、Graph非scroll、E2E-04〜10 | PASS |
| Scientific Benchmark regression | `tests/scientific_benchmarks` | `21 passed` |
| Static | `compileall`, `node --check`, `git diff --check` | PASS |

Default suiteの4 skipはPostgreSQL URL未設定時の条件付きtestである。同じPostgreSQL testを実DBに対して別途全件PASSしており、未検証要件ではない。

Browser evidence: `test-results/browser_e2e/evidence.json`、`trace.zip`、video、E2E-04/05/06/10 screenshots。意図的な負ケース4件のHTTP 422がconsoleへ記録されるが、いずれも期待する入力・業務拒否である。

## 8. Deviations

- 機能要件からの逸脱: なし。
- 実装上の追加対応: 稼働済み一部DBの初期0002 check constraint差異を0003で正本定義へ正規化した。これはE1/E1a regression保持のためであり、現行入力gateは維持される。

## 9. Unresolved Issues

- 実装上の未解決事項: なし。
- 環境注記: test Compose stackは最終確認時点で稼働中。Browser/benchmark artifactは`.gitignore`対象で、記載コマンドにより再生成する。
- Workspace注記: 作業開始時から存在した`bug_and_improvement.md`の移動状態、およびユーザ提供の実装指示書・改訂版文書は変更対象として扱っていない。
