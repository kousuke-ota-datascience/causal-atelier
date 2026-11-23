# 196 — G01/P02 PrivacyDecision RD/LDD/BD/IF/DD/06/07 cross-layer parity audit

**Date:** 2026-11-23 JST  
**Amendment:** AMD-E11-G01-P02-001  
**Status:** AUTHOR_DOCUMENT_CROSS_LAYER_RECONCILED / OWNER_09_S10_S11_PENDING  
**Prior frozen G01-S10:** bcc1d797e1406e8816d12b725eeace07a181c702  
**Observed P02 START_SHA:** 4248ca24204ed8ede27527191b1a53d9ced1ff5a  
**Existing P01 PACKAGE_READY checkpoint:** 9bff61f0eae25236f95f31f2cd3e7c81291f0167  
**Changed doc source commit prior to audit:** 535fb43ca46f1df4f9845798f6775d873517a4a7

## 1. Audit question and common invariant

For the approved G01 DISCOVER aggregate-only lane, a privacy decision must bind *the validated Study, run, request hash, live trusted root dirfd, effective actor, allowed aggregate output class and all actual staged artifacts*. The P05 initial allow does not authorize final publication; the P02 Publisher must reauthorize from the exact staged bytes/real FD and re-evaluate injected stateless Policy. Mismatch denies before Marker/rename; commit rechecks root/UID/inventory, independent Reader reopens final bundle. G01 row-level Parquet is always denied. No public JSON field or second signature authority.

## 2. Layer-by-layer trace and ownership

| Layer | Revised normative files | Authority and precise constraint | Link to G01 06/07 |
| --- | --- | --- | --- |
| Requirement | 10_21 NFR-030; 10_22 NFR-031; 10_91 AC | No unapproved partial/successful published run; privacy decision must bind actual request, root, actor and output | G01-07-05/06/11, PUB/PRIV |
| Logical data | 21_23; 21_40 | Transient immutable PrivacyDecision internal value, verified root FD identity; consistency joins, **not** a Product DB entity | G01 P02 §6.3 decision fields and integrity |
| Basic design | 22_09; 22_12 | P05 initial decision versus P02 pre-seal final authority; deny stale/cross-root/row | P05 run step3/8; P02 seal |
| Interface | 23_41; 23_42 | Public Port seal(sink,manifest,privacy) unchanged; Concrete validate(manifest,*,privacy), no new public wire fields | P02 §6.3/6.4; P05 06 |
| Detailed design | 30_62 | Single run-scoped publisher, exact staged Study/Manifest/Inventory + root/UID/policy comparison before Marker/rename | PUB04/07; G01-07-05/06 |
| Coding WHAT | G01 06 P02/P05 | Exact decision binding, initial authorize, forwarding, publisher reauthorization, invalid-case rejection | Scoped P02 implementation after new approval |
| Independent test WHAT | G01 07 | Positive same-run aggregate + negative wrong run/hash/root/actor/artifacts/deny, actual Linux FD/Reader separately | 07-05/06/11 and G01_999 |

## 3. Semantic consistency checklist (Author document inspection, not executable evidence)

- **Policy evaluator:** Single stateless concrete LocalPrivacyPolicy; no signer/Policy Anchor; Publisher does not trust caller's allowed flag.
- **Decision time:** initial P05 before staging, final Publisher at seal against real inventory, again identity at commit; no imaginary pre-stage Graph digest requirement.
- **Scope:** same run_id, JCS Study request hash, live TrustedRoot FD identity (dev/inode/owner/mode/local FS), effective UID, aggregate-only declared output class. All actual six-field descriptors checked at seal.
- **Failure state:** pre-rename refusal does not create a completed Marker/run; no false science-negative or completed state; post-rename uncertainty remains INDETERMINATE with no deletion.
- **Data persistence:** in-memory PrivacyDecision is not serialized in Study/Status/Manifest or Product DB; public JSON/Port version and Artifact descriptor unchanged.
- **Backward compatibility:** Product v2/RBAC unchanged; P01 checkpoint and existing 76 developer tests preserved; other Gates not authorized.
- **Evidence:** No actual P02 Linux FD/FS/Reader test, independent G01 07/S09 or G01_999 PASS was performed by this review.

## 4. Impact decision and remaining authority

This amendment elaborates pre-existing NFR-030/031 rather than introducing another FR/NFR ID. Changed stock document categories reflect enduring contract knowledge; enhancement-specific audit and 09 remain in control-plane records. The selected source will require a **new full immutable Git SHA** after this audit and trace update. **Owner must separately authorize formal 09 AMD-E11-G01-P02-001 and new provisional S10**, then independently the new limited G01-S11. Old 190/191/193 were for earlier P02 WHAT only.

P02 Trial01 may continue after these decisions using intact P01 checkpoint 9bff61f0eae25236f95f31f2cd3e7c81291f0167, actual clean-tree and lock/Trial preflight; no P01 rerun or formal 08 remediation is implied.
