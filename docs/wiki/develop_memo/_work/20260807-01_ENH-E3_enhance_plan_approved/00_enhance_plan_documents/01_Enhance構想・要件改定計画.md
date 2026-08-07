# Enhance構想・要件改定計画 — ENH-E3

- 作成日: 2026-08-07
- 対象リポジトリ: `kousuke-ota-datascience/causal-atelier`
- 対象ブランチ: `prototype/ariadne_mvp_e3`
- 基準コミット: `3f87379bb3cbf18ba6f436877306959ddfd24163`
- 基準Migration head: `20260806_product_0003`
- エンハンス計画名: `ENH-E3`
- 計画名称: リサーチコンテキスト統合型マルチ分析ワークスペース基盤
- 文書状態: 承認済み
- 承認者: 本チャット依頼者
- 承認日時: 2026-08-07 13:06 JST

## 1. 正本原則

`10_Revised_requirements_definition_documents`の6文書は、ENH-E3完成形を自己完結的に記述する。過去版の差分追記形式、初期版からの時系列説明、旧文書参照を前提とした省略を禁止する。

変更履歴、As-Is、移行、互換性および実装順序は本計画文書群へ記載する。

## 2. Baseline

基準コードでは、Project、Dataset Version、Graph Version、Execution、Result、Artifact、Annotationを中心とする因果分析Product層が存在する。正規Execution Operationは`DISCOVERY / IDENTIFICATION / ESTIMATION / REFUTATION / SENSITIVITY`、正規snapshot schemaは`causal-analysis-spec/2`である。Migration headは`20260806_product_0003`である。

READMEおよび現行Domainは因果探索・因果推論を主対象としており、Explore / PredictiveのProduct Capability、Generic Workflow Plan / Stage Registry、versioned Research Context / Analysis Viewは未実装である。

## 3. 改定理由

- 一つのResearch Topicで探索、因果、予測を扱いたい
- Dataset中心の汎用Workbenchにはせず、Research Contextと来歴を最上位価値とする
- 現行Planner / ExecutorのStage分割思想を流用しつつ、因果固有実装をGeneric Coreと誤認しない
- 改訂正本を旧版への追加章ではなく、ENH-E3の完成形として再構成する
- 因果の科学的contractを保持しつつ、予測のleakage / test isolation contractを追加する

## 4. ENH-E3の目的

1. Project / Research Topic配下に6つのWorkspaceを提供する
2. Research Contextをversioned resourceとして分析へ結び付ける
3. Dataset VersionからAnalysis Viewを作り、三Familyで共有する
4. Explore & Visualize Capabilityを追加する
5. Binary Classification / RegressionのPredictive Capabilityを追加する
6. Planner / Plan / Stage / Runner / ExecutorをGeneric Workflow Coreとして実装する
7. Result、Artifact、Annotationおよびcross-analysis Lineageを統合する
8. 正本文書をENH-E3完成形として全面改訂する

## 5. 対象範囲

- Canonical document full rewrite
- ResearchContextVersion
- AnalysisView
- AnalysisSpecification envelope
- ExecutionPlan / StageExecution
- Planner Registry / Runner Registry / Generic Executor
- Exploratory profiles and charts
- Predictive prepare / split / train / evaluate / explain
- Project Workspace route redesign
- Result envelope、Artifact descriptor、LineageEdge
- additive DB migration
- API / CLI / UI / test / documentation

## 6. 非対象

- Multi-class、forecasting、survival、ranking、recommendation
- online serving、Model Registry、Feature Store、monitoring
- arbitrary SQL / Python
- general BI dashboard builder
- image / NLP / audio
- causal ML拡張を予測MLと同時に無制限追加すること

## 7. 主要設計判断

1. Projectを最上位境界とする
2. Datasetは共有input、Analysis Viewは分析対象条件とする
3. Explore / Causal / PredictiveをAnalysis Familyとして分ける
4. FamilyごとにSchema、Planner、Runner、Validation、Resultを持つ
5. ExecutorはAnalysisロジックを知らない
6. Causal ResultとPredictive Resultを同一scoreで比較しない
7. route-backed tabsを採用する
8. Product Domainからlegacy依存を増やさない
9. `causal-analysis-spec/2`の詳細contractを正本へ完全統合する

## 8. Work Package

| WP | 内容 | 依存 |
| --- | --- | --- |
| WP-0 | Requirements Gate、正本・ID・Schema確定 | なし |
| WP-1 | Domain Resource、Migration、Repository | WP-0 |
| WP-2 | Generic Workflow Core | WP-1 |
| WP-3 | Research Context / Analysis View / Specification | WP-1 |
| WP-4 | Explore & Visualize | WP-2, WP-3 |
| WP-5 | Predictive Capability | WP-2, WP-3 |
| WP-6 | Causal Adapter / Regression Protection | WP-2 |
| WP-7 | Frontend Project Workspace | WP-3〜6 |
| WP-8 | Result / Comparison / Lineage / Export | WP-2〜7 |
| WP-9 | API / CLI / Docs / E2E / Completion Report | 全WP |

## 9. リスク

| Risk | 影響 | 対策 |
| --- | --- | --- |
| Generic化による過剰設計 | 実装量・抽象度増加 | MVP StageとFamilyを限定しRegistry contract testを先行 |
| 因果回帰 | 科学的contract破壊 | 既存payload readerとscientific benchmarkをrelease gate化 |
| 予測leakage | 不正な高精度 | Backend validatorと故意leak test |
| UI肥大化 | 利用者混乱 | Project route分割、用語guard、段階表示 |
| Migration複雑化 | 既存データ読取不能 | additive migration、backfill、dual-read検証 |
| Lineage過剰 | graph性能低下 | 主要FKと明示edgeを分離、depth limit |

## 10. 成果物

- `00_enhance_plan_documents` 6文書
- `10_Revised_requirements_definition_documents` 6文書
- implementation code / migration / tests
- `20_implementation_reports/ENH-E3_completion_report.md`

## 11. 完了条件

- 正本文書が旧文書参照なしに自己完結する
- 10_要件定義のMUST要件がtraceされる
- E2E-01〜08が成立する
- Causal regression、Predictive leakage、Workflow recovery testが成功する
- migration headが一意でupgrade / downgrade手順が確認される
- Completion Reportが実装commitと検証証跡を記録する
