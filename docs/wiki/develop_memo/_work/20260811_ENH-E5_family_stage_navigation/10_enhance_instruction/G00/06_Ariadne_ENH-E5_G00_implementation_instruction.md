# Ariadne ENH-E5 G00 — Family / Navigation Stage Domain Contract — Implementation

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G00`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `acc43f744360e25fc504f608716bed2023817a29`
- 契約状態: `PHASE_K_CONVERGED / EXECUTION_FREEZE_READY`
- Canonical convergence source: `10 / 21 / 22 / 23 / 30 = NFR-019 PASS / FROZEN`
- Document role: `Gate 06 implementation contract`
- Execution Mode: `SINGLE_EXECUTION`

## 0. Authority / execution isolation

- 本文書は、このGateを実装する**Coding Agentに対する唯一のnormative implementation contract**である。
- Coding Agentは仕様補完のために`00〜30`、ADR、他Gate、他Package、`07`、issue、commit message、外部Webを参照してはならない。
- repositoryはcurrent implementation factと実装方法を調査するsubstrateとして参照してよいが、仕様authorityではない。
- 本文書だけでrequired behavior / boundary / migration / error semanticsを一意に決定できない場合は、探索を広げず`BLOCKED_CONTRACT_AMBIGUITY`で停止する。
- Test / Audit Agentのnormative verification sourceはGate `07`のみであり、本`06`を期待挙動の補完に利用しない。


## 1. Outcome

Family-local Navigation catalogとread-only metadata APIを、runtime Execution Stageから独立したapplication/interface contractとして成立させる。Phase G trace=`PF-D2-11`。

## 2. Allowed scope

- immutable Navigation descriptor/value types
- capability-owned Family descriptors
- application/interface catalog aggregator
- `GET /api/v1/navigation/analysis`
- catalog validation
- unit/API/architecture tests

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
- `analysis-navigation/1`をscientific generic `SchemaRegistry`へ登録しない。Navigation metadataはdedicated interface/application validationで検証する。
- catalogからruntime `StageType / StageDefinition / StageExecution`を生成しない。


## 3. API authority

Canonical endpoint:

```http
GET /api/v1/navigation/analysis
```

このresponseはread-only application/presentation metadataであり、ExecutionPlan生成、Runner selection、StageExecution status、AnalysisSpecification mutation、current navigation persistence、Family-specific Result payloadを担当しない。

## 4. Migration policy

- Navigation catalog / route state導入のDB column/table追加は禁止。
- `StageAttempt.effective_random_seed` migrationは本Gateのscope外。
- 新しいpersistent field/tableが必要と判明した場合は独自追加せず`BLOCKED_CONTRACT_AMBIGUITY`。

## Prohibited changes

- `Navigation Stage = Execution Stage`となるmapping、alias、inheritanceを導入しない。
- Navigation Stageを`AnalysisSpecification / ExecutionPlan / Execution / StageExecution`へpersistしない。
- CLI / Python library / backend execution use caseへCurrent Navigation Stageを必須inputとして追加しない。
- `AnalysisSpecification.analysis_family`と重複するFamily discriminatorを追加しない。
- Predictive existing fieldの削除、rename、default semantics変更を行わない。
- LightGBM / DoWhy / EconMLを追加しない。
- D3 / `DEFERRED / FUTURE` requirementをENH-E5 implementationまたはmandatory acceptanceへ混ぜない。
- testをgreenにする目的のassertion弱体化、削除、skip、xfailを行わない。


## 5. Protected contracts

`NONE` — G00はENH-E5 implementation sequenceのfirst Gateである。current runtime Stage/Plan/Runner semanticsはNavigation対応を理由に変更しない。

## Acceptance Criteria

- `AC-G00-001`: canonical Familyはexisting `AnalysisFamily.EXPLORATORY / PREDICTIVE / CAUSAL`のみ。
- `AC-G00-002`: `GET /api/v1/navigation/analysis`がHTTP read-only metadata endpointとして存在する。
- `AC-G00-003`: response top-level fieldは`schema_version`であり、値は`analysis-navigation/1`。`schema`へのrenameは禁止。
- `AC-G00-004`: Stage identity fieldは`stage_id`。generic `id`へのrenameは禁止。
- `AC-G00-005`: canonical metadata response field set、3 Family slug/default/catalogが本文のexact値に一致する。
- `AC-G00-006`: Family exactly-once、global Family slug uniqueness、Family-local Stage ID/slug uniqueness、default membership、deterministic orderをvalidateする。
- `AC-G00-007`: duplicate Family / blank ID or slug / duplicate Stage ID or slug / empty stages / invalid defaultをrejectする。
- `AC-G00-008`: Navigation metadataへruntime input/output/status/retry/attempt/leaseを混入しない。
- `AC-G00-009`: Navigation descriptorをpersistent Domain Resource/Repository/UoWへ登録せず、Navigation導入のDB migrationを行わない。
- `AC-G00-010`: runtime planner/runner/CLI/libraryはNavigation catalog/default/sidebar orderなしでcurrent executionを成立させる。
- `AC-G00-011`: `analysis-navigation/1`をscientific generic `SchemaRegistry`へ登録しない。


## 7. Coding self-verification

- exact field names (`schema_version`, `stage_id`)をAPI contract testで固定する。
- catalog invariant reject casesをunit testする。
- persistent schema diffにNavigation field/tableがないことを確認する。
- runtime StageType/Plan/RunnerがNavigation catalogから生成されないことをarchitecture/static testする。

## Completion evidence

- changed production / test / schema / migration files
- focused test commands and results
- relevant regression commands and results
- candidate SHA / checkpoint SHA
- blocker status (`NONE` or explicit blocker)
