# Template Structure

```text
agentic_enhancement_workflow_template/
├── README.md
├── TEMPLATE_STRUCTURE.md
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
│   ├── 06_{{PROJECT_NAME}}_{{ENHANCE_ID}}_実装指示書.md
│   └── 07_{{PROJECT_NAME}}_{{ENHANCE_ID}}_テスト指示書.md
│
├── 20_implementation_reports/
│   ├── README.md
│   ├── TEMPLATE_implementation_completion_report.md
│   └── TEMPLATE_implementation_report_detail.md
│
├── 30_test_report/
│   ├── README.md
│   ├── TEMPLATE_test_item_report.md
│   └── TEMPLATE_gate_decision_report.md
│
└── 40_operator_prompts/
    ├── README.md
    ├── coding_agent_prompt.md
    ├── fail_rework_coding_agent_prompt.md
    └── test_agent_prompt.md
```
