# ENH-E8 G03 Trial{{TRIAL_NO}} Remediation Instruction

- Document class: Remediation Contract / Historical Exception Note
- Status: `TEMPLATE_WITH_HISTORICAL_EXCEPTION_RECORD`
- Gate: `G03`
- Trial: `{{TRIAL_NO}}`

## 1. Canonical use condition

この08を**active remediation contract**として使用するのは、retrospective Independent Verificationによりcanonical G03 Gate Decision = `FAIL` が発行された場合のみである。

Input:

- failed Fixed Verification Candidate SHA
- failing G03 Test Item / Acceptance Criterion
- independent verification evidence
- effective `06_Ariadne_ENH-E8_G03_implementation_instruction.md`
- effective `07_Ariadne_ENH-E8_G03_test_instruction.md`

## 2. Canonical remediation rule

1. failed evidenceに直接対応する最小修正を定義する。
2. G03 semantic claim / Acceptance Criteriaをsilentに変更しない。
3. ENH-E8 G01/G02のpassed contractをregressionさせない。
4. hidden Identification controls再表示、required属性無条件除去、lineage authorityをcurrent form値へ戻す等のworkaroundを使用しない。
5. Effects / Diagnosticsでbackend未保存情報をfrontend推測値として補完しない。
6. 06/07自体のsemantic defectが判明した場合はremediationを中止し、`09` Gate Contract Amendmentへ送る。
7. remediation後は新しいFixed Trial Candidateを作り、次TrialでIndependent Verificationを行う。

Remediation completionはGate PASSではない。

## 3. Historical workflow exception — CHAT-direct rework

G03に関係する実source修正の一部は、上記canonical 08 activation conditionを満たす前に、agentic enhancement workflowを経由せずCHAT上から直接repositoryを編集して行われた。

したがって、次のsource commitsを「Trial{{TRIAL_NO}}のformal remediation execution」と遡及的に扱ってはならない。これらは**non-canonical CHAT-direct rework evidence**である。

| Commit | Historical message | Reconstructed purpose |
|---|---|---|
| `4815d557f6a6d2ff354c11ee26f73c6be627c411` | `fix(ENH-E9): remove estimation button load-time race` | Estimation bootstrap raceの除去 |
| `06f9aa11128ab3e82bab061524bcfe30343c5d98` | `fix(ENH-E9): enable estimation only after handler binding` | handler binding前のaction抑止 |
| `f5367d66cef1c599dc9406dfedf8e20ee90a60cd` | `fix(ENH-E9): package frontend assets with readable permissions` | static asset read permission修復 |
| `bf9ba32ea518135023aed2b47626bcde12dcb7bd` | `fix(ENH-E9): stop bind-mounting frontend assets into nginx` | host bind mount依存除去 |
| `0a6719675a561ccb45cd6b4f9b041d5b974d09f2` | `fix(ENH-E9): preserve executable directory permissions in frontend image` | directory traverse permission修復 |
| `09d168343498bab80a7b6df673ded64af28707fa` | `feat(ENH-E9): add human-readable causal effects presentation` | Effects human-readable result surface追加 |
| `3cb24e8e647a9fc70c72b9336a9647937aded076` | `feat(ENH-E9): load causal effects presentation after app initialization` | Effects runtime load wiring追加 |
| `61a4039ef90dafad74bf65b4ed7a43b7aca49aec` | `feat(ENH-E9): add human-readable causal diagnostics presentation` | Diagnostics presentation artifact追加 |

Human ownerは2026-09-05に上記source cutoff `61a4039...` をENH-E8関連historyとして明示した。

## 4. Why these commits are not canonical 08 remediation

これらの修正時点では:

- formal G03 Independent Verification FAIL decisionが存在しない。
- failed Fixed Verification Candidateが存在しない。
- current Trialを一意に解決する08がactive contractとしてCoding Agentへ渡されていない。
- source編集がCHATから直接実行された。

したがってTrial番号を捏造したり、これらをformal remediation executionとして記録したりしない。

一方で、実際に発生したfailure discovery -> direct correctionの履歴を消すことも不適切であるため、この08 template内に**historical exception record**として保持する。

## 5. Relationship to 09 amendments

- A01: Estimation bootstrap timing / frontend deliveryがblocking conditionであることをcontractへ追加した。
- A02: CHAT-direct historyを再監査した結果、G03 scopeにEffects / Diagnostics result presentationも含める必要があることを明示した。

これらはformal Test FAILに対するremediationではなく、retrospective contract incompletenessの修正であるため09で扱う。

## 6. Future use

今後G03がformal verificationでFAILした場合、このtemplateをcurrent Trial用08へ具体化する。その際、上記CHAT-direct commitsを「前Trial remediation」として再利用せず、failed candidate / failure evidence / effective A02 06/07から新しいremediation contractを作成する。
