# ENH-E7 G01 P07 — Project Integration / Regression

**文書種別:** Primary Execution Contract  
**Self-containment:** MUST  
**Gate:** G01  
**初回発行Trial:** 01  
**Package:** P07  
**Depends on:** P02,P03,P04,P05,P06  
**Status at issuance:** DRAFT_NOT_FROZEN

## 1. 目的

G01 Project surfaceを統合し、Candidate Assembly前にbrowser/history/domain regressionを確認する。

## 2. このpackageに適用するconstraint

- Project ManagementとAnalysis Workspaceは異なるnavigation scopeである。
- existing domain/execution semanticsを保護する。
- ENH-E6 canonical Analysis route / Family / Stage semanticsをregressionさせない。
- package completionはGate PASSではない。
- **本PxxだけがこのCoding executionのnormative workflow implementation contractである。**
- parent 06 / 07 / P00 / other PxxはHuman traceability用であり、仕様補完目的で読まない。
- source / tests / config / migrationsはimplementation substrateとして調査可能。
- 未承認backend/API/persistence semantic changeが必要なら停止する。

## 3. In scope

- Project create → Overview
- Overview / Context / Data / Results navigation
- direct link / reload / Back / Forward
- Project/Context/Data/Results regression
- protected Analysis regression

## 4. Explicitly out of scope

- G02 replacement surface成立前にlegacy analytical UI shortcutを削除しない。

加えて以下はout of scope。
- Acceptance Criteria変更
- unrelated cleanup / refactoring
- next package実装

## 5. Entry criteria

- current checkoutが`feature/ariadne_mvp_e7`。
- `G01/P07/Trial01`のAgent Execution ReadinessがPASS。
- dependency `P02,P03,P04,P05,P06` が満たされている。
- Architecture Review / Gate contractがexecution前にFROZEN。
- in-scope behaviorを曖昧にする未解決source factがない。

確認不能なら`PACKAGE_BLOCKED`として停止する。

## 6. Required implementation

1. §3 responsibilityを特定する範囲でcurrent source/testsを調査する。
2. §2/§4を維持して§3 behaviorを実装する。
3. repository conventionに従ってfocused testを追加・更新する。
4. substitute backend semanticsを作らない。
5. source factとcontractが矛盾する場合はsilent reinterpretせず停止する。

## 7. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| focused product test | `uv run pytest -q tests/product/test_enh_e7_g01_p07_project_integration_regression.py` | PASS |
| nearby regression | touched responsibilityをcoverするrepository test | PASS |
| source/diff audit | ownership/navigationを含むdiff確認 | out-of-scope semantic changeなし |

## 8. Protected contract

- Protected upstream: ENH-E6 G01 PASS candidate `575cdd139aea09d4f19b46ab6a6d38545f645c71` が確立したcanonical Analysis Family/Stage navigation / transition semantics。
- intentional open Transition Debtは導入しない。
- legacy URL compatibilityを削除しない。

## 9. Reporting

package完了時にimplementation checkpoint full SHAを固定し、
implementation checkpoint reportとpackage execution status reportを作成する。

## 10. Package completion criteria

G01 gate-wide self-checkとcritical browser journeyがPASSする。

加えてfocused verification完了、unresolved blockerなし、checkpoint full SHA固定、required report作成済みであること。

## 11. External reference policy

Coding Agentはsource/test/runtime factを調査してよい。
Gate 06 / Gate 07 / P00 / other Pxx / 00 / 20 / 30をpackage specification補完目的で読まない。

本Pxxが不十分またはverified source factと矛盾する場合は
`PACKAGE_BLOCKED_CONTRACT_AMBIGUITY`として停止する。

## 12. Stop rule

- scope完了 → `PACKAGE_COMPLETE`
- 安全に継続不能 → `PACKAGE_BLOCKED`
- Gate PASS/FAILを宣言しない
- 別packageへ自動継続しない
