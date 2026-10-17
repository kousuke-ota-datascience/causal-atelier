# G01 Gate-local Instruction Set — Predictive Model Backend Contract

- Enhancement: ENH-E10
- Gate: G01
- Status: `FROZEN`
- Execution: **G01/P01 may proceed only after Agent Execution Readiness = READY**
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

## Freeze state

G01 06/07/P00/P01-P03 are FROZEN against canonical requirement/design snapshot:

`3e22d09e7e68e65aceb54d1a3a32cab697d7b480`

Completed prerequisites:

- Human Architecture Review / enhancement approval = APPROVED
- approved requirement/design delta = APPLIED
- approved snapshot = RECORDED
- final traceability review = PASS
- package routing = P01 → P02 → P03


## Work Package decision

Execution Modeは `WORK_PACKAGE` を採用する。Required packagesは `P01, P02, P03`、First executable packageは `P01`。P00/P01-P03 are FROZEN. P01 is the first executable package; P02 requires P01 PACKAGE_COMPLETE, and P03 requires P02 PACKAGE_COMPLETE. Each package still requires Agent Execution Readiness before assignment.

08はformal FAIL後のみ、09はoriginal Gate semantic contract/AC自体のHuman-approved amendment時のみ作成する。

## Authority rule

06 is the frozen Gate implementation semantic authority, 07 is the frozen acceptance authority, assigned Pxx is the package-level normative implementation authority, and 999 Gate Decision is the final independent decision authority.
