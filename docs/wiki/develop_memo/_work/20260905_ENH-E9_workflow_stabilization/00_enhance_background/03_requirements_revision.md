# ENH-E9 Requirements Revision

- Status: `FROZEN`
- Canonical reference: `docs/wiki/requirement_definition/10_requirements_definition.md`
- E9 revised-document location: `00_enhance_background/Revised_requirements_definition_documents/`

## 1. Decision

ENH-E9では **New FR: NONE / New NFR: NONE / New AR: NONE** とする。E9 scopeは既存requirementへのconformance/usability enhancementである。

## 2. Traceability

| E9 concern | Requirement authority | E9 decision |
|---|---|---|
| Saved Analysis View / Analysis Context usability | FR-106, FR-168, FR-171–FR-174 | semantic deltaなし。presentation/usability conformance |
| Discovery / Graph interaction | FR-035–FR-039, FR-174 | scientific semanticsを変えないinteraction conformance |
| Identification inputs | FR-040, FR-174 | causal-question semanticsを変えないergonomics |
| Diagnostics backend | FR-044, FR-048 | **baseline implementation gap confirmed; conformance completion required** |
| Integrated workflow | E2E-04, FR-174 + protected E8 contracts | regression acceptance |

## 3. FR-048 implementation truth

FR-048 requirement textは変更しない。Current canonical snapshotのstatus表記が`IMPLEMENTED`であっても、E9 baseline sourceではfull conformanceを満たしていない。

Confirmed facts:

- `DIAGNOSTICS_RESULT`はsample-size/design/balance/overlapをstructured payloadとして保存する。
- adapterのbalance計算はweightなしで呼ばれ、current `balance`はpost-weighting balanceではない。
- IPW estimatorはESSを内部計算するが、stable structured `DIAGNOSTICS_RESULT` fieldとしてpersistしない。
- actual IPW analysis weight distributionもstructured diagnosticsとしてpersistしない。

したがってE9 execution上のtruthは `FR-048 REQUIREMENT ACTIVE / BASELINE IMPLEMENTATION PARTIALLY CONFORMANT` とする。Canonical source document自体は本Enhancementから直接変更しない。必要なrevision案はRevised snapshot配下にのみ保持する。

## 4. Outcome inheritance

FR-040はOutcomeをCausal Question構成要素として定義する。Historical 2026-08-23 Enhance RequestはIdentificationのOutcomeについて `必須・入力不要 / FIXED Graphから自動継承` と明示している。

E9ではこのexisting behaviorをregression protectionとして扱う。ただし `Outcome one-way ownership` という語をcanonical requirement名として導入しない。

## 5. Requirement-change trigger

G01–G05 execution中に、既存Requirement本文からAcceptance Criteriaを導出できない新しいproduct obligationが判明した場合のみ、Gate semantic changeを停止し、09 amendment + revised requirement proposalへ戻す。Implementation都合でRequirement truthをsilent変更しない。
