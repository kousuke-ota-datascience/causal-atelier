# PREP-04 Design Proportionality — Owner amendment propagation and scoped static review

**Date:** 2026-11-21 JST. **Owner instruction:** simplify ancillary implementation and operational requirements even when this narrowly reopens previous design Freeze.
**Decision authority:** combined_review/131_20261121_dec_prep04_design_proportionality_owner_simplification.md; previous signed individual-row approval correction in combined_review/129.
**State:** DESIGN_AMENDMENT_PROPAGATED / SELECTED_STATIC_CHECKS_COMPLETE / REPOSITORY_WIDE_INDEPENDENT_QA_NOT_RUN / BACKEND_SCIENCE_NOT_RUN / GATE_NOT_FROZEN / CODING_NOT_AUTHORIZED.

## 1. Scope and actual active-document edits

| SIM | Revised current-state artifacts | Verified disposition |
| --- | --- | --- |
| SIM-01 | 22_12 Security BD, 23_41 CLI IF, 23_42 Artifact IF, 30_60 CLI Class, 30_62 Local UseCase/Publisher/Privacy, G01 06/P01/P02/P03/P04/P05/07, G05 06/P00–P04/07, G10 06/P00–P05/07 | Removed as mandatory: separate ACL/xattr digest, mount-ID/namespace visibility proof, CI/container classification. Retained nonroot owner/mode 0700/0600, ext4/XFS same-FS, safe dirfd/path/symlink, G01 atomic publish and Reader. Real OS positive/negative tests still required |
| SIM-02 | G01 06/P01/P02/07, shared decision 131 | Removed independent ECMAScript runtime and Python↔JavaScript parity *execution* as Gate blocker. Retained RFC8785 canonical algorithm, versioned bytes and independently specified RFC expected/golden vectors. Scientific/reference oracle untouched |
| SIM-03 | 22_13 Deployment, 23_41 CLI Interface, G10 06/P00–P05/07 | ENV-COMBINED all extras no longer mandatory current Gate/CI; not supported or verified until separately tested. Four independent BASE/DOWHY/ECONML/TIGRAMITE profiles and Method-specific actual ABI/science tests remain |
| SIM-04 | 22_13 Deployment, 22_16 Test Architecture, 23_41, 23_42, 30_62, G10 06/P00–P05/07, active `e11_local_manifest_v1.schema.json` | Deleted draft Schema `runtime.sbom_ref` and `review.legal_delivery_status`. Internal scientific runs do not require auto-SBOM or customer recipient/license authorization objects. Existing runtime distribution/lock/source metadata and external manual legal review before actual customer delivery preserved |

Historical PREP-02/03 frozen decision files (e.g. 104–117, DEC08) were not rewritten. Only this explicit Owner amendment changes the current initial CLI design requirements. Existing Product/canonical requirement docs were not promoted/changed.

## 2. Static observations and tests NOT performed

- Current active Manifest JSON Schema was parsed as an object before edits, required Review legal field removed from `review.required`, and `sbom_ref` removed from `runtime.properties`. File is serialized as valid JSON in current GitHub tree. Its scientific evidence and runtime distribution fields remain required.
- G01 current 06/P01/P02/07 no longer requires a JavaScript runtime. Actual independently sourced RFC8785 golden vector generation and tests remain NOT_RUN.
- G05 current 06/P00-P04/07 maintains double opt-in and denied-before-read_row safety. Method-specific ApprovedRowSchema remains unavailable/untested. Actual local ext4/XFS ownership, 0700/0600, symlink/no-clobber/readback and Parquet API validation are NOT_RUN.
- G10 current 06/P00-P05/07 states ENV-COMBINED not mandatory and no internal SBOM/recipient approval. Actual 4 profile fresh venv checks, lock compatibility and all independent 41-Method science reference tests are NOT_RUN.
- G01 legacy Policy Anchor/12-port leftovers in current 06/P05 were corrected to 11 injected Ports and no signature verifier. The Owner local export change is not an existing Product v2 API mutation.
- This was an **in-situ targeted static review of named revised documents and specific Gate instructions**, not an automated repository-wide exhaustive content scan, independent external QA or execution of tests.

## 3. Constraints explicitly NOT diluted

FR-186–194, FR-196–203, NFR-029–036 as formal higher-level obligations; AR-028–044 including scientific target/identification/IV AR-set shapes/negative state and independent validation; Owner-adopted 41 Method ID/estimand/method-specific inference limits; DEC07 quantitative plans; Study/Effect/Graph/Manifest v1 wire versions and RFC8785; four separate SHA domains; G01 F03 no-clobber/Reader and existing Product v2 compatibility; 68 Scope R/Q/N/D. `FR-195/NFR-031` still constrain row privacy, while signature/key and extensive FS attestation are removed.

F03 atomic no-clobber/durability protocol, F06 JCS algorithm itself, scientific Method Profile count and core Application/Scientific Port separations were **considered but not deleted** because no demonstrated semantically equivalent simpler implementation has yet been established. A user instruction to remove overengineering is not authority to fabricate equivalent safety.

## 4. Next conditions

Before Contract Freeze: independent PREP-05 QA of 10/22/23/30 ↔ 06/Pxx/07 and current Source ABI; Method-specific row/outputs, DGP/NEG/REF/CI/quant thresholds, effective Backend and actual Linux/Parquet acceptance. If a remaining mandatory acceptance explicitly requires removed SIM-01/02/03/04 machinery, raise it as a documented contradiction rather than quietly reinstate the deleted obligations.

**No Source, test code, pyproject/uv.lock, Product Web/API/DB/Worker or original canonical docs changed. No implementation/independent test/Gate999/Frozen/Coding Authorization claimed.**
