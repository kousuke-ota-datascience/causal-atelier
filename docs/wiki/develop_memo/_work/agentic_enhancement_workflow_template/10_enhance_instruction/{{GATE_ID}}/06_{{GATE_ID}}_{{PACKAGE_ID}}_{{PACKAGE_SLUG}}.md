# {{ENHANCE_ID}} {{GATE_ID}} {{PACKAGE_ID}} — {{PACKAGE_TITLE}}

- Gate: {{GATE_ID}}
- Trial: {{TRIAL_NO}}
- Package: {{PACKAGE_ID}}
- Parent 06: {{PATH_06}}
- P00 Plan: {{PATH_P00}}
- Depends on: {{DEPENDENCIES_OR_NONE}}
- Status at issuance: READY_TO_EXECUTE / BLOCKED_BY_DEPENDENCY

## 1. Purpose

{{PURPOSE}}

## 2. In scope

{{IN_SCOPE}}

## 3. Explicitly out of scope

{{OUT_OF_SCOPE}}

## 4. Entry criteria

{{ENTRY_CRITERIA}}

## 5. Required implementation

{{IMPLEMENTATION_INSTRUCTIONS}}

## 6. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| {{CHECK}} | `{{COMMAND}}` | {{RESULT}} |

## 7. Protected contract / TD considerations

{{PROTECTED_AND_TD}}

## 8. Checkpoint rule

Package completion時:

1. implementation-affecting changeをcommitする。
2. implementation checkpoint full SHAを固定する。
3. `implementation_checkpoint_report`を作成する。
4. `*_in_progress.md`へexecution statusを記録する。
5. report-only commitが別ならcheckpoint SHAと区別する。

## 9. Package completion criteria

{{EXIT_CRITERIA}}

## 10. Stop rule

- package scope完了 -> `PACKAGE_COMPLETE`
- continuation不能 -> `PACKAGE_BLOCKED`
- Gate PASS / FAILは判定しない。
- next packageへ勝手に先行しない。
