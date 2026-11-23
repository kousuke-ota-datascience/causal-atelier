# 208 — AMD-E11-G01-P02-002 limited revised G01-S11 Owner decision docket

**Date:** 2026-11-23 JST  
**Decision requested:** `DEC-G01-P02-002-S11-REAUTH-01`  
**Decision state:** `OWNER_APPROVAL_PENDING`  
**Formal 09:** `AMD-E11-G01-P02-002` Owner-approved in `205`  
**Revised provisional G01-S10:** Owner reFrozen at `0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492` in `207`  
**Previously approved S11:** `201` remains historical for previous frozen WHAT only  
**P01 checkpoint:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167` PACKAGE_READY, preserved  
**Intended next execution:** `GATE_ID=G01 PACKAGE_ID=P02 TRIAL_NO=01`

## 1. Proposed limited authorization

Authorize the bounded `G01/P01–P05` developer coding and verification scope already defined by P00, **starting next at P02/Trial01 only**; P01 is complete and must not be reimplemented absent newly evidenced defect and Owner change. Bind permission to immutable amended WHAT `0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492`, approved remote `kousuke-ota-datascience/causal-atelier`, working branch `feature/ariadne_mvp_e11`, and tracked `uv.lock` blob `2b83110e86b26b7969fbddf8f98a727370ae19f7`.

P02 implementation MUST follow frozen P02 06, relevant P05 06, G01 07 and five-layer RD/LDD/BD/IF/DD contracts, including exactly-value-identical PrivacyDecision acceptance conditional on Publisher's independently trusted allow, field mismatches/Policy denies before Marker and rename, verified root FD/UID/inventory and real Linux atomic FS/independent Reader. No issuer token/signature/nonce requirement, no implicit G01 row export, no Product v2/public schema drift.

## 2. Required runtime checks

Agent preflight must verify actual current HEAD, clean worktree, correct feature branch/remote and immutable `0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492` ancestry; new administrative-only records since freeze, real lock Git blob and file-byte SHA256, P01 ready checkpoint ancestry, P02 no existing checkpoint, Trial01 no formal FAIL/08, and all three records `205` / `207` / future new S11. Focused test results, actual Linux FS verification, no-clobber race/Reader and protected P01+Product regression must be recorded, not inferred.

## 3. Owner decision and unwaived criteria

**Pending:** Owner must explicitly approve `DEC-G01-P02-002-S11-REAUTH-01`. This docket is only a decision request and is not Coding Authorization. G01_999 scientific and FS independent acceptance, S09/B02–B05/T2/T3, and G02–G10 restrictions remain unchanged. If approved, create a **separate positive S11 record** followed by an updated P02 restart handoff.
