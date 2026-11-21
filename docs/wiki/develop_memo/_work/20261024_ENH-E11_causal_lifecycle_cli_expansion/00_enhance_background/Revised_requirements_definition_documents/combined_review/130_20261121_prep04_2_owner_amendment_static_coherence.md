# PREP-04.2 owner-amended G05 — static coherence review (2026-11-21)

**Authority:** DEC-PREP04-G05-LOCAL / combined_review/129_20261121_dec_g05_local_row_export_simplification.md. **Snapshot input:** latest pre-QA E11 branch; actual runtime tests NOT_RUN.
**Result:** CURRENT_DESIGN_PROPAGATED / G05_GUIDANCE_DRAFT / ROW_SCHEMA_OPEN / RUNTIME_VERIFICATION_OPEN / G05_NOT_FROZEN / CODING_NOT_AUTHORIZED.

## Scope and confirmed constraints

- Row-level output is optional intermediate artifact; Owner's deliberate exception supersedes PREP-02 F05 external independent prior authorization and PREP-03 OD-02 signature mechanism ONLY within G05 local export. Historical decisions 117,122,128 remain unchanged.
- FR-195, NFR-031, FR-193/194, Method Estimands/Science, existing public e11-local-study/1 and result/manifest/commit schemas, all legacy v2 Product APIs, G01 safe atomic publisher and Reader, and OD-03 writer/serializer/factory exact signature remain binding.
- Active design files updated: 10_32 Scope, 22_12 Security BD, 23_41 CLI ports, 23_42 file bundle, 30_62 local classes, withdrawn signed-policy schema draft, and G05 06/P00/P01/P02/P03/P04/07 independent instructions. The signed policy JSON Schema exists solely as a withdrawn historical draft.
- Correct semantics: executor != independent approver; non-root Linux ext4/XFS private filesystem, double explicit opt-in, local EUID=root owner, mode0700/0600, safe path/mount/ACL, Method-specific schema/row/byte bounds, no row values in aggregate results or logs.
- Class delta: no signed verification Port/Trust Anchor; LocalRunContext has root/principal/cli_row_flag; LocalPrivacyPolicyPort.authorize no policy parameter; LocalCausalUseCase constructor no policy_verifier; OD-03 RowWriter and G01 Publisher/Reader remain as adopted. This is a scoped change to planned E11 internal interfaces, NOT existing Product v2 API.

## Verification status — NOT A GATE PASS

- No actual Linux ext4/XFS execution or permissions/ACL/mount/rename readback, no real Parquet serialization tests, no G05 07 independent test or G04 canonical 999.
- P2-M01–M08 approved row schema, column dtypes/nullability/row ID, estimation target, row/byte/memory caps and serializer ABI still need authoritative positive/negative fixtures. No Method-specific scientific or numerical truth was invented.
- The repeated signed approval instructions in G05 current 06/Pxx/07 were replaced; the scientific Class/Method and unchanged tables were retained (independent table row checks are still needed in PREP-05).
- Explicit normal behavior: fail initial Privacy gate with zero RowSource iterations and exit3; no aggregate downgrade; after staging error prevent public success, do not assert no private bytes ever existed.

## Release disposition

Signed-approval signer/KeyAdmin/revocation/deployment assignments from PREP-04.2 are **no longer required** for the user-declared local CLI scope. Remaining blockers are Method-specific ApprovedRowSchema, effective OS/FS/Parquet and science validation plus normal G05 07/Gate999. Owner Contract Freeze remains separate from this documentation revision. Source/tests/uv.lock/canonical requirement docs are not touched.
