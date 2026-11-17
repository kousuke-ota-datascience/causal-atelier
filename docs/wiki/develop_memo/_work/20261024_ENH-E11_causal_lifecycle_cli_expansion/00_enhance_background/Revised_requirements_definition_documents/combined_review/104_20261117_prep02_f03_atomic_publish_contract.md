# PREP-02 F03 — Linux Local no-replace publication and readback freeze-preparation contract

- Date: 2026-11-17 JST
- Type: FLOW / mechanical architecture contract draft
- Owner authority: [DEC-PREP02-B](decisions/94_20261117_dec_prep02_owner_architecture_choices.md), Option A
- Status: DETAILED_DRAFT / NO_RUNTIME_FS_PROBE / NOT_FROZEN / NOT_INDEPENDENTLY_REVIEWED

## 1. Explicitly selected mechanism

Use **Linux `renameat2(2)` with `RENAME_NOREPLACE`** for same-mounted-filesystem **directory** transfer from private `ROOT/.staging/<token>` to `ROOT/runs/<run_id>`. Parent directory FDs must be opened under the same `TrustedLocalRoot` capability; do not interpolate attacker-controlled path strings into the final syscall. `Path.exists()+Path.rename()`, ordinary replacement rename, process mutex and preexisting-file deletion are **forbidden alternatives**, not fallback mechanisms. No guarantee beyond successfully exercised FS/kernel combination.

Linux man page source: https://man7.org/linux/man-pages/man2/renameat2.2.html . RENAME_NOREPLACE is not supported uniformly across filesystems. `EEXIST` means a competing destination may exist and **must be fully verified** before same-hash reuse; a conflicting/corrupt destination cannot be replaced. `ENOSYS/EINVAL/EOPNOTSUPP/ENOTSUP/EXDEV` on this operation means unsupported or incompatible and must fail closed; `EACCES/EPERM/EROFS/EIO/ENOSPC` are typed I/O failures. Beware `EEXIST` may also arise from other collisions; inspect destination within the trust boundary instead of assuming same request.

## 2. Candidate Port types and operation signatures

| Type / method | Inputs | Output | Contract |
|---|---|---|---|
| `TrustedLocalRoot.open_verified(Path, LocalPrincipalEvidence, RootPolicy)` | root and OS/ACL/mount evidence | `TrustedLocalRoot` capability containing safely held root/runs/staging dir FDs and identity snapshots | F05 checks before FS writes; reject change of verified identity/permissions/mount before commit |
| `LocalPublicationPort.begin(run_id, request_hash, TrustedLocalRoot)` | safe run ID, SHA256, root capability | private `StagingArtifactSink` | 0700 root staging dir, exclusive token, no final state |
| `StagingArtifactSink.stage(key, bytes, media_type, classification)` | verified relative key, immutable bytes, classification | `StagedArtifactRef` | O_EXCL and no symlinks, reject duplicates/forbidden row data |
| `LocalPublicationPort.seal(staging, manifest, privacy_decision)` | all staged files and canonical manifest | `ValidatedStagedBundle` | verify bytes/size/hash/privacy + marker; fsync files and staging dirs; close mutation handles |
| `LocalPublicationPort.publish(validated, root)` | sealed staged capability, same root | `CommittedLocalRun` or typed failure/indeterminate | Linux atomic no-replace, parent dir fsync, independent reader readback |
| `LocalManifestReaderPort.verify(root, run_id)` | private root, safe run ID | `VerifiedLocalRun` | marker→manifest bytes→artifact bytes, all hash/size/type/schema/version/permission checks |

This is an implementation-ready **candidate**, not an existing Python signature; reconcile class names and module placement with `30_61/62`.

## 3. Required publication state machine and durable order

1. `PREPARING`: secure Open root and both parents, stable `st_dev` and `mnt_id`, effective principal, private modes/ACL, no unsupported FS. Initial target is private POSIX local filesystem; allowlist of tested mount types/revisions is **not yet established**.
2. `STAGING`: create random exclusive staging directory under a safe parent FD, with 0700; create every data file with 0600 using no-follow dirfd traversal. Avoid hardlinks and special files; reject unapproved row-level contents at write time.
3. `VALIDATING`: strict schemas + canonical bytes; SHA256 and byte length from actual open FDs; canonical manifest lists staged artifact refs and input hashes but **not self-hash**; write `manifest.json` then marker `_COMMITTED.json` with `marker_version=e11-commit/1` and manifest bytes hash. Marker is **outside** manifest artifact inventory.
4. Sync every newly created/modified file (including manifest and marker), then stage nested dirs bottom-up, finally staging top dir. Mark bundle sealed (no subsequent writes or chmod). `fsync` errors abort **before publication**. Source `fsync(2)`: https://man7.org/linux/man-pages/man2/fsync.2.html .
5. `PUBLISH`: one `renameat2(staging_parent_fd, token, runs_parent_fd, run_id, RENAME_NOREPLACE)`. Do not call a check-then-rename fallback on unsupported FS. Handle EEXIST by verifying existing run **under stable dirfds** with equal request hash plus all published bytes.
6. After a successful rename, `fsync` both staging-parent and runs-parent directory FDs (not just stage or file FDs). Read back destination via independent `LocalManifestReaderPort`. Only after all steps succeed return `COMMITTED/COMPLETED`.
7. If publication syscall succeeds but subsequent sync/readback fails, **do not delete or overwrite** possibly published directory. Emit `PUBLICATION_INDETERMINATE`/typed failure and an idempotent verification/recovery action. Presence is never sufficient; caller must verify before success.
8. Unpublished staging may be quarantined under limited retention/cleanup policy; never automatically delete any already published run, including one with invalid or missing marker.

## 4. Failure taxonomy (draft)

| Condition | Stable reason code | Expected behavior |
|---|---|---|
| destination exists, conflicting request/hash | `RUN_ID_CONFLICT` | no overwrite; exit publication failure |
| destination same request, full reader validation succeeds | `RUN_REUSED_VERIFIED` (information, not failure) | idempotent existing reference |
| file or manifest invalid | `ARTIFACT_HASH_MISMATCH` / `MANIFEST_HASH_MISMATCH` / `NOT_COMMITTED` | reader deny; do not reuse |
| unsupported rename ABI, FS, cross-mount | `ATOMIC_PUBLISH_UNAVAILABLE` | fail closed, never plain rename |
| file/data/dir fsync failure before rename | `STAGING_DURABILITY_FAILED` | no committed success |
| post-rename directory fsync or reader readback failure | `PUBLICATION_INDETERMINATE` | no deletion; recovery verification required |
| path component symlink/race/special file | `PATH_CONFINEMENT_FAILED` | reject without outside read/write |

Codes are candidates requiring F06 typed registry freeze; do not infer actual OS capability.

## 5. Acceptance/fault injection

Re-use ARCH-F03-01〜06 in [95 acceptance matrix](95_20261117_prep02_f03_f05_f06_acceptance_matrix.md). Distinguish: concurrent 2-process same run ID different/same hash; EEXIST corrupt preexisting; EINTR handling; ENOSYS/EINVAL/EOPNOTSUPP/EXDEV; fault after every sync; abrupt process kill before/after rename; symlink component swap; hardlinks/special files; disallowed mount types; root change between stage and commit. Each test records mountinfo ID/type, kernel/FS, source SHA and actual reader result.

**Not run**. No independent review, FS capability allowlist, target platform ABI or durability proof. F03 remains OPEN.
