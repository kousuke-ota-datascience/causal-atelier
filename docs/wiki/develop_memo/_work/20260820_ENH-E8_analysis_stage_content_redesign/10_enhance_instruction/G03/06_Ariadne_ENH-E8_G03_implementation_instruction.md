# Ariadne ENH-E8 G03 Implementation Contract

- Document class: Primary Execution Contract
- Contract status: `RETROSPECTIVE_FROZEN / A01_APPLIED`
- Status: `RETROSPECTIVE_FROZEN / A01_APPLIED`
- Gate: `G03`
- Execution Mode: `SINGLE_EXECUTION`
- Baseline: ENH-E8 archived state `f39f6860f83032efc08ded77f628353ecaf4797c`
- Reconstruction date: `2026-08-23`
- Amendment: `09_ENH-E8_G03_A01_Gate_Contract_Amendment.md`

## 1. Gate claim

ENH-E8のCausal Stage separation後も、Estimation Stageのsubmission actionはIdentification Stageのhidden form controlsに阻害されず独立して起動できること。

Estimation submissionに必要なdataset / graph / analysis-spec lineageは、現在のhidden Identification form値から再構成せず、userが選択した保存済みIdentification Resultのexecution lineageをauthorityとして復元すること。

さらに、Estimation submission handlerのbootstrap中にuser-visible interaction raceを作らず、handler未ready期間にnative/shared-form submitへfallbackしないこと。canonical Compose frontend runtimeはcurrent sourceのEstimation submission moduleをreadable static assetとして確実に配信すること。

## 2. Problem reconstructed from post-ENH-E8 evidence

ENH-E8 archived stateでは、IdentificationとEstimationがpresentation上はStageごとに分離された一方、Estimation actionは共通`#inference-form`のsubmit semanticsに残存していた。

この構造では、Estimation Stageで非表示となっているIdentification側required controlがbrowser native validation上はinvalidのままとなり、Estimation button activationがEstimation submission処理へ到達しない回帰が成立し得る。

初回G03 reconstruction後の追加bugfixでは、submission moduleのloadを`window.load`まで遅延した場合、DOMが操作可能になってからhandler attachmentまでの間に同種のfallback raceが残ること、およびcanonical Compose frontend runtimeで追加JS assetを確実に配信するruntime delivery conditionが必要であることが明確になった。

このGateはこれらを別機能ではなく、Stage-specific presentationとsubmission ownershipをruntime lifecycle全体で成立させる同一regression contractとして扱う。

## 3. Required behavior

1. Estimation actionはIdentification form validationから独立した明示的button ownershipを持つ。
2. Estimation actionのactivationは、hidden Identification controlがinvalidであってもbrowser native form validationにより遮断されない。
3. submission handler attachment前からEstimation buttonを`type="button"`とし、handler未ready期間はdisabledにする。
4. handler attachment完了後にのみEstimation buttonをenableし、native/shared-form submitへのfallback windowを作らない。
5. app runtime declaration後、`DOMContentLoaded`を起点としてsubmission module loadを開始し、`window.load`待ちによるuser-visible interaction gapを作らない。
6. Estimation実行前に、userが選択した`IDENTIFICATION_RESULT`を一意に取得する。
7. 選択したIdentification Resultにexecution lineageが存在しなければsubmissionしない。
8. lineage復元は`/executions/{execution_id}/prefill`を使用し、prefillが`IDENTIFICATION`由来であることを確認する。
9. `dataset_version_id`、`input_graph_version_id`、`analysis_spec`はprefillをauthorityとして復元する。
10. `input_result_id`には選択済みIdentification Resultの`result_id`を使用する。
11. Estimation固有の`operation_spec`、validation override、estimator variants、revision fieldsはEstimation action側で構成する。
12. submission先は既存`/projects/{project_id}/execution-batches`、operationは`ESTIMATION`を維持する。
13. successful submission後のexecution reload、warning表示、workspace draft-state更新という既存UX semanticsを維持する。
14. canonical Compose frontend runtimeはcurrent sourceの`/causal_estimation_submission.js`をHTTP配信でき、nginx processからread可能である。

## 4. Implementation boundary

Reconstructed implementation targets:

- `frontend/causal_estimation_submission.js`
- `frontend/causal_stage_presentation.js`
- `Dockerfile.frontend`
- `compose.yaml`
- `tests/product/test_enh_e9_estimation_submission_regression.py`
- `tests/browser_e2e/run_enh_e8_g02_causal_stage_content.py`

`frontend/causal_stage_presentation.js`はsubmission business logicのauthorityへ拡張せず、buttonのpre-ready safety stateとsubmission module bootstrap wiringに限定する。

`Dockerfile.frontend` / `compose.yaml` の変更は、G03 required static assetをcanonical runtimeへ配信するdelivery boundaryとして扱う。新しいproduct API、DB schema、backend execution semanticsを導入する理由にしてはならない。

## 5. Protected contracts / non-goals

次を変更してはならない。

- ENH-E8 G01 Project Return Navigation contract
- ENH-E8 G02 Causal/Predictive Stage Content separation semantics
- canonical Causal Navigation Stage catalog
- API route grammar
- DB / persistence schema
- backend causal estimation semantics
- Identification Result / execution lineage semantics
- hidden controlを再表示することによるworkaround
- required属性を無条件に除去してnative validation問題を隠すworkaround
- handler readiness問題をfixed sleepや`window.load`待ちだけで隠すworkaround

## 6. Historical artifact identity / stale-test handling

`tests/product/test_enh_e9_estimation_submission_regression.py` は実装時にENH-E9名で作成されている。G03では、このfilenameをhistorical implementation evidenceとして参照する。

本contractは、その名称から別enhancementのsemantic authorityを推測しない。また、後追い文書作成だけを理由にhistorical test artifactをrenameしない。

A01時点でこのtestは旧button lookup source stringと`window.load`をassertしており、current implementationに対してstaleである。Coding / Verification Agentは、obsolete exact source-string assertionを満たすためにcurrent correct implementationを旧方式へ戻してはならない。testを更新する場合はG03 semantic contractを検証するbehavior/contract assertionへ更新する。

## 7. Coding-side verification obligations

少なくとも以下を確認する。

- Estimation buttonがnative submit buttonではなく独立actionになっている。
- handler未ready期間のbuttonが`type="button"`かつdisabledである。
- `DOMContentLoaded`からsubmission module bootstrapが開始され、handler ready後にbuttonがenableされる。
- hidden Identification required controlsがinvalidでもEstimation action handlerへ到達できる。
- current hidden form valuesではなくselected Identification Resultのprefill lineageを使用する。
- prefill provenance不正時はsubmissionを停止する。
- canonical Compose frontend runtimeから`/causal_estimation_submission.js`を取得できる。
- static file permissionsがruntime readerに対して成立する。
- existing G02 Causal Stage visibility/separation regressionがgreenである。
- API/schema/backend semanticsに不要な変更がない。
- historical stale testをそのままgreenにするためのsemantic regressionを導入していない。

## 8. Candidate / evidence rule

本Gateはpost-hoc reconstructionであり、original bugfix実行時のformal Fixed Trial Candidate transactionは存在しない。

A01はformal verification前のcontract completeness amendmentであるためTrial番号を増やさない。

初回のretrospective verificationでは、A01適用済みcontractに対してverification実行時のexact repository commit SHAを記録し、そのcommitをG03 Trial01のFixed Verification Candidateとして扱う。過去時点へ遡ってcandidate identityを捏造してはならない。

## 9. Exit

implementation evidenceとself-checkを記録し、Gate PASSをCoding側から宣言しない。

Independent VerificationはA01適用済み`07_Ariadne_ENH-E8_G03_test_instruction.md`に従う。
