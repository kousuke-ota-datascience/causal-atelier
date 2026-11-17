# ENH-E11 PREP-01 — Stock/Flow migration manifest (2026-11-17)

**Classification:** FLOW / MIGRATION EVIDENCE, not a canonical Stock design document.
**Source branch:** `prototype/ariadne_mvp`; original input HEAD `14176e2175f1f75db04a7dcb4e836ad296374b4e`.
**Migration:** Root Review/Owner decisions 8, Change Log 5; original content is retained in original Blob SHA, and working links rewritten for relocated file. No change to DEC09 Owner Scope, requirement meanings, science acceptance or canonical promotion decision.

| Old path (relative to Revised root) | New Flow path | Original blob SHA |
| --- | --- | --- |
| `90_structural_split_verification.md` | [`doc01_review/structural_migration/90_structural_split_verification.md`](../doc01_review/structural_migration/90_structural_split_verification.md) | `51aaeeae427e79cbcf9eafe6e865364f081461cb` |
| `92_rd02_restructure_verification.md` | [`doc01_review/rd02_migration/92_rd02_restructure_verification.md`](../doc01_review/rd02_migration/92_rd02_restructure_verification.md) | `7ef7ef6b0e2703156257a5fc9a0fc604a88a2ea1` |
| `93_enh_e11_canonical_promotion_policy.md` | [`combined_review/decisions/93_enh_e11_canonical_promotion_policy.md`](../combined_review/decisions/93_enh_e11_canonical_promotion_policy.md) | `0d7f104993cb42b0f36b589b28462cacc31a87de` |
| `95_rd04_fr_application_review.md` | [`doc01_review/rd04_review/95_rd04_fr_application_review.md`](../doc01_review/rd04_review/95_rd04_fr_application_review.md) | `f3c94d82d0241cf68062ba842e88894ba471447b` |
| `96_rd03_formal_requirement_traceability.md` | [`doc01_review/rd03_review/96_rd03_formal_requirement_traceability.md`](../doc01_review/rd03_review/96_rd03_formal_requirement_traceability.md) | `ad287e8015e71f9cd1f18c83792c23843c536654` |
| `96_rd04_nfr_ar_application_review.md` | [`doc01_review/rd04_review/96_rd04_nfr_ar_application_review.md`](../doc01_review/rd04_review/96_rd04_nfr_ar_application_review.md) | `b55ea661bf95ea72cd815331aae7b14b9658e4e3` |
| `97_rd04_e11_requirement_review.md` | [`doc01_review/rd04_review/97_rd04_e11_requirement_review.md`](../doc01_review/rd04_review/97_rd04_e11_requirement_review.md) | `83f128662e6a13f8ca7cc3b7dfe89f396da4813e` |
| `98_rd04_consistency_verification.md` | [`doc01_review/rd04_review/98_rd04_consistency_verification.md`](../doc01_review/rd04_review/98_rd04_consistency_verification.md) | `3c00b4893bc5d4914498aecfc7b648ce631e42b5` |
| `10_requirements_definition/10_99_change_log.md` | [`doc01_review/history/10_99_change_log.md`](../doc01_review/history/10_99_change_log.md) | `13eb9ff4c5fe4dd131aaccefd411941c2063e449` |
| `21_logical_data_design/21_99_change_log.md` | [`doc01_review/history/21_99_change_log.md`](../doc01_review/history/21_99_change_log.md) | `1329f4a07bf392870abd1c32e640094842aedfbe` |
| `22_product_basic_design/22_99_change_log.md` | [`doc01_review/history/22_99_change_log.md`](../doc01_review/history/22_99_change_log.md) | `d16dbbb351036bf7d8b1dca0204feeefcd6b9371` |
| `23_api_interface_design/23_99_change_log.md` | [`doc01_review/history/23_99_change_log.md`](../doc01_review/history/23_99_change_log.md) | `19dafd39408ce6123ea30273a771d502135b8772` |
| `30_detailed_design/30_99_change_log.md` | [`doc01_review/history/30_99_change_log.md`](../doc01_review/history/30_99_change_log.md) | `ab378a6a083b661fdd71f3c85f7969225cc13ac7` |

## Applied safeguards

1. New 13 Flow files were staged in commit `0be2d2bfbd7342d2dbcdcfb5c82a0447a893f6f8`, retaining original content apart from rebased Markdown relative references (63 links adjusted).
2. Root README, Scientific Method, BD architecture reviews, RD01/RD04 migration records and BD source snapshots were relinked in commits `27a842f8e7251626a489e83b4df3ed5a771949d9` and `d28119367d466b78b6054f0ba2665f62b565e6ce`. Historical source snapshots retain the original content in Git history; current working links are rebased.
3. DOC01 review index and audit addenda were updated in commit `e06d4974dc70bcc0c66aee384951ce259dfad115`. Old paths are removed in the present commit.
4. Staged destination files had 68 local Markdown links checked: **0 broken within the Revised root**. Four links pointed outside this root (working_notes x2, enhancement concept x1, original canonical source x1); these require separate validation from the repo tree. Anchors, non-Markdown path references, other Project documents, and external Notion links are **not fully verified**.
5. No original `docs/wiki/requirement_definition/`, implementation Source, `pyproject.toml`, or `uv.lock` is modified.

## Limitations / acceptance

- Historical Audit paragraphs quoting old relative path literals are intentionally preserved as historical identifiers; **Markdown targets are rebased**, literal inline code is not treated as a live link.
- Full-repo link/Anchor scanning and semantic integrity 122 clauses are pending. This migration is a **structural improvement**, not PREP-01 DONE or independent verification PASS.
- The Owner-approved canonical promotion criterion remains: **no original canonical update until every ENH-E11 related test PASS**.


## Post-migration readback & scope-limited link QA（2026-11-17）

- **Physical tree:** commit `cd4e73856b89bee2be2db4e5c5a50976f431bd91` でRoot旧8件と5群Change Log旧5件を削除。新13件すべて実在、旧13件はtreeから消滅。5群のMarkdown件数は **22/17/18/21/27 = 105**。この数字は「Stockの内容品質PASS数」を意味しない。
- **Additional repair:** `5955ff7eede5c527c3f4f56c3d02933351cb8faa` にて、RD-04移管記録/BD source snapshotsに残っていた旧階層参照19箇所を修正。
- **Internal file existence check:** 新Flow13件のrelative Markdown links 68、RD04移管台帳/BD snapshots等12件の245、5文書群のStock105件の39、Root READMEの164を走査した。合計**516 link occurrences**のうち、改訂Working Copy**内部に解決する参照のbroken=0**。残る**11 link occurrences**は改訂Root外であり、参照する4つのdistinct targets（DEC09 working_note、SR04 trace working_note、enhancement concept、元canonical requirement）を`fetch_file`で存在確認した。件数は複数文書から同一targetを参照する重複を含む。
- **Limits:** 本検査はMarkdownの`[label](relative-path)`形式の**file target existence**を中心とする。Fragment`#anchor`、HTML/画像/参照形式link、CodeSpan文字列、GitHub上の他Enhancement・Notion外部backlinks、semantic accuracyを網羅しない。Github PagesレンダラのslugやCase Sensitivity差は別検証。**Full repo link QA PASSやPREP-01 DONEは宣言しない。**
- **Review:** [Independent Architecture review package](../combined_review/94_20261117_prep02_architecture_review_package.md)は**提出用Draft**、独立Reviewerの判定やOwnerの新たなFreezeではない。
