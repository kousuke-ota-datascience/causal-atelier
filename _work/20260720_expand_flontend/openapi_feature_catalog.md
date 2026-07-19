# causal-atelier OpenAPI機能一覧

`http://localhost:8000/docs`のSwagger UIは、causal-atelierのバックエンド機能を操作するControl Planeインターフェイスです。現在、Health checkを含めて52操作が公開されています。

一方、`http://localhost:8080`のFrontendから操作できるのはProject一覧と新規作成だけです。

## 1. Project管理

| 操作 | API |
|---|---|
| Project作成 | `POST /api/v1/projects` |
| Project一覧 | `GET /api/v1/projects` |
| Project詳細取得 | `GET /api/v1/projects/{project_id}` |
| Project名・説明更新 | `PATCH /api/v1/projects/{project_id}` |
| Project削除（論理削除） | `DELETE /api/v1/projects/{project_id}` |
| Projectメンバー一覧 | `GET /api/v1/projects/{project_id}/members` |
| メンバー追加・権限変更 | `POST /api/v1/projects/{project_id}/members` |

メンバーには次の権限を設定できます。

- `VIEWER`
- `ANALYST`
- `MAINTAINER`
- `PROJECT_ADMIN`

## 2. Dataset・Object管理

| 操作 | API |
|---|---|
| CSV等をObject Storeへupload | `POST /api/v1/projects/{project_id}/objects` |
| Dataset作成 | `POST /api/v1/datasets` |
| Project内のDataset一覧 | `GET /api/v1/datasets` |
| Dataset Version作成 | `POST /api/v1/datasets/{dataset_id}/versions` |
| Dataset Version詳細 | `GET /api/v1/dataset-versions/{version_id}` |
| Dataset RegistryをYAMLでexport | `GET /api/v1/dataset-versions/{version_id}/registry` |
| 既存Registryをimport | `POST /api/v1/datasets/import-registry` |
| Table preview | `GET /api/v1/dataset-table-versions/{table_version_id}/preview` |
| Table profile取得 | `GET /api/v1/dataset-table-versions/{table_version_id}/profile` |
| Column Policy更新 | `PATCH /api/v1/dataset-columns/{column_id}/policy` |
| ETL前後のDataset比較 | `GET /api/v1/etl-runs/{run_id}/dataset-comparison` |

upload可能な形式は次のとおりです。

- CSV
- Parquet
- RDA
- RDS

Datasetには次の種類があります。

- `RAW`
- `INTERIM`
- `PROCESSED`
- `DISCOVERY_FEATURE`
- `INFERENCE_FEATURE`

Column Policyでは以下を制御できます。

- 機密区分
- preview許可
- 分析利用許可
- download許可
- mask方法
- 最小集計件数

## 3. Configuration管理

| 操作 | API |
|---|---|
| Configuration作成 | `POST /api/v1/configurations` |
| Configuration一覧 | `GET /api/v1/configurations` |
| 不変Configuration Version作成 | `POST /api/v1/configurations/{configuration_id}/versions` |
| Version詳細取得 | `GET /api/v1/configuration-versions/{version_id}` |
| YAMLとしてexport | `GET /api/v1/configuration-versions/{version_id}/export` |
| Configuration検証 | `POST /api/v1/configuration-versions/{version_id}/validate` |
| Configuration公開 | `POST /api/v1/configuration-versions/{version_id}/publish` |

管理できるConfigurationの種類は次のとおりです。

- ETL Extract
- ETL Transform
- ETL Load
- Discovery Analysis
- Discovery Feature
- Inference Analysis
- Inference Feature
- Feature Semantics
- Causal Design
- Pipeline

Configuration Versionは基本的に次の状態で管理されます。

```text
DRAFT -> VALID -> PUBLISHED
```

実際の`RUN`では、原則として`PUBLISHED`のConfigurationが必要です。

## 4. Experiment管理

| 操作 | API |
|---|---|
| Experiment作成 | `POST /api/v1/experiments` |

Experimentには以下を記録できます。

- 分析目的
- 仮説
- ノート
- Git repository
- commit ID
- Notebook参照
- tag

現状はExperimentの一覧・詳細・更新・削除APIがありません。

## 5. Pipeline Definition管理

| 操作 | API |
|---|---|
| Pipeline Definition作成 | `POST /api/v1/pipeline-definitions` |
| Pipeline Definition Version取得 | `GET /api/v1/pipeline-definition-versions/{version_id}` |
| 新しいPipeline Version作成 | `POST /api/v1/pipeline-definitions/{definition_id}/versions` |

Pipelineは以下のstageを組み合わせます。

- `ETL`
- `DISCOVERY`
- `INFERENCE`

Inferenceでは次のモードを指定できます。

- `EDGE_WEIGHT`
- `TREATMENT_EFFECT`

各stageには次を指定できます。

- 依存stage
- Dataset Version
- Configuration Version
- 上流Artifact
- runtime parameter
- 出力Artifact種別
- random seed
- fail-fast設定

## 6. Run実行・状態管理

| 操作 | API |
|---|---|
| Run作成・投入 | `POST /api/v1/runs` |
| Run一覧 | `GET /api/v1/runs` |
| Run詳細・Execution Plan取得 | `GET /api/v1/runs/{run_id}` |
| Run event履歴 | `GET /api/v1/runs/{run_id}/events` |
| RunのArtifact一覧 | `GET /api/v1/runs/{run_id}/artifacts` |
| Runキャンセル | `POST /api/v1/runs/{run_id}/cancel` |
| 失敗・キャンセルRunの再試行 | `POST /api/v1/runs/{run_id}/retry` |

Runの実行モードは次の3種類です。

| モード | 動作 |
|---|---|
| `DRY_RUN` | stageを実行せずExecution Planを生成 |
| `VALIDATE_ONLY` | 設定・入力・因果設計等を検証 |
| `RUN` | workerへ非同期実行を投入 |

Runの種類は次のとおりです。

- `PIPELINE`
- `ETL`
- `DISCOVERY`
- `INFERENCE`

Runには`Idempotency-Key`を指定でき、同じrequestの重複投入を防止できます。

## 7. 分析結果の取得

| 操作 | API |
|---|---|
| 因果探索結果取得 | `GET /api/v1/discovery-results/{result_id}` |
| Edge Weight結果取得 | `GET /api/v1/edge-weight-results/{result_id}` |
| Treatment Effect結果取得 | `GET /api/v1/treatment-effect-results/{result_id}` |

因果探索結果には以下が含まれます。

- 使用algorithm
- edge一覧
- source・target
- orientation
- score
- stability

Edge Weight結果には以下が含まれます。

- 探索edgeごとの係数
- 標準誤差
- p値
- 多重比較補正後p値
- 信頼区間
- 診断情報

Treatment Effect結果には以下が含まれます。

- ATEまたはATT等の推定値
- 推定method
- 信頼区間
- 選択された調整変数
- 除外された調整候補
- 宣言された因果仮定
- balance・overlap等の診断

## 8. Artifact管理・来歴確認

| 操作 | API |
|---|---|
| Artifact metadata取得 | `GET /api/v1/artifacts/{artifact_id}` |
| Artifact内容download | `GET /api/v1/artifacts/{artifact_id}/content` |
| Artifact lineage取得 | `GET /api/v1/artifacts/{artifact_id}/lineage` |

Artifactには次のようなものがあります。

- Discovery edge CSV
- 推定結果CSV
- Markdown report
- 診断table
- resolved configuration
- Dataset table
- manifest
- PNG等

Lineage APIでは、対象Artifactの上流・下流関係を確認できます。

## 9. データ集計・Visualization

| 操作 | API |
|---|---|
| Tableに対してquery実行 | `POST /api/v1/dataset-table-versions/{table_version_id}/visualization-queries` |
| query状態・結果取得 | `GET /api/v1/visualization-queries/{query_id}` |
| 非同期queryキャンセル | `POST /api/v1/visualization-queries/{query_id}/cancel` |
| 結果をCSV・PNGでexport | `GET /api/v1/visualization-queries/{query_id}/export` |

指定可能なchart typeは次のとおりです。

- table
- bar
- line
- scatter
- pie
- histogram
- box

queryでは以下を指定できます。

- 対象列
- filter
- group by
- count・sum・mean・min・max
- distinct count
- sort
- 件数制限
- histogramのbin数
- sampling方式・件数・seed
- 時間単位

任意SQLは実行できず、構造化されたquery specificationだけを受け付けます。

## 10. Visualization Specification管理

| 操作 | API |
|---|---|
| 集計・可視化条件を保存 | `POST /api/v1/visualization-specifications` |
| 保存条件を取得 | `GET /api/v1/visualization-specifications/{specification_id}` |
| 保存条件を実行 | `POST /api/v1/visualization-specifications/{specification_id}/execute` |
| SpecificationをJSONでexport | `GET /api/v1/visualization-specifications/{specification_id}/export` |

同じDataset Version・query条件・query engine versionの成功結果はcacheされます。

## 11. Health check

| 操作 | API |
|---|---|
| API processの生存確認 | `GET /health/live` |
| PostgreSQLを含む準備完了確認 | `GET /health/ready` |

## 現在Swaggerにも存在しない主な操作

以下は現状のAPIにありません。

- Project詳細のFrontend画面
- Datasetの更新・削除
- Object単体の一覧・削除
- Experimentの一覧・詳細・更新・削除
- Pipeline Definitionの一覧・削除
- Configurationの更新・削除
- Visualization Specificationの一覧・更新・削除
- ユーザー一覧
- 監査ログ閲覧API
- Browser上の分析設定エディタ
- Browser上のRun監視画面
- Browser上の因果graph・診断結果表示

Swagger UIはバックエンド機能の操作画面としては充実していますが、一般利用者向けWebアプリの代替ではありません。現状は「API中心の分析Control Planeに、Project作成用の最小Frontendを載せた状態」です。
