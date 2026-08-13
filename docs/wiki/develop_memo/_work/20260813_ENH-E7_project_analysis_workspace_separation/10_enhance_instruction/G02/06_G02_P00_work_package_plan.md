# ENH-E7 G02 P00 Work Package Plan

**文書種別:** Planning / Operator Artifact  
**Status:** DRAFT_NOT_FROZEN  
**P00はimplementation Work Packageではない。**

## 1. Work Package Modeが必要な理由

G02はAnalysis Context、routing、3 Familyのsurface migration、legacy cutoverを含むため、
bounded executionとfailure localizationが必要である。
一方、Product claimはAnalysis Workspace全体が操作可能になった時点でのみ成立するためGateは分割しない。

## 2. Effective Gate semantic boundary

- Gate claim: Analysis WorkspaceがProject Managementとは別analysis surfaceとして成立し、Analysis Context、Family/Stage navigation、既存Causal/Exploratory/Predictive surfaceのStage Contents配置、cross-surface navigation、legacy compatibility、browser history semanticsを一体として利用できる。
- Downstream result: ENH-E7をProduct-completeと判定可能になり、後続EnhancementはProject/Analysis surface分離とStage-local presentation ownershipへ依存できる。
- G01 final PASSがmandatory entry。
- Pxxはself-contained。
- Coding AgentはP00 / 06 / 07 / other Pxxを仕様補完目的で読まない。

## 3. Package map

| Package | Purpose | Depends on | Entry criterion | Exit criterion | Focused verification |
|---|---|---|---|---|---|
| P01 | Analysis Workspace shellと明示的current analysis-input contextを作成する。 | G01 PASS | G01 PASS + Gate entry criteria + preflight PASS | Analysis Context / shell contract testがPASSする。 | assigned Pxxのfocused test |
| P02 | Project Management / Analysis Workspace / Results-Lineageをcanonical routeで接続する。 | P01 | G01 PASS + Gate entry criteria + preflight PASS + dependency complete: P01 | Cross-surface routing contract testがPASSする。 | assigned Pxxのfocused test |
| P03 | existing Causal surfaceをSetup / Discovery / Identification / Estimation / Effects / Diagnostics / Sensitivityへ移設する。 | P01,P02 | G01 PASS + Gate entry criteria + preflight PASS + dependency complete: P01,P02 | existing Causal operationをmapped Stage Contentsから操作できる。 | assigned Pxxのfocused test |
| P04 | existing Exploratory operation/resultをStage hierarchyへ移設する。 | P01,P02 | G01 PASS + Gate entry criteria + preflight PASS + dependency complete: P01,P02 | existing Exploratory operationをmapped Stage Contentsから操作できる。 | assigned Pxxのfocused test |
| P05 | existing Predictive presentationをSetup / Train / Predict / Metrics / Explainability / Model Managementへ移設し、新execution modelを作らない。 | P01,P02 | G01 PASS + Gate entry criteria + preflight PASS + dependency complete: P01,P02 | existing Predictive execution regressionとmapped presentation operabilityがPASSする。 | assigned Pxxのfocused test |
| P06 | 重複legacy analytical UI navigationを削除し、legacy URL compatibility / browser history / resource behaviorを統合してTrial candidateを準備する。 | P03,P04,P05 | G01 PASS + Gate entry criteria + preflight PASS + dependency complete: P03,P04,P05 | G02 gate-wide self-checkとcritical browser journeyがPASSする。 | assigned Pxxのfocused test |

## 4. Candidate Assembly

Required package set: P01, P02, P03, P04, P05, P06。

すべてcompleteした後だけCandidate Assemblyを行い、Fixed Trial Candidateを`READY_FOR_TEST`へ進める。
