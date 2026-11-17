# PREP-02 F05 — Trusted Local Root, privacy and row-export authorization freeze-preparation contract

- Date: 2026-11-17 JST
- Type: FLOW / threat model + security wire/Port candidate
- Owner authority: [DEC-PREP02-A](decisions/94_20261117_dec_prep02_owner_architecture_choices.md), Option A (nondelegated effective UID)
- Status: DETAILED_DRAFT / NO_OS_PROBE / SECURITY_REVIEW_NOT_RUN / NOT_FROZEN

## 1. Trust model / non-goals

- Actor is the actual local process effective UID, not CLI-provided identity or Product `X-User-Id` / ProjectMembership. No user delegation, shared/CI/container-root accessible volume in initial support.
- Threats: symlink/TOCTOU, root substitution, untrusted mount namespace, ACL/group/shared access, hardlink/special file, world-readable output, shell/log exception leakage, data set with restricted columns.
- Ownership equality is **necessary but insufficient**. The “trusted” root must be a verifiable private directory held by a stable opened directory FD; OS mode 0700 alone does not establish mount isolation. Unknown identity/mount/ACL facts = reject, not “best effort”.
- Single-UID local policy cannot cryptographically prevent that same UID from modifying its own configuration/policy. Therefore **preauthorized Study policy** must have independently identifiable authority/provenance (separate policy artifact or verified binding), rather than a boolean the untrusted Study request self-asserts. How to attest preauthorization is an explicit F05 unresolved policy implementation choice.

## 2. Trusted root proof (candidate)

| Check | Evidence to collect from OS | Deny cases |
|---|---|---|
| Platform | Linux local POSIX runtime and syscall availability | unsupported OS / atomic primitive unavailable |
| Principal | `geteuid()`, `getuid()`, `getegid()`, supplementary groups, user namespace mapping | delegated/shared/namespace-ambiguous principal; effective UID differs from root owner |
| Root/path | `fstat` on securely opened component FDs, directory type, owner, mode and immutable handle identity | symlink, non-directory, no-private mode, owner mismatch, path race, change before publish |
| ACL | POSIX ACL / security/xattr effective permissions for root and ancestors, under actual mount semantics | group/other effective access, unresolved ACL or missing inspection capability |
| Mount | `statx` mount ID or `/proc/self/mountinfo` identity plus FS type and options; compare staging vs final | shared network/overlay/container/CI bind mounts or ambiguous mapping, cross mount or hidden remote access |
| Output | 0700 dirs / 0600 files and no additional ACL grants; stable type, owner and size/hash | unexpected ACL/modes, modified artifacts post-seal |
| Audit | stable nonsecret principal/root/policy evidence digest and outcome, no row contents | logging row values or credential/absolute sensitive paths |

Root proof is a point-in-time OS observation. It must be renewed or bound to stable file descriptors and inode/mount identities at each mutable boundary (pre-staging, pre-rename, reader). Avoid claims that a “private” mount can be proven only from `st_mode` and `st_uid`.

## 3. Row-export policy conjunction

Let:
- `S` = Study explicitly requests row export
- `F` = CLI `--allow-row-level-export`
- `P` = separately authorized Study privacy-policy evidence (scope includes current study/run, allowlisted columns and max rows)
- `R` = verified private nondelegated TrustedLocalRoot and same euid/root owner, ACL/mount checks all pass
- `C` = all output columns belong to approved allowlist, row count within positive finite bound, no sensitive logging

Then **row output permit = S ∧ F ∧ P ∧ R ∧ C**. On any false/unknown, no row file should be materialized even to staging. An aggregate-only run must still use a verified root; aggregation is not an excuse to publish into an untrusted mount.

| S | F | P | R | C | Outcome |
|---|---|---|---|---|---|
| 0 | any | any | valid | any | aggregate-only, no row artifact |
| 1 | 0 | any | valid | any | DENY row export |
| 1 | 1 | 0/unknown | valid | any | DENY row export |
| 1 | 1 | 1 | invalid/unknown | any | DENY entire unsafe publication |
| 1 | 1 | 1 | valid | 0/unknown | DENY row export |
| 1 | 1 | 1 | valid | 1 | Restricted Parquet artifact only, no console/JSON/log rows |

The initial document does not decide whether a requested but denied row export should abort the complete execution or yield an aggregate-only result; **recommend deny explicit request rather than silently downgrade**, so the caller knows the requested delivery did not occur.

## 4. Candidate typed interfaces

~~~python
@dataclass(frozen=True)
class LocalPrincipalEvidence:
    effective_uid: int
    owner_uid: int
    mount_id: str
    mount_type: str
    acl_evidence_digest: str
    delegated: bool
    process_environment: str  # LOCAL or UNKNOWN/CI/CONTAINER

@dataclass(frozen=True)
class RowExportAuthorization:
    study_identity: str
    policy_ref: ContentRef
    authorized_columns: tuple[str, ...]
    max_rows: int
    classification: str

class TrustedLocalRootPort(Protocol):
    def open_verified(self, raw_root: Path, principal: LocalPrincipalEvidence) -> TrustedLocalRoot: ...

class LocalPrivacyPolicyPort(Protocol):
    def authorize(self, study: LocalStudySpec, cli_flag: bool, root: TrustedLocalRoot, evidence: RowExportAuthorization | None) -> PrivacyDecision: ...
~~~

`TrustedLocalRoot` carries validated directory handles and actual OS security facts. A DTO alone, a caller-supplied `LocalPrincipalEvidence`, or a boolean `row_export_authorized` from the same YAML does **not** establish authorization. The concrete trusted authority for `RowExportAuthorization` is still OPEN and requires Security/Owner input.

## 5. Reasons and tests

Candidate codes: `ROOT_OWNER_MISMATCH`, `ROOT_NOT_PRIVATE`, `MOUNT_UNTRUSTED`, `PRIVACY_POLICY_UNVERIFIED`, `ROW_EXPORT_NOT_AUTHORIZED`, `ROW_EXPORT_COLUMNS_DENIED`, `ROW_EXPORT_LIMIT_EXCEEDED`, `PRIVATE_ARTIFACT_DENIED`, `PATH_CONFINEMENT_FAILED`.

Test ARCH-F05-01〜04 (plus an explicit policy-spoof negative) must verify:
- missing CLI flag or self-authored Study `row_export_authorized: true` is not sufficient;
- UID mismatch, group/ACL exception, mounts/CI/container/namespace ambiguity deny;
- approved minimum Parquet columns, row cap, 0700/0600, no raw stdout/stderr/log/manifest data;
- secrets/path/rows redacted on invalid parser, exception or failed publication; effective reader enforces privacy before bytes return.

**Not run.** F05 cannot be frozen until trusted Policy authority, mount/ACL algorithm, deny behavior and Security review are ratified, along with real system tests.
