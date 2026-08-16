# ENH-E7 G04 P04 — Cross-surface Routing / Browser History

**文書種別:** Primary Execution Contract
**Self-containment:** MUST  
**Information isolation:** MUST  
**Reporting contract:** SELF_CONTAINED
**Gate:** G04
**初回発行Trial:** 01
**Package:** P04
**Depends on:** P02,P03
**Status at issuance:** DRAFT_NOT_FROZEN

## 1. 目的

Project Management ↔ Analysis Workspace ↔ Resultsのcross-surface navigationとdeep-link/reload/Back/Forwardを統合する。

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

- Project Management→Analysis launcher
- Analysis→Project Management return
- Analysis→Results / Lineage
- deep link / reload
- Back / Forward
- surface/state restoration

## 4. Required invariants

以下は実装方法の例ではなく、このpackageが成立させるProduct / architecture invariantである。

- cross-surface transitionでcurrent Project identityを失わない。
- Analysis→Project Management returnはselected ProjectのProject Management routeへ戻る。
- Analysis→Resultsはselected Projectの`/results`へ遷移する。
- Back/ForwardでURLだけでなくvisible top-level surfaceとselected stateも同期する。
- history navigationでold global shellやstale previous surfaceが同時visibleにならない。

## 5. Explicitly out of scope

- legacy URL normalization詳細はP05。
- operation behavior修復はP05。
- Acceptance Criteria変更。
- next package実装。

## 6. Entry criteria

- current checkoutが`feature/ariadne_mvp_e7`。
- dependency `P02,P03` が満たされている。
- `G04/P04/Trial<TRIAL_NO>` Agent Execution ReadinessがPASS。
- preflightがArchitecture / Gate contract readinessをPASSしている。
- in-scope behaviorを曖昧にする未解決source factがない。

確認不能なら`PACKAGE_BLOCKED`として停止する。

## 7. Required implementation

1. G03 surface activationとexisting history handlersを統合する。
2. push/replaceの責務をroute semanticsに合わせて整理する。
3. popstate/reload時にroute-authoritative restoreを行う。
4. cross-surface browser testを追加する。

## 8. Required verification predicates

focused testは単なるelement ID / label文字列の存在確認だけで完了としてはならない。以下のpredicateを直接検査する。

- PM→Analysis→PMでpathname/project/surfaceが整合。
- Analysis→ResultsでPM results surfaceへ到達。
- reload後同route/stateを復元。
- Back/Forward各stepでvisible surface rootがURLと一致。
- duplicate history entryがない。

## 9. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| focused product test | `uv run pytest -q tests/product/test_enh_e7_g04_p04_cross_surface_history_navigation.py` | PASS |
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

`20_implementation_reports/G04/Trial<TRIAL_NO>/packages/ENH-E7_G04_P04_Trial<TRIAL_NO>_package_execution_status.md`

directoryが存在しない場合は作成してよい。

### 11.2 必須内容

```text
# ENH-E7 G04 P04 Package Execution Status

- Enhancement: ENH-E7
- Gate: G04
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
