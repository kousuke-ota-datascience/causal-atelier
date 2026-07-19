# causal-atelier Webサービス起動・アクセスチュートリアル

## 1. Webサービスの構成

Docker Composeは次のserviceを起動します。

| service | 役割 | Hostからのアクセス |
|---|---|---|
| `frontend` | Nginxで静的UIを配信し、`/api/`をAPIへ転送 | `http://localhost:8080` |
| `api` | FastAPI Control Plane | `http://localhost:8000` |
| `worker` | profile、可視化query、Discovery、Inference等を非同期実行 | HTTP portなし |
| `database` | PostgreSQL metadata DB | Compose network内のみ |
| `migrate` | API起動前にAlembic migrationを実行 | 一度実行して終了 |

登録したCSV/Parquet本体と生成Artifactは、Composeの`artifact-data` named volume（container内の`/state`）へ保存されます。Dataset、Dataset Version、Run、Configuration、Saved Graph等のmetadataは`metadata-data` named volumeのPostgreSQLへ保存されます。Webから登録したfileはrepositoryの`data/`配下へ直接コピーされるわけではありません。

## 2. 前提条件

Docker EngineとDocker Compose pluginが必要です。

```bash
docker --version
docker compose version
cd /loc0/bigbrother/repositories/causal-atelier
```

Hostの`8000`と`8080`が他のprocessで使用されていないことも確認してください。

## 3. 起動する

初回はimage buildとPython dependencyの導入があるため時間がかかります。

```bash
docker compose up --build -d
```

状態を確認します。

```bash
docker compose ps
```

期待する状態:

- `database`がhealthy
- `migrate`がexit code 0で完了
- `api`がhealthy
- `worker`と`frontend`がrunning

起動途中や失敗時のlogは次で確認できます。

```bash
docker compose logs --tail=100 database migrate api worker frontend
```

継続してAPIとworkerのlogを見る場合:

```bash
docker compose logs -f api worker
```

## 4. Browserからアクセスする

### Frontend

Browserで次を開きます。

```text
http://localhost:8080
```

現在のFrontend MVPでは、次の分析フローを画面から実行できます。

1. 「新しいProject」を押す。
2. Slugへ`tutorial-project`を入力する。
3. Nameへ`Tutorial project`を入力する。
4. 必要ならDescriptionを入力し、「作成する」を押す。

Slugは小文字英数字とhyphenを使用し、同じSlugを重複作成しないでください。

Projectを開くと、左側に次のworkflowが表示されます。

1. `Analysis dataset`で、ETL済みの単一CSV/ParquetをDataset Versionとして登録する。
2. 各列のFeature Semanticsを定義してpublishする。
3. `Causal discovery`で複数algorithmを実行し、探索グラフを比較する。
4. 採用するグラフをSaved Graph Versionとして保存・publishする。
5. `Causal inference`でEdge WeightまたはTreatment Effectを推定する。

具体的な画面操作は`tutorial_03_how_to_use_web_app.md`を参照してください。複数raw fileのjoin、集計、業務固有変換等のETLはWeb MVPの通常フローには含みません。外部ETLで「1行が1分析単位」のtableを準備してから登録します。

### OpenAPI UI

全APIをBrowserから確認・実行できます。

```text
http://localhost:8000/docs
```

OpenAPI documentそのものは次です。

```text
http://localhost:8000/openapi.json
```

### Health check

```bash
curl --fail http://localhost:8000/health/live
curl --fail http://localhost:8000/health/ready
```

正常時のresponse:

```json
{"status":"ok"}
{"status":"ready"}
```

`live`はAPI process、`ready`はmetadata DBへの接続も確認します。

## 5. APIへ直接アクセスする

Composeの既定値はdevelopment認証です。API requestには同一利用者を表す`X-User-Subject`を付けます。Frontendは`local-developer`を使用しています。

### Projectを作成する

```bash
curl --fail-with-body \
  -X POST http://localhost:8000/api/v1/projects \
  -H 'Content-Type: application/json' \
  -H 'X-User-Subject: local-developer' \
  -H 'X-User-Name: Local analyst' \
  -d '{
    "slug": "api-tutorial",
    "name": "API tutorial",
    "description": "Created from curl"
  }'
```

responseの`id`がProject IDです。

### Projectを一覧する

```bash
curl --fail-with-body \
  'http://localhost:8000/api/v1/projects?page=1&limit=20' \
  -H 'X-User-Subject: local-developer' \
  -H 'X-User-Name: Local analyst'
```

development認証でも、別の`X-User-Subject`を指定すると別利用者として扱われます。他の利用者のProjectは原則として表示されません。

## 6. OpenAPI UIでAPIを実行する

`http://localhost:8000/docs`では、Frontendが利用しているresourceを含む全APIを確認できます。現在のFrontendの中心フローは次のAPIに対応します。

1. `POST /api/v1/projects`でProjectを作る。
2. `POST /api/v1/projects/{project_id}/objects`でCSVまたはParquetをuploadする。
3. `POST /api/v1/datasets`で論理Datasetを作る。
4. `POST /api/v1/datasets/{dataset_id}/versions`でupload objectをversionへ固定する。
5. `PUT /api/v1/dataset-versions/{version_id}/analysis-binding`で分析単位を結び付ける。
6. Feature SemanticsのConfiguration Versionを作成・検証・publishする。
7. `POST /api/v1/runs`へ`input_mode: ANALYSIS_READY`のDiscovery Runを投入する。
8. `GET /api/v1/runs/{run_id}/results`からResultへ移動し、探索グラフを比較する。
9. Causal GraphとGraph Versionを作成し、採用するグラフをpublishする。
10. Saved Graphを入力にInference Runを投入し、`results`から推定結果を確認する。

profile、preview、Visualization APIおよび従来のETL／`CONFIGURED_FEATURE_BUILD`経路も後方互換のため残っていますが、Web MVPの中心操作ではありません。

Swaggerの各操作でheader欄が表示される場合は、次を指定します。

```text
X-User-Subject: local-developer
X-User-Name: Local analyst
```

RunはAPI containerではなく`worker`が処理します。Runが進まない場合は次を確認してください。

```bash
docker compose ps worker
docker compose logs --tail=200 worker
```

## 7. Serviceを停止・再開する

停止:

```bash
docker compose down
```

`metadata-data`と`artifact-data`のnamed volumeは残るため、次回起動時もmetadata、登録file、artifactを再利用できます。

再開:

```bash
docker compose up -d
```

imageを再buildして再開:

```bash
docker compose up --build -d
```

### データも含めて初期化する場合

次の操作はPostgreSQL metadataと保存済みartifactを含むnamed volumeを削除します。必要なデータがないことを確認してから実行してください。

```bash
docker compose down --volumes
```

## 8. よくある問題

### `http://localhost:8080`を開けない

```bash
docker compose ps frontend api
docker compose logs --tail=100 frontend api
```

FrontendはAPIのhealth check成功後に起動します。まず`http://localhost:8000/health/ready`を確認してください。

### Host portがすでに使われている

`compose.yaml`の次のHost側portを空いている番号へ変更します。

```yaml
api:
  ports:
    - "18000:8000"
frontend:
  ports:
    - "18080:80"
```

この場合のアクセス先は`http://localhost:18000/docs`と`http://localhost:18080`です。

### ProjectがFrontendとcurlで異なって見える

Frontendは`X-User-Subject: local-developer`を使います。curlやSwaggerでも同じsubjectを指定してください。

### migrationが失敗する

```bash
docker compose logs migrate database
docker compose run --rm migrate alembic current
```

DB credentialや既存schemaとの不整合を確認します。

## 9. 本番環境へ展開する際の注意

Composeの既定構成はローカル開発用です。本番利用では少なくとも次を変更してください。

- `CAUSAL_ATELIER_AUTH_MODE=oidc`とし、issuer、audience、JWKS URLを設定する。
- PostgreSQL passwordをsecret manager等で管理する。
- Artifact StoreをS3またはAzure Blobへ変更し、永続性とaccess policyを設定する。
- TLS終端、CORS、network policy、backup、monitoringを構成する。
- APIとworkerを個別にscaleし、migrationをdeploy前jobとして一度だけ実行する。

詳細なenvironment variableと運用上の制約は`docs/web_service.md`を参照してください。
