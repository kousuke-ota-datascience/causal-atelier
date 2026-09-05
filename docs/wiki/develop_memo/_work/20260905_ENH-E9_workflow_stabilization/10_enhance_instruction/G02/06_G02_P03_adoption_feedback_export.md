# ENH-E9 G02 P03 — Adoption Feedback / Mermaid Export

**Document class:** Work Package Execution Contract  
**Status:** `FROZEN`  
**Gate:** G02  
**Package:** P03  
**Depends on:** G02 P02 canonical package report `State: PACKAGE_COMPLETE`

## Scope

- Algorithm Output採用結果を、操作したmodal内で確認できるようにする。
- current authoritative GraphからMermaid markdown source exportを提供する。
- export操作はGraphをmutationしない。

## Protected invariants

- adoption/fix semanticsを変更しない。
- GraphVersion lineage、DRAFT/FIXED semantics、FIXED immutabilityを維持する。
- designated Outcome lineageを維持する。
- exportはauthoritative Graphのdeterministic projectionとし、frontend独自scientific semanticsを導入しない。

## Forbidden

- export時のGraph mutation
- new Graph lifecycle/API/schema/persistence
- adoption成功表示だけを根拠に別candidateをselected/fixed扱いすること
- Graph lineageと無関係なOutcome override
- unrelated refactor

## Focused verification

- modal-local adoption feedbackをinteraction/unit testで確認する。
- Mermaid sourceがauthoritative Graphからdeterministically生成されることをunit/contract testで確認する。
- exportがGraphをmutationしないことを確認する。
- adoption/fix/lineage regressionを必要範囲で実行する。
- **Browser E2Eは本Packageでは実行しない。** Browser E2EはGate 07 Independent Verificationの最終verification itemとしてのみ実行する。

## Completion criteria

- Scope内required behaviorが満たされる。
- focused verificationがPASSする。
- P02 completion evidenceが存在する。
- protected invariant regressionがない。
- scope外変更・unresolved blockerがない。
- Package checkpointを作成しcanonical package reportで `State: PACKAGE_COMPLETE` を記録できる。
- 完了後はCandidate Assemblyへ進む。P03完了をGate PASSと表現しない。
