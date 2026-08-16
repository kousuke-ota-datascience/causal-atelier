# ENH-E7 G04 P06 — Full Integration / Cleanup

**文書種別:** Primary Execution Contract
**Self-containment:** MUST  
**Information isolation:** MUST  
**Reporting contract:** SELF_CONTAINED
**Gate:** G04
**初回発行Trial:** 01
**Package:** P06
**Depends on:** P05
**Status at issuance:** DRAFT_NOT_FROZEN

## 1. 目的

G04全behaviorを統合し、stale handler/selector/temporary routing shimを除去してcorrected ENH-E7 Trial candidateを準備する。

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

- full Projects→PM→Analysis→Results→PM journey
- root/deep/legacy entry regression
- Back/Forward/reload
- console/page error cleanup
- duplicate event/history binding audit
- temporary compatibility code cleanup

## 4. Required invariants

以下は実装方法の例ではなく、このpackageが成立させるProduct / architecture invariantである。

- G03 surface architectureが全journeyで維持される。
- 各URLでvisible top-level rootが1つ。
- route/state/historyが二重handlerで重複更新されない。
- stale selectorによるconsole/page errorがない。
- G04用temporary fallbackを最終candidateに残さない。

## 5. Explicitly out of scope

- new feature追加。
- visual polish。
- workflow/test report作成。
- Acceptance Criteria変更。
- next package実装。

## 6. Entry criteria

- current checkoutが`feature/ariadne_mvp_e7`。
- dependency `P05` が満たされている。
- `G04/P06/Trial<TRIAL_NO>` Agent Execution ReadinessがPASS。
- preflightがArchitecture / Gate contract readinessをPASSしている。
- in-scope behaviorを曖昧にする未解決source factがない。

確認不能なら`PACKAGE_BLOCKED`として停止する。

## 7. Required implementation

1. full integration product testを追加・更新する。
2. repository browser harnessでsuccess journeyを実行可能にする。
3. event listener/history mutationのduplicate source auditを行う。
4. dead routing/presentation compatibility codeを削除する。

## 8. Required verification predicates

focused testは単なるelement ID / label文字列の存在確認だけで完了としてはならない。以下のpredicateを直接検査する。

- `/`→Projects→select→PM→Analysis→Family/Stage→Results→PM` journey PASS。
- Back/Forward/reload PASS。
- console/page error 0。
- G03 structural Browser assertions PASS。
- protected full regression PASS。

## 9. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| focused product test | `uv run pytest -q tests/product/test_enh_e7_g04_p06_full_integration_cleanup.py` | PASS |
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

`20_implementation_reports/G04/Trial<TRIAL_NO>/packages/ENH-E7_G04_P06_Trial<TRIAL_NO>_package_execution_status.md`

directoryが存在しない場合は作成してよい。

### 11.2 必須内容

```text
# ENH-E7 G04 P06 Package Execution Status

- Enhancement: ENH-E7
- Gate: G04
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
