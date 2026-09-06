# Test Migration Decision Log

**Status:** `OPEN`  
**Rule:** append decisions; do not silently rewrite historical rationale after execution begins

## D001 — Separate lifecycle authority from verification layer

**Decision:** `tests/` will organize active tests first by lifecycle/authority (`regression`, `enhancement`, etc.) and then by verification layer (`unit`, `contract`, `integration`, `frontend`, `browser_e2e`).

**Rationale:** current structure mixes domain/purpose and test layer at the same level, making ownership and promotion unclear.

## D002 — Regression represents current behavior, not Enhancement history

**Decision:** permanent regression filenames/directories should not retain `enh_e*` identity solely because that Enhancement first introduced the behavior.

**Rationale:** a regression suite is the current executable product contract, not a chronological archive.

## D003 — Historical Browser acceptance runners are not permanent authorities

**Decision:** `run_enh_e1a.py` will not be repaired wholesale and promoted as the canonical causal Browser regression runner.

**Rationale:** it contains a broad historical mega-journey and stale navigation/DOM assumptions. Valuable scenarios are to be distilled into current canonical journeys.

## D004 — Canonical Browser E2E remains small and journey-oriented

**Decision:** target Browser regression will converge on a small set of current critical journeys: project lifecycle, analysis navigation, causal critical journey, predictive critical journey.

**Rationale:** Browser E2E is cross-layer connectivity proof. Detailed semantic/scientific correctness belongs primarily in deterministic lower layers.

## D005 — Active ENH-E9 tests stay enhancement-specific until explicit promotion

**Decision:** current ENH-E9 G01/G02 tests are staged under `tests/enhancement/enh_e9/...`; they are not preemptively labeled permanent regression.

**Rationale:** promotion is a post-stabilization lifecycle decision.

## D006 — Migration/cutover tests require semantic extraction

**Decision:** tests whose main identity is `migration`, `cutover`, `cleanup`, `legacy shutdown`, or similar are not moved unchanged into regression.

**Rationale:** some encode durable negative/current invariants, while others only prove a historical transition. These must be split.

## D007 — Scientific benchmark remains a separate authority class

**Decision:** repeated scientific/statistical acceptance benchmarks remain outside normal regression hierarchy under `tests/benchmarks/scientific/`.

**Rationale:** their execution cost, interpretation, and statistical acceptance semantics differ from deterministic regression.

## D008 — Legacy archive remains excluded

**Decision:** `tests/legacy_archive/` remains a historical evidence area excluded from normal pytest collection.

**Rationale:** the existing isolation is already aligned with the target lifecycle model.

## D009 — Fixture migration is delayed

**Decision:** shared `conftest.py` and product fixture placement will not be mechanically moved in the first migration batch.

**Rationale:** pytest fixture scope is path-sensitive; moving fixtures before consumer/dependency analysis risks false failures unrelated to product/test semantics.

## D010 — G02 product candidate is protected from this workstream

**Decision:** Test Architecture Migration does not mutate ENH-E9 G02 Trial01 Fixed Candidate or weaken frozen `07`.

**Rationale:** the triggering Browser failure was classified as test implementation defect before product workflow verification. Test-infrastructure stabilization and product remediation must remain provenance-separated.
