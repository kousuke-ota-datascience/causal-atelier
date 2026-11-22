# B03 additional strictly typed scientific artifact constraints — 2026-11-22

**Status:** static JSON Schema cross-field patches only, **not** real output readback or independent scientific PASS.

Five existing unpublished internal draft artifacts were reconciled for previously permissive cross-field combinations. The changes maintain original schema ID/draft1 path and fields (no public wire migration):

- CATE: P2-M08 may be tagged only `CONDITIONAL_IV_STRUCTURAL_SLOPE`, P2-M01..07 only `NON_IV_CATE`; AVAILABLE requires a typed CI reference, other statuses require null.
- Event Study: AVAILABLE requires interval reference, unavailable/not-requested/failed cannot invent one.
- SCM: pre/post periods are both present. This is insufficient to prove sorted time order, donor validity or `gap=observed-counterfactual` under a reviewed numerical tolerance.
- Identification Proof: P1-M05 fixed `LATE_COMPLIER`; P1-M01..04 fixed ATE; conditional identified requires nonempty expression and assumptions; other states require null expression and explanatory reason. This enforces *typed* declaration, not validity of IV exclusion/independence/monotonicity.
- Diagnostics: method-operation ID mapping REFUTE(M12..15), SENSITIVITY(M16..17), DIAGNOSE(M18..20); COMPUTED requires at least one statistic, other states require a reason.

For every candidate update, Schema still has `additionalProperties:false`; other fields retained exactly. The companion JSON lists nine explicit positive/negative **design cases**. These patches have **not** been independently validated against all actual scientific fixture bytes, Manifest and Result. A checked-out source+all-schema strict validator and independent cross-file semantics are required before B03 is marked complete. No new Owner scientific Method scope change.
