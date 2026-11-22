# S05 — Method Profile factoring progress and remaining blockers (2026-11-22)

**Input:** 63256f1f019cda27c1243d1f06974b8ad963e5f0. **Status:** `OUTPUT_40_STRUCTURAL_FACTOR_CANDIDATE_AUTHORED / CONFIG_QUESTION_DESIGN_INFERENCE_160_NOT_YET_FACTORED / SCHEMA_PARITY_NOT_RUN / BACKEND_REFERENCE_NOT_RUN / S05_BLOCKED_FOR_FREEZE / CODING_NOT_AUTHORIZED`.

Reviewed the 40 `*_output_profile_v1.schema.json` draft bodies, grouped by Operation: IDENTIFY five (P1-M01–05), ESTIMATE twenty-three (P1-M07–11, P2-M01–08, P3-M04–13), REFUTE four (P1-M12–15), SENSITIVITY two (P1-M16–17), DIAGNOSE three (P1-M18–20), DISCOVER three (P3-M01–03), total 40. Their JSON shape admits a strict common six-field structure with 40 Method-specific const branches; a compiled candidate catalog and strict JSON Schema were added under schema_drafts/method_profiles. No original draft was removed, no active Registry modified.

**Conservatism:** this is a semantic/structural draft review, **not positive+negative schema-validator parity or 41-Method independently executed Science evidence**. Config/Question/Design/Inference (160 Method-specific drafts), G01 P1-M06 baseline, actual DoWhy/EconML/Tigramite/optional backend and Python uv.lock, real runtime and Reference tests remain outstanding. Until these are proven, METHOD_PROFILE_UNAVAILABLE and Gate BLOCKED for unsupported or unverified configurations.
