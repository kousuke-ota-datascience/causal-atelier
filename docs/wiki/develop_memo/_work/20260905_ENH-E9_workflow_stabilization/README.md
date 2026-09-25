# ENH-E9 — Post-E8 Workflow Stabilization

**Document class:** Enhancement Workflow Instance / Authoring Guide  
**Workflow state:** `FROZEN_ACTIVE_EXECUTION`  
**Working branch:** `bugfix/ariadne_mvp_e9`  
**E9 baseline SHA:** `93fc2492112889a9465296a8647c251f84151bc5`

## 1. Objective

ENH-E9は新しいanalytical capabilityを追加しない。ENH-E8後の実利用で残ったworkflow usability gapと、既存Causal Diagnostics requirementに対するbackend conformance gapを、Stage responsibility / Result-Execution lineage / navigation semanticsを変更せず閉じる。

Historical `20260822_NEXT_Enhance_request/Enhance_request.md` は要求の出所・観測inventoryとして扱う。Coding時は、各GateのAcceptance Criteriaをcurrent baselineで既に満たしている項目を再実装せず、verification evidenceのみ追加してよい。

## 2. Entry / current progress

Human ownerは2026-09-05にENH-E8 G03を「解決済み・freeze」と決定した。したがってE8 G03 formal Independent VerificationをE9の未解決blocking prerequisiteとして扱わない。

E9 source baselineは、workflow初期化commitでありsource implementationを変更していない `93fc2492112889a9465296a8647c251f84151bc5`。

Current E9 progress index:

| Gate | Mode | Current operational state | Entry authority |
|---|---|---|---|
| G01 | SINGLE_EXECUTION | PASS | canonical G01 999 |
| G02 | WORK_PACKAGE | READY_FOR_TEST | G01 PASS |
| G03 | WORK_PACKAGE | WAITING_G02_PASS | canonical G02 999 PASS |
| G04 | WORK_PACKAGE | WAITING_G03_PASS | canonical G03 999 PASS |
| G05 | WORK_PACKAGE | WAITING_G04_PASS | canonical G01–G04 999 PASS |

`READY_FOR_TEST` / Candidate Assembly / Package completionはGate PASSではない。Next Gate entryは必ずprevious Gate canonical `999_gate_decision = PASS`で判定する。

## 3. Authority

1. `docs/wiki/requirement_definition/**` — current canonical requirements/designの参照authority。E9から直接変更しない。
2. `00_enhance_background/Revised_requirements_definition_documents/**` — E9で必要なcanonical revision案を保持するlocal revised snapshot。
3. `00_enhance_background/03_requirements_revision.md` / `04_design_revision.md` — E9 requirement/design delta authority。
4. 各Gate `06` — implementation semantic authority / Gate-wide traceability。
5. 各Gate `07` — Acceptance Criteria / Independent Verification authority。
6. Work Package `06_Gxx_Pxx_*.md` — isolated Coding execution boundary。Assigned Coding Agentにとってself-contained normative implementation contract。
7. `999_gate_decision` — final Gate terminal authority。

Coding Agentはassigned Pxxを仕様補完するためにparent 06/07/P00/other Pxxを読まない。必要semantic fragmentはPxx自身に明示する。

## 4. Execution structure

### G01

G01は既にPASS済みであり、そのTrial01 terminal authorityを遡及変更しない。

### G02–G05

未完了Gateは共通Work Package Coding Agentで開始する。

```text
GATE_ID=G0*
PACKAGE_ID=P01
TRIAL_NO=01

40_operator_workflows/agent_entry_prompts/
10_normal_execution_02_work_package_coding_agent_prompt.md
```

P00はすべてplanning-only / non-executable。実行PackageはP01から始める。

Required package chain:

```text
G02: P01 -> P02 -> P03 -> Candidate Assembly -> Independent Verification
G03: P01 -> Candidate Assembly -> Independent Verification
G04: P01 -> P02 -> P03 -> P04 -> Candidate Assembly -> Independent Verification
G05: P01 -> Candidate Assembly -> Independent Verification
```

各Package dependencyはcanonical evidenceから判定し、status literalの手動書換えで進行させない。

## 5. 2026-09-06 execution-contract rebaseline

E7/E8比較reviewにより、未通過GateのPxxがCoding Agent information-isolationに対して薄い箇所を確認した。

`00_enhance_background/07_execution_contract_self_containment_review.md`をreview authorityとし、G03–G05のPxxをself-contained contractへrebaselineした。

Classification:

```text
NON_SEMANTIC_EXECUTION_CONTRACT_REBASELINE
Gate claim change: NONE
Acceptance Criteria change: NONE
Requirement semantic change: NONE
```

G01 PASSは変更しない。G02 Trial01 Fixed Candidateもprovenance保護のため遡及変更せず、現candidateに対するIndependent Verificationを完了する。

Review開始時点でG02は`READY_FOR_TEST`でcanonical 999 PASS未作成だったため、それ以前に開始されたG03 Trial01/P01 Coding成果はFixed Trial Candidate evidenceとして採用しない。G02 PASS後、re-baselined G03 P01を最初から実行する。

## 6. Outcome provenance / protected behavior

`Outcome one-way ownership` はcanonical用語として使用しない。Protected behavior:

```text
Discovery designated Outcome
  -> FIXED Graph / GraphVersion designated_outcome_node
  -> Identification Outcome = automatic inheritance / input不要 / read-only
  -> selected Identification Result lineage
  -> Estimation
```

禁止: Identificationで独立Outcomeを編集可能にすること、Estimationに独立Outcome overrideを追加すること、Graph lineageと無関係なOutcomeをUI convenienceで差し替えること。

## 7. G04 diagnostics contract

Baseline sourceでは`DIAGNOSTICS_RESULT`にsample size / design / unweighted balance / overlapが保存される。一方、IPWで計算されるESS/analysis weightsはstable structured diagnosticsとして保存されず、adapterはbalanceをweightなしで計算している。よってFR-048はE9 baselineでfull conformanceとみなさず、G04でconformanceを完成させる。

Stable direction:

- `balance.before` = unweighted
- `balance.after` = scientifically applicable actual/component-weight balance or null
- applicability = `ESTIMATOR_WEIGHT | PROPENSITY_COMPONENT | NOT_APPLICABLE`
- IPW actual arm weights / ESS / stats persist
- AIPWはwhole-estimator final weightを捏造しない
- OLS/difference-in-meansはNOT_APPLICABLE
- `extreme_rule = "weight > 10.0"`
- `weight == 10.0`はextremeに含めない
- frontendはpersisted diagnosticsを直接consumeし再計算/string parsingしない

Exact authorityは`00_enhance_background/04_design_revision.md`、G04 06/07、isolated P01–P04 contract。

## 8. Browser E2E policy

- Package CodingではBrowser E2Eを実行しない。
- G03/G04ではBrowser E2Eをacceptance numeric/scientific proofとして実行しない。
- G05 Independent Verificationで、static/unit/integration/contract/protected regressionを完了・評価した後、**最後のverification item**としてcritical Browser E2Eを実行する。
- Browser E2Eはcross-layer connectivity proofであり、G04 ESS/weight/balance correctnessのprimary authorityではない。

## 9. Protected regressions

- canonical Navigation Stage catalog / route grammar
- Navigation Stage != Execution operation
- Project / Analysis Context resource ownership
- Discovery Result / Graph Candidate / DRAFT-FIXED GraphVersion semantics
- FIXED Graph designated Outcome lineage
- Identification Result / execution lineage
- Estimation submission architecture
- Effects / Diagnostics presentation ownership
- frontendが未保存diagnosticsを推測・捏造しないこと

## 10. Out of scope

Predictive advanced capability (LightGBM/SHAP/LIME等)はENH-E10、causal foundation reconciliationはENH-E11。Project Management IA redesign、new Navigation Stage、new runtime Stage、不要なAPI route/persistence redesignもE9外。

## 11. Terminal routing

各Gateは06/07に従いFixed Trial Candidateを作り、Independent Verificationのcanonical `999_gate_decision`がPASSになるまで次Gateへ進まない。

- PASS -> current Gate COMPLETE。next Gateを開始するならnext Gate Phase Aへ
- FAIL -> formal FAIL remediation route
- BLOCKED -> blocker resolution

Phase Fで新しいstate/transition/promotion artifactを作らずcanonical 999をterminal authorityとする。
