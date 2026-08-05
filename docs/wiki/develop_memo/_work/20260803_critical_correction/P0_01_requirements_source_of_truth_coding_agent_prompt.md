# Coding Agent Prompt: P0 要件正本の矛盾解消

## 目的

Ariadneの要件文書間に存在する、CLIとWeb/APIのExecution ID方針および実行管理責務の矛盾を解消し、単一の規範的な要件体系へ整理してください。

現在、少なくとも次の2方針が競合しています。

### 方針A

要件定義書v1.3には、CLIとWeb APIを同一Application Serviceへの別Adapterとして共存させ、両Adapterが単一のExecution集約と`execution_id`を共有する旨の記述があります。

### 方針B

「Execution管理とMLflow実験追跡の責務分離」文書には、次の記述があります。

- CLIおよび実験用entry pointではAriadne Executionを作成しない
- CLIはMLflow Runのみを使用する
- CLIでは`execution_id = None`
- CLIの主IDは`mlflow_run_id`
- Web/API経由ではAriadne ExecutionとMLflow Runの両方を作成し、関連付ける

この2方針は、CLIがAriadne Executionを作るか否かについて両立しません。コーディングエージェントは、文書を機械的に統合するのではなく、実装、test、migration、API契約、後方互換性、MLflow責務分離を調査した上で、正本を一つに定め、関連文書を一貫して更新してください。

## 作業前に参照するファイル

最初に、少なくとも以下を全文確認してください。配置が異なる場合はrepository検索で特定してください。

- `ariadne/docs/wiki/requirement_definition/01_web_service_requirements_v1.3.md`
- `ariadne/docs/wiki/requirement_definition/02_data_model_definition_v1.4.md`
- Execution語彙へ改訂済みのデータモデル定義書がある場合は最新版
- `Execution管理とMLflow実験追跡の責務分離.md`
- README
- CLI利用方法
- API仕様
- reproducibility文書
- MLflow設定文書
- `ariadne/src/ariadne/interfaces/cli/`
- `ariadne/src/ariadne/interfaces/api/`
- `ariadne/src/ariadne/application/run_execution/`
- `ariadne/src/ariadne/application/ports/`
- `ariadne/src/ariadne/infrastructure/tracking/`
- `ariadne/src/ariadne/workers/`
- `ariadne/src/ariadne/domain/metadata.py`
- CLI test、API test、Worker test、MLflow test
- `experiments/004_discovery_inference_integration/run.py`

## 最初に行う調査

変更前に、次を事実として整理してください。

1. CLI実行時にAriadne Metadata DBへ接続しているか
2. CLI実行時に`Execution` rowを作成しているか
3. CLI Bootstrap、Planner、RunnerのどこでIDが生成されるか
4. CLIが独自UUIDを生成している箇所
5. CLIがMLflow Runを開始する箇所
6. Web/APIが`Execution`を作成する箇所
7. WorkerがMLflow Runを開始・再利用する箇所
8. `ExecutionIdentity`または同等型の有無
9. `ExperimentTracker` Port、MLflow Adapter、Null Trackerの有無
10. testが前提としているID体系
11. public CLIの既存optionと後方互換要件
12. `run_id`がAriadne ID、MLflow ID、表示名のどれとして使われているか

各`run_id`について、名前空間を分類してください。分類不能なものを推測で改称してはなりません。

## 正本方針

本作業では、以下を規範方針として採用してください。

### Web/API実行

- Ariadne Executionを作成する
- Ariadneの正式な主IDは`execution_id`
- 実処理開始時にWorkerがMLflow Runをensureする
- Web実行では`execution_id`と`mlflow_run_id`を相互に関連付ける
- API受付時点では原則としてMLflow Runを作成しない
- `DRY_RUN`および`VALIDATE_ONLY`では原則としてMLflow Runを作成しない

### CLIおよび実験用entry point

- Ariadne Executionを作成しない
- Ariadne Metadata DBを実行管理のために要求しない
- 科学実験の主IDはMLflowが採番する`mlflow_run_id`
- MLflow無効時は`mlflow_run_id = None`を許容する
- PlannerまたはRunnerが擬似Ariadne Execution IDや擬似MLflow IDを生成してはならない
- 共通処理に識別contextが必要な場合、名前空間を明示したidentity objectを使用する

### 共通識別context

必要に応じて、次と同等の意味を持つ型を使用してください。既に同等型がある場合は重複作成せず統合してください。

```python
@dataclass(frozen=True)
class ExecutionIdentity:
    origin: Literal["CLI", "WEB"]
    execution_id: str | None
    mlflow_run_id: str | None
    primary_namespace: Literal["MLFLOW", "ARIADNE", "NONE"]
    primary_id: str | None
```

不変条件:

- `origin == "WEB"`では`execution_id`が必須
- Webの`RUN`実行でtracking有効なら`mlflow_run_id`を最終的に関連付ける
- `origin == "CLI"`では`execution_id is None`
- CLIでtracking有効なら`primary_namespace == "MLFLOW"`
- CLIでtracking無効なら、擬似IDを生成せず`primary_namespace == "NONE"`を許容する
- 名前空間不明の`run_id` propertyを新規追加しない

## 必須修正

### 1. 要件定義書を正本方針へ更新する

`01_web_service_requirements_v1.3.md`または後継版を改訂し、次の記述を削除または修正してください。

- CLIとWeb APIが単一のAriadne Execution集約を共有する
- CLIとWeb APIが単一の`execution_id`を共有する
- CLI実行でAriadne Execution作成を前提とする記述

代わりに、次を明記してください。

- CLIとWebは因果分析Application Serviceを共有してよい
- ただし実行管理identityの正本は異なる
- WebはAriadne `execution_id`
- CLIはMLflow `mlflow_run_id`
- 共通Application Serviceは、Ariadne Executionの存在を常に仮定しない
- 共通処理の識別子はnamespaceを明示する

文書版を更新し、改訂履歴に矛盾解消内容を記載してください。

### 2. データモデル設計書を責務境界へ整合させる

データモデル設計書では、次を明記してください。

- `execution` tableはWeb/APIの実行オーケストレーションを管理する
- CLI科学実験は原則として`execution` rowを作成しない
- `execution_id`はAriadne namespaceのID
- `mlflow_run_id`はMLflow namespaceのID
- 名前空間不明の`run_id`は導入しない
- MLflow RunはQueue、RBAC、idempotency、lease、heartbeatの正本ではない
- Ariadne Executionは科学実験trackingの全情報を重複保持しない

実装済みschemaにMLflow列がない場合、文書だけで「実装済み」と書かないでください。要件として必要な列と、現在の実装状態を区別してください。

### 3. 責務分離文書を規範文書として整理する

「Execution管理とMLflow実験追跡の責務分離」文書について、次を行ってください。

- 正本か補足設計かを明示する
- 要件定義書との優先順位を明示する
- 同じ規則を重複して矛盾させず、要件IDまたは節への参照に置き換える
- 完了条件とtest要件を最新実装方針へ合わせる
- package/import namespace等、現在のrepositoryと一致しない例を修正する

### 4. 用語集を追加・更新する

最低限、次を定義してください。

| 用語 | 定義 |
|---|---|
| Ariadne Execution | Web実行要求、Queue、RBAC、idempotency、lease、heartbeat、cancel、retryの管理単位 |
| MLflow Run | 科学的・分析的なparams、metrics、artifacts、診断、実験比較の追跡単位 |
| `execution_id` | Ariadneが採番するExecution ID。CLIでは原則null |
| `mlflow_run_id` | MLflowが採番するRun ID |
| `run_name` | 人間向け名称。一意識別子ではない |
| Stage Execution | Ariadne Execution内のstage単位実行 |
| Stage Attempt | Stage Executionの試行履歴 |

### 5. 要件IDと受入条件を更新する

要件IDを使っている場合、少なくとも次の受入条件を追跡可能にしてください。

#### CLI

- CLI実行時にAriadne Executionを作成しない
- CLIでAriadne Metadata DBを必須としない
- tracking有効時はMLflowが`mlflow_run_id`を採番する
- PlannerとRunnerは独自IDを生成しない
- `--resume-mlflow-run-id`は既存MLflow Runの明示的再開だけに使う
- `--disable-mlflow`ではNull Trackerを使用し、擬似IDを生成しない
- 旧`--run-id`が存在する場合は、意味を特定して削除またはdeprecated化する

#### Web/API

- `POST /executions`がAriadne Executionを作成する
- API responseの正式IDは`execution_id`
- Worker開始前は`mlflow_run_id`がnullであり得る
- WorkerがMLflow Runを冪等にensureする
- `DRY_RUN`と`VALIDATE_ONLY`はMLflow Runを作成しない
- retry、cancel、events、artifactsは`execution_id`を使う

#### 共通

- 名前空間不明の`run_id`が共通model、Manifest、Execution Plan、logへ新規追加されない
- log fieldは`execution_id`と`mlflow_run_id`を分離する
- secretをMLflow tag、log、Manifestへ出力しない

### 6. 実装との不一致を修正する

文書更新だけで終わらず、調査により正本方針と実装が不一致なら、必要なコードとtestを修正してください。

対象例:

- CLIがAriadne Executionを作っている
- PlannerがUUIDを生成している
- `args.run_id or config_run_id or uuid...`のようなfallbackがある
- 共通contextが非nullable `execution_id`を要求する
- CLIがMetadata DB接続を必須とする
- Web API受付時にMLflow Runを作成する
- DRY_RUNまたはVALIDATE_ONLYでMLflow Runを作成する
- Worker再実行ごとにMLflow Runを重複作成する
- `run_id`がAriadne IDとMLflow IDの両方の意味で使われる

ただし、今回の主目的は要件正本の矛盾解消です。無関係な大規模refactorは避けてください。

## 後方互換性

- 既存CLI invocationを調査する
- public option変更時はdeprecated期間または明示的なmigration noteを設ける
- `--run-id`の意味が曖昧なままaliasを残さない
- 人間指定名は`run_name`または`mlflow_run_name`とし、IDと混同しない
- Web `/runs`互換aliasが必要な場合は、deprecatedであることをOpenAPIと文書へ明記する
- 新規内部コードと新規永続化はExecution語彙だけを使用する

## 禁止事項

- 文書の片方だけを削除して矛盾を隠さない
- 実装調査なしに方針を断定しない
- `run_id`を一括置換してMLflow SDKの正式用語まで壊さない
- CLIに不要なMetadata DB依存を追加しない
- MLflowをQueue、RBAC、idempotency、lease、heartbeatの正本にしない
- tracking無効時に擬似MLflow IDを生成しない
- WebのAriadne `execution_id`をMLflow `run_id`で代用しない
- testを削除して整合したことにしない

## 必須test

### CLI test

- CLI実行で`Execution` rowが作成されない
- CLI実行がAriadne Metadata DBなしで動作する
- tracking有効時にMLflow IDがidentityへ注入される
- PlannerおよびRunnerがUUIDを生成しない
- tracking無効時に`execution_id`と`mlflow_run_id`がともにnullでも処理可能
- `--resume-mlflow-run-id`が指定Runだけを再開する
- 実験entry pointがCLIと同じbootstrapを使用する

### Web/API test

- `POST /executions`がExecutionを作成する
- 正式response IDが`execution_id`
- API受付時点ではMLflow Runを作成しない
- Worker開始時にMLflow Runをensureする
- DRY_RUNとVALIDATE_ONLYではMLflow Runを作成しない
- retry、cancel、events、artifactsがExecution IDで動作する

### Identity invariant test

- CLI identityにAriadne `execution_id`を設定すると失敗する
- Web identityで`execution_id`がない場合は失敗する
- 名前空間とprimary IDが矛盾する場合は失敗する
- 曖昧な`run_id` propertyがschemaへ存在しない

### Documentation consistency test

可能であれば、規範文書に対して次を自動検査してください。

- 「CLIとWebが単一のexecution_idを共有する」という禁止された記述がない
- CLIの主IDが`mlflow_run_id`と明記されている
- Webの主IDが`execution_id`と明記されている
- `Run`が残る箇所はMLflow Run、外部正式用語、deprecated aliasのいずれかである

## 期待する成果物

1. 矛盾を解消した要件定義書の改訂版
2. 整合したデータモデル設計書の改訂版
3. 整理済みのExecution／MLflow責務分離文書
4. 用語集
5. traceability matrix
6. 必要な最小限のコード修正
7. CLI、Web、Worker、identityのtest
8. migration noteまたは互換性note
9. 変更file一覧
10. 実行したtest commandと結果

## Traceability Matrixの形式

少なくとも次の列を持つ表を作成してください。

| Requirement ID | 規範要件 | 実装file | Test file | 状態 |
|---|---|---|---|---|

状態は次のいずれかに限定してください。

- Implemented
- Partially Implemented
- Not Implemented
- Not Applicable

根拠なしにImplementedとしないでください。

## 完了条件

次をすべて満たした場合のみ完了としてください。

- CLIがAriadne Executionを作るか否かについて、全規範文書が一致する
- Webの主IDが`execution_id`、CLIの主IDが`mlflow_run_id`として一貫する
- 共通Application ServiceがAriadne Executionの存在を常に仮定しない
- 名前空間不明の`run_id`が除去または分類される
- MLflow RunとAriadne Executionの責務境界が一意に定義される
- 要件、データモデル、API、CLI、Worker、testの用語が一致する
- 後方互換性またはdeprecated方針が明示される
- traceability matrixが作成される
- 関連testが成功する

## 最終報告形式

最終回答は次の順で出力してください。

1. 発見した矛盾
2. 採用した正本方針
3. 変更した規範文書
4. 実装変更
5. 後方互換性対応
6. traceabilityの要約
7. test commandと結果
8. 未解決事項とその影響

