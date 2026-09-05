# ENH-E9 Requirements Revision

- Status: `REVIEW_REQUIRED`
- Authority: `docs/wiki/requirement_definition/10_requirements_definition.md`

## 1. Initial decision

ENH-E9 initialization時点では **New FR: NONE / New NFR: NONE / New AR: NONE** とする。

E9のcandidate scopeは既存Requirementへのconformance/usability enhancementとして評価する。

## 2. Primary traceability

| E9 concern | Current requirement authority | Initial decision |
|---|---|---|
| Saved Analysis View / Analysis Context usability | `FR-106`, `FR-168`, `FR-171`–`FR-173` | semantic deltaなしを第一仮説とする。baseline evidenceで確認 |
| Discovery / Graph interaction | `FR-035`–`FR-039`, `FR-174` | scientific semanticsを変えないUI conformance候補 |
| Identification inputs | `FR-040`, `FR-174` | causal question semanticsを変えないergonomics候補 |
| Diagnostics backend | `FR-044`, `FR-048` | **implementation truth再評価が必須** |
| Integrated workflow | `E2E-04`, `FR-174` + E8 protected contracts | regression acceptance |

## 3. FR-048 review rule

Current requirement text:

> estimator/analysisに適用可能なoverlap、balance、weight、sample loss等のdiagnosticをResultとして保存する。全estimatorへ同一diagnostic setを強制しない。

Current snapshot statusは `MUST / ACTIVE / IMPLEMENTED / BASELINE`。

E9では以下を検証する。

- applicable estimatorでeffective sample sizeがstructured Resultとして保存されるか
- estimatorが実際に使用したweightについてstable structured diagnosticsが存在するか
- weighting前後のbalanceが意味的に区別されるか
- difference-in-means / OLS / IPW / AIPWのapplicabilityがmethodologically区別されるか
- AIPWについて単一の「final weight」を捏造していないか

不足が確認された場合、`IMPLEMENTED` statusの整合性をHuman reviewへ戻す。E9 implementationだけでrequirement snapshotの過去truthをsilent修正しない。

## 4. Requirement revision trigger

次のいずれかが成立した場合のみcurrent requirement snapshot revisionを提案する。

1. current requirement本文ではrequired structured diagnostics semanticsを一意に規定できない。
2. existing requirement間に矛盾がある。
3. E9 acceptanceに新しいproduct obligationが必要で、既存Requirementから導出できない。

それ以外はRequirement semantic deltaなしとして実装conformanceを修正する。
