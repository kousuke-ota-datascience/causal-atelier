# Ariadne ENH-E5 G01 — URL-driven Family / Stage Navigation Shell — Verification

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G01`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `83d33f5c981fa1aa5740e91c30bb969dd6097c42`
- 契約状態: `PHASE_K_REMEDIATED / REAUDIT_PENDING`
- Canonical convergence source: `10 / 21 / 22 / 23 / 30 = NFR-019 PASS / FROZEN`
- Document role: `Gate 07 verification contract`

## 0. Authority / verification isolation

- 本文書は、このGateを検証する**Test / Audit Agentに対する唯一のnormative verification contract**である。
- Test / Audit Agentは期待挙動を補完するためにGate `06`、`Pxx`、`P00`、`00〜30`、ADR、issue、commit message、外部Webを参照してはならない。
- repository、candidate diff、test output、migration state、API responseはverification evidenceとして参照してよいが、仕様authorityではない。
- 本文書だけでPASS / FAILを一意に判定できない場合は`BLOCKED_CONTRACT_AMBIGUITY`として報告し、仕様を発明しない。


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


## Gate Acceptance Criteria

- `AC-G01-001`: canonical Stage/resource routesとresource typesがexact。
- `AC-G01-002`: URL/application stateがcurrent Family/Stage authorityでDB persistenceなし。
- `AC-G01-003`: explicit deep route、generic resource link、Family mismatch、unknown Family/Stageのrulesが本文どおり。
- `AC-G01-004`: legacy routeを保持する場合は本文の一方向mappingのみ。
- `AC-G01-005`: Family clickはtarget Family default Stageへ、Stage clickはFamilyを維持してselected Stageへ遷移。
- `AC-G01-006`: frontend full catalog duplicate ownershipなし。renderer missing/catalog invariant failureをsilent fallbackしない。
- `AC-G01-007`: operation availability interface/query/allowed-reason-message contractを利用し、Stage visibilityとaction availabilityを分離。
- `AC-G01-008`: async presentation state=`IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`。
- `AC-G01-009`: E5変更surfaceはkeyboard、deterministic focus、accessible name、error association、non-color semantics、required contrastを満たす。


## Verification architecture

- unit: route parse/serialize/normalize、mismatch/unknown。
- API/integration: catalog consumption、operation availability endpoint/query/response。
- browser: Family click default Stage、sidebar current Family/order、explicit deep route、generic resource deep link、reload/back-forward。
- negative: renderer missing/catalog invalid、`allowed=false`でStage hiddenにしない、silent normalization禁止。
- accessibility: keyboard/focus/accessible name/error/non-color/contrast。
- static: frontend full catalog duplicate ownership、Navigation->runtime Stage生成依存が0件。
