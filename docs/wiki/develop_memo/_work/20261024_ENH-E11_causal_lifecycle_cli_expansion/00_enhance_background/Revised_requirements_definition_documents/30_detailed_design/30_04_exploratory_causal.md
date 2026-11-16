<!-- ENH-E11 split working copy: not a formal approval. -->
# 30 — exploratory causal

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [30_detailed_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/30_detailed_design.md) · blob `04d83541e55ab0364500afb4b92ef55c10785a0c`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 13. Exploratory Capability / Stage Contents

### 13.1 Mapping

| Navigation Stage | Current operation / resource | Detailed placement |
| --- | --- | --- |
| Profile | `PROFILE` | profile execution/control/result |
| Data Quality | dedicated operationなし | `PROFILE` resultのread-only projection |
| Distribution | `DISTRIBUTION` | distribution control/result |
| Relationships | `ASSOCIATION` | association control/result |
| Comparison | `GROUP_SUMMARY`, `TIME_TREND` | comparison/grouping controls/results |
| Findings | `CHART`, saved Exploratory Results | chart control/result/artifact + saved results |

### 13.2 Profile

ProfileはDataset/Analysis Viewのdescriptive profileを生成・表示する。

Profile resultはData Quality Stageからもread-only参照され得る。

### 13.3 Data Quality

Data Quality専用backend operationを作らない。

```text
PROFILE result found
  → render read-only data-quality availability/summary

PROFILE result absent
  → NO_PROFILE_RESULT
  → Profileへの導線
  → Execution/resource/backend stateを新規作成しない
```

`DATA_QUALITY` runtime operation、Result Type、persistent stateを追加しない。

### 13.4 Distribution

`DISTRIBUTION` operation/resultを配置する。Navigation Stage名を理由にruntime StageTypeを増設しない。

### 13.5 Relationships

`ASSOCIATION` operation/resultを配置する。

### 13.6 Comparison

`GROUP_SUMMARY`と`TIME_TREND`を同一Navigation Stageへ配置できる。

`TIME_TREND`はcurrent grouping/aggregation semanticsを維持する。

禁止:

- 新しい時系列モデルの導入
- UI Stage都合だけのtime type validation追加
- time orderingをscientific model semanticsとして暗黙導入

### 13.7 Findings

`CHART`はpersistent operationであり、表示専用mechanismへ置換しない。

- `CHART_RESULT`
- `CHART_SPECIFICATION`等のartifact/specification
- saved Exploratory Results

をcurrent contractに従って扱う。

---

## 14. Causal Capability / Stage Contents

### 14.1 Runtime discriminator / mapping

Causal family spec schema versionは`causal-analysis-spec/2`。runtime operationは次のdiscriminatorを使用する。

```text
DISCOVERY
IDENTIFICATION
ESTIMATION
REFUTATION
SENSITIVITY
```

Representative mapping:

| ExecutionOperation | stage_key | StageType |
| --- | --- | --- |
| `DISCOVERY` | `discovery` | `causal.discovery.v1` |
| `IDENTIFICATION` | `identification` | `causal.identification.v1` |
| `ESTIMATION` | `estimation` | `causal.estimation.v2` |
| `REFUTATION` | `refutation` | `causal.refutation.v1` |
| `SENSITIVITY` | `sensitivity` | `causal.sensitivity.v1` |

runtime input matrix:

| ExecutionOperation | input_graph_version_id | input_result_id |
| --- | ---: | ---: |
| DISCOVERY | なし | なし |
| IDENTIFICATION | 必須 | なし |
| ESTIMATION | 必須 | 必須 |
| REFUTATION | 必須 | 必須 |
| SENSITIVITY | 必須 | 必須 |

`Effects` / `Diagnostics`等のNavigation Stageはsaved Result readで成立し得るため、同名ExecutionOperation/StageTypeを追加しない。

### 14.2 Setup

primary responsibility:

- causal question / design preparation
- direct graph registration where supported
- Research Context / Dataset / Analysis View確認

Identification/Estimation/Sensitivityのmain operationをSetupへ複製しない。

### 14.3 Discovery

primary responsibility:

- discovery specification
- PC / GES等のcurrent discovery operation
- graph candidate
- candidate comparison/edit/adopt/fix
- confounder / mediator / collider / temporal ordering / domain assumption検討

Discoveryのnavigation placementはruntime graph/discovery semanticsを変更しない。

### 14.4 Identification

目的は、causal question / estimandについて識別可能性とdata eligibilityを明示することである。

primary surface:

- Dataset / Analysis View / FIXED Graph prerequisite
- estimand / causal question
- identification strategy
- adjustment set
- exchangeability
- positivity
- consistency
- IV / parallel trends等のstrategy-specific assumption
- Identification execution/result
- Data Eligibility / Estimation gate
- identified / not identified / partially identified等のstatus
- warning/failure reason

estimator tuning、Refutation、Sensitivity controlをIdentificationのmain surfaceへ置かない。

### 14.5 Estimation

目的は、identified estimandを有限標本データから推定することである。

primary surface:

- selected Identification Resultのcompact prerequisite/reference
- estimator selection
- nuisance model configuration
- bootstrap / uncertainty configuration
- revision / override where supported
- execution submission/status
- estimation result linkage

Identification assumptionをestimator parameterへ埋没させない。Identification/Data Eligibilityの全文説明をEstimationのpage purposeとして再掲しない。

### 14.6 Effects

目的は、保存済みTreatment Effect Resultを読み、effect量とuncertaintyを解釈・比較することである。

primary surface:

- `TREATMENT_EFFECT_RESULT`
- ATE / ATT / CATE等、result schemaが持つeffect payload
- uncertainty / interval
- subgroup / heterogeneity projection
- supported comparison/reference

Diagnosticsと同一primary card/headingを共有しない。

### 14.7 Diagnostics

目的は、推定の支持条件・安定性・diagnostic warningを確認することである。

primary surface:

- `DIAGNOSTICS_RESULT`
- balance
- overlap
- effective sample size
- weight diagnostics
- scientific warning

Effects Resultをprerequisite/referenceとして参照してよいが、Effect comparisonをDiagnosticsのpage purposeにしない。

### 14.8 Sensitivity

目的は、推定結果が仮定・仕様変更に対してどの程度頑健かを確認することである。

primary surface:

- target Treatment Effect Result reference
- `REFUTATION_RESULT`
- `SENSITIVITY_RESULT`
- Refutation control/result
- Sensitivity control/result
- alternate assumption/specification依存性
- robustness interpretation

Refutation/Sensitivity operation controlはSensitivity Stageのみが所有する。Identification / Estimation / Effects / Diagnosticsではこれらをeditable controlとして表示しない。

### 14.9 Causal visibility matrix

| Surface | identification | estimation | effects | diagnostics | sensitivity |
| --- | ---: | ---: | ---: | ---: | ---: |
| Identification purpose/input/action | ON | OFF | OFF | OFF | OFF |
| Identification / Eligibility / Gate result | ON | compact prerequisite/reference | OFF | OFF | OFF |
| Estimation config/action | OFF | ON | OFF | OFF | OFF |
| Treatment effect primary result/comparison | OFF | compact completion/reference | ON | optional reference | prerequisite reference |
| Diagnostics result/warnings | OFF | OFF | OFF | ON | optional prerequisite/reference |
| Refutation controls/results | OFF | OFF | OFF | OFF | ON |
| Sensitivity controls/results | OFF | OFF | OFF | OFF | ON |

### 14.10 Causal presentation guidance

Causal Stageのprimary purpose summaryは日本語を基本とする。ATE、ATT、CATE、estimand、overlap、ESS等、実装・分析概念との対応上英語が明確な専門語は英語を維持してよい。

説明文から、少なくとも次を理解できること。

- このStageで何を判断・閲覧するか
- 前後Stageと何が異なるか
- current operationがscientific executionかsaved Result readか

---
