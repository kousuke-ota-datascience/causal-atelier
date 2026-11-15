# ENH-E11 — SR03-D05：CATE／DRIV推論・区間推定Capability契約（B案5件採用）

**文書区分:** `working_notes`／独立した技術比較・科学的制約・個別オーナー採用記録。正式なFR/NFR/AR、Architecture Review、Gate06/07、Coding許可ではない。  
**判断日:** 2026-11-15（JST）  
**判断状態:** `SR03-D05_BBBBB_OWNER_ACCEPTED / SCIENCE_NOT_RUN / FORMAL_SCHEMA_PENDING / GATE_NOT_FROZEN / FULL_CONCEPT_PENDING`  
**基準:** `prototype/ariadne_mvp`、審議着手時のHEAD `1e8acfc5524bb67c3c8d50b36a8ba4744c3dd511`（科学受入用固定SHAではない）  
**関連Scope:** 00_04 P2-01〜P2-17、とくにP2-02〜09、P2-10〜16；E11-REQ-P2／E11-REQ-SR03；Issue #18／#22／#24；SR-03、SR-04／SR-07。

## 0. 目的・文書の責務

Phase2に維持する**非IV CATEの7手法**（LinearDML、CausalForestDML、DRLearner、ForestDRLearner、S-Learner、T-Learner、X-Learner）と、**IV異質効果**のDRIVについて、(1)対象の区別、(2)CIが必須となる利用場面、(3)推論法の選択、(4)点推定・推論・科学受入の状態、(5)受入証拠を定める。

本書はD05固有の**比較・非採用理由・科学的限界・候補fixture**の管理先とする。オーナー採用事実と全体承認の区別は[02承認記録](../00_enhance_background/02_enhancement_concept_approval_record.md)に置く。総合進捗は[SR-03総合メモ](20261101_sr03_identification_estimand_estimator_contract_review.md)へ、要件差分は03、設計責務は04、Gate候補traceabilityは05へ記載する。

**重要な既決境界:** SR03-D01でIV_HETEROGENEOUS_EFFECTを独立Estimand familyとした。SR03-D04で旧Product/v2の互換と新CLIのversioned/typed/strict実行ゲートを採用。DRIVはPhase2候補であって、SR03-D03-4で初期非採用とした条件付きcomplier LATE向け推定器Cと同一ではない。新機能はScientific Core／ローカルCLI／永続ローカル成果物に限り、Web/UI/API/Worker/DB統合を追加しない。

## 1. 現時点の検証結果と根拠の射程（事実）

| 方法 | 2026-11-01のEconML 0.17.0直接probe | 有限CIのAPI取得条件（観測） | 未立証 |
|---|---|---|---|
| LinearDML | fit/effect成功 | 初回構成で取得 | 真値誤差、pointwise coverage、適格なnuisance／variance |
| CausalForestDML | fit/effect成功 | 初回構成で取得 | forest固有推論の適用仮定・coverage |
| DRLearner | fit/effect成功 | forest final model＋autoでは不可。BootstrapInference 12反復明示で取得 | 別構成での適切なCI方式・coverage |
| ForestDRLearner | fit/effect成功 | 初回構成で取得 | forest固有推論の適用仮定・coverage |
| SLearner | fit/effect成功 | inference=Noneの初回は不可。BootstrapInference 12反復で取得 | nuisance/モデル不確実性を考慮したcoverage |
| TLearner | fit/effect成功 | 同上 | armごとのsupportとcoverage |
| XLearner | fit/effect成功 | 同上 | pseudo-outcomeとarm imbalance下のcoverage |
| DRIV | 連続Treatment／Instrument構成でfit/effect成功 | 初回構成で取得 | method固有IV moment/estimandの妥当性、weak-IV下のcoverage、complier LATEへの対応 |

**一次証拠:** [SR-02実行結果](20261101_sr02_backend_runtime_probe_results.md)と[GitHub Actions #41270427977](https://github.com/kousuke-ota-datascience/causal-atelier/actions/runs/41270427977)、[2026-11-01区間推論原因調査](20261101_sr03_late_estimator_options_econml_inference_review.md)、[Bootstrap追加probe #41272111463](https://github.com/kousuke-ota-datascience/causal-atelier/actions/runs/41272111463)。これらはAriadneの新CATE adapterではなく**EconML直接呼出し**であり、新Adapterの機能・品質・統計的被覆を立証しない。

**方法／実装の直接資料:** [EconML公式Inference](https://www.pywhy.org/EconML/spec/inference.html)、[EconML 0.17.0 MetaLearner source](https://github.com/py-why/EconML/blob/v0.17.0/econml/metalearners/_metalearners.py)、[EconML 0.17.0 DRLearner source](https://github.com/py-why/EconML/blob/v0.17.0/econml/dr/_drlearner.py)、[EconML公式IV推定説明](https://www.pywhy.org/EconML/spec/estimation_iv.html)。公式web資料の対象版と実測した0.17.0の差異は、Version-lockとBackend adapterテストで再照合する。

**反証の要点:** 12反復bootstrapで有限の`effect_interval`が得られたことはAPI可用性しか示さない。標本分布の近似、cross-fitting、選択後推論、overlap、IV弱識別、forest推論の適用範囲は別の論点であり、CI出力成功を科学的PASSに変換しない。

## 2. D05-1：推定対象の契約分離 — B案採用

| 案 | 内容 | 利点／欠点 | 判定 |
|---|---|---|---|
| A | 非IV CATEとDRIVを一つのEstimand／Result意味契約へ統合 | 表面上単純だが識別条件・対象集団・Treatment contrastの誤同定を誘発 | 非採用 |
| **B** | 非IV CATE 7手法とDRIVのIV異質効果を**別EstimatorSpec・Estimand contract**で管理。Result envelopeの汎用フィールドのみ共通化 | 対象の意味を保護しつつ再利用可能 | **採用** |

- 非IVの二値Treatment例：`CATE(x) = E[Y(1)-Y(0) | X=x]`。対象母集団、T0/T1、X(effect modifier)とW(confounder)を区別する。単なる予測モデルの`f_1(x)-f_0(x)`は識別仮定なしに因果効果とはならない。
- DRIV：`IV_HETEROGENEOUS_EFFECT`というfamilyのみでは十分ではない。`theta_IV(x)`を、選択したmethodにおける条件付きモーメント・処置コントラスト・Instrument/Outcome/Treatmentの定義・対象集団と識別仮定によって具体化してから受け入れる。連続T/Zでのprobeを二値Z/Aのcomplier LATEやCLATEと黙って同一視しない。
- Methodの提供可否はD04の`IdentificationResult → EstimatorSpec`適格性ゲートで検査。独立familyを維持するD01採用の再確認であり、DRIVの具体的推定対象やMethodとしての科学受入まで確定したわけではない。

## 3. D05-2：CI必須範囲 — B案採用

| 案 | 定義 | 主な影響 | 判定 |
|---|---|---|---|
| A | あらゆる実行と出力に科学的に検証済みCIを必須化 | 不適格構成でも点推定を探索で扱えない／全Methodが実装不可能になる恐れ | 非採用 |
| **B** | **Exploratoryは点推定のみ許容。Confirmatoryは事前指定された目的に適合する区間推論等の妥当な推論証拠が必須** | point可用性を保ちつつ、過大な推論主張を防止 | **採用** |
| C | 全MethodでCIを常時任意として用途を問わず区別しない | 推論を欠いたConfirmatoryを肯定する危険 | 非採用 |

**採用する不変条件:**
1. `EXPLORATORY`: 事前に固定したEstimand/Design/Methodの科学的適格性、モデル検証とsupportを満たす場合、`point_status=AVAILABLE`、`uncertainty_status=UNAVAILABLE`でも結果保存を許可する。ただし推定値は探索的で、CI無しの推論的主張・確定的な意思決定証拠には用いない。
2. `CONFIRMATORY`: 主張・検証対象・推論法・対象水準を**解析前に固定**し、そのMethod/構成で妥当性が検証されたCI等の推論証拠を必須とする。点推定のみ、未検証のfinite CI、推論不能なら**Confirmatory science acceptanceは不成立**。これは「全ての有効な因果推論に一律CIだけが必要」という主張ではなく、E11初期提供の検証可能な運用基準である。
3. どちらのモードでもD04の識別・Method Eligibilityゲート、Outcome/Treatment型、support不足の拒否は緩めない。CI有無で識別仮定の正しさを証明しない。
4. CI非利用はMethodを8つから削減する根拠ではない。`P2-02〜09`の列挙対象を維持し、推論対応度はBackend/Method/構成別capabilityとして管理する。

**追加留保:** Confirmatoryの受入ではpointwise intervalと集団のaverage effect CI、同時信頼帯（simultaneous confidence band）を区別。**初期採用方針は固定したx／contrastでのpointwise推論**。未検証の同時信頼帯・全xでの家族内誤差保証・無制限な事後選択は契約外として別審査する。pointwise「95%」の集合を並べても関数全体の95%同時被覆にはならない。

## 4. D05-3：推論アルゴリズム — B案採用

| 案 | 定義 | 科学上の評価 | 判定 |
|---|---|---|---|
| A | 全8推定器を同一Bootstrap方式へ固定 | 簡単に見えるがMethod固有の分散構造・推論理論・crossfit・forest/IV妥当性を無視し得る | 非採用 |
| **B** | **Method・最終モデル・対象estimand・backend version別に推論方式を選択し検証** | 真の仕様差を保存できる。科学Benchmark/環境lockの負担は必要 | **採用** |
| C | Native/既定inference以外を禁止 | S/T/X等で使える推論経路を根拠なく封じることがある | 非採用 |

**方式候補（採用した実装アルゴリズムではない）:**
| Estimator | 比較すべき候補 | 主要検証ポイント |
|---|---|---|
| LinearDML | 線形final-stageに整合するnative/asymptotic推論 | nuisance/cross-fitting、robust variance、対象contrast |
| CausalForestDML | Forest固有の利用可能な推論（例：内部BLB系） | honest splitting等の実際の構成、対象点/支持域、近似被覆 |
| DRLearner | 推論互換final model、またはBootstrap | final modelの`prediction_stderr`有無と再推定方式、被覆 |
| ForestDRLearner | Forest固有推論 | arm support、forest/nuisance条件、被覆 |
| S/T/X-Learner | Method固有のBootstrap等 | base learner／擬似アウトカム／nuisance再推定の範囲、有限標本被覆 |
| DRIV | IVモーメント/構造モデルに整合する推論 | Instrument relevance、IV-validity仮定、weak IV/conditioning、CATE/LATEラベルへの誤変換禁止 |

**科学上の禁止事項:** 未検証の汎用Bootstrapをあたかも一様にvalidなCIと記載しない。Bootstrap resampling単位（独立観測／クラスタ・時系列等）、fold/nuisanceの再学習有無、random_seed/反復、モデル選択の方法と推論条件をMethod別に記録する。D03のB0/B1 AR反転契約はこのD05で置換しない。

## 5. D05-4：推論不能時のResult — B案採用

| 案 | 内容 | 判定 |
|---|---|---|
| A | 一つのSUCCESS/FAILUREに点推定・CI・科学受入を混載 | 非採用 |
| **B** | **identification、point estimate、uncertainty inference、science acceptanceを区別して保存** | **採用** |

D04の`EffectResult` envelope内で以下の意味軸を持つ（**名前／enumは未承認**）。

- 識別状態：指定Estimandに関する上流`IdentificationResult`が根拠とともに承認可能か（D04でfail-closed）。
- `point_status`: AVAILABLE / UNAVAILABLE / FAILED等の候補。有限点推定値があってもsupport不足・推定対象不一致を科学的成功とは扱わない。
- `uncertainty_status`: AVAILABLE / NOT_REQUESTED / UNAVAILABLE / FAILED等の候補。計算依頼なし、API非対応、計算失敗、非有限値、科学的な適格性不足を理由codeで分離する。実施していない区間を0幅・偽SEで埋めず、区間値はnull。
- 科学的受入状態：Method固有の受入基準と独立科学Benchmarkによって判定する。API成功／finite intervalと独立。
- ResultへEstimand family／definition、population/contrast、CI level/method、pointwiseかsimultaneousか、backend/effective version、nuisance/folds/seed、supportと欠落理由、artifact ref/hashを保持。個票CATE出力はprivacy審査と別。

**具体例:** `fit/effect`成功、`effect_interval`非対応なら点推定を残して`confidence_interval=null`＋`uncertainty_status=UNAVAILABLE`＋理由。Confirmatoryでは受入保留／不成立。探索では用途条件下で閲覧可。依存ライブラリ欠落・version違いはTechnical/Dependency issueであり科学的`NOT_IDENTIFIED`と混同しない。

**衝突回避:** D03 G2のconfidence_setは通常の単一区間と異なり非有界・非連結等を保持する。D05のpointwise CI取得方法を導入してもG2の型付き集合を単一`[lower,upper]`に潰さない。

## 6. D05-5：科学的受入 — B案採用

| 案 | 内容 | 判定 |
|---|---|---|
| A | finite intervalをAPIで取得できればMethodを科学的に受入 | 非採用 |
| **B** | **Estimandの整合・Known-truth・pointwise coverage・Method別の負例と前提条件を独立検証**してから科学受入 | **採用** |

**Method別の検証設計条件:**
1. Known-truth DGPを定義し、`tau(x)`や`theta_IV(x)`を対象と一致させる。定数/線形/非線形異質効果と合意したsupport上のxを区別。
2. 異なる`n`、処置arm数、不均衡、overlap、nuisance mis-specification、fold/seed、final model構成でbias/RMSEと推論失敗を測定。
3. **名目信頼水準に対する経験的pointwise coverage**を独立simulationで評価し、Monte Carlo測定誤差・replicate数・数値許容値を受入前に固定。区間幅・非有限率・欠測/非適用率も報告する。
4. Randomized/Backdoorの交絡・positivityと、IVのrelevance/exclusion/independence等の**識別仮定違反**を区別。DRIVでは弱IV条件と型・momentの不適格が本質的な負例。
5. Pointwise CI、average-effect CI、simultaneous bandの対象差をテストで保証する。特定のxの区間を全xで同時保証と報告しない。事後的なx選択／探索後Confirmatoryは別の多重比較・選択後推論を要し得る。
6. CIが未対応の構成はnull＋理由とし、支持域外のCATEを有効と宣言しない。Science PASSは**独立Gate 07の事前登録基準**とcandidate SHAで判定し、GitHub ActionsのAPI smoke成功を流用しない。

**未決の定量項目:** confidence level（例：95%を採用するか）、Monte Carlo反復数・seed群、被覆許容帯、bias/RMSE閾値、bootstrap samples、時間・CPU・OS・backend version、x grid／support、例外・失敗率の上限。**数値を根拠なしに補完せず、SR-04/Gate 07で固定する。**

## 7. 選択肢・オーナー決定の一覧

| 判断 | 比較した選択肢 | オーナー採用（2026-11-15 JST） | 採用の限界 |
|---|---|---|---|
| **D05-1** | A：同一契約／B：非IV CATEとDRIV分離 | **B** | Method固有の`theta_IV(x)`・DRIV科学妥当性は未実証 |
| **D05-2** | A：全Methodの全実行でCI必須／B：用途別／C：全Method任意 | **B** | Confirmatoryの推論妥当性審査、具体的Acceptance未固定 |
| **D05-3** | A：Bootstrap統一／B：Method別／C：Nativeのみ | **B** | 個別推論アルゴリズム採用・版・パラメータ未固定 |
| **D05-4** | A：成功失敗に統合／B：点・推論・科学受入分離 | **B** | 正式schema/enum/CLI exit code未承認 |
| **D05-5** | A：finite CIでPASS／B：対象・被覆・負例の独立試験 | **B** | 定量閾値・科学Gateは未承認、未実施 |

**人間の明示指示:** 「SR03-D05について、D05-1〜D05-5の5項目すべてB案を採用する。GitHubの独立技術記録に比較・科学的制約を記載し、02承認記録と03/04/05に採用内容を反映せよ。正式schema、数値Benchmark、Gateと全体構想の承認状態は区別すること。」

本判断は**5つの方針について個別採用**であり、8 Methodの正式受入、Ariadne adapterの実装完了、全体スコープ・FR/NFR/AR承認、確定schema・定量Benchmark/Gate 06/07 freeze、canonical 999 PASSではない。

## 8. SR-04／Gate07へ引き渡す候補Fixture（未実行）

| ID | 入力・反証条件 | 期待される契約・科学的挙動 |
|---|---|---|
| D05-T01 | 無交絡CATE既知真値・強いoverlap、非IV7 Method | effect-modifier x別真値と点推定の誤差、正しいlabel |
| D05-T02 | 連続Treatment/IVのDRIV、通常CATE・LATEと対象が違うDGP | `IV_HETEROGENEOUS_EFFECT`の固有momentが無ければ未許可。LATE/CATEへ誤変換禁止 |
| D05-T03 | Exploratoryで点推定成功、CI unavailable | point保存可・CI=null＋reason、Confirmatory成立と表示しない |
| D05-T04 | ConfirmatoryでCI未取得またはAPI finiteでもcoverage未承認 | Confirmatory科学受入は未成立。探索の結果と区別 |
| D05-T05 | DRLearner forest-final推論不可／bootstrap指定可 | 不可理由の正しい区分。API成功と統計的validityを分離 |
| D05-T06 | S/T/Xのinference=None／Bootstrap指定 | NOT_REQUESTED/UNAVAILABLE/AVAILABLEを実装状態と区別。CI availabilityの再現 |
| D05-T07 | CausalForestDML/ForestDRLearner/LinearDMLのMethod別推論 | 学習構成・Methodに応じた可否とcoverage、単なるgeneric Bootstrapへの固定禁止 |
| D05-T08 | n/overlap/arm imbalance/未調整交絡を変更 | bias・RMSE・coverage・無効領域の差、科学的負結果 |
| D05-T09 | DRIVの弱Instrument、無効IV | 効果対象・識別仮定・weak-IV推論制約を分離。有限CIでvalidと認定しない |
| D05-T10 | pointwise 95%区間を複数xへ出力 | simultaneous band／家族内保証と混同しない |
| D05-T11 | 再実行時にseed/fold/bootstrap設定・backend版本を変更 | Manifestに実効設定・versionを保存し、coverage比較が追跡可能 |
| D05-T12 | optional EconML欠落、CI計算例外、対象外処置型 | Dependency/Technical/Scientific eligibilityを別reasonにし、架空CI出力禁止 |
| D05-T13 | 旧v2 Native ATE/ATT推定経路 | D04のread-back回帰・既存Result契約を維持 |

## 9. 残余・次の工程

- **D05個別方針判断完了:** B/B/B/B/B採用（2026-11-15）。
- **未承認／未実施:** 各Methodの推論アルゴリズム／具体InferenceConfig採用、DRIVの正確な識別モーメント・対象集団、確定CI waterline・数値閾値、正式Result/EstimatorSpec schemaとCLI status、独立Known-truth/coverage、Backend version lock、個票CATE privacy、全体Scope、Architecture Review、Gate freeze、Coding。
- **次:** SR03-D06（CPDAG/PAG・部分識別・別識別証明・Graph refixとoverrideの扱い）→SR-03横断の未解決整理→SR-04 Science Acceptance具体化／SR-01〜12の是正・Scope再審査。

**既存文書との責務分離:** D01のestimand family比較は[ファイルD01](20261101_sr03_iv_heterogeneous_estimand_decision.md)、D03の弱IV/AR信頼集合とC後続管理は[残余D03](20261101_sr03_d03_remaining_2sls_weak_iv_review.md)、D04の新旧契約・fail-closed識別ゲートは[独立D04](20261115_sr03_d04_identification_estimator_contract_options.md)が正とする。本書は**D05固有**の比較・科学的制約のみを追加する。
