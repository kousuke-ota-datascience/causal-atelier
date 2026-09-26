# Contract Amendment Log — append-only ledger

**Document class:** Planning / Evidence / Governance Artifact  
**Self-containment:** MUST for own responsibility — freeze / approval後に行われたcontract amendmentの履歴、理由、影響、承認、re-baseline、Git traceabilityをこの文書だけで追跡できること。

## 1. Purpose

本ledgerは、freeze / approval済みcontractに欠陥または変更必要性が判明した場合のamendment履歴をappend-onlyで記録する。

本ledger自体は06 / 07 / Pxx / Rxxのnormative execution authorityではない。Gate-localなcontract change decisionは09に記録し、承認後にaffected primary contractsを明示的にre-baselineする。

## 2. Invariants

- 既存entryを削除・上書きしない。
- 過去TrialのBLOCKED / FAIL / Test Item / Gate Decision evidenceを改変しない。
- amendmentをfailed implementationに合わせてAcceptance Criteriaを緩める手段として使用しない。
- `AMENDMENT_ID`は一意とする。
- amendment application commitのSHAを、同一commit内の本文へ自己参照的に事前記載しない。
- commit SHAが必要な場合は、application後のruntime-derived valueとしてterminal handoffまたは後続traceability entryで固定する。

## 3. Canonical entry schema

各amendmentを以下の形式で末尾へ追記する。

### {{AMENDMENT_ID}} — {{TITLE}}

- Status: PROPOSED / APPROVED / REJECTED / APPLIED
- Trigger: {{TRIGGER}}
- Trigger evidence: {{PATHS_OR_SHA}}
- Gate(s): {{GATE_IDS_OR_NA}}
- Trial(s): {{TRIAL_IDS_OR_NA}}
- Amendment type: CONTRACT_DEFECT / REQUIREMENT_CHANGE / DESIGN_CHANGE / OTHER
- Gate-local 09: {{PATH_OR_NA}}
- Human / architecture owner approval: {{APPROVAL_EVIDENCE}}

#### Affected normative documents

| Artifact | Before identity | Required action | After identity / path |
|---|---|---|---|
| {{PATH}} | {{SHA_OR_VERSION}} | REBASELINE / REPLACE / NONE | {{PATH_OR_SHA}} |

#### Semantic impact

{{SEMANTIC_IMPACT}}

#### Downstream convergence

- Invalidated P00 / Pxx / Rxx: {{IDS_OR_NONE}}
- Invalidated candidate(s): {{SHA_OR_NONE}}
- Required new Trial: YES / NO / N/A
- Required operator route: {{ROUTE}}
- Canonical evidence / downstream dependency impact: {{IMPACT_OR_NONE}}

#### Evidence preservation

- Historical blocker / FAIL evidence preserved: YES / NO
- Immutable evidence paths: {{PATHS}}

#### Git traceability

- Amendment authoring / approval evidence commit: {{SHA_OR_PENDING}}
- Re-baseline / application commit: {{SHA_OR_PENDING}}
- Traceability follow-up commit: {{SHA_OR_NA}}

#### Notes

{{NOTES_OR_NONE}}
