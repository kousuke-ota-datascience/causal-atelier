# Phase 1 修正指示書

## 0. Coding Agentへの指示

Ariadneへ「Identification-first、Graph uncertainty、Refutation、Sensitivity」の基盤を追加せよ。既存API、CLI、Worker、Artifact、Manifest、RBAC、Run／Attemptの契約を維持し、既存のDiscovery／Inference数値実装を削除しないこと。

推測で既存クラス名やDB table名を作らず、着手前に必ずrepository内を検索し、既存のport、repository、Unit of Work、router、schema、migration規約へ合わせること。

## 1. Phaseの目的

次を満たす最低限のend-to-end causal lifecycleを実装する。

```text
Causal Question
 -> Causal Design
 -> Graph
 -> Identification
 -> Estimation
 -> Diagnostics
 -> Refutation
 -> Sensitivity
```

## 2. Scope

### 必須

1. `CausalQuestion`とversion
2. `CausalDesign`拡張
3. DAG／CPDAG／PAG schema
4. Identification stage
5. DoWhy adapter
6. FCI adapter
7. Refutation stage
8. Sensitivity stage
9. Scientific validation gate
10. Artifact／Manifest／API／CLI／Worker統合

### 非目標

- CATE
- policy learning
- Tigramite
- DiD／RDD／Synthetic Control
- 自動的な業務意思決定

# 3. Domain Model

## 3.1 CausalQuestion

追加する値:

- id
- project_id
- name
- description
- status
- current_version_id

Version:

- population
- treatment
- comparator
- outcome
- analysis_unit
- treatment_time
- outcome_window
- estimand
- decision_use
- assumptions
- created_by
- created_at
- content_hash

statusは既存Configuration Versionの状態管理と整合させる。

## 3.2 Graph Schema

追加enum:

- `DAG`
- `CPDAG`
- `PAG`
- `TIME_SERIES_GRAPH`

追加edge endpoint:

- `TAIL`
- `ARROW`
- `CIRCLE`

Edgeは`source_endpoint`と`target_endpoint`を持つ。既存directed edgeは`TAIL -> ARROW`へmigration時または読込時に変換する。

追加metadata:

- source type
- discovery algorithm
- assumptions
- bootstrap probability
- graph-level warnings

## 3.3 IdentificationResult

- project_id
- causal_question_version_id
- causal_design_version_id
- graph_version_id
- status
- strategy
- estimand
- adjustment_sets
- assumptions
- expression
- explanation
- non_identifiability_reason
- backend
- backend_version
- reviewer_status
- artifacts

`NOT_IDENTIFIED`は失敗ではなく正常なdomain resultとする。

## 3.4 RefutationResult／SensitivityResult

各結果はRun、estimation result、specification、seed、status、metrics、interpretation、artifactを保持する。

# 4. Ports

次のProtocol／ABCをapplication portとして追加する。

```python
class IdentificationBackend(Protocol):
    def identify(self, request: IdentificationRequest) -> IdentificationBackendResult: ...

class RefutationBackend(Protocol):
    def refute(self, request: RefutationRequest) -> list[RefutationBackendResult]: ...

class SensitivityBackend(Protocol):
    def analyze(self, request: SensitivityRequest) -> list[SensitivityBackendResult]: ...
```

Domain／Application層からDoWhyの型をimportしてはならない。

# 5. DoWhy Adapter

## 5.1 必須機能

- graph変換
- treatment／outcome設定
- back-door identification
- front-door identification
- IV identification
- identify failureの正規化
- existing estimator resultに対するrefuter実行

## 5.2 必須refuter

- placebo treatment
- random common cause
- data subset
- bootstrap

negative controlはDomain Modelを先に用意し、DoWhyで直接対応できない場合は独自adapterとして分ける。

## 5.3 依存管理

- DoWhyはoptional dependency groupへ追加
- import不可時にAPI process全体を起動不能にしない
- backend選択時のみ明確なconfiguration errorを返す
- package versionをmanifestへ保存

# 6. FCI／PAG

既存causal-learn adapterを調査し、同じregistryへFCIを追加する。

設定:

- alpha
- CI test
- max path length等、実際の利用libraryが提供する引数
- background knowledgeとの互換性

出力:

- PAG
- edge endpoint
- latent-confounder warning
- unresolved orientation count

FCI結果をDAGへ強制変換しない。

# 7. Scientific Validation Gate

次をRun前に検査する。

- causal questionの存在
- causal designとのfield整合
- graph nodeにtreatment／outcomeが存在
- post-treatment variableのadjustment禁止
- estimandとidentification strategyの互換性
- graph typeと使用可能strategy
- identification status
- override許可条件

`FAIL`時はESTIMATEへ進めない。`WARN` override時は理由とactorを保存する。

# 8. Pipeline変更

固定Discovery依存を緩和する。

```text
graph source:
  USER_DEFINED | IMPORTED | DISCOVERED | SAVED

IDENTIFY
  -> ESTIMATE
  -> DIAGNOSE
  -> REFUTE
  -> SENSITIVITY
```

Discoveryなしでユーザー定義Graphから開始できること。

既存`DISCOVERY -> INFERENCE`経路はcompatibility facadeとして維持する。

# 9. API／CLI

## API

追加resource:

- causal questions
- causal question versions
- causal designs／versions
- identification runs／results
- refutation results
- sensitivity results

既存Project RBACを必ず適用する。

## CLI

追加例:

```text
ariadne-identify
ariadne-refute
ariadne-sensitivity
```

ただし、既存CLIの命名・parser構造を確認し、統一できる場合は`ariadne-pipeline --stage ...`形式を優先する。

# 10. Artifact

最低限:

- `causal_question.json`
- `causal_design.json`
- `graph.json`
- `identified_estimand.json`
- `adjustment_sets.json`
- `refutation_results.json`
- `sensitivity_results.json`
- human-readable Markdown report

全Artifactにchecksumとlineageを付ける。

# 11. Migration

- Graph typeおよびendpoint追加
- Causal Question tables
- Identification／Refutation／Sensitivity tables
- Run input reference追加
- 既存Runが読めるnullable migration
- downgrade可否はrepository規約に従う

# 12. Tests

## Unit

- graph endpoint変換
- DAG／CPDAG／PAG validation
- estimand compatibility
- `NOT_IDENTIFIED`
- post-treatment rejection
- backend result normalization

## Component

- DoWhy identification adapter
- refuter adapter
- FCI -> PAG
- optional dependency unavailable

## API

- RBAC
- cross-project 404
- immutable version
- invalid schema 422

## Worker

- identification success
- non-identification success state
- retry safety
- artifact idempotency
- cancellation

## Scientific

既知真値のsynthetic dataで以下を検証:

- back-door
- front-door
- IV
- latent confounderを含むFCI
- placebo refuter
- simulated unobserved confounding

# 13. Acceptance Criteria

- DiscoveryなしでDAGからIdentificationを実行できる
- `NOT_IDENTIFIED`がUI／API／CLIで説明付き表示される
- FCI結果がPAGとして保存される
- DoWhy型がDomain層へ漏れない
- 既存pipeline testがすべて通る
- 新規Runのmanifestにquestion、design、graph、identification、backend versionが含まれる
- Refutation／Sensitivityが再実行可能
- Sphinx docsがwarning zeroでbuildする

# 14. Deliverables

- source code
- migration
- unit／component／API／worker／scientific tests
- API docs
- architecture decision record
- migration guide
- example configuration
- known limitations
