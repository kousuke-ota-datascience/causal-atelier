# ENH-E11 — DOC-01 / IF-01 / DD-01 一括Owner Review Pack

**Created:** 2026-11-16  
**Decision state:** `DOC01_OWNER_APPROVED / IF01_DESIGN_ADOPTED / DD01_DESIGN_ADOPTED / INDEPENDENT_REVIEW_PENDING / CODING_NOT_AUTHORIZED`。  
**Scope:** 正本候補のStock／Flow分離、Local Interface、Local Physical Design。Architecture・Method science・Coding・Legal・Gate06/07・Canonical昇格の既承認を意味しない。

## 1. 三工程の成果物（今回まとめて審査する）

| Phase | 成果物 | 提出時点の内部判定 | 審査上の留保 |
|---|---|---|---|
| DOC-01 | [監査台帳](../doc01_review/README.md)／[全件構造検証](../doc01_review/90_doc01_stock_flow_verification.md) | `STOCK_FLOW_PREPARED / STATIC_CHECK_PASS` | 全122改訂正文の意味比較・Owner final review、anchor/非Markdown参照 |
| IF-01 | [Local CLI/Ports](../23_api_interface_design/23_41_e11_local_cli_scientific_ports.md)／[Result/Graph/Manifest/Artifact](../23_api_interface_design/23_42_e11_local_result_manifest_artifact.md)／[IF Review](../if01_review/90_interface_contract_review.md) | `IF_SPEC_DRAFT_COMPLETE` | Version/CLI grammar/Schema/atomic/privacyの正式Freeze・実行証拠 |
| DD-01 | [Domain/Ports](../30_detailed_design/30_61_e11_local_domain_ports.md)／[UseCase/Publisher](../30_detailed_design/30_62_e11_local_execution_publication.md)／[41 Method adapters](../30_detailed_design/30_63_e11_method_adapters.md)／[DD Review](../dd01_review/90_physical_design_review.md) | `DD_SPEC_DRAFT_COMPLETE` | exact package/reuse、actual Backend/Inference/FS tests、Method Science |

**Scope保証:** ENH-E11の68 Scope（DEC09）／41 Method（20+8+13）／新44 Requirements（19 FR、8 NFR、17 Scientific AR）、旧Product v2との共存・CLI-first・無Web/DB/Worker統合を維持。P1-M05のIV識別対象やMethod別Inference/Endpointの未確定を勝手に解消扱いにしない。

## 2. Owner採用済み設計判断（後続検証は未完）

| Decision | 審議対象／候補 | 技術評価と要修正条件 | 採否記録 |
|---|---|---|---|
| REV-01 | DOC Stock/Flow分類、原105件＋IF/DDの新5件=110件 | 原文・Status保持、Flow台帳隔離、Owner逐条意味審査 | ADOPTED_AS_DESIGN_BASELINE |
| REV-02 | 302 Requirement IDsの整合・MOVE_BD19件一致 | 元正本へは未昇格。122件の意味保存再確認 | ADOPTED_AS_DESIGN_BASELINE |
| REV-03 | E11独立CLI `ariadne-causal-local` とStudy/Result/Manifest/Graph Version `/1` | 旧 `causal-analysis-spec/2`との明示的dispatch／Compatibility | ADOPTED_AS_DESIGN_BASELINE |
| REV-04 | 新E11 Domain Portと既存 `ScientificCorePort`/`ArtifactStorePort` の非同一性 | Adapter bridgeが必要、重複Package/実装範囲はsource再調査 | ADOPTED_AS_DESIGN_BASELINE |
| REV-05 | Typed AR ConfidenceSetとEndpoint Tagged Union | DISCONNECTED/UNBOUNDED/ALL_REAL lossless。EMPTYは正常B0/B1では不可 | ADOPTED_AS_DESIGN_BASELINE |
| REV-06 | staged bundle＋Manifest/Marker＋同一FS atomic no-clobber rename | FS、fsync、hash/readback、symlink/race、crash recoveryを受入試験 | ADOPTED_AS_DESIGN_BASELINE |
| REV-07 | Local OS Principal＋個票CATE二重opt-in | Product RBACの擬似再利用禁止、security threat model実証 | ADOPTED_AS_DESIGN_BASELINE |
| REV-08 | 41 Method→Adapter/Estimand/Inference Registry | FD-A、CATE7/DRIV-A、B0/B1/AR、Temporal、Quasi、SCM point-onlyの区別 | ADOPTED_AS_DESIGN_BASELINE |
| REV-09 | DEC08 Extras/5 Profiles/ENV-RD別、SBOM/License | universal lock/Combined実測・顧客GPL法務審査未済 | ADOPTED_AS_DESIGN_BASELINE |
| REV-10 | IF/DD/Gate06/07/Coding/正本昇格の権威分離 | Owner設計採用≠実装開始許可。科学/法務/テスト全件PASSの後に正本昇格 | ADOPTED_AS_DESIGN_BASELINE |

**Owner採用記録:** 2026-11-16の明示指示によりREV-01〜10の設計選択を採用。審査対象SHAは`c17f0baa01b66b24395cf8d96f6ae224d382cc7a`。正式な採否・残余検証は[Owner承認記録](91_20261116_doc01_if01_dd01_owner_approval_record.md)へ記録。採用と実装／科学／法務の証拠は別。

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
- **三工程の設計案はOwner採用済み。** 実装・実行Test・独立レビュー、Schema/Port Freeze、Coding許可は未完了として厳格に分離する。
