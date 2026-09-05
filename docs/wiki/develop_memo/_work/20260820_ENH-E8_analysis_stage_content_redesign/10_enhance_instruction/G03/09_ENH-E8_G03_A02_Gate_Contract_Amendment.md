# ENH-E8 G03 Gate Contract Amendment A02

- Document class: Gate Contract Amendment
- Status: `APPROVED/APPLIED`
- Gate: `G03`
- Amendment ID: `A02`
- Amendment date: `2026-09-05`
- Trigger: CHAT-direct source editing historyの再監査とG03 coding instruction履歴欠落の修復
- Historical source evidence cutoff: `61a4039ef90dafad74bf65b4ed7a43b7aca49aec`
- Previous latest document commit supplied by Human: `cf6b22626d9c3617f0361ad0d2fec93f8a1aa8d8`

## 1. Amendment reason

Human ownerは、ENH-E8関連sourceについてagentic enhancement workflowを経由せずCHAT上で直接repository sourceを編集したため、G03 coding instructionに実変更履歴が残っていないことを2026-09-05に明示した。

cf6b2262時点のG03 06/07はA01までのEstimation submission / bootstrap / frontend delivery regressionを記録していたが、その後または同じCHAT-direct correction series内で実施された次のsemantic変更を十分に含んでいなかった。

1. Effects Stageへのhuman-readable Treatment Effect presentation追加。
2. Effects presentationをapp runtime initialization後にloadするruntime wiring追加。
3. Diagnostics Stageへのhuman-readable diagnostic presentation artifact追加。
4. source evidence cutoff `61a4039...` 時点ではDiagnostics artifactのruntime load wiringが確認できず、「file exists」と「Stageで成立する」を区別する必要がある。

これらはENH-E8 G02が意図したCausal Stage-specific content separationの後追いconformance / bugfixとしてHumanがENH-E8関連historyに分類したため、G03 effective contractへ追加する。

## 2. Why A01 alone is insufficient

A01は次に限定されていた。

- Estimation handler bootstrap timing safety
- frontend asset delivery
- stale Estimation regression test handling

A01ではEffects / Diagnosticsのresult presentation semantics、runtime integration、backend gapの表示規則をAcceptance Criteriaとして定義していなかった。

したがって、A01をsilent rewriteせずA02をappendし、06/07を再re-baselineする。

## 3. Why 08 is not the authority for this correction

CHAT-direct source changesはformal G03 Independent Verification FAIL後のremediationとして実行されたものではない。

- formal failed Fixed Verification Candidateなし
- canonical FAIL decisionなし
- active Trial-specific 08なし
- Coding Agentへ08を渡したexecutionなし

よって、実source commitsをformal Trial remediationとして捏造しない。

08にはnon-canonical CHAT-direct rework evidenceとして履歴だけを保持し、semantic claim / ACの拡張は09 A02で行う。

## 4. Historical source sequence incorporated by A02

初回G03 document commit `e1ab50c112d1845c5459048ca5f666914a7bf7e7` 以降、source cutoff `61a4039...` までの関連commitは次のとおり。

| Commit | Historical message | Classification |
|---|---|---|
| `4815d557f6a6d2ff354c11ee26f73c6be627c411` | `fix(ENH-E9): remove estimation button load-time race` | Estimation regression fix |
| `06f9aa11128ab3e82bab061524bcfe30343c5d98` | `fix(ENH-E9): enable estimation only after handler binding` | Estimation lifecycle fix |
| `f5367d66cef1c599dc9406dfedf8e20ee90a60cd` | `fix(ENH-E9): package frontend assets with readable permissions` | frontend delivery fix |
| `bf9ba32ea518135023aed2b47626bcde12dcb7bd` | `fix(ENH-E9): stop bind-mounting frontend assets into nginx` | frontend runtime isolation fix |
| `0a6719675a561ccb45cd6b4f9b041d5b974d09f2` | `fix(ENH-E9): preserve executable directory permissions in frontend image` | image filesystem fix |
| `09d168343498bab80a7b6df673ded64af28707fa` | `feat(ENH-E9): add human-readable causal effects presentation` | Effects Stage presentation |
| `3cb24e8e647a9fc70c72b9336a9647937aded076` | `feat(ENH-E9): load causal effects presentation after app initialization` | Effects runtime wiring |
| `61a4039ef90dafad74bf65b4ed7a43b7aca49aec` | `feat(ENH-E9): add human-readable causal diagnostics presentation` | Diagnostics presentation artifact |

commit messageの`ENH-E9`はhistorical provenanceとして維持する。Human ownerの明示指定により、G03ではこれらをENH-E8関連の後追いsource evidenceとして扱う。

## 5. Before / After contract semantics

### Before A02

G03は主に:

- Estimation submission ownership
- Identification Result lineage reuse
- bootstrap race prevention
- frontend asset delivery

を規定していた。

### After A02

上記に加えて:

- Effects Stageの保存済みTreatment Effect Result human-readable presentation
- Effects runtime bootstrap
- Diagnostics Stageの保存済みDiagnostics Result human-readable presentation
- diagnostics backend gapの非捏造表示
- Effects / Diagnosticsのlineage traceability
- Diagnostics presentation artifactのruntime load/install確認

をblocking semanticsとして追加する。

## 6. Added Acceptance Criteria

A02により06/07へ次を追加する。

### Effects

- `G03-AC15` Effects Stageが保存済み`TREATMENT_EFFECT_RESULT`をStage固有primary sourceとしてrenderする。
- `G03-AC16` status / estimand / treatment / outcome / estimator / estimate / uncertainty / adjustment setをhuman-readableに提示する。
- `G03-AC17` non-valid statusで無条件のcausal conclusionを提示しない。
- `G03-AC18` Scientific warningsとtechnical lineageを保持する。
- `G03-AC19` app runtime後にEffects moduleがload/installされる。
- `G03-AC20` backend/API/persistence semanticsを変更しない。

### Diagnostics

- `G03-AC21` Diagnostics Stageが保存済み`DIAGNOSTICS_RESULT`をStage固有primary sourceとしてrenderする。
- `G03-AC22` analysis context / sample support / balance / overlap / warningsをhuman-readableに提示する。
- `G03-AC23` associated Treatment Effectを同一Executionから参照する。
- `G03-AC24` backend未保存diagnosticsをfrontendで捏造しない。
- `G03-AC25` technical lineageへ追跡可能である。
- `G03-AC26` Diagnostics presentation moduleがcanonical runtimeで実際にload/installされる。
- `G03-AC27` source file existenceのみでcompletionと判定しない。

### Cross-cutting

- `G03-AC28` required G03 frontend assetsがcandidate sourceとしてcanonical Compose runtimeから配信される。
- `G03-AC29` historical `ENH-E9` commit labelsを保持しつつENH-E8 G03 evidenceへ追跡できる。

## 7. Known incomplete state at source cutoff

`61a4039...`時点で確認できるsource state:

- `frontend/causal_effects_presentation.js` exists.
- `frontend/causal_stage_presentation.js` loads `/causal_effects_presentation.js` after `DOMContentLoaded`.
- `frontend/causal_diagnostics_presentation.js` exists and self-installs if loaded.
- `frontend/causal_stage_presentation.js` does **not** load `/causal_diagnostics_presentation.js` at that cutoff.

したがって`61a4039...`はDiagnostics source artifactのimplementation evidenceではあるが、`G03-AC26`成立のevidenceではない。

A02はこのgapを隠さない。formal verificationでruntime load/installが成立しなければFAIL、environment理由で判定不能ならBLOCKEDとする。

## 8. Protected contract impact

A02は次を変更しない。

- ENH-E8 G01 Project Return Navigation
- ENH-E8 G02 canonical Causal/Predictive Stage identities
- canonical route / Navigation Stage catalog
- API route grammar
- DB / persistence schema
- backend causal estimation algorithms
- Result / execution lineage semantics

Effects / Diagnosticsはexisting saved Resultをpresentationへ投影するfrontend conformance changeであり、新しいanalytical result semanticsを追加しない。

## 9. Trial / candidate handling

A02時点でもG03 formal Independent Verificationは未実施として扱う。

- Trial番号は増加させない。
- CHAT-direct source commitsをTrial01 candidate transactionへ遡及変換しない。
- `61a4039...`を自動的なFixed Verification Candidateにしない。
- A02 effective 06/07に対するfuture verification開始直前のexact SHAをTrial01 Fixed Verification Candidateとして固定する。

## 10. Human approval / provenance

2026-09-05、Human ownerは以下を明示した。

- ENH-E8関連の最新source code commit SHA: `61a4039ef90dafad74bf65b4ed7a43b7aca49aec`
- 最新document commit SHA: `cf6b22626d9c3617f0361ad0d2fec93f8a1aa8d8`
- agentic enhancement workflowを経由せずCHAT上で直接sourceを編集したため、G03 coding instructionに履歴が残っていない。
- G03内06/07/08/09を会話履歴に基づいてUPDATEする。

この明示指示をA02 approval / provenanceとする。

## 11. Required re-baseline artifacts

A02適用により次をeffective stateへ更新する。

- `06_Ariadne_ENH-E8_G03_implementation_instruction.md`
- `07_Ariadne_ENH-E8_G03_test_instruction.md`
- `08_ENH-E8_G03_{{TRIAL_NO}}_Remediation_Instruction.md`
- `09_ENH-E8_G03_{{AMENDMENT_ID}}_Gate_Contract_Amendment.md` authoring template

A01はhistorical approved amendmentとしてimmutable provenanceを保持する。
