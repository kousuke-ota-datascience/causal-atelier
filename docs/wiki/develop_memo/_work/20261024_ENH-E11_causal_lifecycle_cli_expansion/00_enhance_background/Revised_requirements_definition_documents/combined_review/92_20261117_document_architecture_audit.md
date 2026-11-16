# DOC-02横断監査 — 90番台の配置・23 Interface粒度・30物理Classテンプレート

**実施日:** 2026-11-17 JST  
**対象Snapshot:** `prototype/ariadne_mvp` / `a24e7d528c39f3869a43443ddbaaa588986e2741`。  
**区分:** `FLOW / AUDIT / REWORK_FINDINGS`。この文書自体は10/21/22/23/30のStock本文に昇格しない。  
**監査判定:** `REWORK_REQUIRED / NO_CANONICAL_PROMOTION / NO_CODING_AUTHORIZATION`。2026-11-16 OwnerのDOC-01承認、IF-01/DD-01設計方針採用そのものを無断撤回しないが、文書構成・API仕様粒度・詳細設計粒度の適合を未達と判断する。

**関連監査:** [DOC-01側の同日構造監査](../doc01_review/92_numbering_stockflow_and_class_template_audit.md)。同監査はDOC-01の根拠資料、本書はIF/DDを含む横断Finding／修復優先順位の集約記録として扱い、両者の内容を別々の承認済み規範とみなさない。

## 1. ルート90〜98番台：全8件の役割とDisposition

`Revised_requirements_definition_documents/`の番号付き5文書群が将来のStock候補であるのに対し、ルート直下の90〜98は「どう変更・確認・判断したか」のProcess／Trace／Evidenceとして作成された。正本候補の階層に混在させる必然性は薄い。

| 現ファイル | 調査した実際の役割 | 性質 | 推奨移管先（案） |
|---|---|---|---|
| `90_structural_split_verification.md` | Split前後のblob同一性・構造監査の歴史的Snapshot | FLOW / Historical Audit | `doc01_review/structural_migration/` |
| `92_rd02_restructure_verification.md` | RD-02 57件移管／元正文の構造保存証跡 | FLOW / Migration Audit | `doc01_review/rd02_migration/` |
| `93_enh_e11_canonical_promotion_policy.md` | ENH-E11限定のOwner昇格判断と検証条件 | FLOW / Owner Governance Decision（有効期間中は拘束力あり） | `combined_review/decisions/`または`doc01_review/decisions/` |
| `95_rd04_fr_application_review.md` | 既存FR195中の改訂条文対照とDisposition | FLOW / RD-04 Review | `doc01_review/rd04_review/` |
| `96_rd03_formal_requirement_traceability.md` | 68 Scope／41 Method／10 UC／E11 44発行の根拠・監査Trace | FLOW / RD-03 Trace-Audit（正文のauthorityではない） | `doc01_review/rd03_review/` |
| `96_rd04_nfr_ar_application_review.md` | 既存NFR36・科学的AR27の改訂対照 | FLOW / RD-04 Review | `doc01_review/rd04_review/` |
| `97_rd04_e11_requirement_review.md` | E11新44条文の逐条Review証跡 | FLOW / RD-04 Review | `doc01_review/rd04_review/` |
| `98_rd04_consistency_verification.md` | RD-04の122改訂条文・移管・正本境界の照合 | FLOW / RD-04 Audit | `doc01_review/rd04_review/` |

**Disposition:** 全8件をRootの将来昇格対象と混同しない。移動前に**全backlink／相対パス／画像・アンカー／Root READMEとFlow引用**の依存棚卸しを行い、Git moveに相当する内容同一移管と参照修復を同一変更にする。証跡を削除しない。特に`93`の承認ポリシーは移管しても効力が失われないよう入口とOwner発言・Snapshotを保存する。

## 2. 23系：ENH固有文言と恒常Interfaceの分離

| 文書 | 分類と具体所見 | 推奨処置 |
|---|---|---|
| `23_41_e11_local_cli_scientific_ports.md` | **MIXED**。E11固有Method/Version/IF-01テスト文言を含むが、Local CLI・Port/Status/Version/Capability contract本体は将来も必要な**Stock**。 | 公開・永続契約をStockへ保持し、IF-01進行状態／Reviewer判断／Gate検証証跡を`if01_review/`へ。正式contract identityとE11字句の恒久採用はSchema Freeze時に判断 |
| `23_42_e11_local_result_manifest_artifact.md` | **MIXED**。Result/Graph/Manifest/Publish/Privacyの約束はStock、`## 9. IFテスト`等のテスト実施・工程根拠はFlowとして独立可能。 | 受入不変条件はStock、テストCase／実行証跡／未確定の実FS・法務事情はReview/Gateへ責務分離 |
| `23_40_cli_library.md` | **MIXED**。既存CLIと新Localの互換性境界はStock。`新Interfaceのコード実装は別工程`等は進捗の説明。 | 有効契約のみStock、実装状況はFlow。さらに`## 7.1.`は親`## 7.`の直下なので`### 7.1`相当へ階層修正 |
| `23_99_change_log.md` | **FLOW**。ENH-E2〜E10の変更過程／CHANGEPOINTを記録。現行Contract本文の権威ではないと明記済み。 | `if01_review/`ではなく、複数Enh共通の変更履歴用`history/`または`doc01_review/history/`へ隔離。差分だけが規範になる箇所は責務別Stockへ反映 |
| `23_90_interface_verification.md` | **STOCK寄り**。実行結果ではなく恒常的なInterface verification obligationsを列挙。 | 不変条件・受入契約としてStock可。ただしテスト実施StatusはFlowに置く。文中の`§11〜12`など参照先の文書群を明示 |
| `23_00`〜`23_20`、`23_30`、`23_50`〜`23_52` | 基本は既存Productの現行Interface契約。ENHで追加された条文も、恒常的な契約ならStockで正しい。 | `ENH-E10`等の出自を残す場合も、現行契約の義務と過去の工程説明を分離 |

**重要:** ファイル名に`e11`が入ることのみではFlowと判定できない。判定単位は**section / clause**。ただし`e11-local-study/1`等を永続的な外部Versionとして採用するかは単なるファイル名問題ではなくCompatibility設計判断。2026-11-16のOwner案採用後であるため、無断Rename/Schema変更は行わない。

## 3. 23系：通し番号の不整合（AUD-IF-NUM-01）

元正本`docs/wiki/requirement_definition/23_api_interface_design.md`の共通章順は、`## 1`〜`## 3` → `## 4. Browser Navigation Interface` → `## 5. Web API Interface` → `## 6. Worker` → `## 7. CLI` → `## 8. Cross-cutting` → `## 9. Verification`。

- `23_01_common_conventions.md`: `## 3`が最終。
- **`23_20_browser_navigation.md`: `## 4`が実在**。欠落ではないがファイル番号順だと`23_10`の後になる。
- `23_10_api_project_context.md`: `## 5`と`### 5.1`が先に表示される。
- `23_40_cli_library.md`: `## 7`の後、`## 7.1.`を同レベルに置く見出し階層誤り。
- `23_41`、`23_42`は**各ファイル独立の`## 1`〜`## 8/9`**。旧全体章番号体系と独立採番体系が共存し、単に「§1」と書くと参照不明瞭。
- `23_99`は`## 20`の歴史的章立て。現行Contractの続きとして読ませない。

**推奨修復方針:** 23群では**全体章番号を維持するなら章の読み順とファイル配置を一致**させる。例：Browser Navigationを早いファイル帯へ移すか、目次で章順を明示して章節Anchorの解決規則を固定する。Local独立Interfaceは別 namespace／章体系として区別し、無関係な旧全体章番号`§1`と混同しない。大規模な見出し変更はリンク・Anchor参照修正と一括で検証する。

## 4. 23系：APIファイル間の粒度不整合（AUD-IF-CONTRACT-02）

| 比較 | 実際に確認した内容 | 不足・不整合 |
|---|---|---|
| `23_10_api_project_context.md` | Project/Research Context約11 HTTP操作を主にMethod/Path/用途として列挙し、FR-121を付記 | 操作別Request body/query/path、Response DTO、HTTP status、422/404/403、State/side effect、IdempotencyとVersionが省略または他文書参照不明 |
| `23_11_api_dataset_view.md` | Dataset/AnalysisView operation list、代表response fields、Filter validator/error | 一部詳細がある一方、操作ごとのDTO/requiredness、Lifecycle/権限、成功・失敗HTTP statusの結合が不足 |
| `23_15_api_predictive.md` | capability metadata、split response、subgroup結果とtyped errorまで比較的詳細 | 同じ23群でもOperation間に記載レベル差。例示JSONは全field必須のSchemaとは別だと区別が必要 |
| `23_19_api_frontend_support.md` | Operation Availabilityのclosed key taxonomy、query 7条件、authorization、Error、Evaluation orderまで詳細 | これに比べ23_10等はInterfaceとして再実装可能な粒度に未達 |

**統一する最低限のContract Template（API operation又は同一Schema群）:** (1)Identity/AuthorityとHTTP Method/Path、(2)Request path/query/body + constraints、(3)Success response DTO/schema/version/status、(4)認証・認可とproject scope、(5)state prerequisite・side effects・lifecycle、(6)validation/error+HTTP status、(7)idempotency/retry、(8)compatibility/versionと依存Port／source、(9)Contract/Negative tests・FR/NFR/AR trace。共通規約への参照は許容するが、「省略＝暗黙の既定」にはしない。全GETで同量の説明を重複記載する必要はなく、共通参照+差分でよい。

**Source of truthの区別:** 現行Source／OpenAPIから実在仕様を採取し、設計上必要だが実装がない項目はPROPOSEDと明記。表・JSON例のみから現実のSuccess/Failure statusを推測して記載しない。

## 5. 30系：番号の所在と重複（AUD-DD-NUM-01）

旧正本`30_detailed_design.md`は`## 3` → `## 4. Application navigation state` → `## 5. Analysis Context` → `## 6...`という連続章立て。

- `## 4. Application navigation state`と`## 5. Analysis Context`は **`30_41_navigation_routing.md`内にある**。前段の`30_10_domain_resources.md`には`## 3`があり、ファイル番号順では飛ぶ。
- **`30_21_execution_runtime.md`には別の`## 4. ExecutionOutcome / GenericExecutor`も存在。**
- **`30_20_planning_validation.md`では`## 9`の後に`## 2. PlanValidator`、`## 3. StageRunnerRegistry`を記載。**
- `30_10`には`## 5. GraphVersion`、`30_50`には`## 6. StoredArtifact / ArtifactStorePort`、`30_60`には`## 7. CliManifest`と`## 8. ENH-E11...`を置き、旧全体章番号`3〜24`と重複。
- `30_01_class_design_template.md`に`## 8. Verification boundary`と無採番の`## Common class...`があり、章の責務が混在。

**判定:** 4がないのではなく、**章の非単調配置と重複採番**。同一文書群のグローバル章番号として現在の値を解釈することはできない。全文の既存Heading/Anchor backlinksを確認したうえで、Topic設計とClass物理詳細を分離し採番系を単一化する必要がある。

## 6. 30系：Ownerの7区分Classテンプレート不適合（AUD-DD-CLASS-02）

Owner指定の例：`### 5.X. ClassName`の下に、`#### 5.X.1`識別/責務、`.2`フィールド、`.3`Constructor/Factory、`.4`メソッド、`.5`処理仕様、`.6`I/O・失敗、`.7`検証を置く。非該当項目は理由付きN/A。

| 対象 | 現状の実例 | 判定 |
|---|---|---|
| `30_61_e11_local_domain_ports.md` | `ContentRef`等を`## 2`〜`## 8`に分割。下位は「fields」「methods」「tests」など約3区分。複数Class／Portを一節に混載 | **FAIL**。7区分のClass/Protocol単位の表、責務外、Constructor invariants、Exception、State/transaction、Gateが未整理 |
| `30_62_e11_local_execution_publication.md` | `E11LocalCausalUseCase`は5下位節、`LocalArtifactPublisher`は5節、`LocalPrivacyPolicy`は3節、ReaderとManifestを同節に混載 | **FAIL**。特にValidation、CommitとRecovery、実装Constructor/State、I/O/失敗を明確なClass単位に分類できていない |
| `30_63_e11_method_adapters.md` | Method ID 41件のAllocation表、Backend別数理概要は存在。Adapter Classはまとまった責務記述で7区分なし | **FAIL**。Method IDの41行網羅とClassの実装仕様網羅は別物。実際のAdapter Class単位で必須7区分＋Method-specific設定・負例Traceが必要 |
| `30_20_planning_validation.md` | `PlanValidator`／`StageRunnerRegistry`をFields/Method/Negativeで要約 | **FAIL**。Classごとに7区分なし。Existing Source SHAや詳細検証Traceは別箇所に偏在 |
| `30_21_execution_runtime.md` | `ExecutionOutcome`と`GenericExecutor`を一節に混載 | **FAIL**。Value objectとExecutorが同一Class Specになっている |
| `30_10_domain_resources.md` | `GraphVersion`のClass仕様が`## 5`で簡略記載、他のDomain value objectも章内に集約 | **FAIL / 対象Class inventory精査必要** |
| `30_50_persistence_artifacts.md` | `StoredArtifact`と`ArtifactStorePort`を`## 6`で一括説明 | **FAIL**。DTOとPortは個別7区分 |
| `30_60_cli_adapters.md` | 旧`CliManifest`のFieldと`to_dict`などの要約、別節にE11分離 | **FAIL**。Existing Classテンプレート7区分未達 |
| `30_01_class_design_template.md` | Owner採用7区分の**雛形テキスト**は存在。ただし同ファイルの実クラス説明はない | **Template exists**。ここがあることは30群の実Class定義が適合することを示さない |

**強制修復ルール:** (a)Class/Protocol/DTOを個別Inventory化、(b)各Classに7区分・必須表を記述、(c)Existingは実Source/constructor/method/exceptionを固定SHAで照合、(d)Proposedは未決signature/variantを明示して架空の実装を作らない、(e)Module-level関数も対応するI/O/副作用/error/testを記述、(f)科学MethodはClass Specと別にEstimand/Identifiability/InferenceのMethod別Contractを維持する。7区分の空見出しを機械的に作るだけでは解消しない。

## 7. 優先修正順序とAcceptance

| 優先 | 作業 | 完了判定 |
|---|---|---|
| P0 | Rootの全8 Flow文書移管計画、Stock混入分離、23_99履歴の配置確定 | 責務・権威・参照先が明瞭で、リンク切断と正文欠落がない |
| P0 | 23/30の番号空間の方針統一、読み順／重複解消、参照/Anchor修復 | 当該文書の章番号が読み順に単調、重複Namespaceなし、番号参照が解決できる |
| P0 | 30系のClass inventoryを実Sourceと照合、Owner7区分をクラス単位で再記述 | すべての対象Class/Port/DTOに7区分・N/A理由、Field/Signature/I/O/Gate/Source対応がある |
| P1 | API全操作の最低契約欄をSource/OpenAPIで補完 | Operation × 必須欄のCoverage、共通規約参照と例外が明確、実在・提案の区別 |
| P1 | 23_41/42の恒常ContractとENH固有のTest/Gate進行状況を分割 | 仕様上の要件が失われず、履歴／進捗が正本へ混入しない |
| P1 | 独立DOC/IF/DD内容レビュー、Backward compatibility、Gate受入を再確認 | 独立証拠・Owner/Reviewerの明示DispositionまでPASSとしない |

**未実施:** 全Source symbolの逐条signature照合、全REST実装/OpenAPIとのcontract equality、全Markdown Anchorの機械検査、全既存条文122件の意味比較、全File移動後のリンク再照合、実行テスト。現段階でそれらをPASS扱いしない。

**結論:** 2026-11-16のDOC/IF/DD Owner採用は設計方向の承認として保持できる。しかし、文書の最終品質としては**Stock/Flow分離、章番号、API Contract、Class詳細設計の4点が未完成**。実装前にこの構造的負債を閉鎖すべきである。
