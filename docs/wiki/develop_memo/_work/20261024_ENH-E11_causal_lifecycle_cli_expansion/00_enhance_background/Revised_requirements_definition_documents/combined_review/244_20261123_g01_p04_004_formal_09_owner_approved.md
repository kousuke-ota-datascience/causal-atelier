# 244 — G01/P04 AMD-E11-G01-P04-004 formal 09 Owner approval

**Date:** 2026-11-23 JST  
**Decision ID:** `DEC-G01-P04-004-09-APPROVE-01`  
**State:** `FORMAL_09_OWNER_APPROVED / REVISED_S10_OWNER_APPROVAL_PENDING / REVISED_S11_REAUTH_PENDING`  
**Repository:** `kousuke-ota-datascience/causal-atelier`  
**Branch:** `feature/ariadne_mvp_e11`

## 1. Explicit Owner approval and approved immutable draft

Owner instructed:

> AMD-E11-G01-P04-004の正式09改訂案を承認する。DEC-G01-P04-PRODUCT-POLICY-SHARING-01=Bに基づき、G01/P04のLocal pure policy・Method Registryの実装範囲と、Product v2 ScientificValidationServiceへの接続をDEFERRED_PRODUCT_POLICY_BRIDGEとする設計・IF・06・07の改訂を正式契約として承認せよ。最終的な単一Authority・共通化要求とG01_999の未完了依存は維持する。Product v2コード、P01/P03チェックポイント、公開E11 Schema Version、既承認の科学的・独立検証条件は変更しない。

**Approved full Git SHA before this approval record:** `a12c4247b8a95d5dafabc44e82bdec959693cae6`.

**Formal amendment:** `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P04-004_Gate_Contract_Amendment.md`.  
**Architecture decision:** `DEC-G01-P04-PRODUCT-POLICY-SHARING-01=B_ADOPTED` recorded in `combined_review/243_20261123_g01_p04_product_policy_sharing_B_owner_adopted.md`, supported by non-normative docket `242`.

## 2. Approved bounded implementation and unchanged final requirement

G01/P04/Trial01 may implement the one Local P1-M06 Method metadata and pure eligibility policy authority, its validated Method/Estimand/Design/Inference/Backend capability path, and FCI preflight/adapter; it must not create a second mutable P1-M06 rule table, silently copy Product legacy estimator aliases, route Local P1-M06 into the existing Product validator, or claim Product v2 already delegates to new Local policy.

**Product v2 `ScientificValidationService.validate_submission` and its existing `ESTIMATOR_CAPABILITIES` stay unchanged.** These are legacy-only compatibility baseline logic for the interim stage and **not** P1-M06 scientific authority. The eventual migration to a single common pure policy/metadata authority is `DEFERRED_PRODUCT_POLICY_BRIDGE`, *not* `IMPLEMENTED`, `RETIRED`, or approved Product source changes. Any actual legacy migration requires separate Owner-controlled scope, migration design and complete regression/behavior equivalence verification.

**G01_999 acceptance:** The Product common-policy bridge is an explicitly **unfulfilled architecture dependency**. No G01_999 shared-policy PASS is permitted until a separately approved implementation/verification or an independently authorized formal change to that acceptance staging. This decision does not invent a waiver, transfer the work automatically to another Gate, or release downstream Gates. All independent FCI/MAG/PAG/BK/FS/T2/T3/Product v2 compatibility and G01_999 requirements remain.

## 3. Verified approval-time Git evidence

At approval, the HEAD was exactly `a12c4247b8a95d5dafabc44e82bdec959693cae6`. Compared to stopped G01/P04 Agent START_SHA `99c33a661272d45bf72c8dee61ce1eb129a337dd`, this change comprised **exactly eight files**:

1. `00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md` — modified.
2. `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md` — modified.
3. `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md` — modified.
4. `10_enhance_instruction/G01/06_G01_P04_fci_backend_oracle.md` — modified.
5. `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md` — modified.
6. `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P04-004_Gate_Contract_Amendment.md` — added.
7. `00_enhance_background/Revised_requirements_definition_documents/combined_review/242_20261123_g01_p04_product_v2_shared_policy_scope_decision_docket.md` — added.
8. `00_enhance_background/Revised_requirements_definition_documents/combined_review/243_20261123_g01_p04_product_policy_sharing_B_owner_adopted.md` — added.

GitHub compare verified the following as direct ancestors of the approved SHA (behind 0): prior S10 `cbfdbdd6b91f3a2f889fe9b62c2a4ab286da6132` (ahead 10), P01 checkpoint `9bff61f0eae25236f95f31f2cd3e7c81291f0167` (ahead 73), and P03 checkpoint `858c9f73366036a2d1445e558135cd521f611462` (ahead 38).

No Product v2 source code, completed P01/P03 files, public E11 wire schema, `uv.lock` or other Gate change is among this amendment's diff.

## 4. Preserved prior science and independent test obligations

Preserve AMD-001 exhaustive unordered X/Y/all conditioning subset CI eligibility, AMD-002 strict declared `category_codes` for categorical `chisq/gsq` with complete support, AMD-003 float64 Fisher-Z conditioning and residual thresholds, actual Backend/FCI/PAG circle & endpoint fidelity, validated immutable Graph provenance, non-null BK preflight fail-closed, and independent MAG/PAG Oracle, T2/T3, Linux FS, Product v2 regression and G01_999.

This administrative formal09 approval does **not** imply P04 implementation, focused test PASS, real fit, scientific evidence, a P04 checkpoint or G01_999 acceptance.

## 5. Required separate control-plane approvals

The Owner must approve **new revised S10** on an exact complete Git SHA **including this formal 09 record**, followed by **a distinct limited S11** for `G01/P04/Trial01`. Prior S10 `cbfdbdd6b91f3a2f889fe9b62c2a4ab286da6132` and S11 `DEC-G01-P04-003-S11-REAUTH-01` are historic and insufficient for altered AMD-004 integration timing. The Git SHA creating this record is after the approved draft SHA and does not retroactively change the latter.

No Coding Agent resume is authorized by this formal09 alone.
