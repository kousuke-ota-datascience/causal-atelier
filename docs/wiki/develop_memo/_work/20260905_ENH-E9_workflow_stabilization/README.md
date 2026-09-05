# ENH-E9 — Post-E8 Workflow Stabilization

**Document class:** Enhancement Workflow Instance / Authoring Guide  
**Workflow state:** `FROZEN / READY_FOR_G01_CODING`  
**Working branch:** `bugfix/ariadne_mvp_e9`  
**E9 baseline SHA:** `93fc2492112889a9465296a8647c251f84151bc5`

## 1. Objective

ENH-E9は新しいanalytical capabilityを追加しない。ENH-E8後の実利用で残ったworkflow usability gapと、既存Causal Diagnostics requirementに対するbackend conformance gapを、Stage responsibility / Result-Execution lineage / navigation semanticsを変更せず閉じる。

Historical `20260822_NEXT_Enhance_request/Enhance_request.md` は要求の出所・観測inventoryとして扱う。Coding時は、各GateのAcceptance Criteriaをcurrent baselineで既に満たしている項目を再実装せず、verification evidenceのみ追加してよい。

## 2. Entry decision

Human ownerは2026-09-05にENH-E8 G03を「解決済み・freeze」と決定した。したがってE8 G03 formal Independent VerificationをE9の未解決blocking prerequisiteとして扱わない。

E9のsource baselineは、E9 workflow初期化commitでありsource implementationを変更していない `93fc2492112889a9465296a8647c251f84151bc5` とする。

## 3. Authority

1. `docs/wiki/requirement_definition/**` — current canonical requirements/designの参照authority。E9から直接変更しない。
2. `00_enhance_background/Revised_requirements_definition_documents/**` — E9で必要なcanonical revision案を保持するlocal revised snapshot。
3. `00_enhance_background/03_requirements_revision.md` / `04_design_revision.md` — E9 requirement/design delta authority。
4. 各Gate `06` — implementation semantic authority。
5. 各Gate `07` — Acceptance Criteria / Independent Verification authority。
6. Work Package文書 — coding execution boundary。Gate semanticsを変更できない。
7. `999_gate_decision` — final Gate authority。

## 4. Frozen Gate structure

| Gate | Claim | Mode | Entry |
|---|---|---|---|
| G01 | Saved Analysis ViewとAnalysis Contextの意味を既存resource ownershipを変えず確認できる | SINGLE_EXECUTION | READY |
| G02 | Discovery→Graph比較/選択/採用を明確なinteractionとして利用できる | WORK_PACKAGE | G01 PASS |
| G03 | Identification inputの意味と候補をscientific semanticsを変えず指定できる | SINGLE_EXECUTION | G02 PASS |
| G04 | applicable diagnosticsをstable structured `DIAGNOSTICS_RESULT`として保存しfrontendが推測不要で利用できる | WORK_PACKAGE | G03 PASS |
| G05 | G01–G04統合後もcritical Causal browser journeyが成立する | SINGLE_EXECUTION | G04 PASS |

## 5. Outcome provenance / protected behavior

`Outcome one-way ownership` はcanonical用語として使用しない。2026-08-23 historical Enhance Requestに明示された次のbehaviorを保護する。

```text
Discovery designated Outcome
  -> FIXED Graph / GraphVersion designated_outcome_node
  -> Identification Outcome = automatic inheritance / input不要
  -> Estimation uses selected Identification Result lineage
```

禁止: Identificationで独立Outcomeを編集可能にすること、Estimationに独立Outcome overrideを追加すること、Graph lineageと無関係なOutcomeをUI convenienceで差し替えること。

## 6. G04 confirmed baseline gap

Baseline sourceでは`DIAGNOSTICS_RESULT`にsample size / design / unweighted balance / overlapが保存される。一方、IPWで計算されるESS/analysis weightsはstable structured diagnosticsとして保存されず、adapterはbalanceをweightなしで計算している。よってFR-048はE9 baselineでfull conformanceとみなさず、G04でconformanceを完成させる。

Exact structured contractは`00_enhance_background/04_design_revision.md`およびG04 `06/07`をauthorityとする。

## 7. Protected regressions

- canonical Navigation Stage catalog / route grammar
- Navigation Stage != Execution operation
- Project / Analysis Context resource ownership
- Discovery Result / Graph Candidate / DRAFT-FIXED GraphVersion semantics
- Identification Result / execution lineage
- Estimation submission architecture
- Effects / Diagnostics presentation ownership
- frontendが未保存diagnosticsを推測・捏造しないこと

## 8. Out of scope

Predictive advanced capability (LightGBM/SHAP/LIME等)はENH-E10、causal foundation reconciliationはENH-E11。Project Management IA redesign、new Navigation Stage、new runtime Stage、不要なAPI route/persistence redesignもE9外。

## 9. Execution order

G01 → G02 → G03 → G04 → G05。各Gateは06/07に従いFixed Trial Candidateを作り、Independent Verificationの`999_gate_decision`がPASSになるまで次Gateへ進まない。formal FAILは08、Gate semantic/AC defectは09 amendmentで扱う。
