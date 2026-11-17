# PREP-02 F03/F05/F06 — Shared Architecture Acceptance Matrix

- Date: 2026-11-17 JST
- Type: PREP-02 execution contract / review input; not stock, not test evidence, not independent review
- Authority: [DEC-PREP02 A/A/A](decisions/94_20261117_dec_prep02_owner_architecture_choices.md)
- Baseline before Owner decision: `584fa9e7a709522c73b08ed911cabb71ccdb7684`
- Status: `OWNER_POLICY_ADOPTED / MECHANICAL_CONTRACT_DRAFT / TESTS_NOT_RUN / INDEPENDENT_REVIEW_NOT_RUN`

## 1. Common architecture verification matrix

| AC | Finding | Input / setup | Required observation | Rejection / negative oracle | Proof to collect | Freeze condition |
|---|---|---|---|---|---|---|
| ARCH-F03-01 | F03 | Single local trusted FS, distinct run_id | One immutable fully readable run directory with valid marker→Manifest→artifact hashes | No missing/partial artifact accepted | immutable bundle fixture + readback report | Exact publish/reader Port signatures and JSON Schema |
| ARCH-F03-02 | F03 | Two independent processes race for same run_id, different payload | One winner; other conflict, no replacement or mixed bundle | Either overwritten winner, duplicate success with different payload | multiprocess barrier-driven tests, directory hashes | no-replace primitive/errno handling specified |
| ARCH-F03-03 | F03 | Same request hash, same id retry | reuse **only** after complete readback match | hash-only or path-only equality insufficient | repeat-test and corrupted preexisting bundle | idempotent replay semantic defined |
| ARCH-F03-04 | F03 | Filesystem without verified no-replace semantics, cross-device, unsupported kernel | fail-closed, no run published | silent fallback to check-then-rename or ordinary replace | FS/ABI probe, EXDEV/ENOSYS/EINVAL/ENOTSUP fault cases | supported FS matrix and error taxonomy fixed |
| ARCH-F03-05 | F03 | crash/failure at each stage: file write/hash/fsync; marker/manifest; staging readback; rename; parent fsync | no partial run ever accepted; post-rename recovery validates marker/hashes | staging or corrupt run reported committed; unsupported durability claim | injected fault matrix, post-crash reader outcome | durability boundary/correct recovery semantics specified |
| ARCH-F03-06 | F03 | symlink inserted at intermediate path component, race to replacement | root confinement using verified dirfd safe traversal | escape, TOCTOU, unsafe chmod/open | path race and O_NOFOLLOW/dirfd tests | exact platform security/open APIs fixed |
| ARCH-F05-01 | F05 | default execution without export flag | no row-level file, console, stderr, log or exception data | any individual row value leaked | synthetic sentinel-row test | concrete artifact classification/redaction policy |
| ARCH-F05-02 | F05 | flag=true but Study policy=false (and opposite), UID mismatch | deny row export for each missing condition | flag alone/Study alone/owner mismatch authorizes | truth-table unit + filesystem integration results | privacy evaluator and denied reason codes frozen |
| ARCH-F05-03 | F05 | shared writable/readable mounts, ACL exception, delegated principals, container root, CI volumes, unverifiable mount ownership | reject initial release path | owner UID equality alone assumed sufficient | OS effective UID+mount+ACL introspection logs, reject fixtures | what counts as verified private root defined and reviewed |
| ARCH-F05-04 | F05 | allowed row export in private root | 0700 directories, 0600 files, allowed columns, row cap, no leaks | unauthorized columns/permissions, unbounded rows | stat/ACL + Parquet schema and leak scan | Study authorization provenance and audit schema |
| ARCH-F06-01 | F06 | valid study/graph/effect/manifest/status each declared version | exact tagged-schema dispatch and roundtrip | unknown extra discriminator, missing version, mismatched payload | machine-readable JSON Schema + positive fixtures | formal schema/enum registry fixed |
| ARCH-F06-02 | F06 | unknown version, older E11 version, legacy `causal-analysis-spec/2` / old `CliManifest` | strict E11 rejection; legacy reader independently retains behavior | implicit upgrade/cross-lane interpretation | negative version vectors + Product v2 regression | dispatch table and compatibility tests frozen |
| ARCH-F06-03 | F06/F07 | AR non-finite/disconnected/all-real, null CI with typed reason | lossless roundtrip, tagged infinity, separate science axes | JSON NaN/Infinity number, invented CI, silently finite interval | serialization/property tests + reference checks | typed intervals/null rules as valid JSON Schema |

## 2. Evidence provenance and decision constraints

1. For every executed case, record exact commit, lock SHA, Python/kernel/OS/filesystem/mount type, effective UID and ownership, test runner, fixture/reference hash, execution date and actual observation. Evidence is not to be inferred from documentation.
2. A **unit or static schema test alone** cannot establish Linux filesystem atomicity or private-mount safety. Real multiprocess/FS probe and negative test evidence must be separate.
3. Acceptance of a **design proposal** and **runtime PASS** are distinct. Pre-Coding review can approve implementation-ready contracts, but it cannot assert functionality implemented or tested when absent.
4. Each failing/unavailable scientific inference produces typed negative state, not a successful CI. Method41 scientific thresholds remain Gate-specific; this common matrix is not their substitute.
5. No action here authorizes modifications to Product Web/API/DB/Worker or old reader; no canonical requirement_definition promotion.

## 3. Remaining deliverables and dependencies

| Deliverable | Owner | Required before | Current state |
|---|---|---|---|
| F03 Publisher/Reader Protocol signatures, errno/FS strategy, crash recovery ADR | Architecture author | shared Port Freeze / initial Coding | OPEN |
| F05 principal/ACL/mount threat model and authorization policy wire types | Security/Architecture author | shared Security Freeze / initial Coding | OPEN |
| F06 five machine-readable JSON Schemas, version/dispatch table and typed error registry | Schema owner | shared Schema Freeze / initial Coding | OPEN |
| F04 Product/Local bridge with regression scope and F07 AR/CI schema | Architecture/Science | shared Port/Schema Freeze | OPEN |
| Independently written finding-by-finding Architecture reviewer verdict | Independent reviewer | initial Coding Authorization | NOT_RUN |
| All required actual FS/Security/schema negative tests | Implementation/verification Gate | appropriate Gate's 07 acceptance | NOT_RUN |

**Note:** Per-Method scientific tests and five dependency execution profiles are tracked separately; none are waived by this matrix.


## 4. DEC-PREP02-D acceptance delta（2026-11-17）

- **F07 AR EMPTY**: Schema `EMPTY/components=[]`を受理、非EMPTY空成分・EMPTY非空成分は拒否。`AVAILABLE + EMPTY + valid inversion_evidence`は正常な数学的集合結果。`FAILED`は`confidence_set=null`とreason必須。該当just-identified B0/B1 MethodはEMPTYを科学的不整合として検出する。
- **F05 Policy**: 自己生成Study YAMLの`row_export_authorized:true`や自己発行`policy_ref`のみではDENY。事前承認済み別AuthorityとStudy/Scope/列/行数を照合、root条件をAND、拒否なら**CLI exit3**・row bytes未作成・stdout/stderr/log未露出。
- **F06 Codec**: Product `hash_mapping(default=str)`利用は禁止。E11 typed JSONのRFC8785 JCS候補、UTF-16 keys/Unicode非正規化/ECMAScript float、SHA256 bytesのgolden fixturesをPython/ECMAScript独立実装で検証。
- **F06 CLI**: security/privacy denial=3とconfig/schema=2を正例・負例で区別。Old CLI v2は変更なし。

[Owner決定](decisions/95_20261117_dec_prep02_four_owner_choices.md)。**Tests not executed**。判断の採用を受入試験PASSとして扱わない。
