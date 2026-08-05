# 92 実装移行結果 詳細レポート

- 作成日時: 2026-08-05 UTC
- 対象リポジトリ: `causal-atelier`
- 対象指示書: `41_ariadne_coding_agent_handoff_prompt_20260805.md`
- 要約レポート: `91_migration_result.md`
- Baseline commit: `bb059ffee047c777ab68a52393ebe492d579fca9`
- 現在の`HEAD`: `bb059ffee047c777ab68a52393ebe492d579fca9`
- 対象Gate: A〜I
- 実装判定: **完了**
- 検証判定: **自動Test、PostgreSQL、Compose、Golden Path、backup/restore、rollbackを確認済み**

## 1. 本レポートの読み方

### 1.1 記述の分類

本レポートでは、根拠の性質を次のように区別する。

| 分類 | 意味 |
|---|---|
| 現在確認した事実 | 2026-08-05に現在の作業ツリーまたは実行環境から再確認した内容 |
| 実装時の記録 | `91_migration_result.md`に保存された、実装作業中の実行結果 |
| 推論 | 複数の実装・Test結果から導いた判断。前提と限界を併記する |
| 未確認 | 実装または一部の代替検証はあるが、直接の自動検証を行っていない事項 |

### 1.2 結論

現在確認した事実として、Gate A〜Iに対応するProduct実装、Scientific Adapter、Product DB、Worker、`/api/v1`、CLI、Frontend、Compose、およびTestが作業ツリーに存在する。PostgreSQLを利用する全36 Testを再実行し、`36 passed in 9.28s`を確認した。Composeでは`database`と`api`がhealthy、`worker`と`frontend`がrunningである。

実装時の記録として、実Scientific Coreを使用したCompose Golden Path、PostgreSQL backup/restore後のGolden Path、および隔離DBでのAlembic downgrade/upgradeが成功している。

以上から、指示書のGate A〜Iは完了と判定する。

ただし、次の事実は完了判定と分けて扱う必要がある。

1. 実装差分はBaseline commit上の未コミット作業ツリーに存在する。したがって、完了は「release commit作成済み」を意味しない。
2. Frontendは静的Contract Test、Nginx配信、実API Golden Pathで検証したが、Playwright等によるブラウザ操作の自動E2E Testは存在しない。
3. backup/restoreとrollbackの詳細な標準出力は独立したlog Artifactとして保存されておらず、実行結果は`91_migration_result.md`の記録に依存する。

## 2. 改修の目的と範囲

### 2.1 目的

旧Control Planeを延命するのではなく、次のProduct経路だけでMVP Golden Pathを成立させることを目的とした。

```text
Web App / CLI
    -> /api/v1 または Scientific Core Adapter
    -> Product Application Service
    -> Product PostgreSQL / Local Artifact Store
    -> Product Worker
    -> Scientific Core Adapter
    -> Discovery / Estimation実装
```

### 2.2 Product業務Entity

正本業務Entityは次の7件である。

| Entity | DB table | 主な責務 |
|---|---|---|
| Project | `product_project` | 分析資産の境界、目的、メモ、状態 |
| Dataset Version | `product_dataset_version` | 入力データの不変version、schema、hash |
| Execution | `product_execution` | 再現可能な実行Snapshotと状態遷移 |
| Result | `product_result` | 科学的結果、status、summary、diagnostics、warning |
| Artifact | `product_artifact` | Dataset・Graph・推定結果等の保存物metadata |
| Graph Version | `product_graph_version` | Discovery Result由来の編集可能・固定Graph |
| Annotation | `product_annotation` | ResultまたはGraphに対する判断、仮定、限界 |

`product_idempotency`はHTTP作成処理の再送制御を担う技術用tableであり、第8の業務Entityとして公開しない。ComparisonとLineageは永続EntityではなくQuery Projectionである。

### 2.3 対象外

次は指示書上のMVP外であり、今回の未完了事項には含めない。

- 詳細RBACと承認workflow
- CATE / HTE
- 連続Treatment
- IV / DiD / RDD
- Cloud Artifact Storeを必須とする構成
- 実在client根拠のないLegacy互換契約

## 3. Gate別トレーサビリティ

### 3.1 Gate総括

| Gate | 要求領域 | 主な実装根拠 | 主な検証根拠 | 判定 |
|---|---|---|---|---|
| A | Baseline・Test・互換対象 | `tests/README.md`、`41_互換性台帳.md`、pytest設定 | 36件collect、0 error | 完了 |
| B | Scientific Core Adapter | `scientific/discovery/adapter.py`、`scientific/inference/adapter.py` | PC/GES、4 Estimator、4種の科学的負結果 | 完了 |
| C | Domain・Persistence | `product/domain/`、`product/persistence/`、Product migration | Domain、Snapshot、Graph、PostgreSQL制約Test | 完了 |
| D | Worker | `interfaces/worker/`、atomic claim | Component E2E、2 Worker同時claim Test | 完了 |
| E | Web API・CLI | `interfaces/web_api/`、`interfaces/cli/` | API/Worker Contract、CLI Contract | 完了 |
| F | 4 Workspace Web App | `frontend/index.html`、`app.js`、`styles.css` | Frontend Contract、Compose配信、API Golden Path | 完了。ただし自動browser E2Eなし |
| G | Compatibility | `41_互換性台帳.md` | C2集合なし、Legacy alias不在のArchitecture Test | 完了 |
| H | Cutover | `Dockerfile`、`compose.yaml`、Product Alembic | Compose、Golden Path、backup/restore、rollback | 完了 |
| I | Legacy廃止 | wheel exclude、`.dockerignore`、entrypoint整理 | Architecture Test、runtime image import確認 | 完了 |

### 3.2 Gate A — Baseline・Test・互換対象

#### 実施内容

- Baselineを`bb059ffee047c777ab68a52393ebe492d579fca9`として固定した。
- TestをActive Product、Scientific Characterization、Retired Legacy Control Planeへ分類した。
- Retired Testを`tests/legacy_archive/`へ移動し、`norecursedirs = ["legacy_archive"]`で既定収集から除外した。
- `tests/README.md`へ分類目的と実行条件を記録した。
- `41_互換性台帳.md`を作成した。
- client、owner、fixture、期限のリポジトリ内根拠がないためC2集合を空とした。
- 旧CLI alias `ariadne-discovery`、`ariadne-inference`、`ariadne-pipeline`を削除した。

#### 検証

```text
36 tests collected in 3.86s
0 collection error
```

PC、GES、主要Estimator、Graph serialization、CLI Manifest、CLI exit codeのcharacterizationは`tests/scientific/`および`tests/product/`に存在する。

#### 判定理由

C2を推測で増やさず、互換対象外のEndpointとcommandを台帳に固定したため、互換範囲が曖昧なまま後続Gateへ進む問題を解消した。

### 3.3 Gate B — Scientific Core Adapter

#### Discovery

実装箇所:

- `src/ariadne/scientific/discovery/adapter.py`
- `src/ariadne/product/ports/scientific_core.py`
- `src/ariadne/product/domain/graph_semantics.py`

実装した契約:

- AlgorithmはPCとGESを明示選択する。
- `analysis_spec.feature_columns`を使用し、未指定全列を自動的に分析対象へ加えない。
- 対応可能なconstraintsを明示的に変換する。
- Graph typeとして`DAG`、`CPDAG`、`PAG`を区別する。
- edgeに`endpoint_source`と`endpoint_target`を保持する。
- 未知parameterをsilent ignoreせずvalidation errorとする。
- DB、Repository、Web schemaを参照せず、file input/outputで実行できる。

Graph canonicalizationではnode順とedge順を決定的にし、endpointを`TAIL`、`ARROW`、`CIRCLE`へ正規化する。DAGに`TAIL-TAIL` edgeを指定する等、Graph typeとendpoint pairが矛盾する入力を拒否する。

#### Estimation

実装箇所:

- `src/ariadne/scientific/inference/adapter.py`
- `src/ariadne/causal/inference/estimators/`
- `src/ariadne/product/ports/scientific_core.py`

実装したEstimator:

| 設定値 | 処理 | Scientific Test許容差 |
|---|---|---:|
| `difference_in_means` | 群平均差 | 真値2.0に対して0.7未満 |
| `ols` | 線形回帰調整 | 真値2.0に対して0.25未満 |
| `ipw` | 逆確率重み付け | 真値2.0に対して0.4未満 |
| `aipw` | Augmented IPW | 真値2.0に対して0.3未満 |

上表の許容差は一般的な統計精度保証ではない。seed固定の合成データに対するregression thresholdである。

Adapterは次を明示的に使用する。

- treatment
- outcome
- estimand: ATEまたはATT
- adjustment set
- assumptions
- inference options
- estimator固有parameter
- random seed

出力はestimate、standard error、confidence interval、sample size、balance、overlap、warnings、Artifactを共通形式へ変換する。

#### Scientific Status

許可する値は次の5件だけである。

```text
VALID
NOT_IDENTIFIED
INSUFFICIENT_OVERLAP
INSUFFICIENT_SAMPLE
ESTIMATION_UNRELIABLE
```

科学的負結果は正常なResultとして返す。Artifact Store障害、hash不一致、DB障害、Scientific Core実行例外等の技術失敗は`InfrastructureError`系として扱い、Scientific Resultへ変換しない。

#### 検証

- PCとGESをDBなしで実行し、いずれも`VALID`とGraph endpoint保持を確認した。
- 4 Estimatorで明示adjustment set `['x']`を使用し、confidence interval、sample size、balanceを確認した。
- treatmentからoutcomeへのpathがない場合に`NOT_IDENTIFIED`を確認した。
- 極端なpropensityで`INSUFFICIENT_OVERLAP`を確認した。
- 8行のsmall sampleで`INSUFFICIENT_SAMPLE`を確認した。
- 不確実性を推定できないAIPW条件で`ESTIMATION_UNRELIABLE`を確認した。
- Architecture TestでScientific packageからProduct persistence、Application、Web APIへのimportがないことを確認した。

### 3.4 Gate C — Product Domain・Persistence

#### 状態遷移と不変条件

Executionの主状態遷移は次である。

```text
QUEUED -> RUNNING -> SUCCEEDED
                  -> FAILED -> QUEUED  (retry_count + 1)
QUEUED/RUNNING -> CANCELLED
```

不正な状態遷移は`InvalidStateTransition`で拒否する。retryではSnapshotを再生成せず、既存`snapshot_hash`を保持する。

Graph Versionは`DRAFT -> FIXED`の一方向である。`FIXED` Graphへの編集は`GraphAlreadyFixed`で拒否し、Estimationは`FIXED` Graphだけを受理する。

Annotationは`target_result_id`または`target_graph_version_id`の厳密なXORである。Application層でtargetの存在とProject境界を検証し、DBでもCHECK制約を設定した。

#### Execution Snapshot

Snapshot hashの入力は次を含む。

- objective / rationale
- Dataset Version ID / Dataset content hash
- input Graph Version ID / Graph content hash
- operation
- algorithmまたはestimator
- parameter
- random seed
- analysis spec
- code version
- runtime versions

canonicalizationはobject keyをsortし、`NULL`を保持し、整数・浮動小数を正規化したnumber表現へ変換する。`-0.0`と`0`は同一、`2**60`と`2**60 + 1`は別hashとなる。NaNとInfinityは拒否する。

#### Product migration

- Alembic revision: `20260805_product_0001`
- version table: `alembic_version_product`
- migration設定: `alembic_product.ini`
- migration本体: `product_migrations/versions/20260805_product_0001_baseline.py`

作成table:

```text
product_project
product_dataset_version
product_execution
product_result
product_artifact
product_graph_version
product_annotation
product_idempotency
alembic_version_product
```

主なDB制約:

- 全業務参照に`RESTRICT` FK
- Project status、Execution operation/status、Result type、Scientific status、Graph type/status、Artifact typeのCHECK
- DiscoveryではGraph入力なし、EstimationではGraph入力必須のCHECK
- `retry_count >= 0`、`row_count >= 0`、`column_count >= 0`、`size_bytes >= 0`
- Datasetの`(project_id, dataset_key, version_label)` UNIQUE
- Datasetの`(project_id, dataset_key, content_hash)` UNIQUE
- Artifact `object_key` UNIQUE
- Annotation target XOR CHECK
- Idempotencyの`(project_id, scope, idempotency_key)` UNIQUE

#### 検証

PostgreSQL Testで次を確認した。

- Product tableと`alembic_version_product`が存在する。
- `execution_stage`、`pipeline_`、`outbox`等のLegacy tableが存在しない。
- transaction rollback後にinsert rowが残らない。
- 不正Project statusがCHECK違反になる。
- 存在しないProjectを参照するArtifactがFK違反になる。
- Artifact object key重複がUNIQUE違反になる。

### 3.5 Gate D — Product Worker

#### Atomic claim

`SqlExecutionRepository.claim_next()`は次の処理を同一transactionで行う。

```sql
SELECT ...
FROM product_execution
WHERE status = 'QUEUED'
ORDER BY requested_at
FOR UPDATE SKIP LOCKED
LIMIT 1
```

取得したrowへ`RUNNING`、`started_at`、worker tokenを設定し、callerがtransactionをcommitする。

PostgreSQL上で2 thread、2 DB sessionを同時に開始したTestでは、一方だけが対象Executionを取得し、もう一方は`None`を取得した。最終statusは`RUNNING`だった。

#### Worker処理

`ExecutionProcessor`は次の順で処理する。

1. claim済みExecutionがまだ`RUNNING`か再取得する。
2. Dataset VersionとDataset Artifactを取得する。
3. Artifact StoreからDatasetを一時領域へretrieveする。
4. Dataset file hashをArtifact metadataおよびDataset Version hashと照合する。
5. cancel済みか確認する。
6. Estimationの場合は`FIXED` Graphを取得し、canonical JSON hashを照合する。
7. Scientific Core Adapterを呼ぶ。
8. ResultとArtifact metadataを組み立てる。
9. Artifact本体をStoreへ保存する。
10. Result、Artifact metadata、Execution `SUCCEEDED`を同一DB transactionでcommitする。
11. DB保存に失敗した場合、先に保存したArtifact本体を削除する。

例外時はExecutionを`FAILED`へ遷移させる。科学的負結果は例外ではないため、Resultを保存しExecutionを`SUCCEEDED`とする。

#### Component Testで確認した分岐

- Dataset登録からDiscovery 3件、Graph固定、Estimation 2件、Result/Artifact保存
- scientific negative `NOT_IDENTIFIED`でResult保存 + `SUCCEEDED`
- technical exceptionでResultなし + `FAILED`
- FAILED Executionのretryで`QUEUED`へ戻り、Snapshot hash不変
- QUEUED Executionのcancelで`CANCELLED`

### 3.6 Gate E — Web API・CLI

#### Web API共通契約

- Product endpoint prefix: `/api/v1`
- readiness endpoint: `/health/ready`
- Pydantic model: `extra="forbid"`相当のstrict request validation
- Error envelope: `error.code`、`error.message`、`error.details`、`error.request_id`
- Request ID: `X-Request-Id`を受理し、未指定時はUUIDを生成してresponse headerにも返す。

主なerror mapping:

| 条件 | HTTP | error code |
|---|---:|---|
| Request validation | 400 | `INVALID_REQUEST` |
| Entityなし | 404 | `ENTITY_NOT_FOUND` |
| Project境界違反 | 422 | `PROJECT_BOUNDARY_VIOLATION` |
| Idempotency payload不一致 | 409 | `IDEMPOTENCY_CONFLICT` |
| FIXED Graph更新 | 409 | `GRAPH_ALREADY_FIXED` |
| Execution状態競合 | 409 | `EXECUTION_STATE_CONFLICT` |
| Graph semantics不正 | 422 | `INVALID_GRAPH_SEMANTICS` |
| Analysis spec不正 | 422 | `INVALID_ANALYSIS_SPEC` |
| Artifact hash不一致 | 500 | `ARTIFACT_HASH_MISMATCH` |

#### Endpoint一覧

Project:

```text
POST  /api/v1/projects
GET   /api/v1/projects
GET   /api/v1/projects/{project_id}
PATCH /api/v1/projects/{project_id}
```

Dataset Version:

```text
POST /api/v1/projects/{project_id}/dataset-versions
GET  /api/v1/projects/{project_id}/dataset-versions
GET  /api/v1/dataset-versions/{dataset_version_id}
GET  /api/v1/dataset-versions/{dataset_version_id}/preview
```

Execution:

```text
POST /api/v1/projects/{project_id}/execution-batches
GET  /api/v1/projects/{project_id}/executions
GET  /api/v1/executions/{execution_id}
GET  /api/v1/executions/{execution_id}/prefill
POST /api/v1/executions/{execution_id}/cancel
POST /api/v1/executions/{execution_id}/retry
```

Result / Query:

```text
GET  /api/v1/executions/{execution_id}/results
GET  /api/v1/results/{result_id}
POST /api/v1/comparisons/query
GET  /api/v1/results/{result_id}/lineage
POST /api/v1/results/{result_id}/export
```

Graph Version:

```text
POST  /api/v1/projects/{project_id}/graph-versions
GET   /api/v1/projects/{project_id}/graph-versions
GET   /api/v1/graph-versions/{graph_version_id}
PATCH /api/v1/graph-versions/{graph_version_id}
POST  /api/v1/graph-versions/{graph_version_id}/fix
```

Annotation / Artifact:

```text
POST  /api/v1/projects/{project_id}/annotations
GET   /api/v1/annotations/{annotation_id}
PATCH /api/v1/annotations/{annotation_id}
GET   /api/v1/artifacts/{artifact_id}
GET   /api/v1/artifacts/{artifact_id}/download
```

#### Idempotency

Dataset Version、Execution Batch、Graph Version、Result exportで`Idempotency-Key`を扱う。同じProject、scope、key、request hashの再送は保存済みresponseを返す。同じkeyを異なるpayloadへ再利用すると`409 IDEMPOTENCY_CONFLICT`を返す。

SQLite component testではprocess内`RLock`、PostgreSQLではtransaction-scoped advisory lockを使用し、複数API process間の同時再送を直列化する。永続recordにはrequest hashとresponse JSONを保存する。

#### CLI

公開entrypointは次の4件である。

```text
ariadne-discover
ariadne-estimate
ariadne-api
ariadne-worker
```

分析CLIは次の形式へ統一した。

```bash
ariadne-discover --config discovery.yaml
ariadne-estimate --config estimation.yaml
```

YAML configは未知fieldを拒否し、入力fileの存在とhashを検証する。CLIはWeb API、Product DB、Web Execution IDを作成せず、Scientific Core Adapterを直接使用する。

Manifest 1.0には次を保存する。

- input file pathとcontent hash
- graph pathとcontent hash（Estimation）
- analysis specとparameter
- code/runtime version
- scientific status
- result summary
- Artifact path、media type、size、content hash

exit code:

| code | 意味 |
|---:|---|
| 0 | 成功または科学的負結果 |
| 2 | config/input validation error |
| 3 | input Artifact error |
| 4 | technical Scientific Core error |
| 5 | output write error |

### 3.7 Gate F — 4 Workspace Web App

Frontendはvanilla HTML/CSS/JavaScriptで全面置換した。新しい大規模frameworkは導入していない。

| Workspace | 主な機能 |
|---|---|
| Project / Data | Project作成・選択・更新、Dataset登録・一覧・preview、schema/row/column/hash表示 |
| Discovery | Dataset選択、PC/GES、parameter grid、複数Execution、3 Graph以上の比較、Graph編集・固定、選定理由Annotation |
| Inference | FIXED Graph選択、treatment/outcome、ATE/ATT、adjustment set、assumptions、複数Estimator、preflight、diagnostics比較 |
| Results / Lineage | Result詳細、Scientific Status、warning、diagnostics、Artifact download/export、Annotation、Lineage |

FrontendのAPI baseは`const API="/api/v1"`であり、Legacy API、MLflow、pipelineを参照しない。Nginxは`/api/`をProduct APIへproxyする。

自動Testは4 WorkspaceのDOM ID、必須Endpoint文字列、Legacy参照不在、Graph Version Annotation request shapeを検証する。

検証限界として、実ブラウザで各button、form、画面遷移を操作する自動Testはない。Compose Golden PathはFrontendと同じProduct APIを使用するが、HTTP clientからAPIを直接呼んでいる。このため「UI操作そのものの自動回帰保証」までは得られていない。

### 3.8 Gate G — Compatibility Adapter

互換性台帳のC2集合は空である。根拠は、実在client、owner、fixture、deprecation期限を裏付けるrepository内証拠がないことである。

したがって、推測に基づくCompatibility Adapterは実装していない。旧契約はC0へ分類し、壊れたCLI entrypointを残していない。`interfaces/legacy_compat/`も作成していない。

代替仮説として外部clientが存在する可能性は、repositoryだけでは否定できない。ただし、そのclient情報が提供されない限り、要件上C2へ昇格させる根拠にはならない。

### 3.9 Gate H — Cutover

#### Docker image

- base image: `python:3.12-slim`
- dependency sync: `uv sync --frozen --no-dev`
- runtime user: non-root `causal`
- API command: `uvicorn ariadne.interfaces.web_api.app:app`
- Product Alembic設定とmigrationをimageへcopy
- `/state/objects`と`/state/workspaces`をruntime stateとして使用

#### Compose service

| service | 役割 | 起動依存 |
|---|---|---|
| `database` | PostgreSQL 17 | なし |
| `migrate` | Product Alembic `upgrade head` | database healthy |
| `api` | Product FastAPI | migrate successful |
| `worker` | Product Worker | migrate successful |
| `frontend` | Nginx静的UI | api healthy |

Product DB URLは次で固定され、Legacy DB URLまたはSQLite fallbackは使用しない。

```text
ARIADNE_PRODUCT_DATABASE_URL=postgresql+psycopg://ariadne:ariadne@database:5432/ariadne
```

#### 現在のCompose状態

2026-08-05の再確認結果:

```text
api       Up (healthy)  0.0.0.0:8000->8000
database  Up (healthy)  127.0.0.1:5432->5432
frontend  Up            0.0.0.0:8080->80
worker    Up
```

`migrate`はone-shot serviceであり、正常完了後はrunning一覧に残らない。

#### Compose Golden Path

実装時に`tests/product/compose_golden_path_smoke.py`を実Scientific Coreへ接続して実行した。処理内容は次のとおりである。

1. seed `20260805`の240行synthetic CSV生成
2. Project作成
3. Dataset Version登録と同一idempotency key再送
4. Dataset preview
5. PC alpha 0.01、PC alpha 0.05、GESの3 Discovery
6. 3 Discovery ResultのComparison
7. Discovery ResultからGraph Versionを作成してFIXED化
8. OLS、IPW、AIPWの3 Estimation
9. 3 Estimation ResultのComparison
10. Annotation作成
11. Project、Dataset Version、Execution、Result、Graph Version、Artifact、Annotationを含むLineage確認
12. Artifact download
13. Manifest 1.0 export

記録された最終結果:

```text
discovery_results=3
estimation_results=3
root_result_id=f710da13-43aa-4089-9f82-92a040ec0ac7
status=PASS
```

UUIDはその実行固有であり、再実行時に一致することは要件ではない。

#### Backup / restore

実装時の記録:

```text
pg_dump -Fc ariadne                         -> exit 0
pg_restore -d ariadne_restore <dump file>  -> exit 0
```

restore直後に次を確認した。

- Alembic revision: `20260805_product_0001`
- Project: 2件
- Result: 12件
- Artifact: 26件

復元DBを`ariadne`へ切り替えた後、同じGolden PathがDiscovery 3件、Estimation 3件、`status=PASS`で完走した。

#### Rollback

隔離DB `ariadne_rollback`で次を実行した。

```text
upgrade head -> downgrade base -> upgrade head
```

全commandがexit 0、downgrade後の`product_%` table数が0、再upgrade成功を確認した。隔離DBは検証後に削除した。

#### 破壊的操作の記録

Cutover開始時、指示書の空Product DB要件に基づいて`docker compose down -v`を実行した。旧`metadata-data`および`artifact-data` volumeは削除済みであり、外部backupがない限り削除前の内容は復元できない。その後、新しいvolumeを作成した。

### 3.10 Gate I — Legacy廃止

#### 起動経路からの除去

ComposeにはProduct PostgreSQL、Product migration、Product API、Product Worker、Frontendだけが存在する。Legacy API、Legacy Worker、Legacy DB migration、MLflowは起動構成に存在しない。

#### package/imageからの除去

`pyproject.toml`のwheel excludeと`.dockerignore`で次をruntime package/imageから除外した。

- `src/ariadne/legacy/**`
- 旧Artifact Store、Auth、Data Query、Persistence、Storage、Tracking
- 旧logging/settings/shared identity/exceptions

履歴参照用sourceはrepository内に凍結しているが、wheel、Docker build context、entrypoint、runtime import pathには含まれない。

Scientific Adapterが選択利用する`ariadne.causal`、`ariadne.preprocessing`、共通configは残している。これらはLegacy Control Plane起動経路ではなく数値・前処理資産である。

#### dependency削減

MLflow、EconML、Dask、Azure SDK、AWS SDK、RData、JWT等をruntime dependencyから削除した。実装時のimage計測ではinstall package数が旧構成138からProduct構成59へ減少した。

このpackage数は同一手順で作成した当時のimage比較値であり、一般的な性能指標ではない。依存更新後は再計測が必要である。

#### 検証

- Product/Application/Web APIから`ariadne.legacy` importがない。
- Product runtime設定に旧CLI aliasがない。
- Composeに`ariadne.legacy`、旧Alembic、旧DB URL、MLflowがない。
- runtime imageで`ariadne.legacy`と`ariadne.infrastructure.tracking`がimport不能である。
- `uv build --offline`でsdist/wheel作成に成功し、除外moduleがwheelに含まれない。

## 4. Test結果詳細

### 4.1 2026-08-05再実行結果

実行command:

```bash
ARIADNE_PRODUCT_TEST_DATABASE_URL=postgresql+psycopg://ariadne:ariadne@127.0.0.1:5432/ariadne \
PYTHONDONTWRITEBYTECODE=1 \
/tmp/ariadne-py312-clean/bin/pytest -q
```

結果:

```text
....................................                                     [100%]
36 passed in 9.28s
exit code 0
```

collect-only:

```text
36 tests collected in 3.86s
exit code 0
```

`git diff --check`もexit code 0だった。

### 4.2 Test分類と件数

| Test file | 件数 | 主対象 |
|---|---:|---|
| `tests/integration/test_core.py` | 4 | validation、YAML hash、design schema、shared architecture |
| `tests/integration/test_inference.py` | 7 | estimator method、cross fitting、multiplicity、ATE/ATT、overlap warning |
| `tests/product/test_api_worker_e2e.py` | 1 | API、Worker、Domain contractのcomponent Golden Path |
| `tests/product/test_architecture.py` | 3 | Legacy import禁止、Scientific境界、runtime除外 |
| `tests/product/test_cli_contract.py` | 3 | Manifest、scientific negative exit、unknown field |
| `tests/product/test_domain_and_snapshot.py` | 4 | status集合、Snapshot、Graph round trip、状態遷移 |
| `tests/product/test_frontend_contract.py` | 1 | 4 Workspace、新API限定 |
| `tests/product/test_postgres_contract.py` | 3 | schema、制約、rollback、atomic claim |
| `tests/scientific/test_product_adapters.py` | 10 | PC/GES、4 Estimator、4 Scientific negative |
| 合計 | 36 | すべて成功 |

### 4.3 Testが直接確認する主要Contract

#### API / Worker component Golden Path

- unknown JSON field拒否
- Project作成・一覧
- Dataset idempotent登録とpreview
- Discovery 3 variant
- Discovery Comparison
- Graph Version作成とFIXED化
- FIXED Graph上書き拒否
- GraphとAnnotationのProject境界違反拒否
- DRAFT Graphを使用したEstimation拒否
- OLS/IPW ExecutionとResult/Artifact保存
- Annotation、Lineage、Artifact download
- Result export idempotency
- idempotency keyの異なるpayload再利用拒否
- scientific negativeとtechnical failureの分離
- retry Snapshot不変
- cancel

#### PostgreSQL Contract

- Product schema存在とLegacy table不在
- FK / CHECK / UNIQUE
- rollback
- 2 worker同時claim排他性

#### Scientific Contract

- PC/GESのDB非依存実行
- Graph endpoint semantics
- Difference in means / OLS / IPW / AIPW
- 明示adjustment set
- estimator別数値許容差
- 5 Scientific Statusのうち4種のnegative分岐

#### CLI Contract

- Web Execution IDなし
- Dataset/Graph/Artifact hash
- Manifest version 1.0
- scientific negativeのexit code 0
- unknown config fieldのexit code 2

## 5. 主要変更ファイル

### 5.1 新規追加

```text
.dockerignore
docs/.../41_互換性台帳.md
src/ariadne/interfaces/cli/config_schema.py
src/ariadne/interfaces/web_api/idempotency.py
src/ariadne/interfaces/web_api/routers/artifacts.py
src/ariadne/product/application/artifact_service.py
src/ariadne/product/application/query_service.py
src/ariadne/product/domain/graph_semantics.py
tests/README.md
tests/legacy_archive/
tests/product/
tests/scientific/
```

### 5.2 主な更新

```text
Dockerfile
compose.yaml
pyproject.toml
uv.lock
alembic_product.ini
product_migrations/env.py
product_migrations/versions/20260805_product_0001_baseline.py
src/ariadne/scientific/discovery/adapter.py
src/ariadne/scientific/inference/adapter.py
src/ariadne/product/domain/
src/ariadne/product/application/
src/ariadne/product/persistence/
src/ariadne/interfaces/worker/
src/ariadne/interfaces/web_api/
src/ariadne/interfaces/cli/
frontend/index.html
frontend/app.js
frontend/styles.css
docs/.../23_API・インターフェース設計.md
docs/.../91_migration_result.md
```

### 5.3 Test整理

旧Control Planeに結合したTestを`tests/legacy_archive/`へ移動し、既定pytest対象外とした。これは旧Testを成功扱いに変更したのではなく、Product受入TestとRetired Legacy Testの母集団を分離したものである。

## 6. 再現手順

### 6.1 起動

```bash
cd /loc0/bigbrother/repositories/causal-atelier
docker compose up --build -d
docker compose ps
```

アクセス先:

- Frontend: `http://localhost:8080`
- OpenAPI: `http://localhost:8000/docs`
- Readiness: `http://localhost:8000/health/ready`

### 6.2 Log確認

```bash
docker compose logs --tail=100 database migrate api worker frontend
docker compose logs -f api worker
```

### 6.3 Golden Path smoke

```bash
/tmp/ariadne-py312-clean/bin/python tests/product/compose_golden_path_smoke.py
```

scriptは新しいProjectとResourceを作成するため、実行ごとにDBとArtifact volumeの使用量が増える。

### 6.4 Test

```bash
ARIADNE_PRODUCT_TEST_DATABASE_URL=postgresql+psycopg://ariadne:ariadne@127.0.0.1:5432/ariadne \
PYTHONDONTWRITEBYTECODE=1 \
/tmp/ariadne-py312-clean/bin/pytest -q
```

`/tmp/ariadne-py312-clean`は今回の検証環境固有である。別環境ではPython 3.12と`uv sync --frozen`で環境を構築してからpytestを実行する。

### 6.5 停止

```bash
docker compose down
```

次は永続volumeを削除するため、データ削除の明示的な意図がある場合だけ実行する。

```bash
docker compose down --volumes
```

## 7. 既知の限界・残存リスク

### 7.1 実装完了とは別に残る検証限界

| 項目 | 事実 | 影響 | 推奨対応 |
|---|---|---|---|
| Browser E2E | 自動browser操作Testなし | DOM wiring、表示崩れ、操作順の回帰を完全には検出できない | Playwright等でE2E-01〜03を追加 |
| Backup log | 実行要約は文書にあるがraw log Artifactなし | 後日の監査で実行時刻・command全出力を独立確認できない | CIでdump/restore logとhashを保存 |
| Uncommitted state | `HEAD`はBaselineのまま | commit hashだけでは完成状態を再現できない | review後に単一またはGate単位commitを作成 |
| Performance | 36 TestとGolden Pathは機能検証 | 大量Dataset、高並列Worker、長時間処理のSLOは不明 | load/soak testとSLO定義 |
| Security | local development構成 | 本番OIDC、権限分離、secret管理は未検証 | 本番deploy前にsecurity設計・Test |

### 7.2 反対仮説と評価

#### 「全Test成功ならWeb Appの全操作も保証される」

成立しない。Frontend Contract Testは静的文字列とDOM構造を確認し、Compose Golden PathはAPIを直接呼ぶ。したがって、browser event wiring全体を直接保証しない。

#### 「Legacy sourceがrepositoryに残るためGate I未完了である」

指示書は旧Control Plane codeのarchiveまたは削除を許可している。現状はsourceを履歴参照用に凍結し、wheel、image、entrypoint、Compose、runtime importから除外しているため、起動時依存という意味では廃止済みである。

#### 「C2 AdapterがないためGate G未完了である」

指示書は、実在client根拠がなくC2集合が空の場合に「C2実装なし、C0/C1のみ」での完了を許可している。現在の互換性台帳にはC2を支持するclient/owner/fixtureの証拠がない。

#### 「Test母集団を減らしたため36 passedは旧機能の後方互換を保証する」

成立しない。36 Testは新Product契約と選択したScientific Core契約を検証する。Retired Legacy Testは収集対象外であり、旧Control Planeの後方互換性は意図的に保証しない。

## 8. 最終判定

### 8.1 事実

- Gate A〜Iに対応する実装が現在の作業ツリーに存在する。
- 全36 Testが2026-08-05の再実行で成功した。
- PostgreSQL Integration Test 3件を含む。
- ComposeのProduct APIとdatabaseはhealthy、workerとfrontendはrunningである。
- 実装時に実Scientific Core Golden Path、backup/restore後Golden Path、rollback smokeが成功した記録がある。
- Legacy Control PlaneはProduct runtime package、image、entrypoint、Composeから除外されている。

### 8.2 推論と前提

上記事実、および「C2集合は証拠がない場合に空でよい」「Legacy codeはarchiveまたは削除でよい」という指示書の前提に基づき、Gate A〜Iを完了と判定する。

この判定は、Production security、性能SLO、browser自動E2E、外部に存在する可能性のある未申告Legacy clientまで保証するものではない。また、現在の成果は未コミットであるため、再現可能なrelease単位として確定するにはreviewとcommitが必要である。
