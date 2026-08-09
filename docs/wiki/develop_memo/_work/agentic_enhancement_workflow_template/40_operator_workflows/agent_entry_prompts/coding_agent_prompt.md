# Coding Agent Entry Prompt

以下のGate Coding ContractだけをActive Gateの実装契約として使用してください。

- 06: `{{PATH_06}}`
- Current State Control Sheet: `{{CONTROL_SHEET_PATH}}`
- Applicable remediation 08: `{{PATH_08_OR_NONE}}`

06で許可された範囲とprecedenceに従ってください。
Active Gate以外へ先行着手しないでください。

実装後は、06で指定されたimplementation completion reportとGate-local implementation detailを作成・更新し、implementation commit full SHAを固定してください。

Gate判定は行わず、`READY_FOR_TEST`または明示的な`BLOCKED_*`状態で停止してください。
