# PREP-04.1 G07 — Concrete strict Method Profile drafts (3)

**DRAFT, NOT_FROZEN, NOT_REGISTERED, BACKEND/SCIENCE NOT_VERIFIED.** Five schemas per Method (Config / Question / Design / Output / Inference) are in this directory. These are internal validators only; E11 public wire versions, Product v2 ABI and G01 Reader/Publisher remain unchanged. Every method requires a nonempty strict config with unknown keys rejected, explicit Question/Design and upstream hash semantic validation. Output schema describes positive artifacts; it does not replace the public result/graph schema. Inference syntax does not prove CI availability. Never infer Backend API/CI/License from a Method label.

| Method | Owner | Operation | Target family | Required config | Design role fields | Science obligation |
|---|---|---|---|---|---|---|
| P3-M04 | P01 | ESTIMATE | ATT | design_variant, estimator_spec_ref, cluster_covariance_spec_ref | unit_id, time_id, treatment, outcome, parallel_trends_assumption_ref | DGP-012, DGP-013; NEG-022; REF-Q01 |
| P3-M05 | P01 | ESTIMATE | 10_32 semantic target (not assigned canonical enum) | event_window_start, event_window_end, reference_event_time, cohort_estimator_spec_ref, cluster_covariance_spec_ref | unit_id, time_id, treatment, outcome, cohort_id, pretrend_assumption_ref | DGP-013; NEG-022; REF-Q01 |
| P3-M06 | P02 | ESTIMATE | 10_32 semantic target (not assigned canonical enum) | effect_components, trend_spec_ref, serial_covariance_spec_ref | time_index, outcome, intervention_time, seasonality_spec_ref, autocorrelation_evidence_ref | DGP-014; NEG-023; REF-Q02 |

## Unresolved independent scientific and runtime evidence
- **P3-M04**: 2x2 and staggered targets separate and not naive TWFE. AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q01; ENV-BASE / backend pending. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P3-M05**: Reference event time cohort and pretrend and simultaneous inference need evidence. AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q01; ENV-BASE / backend pending. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P3-M06**: ITS level slope HAC covariance cannot assume iid errors. AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q02; ENV-BASE / backend pending. Explicit point/CI status and G05 privacy policy must be independently verified.

No Method is marked READY by creation of a draft file. Pending normative backend selection/API/CI/DoD/K/R/FWER/MC-SE/independent DGP/NEG/REF make Freeze blocked until resolved. Unregistered profile returns METHOD_PROFILE_UNAVAILABLE; bad input CONFIG_INVALID or METHOD_INCOMPATIBLE; unsupported inference INFERENCE_UNAVAILABLE; missing backend CAPABILITY_UNAVAILABLE. Actual canonical status mapping requires further review.
