# IF-01 follow-up — Web API 10ファイルのContract粒度横断監査

**実施日:** 2026-11-17 JST  
**対象:** `23_10`〜`23_19`全10ファイル、`prototype/ariadne_mvp`。  
**文書種別:** Flow / Audit（23系Stockへ直接昇格しない）  
**判定:** `IF01_DESIGN_ADOPTED / WEB_API_OPERATION_CONTRACT_GRANULARITY_INCOMPLETE / SOURCE_OPENAPI_RECONCILIATION_PENDING`

## 1. 評価対象と検出結果

GitHubの現行分割版10ファイルを全文確認し、Markdownの`| GET/POST/PATCH/DELETE | Path | 用途 |`式行数、および本文のRequest/Response、Authorization、Error、Idempotency、Schema/Versionへの明示言及を確認した。キーワードや表の行数は*仕様の充足性を証明しない*ため、本文の意味も検査対象とした。

| ファイル | HTTP操作表の行数 | 仕様記述の実態 | 不足する代表項目と整合レビュー |
|---|---:|---|---|
| `23_10_api_project_context.md` | 11 | Method/Path/用途とFR-121が主。個別Request/Response Contractなし | Request body/query、Success DTO/status、対象Role/State、error＋code、idempotency、version |
| `23_11_api_dataset_view.md` | 10 | API一覧と一部response/Filter Error、schema。 | 各Operationの必須DTO、Lifecycle/Role、response/error binding、Version |
| `23_12_api_analysis_specification.md` | 7 | AnalysisSpec envelope/schema説明、resource操作 | Endpoint別Request/Response、State/Role/Error、idempotency scope |
| `23_13_api_exploratory.md` | 14 | NavigationとExploratory resource分離、一部Contract | 各操作のInput/Output、State/Role、Failure/Retry、Version |
| `23_14_api_causal.md` | 12 | Graph Version response fields、Idempotency-Key例、Causal Planner contract | 各操作のField requiredness、Role/State/error、VersionとGraph validation |
| `23_15_api_predictive.md` | 3 | Endpoint表の外にadvanced capability・subgroup responseなどの詳細あり | Operation別Request/response適用とAuthorization、HTTP/error、inference/versionの境界 |
| `23_16_api_execution.md` | 20 | Submit input、Execution response、Status、canonical/Pred別のpath表あり | 各POSTのerror/idempotency/Role/State、兩系統の意味的差分、Schema Version |
| `23_17_api_result_comparison_lineage.md` | 15 | ResponseやComparison/Lineage、historical projection記述あり | Data/Resultのread permission、export/create side effects、HTTP statuses、Version |
| `23_18_api_annotation_artifact.md` | 8 | Artifact/Annotation、Roleの一部説明 | Endpoint別Request/Output、idempotency、Error/HTTP、Artifact access policy |
| `23_19_api_frontend_support.md` | 0（表外でGETを定義） | Operation Availabilityにclosed vocabulary、query validation、RBAC、HTTP error、evaluation orderまで詳細 | 他の9文書との差が大きい。Read-only Catalogとの区別・Schema Versionの明示参照を確認 |

**注意:** 上記100行は`23_10`〜`23_19`内でMarkdown表行として書かれたHTTP操作数の合計であり、実装全体の重複除外後のendpoint数ではない。表外定義や重複pathがあるため、OpenAPI endpoint countと同一ではない。

## 2. 機能別に比較可能にする正規Contract Template

原`23_00_overall_IF.md`は界面ごとに①目的とAuthority ②endpoint/route/command identity ③input ④output ⑤Auth ⑥State ⑦Error ⑧Idempotency/Version ⑨context transferを要求する。現行の`Method/Path/用途`3列表だけではこの要求を満たしたことにはならない。

各操作または同一schemaを共有する操作群を以下で記述すること。

| Field | 必須の記述／参照方法 |
|---|---|
| ID / Authority | Interface種別、Operation/HTTP verb、resource、既存or提案、Source/Schemaへの参照 |
| Request | path/query/body DTO、type、requiredness、validation、base URL（`/api/v1`等） |
| Success Response | Status code、Schema/Version、required fields、result/content type |
| Auth | 認証Identity、Project/Resource boundary、Role／sensitive output | 
| State / Side effect | Mutation許容State、persistence/Executionへの作用、read-onlyなど |
| Error | validation/not found/conflict/forbiddenとHTTP＋canonical error code |
| Retry / Idempotency | applicable/N/A（理由）、key scope、同request replay、conflict |
| Compatibility | Old/new version、legacy behaviour、source of truth／dependent Port |
| Test / Trace | positive/negative、FR/NFR/AR、受入Gate、未実施はNOT_RUN |

共通規約へ参照する場合も各操作で`Inherited from 23_01 §X`と明示する。Not Applicableは理由を明示。全GETへ同じ分量の文章を書く必要はないが「説明なしで動作を推測する」状態は不可。

## 3. 認証契約の重要な不一致

`23_01_common_conventions.md` §3.2.1は、現行でBearer/OIDC共通middlewareがなく、`X-User-Id`や`anonymous`を使用する実装があると説明している。§3.2.3は**全project-scoped routeでProjectMembership認可を行う**と規定している。

両者は「現行の事実（CURRENT）」と「適用される要求（REQUIRED）」を明確に分ければ両立可能だが、**現在すべてのrouteで実装済みと読むことはできない**。API Contractには`CURRENT_OBSERVED / REQUIRED_TARGET / NOT_VERIFIED`を分け、各routeの認証・認可Implementation Traceを別途作成する。

## 4. 修正Acceptance

1. 実コード／FastAPI OpenAPI／Pydantic schemaの実在Routesを照合して、API operation全件表を重複排除し、正本authorityを決める。
2. 10ファイルのWeb API全操作に対して上記Contract Fieldの`DEFINED / INHERITED / N/A / NOT_SPECIFIED`を記録する。NOT_SPECIFIEDを暗黙既定としない。
3. 現行コードの実態と承認された将来要件は別列とし、文書を強制的に「実装済み」と書き換えない。
4. ContractのField/MIME/Versionの変更は後続Schema/Port Freezeへ引き渡す。E11新Local CLIを現在の`/api/v1`に追加したと誤解しない。
5. 検証済みSource SHA／実効Schema／API Error negative testを持ってIndependent Architecture／Gate06へ提出する。

**本監査は欠落の診断であり、未取得のOpenAPI/Source事実を想像して補う作業ではない。**