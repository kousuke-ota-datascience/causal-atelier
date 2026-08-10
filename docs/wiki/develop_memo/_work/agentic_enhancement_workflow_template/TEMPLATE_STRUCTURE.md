# Template Structure — v3

```text
agentic_enhancement_workflow_template_v3/
├── README.md
├── TEMPLATE_STRUCTURE.md
├── CHANGELOG_v2.md
├── CHANGELOG_v3.md
├── MANIFEST.json
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
│       └── ...
│
├── 10_enhance_instruction/
│   ├── README.md
│   └── {{GATE_ID}}/
│       ├── README.md
│       ├── 06_{{PROJECT_NAME}}_{{ENHANCE_ID}}_{{GATE_ID}}_実装指示書.md
│       ├── 06_{{GATE_ID}}_P00_work_package_plan.md                 # conditional
│       ├── 06_{{GATE_ID}}_{{PACKAGE_ID}}_{{PACKAGE_SLUG}}.md        # P01-P99 conditional
│       ├── 07_{{PROJECT_NAME}}_{{ENHANCE_ID}}_{{GATE_ID}}_テスト指示書.md
│       ├── 08_{{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_Remediation_Instruction.md
│       ├── 08_{{GATE_ID}}_{{REMEDIATION_PACKAGE_ID}}_{{PACKAGE_SLUG}}.md # R01-R99 conditional
│       └── 09_{{ENHANCE_ID}}_{{GATE_ID}}_{{AMENDMENT_ID}}_Gate_Contract_Amendment.md
│
├── 20_implementation_reports/
│   ├── README.md
│   ├── TEMPLATE_package_execution_status_report.md
│   ├── TEMPLATE_implementation_checkpoint_report.md
│   ├── TEMPLATE_implementation_completion_report.md
│   ├── TEMPLATE_implementation_report_detail.md
│   └── {{GATE_ID}}/
│       ├── README.md
│       ├── {{ENHANCE_ID}}_{{GATE_ID}}_implementation_report_detail.md
│       └── Trial{{TRIAL_NO}}/
│           ├── README.md
│           ├── packages/
│           │   ├── README.md
│           │   ├── {{ENHANCE_SHORT_ID}}-{{GATE_ID}}_{{TRIAL_NO}}_{{PACKAGE_ID}}_in_progress.md
│           │   └── {{ENHANCE_SHORT_ID}}-{{GATE_ID}}_{{TRIAL_NO}}_{{PACKAGE_ID}}_implementation_checkpoint_report.md
│           └── {{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_implementation_completion_report.md
│
├── 30_test_report/
│   ├── README.md
│   ├── TEMPLATE_test_item_report.md
│   ├── TEMPLATE_gate_decision_report.md
│   └── {{GATE_ID}}/
│       ├── README.md
│       └── Trial{{TRIAL_NO}}/
│           ├── README.md
│           ├── {{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_{{TEST_ITEM_ID}}_*.md
│           └── {{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_999_gate_decision.md
│
└── 40_operator_workflows/
    ├── README.md
    ├── agent_entry_prompts/
    │   ├── README.md
    │   ├── VARIABLE_CONVENTIONS.md
    │   ├── coding_agent_prompt.md
    │   ├── work_package_coding_agent_prompt.md
    │   ├── fail_rework_coding_agent_prompt.md
    │   └── test_agent_prompt.md
    ├── architecture_review/
    │   └── ...
    ├── preflight/
    │   └── ...
    └── controlled_runbook/
        └── ...
```

## Structural invariants

- `10 / 20 / 30`は同一Gate namespaceを使う。
- `20 / 30`はTrial directoryを物理階層として持つ。
- `P00`はWork Package Plan reserved IDでありimplementation packageではない。
- `P01-P99`はplanned Work Package、`R01-R99`はformal FAIL後のremediation Work Package。
- Work Package directoryは`WORK_PACKAGE` modeのときだけ必要。
- 06 / 07はGate-local immutable semantic contracts。
- P00 / Pxx / Rxxは06/07をoverrideできない。
- package checkpoint reportはGate acceptance evidenceではない。
- Trial completion reportがFixed Trial Candidateを固定する。
- `999_gate_decision`だけがGateのfinal PASS / FAIL / BLOCKED authorityを持つ。
- `40_operator_workflows`はorchestrationでありproduct acceptance evidenceではない。
