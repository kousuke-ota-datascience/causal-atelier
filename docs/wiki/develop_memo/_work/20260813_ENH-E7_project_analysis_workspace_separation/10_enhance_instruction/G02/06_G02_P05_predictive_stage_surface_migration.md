# ENH-E7 G02 P05 — Predictive Stage Surface Migration

**文書種別:** Primary Execution Contract  
**Self-containment:** MUST  
**Gate:** G02  
**初回発行Trial:** 01  
**Package:** P05  
**Depends on:** P01,P02  
**Status at issuance:** DRAFT_NOT_FROZEN

## 1. 目的

existing Predictive presentationをSetup / Train / Predict / Metrics / Explainability / Model Managementへ移設し、新execution modelを作らない。

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

- Setup: task/features/split
- Train: training/status/result
- Predict: existing prediction output（存在する場合）
- Metrics: evaluation
- Explainability: explanation
- Model Management: model card/management

## 4. Explicitly out of scope

- Prediction Task → Split → Training → Evaluation → Explanation → Model Card semanticsを保護する。
- Predict Stageだけを理由に専用Predict backend executionを作らない。

加えてAcceptance Criteria変更、unrelated cleanup、next package実装はout of scope。

## 5. Entry criteria

- current checkoutが`feature/ariadne_mvp_e7`。
- G01 final PASS済み。
- `G02/P05/Trial01` Agent Execution Readiness PASS。
- dependency `P01,P02` が満たされている。
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
| focused product test | `uv run pytest -q tests/product/test_enh_e7_g02_p05_predictive_stage_surface_migration.py` | PASS |
| nearby regression | touched responsibilityのrepository test | PASS |
| source/diff audit | ownership/navigation/semantics確認 | out-of-scope semantic changeなし |

## 8. Protected contract

G01 final PASS contract、およびENH-E6 canonical Analysis route / Family / Stage navigation semantics。

## 9. Reporting

implementation checkpoint full SHAを固定し、checkpoint report / package execution status reportを作成する。

## 10. Package completion criteria

existing Predictive execution regressionとmapped presentation operabilityがPASSする。

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
