# G01 Gate-local Instruction Set — Predictive Model Backend Contract

- Enhancement: ENH-E10
- Gate: G01
- Status: `MATERIALIZED_DRAFT`
- Execution: **NOT ALLOWED until 06/07 become FROZEN**
- Dependency: ENH-E9 final PASS / accepted pre-E10 code baseline `c56a8809dea688380b113210bef12c30b50ca7f6`

## Required artifacts

- `06_Ariadne_ENH-E10_G01_implementation_instruction.md`
- `07_Ariadne_ENH-E10_G01_test_instruction.md`
- `06_G01_P00_work_package_plan.md`
- `06_G01_P01_model_capability_and_optional_dependency.md`
- `06_G01_P02_lightgbm_model_adapters.md`
- `06_G01_P03_model_artifact_load_and_provenance.md`

## Gate claim

LightGBM Binary Classification / Regressionをoptional model backendとしてregistry、artifact/load、prediction、reproducibility、provenanceまで成立させ、existing logistic/linear behaviorを保護する。

## Freeze prerequisites

Architecture Review technical decisions are complete and recorded in `40_operator_workflows/architecture_review/02_target_architecture_decision_record.md`.

Remaining prerequisites:

- Human Architecture Review / enhancement approval
- approved requirement/design delta application and snapshot
- final traceability review
- 06/07/P01-P03 consistency check
- explicit FROZEN transition


## Work Package decision

Execution Modeは `WORK_PACKAGE` を採用する。Required packagesは `P01, P02, P03`、First executable packageは `P01`。P00/Pxxはmaterialized draftとして同時作成するが、Architecture Reviewのblocking decisionを06/07/Pxxへ反映し、同一freeze batchでFROZENにするまでは実行禁止。

08はformal FAIL後のみ、09はoriginal Gate semantic contract/AC自体のHuman-approved amendment時のみ作成する。

## Authority rule

FROZEN後は06がimplementation semantic authority、07がacceptance authority、999 Gate Decisionがfinal independent decision authorityとなる。現時点のdraftをAgent executionへ直接渡してはならない。
