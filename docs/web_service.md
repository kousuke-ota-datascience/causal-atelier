# Webサービス運用ガイド

## 構成

`compose.yaml` は次の4つのデプロイ単位を起動します。

- `frontend`: Nginxで配信するブラウザUI
- `api`: FastAPI control plane
- `worker`: ETL、profile、可視化query、Discovery、Inferenceのexecution plane
- `database`: PostgreSQL metadata DB

API transactionと非同期処理の受け渡しにはTransactional Outboxを使います。
workerはlease付きでeventをclaimし、Attempt履歴を上書きしません。outbox状態管理、
workspace materialization、result projectionは独立コンポーネントです。Artifactは
論理UUIDとchecksumで管理され、APIへlocal absolute pathを返しません。

Application層は呼出元ではなくuse caseで分割されています。

```text
application/
  pipeline/
  data_catalog/
  configuration_catalog/
  run_execution/
  visualization/
  control_plane/
  ports/
```

APIはMetadata Repository port経由でmetadataを扱い、表データのschema/profile/queryには
Data Query portを使用します。transaction境界用のUnit of Work portとSQLAlchemy adapterも
提供します。SQLAlchemy、PyArrow、Artifact Store実装はInfrastructure adapterとして
差し替えられます。

## 初期化とmigration

Composeでは`migrate` serviceがAPI/workerより先に`alembic upgrade head`を実行します。
手動運用では次を実行します。

```bash
export ARIADNE_DATABASE_URL='postgresql+psycopg://user:password@host/database'
uv run alembic upgrade head
```

`ARIADNE_AUTO_CREATE_SCHEMA=true` はSQLiteを用いるローカル開発・test向けです。
本番ではAlembic migrationを使用してください。

## 認証・認可

`development` modeでは次のheaderで利用者を自動provisionします。

```text
X-User-Subject: stable-local-subject
X-User-Name: Analyst name
X-User-Email: analyst@example.com
```

Project作成者には`PROJECT_ADMIN`が付与されます。Project resourceは`VIEWER`、
`ANALYST`、`MAINTAINER`、`PROJECT_ADMIN`の順に権限を検査し、権限のない
cross-project resourceは存在の有無を隠すため404を返します。

OIDC mode:

```bash
export ARIADNE_AUTH_MODE=oidc
export ARIADNE_OIDC_ISSUER=https://identity.example.com/
export ARIADNE_OIDC_AUDIENCE=ariadne
export ARIADNE_OIDC_JWKS_URL=https://identity.example.com/.well-known/jwks.json
```

## Dataset登録フロー

1. `POST /api/v1/projects/{project_id}/objects` へCSV/Parquetをuploadする。
2. `POST /api/v1/datasets` で論理Datasetを作成する。
3. `POST /api/v1/datasets/{dataset_id}/versions` で1つ以上のobjectを不変versionへ束ねる。
4. workerが各tableのprofileを生成する。
5. preview/profile/visualization query APIで確認する。

既存`load.yaml`は`POST /api/v1/datasets/import-registry`でimportできます。YAMLだけから
server filesystemを読み取ることは許さず、各logical tableにupload済みObject Referenceを
明示的に対応付けます。RDA/RDSはComplete Journey ETLのraw input objectとして登録でき、
preview/profileはCSV/Parquetに限定されます。

## ConfigurationとRun

Configurationは論理resourceと不変versionに分かれます。YAMLまたはcanonical JSONを
versionとして登録し、validate後にpublishします。`RUN`はpublished versionだけを参照し、
`DRY_RUN`と`VALIDATE_ONLY`はstage codeを実行しません。

Run作成では`Idempotency-Key` headerを利用できます。同一Project・同一key・同一requestは
既存Runを返し、異なるrequestでkeyを再利用すると409になります。

Pipeline stageのinput名は既存runnerとの接続上、次を使用します。

| stage | configuration input |
|---|---|
| DISCOVERY | `analysis_config`, `feature_config` |
| INFERENCE | `analysis_config`または`config`, `feature_config`, `feature_semantics`, `causal_design` |

Dataset input、Artifact input、runtime parametersはそれぞれ別のmappingで指定します。
`DISCOVERY -> INFERENCE` dependencyではworkerが上流Artifact IDを下流inputとlineageへ固定します。

## 可視化query

小規模objectは同期処理し、`ARIADNE_QUERY_ASYNC_THRESHOLD_BYTES`を超えるobject、
または`force_async=true`のqueryは202とquery IDを返します。filterは構造化operatorだけを許し、
任意SQLを受け付けません。sampling method、size、seed、scan bytes、engine version、cache hitを
結果へ記録します。CSV、簡易PNG、Visualization Specification JSONをexportできます。

Column Policyでpreview/analysis/download、mask、PII/RESTRICTEDのminimum group countを設定できます。

## Artifact Store

既定のlocal adapter:

```bash
export ARIADNE_ARTIFACT_BACKEND=LOCAL
export ARIADNE_ARTIFACT_ROOT=/srv/ariadne/objects
```

S3互換adapter:

```bash
export ARIADNE_ARTIFACT_BACKEND=S3
export ARIADNE_S3_BUCKET=ariadne-artifacts
export ARIADNE_S3_ENDPOINT_URL=https://s3.example.com  # AWS S3では省略可
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
```

Azure Blob adapter:

```bash
export ARIADNE_ARTIFACT_BACKEND=AZURE_BLOB
export ARIADNE_AZURE_BLOB_CONTAINER=ariadne-artifacts
export ARIADNE_AZURE_STORAGE_CONNECTION_STRING='DefaultEndpointsProtocol=...'
```

connection stringの代わりに`ARIADNE_AZURE_STORAGE_ACCOUNT_URL`と
`ARIADNE_AZURE_STORAGE_CREDENTIAL`も指定できます。S3/Azure Blob objectは
worker-local cacheへmaterializeしてから既存path型runnerへ渡します。

Application/APIではobjectを`backend`、`namespace`、`key`、任意の`version`からなる
`ArtifactLocation`で扱います。`namespace`はS3ではbucket、Azure Blobではcontainerです。
adapter factoryはregistryであり、既存factoryの条件分岐を変更せずbackendを登録できます。

## 主なenvironment variable

| variable | default |
|---|---|
| `ARIADNE_DATABASE_URL` | `.ariadne/metadata.db`のSQLite URL |
| `ARIADNE_ARTIFACT_ROOT` | `.ariadne/objects` |
| `ARIADNE_WORKSPACE_ROOT` | `.ariadne/workspaces` |
| `ARIADNE_ARTIFACT_BACKEND` | `LOCAL` |
| `ARIADNE_AZURE_BLOB_CONTAINER` | Azure Blob利用時は必須 |
| `ARIADNE_AZURE_STORAGE_CONNECTION_STRING` | Azure Blob接続情報 |
| `ARIADNE_AUTH_MODE` | `development` |
| `ARIADNE_QUERY_ASYNC_THRESHOLD_BYTES` | `100000000` |
| `ARIADNE_QUERY_MAX_RESULT_ROWS` | `10000` |
| `ARIADNE_QUERY_MAX_SAMPLE_ROWS` | `50000` |
| `ARIADNE_WORKER_LEASE_SECONDS` | `300` |

## 科学的な表示上の制約

- Discovery graphは真のDAGと断定しない。
- Edge Weightは`EXPLORATORY_EDGE_COEFFICIENT`として扱う。
- Treatment EffectではATE/ATT、調整集合、仮定、balance/overlap等の診断を同時に確認する。
- assumptionは利用者による宣言・評価であり、システムによる証明ではない。
- samplingまたは近似を使用した集計はexact集計と区別する。
