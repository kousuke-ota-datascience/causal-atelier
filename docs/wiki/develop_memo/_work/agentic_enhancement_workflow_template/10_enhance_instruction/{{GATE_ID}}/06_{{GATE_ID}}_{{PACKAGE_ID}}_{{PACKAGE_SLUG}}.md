# {{ENHANCE_ID}} {{GATE_ID}} {{PACKAGE_ID}} — {{PACKAGE_TITLE}}

**Document class:** Primary Execution Contract  
**Self-containment:** MUST — Assigned Coding Agentが本書だけでpackageのnormative execution responsibilityを理解できること。

- Gate: {{GATE_ID}}
- Trial: {{TRIAL_NO}}
- Package: {{PACKAGE_ID}}
- Parent 06 (traceability): {{PATH_06}}
- P00 Plan (traceability): {{PATH_P00}}
- Depends on: {{DEPENDENCIES_OR_NONE}}
- Status at issuance: READY_TO_EXECUTE / BLOCKED_BY_DEPENDENCY

## 1. Purpose
{{PURPOSE}}

## 2. Effective Gate constraints applicable to this package

このpackageが守るべきGate-level semanticsを、Parent 06 / P00を読まなくても実行判断できる粒度で記載する。

{{EFFECTIVE_GATE_CONSTRAINTS}}

## 3. In scope
{{IN_SCOPE}}

## 4. Explicitly out of scope
{{OUT_OF_SCOPE}}

## 5. Entry criteria / required evidence
{{ENTRY_CRITERIA}}

dependency checkpoint / source state等はfactとして外部参照してよい。Entry rule自体は本書内に記載する。

## 6. Required implementation
{{IMPLEMENTATION_INSTRUCTIONS}}

## 7. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| {{CHECK}} | `{{COMMAND}}` | {{RESULT}} |

## 8. Protected contract / Transition Debt constraints
{{PROTECTED_AND_TD}}

## 9. Checkpoint / reporting rule

Package completion時:

1. implementation-affecting changeをcommitする。
2. implementation checkpoint full SHAを固定する。
3. `implementation_checkpoint_report`を作成する。
4. `*_in_progress.md`へexecution statusを記録する。
5. report-only commitが別ならcheckpoint SHAと区別する。

## 10. Package completion criteria
{{EXIT_CRITERIA}}

## 11. External reference policy

source / previous checkpoint / test output / provenanceは外部参照してよい。本書のimplementation rule、prohibited scope、completion criterionをParent 06 / P00へ委譲してはならない。

## 12. Stop rule

- package scope完了 -> `PACKAGE_COMPLETE`
- continuation不能 -> `PACKAGE_BLOCKED`
- Gate PASS / FAILは判定しない。
- next packageへ勝手に先行しない。
