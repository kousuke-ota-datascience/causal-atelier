# ENH-E7 G03 P03 — Project Management Shell

文書種別: Primary Execution Contract
Self-containment: MUST  
Information isolation: MUST  
Reporting contract: SELF_CONTAINED
Gate: G03
初回発行Trial: 01
Package: P03
Depends on: P02
Status at issuance: DRAFT_NOT_FROZEN

## 1. 目的

selected ProjectのOverview / Research Context / Data / ResultsをProject Management ShellとProject-local vertical navigationへ再配置する。

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

- Project Management shell root
- selected Project header/identity presentation
- Overview / Research Context / Data / Results local navigation
- project section content container

## 4. Required invariants

以下は実装方法の例ではなく、このpackageが成立させるProduct / architecture invariantである。

- Project Management local navigationはselected Project routeでのみ表示する。
- local navigationはOverview / Research Context / Data / Results・LineageのProject-local hierarchyである。
- Project Management Shell内にAnalysis Context / Family / Stage navigationを置かない。
- old global sidebarのProject Management/Research Context/Project Data/ResultsをProject-local navの代替として使用しない。
- local navigationはvertical layoutである。

## 5. Explicitly out of scope

- Analysis launcher/history semanticsの最終統合はG04。
- section内部domain behaviorの再設計。
- Analysis shell。
- Acceptance Criteria変更。
- next package実装。

## 6. Entry criteria

- current checkoutが`feature/ariadne_mvp_e7`。
- dependency `P02` が満たされている。
- `G03/P03/Trial<TRIAL_NO>` Agent Execution ReadinessがPASS。
- preflightがArchitecture / Gate contract readinessをPASSしている。
- in-scope behaviorを曖昧にする未解決source factがない。

確認不能なら`PACKAGE_BLOCKED`として停止する。

## 7. Required implementation

1. selected Project sectionsをProject Management shell ownershipへ移す。
2. Project-local navigationをDOM上もProject Management shell配下に置く。
3. 既存section content bindingを維持してpresentation ownershipだけを修正する。
4. vertical navigationとnegative Analysis visibilityを検証する。

## 8. Required verification predicates

focused testは単なるelement ID / label文字列の存在確認だけで完了としてはならない。以下のpredicateを直接検査する。

- selected Project routeでPM shell visible、Projects root/Analysis rootはnot visible。
- PM local navがPM shell descendantであり、Overview/Context/Data/Resultsを含む。
- PM local nav itemsのbounding boxまたはcomputed layoutがvertical stackを示す。
- Analysis Context/Family/StageがPM surfaceではnot visible。

## 9. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| focused product test | `uv run pytest -q tests/product/test_enh_e7_g03_p03_project_management_shell.py` | PASS |
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

`20_implementation_reports/G03/Trial<TRIAL_NO>/packages/ENH-E7_G03_P03_Trial<TRIAL_NO>_package_execution_status.md`

directoryが存在しない場合は作成してよい。

### 11.2 必須内容

```text
# ENH-E7 G03 P03 Package Execution Status

- Enhancement: ENH-E7
- Gate: G03
- Trial: <TRIAL_NO>
- Package: P03
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
