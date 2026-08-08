# Ariadne ENH-E3 実装指示書

- 更新日: 2026-08-07
- 基準ブランチ: `prototype/ariadne_mvp_e3`
- 基準コミット: `3f87379bb3cbf18ba6f436877306959ddfd24163`
- 基準Migration head: `20260806_product_0003`
- 状態: 承認済み・実装開始可
- 承認日時: 2026-08-07 13:06 JST

## 1. 最上位指示

1. `10_Revised_requirements_definition_documents`を正本とする
2. 既存コードから要件を逆生成しない
3. Product Domainからlegacy packageへ依存しない
4. 因果分析の正規payloadとscientific behaviorを回帰させない
5. 予測分析でleakage / test isolationをBackend強制する
6. ExecutorへFamily固有if/elifを追加しない
7. 仕様逸脱が必要な場合は実装で黙って変更せずDeviationとして報告する

## 2. Baseline確認

着手時に次を記録する。

```text
branch
HEAD commit
migration heads
python version
uv lock hash
baseline test commands and results
```

HEADが`3f87379bb3cbf18ba6f436877306959ddfd24163`と異なる場合、差分を監査して計画への影響をCompletion Reportへ記録する。

## 3. Work Package

### 3.1. WP-0 Requirements Gate

- Enum、Schema Version、Resource、status、API pathを一覧化
- 未解決事項をdecision record化
- traceability matrixをtest IDへ拡張

完了条件: 実装者が推測でfield / statusを追加する必要がない。

### 3.2. WP-1 Domain / Migration

実装:

- ResearchContextVersion
- AnalysisView
- AnalysisSpecification
- ExecutionPlan
- StageExecution
- LineageEdge
- family / schema version fields
- additive migration

禁止:

- 既存Result削除
- `causal-analysis-spec/2`の破壊変更
- migration branchの分岐放置

### 3.3. WP-2 Generic Workflow Core

- PlannerRegistry
- RunnerRegistry
- PlanValidator
- BindingResolver
- GenericExecutor
- Stage status / attempt
- artifact commit / compensation

Unit testを先行する。

### 3.4. WP-3 Context / Data / View

- Context API / UI
- Analysis View compiler / validator
- Dataset profile / preview policy
- snapshots / hashes

### 3.5. WP-4 Explore

- profile、distribution、association、group summary、time trend、chart
- Result / Artifact schema
- saved exploration
- create analysis draft

### 3.6. WP-5 Predictive

- Specification schema
- split validator
- leakage validator
- prepare / train / evaluate / explain runners
- classification / regression metric
- Model Card

### 3.7. WP-6 Causal Adapter / Regression

- existing operationsをCAUSAL family planner / runnerへ接続
- input matrix
- identification precedence
- eligibility types
- estimator gate
- revision context
- post-discovery warnings

### 3.8. WP-7 Frontend

- ProjectShell
- 6 routes
- common selectors
- operation availability
- Family-specific terminology
- deep link / browser back

### 3.9. WP-8 Results / Lineage / Export

- common envelope
- same-type comparison
- cross-family summary
- LineageEdge
- Annotation
- Manifest / bundle

### 3.10. WP-9 Verification

必須:

```text
uv run pytest -q
migration upgrade to head
migration downgrade / re-upgrade on test DB
browser E2E
causal scientific benchmark
predictive leakage benchmark
OpenAPI contract test
legacy dependency import check
```

## 4. Coding Guard

- New Domain classはORM annotationを持たない
- JSON fieldはSchema Registryを通す
- external model / dtype objectをResult JSONへ保存しない
- temporary Artifactを成功前にfinal URIとして公開しない
- `SUCCEEDED`とanalytical passを同義にしない
- prediction / explanationの用語にcausal claimを混ぜない

## 5. Test ID

| Test Group | 対象 |
| --- | --- |
| T-E3-DOM-* | Domain invariant / canonicalization |
| T-E3-CTX-* | Research Context |
| T-E3-VIEW-* | Analysis View |
| T-E3-WF-* | Planner / Plan / Runner / Executor |
| T-E3-EXP-* | Explore |
| T-E3-CAU-* | Causal regression / scientific contract |
| T-E3-PRD-* | Predictive split / leakage / metric / explanation |
| T-E3-API-* | API / auth / idempotency |
| T-E3-UI-* | Frontend route / state / terminology |
| T-E3-E2E-* | E2E-01〜08 |

## 6. Completion Report

`20_implementation_reports/ENH-E3_completion_report.md`を作成し、次を含める。

1. Baseline / completed commit
2. Migration head
3. Implemented requirement IDs
4. Changed files
5. Architecture compliance
6. Test commands and exact results
7. Causal regression evidence
8. Predictive leakage evidence
9. Deviations
10. Unresolved issues
11. Final completion decision

証跡がない項目を`Completed`としない。
