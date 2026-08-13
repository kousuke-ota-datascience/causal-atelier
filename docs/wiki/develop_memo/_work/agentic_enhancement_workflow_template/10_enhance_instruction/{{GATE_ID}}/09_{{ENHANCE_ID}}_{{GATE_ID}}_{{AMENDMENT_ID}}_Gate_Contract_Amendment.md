# {{ENHANCE_ID}} {{GATE_ID}} {{AMENDMENT_ID}} Gate Contract Amendment

**Document class:** Derived Contract  
**Self-containment:** MUST for amendment decision — 何が誤り、何をどう変えるか、何をre-baselineするかを本書内で理解できること。元契約全文はtraceabilityとして参照してよい。

- Amendment ID: {{AMENDMENT_ID}}
- Gate: {{GATE_ID}}
- Status: PROPOSED / APPROVED / REJECTED
- Human / architecture owner approval: {{APPROVAL}}
- Affected 06: {{PATH_06}}
- Affected 07: {{PATH_07}}
- Affected P00 / package instructions: {{PATHS_OR_NONE}}
- Contract Amendment Ledger: 00_enhance_background/80_contract_amendment_log.md

## 1. Contract defect
{{CONTRACT_DEFECT}}

## 2. Why 08 remediation is insufficient
{{WHY_08_CANNOT_SOLVE}}

## 3. Before / After semantic change

| Concern | Before | After | Reason |
|---|---|---|---|
| {{CONCERN}} | {{BEFORE}} | {{AFTER}} | {{REASON}} |

## 4. Acceptance Criteria impact

| AC | Before | After | Rationale |
|---|---|---|---|
| {{AC_ID}} | {{BEFORE}} | {{AFTER}} | {{RATIONALE}} |

## 5. Protected passed-Gate impact
{{PROTECTED_IMPACT}}

## 6. Execution plan invalidation

- P00 invalidated: YES / NO / N/A
- Package instructions invalidated: {{PACKAGE_IDS_OR_NONE}}
- Existing candidate invalidated: YES / NO

## 7. Required re-baseline

承認後、次のprimary contract / planを再生成またはversioned replacementする。

- 06: {{REBASELINE_06_ACTION}}
- 07: {{REBASELINE_07_ACTION}}
- P00 / Pxx: {{REBASELINE_PACKAGE_ACTION_OR_NA}}

過去Trialが使用した06 / 07 / 08 / Test evidenceを上書きしない。

## 8. Trial handling
{{TRIAL_HANDLING}}

## 9. Re-approval evidence
{{APPROVAL_EVIDENCE}}

## 10. Amendment ledger / Git traceability

APPROVED / APPLIED時は`00_enhance_background/80_contract_amendment_log.md`へ同じ`AMENDMENT_ID`でappend-only entryを追加する。過去TrialのBLOCKED / FAIL evidenceは変更しない。application commit SHAはruntime-derivedであり、同一commit内へ架空値を事前記載しない。

## 11. Guardrail

An amendment must never be used merely to weaken Acceptance Criteria after a failed implementation. Contract changeには独立した設計・要求上の根拠とHuman approvalが必要である。
