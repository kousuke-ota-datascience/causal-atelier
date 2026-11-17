# ENH-E11 G01 P02 — Trusted Root, Atomic Publisher, Readback

**Document class:** Primary Execution Contract  
**Self-containment:** MUST — Assigned Coding Agentが本書だけでpackageのnormative execution responsibilityを理解できること。

- Gate: G01
- Trial: Trial01（未開始）
- Package: P02
- Parent 06 (traceability): 06_Ariadne_ENH-E11_G01_implementation_instruction.md
- P00 Plan (traceability): 06_G01_P00_work_package_plan.md
- Depends on: P01
- Status at issuance: DRAFT / CODING_NOT_AUTHORIZED

## 1. Purpose
private TrustedRootとimmutable multi-artifact run publicationを実FSで安全に確立する。

## 2. Effective Gate constraints applicable to this package

このpackageが守るべきGate-level semanticsを、Parent 06 / P00を読まなくても実行判断できる粒度で記載する。

G01は正式Gate IDでPxxはbounded Coding Unit。Local laneとProduct v2を分離し旧CLI/Web/API/DB/Workerは改変しない。strict version/Method/EstimatorとJCSのハッシュ対象を検証し、PAGをDAG/ATEへ変換しない。OS root/Privacy/Atomic Publishの不適格はfail-closed、SCI不確実性をPASSに変換しない。Coding Authorization前の実装は禁止。

## 3. In scope — implementation ownership

| Module/Class | Owned implementation | Boundary |
| --- | --- | --- |
| `ariadne.shared.local_fs.TrustedLocalRoot/LocalPrincipal` | verified OS capability and strict root factory at CLI composition | No trust delegated to Study/config string |
| `ariadne.capabilities.causal.ports.content_ref.ContentReferencePort` | App-facing `verify` Protocol | P01 `ContentRef` is lexical only |
| `ariadne.interfaces.cli.local_causal.content_io.LocalContentReferenceAdapter` | exact-byte FD verification and TOCTOU/root confinement | Application never imports CLI adapter |
| `ariadne.capabilities.causal.ports.local_io.LocalPublicationPort` | `begin/seal/publish` App facade | One Concrete publication algorithm |
| `ariadne.interfaces.cli.local_causal.publication.LocalArtifactPublisher` | run-scoped immutable staging/publish state machine | Does not implement scientific estimators |
| `ariadne.capabilities.causal.ports.local_io.LocalManifestReaderPort` and `ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader` | independent marker->manifest->artifacts verification | Product `ArtifactStorePort` and legacy `CliManifest(2.0)` unchanged |

P02 receives P01's strict Codec and Manifest DTO. P03/P04 are not prerequisites: exercise publication with valid *synthetic* typed Graph/Status bytes, never label synthetic bytes a scientific PAG PASS.

## 4. Explicitly out of scope
他GateのMethod実装、旧Product v2変更、根拠なしのScience PASS、行出力自己許可、未承認ACL/mount、既存run上書き、Package外の便乗変更。

## 5. Entry criteria / required evidence
Gate 06/07のFreeze・Coding Authorization・固定branch HEAD確認。Depends on P01の実装checkpoint full SHAとfocused検証を確認。矛盾/依存未成立はBLOCKED。

dependency checkpoint / source state等はfactとして外部参照してよい。Entry rule自体は本書内に記載する。

## 6. Required implementation — security and transaction contracts

### 6.1. Trusted local OS capability (30_60 §10 / 23_41 §4 / REF02–04, PRIV03/04/06)

**Types:** `ariadne.shared.local_fs.TrustedLocalRoot` and `LocalPrincipal` must represent the effective OS subject and verified root-dirfd/owner/ACL/mount information, not an arbitrary Path or caller self-assertion. CLI composition root owns factory and OS verification; `LocalRunContext` later consumes these verified capabilities.

**Factory preconditions:** local Linux target only; reject root outside explicitly authorized base, symlink in any component, unsafe owner/effective UID, unexpected delegation, ACL exposure, shared/CI/container-root visibility or unknown mount property. A mode `0700` alone is not proof of private mount. Keep dirfd for subsequent open/rename, recheck safe identity at publication boundary; no Product ProjectMembership emulation.

**Secure operations:** Open each relative path under verified dirfd with `openat2` (restricted resolution) or correct component-by-component `openat/O_NOFOLLOW` equivalent. Validate regular-file type, mount/owner and opened-FD identity. Reject traversal, symlink changes, hardlink-based unexpected exposure and path replacement. A lexical check is insufficient. Never materialize an absolute untrusted path and reopen by name.

### 6.2. `ContentReferencePort.verify` and `LocalContentReferenceAdapter` (30_60 §10 / REF01–04)

**App Port module:** `ariadne.capabilities.causal.ports.content_ref.ContentReferencePort`; **CLI Concrete:** `ariadne.interfaces.cli.local_causal.content_io.LocalContentReferenceAdapter`. Public signature:

~~~python
def verify(self, ref: ContentRef, *, root: TrustedLocalRoot) -> VerifiedContent: ...
~~~

No Port mutable Instance Fields. Concrete receives verified root on each call; no raw path passed from Application to CLI. Open the referenced regular file safely, read/hash the **same FD** and compare exact bytes, size, content digest and safe metadata with declared `ContentRef`. A same-identity but modified blob fails; a cached validated result cannot bypass per-open consistency. Close FD on all paths. Verify MIME/schema meaning separately in P01/P05.

**Failure:** invalid root/owner/ACL/mount, symlink/hardlink/race, non-regular file, changed inode or actual bytes/hash/size mismatch, missing file, unreadable data -> typed INPUT/SECURITY (CLI exit3), never SCI negative. No I/O writes. Stale verification is not authorization to write outputs.

### 6.3. Application Port facade (30_62 §8.2 / PUB01–10, READ01–07)

~~~python
# ariadne.capabilities.causal.ports.local_io
def begin(self, *, run_id: str, request_hash: str, root: TrustedLocalRoot) -> StagingArtifactSink: ...
def seal(self, *, sink: StagingArtifactSink, manifest: LocalRunManifest, privacy: PrivacyDecision) -> ValidatedStagedBundle: ...
def publish(self, *, bundle: ValidatedStagedBundle, root: TrustedLocalRoot) -> CommittedLocalRun: ...
def verify(self, *, root: TrustedLocalRoot, run_id: RunId) -> VerifiedLocalRun: ... # Reader Port
~~~

Publisher facade creates/binds **one** run-scoped `LocalArtifactPublisher` to `StagingArtifactSink`; `seal` delegates to its `validate` and `publish` to its `commit`. Do not implement a second staging/commit transaction inside the facade. Scientific code sees only `StagingArtifactSink` Protocol (`ariadne.scientific.ports.artifacts`) and never receives final `runs/` path or CLI Concrete type. Reader Port delegates to `LocalManifestReader.read_run`. Runtime type/ownership of sink and bundle must match same run_id, request_hash and root; cross-run substitution rejects.

### 6.4. `LocalArtifactPublisher` (30_62 §3 / PUB01–10)

**Module:** `ariadne.interfaces.cli.local_causal.publication`. A publisher instance is **run-scoped**, unlike stateless Reader.

| Instance Field | Type | Constraint |
| --- | --- | --- |
| `root` | `TrustedLocalRoot` | Immutable verified root capability |
| `run_id` | `str` | Safe ID, no slash/./.. |
| `request_hash` | `str` | 64 lowercase SHA256 of typed Study JCS |
| `state` | `PublishState` | only valid transition table below |
| `staging_handle` | `StagingHandle|None` | owned FD; released on all outcomes |
| `artifacts` | `tuple[ArtifactDescriptor,...]` | append/stage before seal only |
| `permission_policy` | `LocalPrivacyPolicy` | injected Policy evaluator; actual allow decision on call |

**Constructor:** `__init__(self, root: TrustedLocalRoot, run_id: str, request_hash: str, permission_policy: LocalPrivacyPolicy)`. No final directory creation; verify root, ID/hash and caller actor before begin. Immutable inputs cannot be changed after construct.

| Concrete Method | Return | Precondition -> operation -> Postcondition |
| --- | --- | --- |
| `begin(self)` | `StagingArtifactSink` | PREPARING; secure mkdir `root/.staging/{random-token}` 0700 and open dirfd; -> STAGING |
| `stage_bytes(self, key: RelativeArtifactKey, data: bytes, media_type: str, classification: PrivacyClass)` | `ArtifactDescriptor` | STAGING only; unique safe key, private 0600, same-FD exact hash/size; no forbidden row/secret; append inventory |
| `validate(self, manifest: LocalRunManifest)` | `ValidatedBundle` | STAGING -> VALIDATING; confirm all real artifact bytes/schema/Privacy/lineage, write strict Manifest and marker (marker not in Inventory), fsync files+dirs; produce sealed immutable run-scoped bundle |
| `commit(self, validated: ValidatedBundle)` | `CommittedRunRef` | VALIDATING; recheck root/FS; no-clobber rename -> durable parent fsync -> independent full Reader readback; **only then** COMMITTED |
| `abort(self, reason: str)` | `None` | Before rename only; detach/quarantine uncommitted staging and close handles, -> ABORTED; never remove an indeterminate published run |

**State machine:** `PREPARING -> STAGING -> VALIDATING -> PUBLISHING -> COMMITTED`; `ABORTED` only before any publication can have happened, and `INDETERMINATE` after rename may have happened but durable/readback proof absent. Invalid transitions, double begin, stage after seal or commit twice are typed failures. Never imply exactly-once scientific computation.

**Commit algorithm:**
1. Validate all artifact inventory keys/bytes/hashes and Operation Bundle (DISCOVER Graph success versus diagnostics negative); Manifest is valid strict JCS, `manifest.json` and marker remain outside artifact Inventory.
2. fsync every staged file and directory and all created staging ancestor dirs; marker `_COMMITTED.json` binds exact bytes hash of completed `manifest.json`.
3. Check real same-filesystem support and call Linux `renameat2(RENAME_NOREPLACE)` for directory `.staging/{token} -> runs/{run_id}`, no check-then-rename or ordinary `Path.rename()` substitution. Process or filesystem lock alone is not a substitute.
4. fsync both affected parent directories (`.staging` and `runs`); independently reopen committed path and read Marker→Manifest→all Artifact bytes.
5. Return `COMMITTED` only after independent `VerifiedLocalRun`; before that, no result with `technical_status=COMPLETED`. No unconditional post-rename cleanup.

**Race/indeterminate:** On `EEXIST`, never overwrite; read back existing run and reuse only if request hash **and every artifact/manifest/privacy invariant** match. Different request hash -> `RUN_ID_CONFLICT`. Unsupported syscall/FS (ENOSYS/EINVAL/EOPNOTSUPP/EXDEV) -> typed failure, not fallback. Rename success but fsync/readback fault or indeterminate syscall outcome -> `PUBLICATION_INDETERMINATE`, no deletion, second rename, auto-repair or false COMMITTED. If uncommitted pre-rename failure, `abort` may isolate staging safely.

### 6.5. `LocalManifestReader` (30_62 §5 / READ01–07)

**Module:** `ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader`. Stateless: **no required Instance Fields**, `__init__()`, caller supplies verified root per invocation.

~~~python
def read_run(self, trusted_root: TrustedLocalRoot, run_id: RunId) -> VerifiedLocalRun: ...
# Public Port
def verify(self, *, root: TrustedLocalRoot, run_id: RunId) -> VerifiedLocalRun: ...
~~~

**Readback sequence:** (1) secure run directory open under verified Root and effective principal; (2) require `_COMMITTED.json` and validate `e11-commit/1`, run ID and request hash; (3) open exact `manifest.json` safely, compare SHA256 of same FD bytes to marker; (4) strict `LocalRunManifest.from_payload` and Codec/version checks; (5) unique safe Inventory keys, real size/SHA/MIME/classification/visibility, upstream lineage, Method, Study/Status/Graph cross-schema agreement and Privacy; (6) only then return immutable `VerifiedLocalRun`. No inference of committed state from marker existence alone.

Never return private row bytes without independent authorization; default G01 is aggregate-only. Corrupt, partial, legacy, versionless or unsafe ACL/symlink/mount runs -> typed error (`NOT_COMMITTED`, `MANIFEST_HASH_MISMATCH`, `ARTIFACT_HASH_MISMATCH`, `VERSION_UNSUPPORTED`, `PRIVATE_ARTIFACT_DENIED`); **published** readback failure maps to phase PUBLICATION / CLI exit5. Reader cannot mutate, repair or delete a run.

### 6.6. Error and ownership matrix

| Failure stage | Error class / exit when used by CLI | Mandatory safety result |
| --- | --- | --- |
| Ref/root open | unsafe path, ownership, digest, race -> INPUT/SECURITY, exit3 | no root-outside read/write |
| Staging before rename | permission, ENOSPC, schema, fsync -> PUBLICATION, exit5 | no final marker; safe pre-rename abort |
| No-clobber conflict | `RUN_ID_CONFLICT` or same-hash verified reuse, exit5 unless reuse | overwritten final run count = 0 |
| After possible rename | `PUBLICATION_INDETERMINATE` / exit5 | false COMMITTED count = 0; no deletion |
| Published Reader | hash/marker/version/ACL bad -> PUBLICATION, exit5 | no VerifiedLocalRun, no auto-repair |

P02 never claims scientific accuracy from a well-formed Graph file. P01 owns canonical bytes/DTO; P03 owns Graph semantics; P04 scientific Oracle; P05 integrates UseCase and actual Privacy eligibility. Preserve Product `ArtifactStorePort` and legacy `CliManifest(2.0)` contracts.

## 7. Focused verification — real Linux and fault injection

| DD / 07 | Focused file | Required evidence |
| --- | --- | --- |
| REF01–04, PRIV03/04/06; 07-02 | `component/test_g01_bundle_reader.py` plus `integration/test_g01_atomic_publication.py` | actual FD bytes, symlink/hardlink/race/owner/ACL/mount negatives, no root escape |
| PUB01–04; 07-05 | `integration/test_g01_atomic_publication.py` | ENOSPC, marker before/after, crash/kill around rename/fsync; zero false COMMITTED |
| PUB05–09; 07-05 | same integration file | two-process same/different request hash, syscall unsupported, no-clobber 0 overwrite, real dir fsync/readback |
| READ01–07, MAN03–06; 07-06 | `component/test_g01_bundle_reader.py` | marker->manifest->artifact cross-ref, corrupt bytes/size/version, privacy denial; only verified result |

~~~bash
uv run --no-sync python -m pytest tests/enhancement/enh_e11/g01/component/test_g01_bundle_reader.py -q
uv run --no-sync python -m pytest tests/enhancement/enh_e11/g01/integration/test_g01_atomic_publication.py -q
~~~

Tests must assert real syscall path on supported Linux private temp FS, not just monkeypatched methods; environment/FS unavailable -> BLOCKED, never "atomic PASS" from an in-memory mock. Fault injection must not touch real user/Project output. Evidence per DD ID: source/fixture/env SHA, actual syscall/exit and expected result. P02 COMPLETE needs verified no-clobber, fully checked Reader and negative failure cases; Gate-wide real scientific validity is P04/07, not a P02 assertion.

## 8. Protected contract / Transition Debt constraints
Product v2の既存CLI/Manifest/Result contractを回帰保護する。未完成のGraph/Science/個票認可を完成と見なさない。PREPARATION-03の技術判定はG01単一Gate維持（Owner承認待ち）。P02のOS/FS Publication、P04の独立FCI/PAG Science、P05のCLI統合・Privacy/旧v2回帰は別々の必須受入軸であり、全軸が同じFixed Candidate SHAで実証されるまでG01_999 PASS不可。OwnerのGate境界承認・06/07 Freeze/Coding AuthorizationまではPxx着手禁止。

## 9. Checkpoint / reporting rule

Package completion時:

1. implementation-affecting changeをcommitする。
2. implementation checkpoint full SHAを固定する。
3. `implementation_checkpoint_report`を作成する。
4. `*_in_progress.md`へexecution statusを記録する。
5. report-only commitが別ならcheckpoint SHAと区別する。

## 10. Package completion criteria — Definition of Done

- [ ] `TrustedLocalRoot` factory and `LocalContentReferenceAdapter.verify` preserve effective root/principal, same-FD actual bytes and error classification; REF02/03 physical race/TOCTOU cases exercised.
- [ ] `LocalPublicationPort.begin/seal/publish` wraps exactly one run-scoped `LocalArtifactPublisher`; method signatures, field/state transitions, ownership, abort-before-rename restriction implemented.
- [ ] Real local Linux `renameat2(RENAME_NOREPLACE)`, staged and parent fsync, marker/Manifest inventory/hash rules, concurrency and post-rename indeterminate behavior verified on supported private FS; overwrite and false COMMITTED counts zero.
- [ ] Stateless `LocalManifestReader.read_run` and public `verify` reject corrupt marker/manifest/artifacts, unsafe root and legacy v2; only independent complete readback yields `VerifiedLocalRun`.
- [ ] Tests in `component/test_g01_bundle_reader.py` and `integration/test_g01_atomic_publication.py` executed for P02 DD IDs; unsupported/unavailable required FS evidence -> PACKAGE_BLOCKED rather than mock-only PASS.
- [ ] No Product `ArtifactStorePort`/old CLI behavioral changes. Full SHA, fixture/env/real syscall results, report, and checkpoint recorded. No FCI/PAG scientific PASS claimed.

## 11. External reference policy

source / previous checkpoint / test output / provenanceは外部参照してよい。本書のimplementation rule、prohibited scope、completion criterionをParent 06 / P00へ委譲してはならない。

## 12. Stop rule

- package scope完了 -> `PACKAGE_COMPLETE`
- continuation不能 -> `PACKAGE_BLOCKED`
- Gate PASS / FAILは判定しない。
- next packageへ勝手に先行しない。
