# 226 — Owner-approved limited G01-S11 for AMD-E11-G01-P03-001

**Date:** 2026-11-23 JST  
**Owner Decision:** `DEC-G01-P03-001-S11-REAUTH-01=APPROVED`  
**Owner instruction (verbatim):** 「DEC-G01-P03-001-S11-REAUTH-01を承認する。AMD-E11-G01-P03-001に基づく暫定G01-S10凍結SHA 52e5c60176d6b72c91f839ef267f46657bd380b5 を対象に、G01/P01〜P05の限定Coding Authorizationを再発行せよ。次の実行対象はG01/P03/Trial01とし、DEC-G01-P03-P02-COMPAT-01で承認したP02 Readerの限定互換修正を含める。P01チェックポイント9bff61f0eae25236f95f31f2cd3e7c81291f0167、P02チェックポイント3a76a0aa1698037354b284ba7b5a875300473ce6、科学的・独立検証・G01_999受入条件は維持する。」  
**Repository/branch:** `kousuke-ota-datascience/causal-atelier` / `feature/ariadne_mvp_e11`  
**Immutable normative G01-S10 full Git SHA:** `52e5c60176d6b72c91f839ef267f46657bd380b5`  
**Formal 09 approval:** 222 (`AMD-E11-G01-P03-001`)  
**Revised S10 reFreeze:** 224 (`DEC-G01-P03-001-S10-REFREEZE-01`)  
**Bounded completed-P02 compatibility approval:** 221 (`DEC-G01-P03-P02-COMPAT-01`)  
**P01 PACKAGE_READY:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**P02 PACKAGE_READY:** `3a76a0aa1698037354b284ba7b5a875300473ce6`  
**uv.lock blob:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`  
**Next permitted Agent run:** `GATE_ID=G01 PACKAGE_ID=P03 TRIAL_NO=01`

## 1. Authorization scope

This is a **new and independent limited S11 Coding Authorization** under the frozen G01/P01–P05 WHAT `52e5c60176d6b72c91f839ef267f46657bd380b5`, following separate formal 09 and provisional S10 Owner decisions. Implement and developer-verify **G01/P03/Trial01** next. P01 and P02 completed checkpoints, reports and verified evidence are immutable historical records; neither may be recreated or retroactively relabeled.

The Owner has additionally and separately approved **the minimum compatible P02 Reader retrofit** for typed GraphProvenance. Its scope is the relevant semantic check in `src/ariadne/interfaces/cli/local_causal/manifest_reader.py` (including reusable P03 pure Graph validator wiring) and narrow tests in `tests/enhancement/enh_e11/g01/integration/test_local_publication.py` or directly adjoining G01/P03 graph tests. This does not authorize changing P02 Publisher, privacy/TrustedRoot/FD/atomic rename, manifest envelope, P01 implementation, public Port ABI or Product v2 GraphVersion. If implementing reliable actual source ContentRef byte verification requires extending these protected components, STOP and return with evidence for a new Owner decision. Complete focused P02 regression and write new trace/checkpoint for the scoped follow-up rather than overwriting existing P02 checkpoint.

## 2. Frozen Graph contract and trust validation

`e11-local-graph/1` retains top-level Graph fields and Local `version_id=parent_version_id=null`. Existing `provenance` now has exact required keys `method_id,backend,ci_test,assumptions,source_refs,parent_graph_ref`. P1-M06 DISCOVER requires Method `P1-M06`, backend `causal-learn`, CI matching validated Study method config `indep_test`, declared (not independently proved) assumptions, exact five-field Question/Design/Dataset input refs matching Study and Manifest and validated against trusted actual referenced bytes, initial scientific parent `null`. A scientifically genuine local successor parent requires a secure reference to immutable actual bytes, checked against full file ContentRef.sha256 and independently the parent's semantic Graph.content_hash JCS digest. Do not conflate internal semantic Graph digest with external full-file hash. Reconstructed/provenance-forged objects must fail semantic cross-file checks even with recalculated self-consistent Graph hash. Preserve PAG endpoint uncertainty and no implicit PAG→DAG reinterpretation. Schema-valid provenance cannot prove actual FCI science or causal effect identification.

## 3. Actual Agent entry and stop rules

Coding Agent must verify remote and branch, actual HEAD/clean worktree, `52e5c60176d6b72c91f839ef267f46657bd380b5` ancestor, post-freeze differences restricted to approved administrative records, tracked `uv.lock` blob and measured file SHA256, the P01 and P02 checkpoint ancestors plus their PACKAGE_READY reports, absence of P03 checkpoint and Trial01 formal Gate FAIL/08, and separate Owner 09=222, S10=224, S11=this 226. Failed checks are BLOCKED, not permission to forge evidence.

Use frozen five-layer RD/LDD/BD/IF/DD, `10_enhance_instruction/G01/06_G01_P03_pag_graph_version.md`, G01 07 and the separate exception 221 as the implementation WHAT. Validate P03 graph endpoint/temporal/provenance/hash/reader positives and negatives, P02 readback regressions and protected P01/Product regressions against actual environment. Only observed tests count; P03 PACKAGE_READY requires official report/checkpoint. Independent P04 FCI/MAG/PAG science, S09/B02–B05/T2/T3, Gate 07/G01_999, and release are **not authorized to be declared PASS** by S11 or developer tests.

## 4. Historical authorities

Prior S11 record 216 was approved for the earlier amended WHAT `c37cd93d981a6d3777e20bd46b26bc3ae9b2c1f8`; it is superseded as authority for this P03 contract. No new normative contract changes may be self-authorized by Coding Agent; return to formal 09→new S10→distinct S11 if a fresh semantic ambiguity is discovered.
