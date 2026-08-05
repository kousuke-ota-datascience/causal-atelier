# ariadne Webサービス化 要件定義書

- 文書版: 1.4
- 基準リポジトリ: `kousuke-ota-datascience/ariadne`
- 基準ブランチ: `main`
- 初版調査日: 2026-07-18
- 改訂日: 2026-08-04
- 対象: MVPおよびMVP後の拡張

### 改訂履歴

| 版 | 日付 | 変更内容 |
|---|---|---|
| 1.0 | 2026-07-18 | `ariadne` の当時の実装に合わせて全面改訂 |
| 1.1 | 2026-07-19 | ETL変換済みデータのprofile、集計、入力前後比較、保存済み可視化、export、権限制御を追加 |
| 1.2 | 2026-07-20 | MVPの価値をAnalysis-ready Datasetから因果探索・グラフ選択・因果推論までの接続と来歴管理に再定義。ETL、複数table登録、汎用BI可視化をWeb MVP主導線から除外し、単一table入力、Feature Semantics、保存済みCausal Graph Version、Causal Design、結果診断を中心に要件を再編。既存CLI、Complete Journey ETL、既存Feature Buildは後方互換を維持することを明文化 |
| 1.3 | 2026-08-03 | 実装に合わせ、実行管理ドメインの用語を`Run`から`Execution`へ改称。API `/runs`→`/executions`、識別子`run_id`→`execution_id`、`Stage Run`→`Stage Execution`、要件ID `FR-RUN-*`→`FR-EXE-*`、状態遷移節を更新。`execution_mode`値の`DRY_RUN`/`VALIDATE_ONLY`/`RUN`、status `RUNNING`、Stage実行アダプタ`Stage Runner`、外部システムのRun IDは従来名を維持 |
| 1.4 | 2026-08-04 | **矛盾解消**: v1.3の第1節第5項に誤って記載されていた「CLIとWeb APIが単一の`Execution`集約と`execution_id`を共有する」を削除し、正規方針へ置換。CLIはAriadne Executionを作成せず、科学実験の主IDはMLflowが採番する`mlflow_run_id`とする方針を明文化。`run_label`（再現性マニフェスト用の人間指定ラベル）と`execution_id`（AriadneのWeb実行管理ID）の区別を追記。`ExecutionIdentity`共通型の導入方針を追加。 |

---

## 1. 文書の目的

本書は、Pythonパッケージとして実装されている `ariadne` を、Analysis-ready Datasetの登録、変数の意味付け、因果探索、探索結果の比較・選択、因果設計、因果推論、診断、再現性情報の管理を備えたWebサービスへ発展させるための要件を定義する。

本版では、MVPが証明すべき価値を次のように定める。

> 分析用に整備されたDataset Versionを入力すると、変数の意味付け、複数アルゴリズムによる因果探索、グラフ比較・選択、因果設計、因果推論、診断、来歴確認までを、一つのProject内で再現可能に実行できる。

本書の要件は次を原則とする。

1. ariadneは、汎用ETL基盤やData Warehouseの代替を目指さない。
2. データ収集、join、集計、Feature生成等の重いデータ整備は、Databricks等の外部データ基盤または既存パイプラインへ委譲可能とする。
3. MVPでは、1行が分析単位を表す単一のAnalysis-ready Tableを標準入力とする。
4. 因果探索・因果推論の数値実装をWeb層へ移植しない。
5. CLIを廃止せず、Web APIとCLIを同一の因果分析Application Serviceへの別Adapterとして共存させる。ただし、**実行管理identityの正本は経路によって異なる**。
   - **Web/API**: Ariadneが採番する`execution_id`が正式な実行管理IDである。Ariadne ExecutionはWeb受付時に作成する。
   - **CLI / 実験用entry point**: Ariadne Executionを作成しない。科学実験の主IDはMLflowが採番する`mlflow_run_id`である。MLflow無効時は`mlflow_run_id = None`を許容する。
   - **共通Application Service**: Ariadne Executionの存在を常に仮定してはならない。共通処理の識別contextは名前空間を明示した`ExecutionIdentity`型を使用する（FR-EXE-IDENTITY-001参照）。
   - **PlannerおよびRunner**: 擬似Ariadne execution_idおよび擬似MLflow IDを生成してはならない。
6. Dataset、Configuration、Execution、Graph、Result、Artifactを不変versionまたは不変snapshotで結び付ける。
7. 因果探索結果を真のDAG、edge weightを識別済み因果効果として表示しない。
8. 因果的妥当性を自動保証するサービスとは位置付けず、分析者の判断、宣言した仮定、診断結果を明示する。
9. 新しいAnalysis-ready実行経路は、既存CLI・ETL・Feature Build経路を置換せず、追加経路として実装する。

### 1.1. v1.1からの優先順位変更

v1.1でMVP対象としていた次の機能は、本版ではMVPの主導線から外す。

- Complete Journey固有ETL
- 複数table Datasetのブラウザからの一括登録
- ETL入力前後比較
- 汎用group-by可視化およびBI dashboard相当の機能
- Visualization Specificationの高度な管理

ここでいう「MVPの主導線から外す」とは、通常のWeb画面で利用者へ明示的な操作を要求せず、Web MVPの成功判定に含めないという意味である。既存API、CLI、ETL class、Feature Build class、Configuration、回帰テストを削除または非互換変更してよいという意味ではない。

本MVPの実装変更において、既存CLI、Complete Journey ETL、既存Discovery/Inference Feature Buildは維持必須とする。新しいAnalysis-ready modeは、それらと併存すること。

### 1.2. 規範用語

本書では次の意味で用語を使用する。

| 表現 | 意味 |
|---|---|
| 「すること」「してはならない」 | MVP必須要件 |
| 「してよい」「可能とする」 | 許容またはoptional要件 |
| 「MVP対象外」 | Web MVPの新規実装・受入判定の対象外。既存コードの削除指示ではない |
| 「Web主導線から外す」 | 通常UIに操作stepを設けない。API、worker、CLI、classを廃止する意味ではない |
| 「維持する」 | public CLI、既存API契約、import可能なclass、既存testを非互換にしない |

要件間で解釈が競合する場合、既存CLI・ETL・Feature Buildの後方互換要件を優先する。

### 1.3. 本書における「前処理」の分類

「前処理」という語を一括して扱わず、次の3種類を区別する。

| 区分 | 例 | v1.4での扱い |
|---|---|---|
| A. Domain ETL / Feature Build | RDA/RDS読込、複数table join、campaign集計、household単位Feature生成 | 既存classとCLIを維持する。通常Web UIでは利用者へ明示操作させない |
| B. Algorithm Input Conditioning | 列選択、dtype検証、欠損値policy、categorical encoding、標準化、constant列除外、collinearity check | Discovery/Inferenceの内部処理として引き続き実行し、設定と結果を記録する |
| C. Web Orchestration | Dataset Version、Semantics、Execution、Graph、Designの選択・来歴管理 | v1.4 Web MVPの中心機能とする |

Analysis-ready Datasetとは、AのDomain ETL / Feature Buildが完了しているDatasetを指す。BのAlgorithm Input Conditioningまで不要であることを意味しない。

### 1.4. 併存する2つの実行経路

実装は次の2経路を明示的に区別する。

#### CONFIGURED_FEATURE_BUILD経路

- 現行CLI、Complete Journey、既存Feature Configurationが使用する。
- Dataset Registry、既存Feature Build、既存preprocessing classを使用する。
- 本書の対応で削除、無効化、暗黙にAnalysis-ready modeへ変更してはならない。
- 既存CLI invocationでmode指定がない場合、従来と同じ挙動を維持する。

#### ANALYSIS_READY経路

- v1.4の通常Web UIが使用する新しい経路である。
- 単一のAnalysis-ready TableとFeature Semanticsを直接入力する。
- Domain固有join・集計・Feature Buildは実行しない。
- Algorithm Input Conditioningは明示設定に基づいて実行する。

Application層またはExecution Planで解決済み`input_mode`を保持すること。名称は実装設計で変更してよいが、2経路をtable数やfilenameから暗黙推測してはならない。Execution、Execution Plan、Manifestには解決済みmodeを記録すること。

---

## 7. 機能要件（Execution管理）

### FR-EXE-IDENTITY-001

CLIと実験用entry pointは、Ariadne ExecutionをDBへ作成してはならない。

受入条件:
- CLI実行時にAriadne Executionが作成されない。
- CLIはAriadne Metadata DBを実行管理のために必須としない。
- PlannerおよびRunnerは擬似Ariadne execution_idを生成しない。
- MLflow有効時はMLflowが`mlflow_run_id`を採番する。
- MLflow無効時は`execution_id`および`mlflow_run_id`がともにnullでも正常動作する。
- 旧`--run-id` optionはdeprecatedとして維持し、`--run-label`へ誘導する。
- `--execution-id` optionはCLIに存在しない。

### FR-EXE-IDENTITY-002

Web/API実行は、Ariadne Executionを必ず作成する。

受入条件:
- `POST /executions`がAriadne Executionを作成する。
- API responseの正式IDは`execution_id`である。
- Worker開始前は`mlflow_run_id`がnullであり得る。
- WorkerがMLflow Runを冪等にensureする（将来実装）。
- `DRY_RUN`および`VALIDATE_ONLY`モードはMLflow Runを作成しない。
- retry、cancel、events、artifactsは`execution_id`で解決する。

### FR-EXE-IDENTITY-003

共通処理に識別contextが必要な場合、`ExecutionIdentity`型を使用し、名前空間を明示する。

```python
@dataclass(frozen=True)
class ExecutionIdentity:
    origin: Literal["CLI", "WEB"]
    execution_id: str | None   # Ariadne Execution ID（WEB必須、CLI常にNone）
    mlflow_run_id: str | None  # MLflow Run ID（CLIで有効時、WEB Worker開始後）
    primary_namespace: Literal["MLFLOW", "ARIADNE", "NONE"]
    primary_id: str | None
```

不変条件:
- `origin == "WEB"`では`execution_id`が必須
- `origin == "CLI"`では`execution_id is None`
- CLIでtracking有効なら`primary_namespace == "MLFLOW"`
- CLIでtracking無効なら`primary_namespace == "NONE"`（擬似IDを生成しない）
- 名前空間不明の`run_id`プロパティを共通モデルへ新規追加しない

### FR-EXE-MANIFEST-001

CLI再現性マニフェストに記録する識別情報は`run_label`とする。

`run_label`は人間が指定するラベルであり、Ariadne execution_idではない。

- CLIオプション: `--run-label`（`--run-id`はdeprecated alias）
- 未指定時は`run_label: null`をマニフェストへ記録する（擬似IDを生成しない）
- 旧マニフェストの`execution_id`または`run_id`フィールドは後方互換として受理する

---

## 8. 後方互換性

### FR-COMPAT-001

次の後方互換を維持する。

- 既存CLI invocationの`--run-id`オプションは引き続き動作する（`--run-label`のdeprecated alias）
- `--execution-id` CLIオプションは削除済み。旧スクリプトを更新する必要がある
- 旧マニフェストファイルの`execution_id`フィールドはValidation時に`run_label`として読み込む
- Web API `/executions`の`execution_id`は変更しない
- Web API deprecated互換 `/runs`を提供する場合は、OpenAPIにdeprecatedであることを明記する

---

以降のセクション（2〜6、8〜17）はv1.3から継続する。本版での変更は第1節および第7節（FR-EXE-IDENTITY-*、FR-EXE-MANIFEST-001、FR-COMPAT-001）の追加・修正のみである。

> **参照先**: 完全な機能要件一覧はv1.3の各セクションを参照すること。本版は矛盾解消と新規要件の追加のみを行い、v1.3の他の要件は継承する。
