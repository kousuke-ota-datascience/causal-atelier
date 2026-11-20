# PREP-04.1 G08 — Concrete strict Method Profile drafts (5)

**DRAFT, NOT_FROZEN, NOT_REGISTERED, BACKEND/SCIENCE NOT_VERIFIED.** Five schemas per Method (Config / Question / Design / Output / Inference) are in this directory. These are internal validators only; E11 public wire versions, Product v2 ABI and G01 Reader/Publisher remain unchanged. Every method requires a nonempty strict config with unknown keys rejected, explicit Question/Design and upstream hash semantic validation. Output schema describes positive artifacts; it does not replace the public result/graph schema. Inference syntax does not prove CI availability. Never infer Backend API/CI/License from a Method label.

| Method | Owner | Operation | Target family | Required config | Design role fields | Science obligation |
|---|---|---|---|---|---|---|
| P3-M07 | P01 | ESTIMATE | 10_32 semantic target (not assigned canonical enum) | bandwidth, polynomial_order, kernel_spec_ref, cutoff | running_variable, outcome, treatment, cutoff, continuity_assumption_ref, density_check_ref | DGP-015; NEG-023; REF-Q03 |
| P3-M08 | P01 | ESTIMATE | 10_32 semantic target (not assigned canonical enum) | bandwidth, polynomial_order, kernel_spec_ref, cutoff, first_stage_diagnostic_ref | running_variable, outcome, treatment, cutoff, local_iv_assumptions_ref, first_stage_evidence_ref | DGP-016; NEG-006, NEG-023; REF-Q03, REF-I03 |
| P3-M09 | P02 | ESTIMATE | LATE_COMPLIER | design_profile, first_stage_diagnostic_ref, variance_spec_ref | instrument, treatment, outcome, instrument_binary, treatment_binary, adjustment_columns, iv_assumptions_ref | DGP-006; NEG-006, NEG-007; REF-I03, REF-E07 |
| P3-M10 | P03 | ESTIMATE | LATE_COMPLIER | design_profile, first_stage_diagnostic_ref, ar_statistic_spec_ref, covariance_spec_ref | instrument, treatment, outcome, instrument_binary, treatment_binary, adjustment_columns, iv_assumptions_ref | DGP-006, DGP-024; NEG-006, NEG-025; REF-E07, REF-U01 |
| P3-M11 | P03 | ESTIMATE | LINEAR_IV_STRUCTURAL_COEFFICIENT | design_profile, first_stage_diagnostic_ref, ar_statistic_spec_ref, covariance_spec_ref | instrument, treatment, outcome, instrument_binary, treatment_binary, controls, iv_assumptions_ref | DGP-007, DGP-024; NEG-008, NEG-025; REF-E08, REF-U01 |

## Unresolved independent scientific and runtime evidence
- **P3-M07**: Sharp RD manipulation and bias correction inference need probe. AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q03; ENV-BASE / backend pending. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P3-M08**: Fuzzy RD weak first stage and local IV uncertainty need evidence. AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q03; ENV-BASE / backend pending. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P3-M09**: Wald denominator zero or weak invalidates ordinary finite CI. AC-D03, AC-P01, AC-P03, AC-P05, AC-D07; ENV-BASE / backend pending. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P3-M10**: HC1 chi squared AR full real authority history to reconcile. AC-D03, AC-P01, AC-P03, AC-P05, AC-A01, AC-A02, AC-A03, AC-A04, AC-A05, AC-I01, AC-I02; ENV-BASE / backend pending. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P3-M11**: B1 adjusted structural slope not complier LATE and AR inversion needs oracle. AC-D03, AC-P01, AC-P03, AC-P05, AC-A01, AC-A02, AC-A03, AC-A04, AC-A05, AC-I01, AC-I02; ENV-BASE / backend pending. Explicit point/CI status and G05 privacy policy must be independently verified.

No Method is marked READY by creation of a draft file. Pending normative backend selection/API/CI/DoD/K/R/FWER/MC-SE/independent DGP/NEG/REF make Freeze blocked until resolved. Unregistered profile returns METHOD_PROFILE_UNAVAILABLE; bad input CONFIG_INVALID or METHOD_INCOMPATIBLE; unsupported inference INFERENCE_UNAVAILABLE; missing backend CAPABILITY_UNAVAILABLE. Actual canonical status mapping requires further review.
