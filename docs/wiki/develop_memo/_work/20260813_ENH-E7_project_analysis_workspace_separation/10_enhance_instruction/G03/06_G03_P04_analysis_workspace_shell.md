# ENH-E7 G03 P04 — Analysis Workspace Shell

**文書種別:** Primary Execution Contract
**Self-containment:** MUST  
**Information isolation:** MUST  
**Reporting contract:** SELF_CONTAINED
**Gate:** G03
**初回発行Trial:** 01
**Package:** P04
**Depends on:** P03
**Status at issuance:** DRAFT_NOT_FROZEN

## 1. 目的

Analysis Context、Family tabs、Stage navigation、Stage ContentsをProject Managementとは別のAnalysis Workspace Shellへ再配置する。

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

- Analysis Workspace shell root
- Analysis Context top region
- Project Management return action
- Family tabs
- Stage navigation
- Stage Contents layout

## 4. Required invariants

以下は実装方法の例ではなく、このpackageが成立させるProduct / architecture invariantである。

- Analysis WorkspaceはProject Management shellの内部sectionではなく別top-level surface rootである。
- Analysis ContextはAnalysis Workspace内だけに表示する。
- Current Projectはread-only presentationである。
- Project Management return actionをAnalysis Contextと同一top regionに配置する。
- Family navigationはAnalysis Workspace内だけに存在しhorizontal layoutである。
- Stage navigationはAnalysis Workspace内だけに存在しvertical layoutである。
- Stage ContentsはStage navigationの右側main areaである。
- active Family/Stage selected stateを既存semanticsから継承する。

## 5. Explicitly out of scope

- Family/Stage taxonomy変更。
- existing stage operation semantics変更。
- history/cross-surface behaviorの最終統合はG04。
- Acceptance Criteria変更。
- next package実装。

## 6. Entry criteria

- current checkoutが`feature/ariadne_mvp_e7`。
- dependency `P03` が満たされている。
- `G03/P04/Trial<TRIAL_NO>` Agent Execution ReadinessがPASS。
- preflightがArchitecture / Gate contract readinessをPASSしている。
- in-scope behaviorを曖昧にする未解決source factがない。

確認不能なら`PACKAGE_BLOCKED`として停止する。

## 7. Required implementation

1. Analysis関連DOMをAnalysis surface rootへ集約する。
2. global common headerからAnalysis Contextを移設する。
3. Family/Stage/Contentsのlayout containerをtarget topologyに再構成する。
4. existing stage contents bindingを壊さずpresentation ownershipを移す。

## 8. Required verification predicates

focused testは単なるelement ID / label文字列の存在確認だけで完了としてはならない。以下のpredicateを直接検査する。

- analysis routeでAnalysis root visible、Projects/PM rootはnot visible。
- Analysis Context/Family/Stage/ContentsがAnalysis root descendant。
- Family itemのbounding boxesが主としてx方向に並ぶ、またはcomputed flex/grid axisがhorizontal。
- Stage itemのbounding boxesが主としてy方向に並ぶ、またはcomputed flex/grid axisがvertical。
- Stage navの右側にStage Contents main areaが存在する。

## 9. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| focused product test | `uv run pytest -q tests/product/test_enh_e7_g03_p04_analysis_workspace_shell.py` | PASS |
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

`20_implementation_reports/G03/Trial<TRIAL_NO>/packages/ENH-E7_G03_P04_Trial<TRIAL_NO>_package_execution_status.md`

directoryが存在しない場合は作成してよい。

### 11.2 必須内容

```text
# ENH-E7 G03 P04 Package Execution Status

- Enhancement: ENH-E7
- Gate: G03
- Trial: <TRIAL_NO>
- Package: P04
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
