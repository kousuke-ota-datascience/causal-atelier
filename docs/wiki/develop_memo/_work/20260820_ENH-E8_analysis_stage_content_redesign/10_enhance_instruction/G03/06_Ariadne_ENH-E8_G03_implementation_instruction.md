# Ariadne ENH-E8 G03 Implementation Contract

- Document class: Primary Execution Contract
- Contract status: `RETROSPECTIVE_FROZEN / A01_APPLIED / A02_APPLIED`
- Status: `RETROSPECTIVE_FROZEN / A01_APPLIED / A02_APPLIED`
- Gate: `G03`
- Execution Mode: `SINGLE_EXECUTION`
- Baseline: ENH-E8 archived state `f39f6860f83032efc08ded77f628353ecaf4797c`
- Initial reconstruction date: `2026-08-23`
- Historical reconstruction update: `2026-09-05`
- Source evidence cutoff: `61a4039ef90dafad74bf65b4ed7a43b7aca49aec`
- Document baseline before A02: `cf6b22626d9c3617f0361ad0d2fec93f8a1aa8d8`
- Amendments:
  - `09_ENH-E8_G03_A01_Gate_Contract_Amendment.md`
  - `09_ENH-E8_G03_A02_Gate_Contract_Amendment.md`

## 1. Gate claim

G03は、ENH-E8のCausal Stage separation後にCHAT上の直接編集で修復・追加された、**Causal Stageの実行可能性と結果presentationの後追いregression contract**である。

G03が成立するためには、少なくとも次の3 semantic claimを同時に満たす。

### G03-S1 — Estimation submission ownership / lineage

Estimation Stageのsubmission actionはIdentification Stageのhidden form controlsに阻害されず独立して起動できること。

Estimation submissionに必要なdataset / graph / analysis-spec lineageは、現在のhidden Identification form値から再構成せず、userが選択した保存済みIdentification Resultのexecution lineageをauthorityとして復元すること。

submission handlerのbootstrap中にuser-visible interaction raceを作らず、handler未ready期間にnative/shared-form submitへfallbackしないこと。canonical Compose frontend runtimeはcurrent sourceのEstimation submission moduleをreadable static assetとして確実に配信すること。

### G03-S2 — Effects Stage human-readable result presentation

Effects Stageは、保存済み`TREATMENT_EFFECT_RESULT`をraw JSON中心の表示だけにせず、causal question / estimator / effect estimate / uncertainty / warnings / lineageを人間が直接読めるStage固有surfaceとして提示すること。

表示は保存済みResultとexecution prefillをauthorityとし、新しいcausal estimateやbackend semanticsをfrontendで生成してはならない。

### G03-S3 — Diagnostics Stage human-readable diagnostic presentation

Diagnostics Stageは、保存済み`DIAGNOSTICS_RESULT`をraw payloadだけに委譲せず、analysis context、sample support、covariate balance、propensity overlap、scientific warnings、associated Treatment Effect、technical lineageをStage固有surfaceとして提示すること。

backendが構造化保存していないESS、weight diagnostics、weighted/post-adjustment balance等をfrontendで推測・捏造してはならない。利用不能な項目は利用不能であることを明示する。

## 2. Historical workflow exception

G03に関係する一部source変更は、agentic enhancement workflowの06 -> Coding Agent -> report -> 07 verificationという経路を通らず、CHAT上でrepository sourceを直接編集して実施された。

Human ownerが2026-09-05に指定したsource evidence cutoffは:

`61a4039ef90dafad74bf65b4ed7a43b7aca49aec`

その時点より後のdocument commitとして:

`cf6b22626d9c3617f0361ad0d2fec93f8a1aa8d8`

が存在するが、cf6b2262時点の06/07はEffects / Diagnosticsの直接編集履歴を十分に保持していなかった。

本A02 re-baselineはその欠落を修復する。過去に06/07を読んでCoding Agentが実行した、formal Trialが存在した、Independent Verificationが完了していた、とは遡及的に扱わない。

## 3. Reconstructed source history

初回G03 document commit `e1ab50c112d1845c5459048ca5f666914a7bf7e7` より後、source evidence cutoff `61a4039...` までに次のCHAT-direct source commitsが存在する。

| Commit | Historical commit message | G03での意味 |
|---|---|---|
| `4815d557f6a6d2ff354c11ee26f73c6be627c411` | `fix(ENH-E9): remove estimation button load-time race` | Estimation pre-ready race修復 |
| `06f9aa11128ab3e82bab061524bcfe30343c5d98` | `fix(ENH-E9): enable estimation only after handler binding` | handler binding後のみ操作可能にする |
| `f5367d66cef1c599dc9406dfedf8e20ee90a60cd` | `fix(ENH-E9): package frontend assets with readable permissions` | frontend asset delivery修復 |
| `bf9ba32ea518135023aed2b47626bcde12dcb7bd` | `fix(ENH-E9): stop bind-mounting frontend assets into nginx` | host bind mount依存除去 |
| `0a6719675a561ccb45cd6b4f9b041d5b974d09f2` | `fix(ENH-E9): preserve executable directory permissions in frontend image` | nginx image filesystem permission修復 |
| `09d168343498bab80a7b6df673ded64af28707fa` | `feat(ENH-E9): add human-readable causal effects presentation` | Effects Stage presentation追加 |
| `3cb24e8e647a9fc70c72b9336a9647937aded076` | `feat(ENH-E9): load causal effects presentation after app initialization` | Effects runtime bootstrap追加 |
| `61a4039ef90dafad74bf65b4ed7a43b7aca49aec` | `feat(ENH-E9): add human-readable causal diagnostics presentation` | Diagnostics Stage presentation artifact追加 |

commit message上は`ENH-E9`と記録されている。Human ownerは2026-09-05にこれらをENH-E8関連source historyとして指定したため、本G03では**historical commit labelを変更せず、ENH-E8 G03後追いevidenceとして分類**する。

## 4. Required behavior — Estimation

1. Estimation actionはIdentification form validationから独立した明示的button ownershipを持つ。
2. hidden Identification controlがinvalidでもbrowser native form validationにより遮断されない。
3. handler attachment前からEstimation buttonを`type="button"`とし、handler未ready期間はdisabledにする。
4. handler attachment完了後にのみEstimation buttonをenableし、native/shared-form submitへのfallback windowを作らない。
5. app runtime declaration後、`DOMContentLoaded`を起点としてsubmission module loadを開始する。
6. Estimation実行前に、userが選択した`IDENTIFICATION_RESULT`を取得する。
7. 選択Resultにexecution lineageが存在しなければsubmissionしない。
8. `/executions/{execution_id}/prefill`を使用し、prefillが`IDENTIFICATION`由来であることを確認する。
9. `dataset_version_id`、`input_graph_version_id`、`analysis_spec`はprefillをauthorityとして復元する。
10. `input_result_id`には選択済みIdentification Resultの`result_id`を使用する。
11. Estimation固有`operation_spec`、validation override、estimator variants、revision fieldsはEstimation action側で構成する。
12. submission先は既存`/projects/{project_id}/execution-batches`、operationは`ESTIMATION`を維持する。
13. successful submission後のexecution reload、warning表示、workspace draft-state更新を維持する。
14. canonical Compose frontend runtimeは`/causal_estimation_submission.js`をcurrent sourceからHTTP配信できる。

## 5. Required behavior — Effects

1. Effects Stageは保存済み`TREATMENT_EFFECT_RESULT`だけをprimary result sourceとする。
2. result cardでは少なくとも、scientific status、estimand、treatment、outcome、estimator、effect estimate、standard error、95% confidence interval、adjustment setを読める形で提示する。
3. execution prefillからcausal question / design contextを復元してよいが、prefill取得失敗時に新しい分析結果を推測してはならない。
4. scientific statusが解釈可能条件を満たさない場合、推定値を無条件にcausal conclusionとして表示しない。
5. Scientific warningsをResultから提示する。
6. technical details / lineageとしてresult identity、execution identity、analysis spec、dataset / graph / upstream result identityを追跡可能にする。
7. Effects presentation moduleはapp runtime declarationsが利用可能になった後にload / installされる。
8. Effects presentation追加によって`TREATMENT_EFFECT_RESULT`の保存形式、API、backend estimation semanticsを変更しない。

## 6. Required behavior — Diagnostics

1. Diagnostics Stageは保存済み`DIAGNOSTICS_RESULT`をprimary sourceとする。
2. analysis contextとしてestimand、treatment、outcome、estimator、adjustment setを可能な範囲で提示する。
3. sample supportとしてinput / complete observations、sample loss、treated / control counts、treated rate等、保存済み値または機械的に導出可能な値を提示する。
4. covariate balanceとして保存済みbalance rows、standardized mean difference、missing rateを提示する。
5. propensity-based estimatorに対し保存済みoverlap情報が存在する場合はpropensity distribution / configured range / out-of-range observationsを提示する。
6. Scientific warningsを明示する。
7. 同一Executionの`TREATMENT_EFFECT_RESULT`をassociated resultとして参照し、effectそのものの主解釈はEffects Stageへ委譲する。
8. technical details / lineageを追跡可能にする。
9. backendが保存していないESS、weight diagnostics、weighted/post-adjustment balanceをfrontendで生成したように見せてはならない。利用不能であることを明示する。
10. `causal_diagnostics_presentation.js`はcanonical runtimeから実際にload / installされなければならない。source fileが存在するだけではcompletionとしない。

## 7. Implementation boundary

Reconstructed implementation targets:

- `frontend/causal_estimation_submission.js`
- `frontend/causal_stage_presentation.js`
- `frontend/causal_effects_presentation.js`
- `frontend/causal_diagnostics_presentation.js`
- `Dockerfile.frontend`
- `compose.yaml`
- historical regression / Browser E2E artifacts under `tests/`

`frontend/causal_stage_presentation.js`はCausal submission / result computationのbusiness authorityにはしない。runtime module bootstrapとpre-ready safety stateに限定する。

Effects / Diagnostics presentation modulesは保存済みResultとexisting prefill APIをpresentationへ投影するfrontend responsibilityである。新しいresult type、API、persistence、causal computationを追加してはならない。

## 8. Known source-state observation at `61a4039...`

source auditでは:

- `causal_effects_presentation.js`が存在する。
- `causal_stage_presentation.js`は`DOMContentLoaded`後に`/causal_effects_presentation.js`をloadする。
- `causal_diagnostics_presentation.js`が存在し、loadされた場合は自己installする実装を持つ。
- しかし`61a4039...`時点の`causal_stage_presentation.js`はEstimation / Effectsのみをloadし、Diagnostics moduleのload wiringを含まない。

したがって、`61a4039...`はDiagnostics presentation artifactの存在evidenceではあるが、**Diagnostics runtime integration成立のevidenceではない**。formal G03 PASSを宣言してはならず、07でruntime integrationをblocking verification対象とする。

## 9. Protected contracts / non-goals

次を変更してはならない。

- ENH-E8 G01 Project Return Navigation contract
- ENH-E8 G02 Causal/Predictive Stage Content separation semantics
- canonical Causal Navigation Stage catalog
- API route grammar
- DB / persistence schema
- backend causal estimation semantics
- Identification Result / execution lineage semantics
- existing result type semantics
- frontendで未保存diagnosticsを科学的事実として捏造すること
- hidden control再表示やrequired属性無条件除去によるEstimation workaround
- handler readiness問題をfixed sleepや`window.load`待ちだけで隠すこと

## 10. Historical artifact identity / stale-test handling

historical source / test artifactsには`ENH-E9`名が含まれる。G03ではこれをhistorical provenanceとして保持し、名称だけから別enhancementのauthorityを推測しない。

`tests/product/test_enh_e9_estimation_submission_regression.py` はA01時点で旧bootstrap implementation detailをassertしておりstaleである。obsolete exact source-string assertionを満たすためにcurrent semanticsを後退させてはならない。

Effects / Diagnosticsについて、source file存在だけをtest coverageの代替にしない。

## 11. Coding-side verification obligations

少なくとも以下を確認する。

- Estimation pre-ready / ready lifecycleがG03-S1を満たす。
- selected Identification Resultのprefill lineageを使用する。
- canonical Compose frontend runtimeからrequired JS assetsを取得できる。
- Effects moduleがapp runtime後にloadされ、保存済みTreatment Effect Resultをhuman-readableにrenderする。
- Effects表示がscientific status / warnings / lineageを失わない。
- Diagnostics moduleがcanonical runtimeで実際にload / installされる。
- Diagnostics表示が保存済みdiagnosticsとbackend gapを正しく区別する。
- G02 Stage visibility/separation regressionがgreenである。
- API/schema/backend semanticsに不要な変更がない。

## 12. Candidate / evidence rule

本Gateはpost-hoc reconstructionであり、CHAT-direct source editing時のformal Fixed Trial Candidate transactionは存在しない。

A02は過去のsource commitsを新しいformal Trialへ遡及変換しない。

初回retrospective Independent Verificationでは、A02適用済みcontractに対してverification開始直前のexact repository commit SHAをG03 Trial01 Fixed Verification Candidateとして固定する。

`61a4039...`はhistorical source evidence cutoffであり、自動的にformal Fixed Verification CandidateまたはPASS candidateになるわけではない。

## 13. Exit

implementation / historical evidenceを記録してもCoding側からGate PASSを宣言しない。

Independent VerificationはA02適用済み`07_Ariadne_ENH-E8_G03_test_instruction.md`に従う。
