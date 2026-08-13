# ENH-E7 G02 P06 — Legacy Cutover / Integration / Regression

**文書種別:** Primary Execution Contract  
**Self-containment:** MUST  
**Gate:** G02  
**初回発行Trial:** 01  
**Package:** P06  
**Depends on:** P03,P04,P05  
**Status at issuance:** DRAFT_NOT_FROZEN

## 1. 目的

重複legacy analytical UI navigationを削除し、legacy URL compatibility / browser history / resource behaviorを統合してTrial candidateを準備する。

## 2. このpackageに適用するconstraint

- G01 final PASS contractを保護する。
- ENH-E6 canonical Analysis route / Family / Stage semanticsを保護する。
- Stageはpresentation/navigation boundaryであり、backend execution modelを暗黙変更しない。
- package completionはGate PASSではない。
- **本PxxだけがCoding Agentのnormative workflow implementation contractである。**
- Gate 06 / 07 / P00 / other Pxxを仕様補完目的で読まない。
- source / tests / config / migrationsはimplementation substrateとして調査可能。
- 未承認backend/API/persistence semantic changeが必要なら停止する。

## 3. In scope

- old analytical sidebar shortcut削除
- legacy URL → canonical normalization
- Project → Analysis → Project
- Analysis → Results
- deep link / reload / Back / Forward
- resource route
- existing operation availability
- ENH-E6 protected regression

## 4. Explicitly out of scope

- compatibility URLを削除しない。
- frozen designが許可しない限り壊れたexisting operationをempty stateで隠さない。

加えてAcceptance Criteria変更、unrelated cleanup、next package実装はout of scope。

## 5. Entry criteria

- current checkoutが`feature/ariadne_mvp_e7`。
- G01 final PASS済み。
- `G02/P06/Trial01` Agent Execution Readiness PASS。
- dependency `P03,P04,P05` が満たされている。
- Architecture Review / Gate contractがFROZEN。
- implementationを曖昧にするsource unresolved itemがない。

確認不能なら`PACKAGE_BLOCKED`。

## 6. Required implementation

1. in-scope responsibilityを特定する範囲でcurrent source/testsを調査する。
2. protected semanticsを維持して実装する。
3. focused testをrepository conventionに従って追加・更新する。
4. UI taxonomyを埋めるためのsubstitute backend semanticsを作らない。
5. source factとcontractが矛盾すれば停止して報告する。

## 7. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| focused product test | `uv run pytest -q tests/product/test_enh_e7_g02_p06_legacy_cutover_integration.py` | PASS |
| nearby regression | touched responsibilityのrepository test | PASS |
| source/diff audit | ownership/navigation/semantics確認 | out-of-scope semantic changeなし |

## 8. Protected contract

G01 final PASS contract、およびENH-E6 canonical Analysis route / Family / Stage navigation semantics。

## 9. Reporting

implementation checkpoint full SHAを固定し、checkpoint report / package execution status reportを作成する。

## 10. Package completion criteria

G02 gate-wide self-checkとcritical browser journeyがPASSする。

加えてfocused verification完了、unresolved blockerなし、checkpoint full SHA固定、required report作成済み。

## 11. External reference policy

Coding Agentはsource/test/runtime factを調査してよい。
Gate 06 / Gate 07 / P00 / other Pxx / 00 / 20 / 30を仕様補完目的で読まない。

本Pxxが不十分またはverified source factと矛盾する場合は
`PACKAGE_BLOCKED_CONTRACT_AMBIGUITY`として停止する。

## 12. Stop rule

- scope完了 → `PACKAGE_COMPLETE`
- 継続不能 → `PACKAGE_BLOCKED`
- Gate PASS/FAILは宣言しない
- next packageへ自動継続しない
