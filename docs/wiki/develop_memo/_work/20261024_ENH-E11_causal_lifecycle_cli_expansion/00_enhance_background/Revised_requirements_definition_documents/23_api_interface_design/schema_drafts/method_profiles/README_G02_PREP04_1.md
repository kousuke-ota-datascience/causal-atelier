# PREP-04.1 G02 — Method-specific strict profile authoring drafts

**Status: DRAFT / NOT_FROZEN / REGISTRY_NOT_IMPLEMENTED / SCIENCE_NOT_EVALUATED.** These schemas are concrete JSON Schema Draft 2020-12 drafts under review. They do **not** constitute accepted backend signatures, approved statistical defaults, actual test fixtures or authorization to run code. The five per-method files are:

1. `method_config`: validated `Study.method.config`, rejects unknowns; no silent backend defaults.
2. `question_profile`: internal Question payload checked against `ContentRef` and Study target; the general Study wire is unchanged.
3. `design_profile`: declared design, roles and assumption references, with separate cross-asset Graph/Data semantic validation.
4. `output_profile`: **validator metadata for positive output**, not an alternative to canonical public `identification.json`, `e11-local-effect-result/1`, Manifest/Reader.
5. `inference_profile`: validator overlay for the existing Study.inference two-field object; CI request syntax is not proof of CI availability.

**Semantic rule:** JSON Schema cannot certify an IV assumption, nonzero first stage, lack of confounding, Graph Version, backend capability, inferential coverage or cross-file hash. The MethodRegistry/Domain validator must check these before generating ValidatedMethodRequest. If any accepted runtime profile is not registered/verified, fail-closed with typed reason. `config={}` never means backend defaults.

## G02 inventory and unresolved evidence

| Method | Pxx | Operation | Target | Mandatory Config keys | Existing negative | Open evidence |
| --- | --- | --- | --- | --- | --- | --- |
| P1-M01 | P01 | IDENTIFY | legacy target verification pending | identification_rule | NEG-001, NEG-027 | Backend/API + Science NOT_VERIFIED |
| P1-M02 | P01 | IDENTIFY | ATE | identification_rule, adjustment_columns | NEG-002, NEG-003 | Backend/API + Science NOT_VERIFIED |
| P1-M03 | P02 | IDENTIFY | ATE | identification_rule, adjustment_columns | NEG-002, NEG-027 | Backend/API + Science NOT_VERIFIED |
| P1-M04 | P02 | IDENTIFY | ATE | identification_rule, mediator_column | NEG-004 | Backend/API + Science NOT_VERIFIED |
| P1-M05 | P02 | IDENTIFY | LATE_COMPLIER | design_profile, monotonicity_direction | NEG-006, NEG-007 | Backend/API + Science NOT_VERIFIED |
| P1-M07 | P03 | ESTIMATE | ATE | estimation_rule, mediator_column, mediator_model_spec_ref, outcome_model_spec_ref | NEG-004, NEG-005 | Backend/API + Science NOT_VERIFIED |

The adopted P1-M05 target is B0 binary Z/A with no C and conditional compliers LATE **IDENTIFY only**. No DoWhy display label authorizes numerical LATE. P1-M07 is numerical restricted FD-A, not a generic frontdoor formula. P1-M01 target family requires comparison to legacy target before Freeze, not a guessed new estimand. Every independent test must fail on wrong/unknown profile and verify no result.json for IDENTIFY. This G02 authoring package intentionally contains no fake K/R/threshold values or guessed backend ABI.
