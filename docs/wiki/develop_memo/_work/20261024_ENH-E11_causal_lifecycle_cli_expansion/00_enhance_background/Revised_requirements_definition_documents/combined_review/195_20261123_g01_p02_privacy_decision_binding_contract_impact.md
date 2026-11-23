# 195 — G01/P02 Trial01 PrivacyDecision handoff contract impact review

**Status:** AUTHOR_IMPACT_REVIEW_COMPLETE / OWNER_09_S10_S11_PENDING  
**Date:** 2026-11-23 JST  
**Amendment:** AMD-E11-G01-P02-001  
**Observed agent stop:** BLOCKED_CONTRACT_AMBIGUITY at 4248ca24204ed8ede27527191b1a53d9ced1ff5a, no P02 implementation/checkpoint.

## Evidence

Reviewed frozen P02 §6.3 Port seal(sink,manifest,privacy) vs P02 §6.4 Concrete validate(manifest) and injected LocalPrivacyPolicy, P05 pre-stage authorize and subsequent seal, IF 23_41 Port signature, DD 30_62 class and G01 07 acceptance. Confirmed existing GitHub P01 status report PACKAGE_READY with checkpoint 9bff61f0eae25236f95f31f2cd3e7c81291f0167 and 76 reported developer focused/Product regressions. The new P02 contract adds exact internal binding and deny rules but does not independently test a real Linux FS.

## Reconciliation

P05 supplies immutable PrivacyDecision for same Study/run/hash/verified root FD/principal/aggregate-only output class. Facade seal passes it unchanged into same run-scoped Concrete validate(manifest, *, privacy). P02 independently rereads staged Study bytes, recomputes JCS request hash, checks live TrustedRoot and EUID, entire actual staged inventory and recomputed injected LocalPrivacyPolicy against supplied decision. Deny/mismatch/forgery/root or UID changes/row artifact rejection before Marker and rename. Publish rechecks live root/inventory and independent Reader still required. This avoids both trusting a bare caller bool and adding an unnecessary public schema, signer or G01 row right.

## Impact

| Contract | Status |
| --- | --- |
| G01 P02 06 | Changed: PrivacyDecision binding, concrete signature and negative cases |
| G01 P05 06 | Changed: initial decision binding and passthrough |
| Stock 23_41 / 30_62 | Changed: Port/Concrete consistency and reauthorization |
| G01 07 | Changed: precise security contract tests |
| P01 checkpoint 9bff61f0eae25236f95f31f2cd3e7c81291f0167 | Preserve; unchanged P01 source/WHAT, no replay automatically |
| P03/P04, P00, G02-G10, schema, uv.lock | Unchanged |

No scientific or Gate PASS, Python3.12 B02, real FS B03, effective Backend B04, independent MAG/PAG/BK B05/T2/T3, independent 07 or Product regression waiver claimed.

## Decision boundary

Formal 09 AMD-E11-G01-P02-001 Owner decision + new provisional S10 frozen full SHA, then a separate new S11 Coding Authorization. Prior S10 bcc1d797e1406e8816d12b725eeace07a181c702 and S11 record 193 do not cover changed P02 WHAT. Trial01 remains BLOCKED pre-coding; no P02 checkpoint.
