# Variable規約

実行ごとにHumanが与える値:
- `GATE_ID` = ENH-E11正式Gate ID（`G01`〜`G10`のいずれか）。Gate別06/07/08/Pxxが存在・Freeze済みかは実行時に検証し、未作成GateへG01の契約を流用しない。
- `TRIAL_NO` = 2桁 Trial number（例: `01`）
- `PACKAGE_ID` = Package ID（例: `P01`。Work Package coding時のみ）

ENH-E11 Enhancement固定値:
- `PROJECT_NAME=Ariadne`
- `ENHANCE_ID=ENH-E11`
- `ENHANCE_SHORT_ID=E11`
- `BRANCH_NAME=prototype/ariadne_mvp`
- `REMOTE_NAME=causal-atelier`
- `WORK_ROOT=docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion`

Runtime-derived values:
- `START_SHA`
- `PACKAGE_CHECKPOINT_SHA`
- `FIXED_TRIAL_CANDIDATE_SHA`
- `EVIDENCE_COMMIT_SHA`
- `TEST_START_SHA`
- `TEST_EVIDENCE_COMMIT_SHA`
- `PREVIOUS_FAILED_CANDIDATE_SHA`（formal FAIL remediation時）

導出path:
- `docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/10_enhance_instruction/$GATE_ID/06_Ariadne_ENH-E11_$GATE_ID...` — directory listingから正確なfilenameを導出する。semantic matchが0件または複数ならSTOPする。

SHA は実行時の repository state からのみ取得する。架空 SHA を事前生成してはならない。
`PACKAGE_CHECKPOINT_SHA`、`FIXED_TRIAL_CANDIDATE_SHA`、`EVIDENCE_COMMIT_SHA` は意味が異なるため混同しない。

Enhancement-fixed identityは展開済み。Agent実行時にRuntime variableだけを確定する。任意のglob matchを選んではならない。

<!-- BEGIN MANAGED: AGENT_ENTRY_PROMPT_CONTROL -->
## 2. Agent Entry Prompt Variable Conventions

### 2.1. Purpose

`agent_entry_prompts/` はENH-E11用に実体化済みの実行Prompt正本であり、Enhancement-fixed変数は具体値へ展開済みである。実行時に未解決のRuntime変数だけHuman/Orchestratorが指定する。

template directory上のpromptをAgent executionへ直接指定してはならない。

### 2.2. Enhancement-fixed variables

以下はEnhancement-specific prompt instance生成時に必ず具体値へ展開する。

```text
PROJECT_NAME
ENHANCE_ID
ENHANCE_SHORT_ID
BRANCH_NAME
REMOTE_NAME
WORK_ROOT
WORK_DIR_NAME
```

Enhancement-side `agent_entry_prompts/` に上記の未解決placeholderが1件でも残る場合、Agent execution readinessは `BLOCKED_ENHANCEMENT_IDENTITY_UNRESOLVED` とする。

**ENH-E11 Gate scope:** GateはG01〜G10の10件。40 Promptは全Gate共通で、対象Gateの実行mode/Required PackageをGate06から解決する。G01だけに現在具体的な06/07/Pxxが存在し、G02〜G10の実装内容・Gate readinessを推定しない。

### 2.3. Runtime variables

以下はexecution単位でHuman operatorまたはOrchestratorが指定する。

```text
GATE_ID
PACKAGE_ID
TRIAL_NO
REMEDIATION_PACKAGE_ID
AMENDMENT_ID
```

各promptは必要なRuntime variableだけを要求する。不要なRuntime variableを推測で補完してはならない。

### 2.4. Resolution rule

Enhancement identityはEnhancement-fixed variablesから、execution identityはRuntime variablesから解決する。

```text
Execution identity = Enhancement identity + Runtime identity
```

Human entryだけで対象を一意に解決できない場合は実行を開始せず `BLOCKED_EXECUTION_UNRESOLVABLE` とする。

### 2.5. Template and instance distinction

- template側: `agentic_enhancement_workflow_template/40_operator_workflows/agent_entry_prompts/`
  - authoring source
  - Enhancement-fixed placeholdersを保持してよい
  - Agent executionへ直接使用しない
- Enhancement側: `docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/40_operator_workflows/agent_entry_prompts/`
  - execution source
  - Enhancement-fixed placeholdersは0件でなければならない
  - Human Quick HowToUseが参照するcanonical path

### 2.6. Markdown heading numbering

Markdown artifactの見出しは原則として以下に従う。

```text
#       document title: no numeric prefix
##      1. / 2. / 3.
###     1.1. / 1.2.
####    1.1.1.
#####   1.1.1.1.
######  1.1.1.1.1.
```

コードフェンス内の `#` は対象外とする。
<!-- END MANAGED: AGENT_ENTRY_PROMPT_CONTROL -->
