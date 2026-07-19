# `20260719_prompt_memo_02.md`への回答

以下は現状コードを読み取った結果と修正候補である。

## 1. ディレクトリ構成

### 1.1. `frontend/`の責務

結論として、現状の`frontend/`をリポジトリ直下に置く構成は妥当である。`src/causal_atelier`配下へ移す必要はない。

理由は、要件上FrontendがAPIとは別のデプロイ単位だからである。現在もNginxから配信され、Python wheelには含まれない。

| ファイル | 責務 |
|---|---|
| `frontend/index.html` | 画面のHTML構造、Project一覧・作成dialog |
| `frontend/styles.css` | レイアウト、配色、レスポンシブ表示 |
| `frontend/app.js` | API呼び出し、Project取得・作成、DOM更新 |
| `deploy/nginx.conf` | 静的ファイル配信、`/api/`のreverse proxy |
| `compose.yaml` | Frontend/API/Worker/DBのデプロイ構成 |

`src/causal_atelier`配下が適切になるのは、FrontendをFastAPIが同一process・同一Python packageから配信する場合である。その場合は、例えば次の配置が考えられる。

```text
src/causal_atelier/interfaces/web/static/
```

しかし現在は独立Frontendなので、次のいずれかが自然である。

```text
frontend/       # 現状。十分妥当
web/
apps/frontend/  # 将来monorepo化する場合
```

現在の責務に対しては、`frontend/`のままが最も分かりやすい。

## 1.2. `application/`の構成

### 現状の責務

`application/`直下のコードはCLI専用ではない。

| ファイル・ディレクトリ | 責務 |
|---|---|
| `application/planning.py` | Discovery→InferenceのExecution Plan生成 |
| `application/execution.py` | `StageRunner`契約とstage実行 |
| `application/strategies.py` | `DRY_RUN`、`VALIDATE_ONLY`、`RUN`戦略 |
| `application/validation.py` | cross-stage validation |
| `application/discovery_pipeline.py` | Discovery Stage Runner |
| `application/inference_pipeline.py` | Inference Stage Runner |
| `application/etl_pipeline.py` | Complete Journey ETL Application Service |
| `application/end_to_end_pipeline.py` | 統合pipeline facade |
| `application/ports/` | Application層が要求する外部機能の抽象契約 |
| `application/web/services.py` | Dataset、Configuration、Runのtransactional use case |
| `application/web/visualization.py` | 可視化query完了処理、small-cell suppression |

したがって、次の構成は推奨しない。

```text
application/
  cli/
  web/
```

CLIとWebはApplication Serviceの呼び出し側であり、すでに次の場所で分離されている。

```text
interfaces/
  cli/
  api/
```

Application層をインターフェイス別に分けると、CLIとWebで同じuse caseを再利用する設計に反する。

### 現状の問題点

一方、`application/web`という名前も適切ではない。

実際にはAPIだけでなく、`workers/executor.py`も`DataCatalogService`、`RunService`、可視化完了処理を使用している。

つまり、これらは「Web用」ではなく、Control Plane・Data Catalog・Run管理のApplication Serviceである。

規模が拡大するなら、インターフェイスではなくuse case単位に整理する方が適切である。

```text
application/
  pipeline/
    planning.py
    execution.py
    strategies.py
    validation.py
    discovery.py
    inference.py
    etl.py

  data_catalog/
    services.py

  configuration_catalog/
    services.py

  run_execution/
    services.py

  visualization/
    services.py

  ports/
    artifact_store.py
    data_query.py
    metadata_repository.py
    unit_of_work.py
    event_queue.py
```

`common/`は推奨しない。何でも入るディレクトリになりやすいためである。共有物には、責務を表す名前を付ける方が安全である。

```text
application/validation/
application/hashing/
application/events/
shared/
```

### 判定

- `application/`直下の既存pipelineコードはCLI専用ではないため、`application/cli`へ移すべきではない。
- `application/web`はworkerも利用しているため、名称として不正確である。
- 現状でも呼び出しは成立するが、今後拡張するならuse case単位への再編を推奨する。
- `common/`による分類は避ける。

## 1.3. その他のレイヤ不一致

### Application層がInfrastructureへ直接依存している

最も大きな不一致である。

`application/web/services.py`は以下へ直接依存している。

- SQLAlchemy `Session`
- SQLAlchemy永続化model
- 具体的な`PyArrowQueryEngine`

`application/web/visualization.py`もSQLAlchemy modelを直接更新している。

現在の依存方向は次のとおりである。

```text
Application
  └─ Infrastructure persistence / PyArrow
```

本来は次が望ましい構造である。

```text
Application
  └─ Ports
       ├─ MetadataRepository
       ├─ UnitOfWork
       └─ DataQueryPort

Infrastructure
  └─ Portsの実装
```

`ArtifactStore`だけはport化されているが、DBとData Queryは未分離である。

### API RouterがPersistence modelを直接操作している

`interfaces/api/routers/`は、多くの箇所でSQLAlchemy modelを直接検索・更新している。

```text
HTTP Router
  └─ SQLAlchemy model
```

これにより、認可・transaction・domain ruleがRouterとApplication Serviceへ分散している。

理想形は次である。

```text
Router
  └─ Application Use Case
       └─ Repository / UnitOfWork Port
```

### `workers/executor.py`の責務が大きい

現在のWorkerは次を同時に担当している。

- Outbox claim
- Run/Stage/Attempt状態遷移
- workspace materialization
- ETL/Discovery/Inference実行
- Artifact upload
- Manifest生成
- lineage生成
- result projection
- profile生成
- 可視化query実行

Execution Planeの入口を`workers/`とすること自体は、独立デプロイ単位なので妥当である。しかし、`executor.py`内部は分割余地がある。

```text
workers/
  main.py
  outbox_consumer.py

application/
  run_execution/
  materialization/
  artifact_registration/
  result_projection/
  profiling/
```

### `infrastructure/artifacts`と`artifact_store`の名称が近い

現在は次の2つが存在する。

```text
infrastructure/artifacts/
  registry.py

infrastructure/artifact_store/
  local.py
  s3.py
```

責務は異なる。

- `artifacts/registry.py`: 旧CLI用のArtifact計画・Manifest helper
- `artifact_store/`: objectの物理保存adapter

ただし名前だけでは区別しづらいため、将来的には例えば以下が明確である。

```text
application/artifacts/manifest.py
infrastructure/object_store/
```

### 問題のない配置

以下は現在の配置が妥当である。

- `migrations/`: Python packageではなくDB運用資材
- `deploy/`: Nginx等のデプロイ設定
- `interfaces/cli`: CLI adapter
- `interfaces/api`: HTTP adapter
- `infrastructure/auth`: OIDC/JWT adapter
- `infrastructure/data_query`: PyArrow実装
- `infrastructure/persistence`: SQLAlchemy実装
- `causal/`、`etl/`、`preprocessing/`: 分析・変換ロジック

## 2. Azure Blob・Databricks等への拡張

### Azure Blob

拡張可能である。

現在の`application/ports/artifact_store.py`にある`ArtifactStore Protocol`は以下を要求する。

```python
put_file(...)
put_stream(...)
resolve_local_path(...)
open(...)
```

Azure adapterは、例えば次の形で実装できる。

```text
infrastructure/artifact_store/
  local.py
  s3.py
  azure_blob.py
```

`resolve_local_path()`でBlobをworker-local cacheへdownloadすれば、既存のpathベースの分析runnerを変更せず接続できる。

ただし、現在は次の箇所が`LOCAL/S3`を固定的に列挙しているため、adapterファイルを追加するだけでは完了しない。

- Artifact Store factory
- `WebSettings`
- HTTPの`ObjectReference.backend`
- Stored Objectのbackend値
- Azure container/account設定
- Azure SDK dependency

### Databricks

接続対象によって設計が異なる。

#### Unity Catalog Volume等をArtifact保存先として使う場合

Artifact Store adapterとして実装できる。

```text
infrastructure/artifact_store/databricks_volume.py
```

Volume上のfileをworker workspaceへmaterializeすれば、現在のProtocolに合わせられる。

#### Delta TableやDatabricks SQLを分析入力として使う場合

これはArtifact Storeではなく、Data Query / Dataset Sourceの責務である。

```text
infrastructure/data_query/
  pyarrow_engine.py
  databricks_sql.py

infrastructure/dataset_source/
  databricks_delta.py
```

Delta Tableを無理に`object_key`を持つArtifactとして扱うと、table version、snapshot、time travel、catalog/schema/tableといった概念を失う。

その場合は、Dataset Table Versionへ例えば次の参照形式が必要である。

```text
backend: DATABRICKS_DELTA
catalog: ...
schema: ...
table: ...
table_version: ...
```

### 現在の拡張性に関する評価

現在の設計は「新adapterを実装できる」状態だが、「設定だけで任意adapterを追加できるplugin構造」ではない。

特に以下はS3寄りである。

```python
backend
bucket
object_key
```

AzureのcontainerやGCSのbucketへは対応付けられるが、名称が特定基盤寄りである。

より一般化するなら、次のようなlocatorが適切である。

```python
ArtifactLocation(
    backend="AZURE_BLOB",
    namespace="container-name",
    key="path/to/object",
    version="...",
)
```

またfactoryを条件分岐ではなくregistry化すると拡張しやすくなる。

```python
ARTIFACT_STORE_FACTORIES = {
    "LOCAL": build_local,
    "S3": build_s3,
    "AZURE_BLOB": build_azure_blob,
    "DATABRICKS_VOLUME": build_databricks_volume,
}
```

## 推奨順位

修正する場合の優先順位は次のとおりである。

1. `application/web`をuse case単位の名称へ変更する。
2. API RouterからSQLAlchemy操作をApplication Serviceへ移動する。
3. Metadata Repository、Unit of Work、Data Queryのportを追加する。
4. `workers/executor.py`を状態管理・materialization・projectionへ分割する。
5. `ArtifactLocation`を導入して`bucket`依存を弱める。
6. Artifact Store factoryをregistry化する。
7. 必要に応じてAzure BlobまたはDatabricks adapterを追加する。

`frontend/`は現状維持で問題ない。変更するならApplication層とInfrastructure境界の整理を優先すべきである。
