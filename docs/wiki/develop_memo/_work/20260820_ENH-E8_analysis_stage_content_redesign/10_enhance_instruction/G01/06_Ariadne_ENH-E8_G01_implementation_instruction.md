# Ariadne ENH-E8 G01 Implementation Contract

- Document class: Primary Execution Contract
- Contract status: `FROZEN`
- Status: `FROZEN`
- Gate: `G01`
- Execution Mode: `SINGLE_EXECUTION`
- Baseline: `386521d18e9c5cc4d42fb99c97c212430908afc3`

## 1. Gate claim

Selected ProjectからProject Listへ戻る明示的parent navigationを実装し、browser historyのoriginに依存せずcanonical `/projects` をtargetとする。

## 2. Required behavior

1. return actionをSelected Project shellの4 local section（Overview / Research Context / Data / Results / Lineage）で表示する。
2. user activationはexisting application/router transition authorityを介してcanonical Project List `/projects` へ遷移する。
3. target決定に `history.back()` を使わない。
4. `/projects/{project_id}/{section}` へdirect entryした場合でもreturn actionが成立する。
5. user activationはnormal PUSH semanticsとし、BackでSelected Project、Forwardで`/projects`を復元する。
6. existing Project local navigation、archive、Analysis Workspace launcher/navigationを壊さない。
7. accessible nameとkeyboard activationを提供する。

## 3. Implementation boundary

主な想定対象:

- `frontend/index.html`
- `frontend/app.js`
- `frontend/styles.css`

existing `frontend/project_navigation.js` のcollection route serialization / authorityを使用する。

route module変更は、既存canonical helperのexposeが必要な場合に限定する。alternative routeを追加しない。

## 4. Protected non-goals

- API変更なし
- DB/persistence変更なし
- `src/ariadne/**` のdomain/runtime semantics変更なし
- existing `/projects` collection route以外のroute grammar変更なし

## 5. Browser E2E harness ownership

G01 implementationは、次のfrozen commandで実行可能なBrowser E2E scriptをcandidateに含める。

`tests/browser_e2e/run_enh_e8_g01_project_return.py`

scriptはbaselineのexisting Browser E2E conventionに従い、real Chromiumでdirect entry、Project List return、Back/Forwardを検証し、evidenceを `test-results/browser_e2e/` へ保存する。

## 6. Self-check

completion report作成前に以下を確認する。

- deterministic route behavior
- direct-entry behavior
- Back/Forward behavior
- accessibility
- existing Project/Analysis navigation regression

## 7. Exit

implementation evidenceのみを作る。Gate PASSを宣言しない。

Test Agent実行前にTrial implementation completion reportでFixed Trial Candidate SHAを確定する。
