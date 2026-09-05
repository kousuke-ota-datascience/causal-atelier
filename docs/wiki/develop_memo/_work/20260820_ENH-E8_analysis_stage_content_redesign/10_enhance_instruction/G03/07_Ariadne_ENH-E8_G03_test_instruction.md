# Ariadne ENH-E8 G03 Verification Contract

- Document class: Primary Execution Contract / Acceptance Authority
- Verification contract status: `RETROSPECTIVE_FROZEN / A01_APPLIED / A02_APPLIED`
- Status: `RETROSPECTIVE_FROZEN / A01_APPLIED / A02_APPLIED`
- Gate: `G03`
- Historical reconstruction update: `2026-09-05`
- Source evidence cutoff: `61a4039ef90dafad74bf65b4ed7a43b7aca49aec`
- Amendments:
  - `09_ENH-E8_G03_A01_Gate_Contract_Amendment.md`
  - `09_ENH-E8_G03_A02_Gate_Contract_Amendment.md`

## 1. Gate PASS rule

retrospective verification開始時に固定したexact repository commit SHAに対して、blocking Acceptance CriterionがすべてPASSし、protected ENH-E8 regressionがgreenの場合のみPASSとする。

environment / harness要因で判定不能な場合はproduct FAILではなく`BLOCKED`とする。

CHAT-direct source commitsやhistorical test executionの存在だけを理由に、過去時点のformal PASSを遡及認定しない。

## 2. Acceptance Criteria — Estimation

| AC | Criterion | Primary layer |
|---|---|---|
| G03-AC01 | Estimation actionがIdentification formのnative submit ownershipから独立している | frontend contract / product test |
| G03-AC02 | hidden Identification required controlsがinvalidでもEstimation action handlerへ到達できる | Browser E2E |
| G03-AC03 | Identification Result未選択時は明示的にsubmissionを拒否する | frontend behavior / Browser E2E |
| G03-AC04 | selected Identification Resultのexecution lineageを`prefill`から復元する | product test / frontend contract |
| G03-AC05 | `dataset_version_id` / `input_graph_version_id` / `analysis_spec`をcurrent hidden form値から取得しない | product test / code audit |
| G03-AC06 | `input_result_id`がselected Identification Resultを参照する | product test / integration |
| G03-AC07 | invalid / incomplete Identification prefill lineageではsubmissionしない | frontend integration |
| G03-AC08 | submission operation / endpointが既存`ESTIMATION` execution-batch contractを維持する | product/integration |
| G03-AC11 | handler attachment前のEstimation buttonが`type="button"`かつdisabledで、native/shared-form submitへfallbackしない | Browser E2E / DOM lifecycle |
| G03-AC12 | `DOMContentLoaded`を起点としてsubmission module loadを開始し、`window.load`待ちinteraction raceを作らない | frontend contract / Browser E2E |
| G03-AC13 | canonical Compose frontend runtimeがcurrent sourceの`/causal_estimation_submission.js`をHTTP successで配信し、runtime readerからread可能である | container/runtime integration |
| G03-AC14 | regression evidenceがcurrent semantic contractを検証し、obsolete exact source-string assertionをPASS authorityにしない | test audit |

## 3. Acceptance Criteria — Effects

| AC | Criterion | Primary layer |
|---|---|---|
| G03-AC15 | Effects Stageが保存済み`TREATMENT_EFFECT_RESULT`をStage固有primary result sourceとしてrenderする | Browser E2E / frontend integration |
| G03-AC16 | Effects surfaceがstatus / estimand / treatment / outcome / estimator / estimate / standard error / confidence interval / adjustment setをhuman-readableに提示する | Browser E2E / DOM contract |
| G03-AC17 | scientific statusが解釈条件を満たさない場合、effect estimateを無条件のcausal conclusionとして提示しない | frontend behavior / focused test |
| G03-AC18 | Scientific warningsとtechnical lineageを保持し、raw evidenceへ追跡可能である | Browser E2E / DOM contract |
| G03-AC19 | Effects moduleがapp runtime declaration後にload/installされ、保存済みResult更新に追従する | Browser E2E / runtime integration |
| G03-AC20 | Effects presentationはAPI/schema/backend estimation semanticsを変更しない | diff / architecture audit |

## 4. Acceptance Criteria — Diagnostics

| AC | Criterion | Primary layer |
|---|---|---|
| G03-AC21 | Diagnostics Stageが保存済み`DIAGNOSTICS_RESULT`をStage固有primary diagnostic sourceとしてrenderする | Browser E2E / frontend integration |
| G03-AC22 | Diagnostics surfaceがanalysis context / sample support / balance / overlap / warningsをhuman-readableに提示する | Browser E2E / DOM contract |
| G03-AC23 | associated Treatment Effectを同一Executionから参照し、effect主解釈をEffects Stageへ委譲する | frontend integration |
| G03-AC24 | backend未保存のESS / weight diagnostics / weighted balance等を推測表示せず、利用不能であることを明示する | frontend behavior / code audit |
| G03-AC25 | Diagnostics technical detailsからresult / execution / analysis spec / dataset / graph / upstream result lineageへ追跡できる | Browser E2E / DOM contract |
| G03-AC26 | `causal_diagnostics_presentation.js`がcanonical runtimeで実際にload/installされる | Browser E2E / runtime integration |
| G03-AC27 | source fileが存在するだけではDiagnostics completionと判定しない | verification audit |

## 5. Cross-cutting Acceptance Criteria

| AC | Criterion | Primary layer |
|---|---|---|
| G03-AC09 | ENH-E8 G02のStage visibility/separation behaviorを壊さない | protected regression + Browser E2E |
| G03-AC10 | API/schema/DB/backend causal semanticsに不要な変更がない | diff / architecture audit |
| G03-AC28 | canonical Compose runtimeからG03 required frontend assetsをcurrent candidate sourceとして配信できる | runtime integration |
| G03-AC29 | historical commit messageの`ENH-E9`表記をprovenanceとして保持しつつ、Human指定どおりENH-E8 G03 evidenceとして追跡できる | audit / traceability |

## 6. Historical source evidence audit

A02では少なくとも次のsource commitsをaudit対象とする。

- `4815d557f6a6d2ff354c11ee26f73c6be627c411`
- `06f9aa11128ab3e82bab061524bcfe30343c5d98`
- `f5367d66cef1c599dc9406dfedf8e20ee90a60cd`
- `bf9ba32ea518135023aed2b47626bcde12dcb7bd`
- `0a6719675a561ccb45cd6b4f9b041d5b974d09f2`
- `09d168343498bab80a7b6df673ded64af28707fa`
- `3cb24e8e647a9fc70c72b9336a9647937aded076`
- `61a4039ef90dafad74bf65b4ed7a43b7aca49aec`

これらはhistorical implementation evidenceであってformal verification evidenceではない。

## 7. Automated regression evidence policy

Historical Estimation regression guard:

```bash
pytest -q tests/product/test_enh_e9_estimation_submission_regression.py
```

このtestはA01時点で旧bootstrap implementation detailをexact source stringとしてassertしていた。FAIL時はsemantic regressionかstale assertionかを分類し、stale assertionを満たすためcurrent implementationを後退させない。

Effects / Diagnosticsについては、source file existenceやstatic string assertionだけでblocking ACをPASSにしない。runtime renderingとStage ownershipをBrowser E2Eまたはequivalent integration evidenceで観測する。

## 8. Required Browser E2E — Estimation

少なくとも:

1. Estimation Stageで`#run-estimation`がvisibleである。
2. hidden Identification required controlsがinvalidでもaction-level validationへ到達する。
3. handler pre-ready stateでbuttonが`type="button"`かつdisabledである。
4. module load完了後にbuttonがenableされる。
5. selected Identification Resultからprefill lineageを復元し、`ESTIMATION` execution-batch requestへ渡る。

handler loadを意図的に遅延し、pre-ready temporal stateを観測する。最終DOMだけでAC11/AC12をPASSにしない。

## 9. Required Browser E2E — Effects

保存済み`TREATMENT_EFFECT_RESULT`を持つcandidate dataを構成し、少なくとも:

1. Effects StageでTreatment Effect cardがvisibleである。
2. estimator / estimand / treatment / outcome / estimate / uncertaintyがraw JSONを開かなくても読める。
3. Scientific warningsが存在する場合に表示される。
4. non-VALID等のstatusではinterpretationが無条件のcausal conclusionにならない。
5. Technical details / Lineageから元Result / execution contextを追跡できる。
6. 他StageでEffects primary surfaceがcurrent Stageとして露出しない。

## 10. Required Browser E2E — Diagnostics

保存済み`DIAGNOSTICS_RESULT`を持つcandidate dataを構成し、少なくとも:

1. Diagnostics Stageでhuman-readable diagnostic cardがvisibleである。
2. sample support / covariate balance / applicable overlap / warningsが表示される。
3. backendに構造化値がない項目は「利用不能」であることが明示され、fabricated numeric valueを表示しない。
4. associated Treatment Effectが存在する場合に同一Executionへ対応する。
5. Technical details / Lineageを追跡できる。
6. `causal_diagnostics_presentation.js`のnetwork loadまたはequivalent runtime install evidenceが存在する。

`61a4039...` source auditではDiagnostics artifactは存在する一方、`causal_stage_presentation.js`からのDiagnostics load wiringを確認できない。したがって同commitをcandidateとする場合、AC26はPASSと推定せず実runtime observationを要求する。load/installされなければ`FAIL`、environment上観測不能なら`BLOCKED`とする。

## 11. Frontend asset delivery verification

canonical Compose runtimeをbuildし、少なくとも:

- frontend serviceが`Dockerfile.frontend`からcurrent candidate sourceを含むimageとしてbuildされる。
- required G03 JS assetsがHTTP successで取得できる。
- nginx processがstatic assetsをread/traverseできるpermissionを持つ。
- host bind mountの偶然のpermission / local filesystem stateへ依存しない。

fileがrepositoryに存在すること自体をruntime delivery PASS evidenceにしない。

## 12. Fixed Verification Candidate identity

verification開始直前にrepositoryのexact commit SHAを取得し、A02適用済みG03 Trial01のFixed Verification Candidateとしてevidenceへ記録する。

`61a4039...`はhistorical source evidence cutoffであり、自動的なFixed Verification Candidateではない。

verification中にcandidateが変化した場合、その結果を同一candidateのPASS evidenceとして使用しない。

## 13. Protected regression

少なくとも次を保護する。

- ENH-E8 G01 Project return navigation
- ENH-E8 G02 Causal Stage content separation
- existing Identification submission behavior
- existing execution-batch API contract
- canonical Compose API/backend startup behavior
- existing Result / execution lineage semantics

## 14. Test Agent prohibited work

Test Agentはverification中に次を行わない。

- product code修正
- Acceptance Criteriaの緩和
- hidden Identification controls再表示等のworkaround
- historical evidenceの改変
- `ENH-E9` commit labelを削除・改変してprovenanceを消すこと
- stale testをgreenにするためcurrent implementationを旧bootstrap方式へ戻すこと
- Effects / Diagnosticsの未保存情報をfrontendで捏造してACを満たすこと
- Diagnostics source file存在だけでruntime integrationをPASSにすること

## 15. Decision

Test Item evidence作成後、G03のcanonical decisionを`PASS` / `FAIL` / `BLOCKED`のいずれかで記録する。

A02 re-baseline時点では、retrospective Independent Verificationを実行済みとは扱わない。
