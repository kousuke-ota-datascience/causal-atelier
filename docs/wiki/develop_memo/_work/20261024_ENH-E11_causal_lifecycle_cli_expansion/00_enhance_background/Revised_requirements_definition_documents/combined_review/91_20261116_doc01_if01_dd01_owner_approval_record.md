# ENH-E11 — 2026-11-16 DOC-01・IF-01・DD-01 Owner統合承認記録

**文書区分:** FLOW / OWNER DECISION（元正本へ昇格しない）  
**Owner判断日:** 2026-11-16 JST。時刻は会話記録に従う（このファイルでは別途署名時刻を捏造しない）。  
**Owner発言:** 「DOC-01 承認。IF01 DD01 ともにこの案で行く」  
**審査対象Git Commit:** `c17f0baa01b66b24395cf8d96f6ae224d382cc7a`（`prototype/ariadne_mvp`）。このSHAは承認判断の入力Snapshotであり、承認記録の追記Commitとは異なる。  
**判定:** `DOC01_OWNER_APPROVED / IF01_DESIGN_ADOPTED / DD01_DESIGN_ADOPTED / INDEPENDENT_REVIEW_AND_FORMAL_FREEZE_PENDING / CODING_NOT_AUTHORIZED`

## 1. 決定内容と拘束力

| 対象 | Owner決定 | 採用する設計／監査範囲 | 今回の承認で成立しないこと |
|---|---|---|---|
| DOC-01 | **APPROVED** | 10/21/22/23/30のStock/Flow分離、既存105→追加後110のStock候補、Flowアーカイブ、要件302行・ID重複なし、MOVE_BD原文19/19一致の監査成果物と残余管理 | 122改訂正文の独立逐条内容PASS、anchor等の未点検箇所のPASS、原正本への昇格 |
| IF-01 | **ADOPT AS PROPOSED** | 23_41・23_42の独立Local CLI、versioned Study/Result/Graph/Manifest、Port、Method gate、typed effect/AR、Local Privacy、Atomic publication契約 | JSON Schema成果物/CLI grammar正式Freeze、実装済み、Runtime Contract Test PASS |
| DD-01 | **ADOPT AS PROPOSED** | 30_61・30_62・30_63のDomain/Port/UseCase/Publisher/Reader/Privacyと41 Method Adapterの分担、失敗・推論・データ安全性の詳細方針 | exact Python symbol/port signatures、実効Backend/API、数値推論実証、全Class物理Source Audit PASS |

この承認は、3工程の**Ownerレベルの設計方針選択と作業成果物の採用**を意味する。IF/DDの提示された候補名やSchema形状は、実装設計の選択ベースラインとして採用するが、機械検証可能なSchemaファイル、Versioned Port契約、実装との一致まで本承認で「凍結済み」としない。

DOC-01のOwner承認は、全ての手作業・独立検証が実行済みという主張ではない。監査台帳に明示された残余を後続の独立確認・Freeze／Gate受入条件として引き渡す。既存の受入基準を黙って撤回しない。

## 2. Combined Review REV-01〜REV-10

| ID | Owner結果 | 採用内容と残存条件 |
|---|---|---|
| REV-01 | ADOPT | Stock/Flow分離、正本候補110件。改訂全条文の意味監査は追加検証 |
| REV-02 | ADOPT | 302 ID/19原文一致の監査を受領。122条文の独立意味照合は残余 |
| REV-03 | ADOPT | E11専用CLIと明示Schema/Version dispatch。Schema実体のFreezeは後続 |
| REV-04 | ADOPT | E11 Domain Portと既存Product Portの責務分離。具体reuseとPackage依存監査は後続 |
| REV-05 | ADOPT | AR集合のtopology・∞端点のlossless表現。数値反転の科学的検証は後続 |
| REV-06 | ADOPT | staging/manifest/marker/no-clobber同一FS公開。実FS crash/fault proofは後続 |
| REV-07 | ADOPT | Local OS principalと個票CATEの厳格なopt-in。認可threat modelと実効権限検証は後続 |
| REV-08 | ADOPT | 全41 Method Adapterと異なるEstimand/Inferenceの分離。Method-specific API/数値受入は後続 |
| REV-09 | ADOPT | DEC08の5 Profile、ENV-RD候補、lock/SBOM/Legal分離。実効Lock/License承認は後続 |
| REV-10 | ADOPT | Owner設計採用、独立Architecture/Science、Gate/Coding/正本昇格の権威分離を維持 |

**採用判断に新たなMethod追加・Scope拡張は無い。** DEC09の68 Scope、41 Method、10 UC、新規44正式要件、旧`causal-analysis-spec/2`互換性を保持する。P1-M05等の未確定科学条件は明示したままとする。

## 3. Open findingsのDisposition

| Group | Owner判断後の扱い | 次の確証 |
|---|---|---|
| DOC01-F01〜F05 | **ACCEPTED_WITH_OPEN_VERIFICATION**（Stock/Flow分類は承認、欠落／semantic検証は残す） | 122条文の意味保存、anchor/非Markdown参照、旧本文の完全性、索引整合 |
| IF01-F01〜F08 | **DESIGN_CHOICE_ADOPTED / ACCEPTANCE_OPEN** | Version/SchemaファイルFreeze、Contract Test、Runtime/Backend/FS/Privacy/Env/Legal |
| DD01-F01〜F10 | **DESIGN_CHOICE_ADOPTED / IMPLEMENTATION_EVIDENCE_OPEN** | Package reuse調査、Class/Methodの具体Source設計、推論/AR数値検証、fault/security/Env |
| BD01-F03〜F13（11件） | **OPEN**。Owner採用のみではIndependent Architecture Reviewを閉鎖しない | ADR/Port/Schema・Architectureの独立Reviewer |
| Product GAP-C01〜C04 | **OPEN／別Workstream**。E11 CLIによる自動閉鎖禁止 | 独立Product Owner/Work Package |

Open findingは「今回の選択案を拒否した」意味ではなく、実装の科学的／技術的妥当性に関する検証責務として保持する。

## 4. 次工程（設計採用後の実施順）

1. **ARCH-01：独立Architecture整合・Design Decision Freeze準備**。Owner採用版のBD/IF/DD、Package reuse、Version/Port/Schema、atomic/security、Backend designを独立レビューし、F03〜F13のDispositionを決める。現時点で独立Reviewer署名は存在しない。
2. **CONTRACT-01：Schema/Port・Method Configの正式Freeze**。JSON Schema／Version Dispatch／Python Protocol／Error/Manifestの整合と、全41 MethodのBackend/Estimand/Inferenceの未定義を明示的に解消。既存v2回帰を凍結条件とする。
3. **GATE-PREP：Gate06実装受入＋Gate07科学受入の証拠登録**。41 Method×DGP/NEG/REF/AC、FWER=0.05、K/R/Budget/MC、Environment Profile、SBOM/Legal条件をFreeze準備する。未実測値は推定値で埋めずBLOCKEDとして管理。
4. **Coding Authorization：別途判断**。上記の設計／事前受入基準が揃ったWork Packageに対してのみ明示的に発行する。現ターンの設計承認を実装許可と解釈しない。

## 5. 正本昇格と実行上の禁止

改訂成果物は引き続き`docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/00_enhance_background/Revised_requirements_definition_documents/`の内部だけに保存する。元`docs/wiki/requirement_definition/`への反映は、**ENH-E11の対象テストが全件PASSした後**に限り別途実施する。OwnerによるDOC/IF/DD採用、独立Architecture Review、Science PASS、Legal判断、Gate06/07、Coding Authorizationは相互に代用しない。

**関連資料:** [三工程統合Review Pack](90_doc01_if01_dd01_owner_review_pack.md)、[DOC-01台帳](../doc01_review/README.md)、[IF-01内部Review](../if01_review/90_interface_contract_review.md)、[DD-01内部Review](../dd01_review/90_physical_design_review.md)。
