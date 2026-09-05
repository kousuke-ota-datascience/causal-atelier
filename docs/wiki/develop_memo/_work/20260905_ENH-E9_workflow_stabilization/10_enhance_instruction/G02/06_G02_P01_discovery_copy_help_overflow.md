# ENH-E9 G02 P01 — Discovery Copy / Help / Overflow

**Document class:** Work Package Execution Contract  
**Status:** `FROZEN`  
**Gate:** G02  
**Package:** P01  
**Depends on:** G01 canonical `999_gate_decision = PASS`

## Scope

- Discovery execution領域にpurposeが分かるtitleを表示する。
- Objective / Rationaleの意味をhelp/tooltipで説明する。
- Graph Candidates componentのlocal overflowを修正し、page-level overflowを発生させない。

## Protected invariants

- Graph Candidate identityを変更しない。
- Discovery algorithm / scientific semanticsを変更しない。
- GraphVersion lifecycle、lineage、designated Outcome semanticsを変更しない。
- E8 Stage separationを変更しない。

## Forbidden

- new Discovery algorithm/API/schema/persistence
- candidate identityの再生成・frontend独自解釈
- unrelated layout/refactor
- P02/P03 scopeの先行実装

## Focused verification

- frontend unit/static/interaction testでtitle/help/overflowを検証する。
- existing Graph Candidate identity / Discovery surface regressionを必要範囲で実行する。
- `node --check frontend/app.js` 等のsyntax checkを実行する。
- **Browser E2Eは本Packageでは実行しない。** Browser E2EはGate 07 Independent Verificationの最終verification itemとしてのみ実行する。

## Completion criteria

- Scope内required behaviorが満たされる。
- focused verificationがPASSする。
- protected invariant regressionがない。
- scope外変更・unresolved blockerがない。
- Package checkpointを作成しcanonical package reportで `State: PACKAGE_COMPLETE` を記録できる。
