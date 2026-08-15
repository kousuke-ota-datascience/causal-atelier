# ENH-E7 G03 P06 — Surface Architecture Integration

文書種別: Primary Execution Contract
Self-containment: MUST  
Information isolation: MUST  
Reporting contract: SELF_CONTAINED
Gate: G03
初回発行Trial: 01
Package: P06
Depends on: P05
Status at issuance: DRAFT_NOT_FROZEN

## 1. 目的

G03の全surface topologyを統合し、Candidate Assembly前にDOM ownership・runtime visibility・layout・protected semantic smokeを閉じる。

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

- Projects / Project Management / Analysis top-level surface integration
- route fixtureごとのsurface activation smoke
- DOM containment / runtime visibility regression
- success browser structural journey
- candidate cleanup audit

## 4. Required invariants

以下は実装方法の例ではなく、このpackageが成立させるProduct / architecture invariantである。

- 3 surfaceのownershipが相互排他的である。
- Project surfaceではAnalysis-only chromeを表示しない。
- Analysis surfaceではProject Management local navを表示しない。
- Family horizontal / Stage vertical topologyを維持する。
- old global shell / duplicate navigationが復活していない。
- G03のためのtemporary compatibility branch / duplicate DOMを残さない。

## 5. Explicitly out of scope

- G04のroot normalization/history semantics追加。
- new backend behavior。
- unrelated visual polish。
- Acceptance Criteria変更。
- next package実装。

## 6. Entry criteria

- current checkoutが`feature/ariadne_mvp_e7`。
- dependency `P05` が満たされている。
- `G03/P06/Trial<TRIAL_NO>` Agent Execution ReadinessがPASS。
- preflightがArchitecture / Gate contract readinessをPASSしている。
- in-scope behaviorを曖昧にする未解決source factがない。

確認不能なら`PACKAGE_BLOCKED`として停止する。

## 7. Required implementation

1. 全G03 structural invariantを統合testで再確認する。
2. browser harnessでProjects→PM→Analysisのsurface visibilityを確認する。
3. 成功時もsurfaceごとのscreenshot evidenceを生成できるtestを追加する。
4. candidate diffをdead/duplicate presentation code観点で監査する。

## 8. Required verification predicates

focused testは単なるelement ID / label文字列の存在確認だけで完了としてはならない。以下のpredicateを直接検査する。

- Projects/PM/Analysisそれぞれでvisible top-level surface rootが1つ。
- browser runtimeでnegative invariantがすべて成立。
- Family/Stage orientationをcomputed layout/bounding boxで確認。
- console/page errorなし。
- protected route/domain smoke PASS。

## 9. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| focused product test | `uv run pytest -q tests/product/test_enh_e7_g03_p06_surface_architecture_integration.py` | PASS |
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

`20_implementation_reports/G03/Trial<TRIAL_NO>/packages/ENH-E7_G03_P06_Trial<TRIAL_NO>_package_execution_status.md`

directoryが存在しない場合は作成してよい。

### 11.2 必須内容

```text
# ENH-E7 G03 P06 Package Execution Status

- Enhancement: ENH-E7
- Gate: G03
- Trial: <TRIAL_NO>
- Package: P06
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
