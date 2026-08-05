# P1-02: 因果探索CLIの責務分離

## 0. コーディングエージェントの役割

あなたは、Python、Clean Architecture、Hexagonal Architecture、依存性逆転、CLI設計、Application Service、データパイプライン、因果探索システムに精通したシニアソフトウェアエンジニアである。

Ariadneの因果探索CLIをリファクタリングし、CLI引数解析、入力準備、データセット固有前処理、因果探索実行、診断、レポート生成、Artifact永続化の責務を明示的かつ差し替え可能な形に分離せよ。

本改修の主目的は、単に`main()`を短くすることではない。成功条件は次である。

> 新しい入力データ種別を追加する際に、CLI、Pipeline Runner、Discovery Application Service、因果探索アルゴリズム実装を変更する必要がないこと。

Complete JourneyはCLIにハードコードされた唯一のworkflowではなく、汎用的なDiscovery Input Provider契約の一実装として扱うこと。

---

## 1. 主対象

```text
ariadne/src/ariadne/interfaces/cli/discovery.py
```

変更前に、以下の関連領域を調査すること。

```text
ariadne/src/ariadne/application/
ariadne/src/ariadne/application/pipeline/
ariadne/src/ariadne/causal/discovery/
ariadne/src/ariadne/preprocessing/
ariadne/src/ariadne/etl/
ariadne/src/ariadne/infrastructure/
ariadne/src/ariadne/interfaces/cli/
ariadne/src/ariadne/workers/
ariadne/tests/
```

少なくとも以下の既存コンポーネントと全呼び出し元を確認すること。

```text
DiscoveryStageRunner
LogicalTableDataLoader
CompleteJourneyPreprocessor
CausalDiscovery
CausalDiscoveryDiagnostics
CausalDiscoveryReporter
load_analysis_config
load_feature_config
merge_cli_overrides
write_resolved_config
FeatureSemanticsCatalog
ExecutionPlan
StagePlan
ArtifactRegistry
RunManifest
```

既存クラス名、ファイル配置、Repository interface、transaction境界、Factory規約、Test規約を推測で決めてはならない。最初にrepositoryを検索し、妥当な既存規約があれば従うこと。

---

## 2. 現状の問題

現行の`interfaces/cli/discovery.py::main()`は、以下を一括して実行している。

1. CLI引数解析
2. Project Root解決
3. 設定ファイルpath解決
4. Analysis Config読込
5. Feature Config読込
6. CLI override適用
7. Dataset Registry解決
8. Output directory解決
9. `LogicalTableDataLoader`生成
10. Source table読込
11. `CompleteJourneyPreprocessor`生成
12. Complete Journey固有前処理
13. `CausalDiscovery`生成
14. 因果探索アルゴリズム実行
15. resolved config出力
16. diagnostics生成
17. report／Artifact出力
18. summary DataFrame生成
19. CLI標準出力

また、現行の`DiscoveryStageRunner`はCLI Adapterを直接呼び出している。

```python
from ariadne.interfaces.cli.discovery import main as discovery_main

discovery_main(stage_plan.resolved_args)
```

現行の依存方向:

```text
Application Pipeline Runner
  -> CLI Adapter
      -> Data Loader
      -> Complete Journey Preprocessor
      -> Discovery Algorithm
      -> Reporter
```

目標の依存方向:

```text
CLI --------------------\
Pipeline Stage Runner ----> DiscoveryApplicationService
Worker -----------------/
                            |
                            +-> DiscoveryInputProvider
                            +-> DiscoveryBackend
                            +-> DiscoveryArtifactWriter
```

Application LayerからCLI Layerへ依存してはならない。

---

## 3. アーキテクチャ要件

### 3.1 Thin CLI Adapter

`interfaces/cli/discovery.py`は原則として以下のみを担当すること。

- parser構築
- CLI引数解析
- Application Requestへの変換
- Composition RootまたはFactoryからApplication Serviceを取得
- Application Service実行
- CLI向けsummary表示
- exit code返却

CLI moduleから以下を直接importしてはならない。

```text
pandas
LogicalTableDataLoader
CompleteJourneyPreprocessor
CausalDiscovery
CausalDiscoveryDiagnostics
CausalDiscoveryReporter
```

目標形:

```python
def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    request = discovery_request_from_args(args)
    service = build_discovery_application_service(request.project_root)
    result = service.execute(request)
    print_discovery_summary(result)
    return 0
```

名称とreturn規約はrepositoryの既存規約に合わせること。

### 3.2 Discovery Application Service

因果探索use caseを表すApplication LayerのServiceを導入または再利用すること。概念上の推奨名:

```python
DiscoveryApplicationService
```

担当する処理:

1. Input Provider解決
2. 入力準備
3. 探索前validation
4. Discovery Backend実行
5. diagnostics生成または委譲
6. report／Artifact生成の委譲
7. 結果DTO生成

以下を知ってはならない。

- `argparse`または`Namespace`
- stdout formatting
- Complete Journey固有table名
- campaign固有の加工詳細
- Local filesystem固有の保存方法
- causal-learn等の外部library固有型

### 3.3 依存性逆転

同等の既存Portがない場合、Application Layerに以下に相当するPortを定義すること。

```python
class DiscoveryInputProvider(Protocol):
    def prepare(
        self,
        specification: DiscoveryInputSpecification,
    ) -> PreparedDiscoveryInput:
        ...


class DiscoveryBackend(Protocol):
    def discover(
        self,
        prepared_input: PreparedDiscoveryInput,
        specification: DiscoverySpecification,
    ) -> DiscoveryBackendResult:
        ...


class DiscoveryArtifactWriter(Protocol):
    def write(
        self,
        request: DiscoveryRequest,
        prepared_input: PreparedDiscoveryInput,
        discovery_result: DiscoveryBackendResult,
    ) -> DiscoveryArtifactResult:
        ...
```

同等の既存Portを拡張できる場合は、重複する抽象を新設しないこと。

---

## 4. 共通Application DTO

CLI、Pipeline Runner、Workerから共通利用できるimmutableかつtypedなDTOを導入すること。

### 4.1 DiscoveryRequest

最低限、以下に相当する情報を表現すること。

```python
@dataclass(frozen=True)
class DiscoveryRequest:
    project_root: Path
    input_specification: DiscoveryInputSpecification
    discovery_specification: DiscoverySpecification
    reporting_specification: DiscoveryReportingSpecification
    output_specification: DiscoveryOutputSpecification
```

実際の実装はrepositoryのdataclass／Pydantic規約に合わせること。

### 4.2 PreparedDiscoveryInput

すべてのInput Providerは、データソース固有の入力を以下に相当する共通契約へ正規化すること。

```python
@dataclass(frozen=True)
class PreparedDiscoveryInput:
    analysis_frame: pd.DataFrame
    raw_frame: pd.DataFrame | None
    transformed_frame: pd.DataFrame | None
    variable_metadata: Mapping[str, VariableMetadata]
    background_knowledge: BackgroundKnowledge | None
    lineage: InputLineage
    diagnostics: tuple[ValidationIssue, ...]
```

要件:

- Provider固有の内部状態を漏らさない
- `campaign_id`と`pre_weeks`を共通必須fieldにしない
- reportingで不要な場合、raw／transformed frameは省略可能にする
- 既存のtable abstractionが`DataFrame`より適切なら、それを優先する

### 4.3 DiscoveryExecutionResult

以下に相当するtyped resultを返すこと。

```python
@dataclass(frozen=True)
class DiscoveryExecutionResult:
    status: str
    algorithm_results: Mapping[str, DiscoveryResult]
    artifacts: Mapping[str, ArtifactReference]
    sample_count: int
    variable_count: int
    diagnostics: tuple[ValidationIssue, ...]
    metadata: Mapping[str, Any]
```

CLI PresenterはこのDTOから表示し、workflow内部状態を再構築しないこと。

---

## 5. Input Provider

### 5.1 CompleteJourneyDiscoveryInputProvider

現行Complete Journey入力経路の組み立てをCLIから移動すること。

```text
LogicalTableDataLoader
  -> load_all()
  -> CompleteJourneyPreprocessor
  -> preprocess()
  -> PreparedDiscoveryInput
```

このProviderだけが以下を知ること。

- campaign ID
- pre-weeks
- campaigns
- campaign descriptions
- transactions
- demographics
- household aggregation
- campaign windows
- Complete Journey固有Feature Config

初期実装では`LogicalTableDataLoader`と`CompleteJourneyPreprocessor`を再利用し、数値挙動を書き換えたり不要なファイル移動を行ったりしないこと。

### 5.2 SingleTableDiscoveryInputProvider

一行が一分析単位となっている単一table向けProviderを追加すること。

既存のtable／Artifact abstractionを優先して利用する。最低限、単一CSV／Parquet、または既存Dataset Versionの単一tableに対応すること。ただし、既存コードの対応可能範囲を調査し、無理な重複実装は避けること。

責務:

- 対象table読込
- 対象列選択
- 必須列検証
- 数値互換性検証
- 欠測値policy適用
- 定数列検出
- 任意の標準化
- variable metadata生成
- background knowledge解決または生成
- `PreparedDiscoveryInput`返却

以下を要求しないこと。

- campaign ID
- pre-weeks
- campaigns table
- transactions table
- demographics table

### 5.3 Provider Registry

CLIまたはApplication Serviceに拡張し続ける`if`／`elif`分岐を追加してはならない。

以下に相当するRegistry／Factoryを使用すること。

```python
class DiscoveryInputProviderRegistry:
    def register(
        self,
        provider_type: str,
        factory: DiscoveryInputProviderFactory,
    ) -> None:
        ...

    def create(
        self,
        provider_type: str,
        context: ProviderContext,
    ) -> DiscoveryInputProvider:
        ...
```

最低限の登録対象:

```text
completejourney
single_table
```

将来候補:

```text
dataset_version
panel
time_series
external_etl
```

Provider追加時にCLI、Application Service、Discovery Backend、Stage Runnerを変更しなくてよい構造にすること。

Providerはallowlist registryで解決し、利用者が指定したPython class pathを動的importしてはならない。

---

## 6. 設定分離と後方互換性

Input Provider設定と共通Discovery設定を分離すること。

新形式の概念例:

```yaml
input:
  provider: completejourney
  options:
    dataset_yaml: configs/etl/completejourney/load.yaml
    campaign_id: "18"
    pre_weeks: 8
```

Single Table例:

```yaml
input:
  provider: single_table
  options:
    dataset_version_id: "..."
    table: analysis_table
    unit_id: household_id
    columns:
      - age
      - income
      - treated
      - outcome_sales_value
    missing_values: fail
    standardization: zscore
```

以下の既存設定との後方互換性を維持すること。

```text
dataset.yaml_path
run.campaign_id
run.pre_weeks
```

legacy設定をComplete Journey Provider向け設定へ変換するcompatibility mapperを追加すること。意味を黙って変更してはならない。

非推奨化する場合は明確なwarningを出し、既存CLI、YAML、Test、output path、Artifactを壊さないこと。

推奨優先順位:

```text
明示的CLI override
  > provider/input設定
  > legacy compatibility mapping
  > default
```

この優先順位を文書化し、Testで固定すること。

---

## 7. Discovery SpecificationとBackend

現行`CausalDiscovery` constructorは多数の個別設定値を受け取る。既存typed configとの重複を生じない範囲で、設定オブジェクトへの整理を検討すること。

概念例:

```python
@dataclass(frozen=True)
class DiscoverySpecification:
    algorithms: tuple[str, ...]
    pc: PCSpecification
    ges: GESSpecification
    lingam: LiNGAMSpecification
    notears: NOTEARSSpecification
    bootstrap: BootstrapSpecification
    random_seed: int
```

Complete JourneyのFeature Config全体を汎用Discovery Backendへ渡してはならない。Backendが受け取るのは原則として以下に限定すること。

- 準備済み分析行列
- 探索に必要なvariable metadata
- 正規化済みbackground knowledge
- algorithm設定
- diagnostics設定

既存`CausalDiscovery`の数値実装は維持すること。既存クラス自体がBackend契約を満たせない場合は、以下のような薄いAdapterを追加すること。

```python
class CausalLearnDiscoveryBackend(DiscoveryBackend):
    ...
```

Backendは以下を知ってはならない。

- CLI引数
- Project Root探索
- Dataset YAML path
- Complete Journey
- output directory
- report形式
- Artifact Store

本改修ではPC、GES、LiNGAM、NOTEARSの数値挙動を変更しないこと。

---

## 8. ReportingとArtifact

以下をCLI orchestrationから分離すること。

- resolved config出力
- retained columns計算
- raw／transformed／standardized frame出力
- variable metadata出力
- algorithm別edge出力
- diagnostics出力
- summary Artifact生成

必要に応じて以下へ分離すること。

```text
DiscoveryReportRenderer
  -> structured report、bytes、生成file

DiscoveryArtifactWriter
  -> 既存Artifact Storeへ保存
  -> ArtifactReferenceを返却
```

RendererはLocal、S3、Azure Blobの違いを知らないこと。Artifact Writerは因果探索計算を行わないこと。

`CausalDiscoveryReporter`は削除せず、Adapter内部から再利用すること。

以下を含む既存Artifact名とManifest契約を維持すること。

```text
pc/edges.csv
ges/edges.csv
lingam/edges.csv
notears/edges.csv
pc/edge_stability.csv
resolved_analysis_config.yaml
resolved_features_config.yaml
resolved_feature_semantics.yaml
```

---

## 9. DiscoveryStageRunner

CLI Adapterへの依存を除去すること。

最終形で禁止する依存:

```python
from ariadne.interfaces.cli.discovery import main
```

目標概念:

```python
class DiscoveryStageRunner:
    def __init__(
        self,
        service: DiscoveryApplicationService,
    ) -> None:
        self._service = service

    def run(
        self,
        stage_plan: StagePlan,
    ) -> StageExecutionResult:
        request = discovery_request_from_stage_plan(stage_plan)
        result = self._service.execute(request)
        return stage_result_from_discovery_result(result)
```

既存Stage Runner interfaceに従うこと。CLI、Integrated Pipeline、Workerは同一Application Serviceを使用すること。

---

## 10. Composition Root

既存のFactory、Dependency Container、FastAPI dependency、Worker bootstrap、Registry moduleを調査すること。

既存規約があれば利用する。存在しない場合は、以下に相当するfocused factoryを追加すること。

```python
def build_discovery_application_service(
    project_root: Path,
) -> DiscoveryApplicationService:
    ...
```

mutable global singleton、Providerの重複登録、Test間の状態汚染を回避すること。

---

## 11. CLI後方互換性

以下の既存optionと意味を維持すること。

```text
--project-root
--analysis-config
--feature-config
--dataset-yaml
--campaign-id
--pre-weeks
--alpha
--pc-indep-test
--alpha-grid
--bootstrap-samples
--bootstrap-sample-fraction
--random-seed
--pc-discrete-bins
--collinearity-threshold
--no-background-knowledge
--output-dir
--algorithms
--notears-threshold
```

必要なら以下を追加する。

```text
--input-provider
```

以下のsummary情報を維持すること。

- sample count
- variable count
- conditional-independence test
- bootstrap sample count
- output directory
- algorithm別summary

表示組み立てはPresenterまたはpure formatting functionへ分離すること。

---

## 12. エラーモデル

以下を区別し、正規化すること。

- CLI argument error
- configuration error
- unsupported input provider
- input validation error
- preprocessing error
- discovery backend error
- reporting error
- artifact persistence error

Ariadneの既存例外抽象がある場合、Application境界から外部library固有例外を漏らさないこと。

一つの探索algorithmが失敗しても他algorithmを継続する現行挙動がある場合は維持すること。Input preparation失敗時は探索開始前に停止すること。

---

## 13. 段階的な実装手順

### Step 1: Characterization Test

以下の現行挙動をTestで固定する。

- argument parsing
- CLI override
- output path
- stdout summary
- Complete Journey workflow
- algorithm別Artifact
- resolved config
- failure behavior

### Step 2: Application Service抽出

`main()`からworkflow orchestrationをApplication Serviceへ移す。この段階ではComplete Journey専用でもよい。

### Step 3: DTO導入

Request、Prepared Input、Execution Result、Artifact Resultを追加する。

### Step 4: Complete Journey Provider抽出

LoaderとPreprocessorの組み立てをProviderへ移す。

### Step 5: Stage RunnerからCLI依存を除去

Stage RunnerがApplication Serviceを直接呼び出すようにする。

### Step 6: Single Table Provider追加

単一の分析ready tableからDiscoveryを実行可能にする。

### Step 7: Provider Registry追加

Registry／FactoryからProviderを解決する。

### Step 8: Architecture文書更新

CLI利用方法、Provider設定、依存方向、新Provider追加方法を文書化する。

各Stepの後にTest Suiteを実行する。必要な場合を除き、構造変更と挙動変更を同時に行わないこと。

---

## 14. Test要件

### 14.1 Unit Test

以下を追加すること。

- CLI argsから`DiscoveryRequest`へのmapping
- 設定優先順位
- legacy設定mapping
- Provider Registry
- unsupported provider
- Complete Journey Provider
- Single Table Provider
- input validation
- Application Service orchestration
- Artifact Writer
- CLI Presenter
- error normalization

### 14.2 Component Test

以下を追加すること。

- 既存前処理を利用したComplete Journey Provider
- Single Table ProviderからDiscovery実行
- Discovery Backend Adapter
- Reporter Adapter
- Local Artifact Writer

### 14.3 CLI Test

以下を確認すること。

- 既存Complete Journey commandが有効
- Single Table Providerを選択可能
- invalid providerに明確なerror
- invalid inputに明確なerror
- summaryとexit codeが正しい

### 14.4 Pipeline Test

以下を確認すること。

- `DiscoveryStageRunner`がCLIを呼ばない
- `StagePlan`から`DiscoveryRequest`へ変換できる
- Artifactが既存Manifestへ登録される
- dry-runが維持される
- validate-onlyが維持される
- runが維持される

### 14.5 Architecture Test

既存Architecture Testの仕組み、またはAST／import graph testを用いて以下を拒否すること。

```text
application -> interfaces.cli
```

また、`interfaces.cli.discovery`から以下へのimportを拒否すること。

```text
pandas
LogicalTableDataLoader
CompleteJourneyPreprocessor
CausalDiscoveryReporter
```

---

## 15. セキュリティ要件

- Providerはallowlist registryからのみ解決する
- 利用者指定Python module／class pathを動的importしない
- YAMLから任意class pathを受け付けない
- 無制限なserver pathより既存Dataset／Artifact abstractionを優先する
- path traversalを防止する
- arbitrary pickle inputを許可しない
- 既存size limitとProject RBACを適用する
- temporary workspaceをRun／Attempt単位で分離する

---

## 16. Acceptance Criteria

以下をすべて満たすこと。

1. `interfaces/cli/discovery.py::main()`がThin Adapterである
2. CLIがPandasをimportしない
3. CLIが`LogicalTableDataLoader`をimportしない
4. CLIが`CompleteJourneyPreprocessor`をimportしない
5. CLIが`CausalDiscoveryReporter`をimportしない
6. `DiscoveryStageRunner`がCLIをimportしない
7. CLIとStage Runnerが同一Application Serviceを使う
8. 既存Complete Journey CLI workflowが動作する
9. Single Table workflowが動作する
10. Provider追加時にCLI変更が不要
11. Provider追加時にApplication Service変更が不要
12. `CausalDiscovery`がsource dataset typeを知らない
13. Complete Journey固有設定が汎用Backendへ漏れない
14. 既存Artifact名とManifest契約が互換
15. 既存Testがすべて成功
16. 新規Unit、Component、CLI、Pipeline、Architecture Testが成功
17. Sphinx documentationがwarningなしでbuild
18. `uv sync --frozen`で再現可能
19. repository標準formatter、lint、type checkが成功
20. public APIに型注釈と適切なdocstringがある

---

## 17. 非目標

本改修では以下を行わないこと。

- PC、GES、LiNGAM、NOTEARSの数値ロジック変更
- DoWhy、EconML、Tigramite、FCIの追加
- Causal Design全体の再設計
- 不要なDataset DB schema全面改修
- Frontend全面改修
- 既存CLI option削除
- 既存Artifact形式の破壊
- 任意Python Provider upload
- 利用者指定Python pathの動的import

---

## 18. 実装前の必須出力

コード変更前にrepositoryを調査し、以下を簡潔に出力すること。

1. 現在のcall graph
2. 関連ファイル
3. 既存Application Service、Port、Factory、Registry規約
4. 関連Test
5. 変更予定ファイル
6. 新規作成予定ファイル
7. 後方互換性リスク
8. 採用する最終Architecture

確認待ちで停止せず、報告後そのまま実装へ進むこと。

---

## 19. 実装後の必須出力

実装後に以下を出力すること。

1. 変更概要
2. 新しい依存方向
3. 変更後ファイル構成
4. 主要classと責務
5. Complete Journey実行経路
6. Single Table実行経路
7. compatibility mapping
8. 実行したTestと結果
9. 未解決の制約
10. 新しいProviderを追加する手順
11. 変更ファイル一覧
12. migrationの有無と内容

---

## 20. 期待する最終フロー

```text
CLI
  -> parse arguments
  -> build DiscoveryRequest
  -> DiscoveryApplicationService.execute()
      -> DiscoveryInputProviderRegistry.resolve()
      -> provider.prepare()
      -> validate prepared input
      -> DiscoveryBackend.discover()
      -> diagnostics
      -> DiscoveryArtifactWriter.write()
      -> DiscoveryExecutionResult
  -> CLI Presenter
```

Complete Journey:

```text
CompleteJourneyDiscoveryInputProvider
  -> LogicalTableDataLoader
  -> CompleteJourneyPreprocessor
  -> PreparedDiscoveryInput
```

Single Table:

```text
SingleTableDiscoveryInputProvider
  -> Table Reader
  -> Schema Validation
  -> Generic Preprocessing
  -> PreparedDiscoveryInput
```

Pipeline:

```text
DiscoveryStageRunner
  -> DiscoveryApplicationService
```

禁止する最終フロー:

```text
DiscoveryStageRunner
  -> interfaces.cli.discovery.main
```

---

## 21. 実行結果ファイル

本指示に基づくrepository調査、設計判断、コード変更、変更ファイル一覧、実行したTestとその結果、未解決事項を、Markdown形式の次のファイルとして出力せよ。

```text
P1_02_resut.md
```

ファイル名は上記を一字一句変更しないこと。
