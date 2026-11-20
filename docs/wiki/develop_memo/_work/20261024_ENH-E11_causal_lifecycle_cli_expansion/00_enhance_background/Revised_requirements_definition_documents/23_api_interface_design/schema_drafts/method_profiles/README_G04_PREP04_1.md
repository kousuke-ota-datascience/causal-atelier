# PREP-04.1 G04 — Concrete strict Method Profile drafts (8)

**DRAFT, NOT_FROZEN, NOT_REGISTERED, BACKEND/SCIENCE NOT_VERIFIED.** Five schemas per Method (Config / Question / Design / Output / Inference) are in this directory. These are internal validators only; E11 public wire versions, Product v2 ABI and G01 Reader/Publisher remain unchanged. Every method requires a nonempty strict config with unknown keys rejected, explicit Question/Design and upstream hash semantic validation. Output schema describes positive artifacts; it does not replace the public result/graph schema. Inference syntax does not prove CI availability. Never infer Backend API/CI/License from a Method label.

| Method | Owner | Operation | Target family | Required config | Design role fields | Science obligation |
|---|---|---|---|---|---|---|
| P2-M01 | P01 | ESTIMATE | CATE | model_y_ref, model_t_ref, cv_folds, final_model_ref | treatment, outcome, effect_modifiers, controls, unconfoundedness_ref | DGP-003; NEG-011, NEG-012, NEG-013; REF-E05 |
| P2-M02 | P01 | ESTIMATE | CATE | model_y_ref, model_t_ref, cv_folds, n_estimators, min_leaf_size | treatment, outcome, effect_modifiers, controls, unconfoundedness_ref | DGP-004; NEG-010, NEG-012, NEG-013; REF-E05 |
| P2-M03 | P01 | ESTIMATE | CATE | outcome_model_ref, propensity_model_ref, cv_folds | treatment, outcome, effect_modifiers, controls, unconfoundedness_ref | DGP-003, DGP-004; NEG-011, NEG-012, NEG-013; REF-E05, REF-E03 |
| P2-M04 | P01 | ESTIMATE | CATE | outcome_model_ref, propensity_model_ref, cv_folds, n_estimators, min_leaf_size | treatment, outcome, effect_modifiers, controls, unconfoundedness_ref | DGP-004; NEG-010, NEG-011, NEG-013; REF-E05, REF-E03 |
| P2-M05 | P02 | ESTIMATE | CATE | outcome_model_ref, counterfactual_prediction_rule_ref | treatment, outcome, effect_modifiers, controls, unconfoundedness_ref | DGP-002, DGP-003; NEG-010, NEG-012, NEG-013; REF-E05 |
| P2-M06 | P02 | ESTIMATE | CATE | treated_model_ref, control_model_ref | treatment, outcome, effect_modifiers, controls, unconfoundedness_ref | DGP-003, DGP-004; NEG-010, NEG-013; REF-E05 |
| P2-M07 | P02 | ESTIMATE | CATE | treated_model_ref, control_model_ref, cross_arm_weight_model_ref | treatment, outcome, effect_modifiers, controls, unconfoundedness_ref | DGP-003, DGP-004; NEG-011, NEG-012, NEG-013; REF-E05 |
| P2-M08 | P03 | ESTIMATE | CONDITIONAL_IV_STRUCTURAL_SLOPE | outcome_model_ref, treatment_model_ref, instrument_model_ref, cv_folds | treatment, outcome, instrument, effect_modifiers, controls, iv_assumptions_ref | DGP-008; NEG-009, NEG-012, NEG-013; REF-E06 |

## Unresolved independent scientific and runtime evidence
- **P2-M01**: LinearDML nuisance models and effective CI API not verified. AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03; ENV-ECONML. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P2-M02**: CausalForest support and inferred CI API not verified. AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03; ENV-ECONML. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P2-M03**: DRLearner propensity support and valid inference require probing. AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03; ENV-ECONML. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P2-M04**: ForestDRLearner forest inference and support require probing. AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03; ENV-ECONML. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P2-M05**: S learner counterfactual model cannot create CI without validation. AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03; ENV-ECONML. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P2-M06**: T learner treated control support is required. AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03; ENV-ECONML. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P2-M07**: X learner pseudo outcomes and cross arm weights must be specified. AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03; ENV-ECONML. Explicit point/CI status and G05 privacy policy must be independently verified.
- **P2-M08**: DRIV heterogeneous IV slope not non IV CATE or binary LATE. AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03; ENV-ECONML. Explicit point/CI status and G05 privacy policy must be independently verified.

No Method is marked READY by creation of a draft file. Pending normative backend selection/API/CI/DoD/K/R/FWER/MC-SE/independent DGP/NEG/REF make Freeze blocked until resolved. Unregistered profile returns METHOD_PROFILE_UNAVAILABLE; bad input CONFIG_INVALID or METHOD_INCOMPATIBLE; unsupported inference INFERENCE_UNAVAILABLE; missing backend CAPABILITY_UNAVAILABLE. Actual canonical status mapping requires further review.
