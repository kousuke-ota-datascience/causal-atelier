# ENH-E11 Architecture Discovery

**Document class:** Planning / Operator Artifact  
**Status:** INITIAL READ-ONLY INVENTORY / COMPLETENESS REVIEW PENDING  
**Planning source SHA:** `84c5a624389b233fcb97c656f1c94d177f459c5a` for canonical requirement repair; scientific code content unchanged by that document-only commit.

## 1. Facts observed in source

| Concern | Existing source / observed fact |
|---|---|
| Scientific estimation | `src/ariadne/scientific/inference/adapter.py` selects diff/OLS/IPW/AIPW and emits Result/Diagnostics JSON |
| Estimator algorithms | `src/ariadne/causal/inference/estimators/treatment_effect.py` contains IPW/AIPW and ATE/ATT outcome methods |
| PS nuisance | `src/ariadne/causal/inference/nuisance/propensity.py` has logistic propensity fitting |
| Graph discovery | `src/ariadne/scientific/discovery/adapter.py` supports PC/GES/LiNGAM/NOTEARS; no FCI in active registry |
| Identification | `src/ariadne/scientific/identification/adapter.py` has native graph identification and cautious CPDAG/PAG handling |
| Refutation and sensitivity | `src/ariadne/scientific/refutation/adapter.py` and `sensitivity/adapter.py` cover two baseline methods each |
| CLI contract | `src/ariadne/interfaces/cli/config_schema.py` has strict local schemas for discover/identify/estimate/refute/sensitivity |
| CLI manifest | `src/ariadne/interfaces/cli/manifest.py` writes local reproducibility metadata; effective external backend version detail requires review |
| Product spec | `src/ariadne/product/domain/analysis_spec.py` currently limits baseline estimands/identification methods |
| Requirements | `docs/wiki/requirement_definition/10_requirements_definition.md` records FR-035–054 and NFR/AR statuses; §11 excludes unapproved DoWhy/EconML additions |
| E9 tests | `tests/enhancement/enh_e9/g04/scientific/` includes weight applicability, ESS/persistence and before/after balance tests |

The present summary is source-inventory evidence, **not** a fresh test run.
No code, migration, schema or server path was changed by this discovery.

## 2. Inferences requiring validation

1. Domain-native portable types and optional backend adapters can allow new
   method execution without new API/Worker/DB dependencies, provided local
   Question/Design/Graph identity is fully specified.
2. Current E9 weighting diagnostics can be reused by IPTW and only applicable
   Phase2 estimators; not all EconML methods have meaningful final IPW weights.
3. Temporal and quasi-experimental methods require additional typed designs
   rather than overloading existing binary-treatment ATE-only estimation input.
4. Versioned manifests + checksums might bridge to later Product integration,
   but they do **not** establish canonical Product DB resource lineage now.

## 3. Unknowns / required further source verification

- Full Product API/Worker/DB write/read path and migration owners; unchanged in
  E11, but future integration boundaries must be documented.
- Whether existing Product causal Question/Design version objects can be reused
  via local serialization without hidden DB dependencies.
- Which external library versions/platforms support required Phase1–3 APIs and
  their statistical inference methods.
- Exact CLI manifest schema, partial-file atomicity and privacy policy.
- Which historical Gate 999 acceptance artifacts cover each existing behavior
  and which tests must be rerun on fixed SHA.
- Whether a shared CATE/Temporal/Quasi estimation result abstraction preserves
  scientific distinctions rather than hiding method-specific assumptions.

## 4. Decision queue

Target ADR must decide: authority/type/version, optional engine compatibility,
method-specific scientific statuses, local file artifact/read-back contract,
privacy, inferential rigor, and Gate semantic boundaries. Unknowns remain
**OPEN**; no affirmative approval can be inferred from this inventory.
