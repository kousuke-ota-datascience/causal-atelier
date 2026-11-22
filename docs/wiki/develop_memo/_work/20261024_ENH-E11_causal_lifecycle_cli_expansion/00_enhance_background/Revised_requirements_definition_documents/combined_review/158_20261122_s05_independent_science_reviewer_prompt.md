# ENH-E11 S05 — Independent scientific Reviewer launch instruction (DEC-S05-02=A)

## Authority and strict bounds

This standalone instruction is for an **independently launched, fresh-session Review Agent**, not the authoring agent. The Owner approved DEC-S05-02=A on 2026-11-22. Any available Codex CLI mechanism may execute this prompt in a separate context once an authorized Linux execution session exists; a Notion Custom Agent is NOT required. No agent was launched by the present author. Do not reuse or rely on the author's suggested scientific conclusion, earlier self-assessment, or exploratory numeric results as acceptance evidence. Review alone is not human specialist signoff. Escalate questions of statistical method legitimacy to a genuinely qualified human Reviewer where agent-only evidence is inadequate.

Work read-only on Git branch `prototype/ariadne_mvp` at an **explicit frozen commit SHA** supplied with the run. Do not change `src/`, `tests/`, `pyproject.toml`, `uv.lock`, canonical product documents or Git branch refs. No Coding Authorization has been issued. Git branch changes require a separate Owner-authorized document proposal; store findings in an external immutable report until reconciled.

## Inputs; locate all without relying on preceding chat

Repository: `kousuke-ota-datascience/causal-atelier`; enhancement folder `docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/`.

Normative scientific target inventory: `00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md`; designs `30_detailed_design/30_63_causal_method_adapters.md`; independent science candidate registry `combined_review/independent_science_acceptance_registry_draft1.json`; metric families `combined_review/e11_science_metric_minimums_draft1.json`; strict prereg Schema `23_api_interface_design/schema_drafts/internal_scientific/e11_science_prereg_draft1.schema.json`; earlier AR proposal `combined_review/111_20261117_prep02_b0_b1_ar_science_method_contract.md`; Owner DEC-S05-AR01 decision `combined_review/150_20261122_dec_s05_ar01_owner_review_first.md`; new governance decisions `combined_review/156_20261122_dec_s05_02_03_owner_review_and_environment.md`.

A list of 41 planned DGP/NEG/REF/AC IDs is **NOT** the actual Reference or truth. Require concrete implementation/equations/fixtures with SHA and independently reproduced outputs. If absent, mark BLOCKED with precisely what's missing.

## Independent tasks

1. Derive each of the 41 Method's true target, identification assumptions and expected observable output independently from its adopted Method scope and suitable primary scientific references. Challenge the candidate registry for any misleading target, unsupported inference or invalid null/power metric. Ensure P1-M05 conditional binary-IV LATE, P2-M08 conditional IV *structural slope*, P3-M10 B0 LATE vs P3-M11 B1 structural coefficient, PAG/CPDAG equivalence and P3-M12 point-only SCM are not interchanged.
2. For each Method record the smallest adequate analytical/DGP/graph/reference oracle, independence from Backend-under-test, negative counterexample, exact fixture-generation parameters, unit of replication, and Method-specific estimator/CI/graph/vector acceptance criteria. Do not use plausible but invented numerical truth, replication R/K/tolerance/epsilon, or success without actual execution. Label missing as BLOCKED.
3. For G08, rederive from first principles whether `HC1 OLS Z-coefficient chi-square(1)` Anderson–Rubin inversion is a statistically defensible **asymptotic** weak-IV robust test for the agreed B0/B1 sample/iid/heteroskedastic assumptions, and which degeneracies/counterexamples break it. Invert across the entire real line, prove topology and interval endpoints, show gA=0 cases separately from point ratio, discriminate an IV-invalid arithmetic stress case from a legitimate causal DGP. Treat existing `111` HC1 formula as candidate, not adopted. Identify primary literature and whether independent human expertise is required.
4. Design T2 pilot and T3 *disjoint-seed* preregistration. Familywise 0.05 alone is not enough; propose R/K/eps/thresholds **after** evidence-based pilot. Distinguish statistical coverage from artifact schema validity. Add a defensible adjudication of whether individual CI is approved for each EconML method (do not rely solely on API attribute).
5. Report all scientific/statistical counterexamples, conflicts with `10_32` and `30_63`, alternative models, estimated independent-check compute burden, confidence of each conclusion and the required Owner decision if any.

## Output and integrity gates

Return exactly: frozen source commit; independent reviewer identity/model/tool; declaration of clean session and all sources; 41-row `method_id, estimand, DGP, negative, oracle_source_sha256, fixture_sha256, metric family, quantitative threshold status, reviewer verdict, reasons`; a separate fully derived G08 AR analysis with math and adversarial examples; B04 dependency/inference proof gaps; T2/T3 planned evidence; and an overall `PASS | FAIL | BLOCKED` verdict with explicit reasons.

**PASS forbidden** without actual independently executed/reference-verified evidence. Any unknown/invalid Method must remain `BLOCKED`; any proposal altering already Owner-approved scientific target is a **new decision request**, not a silent correction. Do not assert Reviewer independence merely because an LLM generated an answer. Do not launch coding or test agents.

## Source-of-evidence precedence

Frozen approved Method contracts and Owner decisions > primary statistical literature and derivations with reproducible independent computations > tagged Backend source and actual fitted API > secondary summaries. When a normative contract conflicts with science, describe both and raise the discrepancy; do not quietly reinterpret the adopted target or fabricate evidence.
