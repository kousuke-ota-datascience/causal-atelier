# Ariadne ENH-E6 G01 — Observable Family / Stage Navigation Integration — Verification Contract

- Project: Ariadne
- Enhancement: `ENH-E6`
- Active Gate: `G01`
- Baseline SHA: `5a5ced9bd6a0e62027c4058eb66ec487719bde23`
- Contract state: `DRAFT / NOT FROZEN`
- Authority: after freeze, this document alone defines Gate PASS semantics for Test/Audit Agent

## 0. Gate decision semantics

- `PASS`: mandatory AC全てPASS、blocking browser journeys全てPASS、protected regression PASS
- `FAIL`: candidate defectによりmandatory ACを満たさない
- `BLOCKED`: environment/precondition不成立でACを判定不能

source string存在だけで observable UI AC をPASSにしてはならない。

## 1. Acceptance Criteria

### AC-E6-G01-001 — Initial observable shell

fresh browser sessionでProjectを選択し、legacy/normal analysis entryからAnalysisへ遷移した直後、reloadなしで以下が成立する。

- Family tab 3件がvisible/operable
- catalog順・labelと一致
- selected Familyが1件
- current FamilyのStageのみ表示

### AC-E6-G01-002 — Family click default Stage

各Family tabを実際にclickし、以下をassertする。

- URL = target Family default Stage canonical route
- selected Family = clicked Family
- Stage list = target Family catalog stages only
- selected Stage = default Stage
- presentation surface = target `(family, defaultStage)` binding

### AC-E6-G01-003 — Stage click

各代表Familyで非default Stageをclickし、Familyを維持したまま URL / state / selected Stage / presentationが同期する。

### AC-E6-G01-004 — Deep link / reload / history

最低限以下をreal browserで確認する。

1. explicit canonical route direct open
2. reload
3. Family click -> Stage click -> browser Back -> Forward

各stepで URL / selected tab / selected Stage / active presentationが一致する。

### AC-E6-G01-005 — Single transition authority regression

static/code-level verificationで、Family click / Stage click / legacy analytical click / route restore がstate + history + render + presentationを独立に重複実装していないことを確認する。

implementation-specific function nameをassertしてはならない。behavioral dependencyとduplicate mutation pathをinspectionする。

### AC-E6-G01-006 — Stage-aware Causal presentation

real browserまたはDOM integration testで以下を確認する。

- `causal/discovery` -> Discovery surface active, Inference surface inactive
- `causal/identification` -> Inference surface active, Discovery surface inactive
- `causal/estimation` -> Inference surface active
- Family tabはCAUSAL selectedを維持

### AC-E6-G01-007 — Legacy compatibility boundary

left-nav analytical shortcutsをclickし、canonical routeへ収束する。

- Explore -> `exploratory/profile`
- Predictive -> `predictive/setup`
- Causal Discovery -> `causal/discovery`
- Causal Inference -> `causal/identification`

legacy shortcut click後もFamily tabs/sidebarが即時observableで、別のlegacy URL/stateへsplitしない。

### AC-E6-G01-008 — Causal Inference entry semantics

Causal Inference shortcutはidentificationをcompatibility entry pointとして開く。Estimation等へ自動skipしない。

### AC-E6-G01-009 — Fail closed

- unknown Family
- unknown Stage
- catalog current Family missing
- supported catalog Stageにpresentation bindingが無い

でsilent fallbackしない。

### AC-E6-G01-010 — Blocking real-browser proof

実ブラウザで actual Family tab elementをclickするtestをmandatoryとする。HTML文字列に `analysis-family-tabs` がある、JS文字列に `catalog.families.map` がある、だけでは本ACはPASSしない。

### AC-E6-G01-011 — Protected regression

ENH-E5 G01 protected semanticsを維持する。

- parse/serialize
- legacy normalization
- catalog authority
- resource route behavior（変更surfaceに関係する範囲）
- operation availability route query
- back/forward behavior

## 2. Verification architecture

| Layer | Primary responsibility |
|---|---|
| unit | Navigation Context parse/serialize/default/compatibility target |
| DOM/integration | transition coordinatorがselected UI + presentationを同期 |
| static | duplicate full catalog ownershipなし、Navigation->Execution Stage couplingなし、parallel state mutationの検出 |
| browser E2E | observable shell、real click、legacy shortcut、deep link、reload、back-forward |
| regression | E5 G01 protected tests + affected frontend regression |

## 3. Blocking browser journeys

### Journey B01 — Normal entry -> Family switching

1. fresh environment / fresh browser context
2. Project create or deterministic fixture select
3. Explore compatibility entry click
4. Family tabs visibleをassert
5. Predictive tab click
6. URL=`.../analysis/predictive/setup`
7. Predictive stage listをassert
8. Causal tab click
9. URL=`.../analysis/causal/setup`
10. Causal stage listをassert

### Journey B02 — Causal Discovery / Inference surface boundary

1. Causal Discovery shortcut click
2. route=`causal/discovery`
3. discovery surface active
4. Causal Inference shortcut click
5. route=`causal/identification`
6. inference surface active
7. `estimation` Stage click
8. inference surface remains active, selected Stage changes

### Journey B03 — History restore

1. `exploratory/profile`
2. click `predictive`
3. click predictive nondefault Stage
4. Back x2 / Forward x2
5. every stateで route/tab/stage/presentation一致

## 4. Environment / preflight

Gate execution前に baseline reproduction evidenceを保存する。

必須:

- exact candidate SHA
- stack/service readiness
- browser implementation/version
- clean browser context
- deterministic Project fixture or creation procedure

Canonical browser commandは、repository内既存browser harnessをlocal checkoutで確認した後、06/07 freeze前に具体コマンドへ置換する。コマンド未確定のままfreezeしてはならない。

## 5. Failure evidence

browser failure時は最低限保存する。

- current URL
- screenshot
- Family tabs outerHTMLまたはrole/name/selected snapshot
- Stage sidebar snapshot
- active `.workspace` identity
- console error
- relevant network failure

## 6. Anti-false-positive rules

- source existenceのみでAC-001/002/003/004/006/007/008/010をPASSしない
- test専用DOM injectionでFamily tabsを生成しない
- direct `restoreProjectRoute()` invocationだけでnormal left-nav journeyを代替しない
- reloadを挟んで初期render defectを隠さない
