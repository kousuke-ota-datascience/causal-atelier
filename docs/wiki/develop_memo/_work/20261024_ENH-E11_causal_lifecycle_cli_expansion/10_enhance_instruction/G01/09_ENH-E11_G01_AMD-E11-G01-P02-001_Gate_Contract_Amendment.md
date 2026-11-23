# AMD-E11-G01-P02-001 — P02 PrivacyDecision binding and authorization contract defect

**Document class:** Derived Contract / formal 09 amendment candidate  
**Type:** CONTRACT_DEFECT  
**Gate/Package/Trial:** G01/P02/Trial01  
**Status:** PROPOSED / OWNER_09_S10_S11_APPROVAL_PENDING  
**Date:** 2026-11-23 JST  
**Prior S10 freeze SHA:** bcc1d797e1406e8816d12b725eeace07a181c702  
**Agent P02 START_SHA:** 4248ca24204ed8ede27527191b1a53d9ced1ff5a  
**P01 PACKAGE_READY checkpoint:** 9bff61f0eae25236f95f31f2cd3e7c81291f0167  
**Normative content revision commit:** 4c2cc0a598281ab0deaa1b789268c9dda852d4f7  
**Frozen uv.lock Git blob:** 2b83110e86b26b7969fbddf8f98a727370ae19f7

## 1. Contract defect

P02 §6.3 defines public LocalPublicationPort.seal(sink,manifest,privacy:PrivacyDecision) whereas P02 §6.4 Concrete LocalArtifactPublisher.validate(manifest) omitted the decision and only described an injected LocalPrivacyPolicy. The prior contract did not define whether a mismatched caller decision or publisher policy has authority, how to bind it to a specific run/TrustedRoot/principal/artifact inventory, or what to do with a stale/denied/missing decision. The P02 agent correctly reported BLOCKED_CONTRACT_AMBIGUITY before implementation, with no P02 focused test, checkpoint or official P02 status.

## 2. Why 08 remediation is insufficient

No P02 implementation violation, fixed G01 Candidate, formal Gate999 FAIL or approved 08 exists. Primary WHAT must be corrected with formal 09, followed by revised G01 S10 and distinct S11. Keep Trial01 and the independent P01 ready checkpoint.

## 3. Before and after

| Area | Before | Revised normative contract |
| --- | --- | --- |
| Public Port | seal(sink,manifest,privacy) | Unchanged; forwards same decision to same sink-owned Publisher |
| Concrete | validate(manifest) | validate(manifest, *, privacy:PrivacyDecision), explicit typed value and reauthorization |
| Initial P05 decision | Authorize before stage, unclear binding | Immutable G01 decision allowed/run_id/request_hash/verified root-dirfd identity/principal_uid/AGGREGATE/row_export_requested=false/DISCOVER_AGGREGATE_ONLY |
| Binding | Caller allow not tied to resources | Publisher checks staged exact study.json JCS hash vs publisher/sink/Manifest/Decision, live TrustedRoot dirfd dev/inode/owner/mode/FS and current EUID, every actual staged Artifact descriptor/class/visibility |
| Authority | Injected policy interaction unspecified | P02 Publisher recomputes its own injected stateless Policy from validated staged Study, current root/principal and inventory-derived aggregate output class. Both recomputed allow and exact supplied-decision binding required; mere allowed=True never authority |
| Timing | No explicit conflict handling | Missing/denied/forged/stale/cross-run/root/UID or disallowed row artifact rejects before Manifest/Marker seal and rename; publish rechecks root/UID/inventory, Reader reopens final bytes |
| Science and wire | Potential implicit expansion | No new public schema/Policy signature or G01 row authority; true Graph-negative still requires independent P04 scientific justification and P02 Reader |

The decision is issued **before** staging and binds the allowed aggregate-only **class**, not an impossible prediction of Graph-vs-diagnostics byte hashes. Staged file actual membership is rechecked at seal, with fail-closed rejection for a changed/unauthorized output shape.

## 4. Acceptance criteria

G01 07-05/06/11 / PUB/PRIV: exact same-run allow positive plus negative cross-run/hash/root (including equal path text but different root FD), different EUID, false/unknown/missing Policy value, changed staged Study, extra restricted-row Artifact and policy reevaluation disagreement. All must deny before rename with no completed marker; actual Linux no-clobber/FD/readback testing remains mandatory. No AC weakened.

## 5. Protected scope and impact

Modified G01 P02/P05 06, G01 07, 23_41 Port IF and 30_62 Detailed Design. Not modified: P01 06, P03/P04 06, public schemas, P00 dependency order, source/tests/pyproject/uv.lock, other Gates or Product v2. P01 checkpoint 9bff61f0eae25236f95f31f2cd3e7c81291f0167 remains PACKAGE_READY; its reported 76 developer focused/regression PASS is not independent G01 acceptance.

## 6. Plan invalidation

Existing freeze bcc1d797e1406e8816d12b725eeace07a181c702 and prior S11 193 apply to **old** P02 WHAT, not revised source. P02 Trial01 blocked preimplementation, zero checkpoint. No reason to undo P01 checkpoint or increment Trial. No new G02–G10 permission.

## 7. Rebaseline

After recording this 09, impact review and ledger, use actual complete Git application SHA to review all changed blobs vs bcc1d797e1406e8816d12b725eeace07a181c702, unchanged lock and executable P01 checkpoint. Obtain explicit Owner formal 09 AMD-E11-G01-P02-001 approval plus new provisional G01-S10 at selected SHA. Obtain separate new limited G01-S11 approval thereafter. Only then actual P02 Agent preflight/implementation.

## 8. Trial

Continue G01/P02/Trial01 with P01 ready checkpoint 9bff61f0eae25236f95f31f2cd3e7c81291f0167, preserving actual prior Agent stop report. No 08 remediation without formal FAIL.

## 9. Approval

Owner instructed to correct required documents, not yet issued explicit authorization of **this exact amended 09 contract**, new S10 or new S11. Status remains OWNER_APPROVAL_PENDING. Independent S09/B02/B03/B04/B05/T2/T3/07/999 evidence remains pending.

## 10. Ledger

AMD-E11-G01-P02-001 tracked in 80_contract_amendment_log.md and Author impact record 195. The application SHA is actual Git write outcome, not a self-reference invented in this file.

## 11. Guardrails

Fail closed on decision mismatch; no caller-provided boolean as security, no row data in G01, no signed Policy extension, no scientific or FS PASS from a paper contract.


### Five-layer source-document reconciliation

The Owner requested that this amendment be reconciled across **requirements (NFR-030/031 and acceptance), logical data (21_23 transient PrivacyDecision; 21_40 integrity), basic design (22_09 publication; 22_12 local security), IF (23_41 Port/Decision; 23_42 bundle), detailed design (30_62 publisher), coding instructions (P02/P05 06) and test instruction (G01 07)**. The exact aligned source additions were committed at `535fb43ca46f1df4f9845798f6775d873517a4a7`; no original RD requirement ID, acceptance grade or Product v2 contract was changed. These are normative cross-layer *semantic* constraints, not identical repetitions or an added persistent Policy entity. An author reconciliation record is `combined_review/196_20261123_g01_p02_rd_ldd_bd_if_dd_06_07_parity_audit.md`. This 09 remains **PROPOSED / OWNER_APPROVAL_PENDING**; the earlier S10 `bcc1d797...` and S11 record193 do not authorize changed P02 WHAT.
