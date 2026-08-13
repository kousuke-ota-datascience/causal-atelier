# ENH-E7 Requirement / Design整合性・Traceability Review

**文書種別:** Planning / Audit Artifact  
**Status:** PROPOSED; 06/07 FREEZE前に再実施必須

## 1. Planning levelの整合性

- Project resource managementとAnalysis executionのownershipを分離している。
- Analysis Contextをnavigation hierarchyとして扱っていない。
- canonical Analysis routeを保護している。
- existing analysis functionを置換せずStage Contentsへ移設する。
- Agent execution controlとProduct acceptanceを分離している。

## 2. Traceability rule

最終的に以下を一意に追跡可能にする。

```text
Requirement
  -> Design
  -> Gate
  -> Work Package
  -> Acceptance Criterion
  -> Test Item
  -> Evidence
  -> 999 Gate Decision
```

## 3. Freeze rule

各Gate 06/07のfreeze前に以下を確認する。

1. 全MUST Requirementが1つ以上のACへ対応する。
2. 全ACが1つ以上のTest Itemへ対応する。
3. Browser E2Eはcritical journeyに限定する。
4. Pxxが06/07/P00/other Pxxを読まずself-containedに実行可能である。
5. Gateに影響するArchitecture unresolved itemが0件である。
