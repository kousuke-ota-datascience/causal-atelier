# AMD-E11-G01-P05-003 — Independent publication session binding

**Date:** 2026-11-24 JST  
**Gate/Package/Trial:** G01/P05/Trial01  
**Owner decision:** DEC-G01-P05-ABORT-SESSION-BINDING-01=A_ADOPTED (combined_review/258)  
**State:** AUTHOR_PREPARED_FORMAL_09_CANDIDATE / FORMAL_09_OWNER_APPROVAL_PENDING / S10_REFREEZE_PENDING / S11_REAUTH_PENDING / P05_BLOCKED  
**Last blocked START_SHA:** 9420734f7968bfe85d72c535dd670ed85f753874  
**Current immutable S10:** ef8e67ffa795e4ab00a4f86b600dac046548f5b4  
**Prior S11:** DEC-G01-P05-002-S11-REAUTH-01; not authorization for this amendment.

## 1. Defect and scope of supersession

AMD-002 required abort(sink,reason) to distinguish sessions, but existing _Sink only holds its Publisher, and that Publisher stores root, run_id, request_hash and policy, not issuing Adapter or independent attempt identity. Two legitimate sinks sharing policy and STAGING state satisfy self-identity checks. Even equal run/hash/root can describe distinct attempts. The reported ext4 experiment establishes that identification defect, not actual erroneous abort execution. Owner adopts docket 258 A. Supersede only AMD-002's identity/signature, issuance and bounded P02 exception provisions. Preserve AMD-001 Manifest Factory boundary and all other AMD-002 failure, publication and verification rules.

## 2. Exact internal API and source changes permitted after new S11

In src/ariadne/capabilities/causal/ports/local_io.py, define nominal empty class:

~~~python
class PublicationSessionToken:
    __slots__ = ()
~~~

Use object identity, not value equality; do not serialize/log it. P05 constructs a fresh token per attempt, independently retains validated run_id, request_hash and exact root object before begin. No token reuse, no registry. Internal LocalPublicationPort signatures:

~~~python
def begin(self, *, run_id: str, request_hash: str, root: TrustedLocalRoot,
          session: PublicationSessionToken | None = None) -> StagingArtifactSink: ...
def abort(self, *, sink: StagingArtifactSink, session: PublicationSessionToken,
          run_id: str, request_hash: str, root: TrustedLocalRoot,
          reason: str) -> None: ...
~~~

Existing seal/publish and scientific StagingArtifactSink signatures unchanged. In src/ariadne/interfaces/cli/local_causal/publication.py, import token; extend LocalArtifactPublisher.__init__ after existing four arguments by keyword-only issuer: LocalPublicationAdapter | None = None and session: PublicationSessionToken | None = None. Store once as _issuer and _session before creating original _sink. Existing direct construction with four arguments remains valid. Adapter.begin retains existing keyword args and return type, adds session=None; rejects non-null invalid nominal token before staging and constructs original Publisher with issuer=self and session=session, then calls its unchanged concrete begin exactly once. Legacy session=None supports old begin/seal/publish; not facade abort. No setter or new constructor collaborator in Application.

Adapter.abort checks type(sink) is _Sink and type(session) is PublicationSessionToken, then p=sink._publisher, type(p) is LocalArtifactPublisher, sink is p._sink, p._issuer is self, p._session is session, p.run_id == run_id, p.request_hash == request_hash, p.root is root, p.permission_policy is self._permission_policy, p.state in (PublishState.STAGING, PublishState.VALIDATING). All checks precede mutation/delegation; mismatch uses existing PUBLICATION_FAILED. Invoke unchanged p.abort(reason) exactly once only after successful checks. Reason is nonsecret. Use exact nominal classes rather than accepting structural lookalikes. No access to CLI private fields from Application. Trusted in-process accidental substitution boundary, not protection against arbitrary private-field tampering or replacement of every trusted input. Per-session operations sequential; distinct sessions may interleave. Freshness is a caller obligation, no global token registry.

## 3. P05 sequencing and error contract

P05 retains independent tuple before begin; no expectation reconstructed from candidate sink. After successful begin, abort eligibility is true until immediately before invoking publish, when eligibility is cleared, even if publish raises. On Discovery/staging/evidence/Manifest Factory/seal failure while eligible, attempt once with sink and original tuple. No abort before successful begin or after publish invocation; existing concrete Publisher owns failures inside publish and indeterminate results. Retain primary typed failure and CLI exit; secondary nonsecret cleanup fault separately. Never delete potentially committed run; quarantine/FD release is not secure erasure. No newly committed final run/Marker; preserve pre-existing final run; private staged Marker after seal is not committed proof.

## 4. Normative documents and verification

IF 23_41 §4.1b and Port table; DD 30_62 §8.2/8.2a; P05 06 §6.4/6.6a; G01 07 G01-07-05/07/11 identity and failure matrices. Amend these only; historical AMD-001/002 and completed Package records remain historical. Tests require valid pairing and distinct Adapter/same policy, same Adapter/different run, identical run/hash/root/different token, wrong root/hash/policy, fake sink, invalid token, legacy tokenless abort rejection, invalid/repeated state, no mutation/FD closure of either session on refusal, and legacy begin/seal/publish regression. Confirm all independent expected values retained before issuance. Real FS tests and protected P02/Product regressions required; previous reported 207 passes do not cover new path. No source or tests executed here.

## 5. Bounded exception and protected invariants

Only permitted future completed P02 changes: token and Port begin/abort in local_io.py; Publisher constructor optional arguments/private issuance fields and Adapter begin/abort in publication.py, including necessary imports. No changes to existing concrete begin/stage_bytes/validate/commit/abort algorithms, Adapter seal/publish, scientific sink, completed P02 06/07/tests/checkpoint, or P01/P03/P04. A requirement beyond this scope needs separate Owner approval. Existing begin callers and direct constructor calls remain compatible at call level; regression must establish behavioral compatibility.

Retain P01 9bff61f0eae25236f95f31f2cd3e7c81291f0167, P02 3a76a0aa1698037354b284ba7b5a875300473ce6, P03 858c9f73366036a2d1445e558135cd521f611462, P04 7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6. No public E11 Schema Version, scientific meaning, Privacy/Reader, Product v2, uv.lock, independent science or G01_999 acceptance change. DEFERRED_PRODUCT_POLICY_BRIDGE remains UNFULFILLED. No new checkpoint or PASS. Formal 09 Owner approval, exact SHA S10 refreeze and distinct S11 limited authorization remain separately pending. No coding under AMD-003 until all three completed.
