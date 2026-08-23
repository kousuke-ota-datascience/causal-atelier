# Ariadne ENH-E8 G03 Implementation Contract

- Document class: Primary Execution Contract
- Contract status: `RETROSPECTIVE_FROZEN`
- Status: `RETROSPECTIVE_FROZEN`
- Gate: `G03`
- Execution Mode: `SINGLE_EXECUTION`
- Baseline: ENH-E8 archived state `f39f6860f83032efc08ded77f628353ecaf4797c`
- Reconstruction date: `2026-08-23`

## 1. Gate claim

ENH-E8のCausal Stage separation後も、Estimation Stageのsubmission actionはIdentification Stageのhidden form controlsに阻害されず独立して起動できること。

Estimation submissionに必要なdataset / graph / analysis-spec lineageは、現在のhidden Identification form値から再構成せず、userが選択した保存済みIdentification Resultのexecution lineageをauthorityとして復元すること。

## 2. Problem reconstructed from post-ENH-E8 evidence

ENH-E8 archived stateでは、IdentificationとEstimationがpresentation上はStageごとに分離された一方、Estimation actionは共通`#inference-form`のsubmit semanticsに残存していた。

この構造では、Estimation Stageで非表示となっているIdentification側required controlがbrowser native validation上はinvalidのままとなり、Estimation button activationがEstimation submission処理へ到達しない回帰が成立し得る。

このGateは上記regressionを、Stage-specific presentationとsubmission ownershipの不整合として扱う。

## 3. Required behavior

1. Estimation actionはIdentification form validationから独立した明示的button ownershipを持つ。
2. Estimation actionのactivationは、hidden Identification controlがinvalidであってもbrowser native form validationにより遮断されない。
3. Estimation実行前に、userが選択した`IDENTIFICATION_RESULT`を一意に取得する。
4. 選択したIdentification Resultにexecution lineageが存在しなければsubmissionしない。
5. lineage復元は`/executions/{execution_id}/prefill`を使用し、prefillが`IDENTIFICATION`由来であることを確認する。
6. `dataset_version_id`、`input_graph_version_id`、`analysis_spec`はprefillをauthorityとして復元する。
7. `input_result_id`には選択済みIdentification Resultの`result_id`を使用する。
8. Estimation固有の`operation_spec`、validation override、estimator variants、revision fieldsはEstimation action側で構成する。
9. submission先は既存`/projects/{project_id}/execution-batches`、operationは`ESTIMATION`を維持する。
10. successful submission後のexecution reload、warning表示、workspace draft-state更新という既存UX semanticsを維持する。

## 4. Implementation boundary

Reconstructed implementation targets:

- `frontend/causal_estimation_submission.js`
- `frontend/causal_stage_presentation.js`
- `tests/product/test_enh_e9_estimation_submission_regression.py`
- `tests/browser_e2e/run_enh_e8_g02_causal_stage_content.py`

`frontend/causal_stage_presentation.js`はpresentation metadataをruntime submission authorityへ拡張せず、app runtime ready後にEstimation submission moduleをloadするためのbootstrap wiringに限定する。

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

## 6. Historical artifact identity

`tests/product/test_enh_e9_estimation_submission_regression.py` は実装時にENH-E9名で作成されている。G03では、このfilenameをhistorical implementation evidenceとして参照する。

本contractは、その名称から別enhancementのsemantic authorityを推測しない。また、後追い文書作成だけを理由にhistorical test artifactをrenameしない。

## 7. Coding-side verification obligations

少なくとも以下を確認する。

- Estimation buttonがnative submit buttonではなく独立actionになっている。
- hidden Identification required controlsがinvalidでもEstimation action handlerへ到達できる。
- current hidden form valuesではなくselected Identification Resultのprefill lineageを使用する。
- prefill provenance不正時はsubmissionを停止する。
- existing G02 Causal Stage visibility/separation regressionがgreenである。
- API/schema/backend semanticsに不要な変更がない。

## 8. Candidate / evidence rule

本Gateはpost-hoc reconstructionであり、original bugfix実行時のformal Fixed Trial Candidate transactionは存在しない。

したがって、初回のretrospective verificationでは、verification実行時にexact repository commit SHAを記録し、そのcommitをG03 Trial01のFixed Verification Candidateとして扱う。過去時点へ遡ってcandidate identityを捏造してはならない。

## 9. Exit

implementation evidenceとself-checkを記録し、Gate PASSをCoding側から宣言しない。

Independent Verificationは`07_Ariadne_ENH-E8_G03_test_instruction.md`に従う。
