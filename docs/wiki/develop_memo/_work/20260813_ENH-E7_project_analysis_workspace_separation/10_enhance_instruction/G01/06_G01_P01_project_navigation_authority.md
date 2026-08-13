# ENH-E7 G01 P01 — Project Navigation Authority

**文書種別:** Primary Execution Contract  
**Self-containment:** MUST  
**Gate:** G01  
**初回発行Trial:** 01  
**Package:** P01  
**Depends on:** NONE  
**Status at issuance:** DRAFT_NOT_FROZEN

## 1. 目的

Project routeのparse / serialize / normalization / browser history behaviorを作成・集約する。

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

- `/projects` / `/projects/new` / `/projects/<id>/overview|context|data|results` routing
- `/projects/<id>` → `/overview` normalization
- direct-load / reload / history contract

## 4. Explicitly out of scope

- Analysis Family/Stage taxonomyを変更しない。
- approved Architecture amendmentなしにAnalysisNavigationへProject route ownershipを持たせない。

加えて以下はout of scope。
- Acceptance Criteria変更
- unrelated cleanup / refactoring
- next package実装

## 5. Entry criteria

- current checkoutが`feature/ariadne_mvp_e7`。
- `G01/P01/Trial01`のAgent Execution ReadinessがPASS。
- dependency `NONE` が満たされている。
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
| focused product test | `uv run pytest -q tests/product/test_enh_e7_g01_p01_project_navigation_authority.py` | PASS |
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

Focused Project route contract testがPASSする。

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
