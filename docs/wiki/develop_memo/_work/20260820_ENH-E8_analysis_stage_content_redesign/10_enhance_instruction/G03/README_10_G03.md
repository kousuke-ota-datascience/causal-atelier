# G03 — Causal Estimation Submission Regression Contract

Status: `RETROSPECTIVE_FROZEN`

Semantic claim: ENH-E8でStage Contentsを分離したCausal Estimationにおいて、hiddenなIdentification入力のnative form validationへ依存せずEstimation actionを起動でき、選択済みIdentification Resultのexecution lineageからsubmission入力を復元して`ESTIMATION` execution batchを送信できること。

Mode: `SINGLE_EXECUTION`  
Initial Trial: `01`  
Baseline: ENH-E8 archived state `f39f6860f83032efc08ded77f628353ecaf4797c`

## Retrospective status

G03はENH-E8完了後に実施されたbugfixの後追い証跡である。したがって、本Gateの06/07がbugfix実装前にfreezeされていたとは扱わない。

`RETROSPECTIVE_FROZEN` は、2026-08-23時点でrepositoryに存在する修正実装・回帰テストから再構成したsemantic contractを、今後の監査・regression protection用authorityとして固定したことを意味する。

Historical evidenceには `tests/product/test_enh_e9_estimation_submission_regression.py` というENH-E9名のartifactが含まれるが、本GateではこれをENH-E8後追いbugfixの実装証跡として参照する。artifact名の不整合自体はhistorical factとして保持し、G03作成だけを理由に改名しない。
