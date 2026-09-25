# ENH-E9 G02 P02 — Selection / Comparison Clarity

**Document class:** Work Package Execution Contract  
**Status:** `FROZEN`  
**Gate:** G02  
**Package:** P02  
**Depends on:** G02 P01 canonical package report `State: PACKAGE_COMPLETE`

## Scope

- Graph CandidatesにSelect All / Clearを提供する。
- Select All / Clearはselectionだけを変更し、adopt/fixを暗黙実行しない。
- Graph Comparisonでcurrent comparison candidateを視覚的に識別できるようにする。
- comparison対象のalgorithmとrelevant persisted parameter（現行PCではalpha等）をauthoritative persisted/current dataから簡潔に表示する。

## Protected invariants

- Graph Candidate identityを維持する。
- comparison/adoption/fix semanticsを変更しない。
- frontendでGraph scientific semanticsを再計算しない。
- GraphVersion lineage、DRAFT/FIXED semantics、FIXED immutability、designated Outcome lineageを維持する。

## Forbidden

- Select All / Clearからadopt/fixを呼ぶこと
- frontend-only推定値をauthoritative algorithm parameterとして表示すること
- candidate identityを書き換えること
- P03 scopeの先行実装
- unrelated refactor

## Focused verification

- selection-only behaviorをinteraction/unit testで確認する。
- current comparison highlightをfrontend testで確認する。
- algorithm / parameter summaryがauthoritative data由来であることをcontract/fixtureで確認する。
- comparison/adoption/fix regressionを必要範囲で実行する。
- **Browser E2Eは本Packageでは実行しない。** Browser E2EはGate 07 Independent Verificationの最終verification itemとしてのみ実行する。

## Completion criteria

- Scope内required behaviorが満たされる。
- focused verificationがPASSする。
- P01 completion evidenceが存在する。
- protected invariant regressionがない。
- scope外変更・unresolved blockerがない。
- Package checkpointを作成しcanonical package reportで `State: PACKAGE_COMPLETE` を記録できる。
