# Operator Workflows v2

## 0. Purpose

Human / workflow ownerがAgent executionや高リスク操作を制御するためのorchestration layer。

このdirectoryの文書はproduct acceptance evidenceそのものではない。
Acceptance evidenceは`30_test_report/`へ保存する。

## 1. Workflow classes

### 1.1. `agent_entry_prompts/`
Coding / retry Coding / Test Agentへ渡す最小入口prompt。
詳細契約を外側promptへ重複させない。

### 1.2. `architecture_review/`
Architecture / authority / persistence / runtime boundaryを変更するenhancementの事前調査・target decision・Gate decomposition。

### 1.3. `preflight/`
product Gateとは別のexecution prerequisite verification。

### 1.4. `controlled_runbook/`
DB reset、migration repair、data purge、infrastructure operation等を、Humanがstep-by-stepに制御するprompt/result pair workflow。

## 2. Principle

- execution contractは10に一本化。
- product evidenceは30に一本化。
- verified current stateはControl Sheetに一本化。
- operator workflowは「何を次に実行してよいか」を制御する。

## 3. Destructive operations

Destructive operationはAgentの広い裁量で実行させない。
step promptにexact command / precondition / abort conditionを固定し、step resultを確認してから次stepへ進む。
