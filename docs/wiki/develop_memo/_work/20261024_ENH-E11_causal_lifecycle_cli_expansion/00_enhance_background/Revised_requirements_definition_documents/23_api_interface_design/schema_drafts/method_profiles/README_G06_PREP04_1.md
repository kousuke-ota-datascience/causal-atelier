# PREP-04.1 G06 — Concrete strict Method Profile drafts (3)

**DRAFT, NOT_FROZEN, NOT_REGISTERED, BACKEND/SCIENCE NOT_VERIFIED.** Five schemas per Method (Config / Question / Design / Output / Inference) are in this directory. These are internal validators only; E11 public wire versions, Product v2 ABI and G01 Reader/Publisher remain unchanged. Every method requires a nonempty strict config with unknown keys rejected, explicit Question/Design and upstream hash semantic validation. Output schema describes positive artifacts; it does not replace the public result/graph schema. Inference syntax does not prove CI availability. Never infer Backend API/CI/License from a Method label.

| Method | Owner | Operation | Target family | Required config | Design role fields | Science obligation |
|---|---|---|---|---|---|---|
| P3-M01 | P02 | DISCOVER | 10_32 semantic target (not assigned canonical enum) | ci_test_spec_ref, tau_min, tau_max, alpha | time_index, sampling_unit, observed_variables, temporal_ordering_ref, lag_convention_ref | DGP-009; NEG-021; REF-G03 |
| P3-M02 | P02 | DISCOVER | 10_32 semantic target (not assigned canonical enum) | ci_test_spec_ref, tau_min, tau_max, alpha, contemporaneous_rules_ref | time_index, sampling_unit, observed_variables, temporal_ordering_ref, lag_convention_ref, endpoint_convention_ref | DGP-009, DGP-010; NEG-021, NEG-028; REF-G03, REF-G02 |
| P3-M03 | P02 | DISCOVER | 10_32 semantic target (not assigned canonical enum) | ci_test_spec_ref, tau_min, tau_max, alpha, latent_assumptions_ref | time_index, sampling_unit, observed_variables, temporal_ordering_ref, lag_convention_ref, endpoint_convention_ref | DGP-011; NEG-021, NEG-028; REF-G03, REF-G02 |

## Unresolved independent scientific and runtime evidence
- **P3-M01**: PCMCI effective Tigramite API and CI test lag semantics require probe. AC-D01, AC-G01, AC-G02, AC-G03, AC-G05; ENV-TIGRAMITE. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P3-M02**: PCMCI plus contemporaneous endpoints require independent oracle. AC-D01, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06; ENV-TIGRAMITE. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P3-M03**: LPCMCI latent PAG circles cannot be coerced to DAG. AC-D01, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06; ENV-TIGRAMITE. Explicit point/CI status and G05 privacy policy must be independently verified.

No Method is marked READY by creation of a draft file. Pending normative backend selection/API/CI/DoD/K/R/FWER/MC-SE/independent DGP/NEG/REF make Freeze blocked until resolved. Unregistered profile returns METHOD_PROFILE_UNAVAILABLE; bad input CONFIG_INVALID or METHOD_INCOMPATIBLE; unsupported inference INFERENCE_UNAVAILABLE; missing backend CAPABILITY_UNAVAILABLE. Actual canonical status mapping requires further review.
