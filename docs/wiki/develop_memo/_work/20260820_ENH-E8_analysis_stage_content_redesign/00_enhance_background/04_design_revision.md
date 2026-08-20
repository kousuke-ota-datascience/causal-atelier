# ENH-E8 Design Revision

- Status: `APPROVED`
- Requirement semantic delta: `NONE`
- Basic Design delta: `YES`
- Detailed Design delta: `YES`

## 1. Design Invariant

| ID | Design invariant |
|---|---|
| E8-DI-01 | Selected Projectはcanonical Project List `/projects` への明示的parent navigationを持つ。history originをtarget authorityにしない。 |
| E8-DI-02 | Stage Contentsのprimary heading/descriptionはcurrent canonical Navigation Stageを示す。legacy workspace groupingをcurrent Stage identityとして表示しない。 |
| E8-DI-03 | main operation/result/explanationは責務を持つNavigation Stageが所有する。cross-stage dependencyはcompactなreference/prerequisiteに限定する。 |
| E8-DI-04 | Causal sidebar groupingはpresentation-onlyとし、route / stage slug / backend runtime Stage / DB field / persistent stateを追加しない。 |
| E8-DI-05 | Causal Identification / Estimation / Effects / Diagnostics / Sensitivityの責務を分離する。Sensitivity/Refutation controlはSensitivityのみが所有する。 |
| E8-DI-06 | Predictive Setup / Train / Predict / Metrics / Explainability / Model Managementの目的を分離し、既存 `predictive-analysis-spec/1` semanticsを維持する。 |
| E8-DI-07 | 主要semantic sectionは縦方向reading flowを基本とする。compact controlのlocal gridとwide table/chartのlocal overflowは許可する。 |
| E8-DI-08 | canonical Navigation Stage catalog、API、persistence/schema、domain/scientific semantics、ML algorithm/explanation capability、runtime lifecycleを変更しない。 |
| E8-DI-09 | Predictive feature-column編集はSetupが所有し、Dataset-schema-backed popup/dialog + checkbox multi-selectを使う。Train/Predictは該当feature setをread-only表示する。Confirmは既存 `feature_spec.feature_columns` だけを更新する。 |

## 2. Causal presentation model

canonical Causal Stageは変更しない。

`setup / discovery / identification / estimation / effects / diagnostics / sensitivity`

sidebar groupingを使う場合はvisual-onlyとする。

```text
分析設計
  Setup
因果構造
  Discovery
識別
  Identification
推定・評価
  Estimation
  Effects
  Diagnostics
  Sensitivity
```

### Stage responsibility

| Stage | 目的 | 主な操作・結果 |
|---|---|---|
| Identification | estimandの識別可能性とdata eligibilityを判断 | causal question, strategy, adjustment set, assumptions, Identification/Eligibility, gate/warnings |
| Estimation | identified estimandを有限標本から推定 | Identification Result reference, estimator/nuisance/uncertainty/revision, Estimation |
| Effects | 保存済みtreatment effectを読む・比較 | ATE/ATT/CATE, interval, uncertainty, heterogeneity/comparison |
| Diagnostics | 推定の支持条件・安定性を診断 | balance, overlap, ESS, weights, scientific warnings |
| Sensitivity | 仮定・仕様変更への頑健性を確認 | Refutation/Sensitivity control/result |

## 3. Predictive presentation model

| Stage | 目的 | 主な表示 |
|---|---|---|
| Setup | prediction taskとanalysis specificationを定義 | context/dataset/view, task, target/features, timing/horizon, split/specification。feature setはここで編集 |
| Train | modelを学習 | read-only feature set, preprocessing/model/tuning, execution/status, fitted-result reference |
| Predict | existing prediction outputを確認 | saved execution specification由来のread-only feature set + prediction result/artifact。new scoring runtimeは作らない |
| Metrics | predictive performanceを評価 | Evaluation Result, primary/secondary metrics, subgroup/error analysis |
| Explainability | predictive explanationを確認 | explanation result/artifact + predictive-not-causal warning |
| Model Management | model assetとprovenanceを確認 | Model Card, fitted model/preprocessor artifact, Result/Artifact/Lineage |

### 3.1 Predictive feature selection

```text
Selected Dataset Version
        ↓
Dataset schema
        ↓
Feature selector dialog
  [ ] column_a
  [x] column_b
  [x] column_c
        ↓ Confirm
existing feature_spec.feature_columns
```

設計rule:

1. primary editing interactionをcomma-delimited free textにしない。
2. selected Dataset Version schemaをcandidate-column authorityとする。
3. checkbox multi-selection、explicit Confirm、Cancel-without-mutationを提供する。
4. Confirm後の順序はdeterministicとする。Dataset schema orderを推奨する。
5. Dataset Version変更時、新schemaに存在しないselected columnをsilentに保持しない。
6. target/excluded-column、feature availability、split、leakage等のexisting validationを維持する。
7. valid confirmed selectionはexisting Predictive draft-stateでStage切替後も保持する。
8. Train/Predictはeditable selectorを持たない。
9. Causal Discovery selectorを共通化する場合、そのexisting behaviorをprotected regressionとする。

## 4. Layout

top-level Stage sectionは縦方向に積む。意味的に独立したsectionを横並びにしてpage-level horizontal scrollを発生させない。intrinsically wideなtable/chart等はcomponent-local overflowを許可する。

## 5. Compatibility boundary

ENH-E8では以下を追加・変更しない。

- API
- DB/persistence
- backend/runtime semantics
- canonical Navigation Stage
- new Predictive specification version
- LightGBM / LIME / SHAP
- standalone Predict operation
