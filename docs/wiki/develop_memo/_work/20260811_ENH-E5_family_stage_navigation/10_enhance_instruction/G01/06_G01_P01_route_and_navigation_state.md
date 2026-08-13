# Ariadne ENH-E5 G01 — P01 Route and Navigation State

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G01`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `acc43f744360e25fc504f608716bed2023817a29`
- 契約状態: `APPROVED / FROZEN`
- Canonical convergence source: `10 / 21 / 22 / 23 / 30 = APPROVED`
- Document role: `assigned Pxx implementation contract`

## 0. Authority / execution isolation

- 本文書は、このPackage Coding Agentに対する**唯一のnormative implementation contract**である。
- Package Coding Agentは仕様補完のためにGate `06`、他`Pxx`、`P00`、Gate `07`、`00〜30`、ADR、issue、commit message、外部Webを参照してはならない。
- repositoryはcurrent implementation factと実装方法を調査するsubstrateとして参照してよいが、仕様authorityではない。
- 本文書だけでrequired behavior / protected boundary / error semanticsを一意に決定できない場合は、探索を広げず`BLOCKED_CONTRACT_AMBIGUITY`で停止する。
- Test / Audit Agentのnormative verification sourceはGate `07`のみであり、本Pxxを期待挙動の補完に利用しない。


## 1. Outcome

canonical Stage route、resource deep route、URL-authoritative NavigationContext、legacy normalizationを実装する。

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


### Canonical Route Contract

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}

/projects/{project_id}/analysis/{family_slug}/{stage_slug}/resource/{resource_type}/{resource_id}
```

ENH-E5 `resource_type`:

```text
analysis-specification
execution
result
graph-version
```

Rules:

- explicit Family/Stage deep routeはrouteのStageを保持する。
- generic direct resource linkからdeep routeを構築する場合はresourceからFamilyをderiveし、そのFamily default Stageへ遷移する。
- resource actual Familyとexplicit route Familyが不一致ならexplicit mismatch error。silent normalizationは禁止。
- unknown Family / Stage / resource typeはdeterministic not-found/unsupported error。
- routeはpresentation stateでありResource/Executionへpersistしない。
- direct open / reload / browser back-forwardはURLから同じNavigationContextを復元する。
- legacy routeを残す場合は一方向normalize:
  - `/explore -> /projects/{project_id}/analysis/exploratory/profile`
  - `/predictive -> /projects/{project_id}/analysis/predictive/setup`
  - `/causal -> /projects/{project_id}/analysis/causal/setup`


## 2. Required semantics

- `parse(serialize(context)) == context`。
- explicit Family/Stage deep routeはStageを保持。
- generic resource direct linkはresource Familyをderiveし、そのFamily default Stageを利用。
- route Familyとresource actual Family mismatchはexplicit error。
- current Family/StageをDB、AnalysisSpecification、ExecutionPlan、Execution、StageExecutionへ保存しない。
- legacy/new routeを二つの独立authorityとして維持しない。

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

- canonical/deep route exact。
- resource type exact。
- direct/reload/back-forwardでURLからNavigationContextを再構築可能。
- unknown Family/StageとFamily mismatchのnegative test。
- legacy routeを残す場合はexact一方向mapping。
- route関連persistent schema diffなし。

## Completion evidence

- changed production / test / schema / migration files
- focused test commands and results
- relevant regression commands and results
- candidate SHA / checkpoint SHA
- blocker status (`NONE` or explicit blocker)
