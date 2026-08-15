# ENH-E7 G03 P01 — Top-level Surface Activation Authority

文書種別: Primary Execution Contract
Self-containment: MUST  
Information isolation: MUST  
Reporting contract: SELF_CONTAINED
Gate: G03
初回発行Trial: 01
Package: P01
Depends on: G02 PASS
Status at issuance: DRAFT_NOT_FROZEN

## 1. 目的

route/stateからProjects / Project Management / Analysisのtop-level presentation surfaceを一意に決定・activateするauthorityを作る。

## 2. このpackageに適用するconstraint

- G01/G02 normative requirementsとverified application semanticsを保護する。
- current global shell / sidebar presentation topologyはprotected implementationではない。
- backend/API/persistence/domain semanticsを変更しない。
- package completionはGate PASSではない。
- 本PxxだけがCoding Agentのnormative workflow implementation contractである。
- Gate 06 / 07 / P00 / other Pxxを仕様補完目的で読まない。
- source / tests / config / migrationsはimplementation substrateとして調査可能。
- source factと本Pxxが矛盾し、contractをsilent reinterpretしなければ実装できない場合は停止する。
- 未承認backend/API/persistence semantic changeが必要なら停止する。

## 3. In scope

- top-level surface classification / activation
- surface activation時のaria/hidden/active state
- incompatible shellの同時表示防止
- existing route parserとのpresentation-level integration

## 4. Required invariants

以下は実装方法の例ではなく、このpackageが成立させるProduct / architecture invariantである。

- 任意時点でprimary top-level surfaceはProjects / Project Management / Analysisの高々1つだけactiveである。
- `/projects`と`/projects/new`はProjects surface kindへ分類する。
- `/projects/<id>/{overview,context,data,results}`はProject Management surface kindへ分類する。
- `/projects/<id>/analysis/<family>/<stage>`および既存canonical resource analysis routeはAnalysis surface kindへ分類する。
- surface判定を複数箇所の独立booleanやCSS selector条件へ分散させない。単一authorityまたは等価な一貫した責務へ集約する。

## 5. Explicitly out of scope

- 各surfaceの内部layout実装はP02-P04。
- old shell cleanupはP05。
- route semanticsそのものの変更はG04。
- Acceptance Criteria変更。
- next package実装。

## 6. Entry criteria

- current checkoutが`feature/ariadne_mvp_e7`。
- dependency `G02 PASS` が満たされている。
- `G03/P01/Trial<TRIAL_NO>` Agent Execution ReadinessがPASS。
- preflightがArchitecture / Gate contract readinessをPASSしている。
- in-scope behaviorを曖昧にする未解決source factがない。

確認不能なら`PACKAGE_BLOCKED`として停止する。

## 7. Required implementation

1. current sourceのroute restore / workspace activation責務を特定する。
2. top-level surface activation authorityを導入または既存authorityを整理する。
3. surface activationとinternal workspace activationを同一概念として混同しない。
4. existing route behaviorを壊さないfocused testを追加する。

## 8. Required verification predicates

focused testは単なるelement ID / label文字列の存在確認だけで完了としてはならない。以下のpredicateを直接検査する。

- route fixtureごとに期待surface kindが一意に返る。
- runtimeで2つ以上のtop-level surface rootが同時visibleにならない。
- Project internal section切替がtop-level surface kindを不必要に変えない。

## 9. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| focused product test | `uv run pytest -q tests/product/test_enh_e7_g03_p01_top_level_surface_activation_authority.py` | PASS |
| nearby regression | touched responsibilityをcoverするrepository test | PASS |
| source/diff audit | DOM ownership / visibility / event binding / dead codeを含むdiff確認 | out-of-scope semantic changeなし |

## 10. Protected contract

- canonical Project routes / lifecycle semantics。
- canonical Analysis route / Family / Stage catalog semantics。
- existing analysis operations / resource behavior。
- G01/G02のrequirements / acceptance semanticsを満たしていないcurrent presentation implementation自体はprotected implementationではない。
- current non-conforming global shellを互換性維持の名目で残してはならない。

## 11. Package handoff artifact contract

本packageのCoding Agentは、他のworkflow artifactを読まずに以下1ファイルを作成する。

### 11.1 Canonical保存先 / filename

`20_implementation_reports/G03/Trial<TRIAL_NO>/packages/ENH-E7_G03_P01_Trial<TRIAL_NO>_package_execution_status.md`

directoryが存在しない場合は作成してよい。

### 11.2 必須内容

```text
# ENH-E7 G03 P01 Package Execution Status

- Enhancement: ENH-E7
- Gate: G03
- Trial: <TRIAL_NO>
- Package: P01
- State: PACKAGE_COMPLETE | PACKAGE_BLOCKED
- Branch: feature/ariadne_mvp_e7
- Implementation HEAD full SHA: <40-hex SHA or NOT_RECORDED>

## 実施したscope
## Changed files / responsibility
## Required invariant conclusion
## Focused verification
  - exact command / method
  - exit code / result
## Remaining / blocker
## Scope guard確認
```

## 12. Stop condition

`PACKAGE_COMPLETE`または明示的`PACKAGE_BLOCKED`で停止する。Gate PASS/FAILを宣言しない。
