# S05 B05 — all 41 method metric minimums, schema amendment

Enriched e11_science_prereg_draft1.schema.json from 5 to 8 strict typed acceptance metric kinds: POINT, INTERVAL, GRAPH, TOPOLOGY, DIAGNOSTIC, IDENTIFICATION, VECTOR, STABILITY. This fills material scientific omissions: the prior schema had no explicit identification truth, time/CATE/SCM vector, or sensitivity/perturbation metric.

New e11_science_metric_minimums_draft1.json records exactly 41 method IDs with their approved scientific metric family and candidate minimum metric kinds, plus separately conditional kinds activated only if target-specific inference is approved and requested. This is a **draft typed acceptance plan**, not proof of CI availability, coverage, correct causal target, or actual scientific metrics. P3-M12 is point-only VECTOR; P3-M10/M11 require AR topology and coverage when inference is approved and requested. Identifying a graph truth must not silently equate an observational causal assumption with a statistically testable condition.

A formal local Python jsonschema Draft202012.check_schema executed on the eight-kind representation and synthetically checked positive+unknown-field negative examples for new IDENTIFICATION/VECTOR/STABILITY branches: 3 positive + 3 negative PASS. Earlier 1 multi-metric positive + 13 negative shape tests also passed before adding these three branches. These are design-time structural checks, not 41 Method confirmation or final independent scientific review.

Remaining blockers: actual independently reviewed oracle reference implementation/fixture hashes for each required family, Version/Backend fit/CI, real T2 pilot, defensible R/K/eps/tolerances/computation budget, independent reviewer and preregistration before T3. Do not invent numeric targets or use assistant's exploratory AR calculation as a science gate PASS.

DEC-S05-AR01 A requires separate statistical review of HC1/chi-square method candidate before G08 freeze; all full-real AR requirements preserved.
