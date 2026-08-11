# Template Structure — 構造・配置ガイド

**Document class:** Authoring Guide  
**Self-containment:** MUST — この文書だけでcanonical directory / template placement / generated artifact patternを理解できること。

```text
agentic_enhancement_workflow_template/
├── README.md
├── TEMPLATE_STRUCTURE.md
├── MANIFEST.json
├── TEMPLATE_Current_State_Control_Sheet.md
│
├── 00_enhance_background/
│   ├── README.md
│   ├── 01_enhancement_concept_and_requirement_revision_plan.md
│   ├── 02_enhancement_concept_approval_record.md
│   ├── 03_requirements_revision.md
│   ├── 04_design_revision.md
│   ├── 05_requirements_design_consistency_and_traceability_review.md
│   └── Revised_requirements_definition_documents/
│       └── ...
│
├── 10_enhance_instruction/
│   ├── README.md
│   └── {{GATE_ID}}/
│       ├── README.md
│       ├── 06_{{PROJECT_NAME}}_{{ENHANCE_ID}}_{{GATE_ID}}_implementation_instruction.md
│       ├── 06_{{GATE_ID}}_P00_work_package_plan.md                       # conditional
│       ├── 06_{{GATE_ID}}_{{PACKAGE_ID}}_{{PACKAGE_SLUG}}.md             # P01-P99 conditional
│       ├── 07_{{PROJECT_NAME}}_{{ENHANCE_ID}}_{{GATE_ID}}_test_instruction.md
│       ├── 08_{{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_Remediation_Instruction.md
│       ├── 08_{{GATE_ID}}_{{REMEDIATION_PACKAGE_ID}}_{{PACKAGE_SLUG}}.md  # R01-R99 conditional
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
│       └── Trial{{TRIAL_NO}}/
│           ├── README.md
│           └── packages/
│               └── README.md
│
├── 30_test_report/
│   ├── README.md
│   ├── TEMPLATE_test_item_report.md
│   ├── TEMPLATE_gate_decision_report.md
│   └── {{GATE_ID}}/
│       ├── README.md
│       └── Trial{{TRIAL_NO}}/
│           └── README.md
│
├── 40_operator_workflows/
│   ├── README.md
│   ├── agent_entry_prompts/
│   ├── architecture_review/
│   ├── preflight/
│   └── controlled_runbook/
│
└── 90_change_history/
    ├── README.md
    ├── schema_v2.md
    └── schema_v3.md
```

## Generated artifact patterns

Template instantiation時に、以下を必要に応じて生成する。canonical template treeに1行stubは置かない。

```text
20_implementation_reports/{{GATE_ID}}/
  {{ENHANCE_ID}}_{{GATE_ID}}_implementation_report_detail.md
  Trial{{TRIAL_NO}}/
    {{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_implementation_completion_report.md
    packages/
      {{ENHANCE_SHORT_ID}}-{{GATE_ID}}_{{TRIAL_NO}}_{{PACKAGE_ID}}_in_progress.md
      {{ENHANCE_SHORT_ID}}-{{GATE_ID}}_{{TRIAL_NO}}_{{PACKAGE_ID}}_implementation_checkpoint_report.md

30_test_report/{{GATE_ID}}/Trial{{TRIAL_NO}}/
  {{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_{{TEST_ITEM_ID}}_*.md
  {{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_999_gate_decision.md
```

## Structural invariants

- `10 / 20 / 30`は同一Gate namespaceを使う。
- `20 / 30`はTrial directoryを物理階層として持つ。
- `P00`はWork Package Plan reserved IDでありimplementation packageではない。
- `P01-P99`はplanned Work Package、`R01-R99`はformal FAIL後のremediation Work Package。
- 06 / 07 / Pxx / RxxはPrimary Execution Contractとしてnormative self-containmentを満たす。
- 08はDELTA / CONSOLIDATED modeを持つDerived Contract。
- 09はcontract defectを記録し、承認後にprimary contractsをre-baselineするDerived Contract。
- Package checkpoint != Fixed Trial Candidate != Gate PASS。
- `999_gate_decision`だけがfinal Gate decision authorityを持つ。
- `40_operator_workflows`はorchestrationでありproduct acceptance evidenceではない。
