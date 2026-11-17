# DEC-PREP02 — PREP-02 共通Architecture方針 Owner採用記録

- Date: 2026-11-17 JST
- Authority: User (Owner) explicit approval, 2026-11-17 09:21 JST
- Baseline: `prototype/ariadne_mvp` at `584fa9e7a709522c73b08ed911cabb71ccdb7684`
- Disposition: **A=A / B=A / C=A ADOPTED**
- Classification: Flow / Owner decision; not independent Architecture Review, Schema/Port Freeze, scientific or runtime PASS
- Scope: ENH-E11 CLI-only Local. Product Web/API/DB/Worker and legacy `causal-analysis-spec/2` unchanged.

## DEC-PREP02-A — Local row-level export authority: Option A ADOPTED

Initial delivery permits **only non-delegated local execution by the effective UID which owns the trusted local root**. Deny delegated principal, shared/CI/container-root accessible volumes and ambiguous mount/ACL exposure unless a separately reviewed policy explicitly expands support. Default: no row-level export. Row export requires all of: explicit CLI intent, advance Study privacy policy authorization, runtime UID/root ownership match, private filesystem access, column minimization and bounded output. CLI flag alone is not authorization. Do not invent Product ProjectMembership as CLI authority. Fail closed when identity, ACL, mount, group or permissions cannot be proven. Prevent raw rows/secrets in stdout/stderr/log/exception/manifest.

**Still required:** precise principal/mount/ACL probing algorithm, negative integration tests, Security review. The restriction is adopted, not demonstrated.

## DEC-PREP02-B — Atomic no-replace publication: Option A ADOPTED

Initial target is Ubuntu/Linux, same-filesystem staged immutable directory bundle, verified before publishing. Use an **effective atomic no-replace** filesystem primitive (candidate `renameat2(RENAME_NOREPLACE)`) and reject unsupported implementation/FS rather than falling back to check-then-`rename`, plain replacement, or process-local lock. Treat concurrent `run_id` collisions as conflict; accept reuse only after complete verified readback of matching request hash and full bundle. Protect relative keys and intermediate components, write marker/manifest and files in staging, fsync files and directory as specified, then no-replace publish and parent directory fsync. Do not claim cross-FS, NFS/object-store, crash durability, or exactly-once guarantees without targeted evidence.

**Still required:** ABI/errno mapping (`EEXIST`, `ENOSYS`, `EINVAL`, `ENOTSUP`, `EXDEV`), syscall wrapper and platform constraints, fsync/crash matrix, filesystem/race/negative tests and independent Review.

## DEC-PREP02-C — E11 schema namespace: Option A ADOPTED

Adopt version discriminators as **normative identifiers**:

| Logical payload | Required version |
|---|---|
| Study | `e11-local-study/1` |
| Graph | `e11-local-graph/1` |
| Effect result | `e11-local-effect-result/1` |
| Manifest | `e11-local-manifest/1` |
| Status | `e11-local-status/1` |

Readers must perform strict explicit dispatch; unknown versions and `causal-analysis-spec/2` as E11 input fail closed; no implicit aliases/coercion/conversion. Preserve existing legacy v2 reader and tests. Adopted identifiers are **not** approval of still-absent machine-readable JSON Schema, enum equality, Protocol signatures, typed error semantics or compatibility fixtures.

## Follow-through / acceptance

| Finding | Owner decision now | Remaining PREP-02 blocker |
|---|---|---|
| F03 | No-replace Option A | Frozen publish/readback signatures; race/crash/FS evidence; independent review |
| F05 | Non-delegated privacy Option A | Principal/mount/ACL threat model, deny tests, security review |
| F06 | E11 namespace Option A | JSON Schemas, strict dispatch, version-negative and legacy regression tests |
| F04/F07 | No new decision | Port/DTO bridge; confidence-set/null semantics schema |
| F08/F09/F12 | No new decision | 41 Method contracts by Gate, environment probes, independent Architecture Review |

Do not alter `docs/wiki/requirement_definition/`, Product source, `pyproject.toml`, or `uv.lock` on the basis of this approval. PREP-01 and PREP-02 remain IN_PROGRESS; Coding NOT_AUTHORIZED.
