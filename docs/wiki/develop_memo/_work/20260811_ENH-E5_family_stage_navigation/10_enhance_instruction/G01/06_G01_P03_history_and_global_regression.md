# Ariadne ENH-E5 G01 — P03 History, Accessibility and Global Regression

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G01`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `acc43f744360e25fc504f608716bed2023817a29`
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

deep-link/history/reload/focus/accessibilityを完成させ、Navigation state authorityをbrowser routeへ一意化する。

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


## 2. Accessibility / history semantics

- direct URL open、reload、browser back/forwardでFamily/Stage/resource contextをdeterministically復元。
- UI local stateだけをcurrent Family/Stage authorityにしない。
- route change後focusはmain heading/primary region等のdeterministic targetへ移す。
- keyboardのみでFamily/Stage/actionへ到達・操作可能。
- icon-only controlにもaccessible name。
- form errorはinputとprogrammatic associationを持つ。
- state/availability/warningを色だけで表現しない。
- normal text contrast >= 4.5:1。
- large text/UI graphics/focus >= 3:1。
- full legacy UI retroactive remediationはscope外。E5変更surfaceを対象とする。

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

- direct/open/reload/back-forwardがrouteとactive navigationを同期。
- Stage/resource deep link保持。
- explicit route/resource Family mismatchはsilent normalizationなし。
- keyboard/focus/name/error/non-color/contrast evidence。
- current global workspace navigation regression green。

## Completion evidence

- changed production / test / schema / migration files
- focused test commands and results
- relevant regression commands and results
- candidate SHA / checkpoint SHA
- blocker status (`NONE` or explicit blocker)
