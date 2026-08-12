# Ariadne ENH-E5 G01 — URL-driven Family / Stage Navigation Shell — Gate Integration

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G01`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `acc43f744360e25fc504f608716bed2023817a29`
- 契約状態: `PHASE_K_REMEDIATED / REAUDIT_PENDING`
- Canonical convergence source: `10 / 21 / 22 / 23 / 30 = NFR-019 PASS / FROZEN`
- Document role: `Gate 06 integration contract`
- Execution Mode: `WORK_PACKAGE`

## 0. Authority / execution isolation

- 本文書は`WORK_PACKAGE` Gate全体の**Operator / Gate Orchestrator向けintegration contract**である。
- Package Coding Agentへ本`06`をnormative sourceとして渡してはならない。Package Coding Agentの唯一のnormative implementation contractはassigned `Pxx` 1文書である。
- Gate Orchestratorはpackage分割、統合candidate、Gate-level protected invariant、completion evidenceの管理に本書を使用する。
- Package Coding Agentがassigned `Pxx`だけで実装を一意に決定できない場合は、他文書を読ませず`BLOCKED_CONTRACT_AMBIGUITY`として停止する。
- Test / Audit Agentのnormative verification sourceはGate `07`のみであり、本`06`や`Pxx`を期待挙動の補完に利用しない。


## 1. Gate outcome

3 Packageを統合して、canonical/deep route、Family tabs、Family-local sidebar、operation availability、history/deep-link、E5 accessibilityを成立させる。Phase G trace=`PF-D2-09 / PF-D2-11`。

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

Canonical response envelope:

```json
{
  "operations": {
    "<operation>": {
      "allowed": true,
      "reason_code": "...",
      "message": "..."
    }
  }
}
```

各operation item:

```text
allowed: bool
reason_code?: string
message?: string
```

`reason_code`と`message`はoptional。top-level `operations` mapはrequired。

Rules:

- Stage visibilityとaction availabilityは別contract。
- `allowed=false`をStage自体の非表示で表現することを基本挙動にしない。
- Authorizationとscientific prerequisiteは別判定。
- Frontendはbackend resultを表示し、route stateだけから実行可否を再実装しない。


## 2. UI rules

- backend Navigation endpointをcatalog authorityとし、frontendにfull catalogをhard-codeしない。
- Family tabはsupported Familyをdeterministic catalog orderでrenderし、click時はtarget Family default Stageへ遷移。
- Sidebarはcurrent FamilyのStageのみをorder昇順でrenderし、Stage clickでFamilyを変更しない。
- Familyごとのlast-stage memoryはrequired behaviorではない。
- renderer missing / catalog invariant failureはconfiguration defectとして明示しsilent fallbackしない。
- async presentation state=`IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`。
- action availabilityはbackend authority。scientific/business ruleをfrontendへ複製しない。

## 3. Accessibility

E5変更surface:
- keyboard操作可能
- route/navigation後のfocus target deterministic
- icon-only control含むaccessible name
- error/help association
- status/action availabilityを色だけで表現しない
- normal text contrast >= 4.5:1
- large text/UI graphics/focus indicator >= 3:1

## Prohibited changes

- `Navigation Stage = Execution Stage`となるmapping、alias、inheritanceを導入しない。
- Navigation Stageを`AnalysisSpecification / ExecutionPlan / Execution / StageExecution`へpersistしない。
- CLI / Python library / backend execution use caseへCurrent Navigation Stageを必須inputとして追加しない。
- `AnalysisSpecification.analysis_family`と重複するFamily discriminatorを追加しない。
- Predictive existing fieldの削除、rename、default semantics変更を行わない。
- LightGBM / DoWhy / EconMLを追加しない。
- D3 / `DEFERRED / FUTURE` requirementをENH-E5 implementationまたはmandatory acceptanceへ混ぜない。
- testをgreenにする目的のassertion弱体化、削除、skip、xfailを行わない。


## Gate Acceptance Criteria

- `AC-G01-001`: canonical Stage/resource routesとresource typesがexact。
- `AC-G01-002`: URL/application stateがcurrent Family/Stage authorityでDB persistenceなし。
- `AC-G01-003`: explicit deep route、generic resource link、Family mismatch、unknown Family/Stageのrulesが本文どおり。
- `AC-G01-004`: legacy routeを保持する場合は本文の一方向mappingのみ。
- `AC-G01-005`: Family clickはtarget Family default Stageへ、Stage clickはFamilyを維持してselected Stageへ遷移。
- `AC-G01-006`: frontend full catalog duplicate ownershipなし。renderer missing/catalog invariant failureをsilent fallbackしない。
- `AC-G01-007`: operation availability endpoint/queryとtop-level `operations` map + `{allowed, reason_code?, message?}` item contractを利用し、Stage visibilityとaction availabilityを分離。
- `AC-G01-008`: async presentation state=`IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`。
- `AC-G01-009`: E5変更surfaceはkeyboard、deterministic focus、accessible name、error association、non-color semantics、required contrastを満たす。


## 5. Gate integration evidence

- P01/P02/P03 candidateを単一Gate candidateへ統合。
- Gate-level browser/API/static/a11y regressionを実行。
- Package単体PASSをGate PASSとみなさない。
