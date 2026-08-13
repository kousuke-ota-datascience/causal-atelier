# ENH-E6 Enhance構想・要件改定計画

> **Document class:** Planning / Decision Artifact  
> **Self-containment:** MUST for own subject.

- Status: `APPROVED / G01 CONTRACT FROZEN`
- Target branch: `bugfix/ariadne_mvp_e6`
- Production baseline: `5a5ced9bd6a0e62027c4058eb66ec487719bde23`
- Source anomaly: `ANOM-E5-001`
- Canonical requirement/design revision: `NONE`

## 1. Problem statement

ENH-E5はAnalysis画面で3 Family (`EXPLORATORY / PREDICTIVE / CAUSAL`) をtabで切替え、Family切替時にFamily固有Navigation Stageへ切替える契約を持つ。しかしproduction baselineではFamily/Stage shellのDOMとrenderer codeが存在するにもかかわらず、normal analysis entryでFamily buttons/Stage buttonsがobservableにならない。

API READY clean preflightでもProject contextとcanonical `.../analysis/exploratory/profile`が成立した状態でFamily button=0、Stage button=0を再現した。

## 2. Why now

ENH-E5 closeoutが`ANOM-E5-001`をbugfix enhancement follow-upとして明示し、通常利用時にprimary navigationがobservableでないため、E5で成立させたsemantic contractをユーザーが利用できない。後続UI改善より先にnavigation authority/lifecycleを修復する必要がある。

## 3. Current-state problem

- `analysis-family-tabs` / `analysis-stage-sidebar` containerと`renderAnalysisNavigation()`は存在する。
- canonical route restore pathとnormal workspace activation pathのrender lifecycleが非対称。
- Navigation Context、history、selected UI、presentation activationを複数entry pathが部分的に個別操作する。
- Family-only `causal -> discovery` bindingが残り、Causal Discovery/Inferenceのstage-aware presentation boundaryがcanonical authorityになっていない。
- static/source existence testsはobservable normal-entry journeyを証明しない。

Root-cause classification:

| Layer | Cause | Classification |
|---|---|---|
| Direct | normal transitionがNavigation Shell render lifecycleへ必ず収束しない | frontend integration defect |
| Structural | state/history/render/presentation authority fragmented | lifecycle/authority defect |
| Structural | Family-only presentation binding | presentation binding defect |
| Verification | source existenceとobservable behaviorを混同 | acceptance coverage defect |

## 4. Target outcome

1. canonical Family/Stage Navigation Contextを適用するsingle transition authorityを持つ。
2. URL/history、application navigation state、Family selected、Stage selected、presentation surfaceを一貫して同期する。
3. normal entry、Family click、Stage click、deep link、reload、Back/Forward、legacy analysis shortcutを同一authorityへ収束する。
4. legacy analytical left navはcanonical compatibility shortcutに限定する。
5. `(family, stage)`でexisting presentation surfaceをdeterministically bindする。
6. actual Family/Stage elementsを操作するreal-browser blocking regressionを持つ。

## 5. Scope

### In scope

- `frontend/app.js` navigation lifecycle / presentation binding
- 必要な`frontend/navigation_state.js` pure navigation helper
- minimal `frontend/index.html` / `frontend/styles.css` shell lifecycle adjustment
- legacy analysis shortcut compatibility mapping
- stage-aware existing presentation activation
- affected product/static/DOM tests
- existing Playwright harnessを用いるENH-E6 browser regression
- Docker browser runner inclusion (`Dockerfile.browser-e2e`, `.dockerignore`) if required

### Out of scope

- `docs/wiki/requirement_definition/**` revision
- backend navigation catalog schema/Family canonical values revision
- scientific operation semantics/new algorithms
- Navigation StageのExecution runtime persistence
- full left-navigation IA redesign/removal
- Family-specific screen redesign/microfrontend decomposition
- unrelated frontend refactoring

## 6. Requirement changes expected

Canonical product requirement changeはない。ENH-E6では既存要求を確実に実現・検証するため、ENH-local realization requirements `E6-FR-001..009`, `E6-NFR-001..002`を定義する。これらは正本をoverrideしない。

## 7. Design changes expected

- single Navigation Transition Authority
- pure navigation modelとside-effect coordinatorのseparation
- stage-aware presentation binding
- legacy analytical entryをcanonical context resolverへ降格
- analysis-context shell show/render lifecycle明示
- fail-closed unknown/missing binding
- browser E2Eをobservable acceptanceのblocking proofへ昇格

## 8. Risk / migration / compatibility

- persistence/schema migration: none expected
- API contract change: none expected
- legacy entryは互換性のため残すがparallel authorityとしては使わない
- history semantics regressionsに注意 (`pushState/replaceState/popstate`)
- Causal mappingでDiscovery/Inference surface activationを誤るリスク
- browser test runnerが`.dockerignore`によりimageに入らない既知failure mode
- workaroundとしてreloadやsilent fallbackを入れると症状を隠すため禁止

## 9. Architecture-review applicability

- Required: `YES`
- Reason: navigation lifecycle / authority consolidation、legacy path consolidation、UI/history/presentation cross-boundary changeに該当するため。
- Evidence: `40_operator_workflows/architecture_review/`

## 10. Proposed Gate decomposition

`G01 — Observable Family / Stage Navigation Integration` の1 Gate。

PASSすると、supported entry path全体でcanonical Family/Stage navigation、observable shell、stage-aware presentation、history restoreが一貫し、後続作業がreal user behaviorへ依存可能になる。P01-P03は実装execution decompositionでありGate分割ではない。

## 11. Approval required before implementation

Human owner approval required items:

- ENH-E6がcanonical requirement/designを変更しないbugfixであること
- single transition authority方針
- legacy compatibility targets: Explore→`exploratory/profile`, Predictive→`predictive/setup`, Discovery→`causal/discovery`, Inference→`causal/identification`
- stage-aware Causal presentation mapping
- one Gate / Work Package Mode
- 06/07 freeze前のAPI READY clean negative-control preflight

Status: Human owner approved; preflight completed; G01 06/07 frozen. Template-compliance correction does not loosen the semantic contract.
