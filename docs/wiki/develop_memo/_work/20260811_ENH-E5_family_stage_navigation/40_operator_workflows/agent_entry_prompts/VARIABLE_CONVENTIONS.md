# Variable規約 — ENH-E5

実行ごとにHumanが与える値:
- `GATE_ID` = G00..G05
- `TRIAL_NO` = 01..99
- `PACKAGE_ID` = P01..P99（Work Package coding時のみ）

固定値:
- `PROJECT_NAME=Ariadne`
- `ENHANCE_ID=ENH-E5`
- `BRANCH_NAME=feature/ariadne_mvp_e5`

導出path:
- `10_enhance_instruction/$GATE_ID/06_Ariadne_ENH-E5_$GATE_ID...` — directory listingから正確なfilenameを導出する。semantic matchが0件または複数ならSTOPする。

Agent実行前に全variableを明示的に置換・確定する。任意のglob matchを選んではならない。
