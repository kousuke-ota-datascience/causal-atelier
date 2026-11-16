# ENH-E11 — DOC-01 / IF-01 / DD-01 一括Owner Review Pack

**Created:** 2026-11-16  
**Decision state:** `THREE_DRAFTS_SUBMITTED / INTERNAL_STATIC_CHECKS_RECORDED / OWNER_DECISION_NOT_YET_RECORDED`。  
**Scope:** 正本候補のStock／Flow分離、Local Interface、Local Physical Design。Architecture・Method science・Coding・Legal・Gate06/07・Canonical昇格の既承認を意味しない。

## 1. 三工程の成果物（今回まとめて審査する）

| Phase | 成果物 | 提出時点の内部判定 | 審査上の留保 |
|---|---|---|---|
| DOC-01 | [監査台帳](../doc01_review/README.md)／[全件構造検証](../doc01_review/90_doc01_stock_flow_verification.md) | `STOCK_FLOW_PREPARED / STATIC_CHECK_PASS` | 全122改訂正文の意味比較・Owner final review、anchor/非Markdown参照 |
| IF-01 | [Local CLI/Ports](../23_api_interface_design/23_41_e11_local_cli_scientific_ports.md)／[Result/Graph/Manifest/Artifact](../23_api_interface_design/23_42_e11_local_result_manifest_artifact.md)／[IF Review](../if01_review/90_interface_contract_review.md) | `IF_SPEC_DRAFT_COMPLETE` | Version/CLI grammar/Schema/atomic/privacyの正式Freeze・実行証拠 |
| DD-01 | [Domain/Ports](../30_detailed_design/30_61_e11_local_domain_ports.md)／[UseCase/Publisher](../30_detailed_design/30_62_e11_local_execution_publication.md)／[41 Method adapters](../30_detailed_design/30_63_e11_method_adapters.md)／[DD Review](../dd01_review/90_physical_design_review.md) | `DD_SPEC_DRAFT_COMPLETE` | exact package/reuse、actual Backend/Inference/FS tests、Method Science |

**Scope保証:** ENH-E11の68 Scope（DEC09）／41 Method（20+8+13）／新44 Requirements（19 FR、8 NFR、17 Scientific AR）、旧Product v2との共存・CLI-first・無Web/DB/Worker統合を維持。P1-M05のIV識別対象やMethod別Inference/Endpointの未確定を勝手に解消扱いにしない。

## 2. 一括審議する設計判断（Owner adoption pending）

| Decision | 審議対象／候補 | 技術評価と要修正条件 | 採否記録 |
|---|---|---|---|
| REV-01 | DOC Stock/Flow分類、原105件＋IF/DDの新5件=110件 | 原文・Status保持、Flow台帳隔離、Owner逐条意味審査 | PENDING |
| REV-02 | 302 Requirement IDsの整合・MOVE_BD19件一致 | 元正本へは未昇格。122件の意味保存再確認 | PENDING |
| REV-03 | E11独立CLI `ariadne-causal-local` とStudy/Result/Manifest/Graph Version `/1` | 旧 `causal-analysis-spec/2`との明示的dispatch／Compatibility | PENDING |
| REV-04 | 新E11 Domain Portと既存 `ScientificCorePort`/`ArtifactStorePort` の非同一性 | Adapter bridgeが必要、重複Package/実装範囲はsource再調査 | PENDING |
| REV-05 | Typed AR ConfidenceSetとEndpoint Tagged Union | DISCONNECTED/UNBOUNDED/ALL_REAL lossless。EMPTYは正常B0/B1では不可 | PENDING |
| REV-06 | staged bundle＋Manifest/Marker＋同一FS atomic no-clobber rename | FS、fsync、hash/readback、symlink/race、crash recoveryを受入試験 | PENDING |
| REV-07 | Local OS Principal＋個票CATE二重opt-in | Product RBACの擬似再利用禁止、security threat model実証 | PENDING |
| REV-08 | 41 Method→Adapter/Estimand/Inference Registry | FD-A、CATE7/DRIV-A、B0/B1/AR、Temporal、Quasi、SCM point-onlyの区別 | PENDING |
| REV-09 | DEC08 Extras/5 Profiles/ENV-RD別、SBOM/License | universal lock/Combined実測・顧客GPL法務審査未済 | PENDING |
| REV-10 | IF/DD/Gate06/07/Coding/正本昇格の権威分離 | Owner設計採用≠実装開始許可。科学/法務/テスト全件PASSの後に正本昇格 | PENDING |

Decisionごとに `ADOPT / ADOPT_WITH_CHANGES / REJECT / DEFER` の結果、採否理由、文書差分、Owner名／日付、確認対象Git Commit SHAを記録する。現時点では審査依頼でありOwnerの採否を推定しない。

## 3. Cross-phase findings（非重複の集約）

| Category | Unclosed findings | Resolution lane |
|---|---|---|
| DOCUMENT | DOC01-F01〜F05：逐条意味／anchor／Flow rootの古い計画状態 | DOC-01 owner/independent review |
| INTERFACE | IF01-F01〜F08：Schema/version/CLI、privacy、atomic、Method API、5 Profile、Legal | IF-01 → ADR Schema/Port freeze |
| PHYSICAL | DD01-F01〜F10：新Class/Module/reuse、FS fault、41 method science/config、runtime/permission、Source audit | DD-01 → Gate06 preflight and implementation |
| ARCHITECTURE | BD01-F03〜F13：11 open findings（旧BD Review） | Independent Architecture Reviewer |
| SCIENCE/RESOURCE | DEC07 FWER=0.05とK/R/MC/Compute、Method oracle/CI実測 | T2 Pilot→Freeze→T3→Independent Gate07 |
| LEGAL/DELIVERY | GPL/顧客別配布形態・Artifact SBOM | Legal/contract Owner |
| PRODUCT GAP | GAP-C01〜04はE11によって自動解消しない | Separate Product owner/workstream |

## 4. 受入とCoding境界

1. DOC/IF/DDのOwner最終確認により、**具体仕様Snapshot SHA**と全DecisionのDispositionを確定する。Owner修正要求は元StockのVersionとTraceに反映する。
2. 独立Architecture Review（BD01-F12）でPort/Schema/Physicalと既存Product reuse/directionを確認し、採用された設計のADRを発行する。
3. Gate06用のAcceptance、Work Package06/07、科学負例・Method別Reference/Env・Legacy regressionのベースラインをFreezeする。ここで初めてWork Package別のCoding Authorizationを判定する。
4. Coding開始後はImplementation/Contract/Fault/Security/Env結果とIndependent Science T2/T3を証拠として保存する。Science PASS/Legal PASSは別系統である。
5. **原正本 `docs/wiki/requirement_definition/` へはENH-E11の全対象テストPASS後のみ昇格**。Document Review Passだけでは昇格しない。

## 5. 今回の完了定義

- DOC-01：原105 Stock fileの移管/文書分類と静的Audit、302ユニークRequirement ID/19原文一致、Flow監査台帳の作業版がある。
- IF-01：CLI/Port/Result/Graph/Manifest/Atomic/Privacyの具体的Interface契約と負例Test一覧がある。
- DD-01：主要Class/Port Use Case/Publisherと41 Method adapter、scientific/technical negative、テストTraceの設計がある。
- **三つの設計成果物はこのレビューPackageへまとめて提出可能。** 実装・実行Test・独立レビュー・Owner採否は未完了として厳格に分離する。
