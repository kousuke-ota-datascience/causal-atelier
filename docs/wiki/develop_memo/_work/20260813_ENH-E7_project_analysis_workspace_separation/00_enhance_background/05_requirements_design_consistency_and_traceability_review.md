# ENH-E7 Requirement / Design整合性・Traceability Review

**文書種別:** Planning / Audit Artifact  
**Status:** REVIEWED_FOR_G02_FREEZE

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

## 4. G02 freeze traceability result

| Requirement | Design / Pxx | AC | Test Item |
| --- | --- | --- | --- |
| E7-REQ-008,009,010,011 | Analysis Workspace shell / P01 | AC-G02-01–07 | 002, 008 |
| E7-REQ-012,013,018,019 | canonical routing / P02, P06 | AC-G02-12–18 | 003, 007, 009 |
| E7-REQ-014 | Causal stage migration / P03 | AC-G02-08 | 004, 008 |
| E7-REQ-015 | Exploratory final mapping / P04 | AC-G02-09 | 005, 008 |
| E7-REQ-016,017 | Predictive stage migration / P05 | AC-G02-10,11 | 006, 008 |
| E7-REQ-021 | API/persistence non-change / P01–P06 | AC-G02-08–11,19 | 003–009 |

### AR-E7-09 closure

- Data Qualityはoperationではなくread-only availability stageである。
- TIME_TRENDは既存aggregation operationとしてComparisonへ配置する。
- CHARTは既存の永続operationとしてFindingsへ配置する。
- この決定はRequirement変更を要しない。E7-REQ-015およびE7-REQ-021の範囲であり、`03_requirements_revision.md`は変更しない。

### Consistency conclusion

- 全G02 requirementは少なくとも1つのACに対応し、全ACは少なくとも1つのblocking Test Itemに対応する。
- P04はAR-E7-09のfinal mappingを自己完結に含むため、Coding AgentがArchitecture Review / 00-layerを参照せず実装できる。
- source confirmationで未解決semantic blockerは検出されなかった。
