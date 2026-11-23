# 198 — G01/P02 AMD-E11-G01-P02-001 formal 09 Owner approval

**Date:** 2026-11-23 JST  
**Decision:** `DEC-G01-P02-REBASELINE-01 / FORMAL_09_APPROVAL = APPROVED`  
**Owner instruction (verbatim):** 「DEC-G01-P02-REBASELINE-01を承認する。AMD-E11-G01-P02-001の正式09契約変更を承認し、Git SHA 6df4b94de72a6ec8619f315e55ba7821e1eb157c を改訂後の暫定G01-S10として再Freezeせよ。P01チェックポイント9bff61f0eae25236f95f31f2cd3e7c81291f0167は維持する。」  
**Amendment:** `AMD-E11-G01-P02-001` / `CONTRACT_DEFECT`  
**Approved exact normative source SHA:** `6df4b94de72a6ec8619f315e55ba7821e1eb157c`  
**Previous S10:** `bcc1d797e1406e8816d12b725eeace07a181c702` (superseded for current P02 WHAT)  
**P01 existing PACKAGE_READY checkpoint preserved:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**Frozen uv.lock Git blob:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`  
**Repository/branch:** `kousuke-ota-datascience/causal-atelier` / `feature/ariadne_mvp_e11`

## 1. Approved formal 09 scope

The Owner formally approves the **actual amended contract** under `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P02-001_Gate_Contract_Amendment.md`, with its change impact record `195`, seven-layer parity audit `196`, and P01 historical implementation reverse-alignment audit `197`, all as of the exact frozen source SHA above.

The amendment closes the ambiguity between `LocalPublicationPort.seal(*,sink,manifest,privacy)` and Concrete `LocalArtifactPublisher.validate(manifest,*,privacy)`. The decision is passed to the **same sink-owned publisher**. Publisher independently validates staged exact Study bytes and strict JCS request digest, same run ID/request hash/live verified TrustedRoot FD identity/effective UID, exact staged Artifact inventory and current injected stateless LocalPrivacyPolicy; a caller-supplied `allowed=True` is not authority. Denied, absent, forged, stale, cross-run/root/UID, disagreed policy or forbidden row output must fail closed before Manifest/Marker seal and rename; root/UID/inventory checks repeat before commit and Reader checks final bytes.

Public Port/Study/Status/Manifest wire and ArtifactDescriptor fields remain unchanged. Initial G01 aggregate-only never permits row output. No new signer, persistent Policy or Product v2 changes.

## 2. Reconciled document hierarchy, preservation and evidence boundary

The reviewed baseline includes: Requirement `10_17/10_20/10_21/10_22/10_91`; LDD `21_23/21_25/21_40`; BD `22_06/22_09/22_12/22_15`; IF `23_41/23_42`; DD `30_62`; G01 06 P02/P05 and 07; formal AMD-001, AMD-002 and this AMD P02-001 in their respective historical states. P01 coding-06 and DD 30_60/30_62 were used as post-implementation technical authority **only for the bounded P01 upstream documentation exception** recorded in 197; prior FR/NFR MUST/AC grades were not relaxed.

Git comparison confirmed P01 checkpoint SHA is ancestor of approved source SHA, and no `src/`, `tests/`, `pyproject.toml` or `uv.lock` changes occurred **after** that P01 checkpoint. The actual P01 Package report records `PACKAGE_READY` / 76 developer tests; independent G01 tests and real P02 Linux filesystem work are **not** thereby considered complete. This approval neither rewrites nor reruns the checkpoint. P02 has no checkpoint.

## 3. Sequential authority boundary

1. `198`: **formal 09 AMD-E11-G01-P02-001 Owner approval**, recorded here.
2. `199`: separately record the explicitly Owner-approved **revised provisional G01-S10 reFreeze**, anchored at `6df4b94de72a6ec8619f315e55ba7821e1eb157c`.
3. **New independent limited G01-S11 Coding Authorization**: **NOT APPROVED** by `DEC-G01-P02-REBASELINE-01`. Must be requested separately and recorded before any resumed P02 implementation. Previous 193 applies to old S10 and cannot authorize the amended P02 contract.

Three layers of approval must not be conflated. This administrative record does not move the frozen normative source SHA. Current Trial remains 01 absent actual formal Gate FAIL/08; the prior P02 stop remains `BLOCKED_CODING_AUTHORIZATION`, not Package FAIL.

## 4. Unwaived tests and safety

Real P02 Linux root FD/atomic no-replace/fsync/Reader, PrivacyDecision cross-run/root/UID/mutated inventory and policy re-evaluation negatives, downstream P03/P04/P05 work, independent G01 S09/B02–B05/T2/T3/07 and Gate999, plus Product v2 regressions remain mandatory at their own defined points. No assumption of their PASS or scientific negative proof. No other Gates or release authorized.
