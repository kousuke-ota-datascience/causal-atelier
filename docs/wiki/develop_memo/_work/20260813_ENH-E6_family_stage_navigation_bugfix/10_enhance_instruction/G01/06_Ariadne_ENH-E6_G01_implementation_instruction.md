# Ariadne ENH-E6 G01 — Observable Family / Stage Navigation Integration — Gate Coding Contract

- Project: Ariadne
- Enhancement: `ENH-E6`
- Active Gate: `G01`
- Branch: `bugfix/ariadne_mvp_e6`
- Baseline SHA: `5a5ced9bd6a0e62027c4058eb66ec487719bde23`
- Contract state: `APPROVED / FROZEN`
- Execution Mode: `WORK_PACKAGE`

## 0. Authority

本06は frozen Gate integration semantic contract である。Package Coding Agentへはassigned Pxxを直接 normative source として与え、本06はGate全体のintegration semantic boundaryとして拘束する。Test/Audit Agentのnormative sourceは07のみ。

## 1. Gate outcome

G01は、ENH-E5で意図された Family / Family-local Stage Navigation Shell を、通常ユーザー導線を含む全supported navigation pathへ統合する。

PASS後、後続作業は次へ依存できる。

- 3 Family tabsがanalysis contextでobservable
- current FamilyのみのStage sidebar
- canonical route / history / application state / selected navigation / presentationの同期
- legacy analysis entryがparallel authorityではなくcanonical compatibility entry
- Causal Stageに応じたexisting presentation surface binding

## 2. Protected canonical semantics

次を変更してはならない。

- Family: `EXPLORATORY / PREDICTIVE / CAUSAL`
- backend catalog authority
- canonical route shape: `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`
- `Navigation Stage != Execution Stage`
- Navigation Context non-persistence
- E5 operation availability semantics

## 3. Required implementation semantics

### 3.1 Single Navigation Transition Authority

Navigation Contextを画面へ適用する単一 orchestration pathを実装する。

最低責務:

1. catalog validation
2. `state.navigationContext` commit
3. canonical URL/history synchronization
4. Family tabs render/selected update
5. current Family Stage sidebar render/selected update
6. `(family, stage)` presentation binding resolution
7. presentation surface activation
8. route-dependent operation availability refresh
9. deterministic focus

名称は実装自由だが、entry handlerがこれらを重複実装してはならない。

### 3.2 Entry convergence

以下は同一transition authorityへ収束すること。

- Family tab click
- Stage click
- canonical deep link initial restore
- reload
- browser `popstate`
- legacy route normalization
- legacy analytical left-nav shortcut

### 3.3 Observable shell

analysis contextでは Family tabs / Stage sidebarをobservableにする。non-analysis contextで空shellを誤表示しない。show/hideの実装方式は自由だが、analysis entry直後にreloadなしでtabが操作可能であること。

### 3.4 Legacy compatibility mapping

freeze target:

| Legacy entry | canonical context |
|---|---|
| Explore | `exploratory/profile` |
| Predictive | `predictive/setup` |
| Causal Discovery | `causal/discovery` |
| Causal Inference | `causal/identification` |

legacy entryはworkspaceを先に直接activateしてからcanonical stateを後追い更新してはならない。

### 3.5 Stage-aware presentation binding

Family-only `ANALYSIS_WORKSPACES` をcanonical presentation authorityとして使用してはならない。

Required minimal binding:

- `exploratory/* -> explore`
- `predictive/* -> predictive`
- `causal/setup|discovery -> discovery`
- `causal/identification|estimation|effects|diagnostics|sensitivity -> inference`

未知stage / missing bindingはexplicit configuration error。silent default to `discovery`禁止。

### 3.6 History rules

- user navigation: `pushState`
- legacy normalization: `replaceState`
- `popstate`/initial canonical restore: current URLをauthorityとして適用し、新規history entryを作らない
- same targetへの不要なduplicate history entryを作らない

### 3.7 Failure semantics

- invalid/unknown canonical route: existing deterministic route error
- navigation catalog invariant failure: explicit error
- presentation binding missing: explicit error
- operation availability failure: navigation identityを別routeへsilent fallbackしない

## 4. Allowed change surface

Primary:

- `frontend/app.js`
- `frontend/navigation_state.js`
- `frontend/index.html`
- `frontend/styles.css`
- relevant frontend/presentation helper module
- `tests/product/*ENH-E6*` または既存G01 regression test
- existing browser E2E harness/test files

Backend production codeは、current catalog/route contractの欠陥がpreflightで新規に証明されない限り変更しない。

## 5. Prohibited changes

- E5 frozen 06/07/report/evidence の書換え
- backend full catalogをfrontendへ複製
- Navigation Stageのruntime persistence
- Family/Stageをscientific execution stateとして扱うmapping
- left nav全体の大規模IA redesign
- test assertion weakening / skip / xfailによるgreen化

## 5.1 Frozen preflight facts

2026-08-13 の Human owner 実行による clean browser probe で以下を確認した。

- existing `browser-e2e` Playwright / Chromium harness が build / start 可能
- `#health` = `API READY`
- UIから新規Projectを作成・選択し、Project route contextを確立
- normal Explore entry 後の URL = `/projects/{project_id}/analysis/exploratory/profile`
- `#analysis-family-tabs` container count = 1
- Family button count = 0
- Stage button count = 0

したがって `ANOM-E5-001` は backend unavailable や Project context未確立だけでは説明できず、API READY / canonical route成立下でも observable shell が未描画となる integration defect として再現済みである。

## 6. Work Packages

- `P01`: navigation transition authority + entry convergence
- `P02`: stage-aware presentation binding + legacy compatibility
- `P03`: regression test / real browser observable journey

P01/P02のproduction implementation完了だけではGate PASSではない。

## 7. Gate completion evidence

- fixed Trial candidate SHA
- changed file list
- package checkpoint reports
- unit/static/API regression output
- blocking browser E2E output
- failure screenshots/DOM evidence if applicable
- independent Gate Decision
