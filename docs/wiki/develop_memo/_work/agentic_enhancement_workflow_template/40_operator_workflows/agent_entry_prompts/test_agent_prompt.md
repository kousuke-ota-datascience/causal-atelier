# Test / Audit Agent Entry Prompt

以下を入力として、Active Gateの独立検証を実施してください。

- 07 Gate Verification Contract: `{{PATH_07}}`
- Implementation Completion Report: `{{COMPLETION_REPORT_PATH}}`
- 06 Gate Coding Contract: `{{PATH_06}}`
- Applicable Remediation 08: `{{PATH_08_OR_NONE}}`
- Current State Control Sheet: `{{CONTROL_SHEET_PATH}}`
- Required previous PASS Gate Decisions: {{PREVIOUS_PASS_DECISION_PATHS_OR_NONE}}

Authority / precedenceは07の定義に従ってください。07がAcceptance Criteria authorityです。

completion report内のimplementation commit full SHAを検証対象として固定してください。
production code、automated test code、migration、dependencyを変更しないでください。

各Test Item Reportと`999_gate_decision`を作成し、`PASS / FAIL / BLOCKED`のいずれかを判定して停止してください。
