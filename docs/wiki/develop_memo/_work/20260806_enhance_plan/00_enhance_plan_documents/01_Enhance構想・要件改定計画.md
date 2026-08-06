# Enhance構想・要件改定計画

- 作成日: 2026-08-06
- 対象システム: Ariadne 初期価値検証版
- 対象リポジトリ: `kousuke-ota-datascience/causal-atelier`
- 対象ブランチ: `prototype/ariadne_mvp`
- 基準コミット: `f5e6e5ad5774a3951af5af65b724c4b53aada56a`
- 改定識別子: `ENH-E1`
- 改定名称: 科学的妥当性基盤強化
- 文書状態: 承認対象

> **要件定義書は常にシステムの正本である。**
>
> **実装、既存コード、DBスキーマ、API、UI、テスト結果から要件定義書を逆生成または事後更新してはならない。**

## 1. 要件定義書正本原則

### 1.1. 正本の定義

承認済み要件定義書および承認済み要件変更履歴を、システムが満たすべき要求の唯一の正本とする。

以下は要件定義書から導出される下位成果物である。

- プロダクト基本設計書
- 論理データ設計書
- API・インターフェース設計書
- 詳細設計書
- 実装指示書
- ソースコード
- DBスキーマ
- API実装
- UI
- テスト
- 運用手順

### 1.2. 実装からの要件更新禁止

以下を禁止する。

1. 現行コードの挙動を、そのままTo-Be要件へ昇格すること
2. 実装が困難であることを理由に、要件を弱めること
3. 実装済み機能を正当化する目的で、要件定義書を事後更新すること
4. テストが通る範囲を、要件の範囲として再定義すること
5. DBスキーマ、API payload、画面構造から要件を逆生成すること
6. Coding Agentに要件または設計の未決事項を補完させること
7. 既存コードの互換性を、承認なく新システムの要件へ昇格すること

### 1.3. 不一致の処理

```text
要件と設計・実装の不一致を検出
→ 対応する要件IDと受入条件を特定
→ 原則として設計・実装・テストを修正
→ 要件自体の変更が必要な場合は独立した変更提案を作成
→ 要件変更を承認
→ 要件定義書を先に更新
→ 下位設計書を更新
→ 整合性を再確認
→ 実装を再開
```

## 2. Enhance構想の目的

### 2.1. 現行MVPの価値検証経路

```text
Dataset Version登録
→ 複数の因果探索
→ Graph比較・選定・固定
→ 複数のATE／ATT推定
→ Result比較
→ Annotation
→ Lineage確認
```

### 2.2. 現行MVPの科学的方法論上の不足

現行MVPでは、以下の概念が十分に分離されていない。

- 因果的な問いと数値計算条件
- IdentificationとEstimation
- 識別可能性と数値計算可能性
- Algorithm Output Graphと人為修正Graph
- Data EligibilityとEstimator実行可能性
- DiagnosticsとIdentificationの妥当性
- 推定成功とRefutation／Sensitivity
- 探索的分析と確認的分析

### 2.3. 本改定の目的

現行の7 EntityおよびExecution Snapshotモデルを維持しながら、上記の科学的意味を機械可読かつ追跡可能にする。

## 3. Ariadneの概念体系

### 3.1. Project

```text
Project
= 1つのResearch Topicを扱う業務、権限、来歴の境界
```

### 3.2. Research Context

```text
Research Context
= 分析を行う理由と問いの文脈

Problem Statement
+ Research Question
+ Significance
+ Hypothesis
```

### 3.3. Analysis Specification

```text
Analysis Specification
= 何を、どの方法、仮定、評価基準で分析するかを表す仕様
```

### 3.4. Execution Plan

```text
Execution Plan
= 入力Version、Research Context、Analysis Specification、
  Algorithm、Parameter、Runtime、出力契約を固定した不変計画
```

### 3.5. Execution、Result、Artifact、Claim

```text
Execution
= Execution PlanをAriadne管理下で遂行する一回の処理要求

Result
= Executionによって得られた分析上の結果

Artifact
= Resultを構成または裏付ける物理的生成物

Claim / Interpretation
= Resultを根拠として人間が提示する、
  範囲、仮定、限界付きの回答
```

## 4. MVPにおける概念の写像

### 4.1. 写像方針

ENH-E1では、Research Context、Analysis Specification、Execution PlanおよびClaimを新しい独立Entityにしない。

| 概念 | ENH-E1での表現 |
|---|---|
| Project | `Project` |
| Research Context | Project属性およびExecution Snapshot |
| Analysis Specification | `Execution.analysis_spec_json` |
| Execution Plan | Executionの不変Snapshot |
| Execution | `Execution` |
| Result | `Result` |
| Artifact | `Artifact` |
| Claim / Interpretation | `Annotation` |
| Comparison | Query Projection |
| Lineage | 明示的な参照関係から生成するView |

### 4.2. 主要Entity

以下の7 Entityを維持する。

```text
Project
Dataset Version
Execution
Result
Artifact
Graph Version
Annotation
```

## 5. 目標科学ライフサイクル

### 5.1. 標準経路

```text
Research Question
→ Causal Question
→ Causal Design
→ Graph and Assumptions
→ Identification
→ Data Eligibility
→ Estimation
→ Statistical Inference
→ Diagnostics
→ Refutation
→ Sensitivity
→ Claim / Interpretation
→ Re-analysis
```

### 5.2. Discoveryの位置付け

DiscoveryをIdentificationの必須前段とはしない。

以下の経路を許可する。

```text
Discovery Result
→ Graph Version
→ Identification
```

```text
User-defined Graph Version
→ Identification
```

```text
Imported Graph Version
→ Identification
```

## 6. Enhanceリリース区分

### 6.1. ENH-E1の対象

1. Research Contextの構造化Snapshot
2. Causal Questionの構造化Snapshot
3. Causal Designの構造化Snapshot
4. 探索的分析と確認的分析の区別
5. Graph originおよび編集来歴
6. DAG、CPDAG、PAGの意味保持
7. Identification Execution
8. Data Eligibility Result
9. Estimation前の科学的Validation Gate
10. Identification Resultの下流再利用
11. Result Type固有のscientific status
12. 最小限のRefutation
13. 最小限のSensitivity
14. SyntheticおよびSemi-synthetic Benchmark
15. Lineageの上流Result対応
16. API、Worker、CLI、UIにおける科学的意味の統一

### 6.2. ENH-E2の候補

- 連続Treatment
- CATE／HTE
- DML
- Causal Forest
- Meta Learner
- Subgroup Multiplicity
- Policy-ready Artifact

### 6.3. ENH-E3の候補

- IV
- DiD
- RDD
- Synthetic Control
- 時系列因果分析
- 生存時間Outcome
- 反復介入
- Mediation

### 6.4. ENH-E4の候補

- Policy Optimization
- Off-policy Evaluation
- Monitoring
- Effect Drift
- Claimの正式なVersion管理
- 独立Review／Approval Workflow
- 詳細RBAC
- Research Contextの独立Resource化

## 7. ENH-E1の非対象

以下をENH-E1へ混入させてはならない。

- 新しい主要Entity
- Causal Question専用Table
- Causal Design専用Table
- Identification専用Table
- Refutation専用Table
- Sensitivity専用Table
- Stage Execution
- Stage Attempt
- 汎用Lineage Relation Table
- Comparison Resource
- Transactional Outbox
- 詳細RBAC
- 承認Workflow
- 旧Run／Attemptとの互換
- 旧Metadata DBのデータ移行
- 旧Control Planeの復活
- ENH-E2以降の分析方式

## 8. 主要設計方針

### 8.1. 科学段階のExecution Operation化

Execution Operationを以下へ拡張する。

```text
DISCOVERY
IDENTIFICATION
ESTIMATION
REFUTATION
SENSITIVITY
```

Data EligibilityはIdentification Executionが生成するResultとする。

DiagnosticsはEstimation Executionが生成するResultとする。

### 8.2. 上流Resultの直接参照

Executionに`input_result_id`を追加する。

- EstimationはIdentification Resultを参照する
- RefutationはTreatment Effect Resultを参照する
- SensitivityはTreatment Effect Resultを参照する
- Project境界を越えるResult参照を禁止する
- Operationと上流Result Typeの組合せを検証する

### 8.3. 技術状態と科学状態の分離

Execution Statusは技術処理状態を表す。

```text
QUEUED
RUNNING
SUCCEEDED
FAILED
CANCELLED
```

Resultのscientific statusは科学的評価を表す。

`NOT_IDENTIFIED`、`FAILURE_DETECTED`、`FRAGILE`等を技術的失敗として扱わない。

### 8.4. Graphの意味保持

最低限、以下を区別する。

- Graph Type
- Endpoint Semantics
- Graph Origin
- Algorithm Output
- Constraint Adjusted
- User Defined
- Imported
- User Edited
- Background Knowledge
- Unresolved Orientation
- Latent Confounding Warning
- Bootstrap Agreement
- Algorithm Agreement

## 9. Enhance構想の完了条件

以下をすべて満たした場合、ENH-E1構想を完了とする。

1. ENH-E1の対象範囲が明示されている
2. ENH-E2以降との境界が明示されている
3. 7 Entityを維持する方針が明示されている
4. 科学段階と物理Entityが分離されている
5. 旧Enhance計画の旧アーキテクチャ依存部分が失効扱いになっている
6. 要件定義書の改定対象が明示されている
7. 実装から要件定義書を更新しない原則が明示されている
