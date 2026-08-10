# 40_operator_workflows — Human-controlled Orchestration v3

## 0. Purpose

Agent起動、architecture discovery、preflight、destructive/controlled operation等の**orchestration**を保存する。

ここにあるartifact自体はproduct acceptance evidenceではない。

## 1. Agent entry prompt policy

v3ではparameterized operator promptを標準とする。

```text
Human-supplied identity variables
  ↓
Derived naming/path variables
  ↓
Expansion validation
  ↓
Agent execution
```

### MUST

- HumanはGate / Trial / Package等のidentityを明示する。
- path / filenameは可能な限りderived variableから生成する。
- variableはUPPER_SNAKE_CASE。
- unresolved `{{...}}`が残った状態で実行しない。
- instruction globが複数一致したら任意選択しない。
- Work Package Agentはassigned packageだけを実行する。
- Audit AgentはFixed Trial Candidateを対象とする。

## 2. Agent prompts

- `coding_agent_prompt.md`: SINGLE_EXECUTION Gate
- `work_package_coding_agent_prompt.md`: Pxx/Rxx execution
- `fail_rework_coding_agent_prompt.md`: formal FAIL後のretry Trial
- `test_agent_prompt.md`: Independent Test / Audit

## 3. Other workflows

- `architecture_review/`
- `preflight/`
- `controlled_runbook/`

Gate decompositionとWork Package decompositionは別責務である。
