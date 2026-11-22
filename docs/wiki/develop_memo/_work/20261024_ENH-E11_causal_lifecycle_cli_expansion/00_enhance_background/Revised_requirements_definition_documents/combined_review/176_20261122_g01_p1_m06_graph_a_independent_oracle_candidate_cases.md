# G01 P1-M06 / GRAPH-A — independent scientific oracle candidate cases and proof obligations

**Date:** 2026-11-22 JST  
**Status:** \`AUTHOR_ANALYTIC_ORACLE_DESIGN_ONLY / INDEPENDENT_REFERENCE_NOT_IMPLEMENTED / S09_NOT_RUN / SCIENCE_NOT_ACCEPTED\`.  
**Scientific authority:** Owner-adopted \`working_notes/20261116_sr04_dec04_graph_oracle_graph_a_owner_decision.md\` (GRAPH-A), current Method P1-M06 in \`10_32_scientific_method_scope.md\`, \`working_notes/20261115_sr04_scientific_fixture_catalog_draft.md\` DGP-011, DGP-021, NEG-003/021/028, REF-G02, and G01 06/P04 + 07-09/10. This record introduces **no new DGP ID, no accepted new method/threshold, no Owner target change**.

## 1. Independence is a scientific design constraint, not a repo path

The acceptance oracle is **not** the FCI Backend output, Ariadne \`GraphEvidence\`, or a graph copied from another FCI implementation. Construct analytic/graph-theoretic conditional-independence truth from a **stipulated causal DAG and explicit stochastic generating equations**. For PAG scoring, first establish latent projection to a valid observed MAG, then derive the MAG Markov-equivalence class (including permissible endpoint marks), with an independently reviewed proof and separately versioned executable oracle/fixture code.

- **Layer T1 (deterministic):** proof-derived d/m-separation relations, known forced collider arrowheads, input-to-output endpoint encoding losslessness and rejected inconsistent graph/invalid BK. Actual graph file/hash/Schema test remains implementation-dependent.
- **Layer T2 (stochastic pilot):** run FCI on *nonconfirmatory* seeds to measure graph adjacency and endpoint error under each DGP/CI-mode/n/strength combination, determine power and permissible MCSE; calibrate sample size, tests K/R and bounded compute according to the existing Owner DEC07 policy. A formal parameter is not selected merely because code runs.
- **Layer T3 (confirmatory):** freeze the proof/fixture/independent reference hash, family/outcome set, R, K, seed manifest and multiplicity/error protocol **before** drawing T3 evidence. Publish denominators, negatives and INCONCLUSIVE; no posthoc graph truth or selected-subset PASS.

FCI setting \`alpha=0.05\` is a per-CI-test significance parameter, **not by itself** a familywise graph error guarantee at 0.05. Do not equate truth of a generating DAG with statistically guaranteed finite-sample correct FCI orientation.

## 2. DGP-021 collider variant — independent analytic truth candidate (positive collider evidence)

Existing DGP-021 includes a **collider variant** \`A → K ← Y\`. Use one fixed variant, not a blend of other DGP-021 fork/mediator variants.

Let independent standard Gaussian variables \`A\`, \`Y\`, \`ε_K\` have unit variance, and put

\[
K = a A + b Y + \sigma \varepsilon_K,\qquad a\ne0,\ b\ne0,\ \sigma>0.
\]

Then the population claims can be proved without running FCI:

- \(\operatorname{Cov}(A,Y)=0\), so \(A\perp Y\) for jointly Gaussian inputs.
- \(v_K=\operatorname{Var}(K)=a^2+b^2+\sigma^2\).
- \(\operatorname{Cov}(A,Y\mid K)=0-\operatorname{Cov}(A,K)\operatorname{Cov}(K,Y)/v_K=-ab/v_K\ne0\). The corresponding conditional partial correlation is nonzero.
- Thus observed **unshielded collider** \`A-K-Y\` has \`A ⟂ Y\` marginally, but \`A\not\perp Y\mid K\`; the arrowheads **at K** are the intended compelled-collider evidence under applicable FCI faithfulness/graph assumptions.

**Do not** declare all tails at A and Y compelled by these covariance identities. The precise *full* PAG endpoint pair (including circles/tails) and eligibility for a latent-allowed MAG class require independent derivation and reviewer approval. This is an analytic CI truth case, **not yet an accepted complete PAG oracle**.

**Negative scientific tests:** triangle \`A–Y\` adjacency invented despite marginal independence (subject to finite-sample rates); collider orientation omitted systematically; \`A → K ← Y\` DAG edge arrows copied directly as a complete PAG rather than justified invariant endpoint marks; an incorrectly requested \`CI=chisq\` on continuous Gaussian input silently coerced.

## 3. DGP-021 mediator chain — noncollider counterexample

Existing DGP-021 includes a **mediator** variant \`A → M → Y\`. Consider independent mean-zero standard Gaussian \`A\`, \`ε_M\`, \`ε_Y\` and

\[
M=cA+\sigma_M\varepsilon_M,\qquad
Y=dM+\sigma_Y\varepsilon_Y,\qquad c,d\ne0,\ \sigma_M,\sigma_Y>0.
\]

Then

\[
\operatorname{Cov}(A,Y)=cd,\quad
\operatorname{Cov}(A,Y\mid M)
=\operatorname{Cov}(A,Y)-{\operatorname{Cov}(A,M)\operatorname{Cov}(M,Y)\over\operatorname{Var}(M)}
=cd-c(d\,\operatorname{Var}(M))/\operatorname{Var}(M)=0.
\]

Thus \`A\not\perp Y\` marginally while \`A\perp Y\mid M\`, unlike the collider. **Do not** require the generated \`A→M→Y\` directions as uniquely recoverable PAG arrows without an independent equivalence-class proof. A test that demands full DAG orientation here is a **false acceptance oracle**.

## 4. DGP-011 two-observed-variable latent-stress — formal observational nonidentification

The adopted catalog's DGP-011 includes latent time-varying \`H_t\` and evolving \`X_t,Y_t\`; its two-observed-variable time slice is an **uncertainty/stress case**, *not* an accepted full-PAG positive oracle (existing DEC-SR04-04 explicitly says so).

For intuition only, a separate Gaussian *single-time-slice illustration* (not a replacement for DGP-011's approved temporal generating process) is

\[
X=uH+\varepsilon_X,\quad Y=vH+\varepsilon_Y,
\]

where \`H\`, \`ε_X\`, \`ε_Y\` are mutually independent mean-zero Gaussian with positive variance. The covariance \(\operatorname{Cov}(X,Y)=uv\,\operatorname{Var}(H)\) can be reproduced by an *observationally equivalent* direct \`X→Y\` Gaussian regression with

\[
\beta={\operatorname{Cov}(X,Y)\over\operatorname{Var}(X)},\quad
Y=\beta X+\eta,\quad
\operatorname{Cov}(X,\eta)=0,
\]

and Gaussian \(\eta\) independent of \(X\). Choose the residual variance to reproduce \(\operatorname{Var}(Y)\). Therefore **bivariate observational Gaussian covariance alone does not identify latent common causation**. A two-observed-node FCI graph cannot be scored as a mandatory uniquely bidirected \`X↔Y\` latent-cause truth. Explicitly reject any such reference-generation procedure.

To obtain an actual accepted latent MAG/PAG positive target, the independent reviewer must select a **multivariate** approved-variant graph (possibly a reviewed extension of DGP-021) with explicit latent projection and documented m-separation/Markov-equivalence proof. No invented graph-PAG endpoint is a frozen expected result before that proof is accepted.

## 5. BK forbidden-direction tagged-source counterexample and proof gap

On selected \`causal-learn==0.1.4.8\` tagged \`FCI.py\` (Git blob \`869b8de01ed495ce4738d3452e0217604dc31e9b\`), \`fci_orient_bk\` handles forbidden-edge constraints with \`add_directed_edge\` instead of altering only the constrained endpoint; **an unsupported TAIL can appear**. Upstream [py-why/causal-learn#266](https://github.com/py-why/causal-learn/issues/266) describes a concrete latent \`U→Z,U→Y, Z→Q→Y\` class where \`Z o→Y\` is over-oriented to \`Z→Y\` by forbidden BK.

The scientific test must **independently derive** the observational MAG/PAG equivalence class and justify that any endpoint claimed invariant really is. Repeating the issue's expected string without independent oracle construction is **not** independent validation. For G01 until correction and independent review, \`background_knowledge≠null\` (even empty arrays) is rejected with typed \`BACKEND_SEMANTICS_UNVERIFIED\` before invoking FCI; this also prevents known process-global BK \`print\` and CLI JSON stdout contamination. A valid BK support solution must satisfy **both** endpoint orientation and stdout/log isolation; merely suppressing stdout is scientifically inadequate. This interim fail-close does not eliminate G01_999 BK positive tests.

## 6. Independent reviewer minimum deliverables before G01-S10

| Artifact | Necessary evidentiary properties | Status |
| --- | --- | --- |
| Truth equation + CI relation | specific DGP-021 collider and mediator variants with proof, true marginal/conditional independence structure, finite-support/faithfulness conditions | **author analytic candidates only** |
| Latent MAG/PAG exact oracle | independently enumerated equivalence-class MAG(s), compelled/circle endpoint matrix for a concrete multivariate latent motif; all admissibility assumptions | **NOT_DERIVED / BLOCKED** |
| Source/Fixture identity | independent reference executable source \`sha256\`, exact immutable DGP parameterization, sample generator/fixture identity \`sha256\`, original Source full SHA | **NULL / NOT_RUN** |
| G01 BK remedy method | demonstrably correct required/forbidden BK graph semantics for selected Backend/version, with no stdout leakage and independently tested valid/invalid motifs | **NOT_SELECTED / NOT_APPROVED / BLOCKED** |
| T2/T3 quantitative protocol | graph adjacency/endpoint/bias/CI-test family, scientifically defensible K/R/n/epsilon/threshold/seed/compute strategy and frozen post-pilot confirmatory plan | **CANDIDATE PROTOCOL ONLY** |
| Independent G01 S09 | reviewer identity/session separate from Author, actual source evidence and P1-M06 science/Backend semantic verdict | **NOT_RUN** |

Owner GRAPH-A principles are **already adopted**. The missing independent MAG/PAG truth, evidence-source hashes, fitted-backend validation and BK remedy are scientific/operational **blockers**, not permission to invent one, drop an Owner-adopted Method or force all 41 Method science before G01.

**No E11 product code, tests, \`uv.lock\` or official Product RD/BD/IF/DD was edited.**
