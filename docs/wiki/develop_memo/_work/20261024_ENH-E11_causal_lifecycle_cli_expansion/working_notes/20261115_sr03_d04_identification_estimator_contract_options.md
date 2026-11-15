# ENH-E11 — SR03-D04 識別結果と推定器の接続・v2互換性：技術審議記録

**文書区分:** working_notes／未承認の技術比較・推奨。正式FR/NFR/AR、Architecture Review、Gate 06/07、コーディング許可ではない。  
**記録日:** 2026-11-15（JST）  
**判断状態:** SR03-D04_TECHNICAL_RECOMMENDATION_PREPARED / OWNER_DECISION_PENDING / SCIENCE_NOT_RUN  
**照合したHEAD（作成前）:** prototype/ariadne_mvp = 3c3e69148d0549eb9c2f693179fc4b4608359007  
**既採用前提:** D01 IV_HETEROGENEOUS_EFFECT独立family、D02 Frontdoor数値推定、D03-1 S2（B0+B1）、D03-2 I2（AR反転）、D03-3 G2改訂（型付き集合）、D03-4 C1（推定器Cは後続審議）。全体構想の承認状態はPENDING_FULL_CONCEPT_APPROVAL。

## 0. 目的・権威・非対象

D04はDoWhy等の識別結果をAriadneの意味保存型IdentificationResultに正規化し、CausalQuestion／Design／Estimand／EstimatorSpecを照合した場合だけ、EconML等の新Methodを数値推定へ渡す科学契約を審議する。ライブラリが返す数値・内部Estimand名・graphical identification成功だけをもって科学的な実行許可としない。

本書をD04の選択肢・反証・推奨の詳細記録とする。採用されたHuman owner判断のみ[02構想承認記録](../00_enhance_background/02_enhancement_concept_approval_record.md)へ追記する。横断進捗は[SR-03総合メモ](20261101_sr03_identification_estimand_estimator_contract_review.md)、ScopeのDispositionは00_04、要件・設計は03/04、追跡は05へそれぞれ保管し、同一詳細を重複保守しない。

**非対象:** D05の個別CATE/DRIV推論可否とCI必須水準、D06のCPDAG/PAG追加識別・owner override確定、SR-04/Gate07の数値閾値・coverage採否、Product API/UI/Worker/DBへの新規統合。これらをD04承認とみなさない。

## 1. 現行実装との照合（コードから確認できる事実）

| 照合箇所 | 現状 | D04への影響 |
|---|---|---|
| src/ariadne/product/domain/analysis_spec.py | SCHEMA_VERSIONはcausal-analysis-spec/2。unknown fieldは拒否し、causal_question.estimandはATE/ATT、IDENTIFICATIONのstrategyはRANDOMIZED/BACKDOORに限定。causal_question_hashはquestion dictだけをJSON正規化してSHA256化。 | v2へ新字段を黙って投入できない。Design hash、対象コントラスト・Method固有対象の識別には新契約が必要。 |
| src/ariadne/interfaces/cli/config_schema.py | 各CLIのconfig_versionはLiteral["2.0"]。EstimationのMethodはdiff/OLS/IPW/AIPW系6別名。 | 新Methodには明示的なversion/variantの配線が必要。 |
| src/ariadne/interfaces/cli/scientific_stage.py | Identification出力Manifestはmanifest_version="2.0"、IDENTIFICATION_RESULTとDATA_ELIGIBILITY_RESULTをresult_summaryに同梱。dataset/graph hash・question hashは保存、backend_versionは固定文字列。 | 新Resultは現行v2 Resultを無条件に上書き・再解釈しない。effective optional backend versionは別に記録する。 |
| src/ariadne/interfaces/cli/estimation.py | upstream identification_statusにIDENTIFIEDとREQUIRES_REVIEWを許容。Eligibility=WARNではvalidation_overrideを確認するが、CLI関数の当該箇所ではIDENTIFICATIONのREQUIRES_REVIEWに対するoverride確認がない。上流Manifestからstrategy/adjustmentを読み、現行compatibility validatorを呼ぶ。 | 新E11経路ではREQUIRES_REVIEWを明示的にfail-closedにする。現行Product／v2経路の挙動変更は別途影響審査。 |
| src/ariadne/product/application/scientific_validation_service.py | Product経路はQuestion hash、DatasetVersion、GraphVersion、upstream Result type、eligibility、Method capabilityを検証し、REQUIRES_REVIEWに対してoverrideを要求。 | Product互換を保持しつつ、新規CLIだけにより厳しい非識別禁止規則を定義する。 |
| src/ariadne/scientific/identification/adapter.py | Native Randomized/BackdoorのDAG判定とData Eligibility Resultを返し、非DAGをREQUIRES_REVIEWで保持。 | Native結果の再利用可。DoWhyの内部オブジェクトを新規portable resultへ直列化しない。 |
| src/ariadne/scientific/inference/adapter.py | binary treatment ATE/ATT、DAG、既存Method向け。非DAGは負結果を返す。 | 新Estimatorが既存Native adapterの処理能力を持つと仮定しない。 |

**評価上の留保:** CLIがREQUIRES_REVIEWを入力許容することはコード上の事実だが、非DAGでは下流adapterが拒否する分岐もある。「現行CLIで任意の未識別結果から数値が必ず出る」とは主張しない。上流Dataset/Graph hashと下流入力とのクロス実行照合、Design hash、MethodごとのEligibilityの欠落は新契約の是正候補であり、全経路の実測脆弱性を証明したものではない。

## 2. D04-1：互換性・versioningの選択肢

| 案 | 内容 | 利点 | 欠点／リスク | 技術評価 |
|---|---|---|---|---|
| V1：v2内に追加 | causal-analysis-spec/2の許容項目・enumを増やし既存readerも同時に変更 | バージョン分岐が少ない | strict v2 readerでunknown field拒否。既存Product受入意味の変更・旧manifestとの曖昧な互換を生む | 非推奨 |
| **V2：v2保護＋新たなCLI-only版付き契約** | v2の入力・reader・出力を維持し、新E11用local spec / identification / effect / manifestをversion dispatch。内部で必要なPort/Domain型を再利用する | 既存E5〜E10回帰と新Methodの科学的意味を分離。移行・併存試験可能 | 2系統readerとversion変換規則が必要 | **推奨（Owner未採用）** |
| V3：backend objectを直結 | DoWhy IdentifiedEstimandやEconMLのオブジェクトをそのまま下流へ渡す | 短期コード量は少ない | backend結合、再現性・portable JSON破綻、Estimand誤表示とCI差の管理困難 | 非推奨 |

V2の命名例はlocal analysis spec = causal-analysis-spec/3、config_version = 3.0、manifest_version = 3.0とするが、**文字列・正式schema versionそのものは未決**。新CLIの読取はversion必須で分岐し、v2読取は従来どおりv2として扱う。v2 Artifact/Manifestを新Methodに無言で昇格させない。必要なら明示的なmigration commandと新たな識別検証・lineageを要求し、未検証なら移行を拒否する。

## 3. D04-2：Normalized Resultと実行許可の境界

### 3.1. 推奨データ責務（正式field名ではない）

| オブジェクト | 所有する意味 | 必須候補 |
|---|---|---|
| CausalQuestion | 研究者が定義した対象。Effectの集団・尺度・処置比較を先に固定 | question_id/hash、target_population、analysis_unit/time、treatment/control/contrast、outcome、estimand_family、estimand_definition、effect_modifiers |
| CausalDesign | 識別を正当化する候補根拠 | strategy、Graph ref/type/hash、adjustment_set、mediators、instruments、assignment mechanism、assumption declarations（根拠・assessor・機械的検証可否） |
| IdentificationResult | **指定されたEstimandの識別評価**と証拠の正規化（DoWhy等の生オブジェクトではない） | result_id/schema_version、question/design/dataset/graph hashes、strategy、normalized expression、target、assumption evidence、identified adjustment/instrument/mediator、status＋reason_codes、backend/version、lineage、candidate_method_families（実行保証ではない） |
| EstimatorSpec | そのMethodが**その研究Designと対象**を扱えるかを静的・動的に判定 | method_id/version、supported_strategy/estimand_definition、treatment/instrument/outcome types、required_columns、nuisance/crossfit、inference_capability、required assumptions、method-specific eligibility rule |
| EffectResult | 実行した数値と科学的意味・推論可否を混同せず保存 | analysis identity＋upstream result ref/hash、method/config/backend/version、point/point_status、uncertainty_status、confidence_interval/confidence_set、diagnostics、warnings、scientific_status、artifact hashes |

**authority:** Question/Design/Methodの科学的意味とeligibilityはAriadneの外部ライブラリ非依存の型・Validatorが管理する。DoWhyは識別候補と根拠を出すbackend、EconML等はMethod実行backend。CLIはportable input/output、version dispatch、hashとmanifestを管理する。既存ProductのDB Resource/Result authorityは変更しない。

**重要:** DoWhyの非パラメトリックATE向け識別結果がIV経路を含んでも、それだけでcomplier LATE、B1の線形構造係数、IV heterogeneous effectへの変換を保証しない。Method固有の識別式・対象・追加仮定をAriadneで独立に照合する。DoWhyのproceed_when_unidentifiable等をAriadneの自動実行許可flagと同一視しない。

### 3.2. Compatibility / eligibility matrix（候補、未承認）

| Graph / Strategy | Target estimand | Method候補 | 数値推定の必要条件／禁止事項 | D04の仮判定 |
|---|---|---|---|---|
| fixed DAG / RANDOMIZED | ATE（binary A） | Native diff/OLS/IPW/AIPWの現行適合部分 | 比較・対象・既存Validationを維持。新規CATEへ流用しない | 既存v2の回帰保護 |
| fixed DAG / BACKDOOR | ATE/ATT | Native OLS/IPW/AIPW | adjustment一致、positivity、Estimator個別のTarget対応 | 既存v2の回帰保護 |
| fixed DAG / BACKDOOR | CATE（conditional ATE） | Phase2のDML/DR/Meta群 | effect modifierと交絡調整を区別、各xのsupport、モデル・splitとMethod適合。ATEの識別のみをCATEの科学受入証拠にしない | 条件付き新契約候補 |
| fixed DAG / FRONTDOOR | ATE（指定母集団） | Phase1数値Frontdoor estimator | Mediator M、frontdoor条件、モデル・識別式に整合した数値推定、識別≠推定品質 | 新契約で条件付き許容候補 |
| fixed DAG / IV | binary Z/Aのcomplier LATE | Phase3 Wald / B0 just-ID 2SLS | relevance、independence、exclusion、monotonicityの宣言・根拠、support。弱IVはAR型confidence setを別出力 | D03の採用範囲として新契約候補 |
| fixed DAG / IV | B1の加法線形IV構造係数 | Phase3 B1 2SLS | pre-treatment C、単一Z/A、構造モデル仮定、正しいIV推論。LATE/ATE/CLATEへ自動再分類しない | D03の採用範囲として新契約候補 |
| fixed DAG / IV | IV_HETEROGENEOUS_EFFECT（Method固有） | Phase2 DRIV等 | theta_IV(x)、モーメント、処置/IV型とcontrast、nuisance条件をMethod別に特定。fit成功からCATE/LATEへ読み替えない | D05／SR04の具体化待ち |
| fixed DAG / IV | 条件付きcomplier LATE用C | 将来の推定器C | D03-4 C1により初期実装非採用。Method固有の審議TriggerとOwner採否が必要 | 初期BLOCKED（スコープ外） |
| CPDAG/PAG / 任意 | ATE/ATT/CATE/LATE等 | 新E11数値Method | orientation未確定をDAGに偽装しない。別途識別証明がない限り実行不可。別証明・Graph refixの採否はD06で決定 | REQUIRES_REVIEW／自動不実行 |
| fixed DAG / その他準実験 | DiD/ITS/RDD/SC/SDID等 | Phase3固有 | backdoor/IV matrixの単純拡張ではない。Design/estimandとMethod独立契約をSR04/SR09で検討 | D04では推定許可を確定しない |

**識別されたことと仮定が現実に正しいことは異なる。** 特にInstrumentのexclusion、independence、monotonicityは一般に観測データのみから保証できない。assumption_declared/evidence/checkedを分け、宣言欠落・矛盾があれば新Methodへ進めない。仮定を確認できないことと統計的に棄却されたことも分ける。

### 3.3. 推奨state machine（新E11に限定）

1. versionが認識されない・型が不正 → CONFIG/CONTRACT_ERROR。科学的非識別と区別する。
2. Question/Design/Graph/Dataのidentityとsha256、upstream result_id/hash、method_id、必要列・Data role・処置比較を照合。不一致はCONTRACT_ERRORで実行拒否。
3. IdentificationResultがIDENTIFIEDでも**対象estimand_definition・strategy・仮定がMethodへ一致するか**再判定。candidate_method_familiesは候補に過ぎず、許可リストではない。
4. NOT_IDENTIFIED、REQUIRES_REVIEW、PARTIALLY_IDENTIFIED（境界のみ） → **新E11点推定へ自動接続しない**。D06で認める別の識別根拠または研究者のGraph改訂が成立すれば**新しい識別結果**を発行する。既存validation_overrideは科学的な識別成立の代用にしない。
5. EligibilityがFAIL/不明な必須条件 → 実行拒否または意味を持つ科学的NOT_APPLICABLE。WARNはMethod別に緩和可能な警告と非緩和の前提欠落を区別し、明示的・根拠付きwarning overrideだけを審査可能にする。
6. Methodの実行不能（optional依存の欠落、version非対応、API失敗）はBACKEND_UNAVAILABLE／TECHNICAL_FAILURE等と区別。科学的な非識別に改称しない。
7. 点推定の成立と推論可用性を独立に保持：point_status、uncertainty_status、scientific_status、reason_codesを別軸とする。CIが未取得ならnull＋理由。科学的Benchmark PASSはさらに別の独立受入結果であり、実行成功では自動認定しない。

状態enum、warning-override権限、CLI exit codeの正式採否はArchitecture Reviewで確定。現行v2 ProductがREQUIRES_REVIEW＋overrideを許容する契約はD04だけを理由に遡及変更せず、旧読取・Product回帰を別検証する。

## 4. D04-3：Manifest／旧Result／lineageの後方互換

**推奨（V2と一体）:** v2 input/manifestは既存形式のまま読み続ける。新たな版のmanifestは互いに参照可能なidentification_result_ref、estimator_spec_id、question_hash、design_hash、graph_hash、dataset_hash、config_hash、upstream_manifest_sha256、effective backend/package versions、random_seed、split indicesまたはhash、artifact checksum、status/limitationを持つ。Product DBのIDを必須としない。

- v2→新Methodの自動upgradeは**禁止**。旧Manifestで必須科学証拠が欠ける場合、再識別・再生成か明示migration＋科学レビューを要する。
- v2→v2の正常なNative ATE/ATT CLIおよびProduct経路は現状維持。新CLIの互換dispatchを入れてもv2の旧Readerや旧Result payloadを破壊しない。
- upstreamのdataset/graph実バイトhashを下流入力と照合。Question hashだけでなくDesign hash、estimand definitionとcontrast、graph identityも照合。旧resultに無いフィールドを勝手に埋めて「確認済」と記録しない。
- manifestはreferenceの実ファイルhashを保持し、オブジェクトのVersion、schema、canonicalization規則（JSONキー順序、float、timezone、欠損、UTF-8等）を固定する。固定方法の最終採用はSR-10／Architecture Review。
- 既存ResultType/ScientificStatusの意味変更は避け、必要な新enumは版付き新Envelopeで定義。v2への片方向・損失ありマッピングを黙って行わない。
- optional backendに依存するオブジェクト・pickleをcross-stage canonical artifactへ持ち込まない。partial write/atomic replacement、relative path、privacyはSR-10へ引渡す。

## 5. D04-4：D03 G2信頼集合の新EffectResultへの接続

**採用済みの意味:** B0/B1のAR反転は弱IV頑健な信頼集合を返し得る。単一区間、非有界区間、非連結な複数成分、全実数を損失なく表す。汎用schemaがEMPTYを表現できても、初期just-identified B0/B1の正常なAVAILABLE/EMPTYは**不許可**。G2の正式型・enumは未採用。

**型付き候補（正式JSON schemaではない）:** confidence_setはstatus、method、level、集合のordered interval componentsを持つ。各成分はlower/upperの有限値またはnull、lower_unbounded/upper_unboundedの真偽、端点の開閉を持つ。端点がnullで無界flagがfalse等の矛盾をvalidatorで拒否する。全実数は両側無界の単一成分で表せ、非連結は2成分以上で表せる。数値JSONにInfinity/NaNを格納しない。可用性なしはconfidence_set=null＋unavailability reasonとする。Methodごとに集合の正規化・非重複・端点順・EMPTY禁止を検証する。

**意図的に未決:** confidence_set/1等のversion、ステータスenum、境界の開閉の規約、AR統計量、数値反転法、被覆率・許容誤差はD04後のArchitecture Review／SR-04／Gate07で決める。通常Wald CIをAR weak-IV robustとして保存しない。

## 6. D04で準備する正例・負例（SR-04/Gate07候補。未実行）

| ID | 入力と着目点 | 期待する科学・契約上の挙動 |
|---|---|---|
| D04-T01 | v2 Native Randomized/Backdoor→ATE/ATT、旧CLIとProduct | 旧Reader/Manifest/Resultで現行動作を回帰保護。v3へ無言で変換しない |
| D04-T02 | fixed DAG、DoWhy Backdoor、指定adjustmentを一致させたATE | 正規化したIDENTIFIED Result、Method別eligibility、正しいlineageで初めてEstimatorへ通す |
| D04-T03 | Frontdoor（Mあり）/M欠落、識別成功・数値モデル不適合 | 適格構成のみMethod候補。識別成功≠推定科学PASS。M欠落を拒否 |
| D04-T04 | binary Z/AのB0＋B1、Cの位置変更、IV heterogeneous effect | Method別Estimandを分離し、B1やDRIVを一般ATE/LATEに自動写像しない |
| D04-T05 | PAG/CPDAG、IDENTIFICATION=REQUIRES_REVIEW、旧overrideを添付 | 新E11数値Methodは自動不実行。Graphの黙示DAG化禁止。既存v2経路の意味は別検証 |
| D04-T06 | Graph/Dataset/Question/Design/contrast/上流artifact hashのいずれか不一致 | 下流実行をCONTRACT_ERRORで拒否し、科学的NOT_IDENTIFIEDへ偽装しない |
| D04-T07 | Eligibility WARN（緩和可能/不能）、未記録assumption、unsupported T/Z型 | Method別reason付きで阻止。単なるvalidation_overrideでは硬い識別前提を解除しない |
| D04-T08 | EconML point成功・CI未利用／optional package欠落／backend API失敗 | point_statusとuncertainty_statusを分離。後者2つは科学的非識別と区別 |
| D04-T09 | AR単一/非有界/非連結/ALL_REAL、B0/B1でEMPTY発生 | G2集合のlossless round-trip。正常B0/B1でEMPTYを拒否し原因を診断 |
| D04-T10 | 古いv2 manifestを新Methodへ流用、schema版誤認、unknown field | 自動昇格せず明示移行または再識別を要求。旧v2は読取可能 |
| D04-T11 | DoWhyの内部ラベルがnonparametric ATE、実際の狙いはbinary LATE/IV heterogeneous effect | 明示的Method-specific targetが無ければ新ラベルでの推定禁止 |
| D04-T12 | 科学的にIDENTIFIEDだがexclusion/independence等の宣言・根拠が欠落 | 機械的識別結果と実世界の仮定妥当性を分離し、必要なreview状態を返す |

これらは**試験設計候補**であり実測成功・科学Benchmark PASSではない。既知真値fixture、coverage、数値閾値、seed/replicateはSR-04/Gate 07の独立審査で固定する。

## 7. Human ownerへ提示するD04判断票

| 判断ID | 推奨候補 | 採用時に固定する方針 | 別審査へ残す事項 |
|---|---|---|---|
| D04-1 | **V2** | v2のProduct/CLI/Resultを保護し、新E11は版付きlocal input/result/manifestの並行経路 | 新版番号・schema fieldの正式定義とMigration実装 |
| D04-2 | **E2** | Ariadne normalized IdentificationResult＋Method別EstimatorSpecでfail-closedし、DoWhy内部オブジェクトやIDENTIFIED単独では実行許可しない | Method固有の条件・識別式と数値Science Bench |
| D04-3 | **M2** | 明示version dispatch、旧v2のread-back保証、新Methodへ旧manifestを自動昇格させず、上流のQuestion/Design/Graph/Dataset hash一致を必須化 | canonicalization、path/privacy、実装migrationの範囲 |
| D04-4 | **G2-Bridge** | 採用済みG2の型付き信頼集合を新EffectResultの独立uncertainty軸として保持。B0/B1正常ARのEMPTYは禁止 | 正式schema enum、AR数値反転・coverage |
| D04-5 | **R2** | 既存Product/v2のREQUIRES_REVIEW＋override契約と新E11の自動実行禁止を区別し、旧経路回帰を必須にする | Product契約自体を変更すべきかの別判断、D06のowner refix/partial ID |

**現時点の判断:** 上記はすべて**技術推奨のみ**。Human ownerの採否は未取得。D04のオーナー判断を02へ書き込まず、03/04/05・ADR・Gate 06/07の正式承認状態も変更しない。

## 8. 依拠資料と次工程

- [SR-03横断契約](20261101_sr03_identification_estimand_estimator_contract_review.md)
- [D01独立IV familyの個別判断](20261101_sr03_iv_heterogeneous_estimand_decision.md)
- [D03-1〜4の科学判断](20261101_sr03_d03_remaining_2sls_weak_iv_review.md)
- [02構想承認記録（全体PENDING）](../00_enhance_background/02_enhancement_concept_approval_record.md)
- [03要件案](../00_enhance_background/03_requirements_revision.md)、[04設計案](../00_enhance_background/04_design_revision.md)、[05整合性レビュー](../00_enhance_background/05_requirements_design_consistency_and_traceability_review.md)
- [DoWhy公式API](https://www.pywhy.org/dowhy/main/dowhy.html)：identify_effectは複数の識別経路を探索し、target estimandは別途解釈が必要。
- [EconML公式IV methods](https://www.pywhy.org/EconML/spec/estimation_iv.html)：IV系異質効果はMethod/仮定ごとに解釈する。

**次の順番:** （1）Human ownerにD04-1〜5を個別提示 →（2）採用された判断のみ02とSR-03総合メモへ反映 →（3）D05のCATE/DRIV CI推論審議 →（4）D06のGraph不確定性 →（5）SR-01〜12の是正・00_04再審査／承認。Architecture Review、正本Snapshot、Gate freezeが終わるまでCoding許可を出さない。
