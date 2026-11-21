# DEC-PREP04-G05-LOCAL — Owner-directed limited security amendment (2026-11-21)

**Decision authority:** Explicit Owner statement 2026-11-21 10:25 JST. This is an exception to the prior F05/OD-02 independent-preauthorization design, NOT a claim that historical decisions never existed. Original PREP-02 117, PREP-03 122, PREP-04.2 128 are retained unchanged as dated records.
**Status:** OWNER_DIRECTED / DESIGN_AMENDMENT_PENDING_CROSS_DOCUMENT_QA / NOT_FROZEN / CODING_NOT_AUTHORIZED.

## 1. New scope and approval semantics

- The authorizing person is the **program executor**. This is **self-opt-in**, NOT an independent approver; no affiliation, organization role, external issuer, delegated principal or separate human sign-off is required.
- Individual causal effect output is an opt-in **local intermediate artifact**; data classification and exposure-minimization requirements remain binding. Intermediate does NOT imply public or non-sensitive.
- Ed25519 signatures, public/private signing keys, trust-store issuer roles, approval policy envelope, admin key deployment, rotation/revocation, signed expiry and clock freshness are NOT required in this initial local execution scope.
- Runtime target: unprivileged Linux user (non-root effective UID), local ext4 or XFS filesystem, same-FS staging/publish; private owner-controlled TrustedRoot, directory/staging mode 0700, row file mode 0600, verified UID/ACL/mount/namespace and symlink/path safety. Same-UID processes and administrators are within the trusted computing base; 0700/0600 alone do not protect from them.
- Required eligibility conjunction: Study.privacy.row_export_requested=true AND CLI --allow-row-level-export AND local executing EUID owns verified private root AND correct RESTRICTED_ROW_LEVEL output / eligible Method-specific approved ordered row schema, allowed columns, row/byte/memory bound AND same-run G01 staging sink.
- Failed or missing conjunct: privacy denial (exit3), zero RowSource.read_rows calls and zero row bytes **before initial authorization**, no silent fallback to aggregate, no JSON/Manifest/stdout/stderr/log individual values.
- Recheck local root EUID/ACL/mount/lineage before staging, seal and publish. Failure after already-authorized private staging does not justify a false claim that past private bytes never existed; do not commit partial run.

## 2. Explicit modification of previously frozen terms

| Previously approved boundary | Current disposition |
| --- | --- |
| PREP-02 F05 independent prior approval | Superseded ONLY for local G05 row intermediate output with executor opt-in and OS safety |
| PREP-03 OD-02=A signed Ed25519/admin trust | Superseded/withdrawn in current local CLI G05; signing scheme and KeyAdmin not implemented |
| F04 LocalPolicyVerifierPort.verify, TrustedPolicyAnchor, VerifiedStudyPolicyEvidence | Not part of active local row export implementation; no dummy verifier. Review only planned unimplemented E11 interfaces, do not change Product v2 |
| LocalRunContext(root,principal,cli_row_flag,policy_anchor) | Current local design: root, principal, cli_row_flag (remove policy_anchor) |
| LocalCausalUseCase constructor policy_verifier injection | Remove policy_verifier for this local CLI feature; retain other Ports and clock for non-signing purposes |
| LocalPrivacyPolicyPort.authorize(*,study,cli_row_flag,root,principal,policy,output_shape) | Change active internal E11 signature to (*,study,cli_row_flag,root,principal,output_shape) |
| e11-local-study/1 privacy.policy_ref | Preserve version and optional wire field; current unsigned mode requires null if provided; a nonnull signed policy is not an authority |
| OD-03 RowEffectsParquetWriter, Factory, DeferredRowEffectsSource, Serializer | Retain exact existing approved signatures / bounded materialization, same G01 staging/publish/Reader authority |
| FR-195, NFR-031, F03/F06/F07 and Method science | UNCHANGED: access minimization, safe artifact, JCS/hash, atomic publication, original scientific targets and all Product legacy v2 compatibility |

## 3. Independent tests and remaining blockers

- Verify single-factor opt-in negative cases, both-factor positive with actual EUID/root/ext4 or XFS, wrong EUID/owner/ACL/mount/symlink/path/namespace, row iteration zero on initial denial, correct Method row type/columns/limits, file/dir perms, mixed run/hash, no leaking rows into aggregate outputs, G01 no-clobber/Reader readback and old v2 regression.
- Method-specific ApprovedRowSchema and caps are still incomplete; cannot invent scalar/vector target or dtype, output CI semantics, identity columns or numerical limits.
- Effective Parquet dependency API, filesystem atomic-rename/fault behavior, independent science DGP/NEG/REF and quantitative thresholds remain unverified.
- No new Source/tests/uv.lock, no signed key, no Gate999, no Coding Authorization, no Contract Freeze. Future customer delivery or external data disclosure is not licensed simply because a local operator can write a file.

## 4. Status and trace

Previous design history is preserved, with this later Owner decision taking precedence **only** in the explicitly changed G05 security/authorization mechanism. Required current-state design and independent G05 instructions must be reconciled and audited before PREP-05/06. No other frozen scientific, functional or non-functional contracts are modified.
