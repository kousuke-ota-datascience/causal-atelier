# ENH-E7 G04 P03 — Analysis Context / Family / Stage State

文書種別: Primary Execution Contract
Self-containment: MUST  
Information isolation: MUST  
Reporting contract: SELF_CONTAINED
Gate: G04
初回発行Trial: 01
Package: P03
Depends on: P02
Status at issuance: DRAFT_NOT_FROZEN

## 1. 目的

G03 Analysis WorkspaceへAnalysis Context restore/selectionとFamily/Stage canonical navigation stateを再結合する。

## 2. このpackageに適用するconstraint

- G03 final PASS surface architectureをblocking protected contractとする。
- G01/G02 canonical route/domain/analysis semanticsを保護する。
- backend/API/persistence semanticsを変更しない。
- package completionはGate PASSではない。
- 本PxxだけがCoding Agentのnormative workflow implementation contractである。
- Gate 06 / 07 / P00 / other Pxxを仕様補完目的で読まない。
- source / tests / config / migrationsはimplementation substrateとして調査可能。
- source factと本Pxxが矛盾し、contractをsilent reinterpretしなければ実装できない場合は停止する。
- 未承認backend/API/persistence semantic changeが必要なら停止する。

## 3. In scope

- Current Project read-only binding
- Research Context / Dataset Version / Analysis View restore/select
- Family selected state
- Stage selected state
- Family default Stage catalog integration
- Stage Contents activation

## 4. Required invariants

以下は実装方法の例ではなく、このpackageが成立させるProduct / architecture invariantである。

- Current ProjectはURL project_id authorityでread-only。
- Research Context / Dataset / Analysis View変更だけでFamily/Stage URLを書き換えない。
- invalid/incompatible inputは架空default resourceを作らずunselectedへ戻す。
- Family切替時default Stageはexisting catalog authorityから得る。
- Family/Stage URL・selected state・Stage Contentsが一致する。
- G03 horizontal/vertical layoutを維持する。

## 5. Explicitly out of scope

- Project切替をAnalysis内に追加しない。
- new backend operation/resourceを作らない。
- cross-surface historyはP04。
- Acceptance Criteria変更。
- next package実装。

## 6. Entry criteria

- current checkoutが`feature/ariadne_mvp_e7`。
- dependency `P02` が満たされている。
- `G04/P03/Trial<TRIAL_NO>` Agent Execution ReadinessがPASS。
- preflightがArchitecture / Gate contract readinessをPASSしている。
- in-scope behaviorを曖昧にする未解決source factがない。

確認不能なら`PACKAGE_BLOCKED`として停止する。

## 7. Required implementation

1. existing context restore/state codeをG03 Analysis DOMへbindする。
2. Family/Stage selected stateとcontents activationを新DOMへbindする。
3. hard-coded duplicate default-stage mappingがあれば増やさずcatalog authorityへ統合する。

## 8. Required verification predicates

focused testは単なるelement ID / label文字列の存在確認だけで完了としてはならない。以下のpredicateを直接検査する。

- analysis deep route loadでproject/context/family/stage stateが期待値。
- Family click後default Stageがcatalog value。
- context selector変更後Family/Stage pathname不変。
- selected Family/Stageがvisible contentsと一致。

## 9. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| focused product test | `uv run pytest -q tests/product/test_enh_e7_g04_p03_analysis_context_family_stage_state.py` | PASS |
| nearby regression | touched responsibilityをcoverするrepository test | PASS |
| source/diff audit | DOM ownership / visibility / event binding / dead codeを含むdiff確認 | out-of-scope semantic changeなし |

## 10. Protected contract

- G03 Projects / Project Management / Analysis surface separation。
- G03 Family horizontal / Stage vertical / obsolete shell absence。
- existing Project/domain/analysis operation semantics。
- G01/G02のrequirements / acceptance semanticsを満たしていないcurrent presentation implementation自体はprotected implementationではない。
- current non-conforming global shellを互換性維持の名目で残してはならない。

## 11. Package handoff artifact contract

本packageのCoding Agentは、他のworkflow artifactを読まずに以下1ファイルを作成する。

### 11.1 Canonical保存先 / filename

`20_implementation_reports/G04/Trial<TRIAL_NO>/packages/ENH-E7_G04_P03_Trial<TRIAL_NO>_package_execution_status.md`

directoryが存在しない場合は作成してよい。

### 11.2 必須内容

```text
# ENH-E7 G04 P03 Package Execution Status

- Enhancement: ENH-E7
- Gate: G04
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
