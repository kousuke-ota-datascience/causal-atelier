# 199 — Revised provisional G01-S10 Owner reFreeze after AMD-E11-G01-P02-001

**Date:** 2026-11-23 JST  
**Decision:** `DEC-G01-P02-REBASELINE-01 / G01_S10_REFREEZE = APPROVED`  
**Owner instruction:** 「DEC-G01-P02-REBASELINE-01を承認する。AMD-E11-G01-P02-001の正式09契約変更を承認し、Git SHA 6df4b94de72a6ec8619f315e55ba7821e1eb157c を改訂後の暫定G01-S10として再Freezeせよ。P01チェックポイント9bff61f0eae25236f95f31f2cd3e7c81291f0167は維持する。」  
**New frozen immutable full Git SHA:** `6df4b94de72a6ec8619f315e55ba7821e1eb157c`  
**Previous frozen full Git SHA:** `bcc1d797e1406e8816d12b725eeace07a181c702` (historical for earlier WHAT)  
**Formal 09 prerequisite:** `combined_review/198_20261123_g01_p02_formal_09_owner_approved.md`; prior approval commit `07e2343816e7f95c9e966e5483752d63fbfea37d`.  
**P01 checkpoint:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167` — `PACKAGE_READY`, preserved  
**Frozen uv.lock Git blob:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`  
**Repository/branch:** `kousuke-ota-datascience/causal-atelier` / `feature/ariadne_mvp_e11`  
**Required next Owner decision:** `DEC-G01-P02-S11-REAUTH-01` (PENDING).

## 1. Freeze identity and normative source scope

The frozen source `6df4b94de72a6ec8619f315e55ba7821e1eb157c` is a single immutable G01 S10 baseline that includes all revised **P02 PrivacyDecision binding** documents and the separately Owner-directed exceptional post-implementation P01 upper-layer reverse reconciliation:
- RD `10_17/10_20/10_21/10_22/10_91`
- LDD `21_23/21_25/21_40`
- BD `22_06/22_09/22_12/22_15`
- IF `23_41/23_42`
- DD `30_62` and reference `30_60`
- G01 coding 06 P01–P05, G01 test 07, formal AMD-E11-G01-P02-001 09 and review 195/196/197.

The Owner formal 09 approval record 198 recognizes the amendment despite the historical in-file `PROPOSED` text; retain that earlier text as an immutable description at the frozen Git SHA. This separate record defines **approved status** and **freeze provenance**. Any post-freeze Owner/admin records added to HEAD must not shift the approved immutable full SHA or introduce undocumented contract changes.

## 2. Exact package and implementation scope

G01 only, DISCOVER, P1-M06/causal-learn, normal Trial01 until actual formal FAIL/08 proves otherwise. P01 checkpoint `9bff61f0eae25236f95f31f2cd3e7c81291f0167` is historically PACKAGE_READY; do **not** redo, overwrite or invalidate without actual discrepancy. The next intended Package is **P02**, then P03/P04/P05 by P00 dependencies. Public ABI/JSON/ArtifactDescriptor and Product v2 are unchanged; source/tests and `uv.lock` after P01 checkpoint were not modified at freeze.

P02's public Port `seal(sink,manifest,privacy)` forwards the exact decision to the same sink-owned concrete `validate(manifest,*,privacy)`, and Publisher checks actual staged Study JCS bytes/run/hash, live root dirfd identity/UID, complete actual inventory and recomputed injected stateless Privacy Policy. Missing, denied, conflicting, stale, forged, cross-run/root/actor decisions and unauthorized row output deny before Marker/rename. Both actual Linux FS and independent Reader evidence remain required.

The revised S10 source is **not** itself proof of P02 correctness, a completed package, genuine scientific negative, or independent scientific acceptance.

## 3. Subsequent authority barrier

**No new S11 coding authorization is granted by this S10 reFreeze.** Historical S11 record 193 authorized earlier frozen WHAT only and cannot be used for amended P02. Before any resumed P02 code, obtain a distinct Owner decision `DEC-G01-P02-S11-REAUTH-01` and record approved new S11 bounded to `6df4b94de72a6ec8619f315e55ba7821e1eb157c`, P01 checkpoint and current branch. Until then Coding Agent must stop `BLOCKED_CODING_AUTHORIZATION`.

Once Owner issues new S11, actual Coding Agent preflight still must verify real worktree/branch/remote, actual START_SHA, clean state, pinned frozen commit reachability, HEAD/worktree `uv.lock` Git blob plus byte SHA-256, diff since frozen WHAT (approved admin only), Owner 198/199/new S11, normal Trial state and preserved P01 checkpoint. Do not demand moving HEAD equals immutable freeze; do not destroy user's files or old stop reports.

## 4. Unwaived acceptance

No changes to G01_999 independent S09, B02/03/04/05, T2/T3, independent 07, actual Python/secure OS FD/atomic no-clobber/readback, Method science, Product v2 regression and other Gate security/privacy obligations. No formal FAIL/08 has been shown. No G02–G10 or release is authorized.
