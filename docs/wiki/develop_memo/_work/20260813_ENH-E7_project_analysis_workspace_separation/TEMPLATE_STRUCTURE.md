# ENH-E7 Workflow Instance Structure

This instance follows the repository `agentic_enhancement_workflow_template` document layers and expands the single template Gate directory into concrete G01 and G02 directories.

```text
20260813_ENH-E7_project_analysis_workspace_separation/
├─ README.md
├─ Current_State_Control_Sheet.md
├─ MANIFEST.json
├─ INSTANCE_VALIDATION_REPORT.md
├─ 00_enhance_background/
│  ├─ 01_enhancement_concept_and_requirement_revision_plan.md
│  ├─ 02_enhancement_concept_approval_record.md
│  ├─ 03_requirements_revision.md
│  ├─ 04_design_revision.md
│  ├─ 05_requirements_design_consistency_and_traceability_review.md
│  ├─ 80_contract_amendment_log.md
│  ├─ Revised_requirements_definition_documents/
│  └─ provenance/
├─ 10_enhance_instruction/
│  ├─ G01/
│  └─ G02/
├─ 20_implementation_reports/
│  ├─ G01/Trial01/packages/
│  └─ G02/Trial01/packages/
├─ 30_test_report/
│  ├─ G01/Trial01/
│  └─ G02/Trial01/
├─ 40_operator_workflows/
│  ├─ agent_entry_prompts/
│  ├─ architecture_review/
│  ├─ controlled_runbook/
│  └─ preflight/
└─ 90_change_history/
```

## Conditional artifacts

08 remediation and 09 Gate Contract Amendment files are supplied as `TEMPLATE_ONLY` skeletons. They do not become active contracts until their workflow trigger occurs.

## Execution control state

G01はArchitecture Review承認済み、Gate 06/07確認済みのpre-P01 execution baselineである。

Pxx execution eligibilityはdeclared status literalではなく、preflightが実際のdependency evidence等から導出する。
package文書をP01→P02→...のworkflow cursorとして手動更新しない。

G02はGate 06/07に明示的draft stateが残るため、freeze前は実行対象外である。
