# 207 — AMD-E11-G01-P02-002 revised provisional G01-S10 Owner reFreeze

**Date:** 2026-11-23 JST  
**Decision:** `DEC-G01-P02-002-S10-REFREEZE-01`  
**Decision status:** `OWNER_APPROVED / REVISED_PROVISIONAL_G01_S10_FROZEN`  
**Verbatim Owner instruction:** 「DEC-G01-P02-002-S10-REFREEZE-01を承認する。AMD-E11-G01-P02-002を反映した完全Git SHA 0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492 を改訂後の暫定G01-S10として再Freezeせよ。P01チェックポイント9bff61f0eae25236f95f31f2cd3e7c81291f0167を維持し、独立検証とG01_999の受入条件は変更しない。」  
**Frozen immutable full Git SHA (normative WHAT):** `0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492`  
**Prior frozen G01-S10:** `6df4b94de72a6ec8619f315e55ba7821e1eb157c` (superseded for changed P02 WHAT)  
**Previous formal 09 prerequisite:** `combined_review/205_20261123_g01_p02_002_formal_09_owner_approved.md` (`AMD-E11-G01-P02-002`)  
**P01 PACKAGE_READY dependency checkpoint:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**uv.lock Git blob:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`  
**Repository:** `kousuke-ota-datascience/causal-atelier`  
**Branch:** `feature/ariadne_mvp_e11`

## 1. Frozen contract scope and rationale

Freeze `0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492` incorporates the minimal AMD-E11-G01-P02-002 correction: `PrivacyDecision` is a private immutable **value**, not issuer-authenticated proof. A separately instantiated value-identical decision is permitted if the sink-owned Publisher independently rechecks the real staged Study/JCS request hash, live TrustedRoot FD and EUID, exact inventory, and its trusted injected Policy returns allowed and equals the supplied decision field-by-field. Invalid/mismatched/denied/stale decisions and row artifacts still fail closed before Marker/rename. No cryptographic issuer, object identity test or new public wire value exists.

Normative revised source files included in this full SHA: requirements `10_22`, `10_91`; logical data `21_23`, `21_40`; basic design `22_09`, `22_12`; interfaces `23_41`, `23_42`; detailed design `30_62`; G01/P02 and P05 Coding `06`; G01 Test `07`; formal `09_AMD-E11-G01-P02-002`; author impact audit `204`; change Ledger `80`. No P01 implementation contract change, public JSON schema, Product v2, runtime code/tests/lockfile or G01 scientific-test relaxation is authorized.

The separate Owner formal 09 approval is recorded in `205`; this record **only** implements the subsequent explicit Owner **S10 reFreeze**. The chosen `0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492` is immutable and is not shifted by adding Owner administrative records `205/206/207` after that SHA.

## 2. Previous work and test evidence

P01 `9bff61f0eae25236f95f31f2cd3e7c81291f0167` remains an ancestor and PACKAGE_READY based on the historical developer report. No P02 source code/checkpoint or real Linux FD/atomic publish/Reader test was completed at the reported stop. The external Coding Agent separately reported 76 P01 focused/Product CLI tests passing; this is not independently re-executed by this change-management action. No formal Gate FAIL or 08 remediation; use Trial01 unless new evidence establishes otherwise.

## 3. Separate S11 authority barrier

**No new Coding Authorization is granted here.** Previous G01-S11 `combined_review/201` applies to prior frozen `6df4b94de72a6ec8619f315e55ba7821e1eb157c` and does **not** authorize changed AMD-002 P02 WHAT. A separate Owner approval of `DEC-G01-P02-002-S11-REAUTH-01` and a new limited S11 record referencing precisely `0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492` are required **before** P02/Trial01 coding restarts. Until then Coding Agent must report `BLOCKED_CODING_AUTHORIZATION` if asked to execute.

After new S11, live preflight must independently confirm correct repo/branch, clean worktree, frozen SHA ancestry, source diff limited to approved administrative documents, lock blob and actual file digest, existing P01 checkpoint and Trial state, and the complete approval sequence. Do not mistake the later HEAD for the immutable contract source.

## 4. Unwaived acceptance

Real P02 FS secure read/atomic no-clobber/stage/Marker/rename/readback, same-value positive and mismatched/denied decision negatives, downstream P03/P04/P05, actual Python/FCI/BK, independent MAG/PAG reference, B02–B05, T2/T3, G01 07/S09/999 and Product v2 regressions remain mandatory at their established authority boundaries. No science PASS, full Gate PASS or release is asserted by a provisional S10 freeze.
