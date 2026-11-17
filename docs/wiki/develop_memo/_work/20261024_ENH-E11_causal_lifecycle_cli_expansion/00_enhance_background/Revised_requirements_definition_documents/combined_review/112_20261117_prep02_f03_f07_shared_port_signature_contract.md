# PREP-02 F03–F07 — Cross-Port / DTO / schema mechanical contract v1 review candidate

- Date: 2026-11-17 JST
- Kind: FLOW / draft cross-component Interface contract; **not** production source, Architecture Freeze or authorization to code
- Authority: DEC-PREP02 A/A/A + DEC-PREP02-D A/A/A/A, existing IF 23_41/42 and DD 30_61/62, Product Ports source snapshot
- **2026-11-17 Design baseline update:** [117](117_20261117_prep02_common_contract_baseline_freeze.md)により、**§1・§2の論理Port署名とcross-Port不変条件を共通設計baselineとして採用**した。実装Python module ABI / DTO constructor / Method固有の型はGate 06で完成させ、実行試験はGate 07とする。Reviewer証跡の追加提出は工程阻害条件にしない。`COMMON_LOGICAL_PORT_CONTRACT_FROZEN / MODULE_ABI_PENDING / CODING_NOT_AUTHORIZED`。旧候補文言は採用前の注釈。

## 1. One authority per boundary

| Owner Port / DTO | Input authority | Output authority | Forbidden shortcut |
|---|---|---|---|
| `LocalConfigDecoder` | strict explicit version + safe parse + typed E11 fields | `ValidatedStudy` | Product `causal-analysis-spec/2` fallback / YAML Python object / duplicate key |
| `ContentReferencePort` | `ContentRef` + verified dirfd `TrustedLocalRoot` | `VerifiedContent` (opened-fd actual digest, immutable bytes) | lexical path-only validation / hash of path string |
| `MethodCapabilityPort` | Method registry ID, explicit Backend/Profile/Estimand/Inference | `BackendCapabilityRecord` or typed unavailable | silent backend fallback / deferred wrong result target |
| `IdentificationPort` | `ValidatedIdentificationRequest` | `IdentificationOutcome` | Product status casting / proof without hash/estimand |
| `EstimatorPort` | `ValidatedEstimatorRequest` plus private `StagingArtifactSink` | `EffectOutcome` | final run path or untyped external library object |
| `LocalPolicyVerifierPort` | external `policy_ref`, authenticated issuer Trust Anchor, VerifiedStudy scope | `VerifiedStudyPolicyEvidence` or exit3 typed denial | Study boolean or PolicyRef string accepted as permission |
| `LocalPrivacyPolicyPort` | Study intent + CLI flag + TrustedRoot + VerifiedPolicy + columns/rows | `PrivacyDecision` | row bytes staged before approval or silent aggregate fallback |
| `LocalPublicationPort` | `ValidatedStagedBundle` + `TrustedLocalRoot` | `CommittedLocalRun` (verified) | Product ArtifactStore, ordinary rename, process lock, success after post-rename fsync failure |
| `LocalManifestReaderPort` | safe run ID + TrustedRoot | `VerifiedLocalRun` after Marker→Manifest→all artifacts | mark a corrupt/partially published directory COMMITTED |

## 2. Exact candidate Python Protocol signatures — reconcile before freezing

~~~python
class LocalConfigDecoder(Protocol):
    def decode(self, raw: bytes, *, declared_format: Literal["yaml", "json"]) -> ValidatedStudy: ...

class ContentReferencePort(Protocol):
    def verify(self, ref: ContentRef, *, root: TrustedLocalRoot) -> VerifiedContent: ...

class MethodCapabilityPort(Protocol):
    def resolve(self, request: ValidatedCapabilityRequest) -> BackendCapabilityRecord: ...

class IdentificationPort(Protocol):
    def identify(self, request: ValidatedIdentificationRequest) -> IdentificationOutcome: ...

class EstimatorPort(Protocol):
    def estimate(self, request: ValidatedEstimatorRequest, *, sink: StagingArtifactSink) -> EffectOutcome: ...

class DiagnosticPort(Protocol):
    def run(self, request: ValidatedDiagnosticRequest, *, sink: StagingArtifactSink) -> DiagnosticOutcome: ...

class LocalPolicyVerifierPort(Protocol):
    def verify(self, *, policy_ref: ContentRef, study: ValidatedStudy,
               root: TrustedLocalRoot, anchor: PolicyTrustAnchor) -> VerifiedStudyPolicyEvidence: ...

class LocalPrivacyPolicyPort(Protocol):
    def authorize(self, *, study: ValidatedStudy, cli_row_flag: bool,
                  root: TrustedLocalRoot, policy: VerifiedStudyPolicyEvidence | None,
                  output_shape: PlannedOutputShape) -> PrivacyDecision: ...

class LocalPublicationPort(Protocol):
    def begin(self, *, run_id: RunId, request_hash: Sha256Digest,
              root: TrustedLocalRoot) -> StagingArtifactSink: ...
    def seal(self, *, sink: StagingArtifactSink, manifest: LocalRunManifest,
             privacy: PrivacyDecision) -> ValidatedStagedBundle: ...
    def publish(self, *, bundle: ValidatedStagedBundle,
                root: TrustedLocalRoot) -> CommittedLocalRun: ...

class LocalManifestReaderPort(Protocol):
    def verify(self, *, root: TrustedLocalRoot, run_id: RunId) -> VerifiedLocalRun: ...
~~~

**Version authority**: `LocalStudySpec` is decoded into `ValidatedStudy` only by an internal validation factory. `Validated*Request` constructors must reject forgery or revalidate every invariant. The type hints alone are not security proofs. No E11 Domain or Port module imports optional scientific engines or Product scientific statuses.

## 3. State-machine, idempotency and publication error semantics

`RAW→VALIDATED→ELIGIBLE→EXECUTED→SEALED→PUBLISHED→READBACK_VERIFIED`. A negative scientific outcome can pass the technical stages if correctly represented in Result/Manifest. No final directory write from an Estimator.

- Only a `READBACK_VERIFIED` value may map to `technical_status=COMPLETED`. `renameat2(RENAME_NOREPLACE)` success before parent directory fsync/readback **does not** imply a completed result.
- If destination already exists, verify marker+manifest+hash+privacy+same request hash before returning an idempotent reuse. Same request digest but corrupt, missing marker or wrong content = **failure**, not replacement or recovery by delete.
- On post-rename error, emit `PUBLICATION_INDETERMINATE` and retain run bytes for independent verification; do not remove, overwrite or mark complete.
- `ValidatedStagedBundle` contains frozen Artifact descriptor list and marker/manifest bytes; `StagingArtifactSink` is **not** allowed to publish and cannot be reused after seal/abort. `TrustedLocalRoot` carries descriptor-scoped owner/mount/ACL proof, not a raw `Path`.

## 4. Error envelope and context-dependent exit codes

Candidate `E11Error`: `{error_version:"e11-local-error/1", code: ErrorCode, phase: ErrorPhase, public_message: SanitizedString, evidence_ref: ContentRef|null}`. Private details/raw bytes are excluded. **Error payload version is an additional internal type**, not a replacement for five Owner-adopted *output payload versions*.

| Error phase | Example codes | CLI exit | Must not claim |
|---|---|---:|---|
| `INPUT_SCHEMA` | VERSION_UNSUPPORTED, SCHEMA_INVALID, UNKNOWN_METHOD_ID | 2 | Sci FAIL or Product v2 fallback |
| `INPUT_SECURITY` | INPUT_HASH_MISMATCH, PATH_CONFINEMENT_FAILED, PRIVACY_POLICY_UNVERIFIED, ROW_EXPORT_NOT_AUTHORIZED, ROOT_OWNER_MISMATCH, MOUNT_UNTRUSTED | **3** | successful downgraded individual export |
| `ENGINE` | BACKEND_API_MISMATCH, SCIENTIFIC_EXECUTION_FAILED, METHOD_CAPABILITY_UNAVAILABLE | 4 | Science PASS |
| `PUBLICATION` | RUN_ID_CONFLICT, ATOMIC_PUBLISH_UNAVAILABLE, STAGING_DURABILITY_FAILED, PUBLICATION_INDETERMINATE, NOT_COMMITTED, MANIFEST_HASH_MISMATCH | 5 | already committed/exactly once |
| `SCIENTIFIC_RESULT` | NOT_IDENTIFIED, INFERENCE_UNSUPPORTED, AR_SCIENCE_INCONSISTENT | 0 **only if** completely published valid negative result | successful identification or confirmatory PASS |

**Context-sensitive key:** `SCHEMA_INVALID`/version failure in *untrusted CLI input* belongs to exit2; the **same malformed wire in a persisted run readback** belongs to exit5 (PUBLICATION). A reason-code-only global mapping is insufficient; `phase` must be preserved. Scientific negative with no valid published run is **not** an automatic exit0.

## 5. Cross-schema invariants and tests to freeze

1. ContentRef is exactly `identity/relative_key/sha256/media_type/schema_version`, plus verified source scope; no `path/id` alias.
2. `run_id`, `request_hash`, `schema_dispatch`, `estimand_kind`, `method_id`, `codec_version`, PrivacyDecision and all upstream digests agree between Study→Result→Status→Manifest→Marker; no string-only replacements.
3. `request_hash = SHA256(JCS(validated typed Study JSON))`; Product `hash_mapping(default=str)` not used. Manifest includes draft `canonical_codec_version`. Marker SHA256 over actual persisted manifest bytes, not serialized metadata concept.
4. Inference `AVAILABLE+AR_CONFIDENCE_SET+EMPTY` with 0 components is well-formed generic wire; `FAILED` has no set and typed reason. B0/B1 Method-specific independent Science Oracle checks appropriateness.
5. Reader rejects artifact duplicated keys, invalid relative key, object type other than regular file, unexpected file/ACL, checksum/size mismatch, ineligible row privacy; ignore no checksum. Do not publish secrets/raw row values in result/error/manifest.
6. Strict YAML duplicate keys/unsupported tags, JSON duplicate keys, unknown version, missing reason/null inconsistency all fail before domain instantiation.
7. Error exit3 for unauthorized requested row-level export, no row staging; exit0 means technical complete, not Science acceptance.

**Freeze gate**: independent architecture/scientific/security review of this exact contract; Method-specific G08 references, real FS/ACL/Codec/Schema verification, legacy readback must be collected at appropriate authorized Gate. The matrix is a design candidate, not a test execution.
