# PREP-04.1 G03 — Concrete strict Method Profile drafts (13)

**DRAFT, NOT_FROZEN, NOT_REGISTERED, BACKEND/SCIENCE NOT_VERIFIED.** Five schemas per Method (Config / Question / Design / Output / Inference) are in this directory. These are internal validators only; E11 public wire versions, Product v2 ABI and G01 Reader/Publisher remain unchanged. Every method requires a nonempty strict config with unknown keys rejected, explicit Question/Design and upstream hash semantic validation. Output schema describes positive artifacts; it does not replace the public result/graph schema. Inference syntax does not prove CI availability. Never infer Backend API/CI/License from a Method label.

| Method | Owner | Operation | Target family | Required config | Design role fields | Science obligation |
|---|---|---|---|---|---|---|
| P1-M08 | P01 | ESTIMATE | ATE | variance_spec_ref, treatment_coding_ref | treatment, outcome, randomization_evidence_ref, allocation_unit | DGP-001, DGP-022; NEG-001, NEG-010; REF-E01 |
| P1-M09 | P01 | ESTIMATE | 10_32 semantic target (not assigned canonical enum) | linear_model_spec_ref, contrast_spec_ref, covariance_spec_ref | treatment, outcome, adjustment_columns, identification_evidence_ref | DGP-002, DGP-003; NEG-002, NEG-008, NEG-020; REF-E01, REF-I01 |
| P1-M10 | P02 | ESTIMATE | 10_32 semantic target (not assigned canonical enum) | propensity_model_ref, weight_normalization_spec_ref, positivity_diagnostic_ref | treatment, outcome, confounders, overlap_assumption_ref | DGP-002, DGP-003; NEG-010, NEG-018; REF-E02 |
| P1-M11 | P02 | ESTIMATE | 10_32 semantic target (not assigned canonical enum) | propensity_model_ref, outcome_model_ref, crossfit_folds, variance_spec_ref | treatment, outcome, confounders, overlap_assumption_ref | DGP-002, DGP-003; NEG-010, NEG-011, NEG-012; REF-E03 |
| P1-M12 | P03 | REFUTE | 10_32 semantic target (not assigned canonical enum) | placebo_rule_ref, repetitions | base_effect_hash, design_evidence_ref, resampling_unit | DGP-022; NEG-014; REF-R01 |
| P1-M13 | P03 | REFUTE | 10_32 semantic target (not assigned canonical enum) | subset_selection_ref, subset_fraction | base_effect_hash, design_evidence_ref, sampling_unit | DGP-001, DGP-002; NEG-015; REF-R01 |
| P1-M14 | P03 | REFUTE | 10_32 semantic target (not assigned canonical enum) | perturbation_generator_ref, repetitions | base_effect_hash, design_evidence_ref, perturbation_scope_ref | DGP-002; NEG-017; REF-R01 |
| P1-M15 | P03 | REFUTE | 10_32 semantic target (not assigned canonical enum) | resampling_unit, resamples | base_effect_hash, design_evidence_ref, resampling_unit | DGP-001, DGP-002; NEG-016; REF-R01 |
| P1-M16 | P04 | SENSITIVITY | 10_32 semantic target (not assigned canonical enum) | candidate_adjustment_sets, design_check_rule_ref | base_effect_hash, graph_evidence_ref, candidate_adjustment_sets | DGP-021, DGP-002; NEG-002; REF-G01, REF-R01 |
| P1-M17 | P04 | SENSITIVITY | 10_32 semantic target (not assigned canonical enum) | clip_lower, clip_upper, diagnostic_spec_ref | base_effect_hash, propensity_evidence_ref, overlap_assumption_ref | DGP-002, DGP-023; NEG-010, NEG-018; REF-E02, REF-R01 |
| P1-M18 | P05 | DIAGNOSE | 10_32 semantic target (not assigned canonical enum) | negative_control_exposure, explicit_opt_in, null_diagnostic_spec_ref | outcome, treatment, negative_control_exposure, null_assumption_ref, adjustment_columns | DGP-019; NEG-019, NEG-026; REF-R02 |
| P1-M19 | P05 | DIAGNOSE | 10_32 semantic target (not assigned canonical enum) | negative_control_outcome, explicit_opt_in, null_diagnostic_spec_ref | outcome, treatment, negative_control_outcome, null_assumption_ref, adjustment_columns | DGP-019; NEG-019, NEG-026; REF-R02 |
| P1-M20 | P05 | DIAGNOSE | 10_32 semantic target (not assigned canonical enum) | q, ols_model_spec_ref, target_coefficient_ref, variance_kind | outcome, treatment, ols_fit_evidence_ref, degrees_of_freedom | DGP-020; NEG-020; REF-R03 |

## Unresolved independent scientific and runtime evidence
- **P1-M08**: Randomized variance method and treatment encoding require explicit scientific review. AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02; ENV-BASE. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P1-M09**: ATE versus ATT and coefficient contrast with robust covariance must be settled. AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02; ENV-BASE. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P1-M10**: ATE ATT normalization and overlap diagnostics must remain separate. AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-R05; ENV-BASE. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P1-M11**: AIPW score and crossfit and valid uncertainty not yet verified. AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02; ENV-BASE. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P1-M12**: Placebo null does not prove identification. AC-D01, AC-R01, AC-T01; ENV-BASE. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P1-M13**: Sample support and subset selection may alter target. AC-D01, AC-D03, AC-R02; ENV-BASE. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P1-M14**: Synthetic confounder perturbation not yet independently specified. AC-D01, AC-D03, AC-R02; ENV-BASE. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P1-M15**: Resampling must honor observational unit and does not authorize CI. AC-D01, AC-D03, AC-R02; ENV-BASE. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P1-M16**: Post treatment and collider adjustments must be rejected. AC-D01, AC-D02, AC-R02; ENV-BASE. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P1-M17**: Require lower strictly below upper and disclose population shift. AC-D03, AC-R05; ENV-BASE. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P1-M18**: Observed NCE conditional null is a diagnostic only. AC-D01, AC-T01, AC-T02, AC-T03, AC-R03; ENV-BASE. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P1-M19**: Observed NCO conditional null is a diagnostic only. AC-D01, AC-T01, AC-T02, AC-T03, AC-R03; ENV-BASE. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P1-M20**: Classical OLS partial R2 point RV q 1 only not HC generalization. AC-D01, AC-D03, AC-R04; ENV-BASE. Explicit point/CI status and G05 privacy policy must be independently verified.

No Method is marked READY by creation of a draft file. Pending normative backend selection/API/CI/DoD/K/R/FWER/MC-SE/independent DGP/NEG/REF make Freeze blocked until resolved. Unregistered profile returns METHOD_PROFILE_UNAVAILABLE; bad input CONFIG_INVALID or METHOD_INCOMPATIBLE; unsupported inference INFERENCE_UNAVAILABLE; missing backend CAPABILITY_UNAVAILABLE. Actual canonical status mapping requires further review.
