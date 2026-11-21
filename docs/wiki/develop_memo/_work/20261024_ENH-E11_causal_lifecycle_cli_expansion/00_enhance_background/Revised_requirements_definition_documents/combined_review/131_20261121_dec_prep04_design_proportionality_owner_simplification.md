# DEC-PREP04-SIMPLIFY — Scientific-first scope and proportionality amendment (2026-11-21)

**Owner directive:** 2026-11-21 JST, reopen earlier common design Freeze if needed and remove simplifiable non-core conditions/functions. This is a bounded explicit change authorization to design, not Coding Authorization, scientific Method re-selection, or Gate Freeze.
**Authority order:** this decision supersedes older PREP-02/03 design records only for the listed mechanisms; historical records stay intact. G05 signed authorization was already removed by amendment 129.
**Status:** OWNER_DIRECTION_ACCEPTED / MECHANICAL_DESIGN_AMENDMENT / INDEPENDENT_AUDIT_NOT_RUN / CODING_NOT_AUTHORIZED.

## 1. What E11 is for

Primary deliverable: scientifically valid Causal Discovery, Identification, Effect Estimation, Refutation/Sensitivity, Heterogeneous Effects, Temporal and Quasi-experimental Methods, plus Method-specific independent tests and a reproducible local CLI. Governance of the row intermediate output is ancillary. NFR-035/AR-044, FR-186–194, FR-196–200, FR-202 and all signed-off estimands/inference limitations are NOT simplified.

## 2. Approved eliminations of excessive *mechanisms*

| ID | Remove as **mandatory implementation/release activity** | Keep as necessary invariant |
| --- | --- | --- |
| SIM-01 / F05 | Dedicated POSIX ACL/xattr evidence digest, ACL-reader capability detection, statx mount-ID tracking for security proof, per-transition namespace/mount visibility proof, CI/container environment classification and blanket fail solely because such proof is unavailable | Non-root Linux EUID owns root, mode 0700 directories and 0600 row artifacts, verified local ext4/XFS and same filesystem for atomic rename, secure dirfd/O_NOFOLLOW/symlink/path containment, no row leakage; deny actual unsafe ownership/mode, wrong FS or path. No guarantee against same UID, root/admin or separately remounted/exposed FS |
| SIM-02 / F06 | Independent ECMAScript/JavaScript runtime and cross-language byte-parity execution as a mandatory G01/G10 test dependency for a Python-only local CLI | Strict RFC8785 JCS semantics and fixed golden expected bytes, raw SHA256/semantic digest projections, lossless JSON/Graph/AR, versioned wire, duplicate-key/nonfinite/unknown object rejection. Independent *expected vectors* still required; self-derived fixture not acceptable |
| SIM-03 / DEC08 ENV | ENV-COMBINED DoWhy+EconML+Tigramite fresh environment and full all-installed backend test as mandatory Gate PASS/deployment profile | ENV-BASE and independent ENV-DOWHY, ENV-ECONML, ENV-TIGRAMITE plus only Method actually used; universal lock resolution and effective Method-by-Method API/inference probes. No claim of validated simultaneous combined environment until actually tested |
| SIM-04 / NFR-034 | An in-CLI customer/recipient/license approval service, runtime per-recipient release state, automatic SBOM production as a blocker of *internal scientific runs* | Manual Owner/legal assessment **before actual external customer delivery** of covered dependencies. Retain effective package metadata/version and lock provenance for NFR-029/033. An unreviewed customer deliverable is NOT approved |

## 3. Explicitly NOT removed

- F03 same-FS no-clobber/atomic publish, safe staging/commit marker, verifying Reader and no overwrite remain: no equally safe simpler alternative with proven same-run retry/partial state semantics is presently established. Specific filesystem and failure proofs cannot be substituted with guesses.
- F06 canonical binary identity, content hashes, schema/version/operation-specific validators and no false-completed Marker remain. Multiple hash domains distinguish logically different objects, not duplicated steps.
- Port/Application vs Scientific Kernel and legacy Product v2 separation: no evidence yet that deleting particular Port preserves type boundaries and old callers; no speculative collapse.
- NFR-032 optional-backend isolation, NFR-033 verified environments, NFR-035/AR-044 independent DGP/negative/known truth, method-specific K/R/FWER, all 41 Method targets and 68 Scope dispositions, license constraint on customer delivery, and FR-195/NFR-031 actual privacy and data minimization all remain.
- Current 40 Method's 5 schema groups encode independent scientific boundaries; consolidate mechanically only if fully equivalent, not by deleting inference/identification/eligibility fields.

## 4. Operational implementation boundaries

SIM-01 security decision accepts the declared threat model: a single ordinary user on a local ext4/XFS filesystem. Linux owner-only mode bits and secure FD-backed traversal are necessary. It does not assert protection from privileged OS processes or any actor who can read files as the same UID. A mount actually reported as NFS, overlay, unsupported, or different st_dev is rejected; *extra provenance/namespace proof* is unnecessary. Method-specific row/column/byte bounds and safe logs remain. Existing G05 double opt-in remains.
SIM-02 does not replace the adopted JCS wire version or algorithm; only removes the extra cross-language execution fixture obligation. Fixed independent expected vectors remain necessary for verifiability. Do not silently rewrite public Version IDs.
SIM-03 controls acceptance scope, not the legal or dependency compatibility of a combined environment someone may construct later; explicitly label all-extras usage NOT_VERIFIED and block claiming it supported without tests.
SIM-04 is not permission to distribute GPL code unreviewed. Releasing a package to a customer is a separate decision and must be blocked absent approval. Local analysis results are not customer distribution merely because produced.

## 5. Verification/status

Audit the present 10/22/23/30 design and current G01/G05/G10 06/Pxx/07 instructions for contradictory old constraints. Change only these four mechanisms, not science. Run the remaining real Linux/private-path and JCS golden tests, Method-specific backend and reference tests after separate Coding Authorization. Runtime tests NOT_RUN; G01/G05/G10 NOT_FROZEN; no Source/tests/uv.lock or canonical docs changed.
