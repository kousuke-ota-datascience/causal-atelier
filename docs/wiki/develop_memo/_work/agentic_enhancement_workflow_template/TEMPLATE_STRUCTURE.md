# Template Structure — v2

```text
agentic_enhancement_workflow_template_v2/
├── README.md
├── TEMPLATE_STRUCTURE.md
├── CHANGELOG_v2.md
├── TEMPLATE_Current_State_Control_Sheet.md
│
├── 00_enhance_background/
│   ├── README.md
│   ├── 01_Enhance構想・要件改定計画.md
│   ├── 02_Enhance構想承認記録.md
│   ├── 03_要件定義書改定.md
│   ├── 04_設計書改定.md
│   ├── 05_要件・設計整合性およびトレーサビリティ確認.md
│   └── Revised_requirements_definition_documents/
│       ├── README.md
│       ├── 00_プロダクトコンセプトメモ.md
│       ├── 10_要件定義.md
│       ├── 21_論理データ設計.md
│       ├── 22_プロダクト基本設計.md
│       ├── 23_API・インターフェース設計.md
│       └── 30_詳細設計.md
│
├── 10_enhance_instruction/
│   ├── README.md
│   └── {{GATE_ID}}/
│       ├── 06_{{PROJECT_NAME}}_{{ENHANCE_ID}}_{{GATE_ID}}_実装指示書.md
│       ├── 07_{{PROJECT_NAME}}_{{ENHANCE_ID}}_{{GATE_ID}}_テスト指示書.md
│       ├── 08_{{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_ID}}_Remediation_Instruction.md
│       └── 09_{{ENHANCE_ID}}_{{GATE_ID}}_Gate_Contract_Amendment.md
│
├── 20_implementation_reports/
│   ├── README.md
│   ├── TEMPLATE_implementation_completion_report.md
│   ├── TEMPLATE_implementation_report_detail.md
│   └── {{GATE_ID}}/
│       ├── {{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_ID}}_implementation_completion_report.md
│       └── {{ENHANCE_ID}}_{{GATE_ID}}_implementation_report_detail.md
│
├── 30_test_report/
│   ├── README.md
│   ├── TEMPLATE_test_item_report.md
│   ├── TEMPLATE_gate_decision_report.md
│   └── {{GATE_ID}}/
│       ├── {{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_ID}}_{{TEST_ITEM_ID}}_*.md
│       └── {{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_ID}}_999_gate_decision.md
│
└── 40_operator_workflows/
    ├── README.md
    ├── agent_entry_prompts/
    │   ├── coding_agent_prompt.md
    │   ├── fail_rework_coding_agent_prompt.md
    │   └── test_agent_prompt.md
    ├── architecture_review/
    │   ├── README.md
    │   ├── 01_architecture_discovery_prompt.md
    │   ├── 02_target_architecture_decision_record_template.md
    │   └── 03_gate_decomposition_template.md
    ├── preflight/
    │   ├── README.md
    │   ├── TEMPLATE_preflight_instruction.md
    │   └── TEMPLATE_preflight_result.md
    └── controlled_runbook/
        ├── README.md
        ├── TEMPLATE_step_prompt.md
        ├── TEMPLATE_step_result.md
        └── TEMPLATE_completion_summary_decision_record.md
```

## Notes

- `{{GATE_ID}}` directories are instantiated per actual Gate (`G00`, `G01`, ...).
- 06 / 07 are Gate-local immutable contracts.
- 08 is created only for a retry Trial after FAIL unless a project explicitly defines Trial 01 remediation.
- 09 is exceptional: use only when the Gate contract itself is defective and a Human/architecture owner explicitly approves an amendment.
- `20` and `30` use the same Gate namespace as `10`.
- `40_operator_workflows` is not evidence of product acceptance by itself; authoritative acceptance evidence lives in `30_test_report`.
