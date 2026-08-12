# Ariadne ENH-E5 G01 — P02 Navigation Shell UI and Action Availability

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G01`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `83d33f5c981fa1aa5740e91c30bb969dd6097c42`
- 契約状態: `PHASE_K_REMEDIATED / REAUDIT_PENDING`
- Canonical convergence source: `10 / 21 / 22 / 23 / 30 = NFR-019 PASS / FROZEN`
- Document role: `assigned Pxx implementation contract`

## 0. Authority / execution isolation

- 本文書は、このPackage Coding Agentに対する**唯一のnormative implementation contract**である。
- Package Coding Agentは仕様補完のためにGate `06`、他`Pxx`、`P00`、Gate `07`、`00〜30`、ADR、issue、commit message、外部Webを参照してはならない。
- repositoryはcurrent implementation factと実装方法を調査するsubstrateとして参照してよいが、仕様authorityではない。
- 本文書だけでrequired behavior / protected boundary / error semanticsを一意に決定できない場合は、探索を広げず`BLOCKED_CONTRACT_AMBIGUITY`で停止する。
- Test / Audit Agentのnormative verification sourceはGate `07`のみであり、本Pxxを期待挙動の補完に利用しない。


## 1. Outcome

backend catalogをauthorityとするFamily tabs / Family-local sidebar / renderer binding / action availability presentationを実装する。

### Canonical Navigation Catalog

| family | slug | default_stage_id | stages in deterministic order |
|---|---|---|---|
| `EXPLORATORY` | `exploratory` | `profile` | `profile`, `data-quality`, `distribution`, `relationships`, `comparison`, `findings` |
| `PREDICTIVE` | `predictive` | `setup` | `setup`, `train`, `predict`, `metrics`, `explainability`, `model-management` |
| `CAUSAL` | `causal` | `setup` | `setup`, `discovery`, `identification`, `estimation`, `effects`, `diagnostics`, `sensitivity` |

Canonical metadata response fields:

```text
schema_version = "analysis-navigation/1"
families[].family
families[].slug
families[].label
families[].default_stage_id
families[].stages[].stage_id
families[].stages[].slug
families[].stages[].label
families[].stages[].order
```

Required invariants:

- Family descriptorは`EXPLORATORY / PREDICTIVE / CAUSAL`各1件。
- Family slugはglobalに一意。
- `stage_id / slug`はFamily内で一意。
- `default_stage_id`は当該FamilyのStage内に存在。
- Stage orderはdeterministic。
- `stage_id == slug`をENH-E5 canonical valueとする。
- runtime input/output/status/retry/attempt/leaseをNavigation metadataへ含めない。
- Navigation descriptorをpersistent Domain Resource、Repository、UoWへ登録しない。
- catalogからruntime `StageType / StageDefinition / StageExecution`を生成しない。


### Operation Availability Contract

```text
GET /projects/{project_id}/operation-availability
```

Query:

```text
resource_type
resource_id
route
```

Responseはoperationごとに最低限:

```text
allowed: bool
reason_code?: string
message?: string
```

Rules:

- Stage visibilityとaction availabilityは別contract。
- `allowed=false`をStage自体の非表示で表現することを基本挙動にしない。
- Authorizationとscientific prerequisiteは別判定。
- Frontendはbackend resultを表示し、route stateだけから実行可否を再実装しない。


## 2. Shell behavior

- catalog source=`GET /api/v1/navigation/analysis`。
- frontend full catalog hard-code禁止。
- Family tabは3 Familyをcatalog orderでrenderし、target Family default Stage routeへ遷移。
- Sidebarはcurrent Family Stageのみ、`order`昇順。
- Stage clickはFamilyを維持してselected Stage routeへ遷移。
- Family last-stage memoryはrequired behaviorではない。
- `(AnalysisFamily, navigation_stage_id)`はpresentation renderer/use-case adapter bindingだけに使用。
- renderer missing / catalog invariant failureをsilent fallbackしない。
- sidebar order/defaultをruntime dependencyへ利用しない。
- async state=`IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`。
- `allowed=false`でもStageをscientific prerequisite表現として自動非表示にしない。

## Prohibited changes

- `Navigation Stage = Execution Stage`となるmapping、alias、inheritanceを導入しない。
- Navigation Stageを`AnalysisSpecification / ExecutionPlan / Execution / StageExecution`へpersistしない。
- CLI / Python library / backend execution use caseへCurrent Navigation Stageを必須inputとして追加しない。
- `AnalysisSpecification.analysis_family`と重複するFamily discriminatorを追加しない。
- Predictive existing fieldの削除、rename、default semantics変更を行わない。
- LightGBM / DoWhy / EconMLを追加しない。
- D3 / `DEFERRED / FUTURE` requirementをENH-E5 implementationまたはmandatory acceptanceへ混ぜない。
- testをgreenにする目的のassertion弱体化、削除、skip、xfailを行わない。


## 4. Package Acceptance Criteria

- backend catalogだけでtabs/sidebar labels/order/defaultが決まる。
- frontend duplicate full catalog 0件。
- operation availability query/resultを表示へ反映し、routeからscientific ruleを推測しない。
- missing renderer/catalog failureはexplicit error state。
- async state exact vocabulary。

## Completion evidence

- changed production / test / schema / migration files
- focused test commands and results
- relevant regression commands and results
- candidate SHA / checkpoint SHA
- blocker status (`NONE` or explicit blocker)
