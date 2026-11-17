# PREP-02 F05 — Preauthorized row-export Policy Trust Anchor implementation candidate

- Date: 2026-11-17 JST
- Classification: FLOW / security mechanism architecture candidate, not Owner grant or independent Security Review
- Owner authority: DEC-PREP02-A Option A and DEC-PREP02-D D-F05-POLICY Option A
- Status: `POLICY_AUTHORITY_MECHANISM_PROPOSED / SECURITY_REVIEW_NOT_RUN / NOT_FROZEN`

## 1. Threat boundary and feasibility

Initial executor is a nondelegated Linux effective UID operating in its own private local artifact root. That **does not** establish independence of an approval merely because a `policy_ref` lives in a different file. The same UID can generally forge a local authorization file it owns. The verified prior approval therefore requires **a separate trust anchor not writable by the executing UID**, or a cryptographic signature verifiable against a key that the executing UID cannot substitute.

**Preferred mechanism proposal:** detached **Ed25519 signature on the canonical typed policy bytes**, with the public verification-key allowlist and issuer/role bindings provisioned in an administrator-owned, non-writable local trust store (e.g. an OS-managed policy root owned by a separate administrative principal). Do not accept a public key supplied in the Study, a copied key beside the policy, or a trusted-key file writable by EUID. The execution UID must not be able to alter issuer grants or approval records. If the trust anchor does not exist or cannot be verified, **row export is unavailable**, aggregate-only runs can remain available in verified roots. The signer/admin provisioning and provisioning lifecycle are a deployment prerequisite, not a Product RBAC dependency.

## 2. Suggested immutable Policy envelope (wire draft)

~~~json
{
  "policy_version": "e11-local-row-export-policy/1",
  "policy_id": "approved-policy-001",
  "issuer_id": "admin-policy-authority",
  "key_id": "provisioned-public-key-001",
  "subject_study_identity": "study-id-pinned",
  "subject_study_approval_digest": "sha256-of-study-approval-projection",
  "approved_scope": ["ROW_EFFECT_PARQUET"],
  "classification": "RESTRICTED_ROW_LEVEL",
  "allowed_columns": ["row_id", "estimated_effect"],
  "max_rows": 1000,
  "issued_at": "2026-11-17T00:00:00Z",
  "expires_at": "2026-12-17T00:00:00Z",
  "revocation_epoch": 0
}
~~~

**Sample values are illustrative, not accepted identities.** Signature is a detached binary value authenticated over **domain-separated, versioned canonical Policy bytes**. The Policy envelope is not itself the verification key. Define `subject_study_approval_digest = SHA256(JCS(typed Study with privacy.policy_ref replaced by null))`. **This digest is deliberately distinct from** the full `request_hash = SHA256(JCS(typed Study including privacy.policy_ref))`. The signature covers `subject_study_approval_digest` (plus scope and issuer claims). Reader recomputes both independently; do not confuse the approval-subject digest and the run request hash. A blind signature over `study.request_hash` that includes its own `policy_ref` must define how those references are bound and cannot be presumed correct. The exact domain-separation and digest-projection contract require Architecture/Security review.

## 3. Port contract and fail-closed algorithm

~~~python
class LocalPolicyVerifierPort(Protocol):
    def verify(self, *, policy_ref: ContentRef,
               study: ValidatedStudy,
               root: TrustedLocalRoot,
               anchor: PolicyTrustAnchor) -> VerifiedStudyPolicyEvidence: ...
~~~

Verify, in order: (1) secure-open root-trusted `policy_ref` and actual bytes hash; (2) strict versioned parser and schema; (3) load issuer key/authorization from admin-only trust store and check permissions/immutability; (4) detached signature over exact domain-separated canonical bytes; (5) issuer permission for ROW_EFFECT_PARQUET; (6) approved Study identity + projected request hash + scope; (7) UTC issued/expires interval, revocation list/epoch freshness; (8) allowed column subset and maximum rows positive finite, confidentiality class; (9) runtime EUID/root/ACL/mount policy; (10) return immutable `VerifiedStudyPolicyEvidence` containing **only approved fields and nonsecret digest**.

- Invalid signature, missing issuer, stale revocation, changed body, mismatched Study, expired approval, untrusted mount/ACL, unknown format => `PRIVACY_POLICY_UNVERIFIED` or `ROW_EXPORT_NOT_AUTHORIZED` **exit3**, row bytes not staged.
- A Study CLI request and its own `row_export_authorized:true` are never independent approval.
- No secret private signing key is bundled in the CLI, manifest, output root or package. Public trust-store metadata may be logged in redacted form; row values never logged.
- Time-of-check/time-of-use: validate full authorization before staging and check expiry/revocation/root before seal; no silent fallback to aggregate if user requested rows.
- Agent/OS identity limitations: this local guard does not secure data from an administrator or the filesystem's legitimate owner outside Ariadne; it only constrains what Ariadne is authorized to publish.

## 4. Freeze blockers

| ID | Test/review to perform | Accepted if |
|---|---|---|
| POL-01 | signer and key provisioned outside the EUID; admin file unwritable, secure open | Unprivileged actor cannot substitute trust anchor |
| POL-02 | self-signed, arbitrary local key, changed policy, mismatched subject hash/scope | exit3 and no row-file bytes |
| POL-03 | expired, revoked, unknown issuer, stale epoch, time spoof within stated trust model | fail-closed and evidence |
| POL-04 | policy with extraneous columns, too many rows, classification mismatch | deny; no leaking diagnostic |
| POL-05 | root mounted/shared/ACL unsafe/identity changed before publication | deny; no out-of-scope write |
| POL-06 | legitimate independently signed scope + owner EUID + private root + CLI/Study request | restricted Parquet with bounded rows/columns, 0600/0700, no console/log data |

**Unresolved:** who is authorized to approve, key lifecycle/rotation, revocation freshness, projection of Study identity versus PolicyRef, external trust-store support on target machine. The exact Ed25519 mechanism is an engineering proposal consistent with Owner A, not additional Owner approval. Without verified trust anchor, F05 cannot be frozen.
