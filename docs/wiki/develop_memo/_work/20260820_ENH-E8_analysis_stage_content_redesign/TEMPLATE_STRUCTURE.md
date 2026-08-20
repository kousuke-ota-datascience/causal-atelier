# ENH-E8 Workflow構造

**Document class:** Authoring Guide  
**Self-containment:** MUST

```text
20260820_ENH-E8_analysis_stage_content_redesign/
├── README.md
├── README_Appendix_HowToUse.md
├── README_NAMING_CONVENTION.md
├── TEMPLATE_STRUCTURE.md
├── MANIFEST.json
├── 00_enhance_background/
│   ├── README_00.md
│   ├── 01_enhancement_concept_and_requirement_revision_plan.md
│   ├── 02_enhancement_concept_approval_record.md
│   ├── 03_requirements_revision.md
│   ├── 04_design_revision.md
│   ├── 05_requirements_design_consistency_and_traceability_review.md
│   ├── 80_contract_amendment_log.md
│   └── Revised_requirements_definition_documents/
├── 10_enhance_instruction/
│   ├── README_10.md
│   ├── G01/
│   └── G02/
├── 20_implementation_reports/
│   ├── README_20.md
│   ├── TEMPLATE_implementation_*.md
│   ├── G01/Trial01/packages/
│   └── G02/Trial01/packages/
├── 30_test_report/
│   ├── README_30.md
│   ├── TEMPLATE_test_item_report.md
│   ├── TEMPLATE_gate_decision_report.md
│   ├── G01/Trial01/
│   └── G02/Trial01/
├── 40_operator_workflows/
│   ├── BROWSER_E2E_GATE_POLICY.md
│   ├── README_40.md
│   ├── agent_entry_prompts/
│   ├── architecture_review/
│   ├── controlled_runbook/
│   ├── preflight/
│   └── tools/
└── 90_change_history/
```

実装・テストevidenceは架空の `PASS` / `READY_FOR_TEST` を事前投入しない。Trial directoryには、Agentが実evidenceを生成するまではREADME guidanceのみを置く。
