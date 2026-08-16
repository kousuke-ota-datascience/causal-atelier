## 1. README > HowToUse の記載強化

agentic_enhancement_workflow_templateの
README.md
について、howtouseの記載内容が甘い。
エージェントに指示するプロンプトをそのまま使える形で記載せよ
必要に応じて、セクションに格上げしても可

例）

`````
## X. Operator Quick HowToUse （←今回はこちらを採用）
or 
### X.1. Operator Quick HowToUse


## X.1. コーディングエージェントへの指示

### X.1.1. SINGLE EXECUTION

```text
下記文書に記載の指示を実行すること。

- {{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/
    - 10_normal_execution_01_single_execution_coding_agent_prompt.md

今回の指示は
- GATE_ID=<GATE_ID>
- TRIAL_NO=<TRIAL_NO>
である。
```

### X.1.2. WORK PACKAGE EXECUTION

### X.1.2.1. STEP by STEP EXECUTION

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

### X.1.2.2. GATE WIDE AUTONOMOUS EXECUTION

```text
下記文書に記載の指示を実行すること。

- {{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/
    - 50_orchestration_01_gate_orchestrator_prompt.md

今回の指示は
- GATE_ID=<GATE_ID>
- TRIAL_NO=<TRIAL_NO>
である。
```

### X.1.2.3. CANDIDATE ASSEMBLY

```text
下記文書に記載の指示を実行すること。

- {{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/
    - 20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md

今回の指示は
- GATE_ID=<GATE_ID>
- TRIAL_NO=<TRIAL_NO>
である。
```

（以下、`agentic_enhancement_workflow_template/40_operator_workflows/agent_entry_prompts` に格納されているファイル分記載）
`````

## 2. markdownファイル作成時の見出しへの接頭辞の付与

### 2.1. 修正指示

markdown ファイルを作成する際、見出しの階層レベルに応じて接頭辞を付与せよ

### 2.2. 例）

現状
```
## 3. エンハンス文書を作成する順序

### Step 1 — Background / requirements / designを作成する

```

修正後
```
## 3. エンハンス文書を作成する順序

### 3.1. Step 1 — Background / requirements / designを作成する

```