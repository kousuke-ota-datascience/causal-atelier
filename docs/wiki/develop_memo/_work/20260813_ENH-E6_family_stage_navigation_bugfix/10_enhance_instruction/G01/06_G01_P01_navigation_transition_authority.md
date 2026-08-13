# ENH-E6 G01 P01 — Navigation Transition Authority

- Enhancement: `ENH-E6`
- Gate: `G01`
- Package: `P01`
- Status: `APPROVED / READY_TO_START`
- Execution role: Coding Agent
- Parent Gate contract: `06_Ariadne_ENH-E6_G01_implementation_instruction.md` (`APPROVED / FROZEN`)
- Verification authority: `07_Ariadne_ENH-E6_G01_test_instruction.md` (`APPROVED / FROZEN`)
- Production baseline SHA: `5a5ced9bd6a0e62027c4058eb66ec487719bde23`

## 0. Package objective

Family / Stage `NavigationContext` を application state、browser history、Navigation Shell renderへ適用する lifecycle を単一 authority へ収束させる。

P01 の目的は「Family tabを見えるようにするための個別render call追加」ではない。各navigation entryが独立に state / history / render を変更する構造を解消し、後続P02が stage-aware presentation binding / legacy compatibility semantics を安全に接続できる transition boundary を成立させることである。

## 1. Frozen baseline defect facts

ENH-E6 preflight で以下は reproduced fact として固定済み。

- existing Playwright / Chromium harnessで `API READY`
- UIからProjectを作成・選択し Project contextを確立
- normal Explore entry 後に canonical `.../analysis/exploratory/profile` へ到達
- `#analysis-family-tabs` container count = 1
- Family button count = 0
- Stage button count = 0

source inspectionでは additionally:

- Family / Stage DOM と `renderAnalysisNavigation()` 自体は存在する
- canonical route restore pathは Navigation Shell rendererを呼ぶ
- normal workspace activation pathはNavigation Context/historyを変更し得るが同じrender lifecycleへ収束しない

したがって P01 は missing DOM/CSS 作成ではなく lifecycle integration defect を修正する。

## 2. Protected scope

変更禁止:

- `docs/wiki/requirement_definition/**`
- ENH-E5 frozen 06/07、implementation report、test report、Gate Decision、technical debt provenance
- backend Family / Stage catalog canonical semantics
- Family: `EXPLORATORY / PREDICTIVE / CAUSAL`
- canonical route shape `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`
- `Navigation Stage != Execution Stage`
- Navigation Context non-persistence

ENH-E6 planning docsは契約確認のためreadしてよいが、P01 Coding Agentが semantic contractを再設計してはならない。

## 3. Required implementation

### 3.1 Single apply authority

実装名は自由だが、概念的に次を一箇所へ集約する。

```text
applyAnalysisNavigation(context, historyMode, source)
  1. validate context against current catalog
  2. commit state.navigationContext
  3. synchronize URL / browser history according to historyMode
  4. render/update Family tabs selected state
  5. render/update current-Family Stage sidebar selected state
  6. trigger presentation activation through an explicit boundary
  7. refresh route-dependent operation availability
  8. apply deterministic focus where required
```

P01時点で presentation binding の最終 Causal stage mapping を新規確定してはならない。presentation activation は後続P02が差し替え可能な明示的 boundary とする。

### 3.2 Entry convergence

最低限、次のentryが Navigation Context apply logicを重複実装しない状態へする。

- Family tab click
- Stage click
- canonical route initial restore
- reload restore
- browser `popstate`
- normal analysis workspace activationからcanonical contextを適用するpath

entry handlerは target context / history mode / source の決定に限定し、state + history + shell renderを個別に再実装しない。

### 3.3 History modes

最低限次を区別する。

- user navigation: `push`
- normalization / compatibility transition: `replace`
- initial canonical restore / `popstate`: `none`

`popstate`処理が新しいhistory entryを生成してはならない。同一targetへの不要なduplicate entryを作らない。

### 3.4 Observable shell lifecycle

analysis contextへ Navigation Context がapplyされた直後、reloadを要求せず Family / Stage shell をrender/updateできること。

non-analysis workspaceでは空のanalysis shellを誤ってprimary navigationとして表示しない。

## 4. Allowed change surface

Primary candidates:

- `frontend/app.js`
- `frontend/navigation_state.js`
- P01を成立させるために必要な既存frontend helper
- focused product/DOM regression tests under `tests/product/`

`frontend/index.html` / `frontend/styles.css` は lifecycle integrationに本当に必要な場合のみ変更可。baselineにはDOM/CSSが存在するため、単なる再作成をしてはならない。

Backend production code、browser E2E image/harness本体はP01では変更しない。

## 5. Explicitly out of P01 scope

次は P02 / P03 の責務であり、P01で完了扱いしない。

- final `(family, stage) -> presentation surface` binding
- `Causal Discovery -> causal/discovery` / `Causal Inference -> causal/identification` のlegacy shortcut最終適用
- Family-only `ANALYSIS_WORKSPACES.causal = discovery` の最終廃止・stage-aware replacement
- new ENH-E6 Playwright runner
- `Dockerfile.browser-e2e` / `.dockerignore` のE6 runner integration
- Gate全体のbrowser PASS判定

P01実装上、後続P02のためのpresentation boundaryを追加することは可。ただしP02 semantic mappingを先取りして固定しない。

## 6. P01 focused acceptance

P01 checkpointとして最低限次を証明する。

1. Navigation Context apply lifecycle のsingle authorityが存在する。
2. Family click / Stage click / canonical restore / `popstate` / normal analysis activation が同authorityへ収束する。
3. normal analysis activation後に shell render/update lifecycle が実行される構造になっている。
4. `popstate` は新規history entryを作らない。
5. invalid catalog/context はsilent fallbackせず既存error semanticsまたはexplicit errorへ収束する。
6. P01変更で既存E5 navigation-state / route / history contract testを弱めていない。
7. P01のために source-string assertionを追加する場合も、それをGate browser proofの代替と表現しない。

P01 checkpoint PASS は G01 Gate PASS ではない。

## 7. Verification to run and report

Coding Agentはrepositoryで既存test conventionを確認し、最低限以下の関係testを実行する。

- Navigation state parse / serialize / history tests
- ENH-E5 G01 navigation shell regression
- ENH-E5 G01 history / accessibility regression
- P01で追加・変更した focused product/DOM tests

テストコマンドは推測で報告せず、実際に実行した exact command と exit status を記録する。

browser E2E full Gate journeyはP03でblocking実行するため、P01単独では必須ではない。ただし既存browser harnessを壊す変更を意図的に入れてはならない。

## 8. Coding constraints

- minimal semantic diffを優先する。
- `activateWorkspace()` に `renderAnalysisNavigation()` を1行足すだけで完了としてはならない。
- full backend catalogをfrontendへ複製しない。
- Navigation StageをExecution Stageへ変換・persistしない。
- test skip / xfail / assertion weakening禁止。
- unrelated refactor、visual redesign、naming cleanupを混在させない。

## 9. Checkpoint report

P01終了時、Coding Agentは少なくとも以下を報告する。

- changed files
- implemented transition authorityの責務とentry convergence一覧
- baseline root causeと修正の対応
- exact tests executed / result
- remaining P02/P03 work
- known risk / unresolved issue
- working tree / commit identity（利用可能な範囲）

Gate PASS、ANOM-E5-001 close、ENH-E6完了とは表現しない。

## 10. Stop conditions

以下が判明した場合は勝手にscopeを拡張せず停止して報告する。

- backend canonical catalog/route contract自体の変更が必要
- `docs/wiki/requirement_definition/**` の改定が必要に見える
- frozen legacy mapping / Causal mappingと矛盾する既存仕様を発見
- P01だけでは成立しない大規模frontend architecture migrationが必要
- baseline production codeが `5a5ced9...` からENH-E6 planning docs以外にも予期せず変更されている
