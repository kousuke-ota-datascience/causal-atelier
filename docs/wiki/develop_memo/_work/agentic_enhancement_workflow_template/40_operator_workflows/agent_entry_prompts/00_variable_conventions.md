# Variable規約

実行ごとにHumanが与える値:
- `GATE_ID` = Gate ID（例: `G00`）
- `TRIAL_NO` = 2桁 Trial number（例: `01`）
- `PACKAGE_ID` = Package ID（例: `P01`。Work Package coding時のみ）

Template / Enhancement 固定値:
- `PROJECT_NAME={{PROJECT_NAME}}`
- `ENHANCE_ID={{ENHANCE_ID}}`
- `ENHANCE_SHORT_ID={{ENHANCE_SHORT_ID}}`
- `BRANCH_NAME={{BRANCH_NAME}}`
- `REMOTE_NAME={{REMOTE_NAME}}`
- `WORK_ROOT={{WORK_ROOT}}`

Runtime-derived values:
- `START_SHA`
- `PACKAGE_CHECKPOINT_SHA`
- `FIXED_TRIAL_CANDIDATE_SHA`
- `EVIDENCE_COMMIT_SHA`
- `TEST_START_SHA`
- `TEST_EVIDENCE_COMMIT_SHA`
- `PREVIOUS_FAILED_CANDIDATE_SHA`（formal FAIL remediation時）

導出path:
- `{{WORK_ROOT}}/10_enhance_instruction/$GATE_ID/06_{{PROJECT_NAME}}_{{ENHANCE_ID}}_$GATE_ID...` — directory listingから正確なfilenameを導出する。semantic matchが0件または複数ならSTOPする。

SHA は実行時の repository state からのみ取得する。架空 SHA を事前生成してはならない。
`PACKAGE_CHECKPOINT_SHA`、`FIXED_TRIAL_CANDIDATE_SHA`、`EVIDENCE_COMMIT_SHA` は意味が異なるため混同しない。

Agent実行前に全variableを明示的に置換・確定する。任意のglob matchを選んではならない。
