# ENH-E5 Gate Decomposition（Gate分解） Record

文書区分: Architecture / Planning Artifact（アーキテクチャ・計画資料）
状態: `DRAFT_FOR_REVIEW`（レビュー前ドラフト）

## Decomposition principle

Gateは、後続が利用できるsemantic resultを持つ独立acceptance boundaryである。Coding量はWork Packageで分割する。

## Gates

| Gate | PASS時に成立すること | 後続が依存できる理由 |
|---|---|---|
| G00 | FamilyとNavigation Stageのapplication contractをExecution Stageから独立して成立させ、capability-owned canonical stage catalogとread APIを提供する。 | G01以降が、stable Family ID / stage ID / order / default Stage / catalog APIへ依存できる。 |
| G01 | canonical catalogを利用してtop Family tabs + Family-local Stage sidebarを成立させ、URL/deep link/history/legacy route compatibilityを確立する。 | Family-specific G02-G04が同一navigation shell上へStage contentを安全に配置できる。 |
| G02 | current Predictive workspaceをSetup/Train/Predict/Metrics/Explainability/Model Managementへ再配置し、既存設定項目とgenerated spec/execution semanticsの完全互換を成立させる。 | ユーザーとG05が、新navigation下でもcurrent Predictive capabilityがsemantically unchangedで利用できることへ依存できる。 |
| G03 | current Causal Discovery/Inference surfacesをSetup/Discovery/Identification/Estimation/Effects/Diagnostics/Sensitivityへ再配置し、IdentificationとEstimationの責務分離を明示する。 | ユーザーとG05が、causal design/execution/resultsをdistinct Stage contextで利用しつつ既存causal semanticsへ依存できる。 |
| G04 | current Explore & Visualize capabilityをProfile/Data Quality/Distribution/Relationships/Comparison/Findingsへ再配置し、visualizationをanalytical Stageではなく各Stageの表現手段として位置づける。 | ユーザーとG05が、EDAを探索観点別にnavigationしつつ既存exploratory resultsを失わず利用できる。 |
| G05 | 3 Familyのnavigation/Stage recomposition後に、project context・Results/Lineage・routing・existing analytical execution/persistenceがcross-familyで一貫することを確立する。 | ENH-E5全体をproduct-level verified contractとして利用・release判断できる。 |

## Dependency DAG

```text
G00 -> G01 -> G02 ----\
             G03 -----+-> G05
             G04 ----/
```

G02/G03/G04はすべてG01に依存する。G01 PASS後はFamily再構成contractとしてsemantically独立する。運用上の単純さから実行順をG02 -> G03 -> G04としてよい。G05は3つすべてに依存する。

## Work Package rationale

- G00: bounded domain/API contract。`SINGLE_EXECUTION`。
- G01: route/state/UI/historyが分離可能なcoding unitに跨るため`WORK_PACKAGE`。
- G02: compatibility inventory、UI再構成、regressionを1つのsemantic claim下のexecution unitとして扱うため`WORK_PACKAGE`。
- G03: mapping、Identification/Estimation分離、regressionを分割実行するため`WORK_PACKAGE`。
- G04: mapping、visualization/findings composition、regressionを分割実行するため`WORK_PACKAGE`。
- G05: 実装済みcontract全体のconvergence/regression acceptanceを行うため`SINGLE_EXECUTION`。

## Non-gates

- 「backend work」「frontend work」は単独でproduct semanticsを成立させないためGateにはしない。
- 個別Stage実装だけではFamily contract全体がcoherentにならず後続利用可能にならないため、個別StageをGateにはしない。

## Execution contract isolation

Gate decomposition後、Planning情報をExecution Agentへそのまま渡さない。

- SINGLE_EXECUTION: 06へ必要十分なimplementation semanticsを収束する。
- WORK_PACKAGE: 06をGate semantic authorityとして作成した後、各Pxxへ担当範囲のeffective semanticsを自己完結的に収束する。Package Coding AgentはPxxのみをnormative sourceとして実行する。
- Test: 07へAcceptance semanticsを収束し、Test Agentは07のみをnormative sourceとして実行する。

この収束に失敗し、Agentが00〜30/ADR/他contractを読まないと判断できない場合はfreezeしない。
