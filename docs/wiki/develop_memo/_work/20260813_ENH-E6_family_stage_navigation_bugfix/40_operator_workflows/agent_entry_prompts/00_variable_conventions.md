# Variable規約

実行ごとにHumanが与える値:
- `GATE_ID` = Gate ID（例: `G00`）
- `TRIAL_NO` = 2桁 Trial number（例: `01`）
- `PACKAGE_ID` = Package ID（例: `P01`。Work Package coding時のみ）

Template / Enhancement 固定値:
- `PROJECT_NAME=Ariadne`
- `ENHANCE_ID=ENH-E6`
- `ENHANCE_SHORT_ID=E6`
- `BRANCH_NAME=bugfix/ariadne_mvp_e6`
- `REMOTE_NAME=causal-atelier`
- `WORK_ROOT=docs/wiki/develop_memo/_work/20260813_ENH-E6_family_stage_navigation_bugfix`

Runtime-derived values:
- `START_SHA`
- `PACKAGE_CHECKPOINT_SHA`
- `FIXED_TRIAL_CANDIDATE_SHA`
- `EVIDENCE_COMMIT_SHA`
- `TEST_START_SHA`
- `TEST_EVIDENCE_COMMIT_SHA`
- `PREVIOUS_FAILED_CANDIDATE_SHA`（formal FAIL remediation時）

導出path:
- `docs/wiki/develop_memo/_work/20260813_ENH-E6_family_stage_navigation_bugfix/10_enhance_instruction/$GATE_ID/06_Ariadne_ENH-E6_$GATE_ID...` — directory listingから正確なfilenameを導出する。semantic matchが0件または複数ならSTOPする。

SHA は実行時の repository state からのみ取得する。架空 SHA を事前生成してはならない。
`PACKAGE_CHECKPOINT_SHA`、`FIXED_TRIAL_CANDIDATE_SHA`、`EVIDENCE_COMMIT_SHA` は意味が異なるため混同しない。

Agent実行前に全variableを明示的に置換・確定する。任意のglob matchを選んではならない。
