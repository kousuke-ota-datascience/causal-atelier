# ENH-E11 — SR03-D03残余論点：2SLS対象・弱IV推論・Confidence Set・C案の技術審議

**文書区分:** `working_notes`／SR03-D03-1〜D03-4の**技術審査・推奨案（オーナー採否待ち）**。正式要件／設計／科学Gate／実装許可ではない。  
**審議日:** 2026-11-01（JST）  
**状態:** `D03_A_PLUS_B_PREVIOUSLY_OWNER_ACCEPTED / D03_REMAINING_TECH_REVIEW_PREPARED / OWNER_DECISIONS_PENDING / SCIENCE_NOT_RUN`  
**確認Baseline:** `prototype/ariadne_mvp`、本レビュー着手時HEAD `a18af8c7916a4919fdd27bf2ff54b2cc4d780300`。検討は現行コード・既存SR-02 API smokeの記録と外部一次根拠に基づく。新たなIV実装、numerical parity、弱IV coverageの実測は実施していない。  
**関連:** 00_04 P3-12／P3-16、UC-08、Issue #22（Phase3 IV/LATE）、SR-03／SR-04、Gate 07候補。

## 0. 責務の境界・従前決定

**変更しない既決事項:** Phase3の初期EstimatorはA＝二値Z/AのWald比（complier LATE Reference）＋B＝2SLS、C＝条件付きIVのDR／効率的LATEは**追加審議**とする（オーナー採用2026-11-01）。D01の独立 `IV_HETEROGENEOUS_EFFECT` family採用を維持し、DRIVを自動的にcomplier LATEへ置換しない。

**判断の管理:** [02承認記録](../00_enhance_background/02_enhancement_concept_approval_record.md)がオーナーによる個別決定を保持。[D03初期比較・EconML probeメモ](20261101_sr03_late_estimator_options_econml_inference_review.md)はA/B/Cの当初比較・採用事実・EconML区間推論根拠を保持。**本ファイルがD03-1〜D03-4の新たな選択肢比較・推奨、Estimator/Inference/Confidence Setの詳細条件、未決・検証引渡しの唯一の詳細技術記録となる。** [SR-03総合メモ](20261101_sr03_identification_estimand_estimator_contract_review.md)は全Methodの横断契約・Fixture一覧を管理し、D03残余の詳細を重複管理しない。00_04／03／04は正式採用前の本提案を決定済みの要件・設計に格上げしない。

## 1. 一次根拠と判断のための事実

1. Imbens & Angrist (1994), [*Identification and Estimation of Local Average Treatment Effects*](https://www.gsb.stanford.edu/faculty-research/publications/identification-estimation-local-average-treatment-effects)：IVが有効というだけでは一般ATEは得られず、単調性等の条件下でcomplierに対するLATEを対象とする。一般のIV係数とLATEの対応はDesign依存。
2. Abadie (2000), [*Semiparametric Estimation of Instrumental Variable Models for Causal Effects*](https://www.nber.org/papers/t0260)：共変量・異質性下の2SLS係数を常に単一のcomplier平均効果と呼べない。追加の対象・モデル仮定が必要。
3. Staiger & Stock (1997), [*Instrumental Variables Regression with Weak Instruments*](https://www.nber.org/papers/t0151)：弱いFirst Stageでは通常の2SLS統計的近似が不安定であり、通常Wald型CIの妥当性は保証されない。
4. Lee & Porter (2026), [*Correct (and Incorrect) Inference with a Single Instrumental Variable*](https://www.aeaweb.org/articles?id=10.1257/jep.20251464)：just-identified 1 endogenous/1 instrumentでの通常CIとAR等の弱IV頑健な推論の違い、および画一的なF>10規則の限界。
5. Mikusheva (2010), [*Robust confidence sets in the presence of weak instruments*](https://dspace.mit.edu/entities/publication/702ee950-3381-435d-8a9e-b2f7d9eb7fed)：AR・CLR等の反転信頼集合はbounded単一区間に限定できない。
6. [linearmodels公式 IV導入・推論API](https://bashtage.github.io/linearmodels/iv/introduction.html)：IV2SLS、heteroskedastic/cluster/HAC covariance、First Stage診断を区別し、識別検定の有意性やF統計量だけを強IV保証と解釈しない。**ソフトウェア候補資料であり、Ariadne/Python3.12/pandas3とのinstall・parity・license・採用版の検証は未実施**。

**特に区別:** `first_stage_F` が大きいこととexclusion/independence/monotonicityが成立することは別。ARは弱識別に対する推論法であって無効なInstrumentを修復するものではない。計算可能性≠識別妥当性≠区間被覆率。

## 2. D03-1：2SLS初期保証範囲と推定対象

| 案 | 初期保証範囲 | 利点 | 費用・危険 | 技術判断 |
|---|---|---|---|---|
| **S1（最小）** | B0＝二値Z・二値A／単一excluded IV／共変量なし／切片あり／just-identified | Waldとの厳密な点推定パリティが可能。モデル・推論が明確 | BがAと数値的に同じとなり追加2SLS能力が限定される | 採用可能だが初期Bとして狭い |
| **S2（段階拡張）** | **B0＋B1**：B1＝二値Z・二値A・1内生処置・1 excluded IV・事前指定のpre-treatment共変量C・切片・additive linear structural model | 初期の2SLSとして調整共変量を扱える。数値パリティとモデル依存拡張を区別できる | Cの正しい指定と構造効果の不変性を仮定しなければ因果的解釈が崩れる | **推奨（未承認）** |
| **S3（一般化）** | 複数IV・複数内生変数・連続処置・相互作用・異質効果・非線形設計を初期から保証 | 広い用途 | Momentのランク、対象、弱IVの多変量推論・CI topologyが拡大。科学受入の未確定が多い | 初期には非推奨 |

**S2のB0:** 切片付き just-identified `Z∈{0,1}, A∈{0,1}`、共変量なし。`Δ_Z E[Y]/Δ_Z E[A]` と2SLS点推定は同じ標本・定義のもとで代数的に一致する。有効なIV仮定、nonzero first stage、monotonicity等を前提としてcomplier LATEを対象とする。標本の割当群がない場合やFirst Stageがゼロなら比は定義できない。

**S2のB1:** 一つの内生処置A、一つのexcluded Instrument Z、事前定義されたpre-treatment C、線形構造式
`Y = alpha + beta*A + gamma^T*C + epsilon`、`E[epsilon|Z,C]=0` を**追加の科学仮定**として宣言する。正しいベースライン関数（この提案ではadditive linear）、exogeneity、rank、overlapが必要。betaはまず**条件付きモーメントに基づく線形IV構造係数**として記録し、ATE／LATE／CLATEと自動的にlabel同一視しない。潜在的に全対象でconstant additive treatment effectという強い実質仮定が成立する場合の因果効果との対応は、個別のDesign根拠を必要とする。Treatment異質性やCへの非線形依存がある場合、一般2SLS係数を平均complier LATEと表示しない。

B1では未調整Waldとの点推定一致を要求しない。**このレビューではS2を推奨するが、B1の因果的対象、Cの指定とCI可用性をオーナーが承認するまで保証しない。** 連続A・複数Z・multiple endogenous／cluster/HAC等の一般化を初期提供に含めるかは別審議。

## 3. D03-2：弱IV診断・推論方式

| 案 | 内容 | 重大な制約 | 技術判断 |
|---|---|---|---|
| **I1** | First-stage診断と通常2SLS Wald区間のみ。弱い場合はwarning | 弱識別時にnominal coverageを維持できず、区間表示が誤解を誘う | 非推奨 |
| **I2** | **B0/B1でAR（Anderson–Rubin）検定反転による信頼集合を初期の基準推論とする**。独立観測下のheteroskedasticity-robust漸近検定を候補とし、First-stage診断・正しいIV-SEを併記 | ARもInstrumentの無効性を補正しない。小標本の厳密coverageは保証されず、数値的反転の全領域確認が必要 | **推奨（未承認）** |
| **I3** | I2にCLR、LM、tF等を初期から追加 | 前提、計算、出力差分、複数Instrumentへの拡張と独立検証が増える | 初期非推奨。将来比較候補 |

**I2の科学的意味:**

- B0で `rY = mean(Y|Z=1)-mean(Y|Z=0)`、`rA = mean(A|Z=1)-mean(A|Z=0)` とおき、`H0: beta=beta0` について `rY-beta0*rA=0` を検定する。母集団のIV条件が満たされるとき、null下でのreduced-form contrastの分散を反映して反転する。
- B1では `Y-beta0*A` を事前定義した外生共変量CとInstrument Zへ回帰し、Zの係数ゼロを検定して反転する案。ただしこの解釈は正しいadditive structural model／IVの条件付き外生性に依存し、任意のconditional LATEに自動適用できない。
- 主たる初期想定は**単一excluded Z・単一endogenous A、相互に独立な観測単位、heteroskedasticityを許容する漸近推論**。Cluster依存・serial dependence・複数IV／内生変数・conditional LATE一般形はこの特定のAR受入から除外する案。推論方式を失敗・非適用として表し、誤って独立観測用CIを返さない。
- `first_stage_effect`, SE, instrument/treatmentの群別support、partial first-stage情報、検定の定義・covariance・実効自由度／分布・推論可用性を記録。**単一F>10閾値による「強IV PASS」判定を禁止**する。強弱の数値基準・warningsはGateで事前固定する。
- 通常2SLSのheteroskedasticity-robust sandwich SE（第一段階推定を無視しない）を診断用に計算してよいが、対応Wald型区間を**弱IV頑健な推論と表示しない**。弱識別が疑われる場合、通常Wald CIを科学的に有効な主結果として採用しない。
- First Stageが標本上ゼロなら比の点推定はundefinedであり、AR信頼集合まで必ずundefinedとは限らない。点推定状態と信頼集合状態を分ける。
- exclusion／independence／monotonicityの根拠不足は別の`REQUIRES_REVIEW`であり、ARの有意性による代替証明はできない。

**数値実装注意:** just-identified B0のAR反転は、`rY-beta*rA`とその共分散からFieller型の二次不等式として解析可能な場合がある。B1の検定反転・heteroskedasticity-robust covarianceも`beta`依存を持つため、**有限grid探索で左右端を恣意的に切断しない**。必要なら数式による全域解または同等の厳密な形状検査を独立検証する。

## 4. D03-3：弱IV信頼集合のResult表現

**提案:** 一般の `confidence_interval = [finite_lower,finite_upper]` のみでは受入不能。IV推論の別オブジェクト `confidence_set`（名称未承認）に以下を持たせる。

| Field案 | 科学的意味・不変条件 |
|---|---|
| `method`, `confidence_level`, `test_distribution`, `covariance_type` | AR反転か等、名目水準と近似前提を明記 |
| `set_kind` | `BOUNDED_INTERVAL / UNBOUNDED_CONNECTED / DISCONNECTED / ALL_REAL / EMPTY`等。Methodに適用できない形状は安易に生成しない |
| `components[]` | 閉区間の和集合を境界順で格納。各成分はlower/upperとそれぞれの`unbounded` flagを持つ。JSONで `Infinity/-Infinity/NaN` を数値と偽装しない |
| `inference_status`, `validity_scope`, `reason_codes` | `AVAILABLE/NOT_REQUESTED/NOT_APPLICABLE/FAILED/UNAVAILABLE`候補と仮定・標本条件を分ける |
| `point_estimate`, `point_estimate_status` | 別axis。点推定が未定義でも、定義された信頼集合を保持できる |
| `diagnostics`／`backend_version`／`lineage_hash` | First-stage・AR検定構成・データ/Graph/Question/Designの再現性 |

- `EMPTY`は計算失敗ではなく、**採用した検定族のすべての候補値を棄却したという統計的結果**であり得る。失敗は別statusへ。
- `ALL_REAL`は情報が弱い等の結果として生じることがあり、効果ゼロ・無効果を意味しない。
- `DISCONNECTED`は複数成分を失わず保持し、有限区間一つへ丸めない。
- schema表現では非有界側の数値境界は`null`とunbounded flagを併記する。**CI取得不能のnullと、上端が非有界なnullを明確に区別**する。
- これは科学的なtopologyの保存契約であり、CLI JSONの正式field名・Versionや旧Resultとの共存はD04／Architecture Reviewで確定する。

## 5. D03-4：C案（条件付きIVのDR／効率的LATE）

| 案 | 内容 | 判断 |
|---|---|---|
| **C1** | **初期A+Bを維持したまま、Cを明示的な後続科学的方法審議として管理**。レビュー起動条件・責任者・成果物を固定 | **推奨（未承認）** |
| **C2** | CをPhase3初期Methodに追加 | 既決の初期A+B範囲を拡大する変更判断と、新識別／推論科学Benchが必要 | 現時点で非推奨 |
| **C3** | Cを期限・責任なしで無期限先送り | 過去の差戻し理由（暗黙のスコープ削減）を解消できない | 非推奨 |

**C1に必要な責任・Trigger案:** 初期のPhase3 P3-12スコープ確定時に、Cが初期提供から除外される理由・対応Issue・後続のScientific Methods owner（実名は未指定）・Scope承認者（Human owner）を確定する。**conditional IVのみでInstrument independenceが成立し、処置効果が異質なUC-08が初期B1の線形一定効果仮定では科学的に扱えないことが要求として明らかになった場合**、または独立したPhase3後続Enhancementの開始前に再審議する。採用する場合にはconditional LATEの識別式、Instrument assignment/propensity、complier support、nuisance models・cross-fitting、推論／coverage、弱IV問題を別の科学的Contract・Benchmarkで定義する。CはEconML DRIVと同一Methodではない。

**未決のOwnerを捏造しない:** `#22` を既存IV/LATE追跡Issueとして参照するが、C専用後続Issueの番号・担当者・具体的期限はまだ決まっていない。正式にC1を採用する際にオーナーが明示してから記録する。

## 6. 検証・SR-04/Gate 07引渡し（まだ実施しない）

| Fixture候補 | 必須の反証・期待結果 |
|---|---|
| `D03R-T01` | 二値Z/A・共変量なしのjust-identifiedでWald/2SLS点推定の標本代数的パリティ、complier LATE既知真値 |
| `D03R-T02` | B1で正しいadditive constant-effect構造と有効なconditional IVの既知真値パリティ、共変量誤指定で不当なLATE/ATEラベルを付与しない |
| `D03R-T03` | `first_stage=0`、local-to-zero、強いfirst stageを分離。点推定undefinedとAR信頼集合availableを区別 |
| `D03R-T04` | AR反転と独立reference手法の集合一致、正しい群分散・共分散、有限／非有界／非連結／全実数／空集合の構造試験 |
| `D03R-T05` | Instrument invalid（exclusion・independence・monotonicity違反）ではAR実行結果を「valid IV証明」としない |
| `D03R-T06` | cluster/time依存、複数IV、連続Treatment等を初期契約では明示非適用。無警告のrobust CI出力を禁止 |
| `D03R-T07` | 適格・不適格Design別のcoverage/type-I error・数値精度、ランダムseed・反復数、被覆誤差の不確実性を測定 |
| `D03R-T08` | optional backend導入不可・effective version差・旧Native ATE/ATTの回帰を科学的不適格と区別 |

既存`SR03-T05/T06`はSR-03横断fixtureの参照IDであり、本ファイルの`D03R-Txx`は**提案レベルのMethod別詳細**とする。最終のGate Test ID、confidence level、許容誤差、Monte Carlo回数、CPU/OS/backend supportは独立Scientific Reviewで固定し、実測してからPASS判定する。デフォルトの弱IV F閾値や任意の数値品質基準を根拠なしに採用しない。

## 7. 決定票：Human ownerに残す採否

| ID | 技術推奨（全て**未承認**） | オーナーが明示すべき事項 |
|---|---|---|
| **D03-1** | **S2**：B0 just-ID＋B1 単一Z/A・共変量Cの線形構造2SLS | B1まで初期保証するか。構造constant-effect仮定と対象label。連続A/複数Zを後続にするか |
| **D03-2** | **I2**：B0/B1にAR反転の弱IV頑健な主信頼集合（独立標本・漸近heteroskedasticity-robust） | ARを初期必須とするか。cluster/HAC等の対象外と通常CIの扱い |
| **D03-3** | **G2**：非有界・非連結・ALL_REAL・EMPTYを型付き集合として表現 | 具体schema/旧ResultのcompatibilityはD04へ委譲すること |
| **D03-4** | **C1**：Cは初期非採用を維持し、科学的使用場面に基づく後続審議trigger/責任を確定 | C専用Issue/Owner、正式な再審議契機、初期除外の承認理由 |

**今回の記録の判定:** `TECHNICAL_RECOMMENDATION_PREPARED`。オーナーのS2/I2/G2/C1採否、実装方法、正式schema、依存lock、科学Benchmark/Gate 07は**未承認・未実施**。既存の`A＋B採用／C追加審議`は変更していない。
