# PREP-02 F04 — Product / Local Scientific Port & DTO boundary ADR candidate

- Date: 2026-11-17 JST
- Scope: ENH-E11 CLI-only (no Product API/DB/Worker changes)
- Kind: FLOW / architecture decision PROPOSAL / independent review input
- Status: PROPOSED_NOT_FROZEN / REVIEW_NOT_RUN / CODING_NOT_AUTHORIZED
- Owner choices DEC-PREP02 A/A/A retained; no new Owner decision assumed

## 1. Observed existing API contracts (source-verified)

| Product component | Source blob | Observable signature | E11 incompatibility |
|---|---|---|---|
| Product ScientificCorePort | `ccf89d307d626e7b4c82fe3f919230bb781d7f6a` | `run_discovery/identification/estimation/refutation/sensitivity(input_, output_dir:Path) -> list[ScientificResultDescriptor]` | Product `ResultType/ScientificStatus` and generic payload; no typed partial identification, AR set, CI null-reason guarantee |
| Product ScientificResultDescriptor | same | `result_type, scientific_status, summary, payload, diagnostics, warnings, artifacts` | Status is tied to Product result type and does not represent E11 independent technical/inference/science axes |
| Product ArtifactStorePort | `e5bb990f9b69ef68df46a1559560ffb67b64caaf` | `store/retrieve/exists/delete` | Does not implement immutable atomic multi-file run directory commit |
| Legacy CliManifest | `97216eca9d777e97f7a5ebd4e248afd31c6b4de0` | `manifest_version` and `snapshot_schema_version="causal-analysis-spec/2"` | No E11 strict version/marker/readback; cannot be auto-upgraded |
| Product GraphVersion | `37ff76e001c8e269a00127e18d375f1dbc34c0e3` | `graph_type` DAG/CPDAG/PAG and `graph_json` | E11 endpoint/lag evidence cannot be presumed to survive projection |

## 2. Proposed architectural decision: parallel local DTOs and Ports

**Recommend distinct Local Contracts, not inheritance, casting, or an implicit adapter from existing Product Ports.** Only verified framework-free calculation functions with semantically matching Method/Estimand/Inference may be reused behind explicit E11 adapters. The E11 DTO is the boundary authority; optional library return objects do not cross it.

- Dependency: CLI File Adapter -> Local Application -> local typed Domain Port <- Scientific Adapters.
- `LocalStudySpec` (Study v1) owns run intent and ContentRef identities; `GraphEvidence`/`IdentificationOutcome` are immutable science evidence; `EffectOutcome` owns point, inference, status and upstream hashes as separate dimensions.
- `ContentReferencePort.verify` returns bytes/verified metadata from securely opened and hashed descriptors. No Python Path identity alone is a verified input.
- `MethodCapabilityPort.resolve` returns effective backend ID/version/API, supported target and inference; no eager optional imports or silent fallback.
- `IdentificationPort.identify` requires approved identifier request and returns typed proof/negative; `EstimatorPort.estimate` takes validated eligible request and **staging-only** artifact sink. It never writes final `runs/{run_id}` directly.
- `LocalPublicationPort.publish` (F03) and `LocalManifestReader.verify` own no-replace commit, immutable evidence readback and strict v1 dispatcher; Product ArtifactStorePort is not the same guarantee.

### Proposed executable-style Protocol signatures (typing design only)

~~~python
class ContentReferencePort(Protocol):
    def verify(self, ref: ContentRef, root: TrustedLocalRoot) -> VerifiedContent: ...

class MethodCapabilityPort(Protocol):
    def resolve(self, method_id: MethodId, backend: BackendId, profile: ProfileId) -> BackendCapabilityRecord: ...

class IdentificationPort(Protocol):
    def identify(self, request: ValidatedIdentificationRequest) -> IdentificationOutcome: ...

class EstimatorPort(Protocol):
    def estimate(self, request: ValidatedEstimatorRequest, sink: StagingArtifactSink) -> EffectOutcome: ...

class DiagnosticPort(Protocol):
    def run(self, request: ValidatedDiagnosticRequest, sink: StagingArtifactSink) -> DiagnosticOutcome: ...

class LocalPublicationPort(Protocol):
    def publish(self, staged: ValidatedStagedBundle, root: TrustedLocalRoot) -> CommittedLocalRun: ...

class LocalManifestReaderPort(Protocol):
    def verify(self, ref: LocalRunRef, root: TrustedLocalRoot) -> VerifiedLocalRun: ...
~~~

All names and Protocol signatures are **candidate**, to be frozen only after source contract review and separate schema/Error alignment. `TrustedLocalRoot` is a verified root capability, **not an arbitrary caller-supplied Path**. `Validated*Request` must bind question/design/graph/dataset/estimand/method and upstream content hashes; it cannot be fabricated by a caller without validation.

## 3. Adapter eligibility and failure matrix

| Case | Required behavior |
|---|---|
| Product `ScientificResultDescriptor` with `ESTIMATED` but missing inference and science evidence | **Do not cast** as E11 CONFIRMATORY PASS |
| Product `ScientificStatus.IDENTIFIED` without a proof that fixes Estimand and GraphVersion | **Do not treat as a sufficient E11 IdentificationOutcome** |
| DoWhy implementation label resembles LATE, B0/B1/DRIV target differs | BLOCK semantic adaptation; preserve target by explicit Estimand ID |
| Product ArtifactStore can write every file but multi-file publication is not atomic | BLOCK use as E11 commit, even if file checksums are correct |
| Product CliManifest v2 | Reject in E11 decoder; preserve legacy reader unchanged |
| Method not eligible / inference unsupported | Typed ScientificNegativeOutcome or preflight unsupported response, **not** a fake finite Effect/CI |
| External backend import unavailable | Typed capability error, no silent substitute backend |
| Lossless plain computational primitive (fixed estimand, evidence preserved) | Reuse behind explicit Local adapter **only after** Method Gate scientific evidence |

## 4. Required verification before Port Freeze

- F04-P01: type-check all Protocol signatures with pure local DTOs, no Product Domain/CLI import in Local Domain module, no optional backend import at import time.
- F04-P02: 5 existing Product `ScientificCorePort` call signatures and legacy v2 readback unchanged (regression at relevant Gate).
- F04-P03: every E11 Method maps to exactly declared Operation×Estimand×Backend×Inference; unsupported combination rejects.
- F04-P04: reject Product-to-Local status flattening, AR set loss, Graph endpoint/lag conversion, incomplete upstream hash.
- F04-P05: verified ContentRef and staging sink cannot use arbitrary final path; F03/F05 filesystem and privacy tests separately.
- F04-P06: distinguish code-level Protocol typing PASS, independent Architecture review disposition, runtime backend Science Gate PASS.

**Open:** exact module path, typed error registry, real backend API probes, all 41 Method Gate cells and Independent Architecture Reviewer verdict. This document does not approve code entry.


## 5. PREP-02 cross-Port signature reconciliation（2026-11-17）

[F03–F07 definitive review **candidate**](112_20261117_prep02_f03_f07_shared_port_signature_contract.md) supersedes the earlier illustrative Protocol forms in §2 as the **single common review input**. `ValidatedStudy` is constructed by CLI `LocalConfigDecoder` outside Application; `ValidatedCapabilityRequest` and other verified types flow into Ports; `EstimatorPort`/`DiagnosticPort` take keyword-only `sink`. `LocalPublicationPort.begin/seal/publish` is a Façade over per-run `LocalArtifactPublisher` handles, not an alias to Product `ArtifactStorePort`. `LocalPrivacyPolicyPort.authorize` verifies signed/independent Policy before any internal `LocalPrivacyPolicy.assert_export_allowed` guard. The exact Python module ABI and runtime type checking remain unproven.
