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
