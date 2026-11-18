# PREP-03 / OD-02 + OD-03 — Independent row approval and Parquet Writer design candidates

**Document class:** FLOW / Security + Architecture design candidate. NOT adopted by Owner, not normative executable Pxx.  
**State:** `OD-02_OPEN / OD-03_OPEN / G05_ROW_EXPORT_BLOCKED / NOT_FROZEN`  
**Invariants already adopted:** PREP-02 F05 independent prior approval; Study request AND CLI row flag AND independently verified approval AND same-UID private TrustedRoot AND allowed columns/rows. Deny = CLI exit 3 and zero row artifact bytes before initial authorization. G01 atomic Publisher/Reader is the only publication authority; no independent row publisher.

## 1. OD-02: trust and authorization boundary

### Existing design vs. real gap

- [PREP02 F05 Trust Anchor candidate](113_20261117_prep02_f05_policy_trust_anchor_candidate.md) already proposes signed canonical policy with Ed25519 and a separate administrator-owned trusted key store.
- [DEC-PREP02-D](decisions/95_20261117_dec_prep02_four_owner_choices.md) adopts independence of a prior authorization authority, NOT the name of a signer or concrete key/rotation/revocation mechanism.
- [23_41](../23_api_interface_design/23_41_cli_scientific_ports.md) already defines `LocalPolicyVerifierPort.verify(*, policy_ref, study, root, anchor) -> VerifiedStudyPolicyEvidence` and `LocalRunContext.policy_anchor`; [30_62](../30_detailed_design/30_62_local_execution_publication.md) already makes `LocalPrivacyPolicy.authorize` a pure conjunction. Do not duplicate those APIs.
- A policy file stored under the running user's root cannot be trusted merely because its filename differs. EUID must not be able to modify the key allowlist, issuer grants, revocation state or private signing key. A user-programmable Python object/CLI flag alone is not an authorization credential.

### Alternatives

| Option | Concrete mechanism | Consequence |
|---|---|---|
| **A (recommended)** | Independent deployment-designated approver signs an immutable, run-bound policy with Ed25519; CLI verifies with administrator-owned root and current revocation snapshot | Local offline verification, no Product RBAC/DB; deployment must provision approver, keys and revocation feed |
| B | External online authorization service with mutually authenticated attestation | Better centralized revocation potential; changes offline-only execution contract and introduces availability dependency |
| C | No row export until independent authority can be deployed | Safe fail-closed fallback; G05's mandatory row-export positive case cannot PASS without explicit scope amendment |

**Recommendation A is a proposal.** The actual responsible approving principal/organization, deployment platform and trust-store provisioner remain a **required Owner decision**. Do not fabricate identities or treat this chat as a signed policy.

### Proposed exact Class/Port contract for A

| Type / Class | Target module | Signature / responsibility |
|---|---|---|
| `LocalPolicyVerifierPort` | existing design: `ariadne.capabilities.causal.ports.local_policy` | `verify(self, *, policy_ref: ContentRef, study: ValidatedStudy, root: TrustedLocalRoot, anchor: TrustedPolicyAnchor) -> VerifiedStudyPolicyEvidence`; **existing logical Port kept** |
| `Ed25519LocalPolicyVerifier` | proposed `ariadne.interfaces.cli.local_causal.policy_verifier` | `__init__(self, *, codec: StrictJcsCodec, clock: TrustedUtcClock)` and `verify(self, *, policy_ref: ContentRef, study: ValidatedStudy, root: TrustedLocalRoot, anchor: TrustedPolicyAnchor) -> VerifiedStudyPolicyEvidence` |
| `TrustedPolicyAnchor` | proposed `ariadne.interfaces.cli.local_causal.policy_trust` | immutable trusted administrative dirfd + verified issuer/key/role registry + checked revocation snapshot. Created only by OS-aware composition-root loader; arbitrary Study Path cannot construct trust |
| `VerifiedStudyPolicyEvidence` | shared Application Port contract | immutable non-secret policy/issuer/scope/study digest/column bound/row bound/validity/trust epoch; generated only after successful signature/authority validation, not from self-assertion |

**Note:** `TrustedPolicyAnchor` vs `PolicyTrustAnchor` naming in PREP02 proposal must be normalized at adoption. Port call signature is unchanged: `anchor` is trusted runtime configuration, NOT a user-supplied key or self-authored file.

**Candidate signed artifact:** One strict policy envelope at `ContentRef`, with `payload` and `signature_ed25519` as separate fields. Signature authenticates **only** RFC8785 JCS of `payload` prefixed by domain separator `ARIADNE-E11-ROW-POLICY-v1\0`; signature and arbitrary file metadata do not recursively sign themselves. The complete envelope bytes are independently SHA256-bound by `ContentRef`. Validate signature encoding and exact payload schema; public key from admin-owned registry indexed by signed issuer/key ID, never from the payload itself.

**Required payload:** version `e11-local-row-export-policy/1`, policy_id, issuer_id, key_id, signed `subject_study_approval_digest`, run_id, approved_scope=[ROW_EFFECT_PARQUET], classification, allowlisted columns in stable order, max_rows, max_output_bytes, issued_at, expires_at and revocation_epoch. Times are UTC strict. `subject_study_approval_digest = SHA256(JCS(ValidatedStudy with privacy.policy_ref=null))`; full request_hash includes the policy_ref. Record and validate **both**; never circularly sign a request containing its own approval reference.

**Issuer and role:** Administrator provisions allowed key IDs and `ROW_EFFECT_PARQUET_APPROVER` role; private signing key remains with independent issuer outside CLI, repository, output root, stdout or logs. OS trust-store directory and current revocation snapshot must be unreadable for modification by EUID, protected against symlink/ACL/mount namespace substitution. Keys revoke by ID; policies revoke by ID; expired/stale revocation snapshot fails closed. New trusted keys require out-of-band admin deployment. Signed expiry alone is NOT revocation.

**Replay and check timing:** Bind approval to exact run_id and approval-subject digest containing the run/data/estimand/Method/row intent. Reusing the policy for a different run or changed content is rejected; same-hash retries use existing immutable run only after full Publisher readback. This provides **cross-run replay resistance**, not one-time spending semantics; no unimplemented transaction ledger is assumed. Verify full authorization (including root/principal and revocation) **before any row materialization or row-file bytes**, then recheck effective trust/expiry/revocation/root before seal/publication. If authorization is revoked after authorized private staging has begun, do not publish and isolate/dispose the staging data; absolute historical zero-bytes cannot truthfully be guaranteed for a mid-run revocation.

**Failure:** invalid/missing issuer, key, signature, envelope schema, study/run/digest/scope, stale or revoked key/policy, expiry, unsafe root, disallowed columns/count, no flag or missing user request all fail closed; `PRIVACY_POLICY_UNVERIFIED` / `ROW_EXPORT_NOT_AUTHORIZED` ⇒ exit 3; no fallback to aggregate on a row-requesting run. Sensitive data/secret/issuer material must not appear in errors or logs.

## 2. OD-03: row writer ownership and exact boundary

**Accepted separation:** The existing `LocalArtifactPublisher` owns stage/validate/commit/no-replace/readback; the new Row Writer owns only **authorized, bounded row projection and Parquet serialization to StagingSink**. No Row Writer may independently publish into `runs/`, create a commit marker, implement alternate readback or confer authorization.

| Class/Type | Proposed module | Signature and contract |
|---|---|---|
| `RowEffectsParquetWriter` | `ariadne.interfaces.cli.local_causal.row_effects_parquet` | `__init__(self, *, serializer: ValidatedParquetSerializer, max_memory_bytes: int)`, `write(self, *, source: DeferredRowEffectsSource, study: ValidatedStudy, decision: PrivacyDecision, selection: ColumnSelection, sink: StagingArtifactSink) -> ArtifactDescriptor` |
| `DeferredRowEffectsSource` | shared Scientific result reader Protocol | `schema() -> ColumnSchema` and `read_rows() -> Iterable[Mapping[str, JsonValue]]`; source must not materialize or serialize rows before valid authorization |
| `ValidatedParquetSerializer` | CLI adapter-injected serializer Protocol | `encode(self, *, rows: BoundedRowBatch, schema: ApprovedRowSchema) -> bytes`; effective backend API/lock and Parquet schema pinned, no stdout/log data |
| `RowEffectsWriterFactory` | CLI composition root / same module | `create(self, *, serializer: ValidatedParquetSerializer, max_memory_bytes: int) -> RowEffectsParquetWriter`; factory has NO approval right |

**Order (candidate protocol):**
1. Receive verified Study, CLI flag, TrustedRoot/principal, `VerifiedStudyPolicyEvidence`; call unchanged `LocalPrivacyPolicy.authorize(...)` and `filter_export_columns(...)`. Unauthorized ⇒ stop before `DeferredRowEffectsSource.read_rows` or row staging.
2. Tie immutable `PrivacyDecision` and `ColumnSelection` to current run/request/study approval digest, policy digest, allowed ordered columns, privacy classification and row/byte cap. Reject a passed-in `PrivacyDecision` that lacks verifiable lineage; **a Python DTO by itself is not an independent security proof**.
3. Validate declared row schema; lazily obtain rows only after successful check. Materialize **at most** the preauthorized row cap + one sentinel row into bounded private memory to detect overflow before serializing. Reject zero-row or missing mandatory per-row effect values as typed defined profile violations; unknown columns, unsupported dtypes, duplicate IDs and non-finite effect values fail closed. Reject over-memory/bytes policy before writing. The first release does not pretend unbounded streaming is safe.
4. Encode only ordered allowlisted columns into in-memory Parquet bytes using effective pinned serializer; validate content and byte size, and recheck issuer validity/expiry/revocation/root before invoking `sink.stage_bytes(RelativeArtifactKey("row_effects.parquet"), ..., PrivacyClass.RESTRICTED_ROW_LEVEL)`. No separate `Path.open`, `DataFrame.to_parquet(untrusted_path)` or automatic aggregate downgrade.
5. Publisher `seal` verifies Parquet schema, count, SHA256, classification and policy lineage against manifest; independently repeat authorization freshness and root/OS checks before final atomic publish. Reader verifies policy metadata/classification and permitted access on readback. No secret/row values embedded in JSON status/manifest/CLI.
6. A stale/revoked approval after authorized staging ⇒ abort without publication, no completed marker and staging isolation/cleanup according to existing Publisher rules. Concurrent approvals or identical run IDs cannot bypass no-clobber.

**Physical file:** `row_effects.parquet` exists only for authorized row export, in the same authenticated run bundle, annotated as `RESTRICTED_ROW_LEVEL`. Field identities/types must be a versioned `ApprovedRowSchema`; the per-method scalar/heterogeneous-effect shape must be fixed before test Freeze. No new global Result payload version is necessary.

**Implementation ownership:** G05/P02 owns trusted Policy verifier/OS anchor integration; G05/P03 owns row Serializer/Writer and Publisher integration; G05/P04 validates E2E and no-unsafe-path; G01 continues to own common Publisher protocol, G10 owns compatibility/legal. No other Gate takes row export by implication.

## 3. Required independent negative and positive tests (NOT RUN)

| ID | Setup | Mandatory observation |
|---|---|---|
| ROW-POL-01 | Study flag only / CLI flag only / self-signed policy / key from Study | exit3, no RowSource iteration, no row artifact bytes |
| ROW-POL-02 | Admin key not readable for substitution by EUID; malicious altered allowlist/issuer/scope/subject hash | fail closed; never trust user-owned trust store |
| ROW-POL-03 | wrong run_id, replay to different request, expired policy, revoked policy/key, stale revocation feed | exit3; no new row stages |
| ROW-POL-04 | unsafe mount, ACL, namespace, root UID/EUID change before stage or seal | deny; no out-of-scope publication |
| ROW-WRITE-01 | actual authorized policy with allowed subset of columns + finite bounded rows | precise Parquet schema/order, 0600/0700, exact count, manifest/marker/readback |
| ROW-WRITE-02 | cap+1, unapproved column, invalid dtype, duplicate row identity, NaN/Infinity, excessive bytes | no row artifact staged; typed rejection |
| ROW-WRITE-03 | revocation midrun or between stage/seal/commit; crash/rename race | never committed after revocation, safe staging, no false marker |
| ROW-WRITE-04 | stdout/stderr/log/exception and old Product v2 regression | no row values/secrets or ABI regression |

**Evidence requirement:** actual OS principal, effective issuer/trust store metadata, policy body/hash (no private signing key), fixture hash, sink operations, row-creation counter, FS permissions, Reader actual result, command/execution SHA. Mock or generated signature with a test key demonstrates contract behavior only, **not deployment authorization**.

## 4. Owner decisions still required (not inferred)

1. Select `A Ed25519/admin trust store`, `B online authority` or `C disabled export`. If A: designate the **independent approving role and administrative provisioning owner** (no invented named organization).
2. Approve proposed signing payload/version/domain-separation, run binding, key revocation/rotation/maximum trust snapshot age, trustworthy time assumptions, and deployment support matrix; unknowns remain fail-closed.
3. Approve Writer module/class/factory/method signatures, row schema profile and caps; do not treat `LocalArtifactPublisher` as Row Writer.
4. After approval propagate full adopted contract to `30_62`, `23_41`, `23_42`, G05 06/P02/P03/P04/07 and G10; create strict schema and independent verification plan. No Contract Freeze until this is done.

**External technical source:** [pyca/cryptography Ed25519.verify](https://github.com/pyca/cryptography/blob/main/docs/hazmat/primitives/asymmetric/ed25519.rst) specifies that verification checks the supplied exact message bytes/signature and raises on invalid signature. It does not provide Ariadne's issuer trust, key ownership or revocation policy by itself.
