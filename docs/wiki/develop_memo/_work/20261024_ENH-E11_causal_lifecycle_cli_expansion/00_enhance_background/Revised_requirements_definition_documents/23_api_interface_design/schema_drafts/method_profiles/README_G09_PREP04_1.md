# PREP-04.1 G09 — Concrete strict Method Profile drafts (2)

**DRAFT, NOT_FROZEN, NOT_REGISTERED, BACKEND/SCIENCE NOT_VERIFIED.** Five schemas per Method (Config / Question / Design / Output / Inference) are in this directory. These are internal validators only; E11 public wire versions, Product v2 ABI and G01 Reader/Publisher remain unchanged. Every method requires a nonempty strict config with unknown keys rejected, explicit Question/Design and upstream hash semantic validation. Output schema describes positive artifacts; it does not replace the public result/graph schema. Inference syntax does not prove CI availability. Never infer Backend API/CI/License from a Method label.

| Method | Owner | Operation | Target family | Required config | Design role fields | Science obligation |
|---|---|---|---|---|---|---|
| P3-M12 | P01 | ESTIMATE | 10_32 semantic target (not assigned canonical enum) | weight_objective_spec_ref, preperiod_fit_spec_ref, donor_eligibility_spec_ref | treated_unit, donor_units, time_index, preperiod_end, intervention_time, no_donor_contamination_ref | DGP-017; NEG-024; REF-Q04 |
| P3-M13 | P02 | ESTIMATE | 10_32 semantic target (not assigned canonical enum) | unit_weights_spec_ref, time_weights_spec_ref, variance_spec_ref, donor_eligibility_spec_ref | treated_units, donor_units, time_index, preperiod_end, intervention_time, panel_support_ref | DGP-018; NEG-024; REF-Q05 |

## Unresolved independent scientific and runtime evidence
- **P3-M12**: SCM treated unit gap point only and donor contamination prohibited. AC-D03, AC-P01, AC-P03, AC-Q04; ENV-BASE / backend pending. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P3-M13**: SDID panel average effect unit time weights and CI need evidence. AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q05; ENV-BASE / backend pending. Explicit point/CI status and G05 privacy policy must be independently verified.

No Method is marked READY by creation of a draft file. Pending normative backend selection/API/CI/DoD/K/R/FWER/MC-SE/independent DGP/NEG/REF make Freeze blocked until resolved. Unregistered profile returns METHOD_PROFILE_UNAVAILABLE; bad input CONFIG_INVALID or METHOD_INCOMPATIBLE; unsupported inference INFERENCE_UNAVAILABLE; missing backend CAPABILITY_UNAVAILABLE. Actual canonical status mapping requires further review.
