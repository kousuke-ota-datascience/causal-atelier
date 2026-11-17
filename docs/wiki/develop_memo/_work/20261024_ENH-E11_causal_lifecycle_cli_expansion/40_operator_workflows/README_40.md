# 40_operator_workflows — Human-controlled orchestrationの作成・使用ガイド

**Document class:** Authoring Guide  
**Self-containment:** MUST — このREADMEだけで40層の用途・各workflowの責務・operator artifactのself-containment ruleが分かること。

## 1. Purpose

`40_operator_workflows/`は、product acceptance contractとは別に、HumanがAgentの起動・architecture discovery・preflight・destructive operation等をbounded executionとして制御する層である。

40層のresultは、明示的に30層へ取り込まれない限りGate PASS authorityを持たない。

## 2. Sub-workflows

### `agent_entry_prompts/`
Single Execution Coding / Work Package Coding / Candidate Assembly / FAIL rework / Independent Test / Gate Orchestratorを起動するparameterized prompt。各prompt自身にhuman-supplied variables、derived-variable rule、target path、required output、stop conditionを含める。

### `architecture_review/`
current architecture discovery、target architecture decision、Gate decompositionを行う。product codeを実装するworkflowではない。

### `preflight/`
DB / migration / service / toolchain等のexecution prerequisiteを検証する。preflight FAILとproduct implementation FAILを区別する。Gate blocking Browser E2Eではstale service / image / fixtureに依存しないhermetic execution prerequisiteを確認する。

### `BROWSER_E2E_GATE_POLICY.md`
Browser E2Eを少数のcritical user journeyへ限定し、test-layer allocation、hermetic environment、semantic synchronization、observable assertion、failure evidence / classificationを定義する共通authoring / operational policy。個別GateのAcceptance authorityではなく、必要なGate固有ruleはfrozen 07へ具体化する。

### `controlled_runbook/`
破壊的・不可逆・infrastructure-sensitive operationをstep単位で実行し、各step後にHuman decision boundaryを置く。

## 3. Operator Artifact self-containment

Agentへ直接渡すprompt / instructionは、そのexecutionのために必要な以下を本文内に持つ。

- required variables / expansion rule
- exact target / allowed action
- prohibited action
- output schema / output path
- completion / abort / stop condition

共通ガイドを別ファイルに保持してよいが、**実行時に別のvariable conventionやresult templateを読まなければpromptを実行できない構造にしない。**

external source / commit / DB / previous result等はexecution target / precondition evidenceとして参照してよい。

<!-- BEGIN MANAGED: WORKFLOW_EXECUTION_CONTROL -->
## 2. Workflow Execution Control

### 2.1. Template-side prompt direct execution prohibition

`agentic_enhancement_workflow_template/40_operator_workflows/agent_entry_prompts/` はauthoring sourceであり、Agent executionへ直接指定してはならない。

Enhancement開始時にEnhancement-specific prompt instanceを以下へ生成する。

```text
{{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/
```

### 2.2. Variable lifecycle

Enhancement-fixed variablesはinstance化時に確定する。

```text
PROJECT_NAME
ENHANCE_ID
ENHANCE_SHORT_ID
BRANCH_NAME
REMOTE_NAME
WORK_ROOT
WORK_DIR_NAME
```

Runtime variablesだけをexecution時にHuman operator / Orchestratorが与える。

```text
GATE_ID
PACKAGE_ID
TRIAL_NO
REMEDIATION_PACKAGE_ID
AMENDMENT_ID
```

### 2.3. Coding Agent context isolation

Work Package Coding Agentのnormative contextはassigned Pxxだけとする。

Human/auditor traceabilityとAgent-visible normative contextを分離する。

```text
Human traceability != Agent-visible normative context
```

### 2.4. Execution readiness

Document complianceとAgent Execution Readinessを独立判定する。readinessがFAILならAgentを起動しない。

最低4軸:

1. Artifact completeness
2. Content completeness
3. Execution resolvability
4. Information isolation

Metadata parsingはMarkdown decorationに依存させない。`**Field:** value` / `Field: value` / `- Field: value` のような意味的に同一の表記差は許容し、field欠落・空値・解釈不能なdependency・evidence欠落のみをblocking対象とする。共通実装は `40_operator_workflows/tools/workflow_metadata.py` を使用する。

### 2.5. Runtime authority minimization

Normal-path preflight / orchestrationのrouting authorityはGate 06 / 07へ集約する。

- Gate dependency declaration: 06 `Depends on`
- execution mode: 06 `Execution mode`
- required package set: 06 `Required packages`
- package dependency: each Pxx `Depends on`
- Gate dependency evidence: canonical 999

Gate local README / P00 / Architecture Review artifactはnormal runtime authorityにしない。
<!-- END MANAGED: WORKFLOW_EXECUTION_CONTROL -->

<!-- BEGIN MANAGED: OPERATOR_QUICK_HOWTOUSE -->
## 3. Operator Quick HowToUse

### 3.1. Prerequisite

以下のentry instructionは、**Enhancement-specificにinstance化済みの** `{{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/` を参照する。

template directory上の `agentic_enhancement_workflow_template/40_operator_workflows/agent_entry_prompts/` をAgentへ直接指定してはならない。

### 3.2. SINGLE EXECUTION

```text
下記文書に記載の指示を実行すること。

- {{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/
    - 10_normal_execution_01_single_execution_coding_agent_prompt.md

今回の指示は
- GATE_ID=<GATE_ID>
- TRIAL_NO=<TRIAL_NO>
である。
```

### 3.3. WORK PACKAGE EXECUTION — STEP by STEP

```text
下記文書に記載の指示を実行すること。

- {{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/
    - 10_normal_execution_02_work_package_coding_agent_prompt.md

今回の指示は
- GATE_ID=<GATE_ID>
- PACKAGE_ID=<PACKAGE_ID>
- TRIAL_NO=<TRIAL_NO>
である。
```

### 3.4. CANDIDATE ASSEMBLY

```text
下記文書に記載の指示を実行すること。

- {{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/
    - 20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md

今回の指示は
- GATE_ID=<GATE_ID>
- TRIAL_NO=<TRIAL_NO>
である。
```

### 3.5. INDEPENDENT VERIFICATION

```text
下記文書に記載の指示を実行すること。

- {{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/
    - 30_independent_verification_01_test_agent_prompt.md

今回の指示は
- GATE_ID=<GATE_ID>
- TRIAL_NO=<TRIAL_NO>
である。
```

### 3.6. FORMAL FAIL REMEDIATION

```text
下記文書に記載の指示を実行すること。

- {{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/
    - 40_fail_remediation_01_fail_rework_coding_agent_prompt.md

今回の指示は
- GATE_ID=<GATE_ID>
- REMEDIATION_PACKAGE_ID=<REMEDIATION_PACKAGE_ID>
- TRIAL_NO=<TRIAL_NO>
である。
```

### 3.7. GATE WIDE AUTONOMOUS EXECUTION

```text
下記文書に記載の指示を実行すること。

- {{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/
    - 50_orchestration_01_gate_orchestrator_prompt.md

今回の指示は
- GATE_ID=<GATE_ID>
- TRIAL_NO=<TRIAL_NO>
である。
```


### 3.8. SUPPORTING DOCUMENTS — NOT DIRECT EXECUTION ENTRY POINTS

以下もEnhancement-specific `agent_entry_prompts/` instanceへ含めるが、Human operatorがAgentへ直接指定するexecution promptではない。

- `README_40_agent_entry_prompts.md`
- `00_variable_conventions.md`

Agent起動前にtemplate-side readiness validatorを実行し、`OVERALL: READY_FOR_AGENT_EXECUTION` の場合のみ上記entry instructionを使用する。
<!-- END MANAGED: OPERATOR_QUICK_HOWTOUSE -->

<!-- BEGIN MANAGED: README_NAMING_CONVENTION -->
## 4. README Naming Convention

### 4.1. Rule

Enhancement work root / workflow template rootのtop-level READMEだけを無印 `README.md` とする。

nested directoryのlocal READMEは、directory pathから機械的に導出した `PATH_ID` をpostfixとして付与する。

```text
README filename = deterministic function(directory path)
```

```text
root/
  README.md

root/00_enhance_background/
  README_00.md

root/20_implementation_reports/G01/Trial01/
  README_20_G01_Trial01.md

root/40_operator_workflows/agent_entry_prompts/
  README_40_agent_entry_prompts.md
```

### 4.2. PATH_ID generation

Enhancement/template rootからREADME配置directoryまでのrelative pathを左から処理する。

1. `NN_<semantic_name>` 形式のworkflow namespace directoryは `NN` に短縮する。
2. `G01`, `P01`, `Trial01` 等のruntime identity directoryはそのまま保持する。
3. `agent_entry_prompts`, `preflight` 等の非numbered semantic directoryは名前を保持する。
4. tokenを `_` で連結する。
5. `README_<PATH_ID>.md` とする。

例:

```text
00_enhance_background
  -> 00
  -> README_00.md

20_implementation_reports/G01/Trial01
  -> 20_G01_Trial01
  -> README_20_G01_Trial01.md

40_operator_workflows/agent_entry_prompts
  -> 40_agent_entry_prompts
  -> README_40_agent_entry_prompts.md
```

### 4.3. Invariants

- root以外に無印 `README.md` を置いてはならない。
- 同一directoryに複数のlocal READMEを置いてはならない。
- 手作業でpostfixを決めてはならない。必ずpath-derived naming functionを使用する。
- rename時はMarkdown links、plain path references、operator prompts、structure/manifest、validator/instantiation toolingを同時更新する。
- target filename collisionが発生した場合は自動上書きせず `BLOCKED_README_NAMING_COLLISION` とする。

### 4.4. Canonical implementation

canonical naming functionは以下とする。

```text
40_operator_workflows/tools/readme_naming.py
```

Template migration/apply tooling、instantiation tooling、validatorは同一規則を使用し、別々の命名ロジックを持たない。
<!-- END MANAGED: README_NAMING_CONVENTION -->
