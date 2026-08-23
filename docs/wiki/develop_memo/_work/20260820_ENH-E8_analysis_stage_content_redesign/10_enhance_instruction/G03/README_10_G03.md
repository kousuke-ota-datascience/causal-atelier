# G03 — Causal Estimation Submission Regression Contract

Status: `RETROSPECTIVE_FROZEN / A01_APPLIED`

Semantic claim: ENH-E8でStage Contentsを分離したCausal Estimationにおいて、hiddenなIdentification入力のnative form validationへ依存せずEstimation actionを起動でき、選択済みIdentification Resultのexecution lineageからsubmission入力を復元して`ESTIMATION` execution batchを送信できること。さらに、submission handlerのbootstrap中もnative/shared-form submitへfallbackせず、canonical frontend runtimeからsubmission moduleが確実に配信されること。

Mode: `SINGLE_EXECUTION`  
Initial Trial: `01`  
Baseline: ENH-E8 archived state `f39f6860f83032efc08ded77f628353ecaf4797c`

## Retrospective status

G03はENH-E8完了後に実施されたbugfixの後追い証跡である。したがって、本Gateの06/07がbugfix実装前にfreezeされていたとは扱わない。

`RETROSPECTIVE_FROZEN` は、2026-08-23時点でrepositoryに存在する修正実装・回帰テストから再構成したsemantic contractを、今後の監査・regression protection用authorityとして固定したことを意味する。

Initial reconstruction後の追加bugfixにより、handler attachmentまでのinteraction raceとcanonical frontend runtimeでのstatic asset deliveryがblocking conditionであることが判明した。これを`09_ENH-E8_G03_A01_Gate_Contract_Amendment.md`で明示し、06/07をre-baselineした。

Historical evidenceには `tests/product/test_enh_e9_estimation_submission_regression.py` というENH-E9名のartifactが含まれるが、本GateではこれをENH-E8後追いbugfixの実装証跡として参照する。artifact名の不整合自体はhistorical factとして保持し、G03作成だけを理由に改名しない。

なお、このhistorical product testはA01時点では旧bootstrap implementation detail（旧button lookup / `window.load`）をassertしており、current implementationに対してstaleである。更新または代替verificationなしにG03 PASS authorityとして使用してはならない。

## Effective authority

- Gate semantic / implementation authority: re-baselined `06_Ariadne_ENH-E8_G03_implementation_instruction.md`
- Acceptance authority: re-baselined `07_Ariadne_ENH-E8_G03_test_instruction.md`
- Amendment provenance: `09_ENH-E8_G03_A01_Gate_Contract_Amendment.md`
- Formal Independent Verification: 未実施
