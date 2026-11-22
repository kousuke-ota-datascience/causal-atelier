# ENH-E11 G01 / B04 — pinned causal-learn 0.1.4.8 FCI source preflight, BK/PAG and stdout hazards

**Date:** 2026-11-22 JST  
**Kind:** `AUTHOR_STATIC_TAGGED_SOURCE_REVIEW / INDEPENDENT_SCIENCE_NOT_RUN / PY312_BACKEND_FIT_NOT_RUN / G01_S09_NOT_RUN`.  
**Scope:** G01 / P1-M06 FCI only; this report is not an import success, numerical science PASS, independent review, S10 Freeze or S11 Authorization.

## 1. Verified primary upstream identities

- `py-why/causal-learn`, published tag **`0.1.4.8`** (release listed as 0.1.4.8; package installation/resolution still NOT_RUN).
- Tagged source `causallearn/search/ConstraintBased/FCI.py`, Git blob SHA **`869b8de01ed495ce4738d3452e0217604dc31e9b`** (read directly from GitHub on this tag).
- Tagged `causallearn/utils/PCUtils/BackgroundKnowledge.py` blob SHA **`22cb0beba328acdce194d80e8a0dfa1799c36e67`**.
- Upstream issue [py-why/causal-learn#266](https://github.com/py-why/causal-learn/issues/266): **OPEN** as checked 2026-11-22, filed 2026-06-04; describes BK forbidden-direction over-orientation from `Z o-> Y` to `Z --> Y`.

Primary source links: [FCI.py @ 0.1.4.8](https://github.com/py-why/causal-learn/blob/0.1.4.8/causallearn/search/ConstraintBased/FCI.py), [BackgroundKnowledge.py @ 0.1.4.8](https://github.com/py-why/causal-learn/blob/0.1.4.8/causallearn/utils/PCUtils/BackgroundKnowledge.py).

## 2. Source observations — no executed FCI

| Observation | Exact tagged source | Implication for G01 pre-code contract |
| --- | --- | --- |
| `fci` API declares `dataset`, `independence_test_method`, `alpha`, `depth`, `max_path_length`, `verbose`, `background_knowledge`, **`show_progress`**, **`node_names`**, `**kwargs`, returning tuple `Graph, List[Edge]` | `FCI.py` lines ~1061–1064 | Source-level feasibility of arguments is established for this tag. Actual Python3.12 import, signature, call, return graph and CI behavior **not** established. No implicit PC fallback |
| If `node_names` omitted, defaults to `X1`, `X2`, etc; GraphNode built from supplied names | `FCI.py` lines ~1118–1123 | Passing validated exact ordered Dataset names to available `node_names` argument is preferable to unverifiable string replacement; 1:1 edge endpoint/column identity must still be independently checked. No claim that `node_names` changes statistical equivalence |
| `fci_orient_bk(bk,graph)` returns immediately if `bk is None`, otherwise uses unconditional `print("Starting BK Orientation.")`, edge-line `print`, `print("Finishing BK Orientation.")` | `FCI.py` lines ~267–293, invoked within `rule0` | **Even if `verbose=False`, `show_progress=False`**, non-null BK may print process-global stdout including graph edge names. G01 CLI contract requires exactly one JSON control object for `--json` and no observational/sensitive node leaking; parameter settings alone are **not** adequate proof |
| For forbidden directed BK, `graph.remove_edge` + `graph.add_directed_edge(...)` writes both TAIL and ARROW instead of preserving the uncertain endpoint | `FCI.py` lines ~274–284 | Direct code-level match to issue #266; can over-orient PAG scientific meaning. Required/forbidden BK correctness is NOT established by structural JSON Schema; do not silently accept BK because the API accepts the argument |
| `CIT(dataset,method=independence_test_method,...)` invoked and FCI result built from data | `FCI.py` lines ~1106–1128 | Accepted spelling `fisherz/chisq/gsq` matches public docs in principle, but Python3.12 effective fit and conditional test assumptions remain B04 blocked |

## 3. G01 normative operational disposition (unchanged Owner scope)

1. G01 `Study.method.config.background_knowledge=null` is the **only currently eligible route for selected FCI**, subject also to all other normal dataset/CI/backend/preflight checks. Null BK avoids the identified `fci_orient_bk` printing branch (not a claim that the full Backend never logs). **Actual non-BK fit remains NOT_RUN.**
2. The strict Method Config and Design Schema may structurally recognize a `background_knowledge` object; **non-null** (including an object with empty required/forbidden arrays) is **not scientifically/runtime enabled** until independently verified source-fix/equivalent method and actual motifs. Return typed `BACKEND_SEMANTICS_UNVERIFIED`/Capability unavailable under the documented exit-4 routing before FCI invocation, stdout/node leakage or completed publication. Never silently downgrade to BK=null, PC, a different FCI library or silently strip forbidden edges.
3. Before declaring non-null BK supported, independently verify both (a) precise MAG→PAG endpoint preservation under #266 forbidden-edge/tiered motif, with uncertain circle **not** silently replaced by TAIL, and (b) **stdout/log containment** (including named variables) under real selected FCI and `--json`. Required-vs-forbidden contradictions and self/cycle/error negatives also remain mandatory. Do not count capturing stdout alone as correction of scientifically false PAG endpoints.
4. The exact G01 Method scope still contains the declared BK semantics and independent AC obligations. This interim fail-closed dispatch is **not a waiver of eventual G01_999 BK acceptance requirements**. If no correct supported implementation can satisfy those, report as a separate scientific/implementation blocker requiring a justified Owner decision, not a silent Method reduction.

## 4. Evidence and next mandatory execution

On the approved isolated Linux Python3.12 `ENV-BASE`: obtain actual resolver/lock/distribution/API identity, `inspect.signature`, `node_names` behavior, valid non-BK FCI tiny fitted example and invalid CI/missing/malformed/BK attempt with stdout capture, Graph endpoint reconstruction. Independent science reviewer separately derives the Graph-A MAG/PAG oracle and approves acceptance test protocol. Execute post-S11 true E11 integration and Gate07/999 on a fixed candidate SHA. Neither the tagged source, the known open issue nor this Author report establishes actual fitted API/Science PASS.

**No application source/tests/uv.lock changed by this review.**
