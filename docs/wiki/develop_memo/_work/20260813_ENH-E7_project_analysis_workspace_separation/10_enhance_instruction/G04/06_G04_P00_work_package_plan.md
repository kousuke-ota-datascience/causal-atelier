# ENH-E7 G04 P00 Work Package Plan

**文書種別:** Planning / Operator Artifact  
Status: DRAFT_NOT_FROZEN  
P00はimplementation Work Packageではない。

## 1. Work Package Modeが必要な理由

G03後の新surface architectureへ既存route/state/history/operation behaviorを再結合するため、
routing、Project state、Analysis state、cross-surface、legacy/resourceをbounded packageへ分割する。

## 2. Effective Gate semantic boundary

G04は「新shellがある」だけではPASSしない。
root/deep/legacy entry、Project Management、Analysis、browser history、existing operationが
一体として正しく動作した時点をsemantic acceptance boundaryとする。

## 3. Package map

| Package | Purpose | Depends on | Exit criterion |
|---|---|---|---|
| P01 | `/`とcanonical Project routeをG03 surfacesへ再結合 | G03 PASS | root/project route contract PASS |
| P02 | Project Management local nav / selected state / section behaviorを再結合 | P01 | PM route/state PASS |
| P03 | Analysis Context / Family / Stage stateを再結合 | P02 | analysis state contract PASS |
| P04 | Project↔Analysis↔ResultsとBack/Forward/reloadを統合 | P02,P03 | cross-surface history PASS |
| P05 | legacy/resource/operation compatibilityを回帰確認・必要最小限修復 | P04 | operation/resource regression PASS |
| P06 | full journey / stale binding cleanup / candidate integration | P05 | G04 Candidate Assembly可能 |

## 4. Dependency policy

P04はP02/P03双方のcompletionを必要とする。
G03 topologyを壊す修復は認めない。
