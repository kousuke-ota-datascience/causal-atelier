# 22_23 — ENH-E11 Optional Backend / Security / Compatibility / Delivery

**State:** `BD01_REVISED_DESIGN / OWNER_ARCHITECTURE_POLICY_ACCEPTED / INDEPENDENT_REVIEW_PENDING / IF_DD_SCHEMA_UNFROZEN / NOT_IMPLEMENTED`  
**Date:** 2026-11-16. **Authority:** [DEC-SR04-09](../../../working_notes/20261116_sr04_dec09_scope_requirements_architecture_gate_integrated_owner_approval.md), [formal RD-03 trace](../../doc01_review/rd03_review/96_rd03_formal_requirement_traceability.md), [RD-04 audit](../../doc01_review/rd04_review/98_rd04_consistency_verification.md). 本文のPort名・層は論理的な責務名称であり実装済Class/Schemaを意味しない。

## 1. Environment design decision (DEC08 A1〜A8)

- **Dependency declaration:** `pyproject.toml`にOptional Extraを明示し、`uv.lock`は1つのuniversal resolutionとして扱い、Manifestは実効Profileとライブラリversionを記録する。Lock単独ではBackend/Science/LegalのPASSを意味しない。
- **Baseline:** DEC08採用対象はUbuntu 24.04 / CPython 3.12.x / x86_64 / CPU。OS・Python patch・BLAS・native ABIが異なれば暗黙保証しない。
- **Current status:** 現行`uv.lock`へDoWhy/EconML/Tigramite等のE11 extrasを追加したことを本書は主張しない。

| Profile | Scope | Backend / key checks | Status |
|---|---|---|---|
| ENV-BASE | Core-only | E9/v2回帰と未導入Method unavailable | Adopted plan; not tested with new lock |
| ENV-DOWHY | E11 DoWhy | Identification/FD-A実効APIと旧CLI回帰 | Adopted plan; not tested with new lock |
| ENV-ECONML | E11 EconML | CATE/DRIV、nuisance、CI availability | Adopted plan; not tested with new lock |
| ENV-TIGRAMITE | E11 temporal | PCMCI family、CI test、Graph endpoints | Adopted plan; not tested with new lock |
| ENV-COMBINED | DoWhy + EconML + Tigramite | Combined conflict・legacy・Science | Adopted plan; not tested with new lock |
| ENV-RD | RD追加候補（初期5件外） | Sharp/Fuzzy RD実効API、推論、GPL顧客配布 | Conditional / not automatically approved for delivery |

- 各Profileはfresh isolated venvで`uv lock --check`、`uv sync --locked`、`uv pip check`等の適合検証を行い、`--frozen`をlock stale検証と取り違えない。Runtimeでは`--no-dev`等の環境要件を明記する。
- 41 MethodごとにBackend/Version/APIを照合し、選択Methodのincompatible/missing状態は**typed unavailable**として結果・Manifestへ反映する。予期せぬfallbackは認めない。
- Effective environment provenanceとSBOM/LicenseはRelease候補のSource SHA/Lock SHAおよび実効wheel/sourceをTraceする。実測なしにbitwise reproducibleを保証しない。

## 2. Local security model (not Product RBAC)

| Trust boundary | Required behavior | Open contract |
|---|---|---|
| CLI runner identity | 実行主体はlocal OS実行者。Product `X-User-Id`/Project Roleを強制前提としない | OS user/privilege model and delegation |
| Input Path | Root/path allowlist、traversal・symlink escapeを拒否 | canonical root/reparse/TOCTOU strategy |
| Config / Serialization | Versioned typed inputのみ受入。未信頼のpickleなど任意code実行を既定経路で許さない | exact parser/allowlist |
| Output directory | private artifact root、権限・umask等を設計し、失敗時も保護 | filesystem support, ACL/permissions |
| Row-level CATE and individual explanations | 明示的opt-inと機微Artifact扱い、許可されたexportに限定 | 実行者・承認者の関係、Policy authority / evidence |
| Manifest/Logs | Credential・機微列・個票値を原則含めず、hashや統計量を記録 | deidentification/log retention |
| Backend | optional codeを実効版・license・安全性基準で選別 | package audit and runtime isolation |

Productの`OWNER/EDITOR/VIEWER` RBACはProduct laneの既存契約であり、**Local CLIの個票出力の認可をProduct membershipなしで説明できる設計**が必要。これは未解決のBD-01 blocking itemである。明示opt-inだけであらゆる漏洩対策が完成したと解釈しない。

## 3. Compatibility and regression boundary

- `causal-analysis-spec/2`と旧CLI parser/Result/overrideの意味を保護する。新Local E11のversioned schemaは別dispatchし、old v2を暗黙移行させない。
- Product Web API、Frontend、Worker、DB migrationには新E11のroute/field/role/Stageを追加しない。既存Productの認証上の不完全性をE11の設計で解消済みと宣言しない。
- Local Scientific Core共有部分の改変が既存E9/E10機能・Predictive Model Loader/SHAP/LIMEに影響しないことを回帰試験で確認する。
- Product GAP-C01〜04は明示的に別Workstreamへ残す。担当・期限未確定のものをE11 CLIのテストPASSでClosedにしない。

## 4. Licensing and delivery boundary

- Internal Science使用、顧客へのwheel/container/sourceのSI納入、クラウドサービス提供で法的評価の対象は異なる。License種別・実配布Artifact・受領者・結合・通知・ソース提供・契約条件を法務とOwnerが審査する。
- DEC08の記録ではTigramiteのGPLv3-or-later、およびrdrobust PythonのGPL-3.0-onlyが審査対象候補として挙げられている。**本書は個別法務判断をしない**。
- Mandatory Science PASS／Environment PASS／Legal Delivery APPROVALは独立状態。GPLをoptional extrasにすることだけでは顧客配布の許可条件を満たさない。

## 5. Test / owner follow-up

ARC09-02/04/06/07、E11-A-02/04/06/07；FR-195/201/203、NFR-029/031/032/033/034/036。未完了の実効Pin/lock/5 Profile/Method API、OS policy、個票export authority、Legal Approvalは[BD-01 review](../90_architecture_consistency_review.md)へ引き渡す。
