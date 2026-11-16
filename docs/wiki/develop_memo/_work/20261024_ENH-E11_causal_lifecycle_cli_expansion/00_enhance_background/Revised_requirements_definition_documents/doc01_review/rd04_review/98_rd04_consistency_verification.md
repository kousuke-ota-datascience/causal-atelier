# RD-04 — 要件本文改訂・設計移管・整合性監査（2026-11-16）

**State:** `RD04_WORKING_COPY_REWRITTEN / AUTOMATED_STRUCTURE_AND_TRACE_AUDIT_PASS / OWNER_CONTENT_SIGNOFF_PENDING / NO_CANONICAL_PROMOTION`。

## 1. Scope and disposition after independent reassessment

| Status | FR | NFR + scientific AR | Sum |
|---|---:|---:|---:|
| KEEP_RD | 107 | 29 | 136 |
| REWRITE_RD | 3 | 4 | 7 |
| SPLIT | 69 | 27 | 96 |
| MOVE_BD | 16 | 3 | 19 |
| **Total** | **195** | **63** | **258** |

- 元の195 FR／36 NFR／27 Scientific ARをRD-01逐条台帳から再審査し、同一ID・Level・Requirement Status・Implementation Status・Deliveryのまま要件文を改訂。
- **122件**で要件文を変更、**136件**のKEEP_RDは原文のまま。MOVE_BDの旧IDは`Legacy Trace`としてRD上に残し、承認なしにRETIREDへ遷移させない。
- FR-072は同一DatasetVersion・同一TEST sample identity/hash・同一定義metricを保護。FR-176/177、AR-021/024は設計移管だけではなく外部可観測な要求核があるためSPLITへ変更。AR-016のSubgroup 95%・1000 bootstrap resamples・deterministic seedはMethod ScopeとAcceptanceに残した。
- [FR review / diff](95_rd04_fr_application_review.md)／[NFR+AR review / diff](96_rd04_nfr_ar_application_review.md)。

## 2. Destination proof (source IDs preserved)

| Destination family | Unique transferred source IDs | Record status |
|---|---:|---|
| 21 LDD（責務別10ファイル） | 38 | PASS — source IDs and counts checked after GitHub readback |
| 22 BD（責務別16ファイル） | 91 | PASS — source IDs and counts checked after GitHub readback |
| 23 IF（責務別12ファイル） | 45 | PASS — source IDs and counts checked after GitHub readback |
| 30 DD（責務別12ファイル） | 32 | PASS — source IDs and counts checked after GitHub readback |
| RD Scientific 10_30／31／32 | 12 | PASS — source IDs and counts checked after GitHub readback |
| **Total destination records** | **218** | one source ID can appear in multiple destination documents |

**119件**の改訂済み要件が少なくとも1つの設計または科学的契約の移管先を持つ。うち3件はREWRITE_RDのみで下位移管不要。MUST/Statusを喪失する形の無言の削除は行っていない。下位設計の98節は**既存原文の実現契約を保持する移管レコード**であり、全Classの物理詳細が完成したと見なさない。

## 3. Formal E11 clause preservation and trace

| Object | Current ID count | Test |
|---|---:|---|
| FR (existing 195 + E11 19) | 214 | PASS：195件の旧Status保持、19件のE11条文がRD03と同一 |
| NFR (36 + 8) | 44 | PASS：36件の旧Status保持、8件のE11条文がRD03と同一 |
| Scientific AR (27 + 17) | 44 | PASS：27件の旧Status保持、17件のE11条文がRD03と同一 |
| **Total requirement rows** | **302** | PASS：各区分でID重複なし |
| DEC09 Scope | 68 | PASS：全行のTraceを[RD-03](../rd03_review/96_rd03_formal_requirement_traceability.md)に保持 |
| SR04-F Method | 41 | PASS：Method全行を[10_32](../../10_requirements_definition/10_32_scientific_method_scope.md)で保持 |
| UC | 10 | PASS：全UCのTraceを保持 |

新E11条文の科学的・機能的論点は[RD-04 E11 review](97_rd04_e11_requirement_review.md)に列挙。Scope/R/Q/N/DのDisposition、限定Frontdoor FD-A、NCE/NCO、B0/B1、DRIV、SCM point-onlyの制限を変更していない。

## 4. Canonical and approval boundary

- 旧正本5ファイルのGitHub Blob SHAはすべてRD-02監査と一致し**原正本は変更されていない**。
- RD-04の作業範囲は`Revised_requirements_definition_documents/`配下。元の`docs/wiki/requirement_definition/`はENH-E11の対象テスト**全件PASS後**にのみ昇格する（[決定](../../combined_review/decisions/93_enh_e11_canonical_promotion_policy.md)）。
- 本監査のPASSは**文書行・ID・Trace・移管レコードに対する構造監査**であり、Methodの実行検証・科学的受入、Gate06/07、Legal、Owner最終SHA内容承認のPASSではない。
- RD-04のDisposition再審査結果は作業版へ反映済み。個別条文のOwner最終確認は後続の設計整合レビュー時に実施する。

## 5. Follow-up items

1. BD-01：移管された設計制約を全体アーキテクチャと具体Method契約へ統合し、移管レコードだけで終わらせない。
2. IF-01：Local CLI契約、typed Scientific Result、Error、Privacy、optional backendをFreeze可能なSchemaへ展開。
3. DD-01：採用済みClass templateでModule/Class/MethodのSignature・数値制約・Exception・Testを具体化。
4. Gate06の受入条件・Environment・Science/Legal依存を未了事項として管理し、実装着手をこのRD-04のみで承認しない。
