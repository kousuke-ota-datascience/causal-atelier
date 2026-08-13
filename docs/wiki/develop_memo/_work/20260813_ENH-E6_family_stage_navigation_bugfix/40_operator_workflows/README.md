# 40_operator_workflows — ENH-E6 Human-controlled orchestration

**Document class:** Authoring Guide / ENH instance operator index  
**Self-containment:** MUST.

## 1. Purpose

ENH-E6でHuman/operatorが制御するarchitecture review、preflight、Agent entry route、Browser E2E運用境界を追跡する。Generic Agent entry prompt自体はworkflow template側をcanonical sourceとして使用し、ENH-E6 directoryへ複製しない。

## 2. Sub-workflows

### `agent_entry_prompts/`

ENH-E6 directoryには複製しない。canonical promptは`docs/wiki/develop_memo/_work/agentic_enhancement_workflow_template/40_operator_workflows/agent_entry_prompts/`を直接使用する。

P01 Coding Agent entryは`10_normal_execution_02_work_package_coding_agent_prompt.md`に`GATE_ID=G01`, `PACKAGE_ID=P01`, `TRIAL_NO=01`を与えるだけとする。Coding AgentへGate07/06/P00/他Pxx/planning docsを直接渡さない。

### `architecture_review/`

ENH-E6はnavigation lifecycle/authority/legacy consolidationに該当するため適用済み。Discovery facts、Target ADR、Gate decompositionを保存する。

### `preflight/`

API READY/current-source browser harness、Project context、canonical Analysis route、pre-fix Family/Stage observable negative controlを保存する。

### `BROWSER_E2E_GATE_POLICY.md`

ENH instanceへ複製しない。Generic policyはtemplate側をoperator/authoring guidanceとして参照し、G01固有blocking journey/command/environment/evidence/decision semanticsはfrozen 07本文へ具体化済み。

### `controlled_runbook/`

現時点N/A。ENH-E6はstandard Work Package operator prompt + package checkpoints + Candidate Assembly + Independent Verification routeで運用する。Humanが追加のcontrolled runbookを必要と判断した場合のみtemplateからinstance化する。

## 3. Operator Artifact self-containment

ENH-E6固有のarchitecture/preflight resultは自身のfact/decision/eligibilityを本文内に持つ。Generic operator promptへENH-specific acceptance semanticsを埋め込まず、assigned Pxx/07それぞれの情報隔離を維持する。
