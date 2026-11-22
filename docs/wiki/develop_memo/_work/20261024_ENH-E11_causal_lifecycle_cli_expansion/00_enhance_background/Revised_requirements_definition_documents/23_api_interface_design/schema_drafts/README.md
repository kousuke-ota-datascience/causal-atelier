# E11 Local v1 JSON Schema drafts — PREP-02

**2026-11-17 scoped design Freeze:** [PREP-02 baseline 117](../../combined_review/117_20261117_prep02_common_contract_baseline_freeze.md) fixes common v1 payload identifiers, outer envelope/ContentRef/Graph & Manifest hash semantics, typed science and Error/Privacy/Publish invariants. **These machine-readable files remain structural DRAFTs for Method-specific config, operation bundles and runtime validation.** Design-basis adopted ≠ all 41 configs verified, runtime Schema PASS or Coding Authorization.

| Contract | Machine-readable draft | Version |
|---|---|---|
| Study | [e11_local_study_v1.schema.json](e11_local_study_v1.schema.json) | `e11-local-study/1` |
| Graph | [e11_local_graph_v1.schema.json](e11_local_graph_v1.schema.json) | `e11-local-graph/1` |
| Effect | [e11_local_effect_result_v1.schema.json](e11_local_effect_result_v1.schema.json) | `e11-local-effect-result/1` |
| Manifest | [e11_local_manifest_v1.schema.json](e11_local_manifest_v1.schema.json) | `e11-local-manifest/1` |
| Status | [e11_local_status_v1.schema.json](e11_local_status_v1.schema.json) | `e11-local-status/1` |
| Commit marker | [e11_local_commit_marker_v1.schema.json](e11_local_commit_marker_v1.schema.json) | `e11-commit/1` |
| AR/Inference definitions | [e11_ar_inference_defs.schema.json](e11_ar_inference_defs.schema.json) | Internal `$defs`, not an independent payload |

The Effect schema embeds the AR/Inference `$defs`, including the generic `EMPTY` topology with zero components; the separate AR definitions mirror this structural shape. This correction concerns the JSON Schema shape only. Cross-schema joins, topology semantics, Method-specific just-identified nonempty conditions, runtime JCS conformance and scientific coverage remain unverified, so the Method-specific schemas are not frozen. The [F06 contract](../../combined_review/106_20261117_prep02_f06_dispatch_codec_error_contract.md) records discriminator, legacy-v2 and canonicalization decisions; it is design provenance, not the runtime authority.

The current schemas are structurally strict at top-level and some subobjects, but flexible method-specific `config`, `provenance`, `stochastic`, etc. are **intentionally not contract-complete**. Completing their typed definitions, duplicate artifact uniqueness, hash/cross-reference correctness, URI/path confinement, graph semantics and scientific inference is mandatory before Freeze. JSON Schema shape checking cannot prove scientific or OS security properties.


## Owner採用 D-F07-EMPTY / D-F05-POLICY / D-F06-CODEC・ROW-EXIT（2026-11-17）

- Generic AR Confidence Setは`EMPTY` topologyの0 componentを受理。Effect schemaへ同じ規則を複製して更新。Method別just-ID拒否は科学的検証に残る。
- **Current Owner S02:** Studyでは`privacy.row_export_requested=true`を単一明示opt-inとし、未公開の`privacy.policy_ref`を削除。撤回済み署名Policy/独立鍵の記述は履歴であり現行実装の要件ではない。
- E11 strict canonicalizationはOwner採用済み方向性。RFC8785 JCSを技術候補とし、Manifestに`canonical_codec_version`を持つDraft、`default=str`は禁止。実装・クロス言語検証は残る。
- Privacy/authorization denialはExit 3。No silent aggregate-only fallback。

[Owner決定記録](../../combined_review/decisions/95_20261117_dec_prep02_four_owner_choices.md)。**Schema drafts**でありFreeze済みではない。


## F07 EMPTY and E11 Canonical Codec — Owner four-choice update

- [DEC-PREP02-D](../../combined_review/decisions/95_20261117_dec_prep02_four_owner_choices.md) adopted generic mathematically `EMPTY` AR confidence sets. The `e11_ar_inference_defs` and embedded Effect Result `$defs` both contain `EMPTY`/`components=[]` and require nonempty components for nonEMPTY topologies. Semantic set validation and just-ID Method-specific nonempty assertions are separate.
- Owner adopted an **independent strict canonical Codec**, not a specific implementation standard. RFC8785 JCS is the engineering candidate, with [7 positive / 7 negative golden vectors](e11_jcs_golden_vectors.json) and [design reasoning](../../combined_review/107_20261117_prep02_jcs_codec_vectors.md). Proposed `canonical_codec_version=e11-json-jcs-rfc8785/1` has been added to the Manifest Schema draft; Python↔ECMAScript bytes conformance is **not verified**.
- Privacy authorization denial = CLI exit3; root/UID/Method/schema/caps and explicit Study-only opt-in are mandatory before row access. No independent signed-policy proof in current E11.


## Cross-schema semantics for F06 (current design candidate)

[Cross-schema invariants](../../combined_review/114_20261117_prep02_f06_schema_semantic_invariants.md) specify two distinct Graph hashes: `Graph.content_hash` is the JCS digest of Graph excluding that field itself; external `ContentRef.sha256` verifies full Graph file bytes. The Manifest `schema_dispatch.result` is **nullable** for non-Effect operations, but an Operation-specific scientific Bundle validator must reject missing required Effect or a fake Effect in discovery-only operations. [Shared Port and ErrorPhase](../../combined_review/112_20261117_prep02_f03_f07_shared_port_signature_contract.md) governs typed cross-artifact joins and phase-specific CLI exit codes. These runtime/semantic rules cannot be certified by JSON Schema alone.


## P1-M06 FCI Method/Question/Design validation profiles

Method P1-M06の`Study.method.config`だけを[FCI config schema](e11_p1_m06_fci_method_config_v1.schema.json)でMethod registry dispatchする。P1-M06の外部入力Question/Designは[Question profile](e11_p1_m06_fci_question_profile_v1.schema.json)、[Design profile](e11_p1_m06_fci_design_profile_v1.schema.json)で厳格検証。**これら3件はP1-M06用の内部Validation Profileであって、Ownerが採用した5種類のE11公開payload/schema versionを変更・追加するものではない。** Strict duplicate key/semantic join/Dataset type/CI admissibilityは07の実行時検査対象。


**Naming / authority:** 上記 `e11_p1_m06_fci_*.schema.json` がMethod-IDに紐付く参照対象。旧 `e11_g01_*.schema.json` は過去の作業記録への参照互換性のため残す歴史的draftであり、新しいDomain/Method実装がdispatch対象にしてはならない。Schemaはstructural validation、ID/hashes/CI eligibility/BKのcross-asset semantic ruleは別途検証する。過去のPREP-02/PREP-03は設計履歴としてのみ扱い、これらのProfileはG01というGate IDで選択しない。

## Graph identity and parent linkage

`e11-local-graph/1`では両Versionキーは存在必須・現在のLocal専用Schemaでconst nullとする。CLI standalone discoveryは`version_id=null,parent_version_id=null`を正規形とし、現行Local GraphにはProduct由来の識別子を設定しない（両方null）。将来のProduct importは別契約・別Schemaで審議する。**graph content_hash/JCS、endpointの科学意味**は外部semantic Validatorで検証し、JSON SchemaだけでProduct linkageの正しさを宣言しない。公開Version文字列は変更しない。

## PREP-03 OD-02/03 Owner採用（2026-11-19）

- Signed G05 row-policy Schemaは現行Schema Draft treeから削除済み。過去の採用・撤回判断は`combined_review/128/129/131/137`とGit Historyに保持し、現行`e11-local-study/1`では`policy_ref`を登録・解釈しない。
- Historical signed-policy authority is not an initial E11 functionality; no keys, Trust Store, independent reviewer or revocation contract are required.
- G05 Row WriterのParquet columns/dtypesとMethod固有`ApprovedRowSchema`は別に確定が必要。G02〜G09の40件Method Config/Question/Design/Output/Inference Schemaを本Owner採用で一括生成済みと扱わない。

Decision: [DEC-PREP03-OD01–05](../../combined_review/122_20261119_dec_prep03_od01_od05_owner_adoption.md)。Runtime/Security review, Gate Freeze and Coding Authorization remain pending.

## Current strict draft boundaries

Studyには個票出力の単一明示booleanだけを持ち、撤回済み署名Policy参照を含めない。現行Local GraphのProduct Version IDはnull固定であり、将来のProduct連携には新たな明示契約が必要。40 MethodのOutput共通Schema候補は、各Methodの固定Operation/Artifact/Result制約と同等な場合のみ登録できる。Schemaの構造検証だけでは実効Backend、Path安全性、統計的妥当性は証明できない。

## Factored Method Profile (40×5)

The prospective strict **structural** authority for all 200 internal Method Profile drafts is now `method_profiles/factored/e11_{method_config,question_profile,design_profile,output_profile,inference_profile}_factored_v1.json`. Each bundle reconstructs its Method ID's exact original single-object JSON Schema using a common core plus a per-Method overlay. Do **not** validate common and overlay separately with `allOf` and `additionalProperties:false`; that changes acceptance semantics. The former 200 individual files are kept as immutable hash-pinned baselines until the independent Draft202012 parity runner succeeds in a pinned checkout. This internal draft registry is not a new public payload version and does not grant Method/Backend/Scientific availability. Cross-artifact B03 semantics, Source/Method Profile integration and Final Coding Authorization remain separate.
