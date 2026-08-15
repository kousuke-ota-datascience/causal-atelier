# ENH-E7 G03 P02 — Projects Surface Separation

文書種別: Primary Execution Contract
Self-containment: MUST  
Information isolation: MUST  
Reporting contract: SELF_CONTAINED
Gate: G03
初回発行Trial: 01
Package: P02
Depends on: P01
Status at issuance: DRAFT_NOT_FROZEN

## 1. 目的

`/projects`と`/projects/new`をselected Project shellやAnalysis shellから独立したProjects Surfaceとして成立させる。

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

- Project List surface
- New Project surface
- Projects surface chrome / action placement
- Project selection / New Project entryのpresentation binding

## 4. Required invariants

以下は実装方法の例ではなく、このpackageが成立させるProduct / architecture invariantである。

- Project List表示時にSelected Project local navigationを表示しない。
- Project List/New Project表示時にAnalysis Context / Family / Stage navigationを表示しない。
- Project未選択時にCurrent Project / Research Context / Dataset / Analysis Viewのanalysis-input barを表示しない。
- Project ListとNew Projectはold global sidebar内の`workspace`としてではなくProjects surface rootのownership下にある。
- Project selection/createのdomain semanticsは変更しない。

## 5. Explicitly out of scope

- selected Project Overview/Context/Data/Results内容。
- Analysis Workspace内容。
- create成功後route semanticsの変更はG04。
- Acceptance Criteria変更。
- next package実装。

## 6. Entry criteria

- current checkoutが`feature/ariadne_mvp_e7`。
- dependency `P01` が満たされている。
- `G03/P02/Trial<TRIAL_NO>` Agent Execution ReadinessがPASS。
- preflightがArchitecture / Gate contract readinessをPASSしている。
- in-scope behaviorを曖昧にする未解決source factがない。

確認不能なら`PACKAGE_BLOCKED`として停止する。

## 7. Required implementation

1. Project List/New Project DOMをProjects surface rootへ移す。
2. Projects surfaceに不要なselected-project/analysis chromeへの依存を除去する。
3. existing project list/create bindingを新ownershipへ再接続する。
4. negative visibility invariantをfocused testで直接検証する。

## 8. Required verification predicates

focused testは単なるelement ID / label文字列の存在確認だけで完了としてはならない。以下のpredicateを直接検査する。

- `/projects` runtimeでProject List visibleかつPM local nav / Analysis Context / Family / Stageがnot visible。
- `/projects/new` runtimeでProject Register visibleかつPM local nav / Analysis Context / Family / Stageがnot visible。
- DOM containmentでProject List/New ProjectがProjects root配下にある。

## 9. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| focused product test | `uv run pytest -q tests/product/test_enh_e7_g03_p02_projects_surface_separation.py` | PASS |
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

`20_implementation_reports/G03/Trial<TRIAL_NO>/packages/ENH-E7_G03_P02_Trial<TRIAL_NO>_package_execution_status.md`

directoryが存在しない場合は作成してよい。

### 11.2 必須内容

```text
# ENH-E7 G03 P02 Package Execution Status

- Enhancement: ENH-E7
- Gate: G03
- Trial: <TRIAL_NO>
- Package: P02
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
