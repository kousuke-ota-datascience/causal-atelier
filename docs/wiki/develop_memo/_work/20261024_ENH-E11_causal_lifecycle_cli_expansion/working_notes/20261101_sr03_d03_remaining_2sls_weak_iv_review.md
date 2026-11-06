# ENH-E11 — SR03-D03残余論点：2SLS対象・弱IV推論・Confidence Set・C案の技術審議

**文書区分:** `working_notes`／SR03-D03-1〜D03-3の**個別オーナー採用に対応する技術判断記録**とD03-4の技術審査・推奨案。正式要件／設計／科学Gate／実装許可ではない。  
**審議日:** 2026-11-01（JST）  
**状態:** `D03_A_PLUS_B_PREVIOUSLY_OWNER_ACCEPTED / D03-1_S2_OWNER_ACCEPTED_2026-11-05 / D03-2_I2_OWNER_ACCEPTED_2026-11-05 / D03-3_G2_REVISED_OWNER_ACCEPTED_2026-11-06 / D03-4_C1_PENDING / SCIENCE_NOT_RUN`  
**個別採用日:** D03-1・D03-2＝2026-11-05（JST）、D03-3＝2026-11-06（JST）。2026-11-01は元の技術審議作成日である。  
**確認Baseline:** `prototype/ariadne_mvp`、本レビュー着手時HEAD `a18af8c7916a4919fdd27bf2ff54b2cc4d780300`。検討は現行コード・既存SR-02 API smokeの記録と外部一次根拠に基づく。新たなIV実装、numerical parity、弱IV coverageの実測は実施していない。  
**関連:** 00_04 P3-12／P3-16、UC-08、Issue #22（Phase3 IV/LATE）、SR-03／SR-04、Gate 07候補。

## 0. 責務の境界・従前決定

**変更しない既決事項:** Phase3の初期EstimatorはA＝二値Z/AのWald比（complier LATE Reference）＋B＝2SLS、C＝条件付きIVのDR／効率的LATEは**追加審議**とする（オーナー採用2026-11-01）。D01の独立 `IV_HETEROGENEOUS_EFFECT` family採用を維持し、DRIVを自動的にcomplier LATEへ置換しない。

**判断の管理:** [02承認記録](../00_enhance_background/02_enhancement_concept_approval_record.md)がオーナーによる個別決定を保持。[D03初期比較・EconML probeメモ](20261101_sr03_late_estimator_options_econml_inference_review.md)はA/B/Cの当初比較・採用事実・EconML区間推論根拠を保持。**本ファイルがD03-1〜D03-4の新たな選択肢比較・推奨、Estimator/Inference/Confidence Setの詳細条件、未決・検証引渡しの唯一の詳細技術記録となる。** [SR-03総合メモ](20261101_sr03_identification_estimand_estimator_contract_review.md)は全Methodの横断契約・Fixture一覧を管理し、D03残余の詳細を重複管理しない。00_04／03／04は**D03-1 S2・D03-2 I2・D03-3 G2改訂の個別採用**を候補スコープ・要件・設計差分に反映し、D03-4 C1の推奨を採用済みとして扱わない。正式なFR/NFR/AR・Gate・実装は引き続き未承認。

## 1. 一次根拠と判断のための事実

1. Imbens & Angrist (1994), [*Identification and Estimation of Local Average Treatment Effects*](https://www.gsb.stanford.edu/faculty-research/publications/identification-estimation-local-average-treatment-effects)：IVが有効というだけでは一般ATEは得られず、単調性等の条件下でcomplierに対するLATEを対象とする。一般のIV係数とLATEの対応はDesign依存。
2. Abadie (2000), [*Semiparametric Estimation of Instrumental Variable Models for Causal Effects*](https://www.nber.org/papers/t0260)：共変量・異質性下の2SLS係数を常に単一のcomplier平均効果と呼べない。追加の対象・モデル仮定が必要。
3. Staiger & Stock (1997), [*Instrumental Variables Regression with Weak Instruments*](https://www.nber.org/papers/t0151)：弱いFirst Stageでは通常の2SLS統計的近似が不安定であり、通常Wald型CIの妥当性は保証されない。
4. Lee & Porter (2026), [*Correct (and Incorrect) Inference with a Single Instrumental Variable*](https://www.aeaweb.org/articles?id=10.1257/jep.20251464)：just-identified 1 endogenous/1 instrumentでの通常CIとAR等の弱IV頑健な推論の違い、および画一的なF>10規則の限界。
5. Mikusheva (2010), [*Robust confidence sets in the presence of weak instruments*](https://dspace.mit.edu/entities/publication/702ee950-3381-435d-8a9e-b2f7d9eb7fed)：AR・CLR等の反転信頼集合はbounded単一区間に限定できない。
6. [linearmodels公式 IV導入・推論API](https://bashtage.github.io/linearmodels/iv/introduction.html)：IV2SLS、heteroskedastic/cluster/HAC covariance、First Stage診断を区別し、識別検定の有意性やF統計量だけを強IV保証と解釈しない。**ソフトウェア候補資料であり、Ariadne/Python3.12/pandas3とのinstall・parity・license・採用版の検証は未実施**。

**特に区別:** `first_stage_F` が大きいこととexclusion/independence/monotonicityが成立することは別。ARは弱識別に対する推論法であって無効なInstrumentを修復するものではない。計算可能性≠識別妥当性≠区間被覆率。

## 2. D03-1：2SLS初期保証範囲と推定対象

**オーナー採用（2026-11-05）：S2案＝B0＋B1をPhase3初期の2SLS保証対象とする。** B0は二値Z/A・切片・単一excluded IV・共変量なしのjust-identified設定で、Wald比と点推定パリティを確認する。B1は単一二値Z/A・事前に指定したpre-treatment C・切片・加法線形構造式に限定する。**B1の係数はモデル固有の線形IV構造係数として表し、complier LATE／ATE／CLATEとの同一性は追加の識別仮定なしに主張しない。** 複数IV・連続A・複数内生処置・任意の非線形／異質構造は初期保証外とする。**推論法I2は2026-11-05に採用済み。G2改訂の集合意味は2026-11-06に採用済み。C案C1は未採用。** 02は採用事実、本ファイルは詳細な科学的範囲・比較・検証条件を管理する。

| 案 | 初期保証範囲 | 利点 | 費用・危険 | 技術判断 |
|---|---|---|---|---|
| **S1（最小）** | B0＝二値Z・二値A／単一excluded IV／共変量なし／切片あり／just-identified | Waldとの厳密な点推定パリティが可能。モデル・推論が明確 | BがAと数値的に同じとなり追加2SLS能力が限定される | 採用可能だが初期Bとして狭い |
| **S2（段階拡張）** | **B0＋B1**：B1＝二値Z・二値A・1内生処置・1 excluded IV・事前指定のpre-treatment共変量C・切片・additive linear structural model | 初期の2SLSとして調整共変量を扱える。数値パリティとモデル依存拡張を区別できる | Cの正しい指定と構造効果の不変性を仮定しなければ因果的解釈が崩れる | **オーナー採用（2026-11-05）** |
| **S3（一般化）** | 複数IV・複数内生変数・連続処置・相互作用・異質効果・非線形設計を初期から保証 | 広い用途 | Momentのランク、対象、弱IVの多変量推論・CI topologyが拡大。科学受入の未確定が多い | 初期には非推奨 |

**S2のB0:** 切片付き just-identified `Z∈{0,1}, A∈{0,1}`、共変量なし。`Δ_Z E[Y]/Δ_Z E[A]` と2SLS点推定は同じ標本・定義のもとで代数的に一致する。有効なIV仮定、nonzero first stage、monotonicity等を前提としてcomplier LATEを対象とする。標本の割当群がない場合やFirst Stageがゼロなら比は定義できない。

**S2のB1:** 一つの内生処置A、一つのexcluded Instrument Z、事前定義されたpre-treatment C、線形構造式
`Y = alpha + beta*A + gamma^T*C + epsilon`、`E[epsilon|Z,C]=0` を**追加の科学仮定**として宣言する。正しいベースライン関数（この提案ではadditive linear）、exogeneity、rank、overlapが必要。betaはまず**条件付きモーメントに基づく線形IV構造係数**として記録し、ATE／LATE／CLATEと自動的にlabel同一視しない。潜在的に全対象でconstant additive treatment effectという強い実質仮定が成立する場合の因果効果との対応は、個別のDesign根拠を必要とする。Treatment異質性やCへの非線形依存がある場合、一般2SLS係数を平均complier LATEと表示しない。

B1では未調整Waldとの点推定一致を要求しない。**S2の提供対象は採用済みだが、B1の因果的解釈はモデル・識別仮定に条件付きであり、Cの適格性、first stage、CIの実現性・被覆率は未検証である。** 連続A・複数Z・multiple endogenous／cluster/HAC等の一般化は今回の初期保証に含めず、別審議とする。

## 3. D03-2：弱IV診断・推論方式

**オーナー採用（2026-11-05）：I2。** S2で確定したB0・B1に対し、Anderson–Rubin（AR）検定反転を初期基準の**弱IV頑健な信頼集合推論方式**として採用する。初期の科学的適用範囲は、単一excluded IV／単一内生処置・独立観測・異分散頑健な漸近検定とする。First-stage効果・SE・Instrument support・適切なIV共分散を報告し、通常2SLS Wald型CIを弱IV頑健と表示しない。ARはexclusion・independence・monotonicityの成立を証明せず、cluster/HAC・時系列依存・複数IV等へ自動適用しない。**方式・初期適用境界の採用であり、AR検定統計量／数値実装／coverage・小標本補正／G2結果schema／Gateを承認したものではない。** 詳細の管理先は本ファイル、採用事実の管理先は02とする。

| 案 | 内容 | 重大な制約 | 技術判断 |
|---|---|---|---|
| **I1** | First-stage診断と通常2SLS Wald区間のみ。弱い場合はwarning | 弱識別時にnominal coverageを維持できず、区間表示が誤解を誘う | 非推奨 |
| **I2** | **B0/B1でAR（Anderson–Rubin）検定反転による信頼集合を初期の基準推論とする**。独立観測下のheteroskedasticity-robust漸近検定を候補とし、First-stage診断・正しいIV-SEを併記 | ARもInstrumentの無効性を補正しない。小標本の厳密coverageは保証されず、数値的反転の全領域確認が必要 | **オーナー採用（2026-11-05）** |
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

## 4. D03-3：弱IV信頼集合のResult表現（G2改訂採用、2026-11-06）

**オーナー採用（2026-11-06）：`D03-3_G2_REVISED_OWNER_ACCEPTED / FORMAL_SCHEMA_PENDING / SCIENCE_NOT_RUN`。** 有界・非有界・非連結・全実数を型付き区間集合として損失なく保存し、推論状態・点推定状態・科学的適格性を分離する**意味契約**を採用。汎用集合型には将来の`EMPTY`を表現する余地を残すが、初期just-identified B0/B1 ARで**正常な`AVAILABLE/EMPTY`を禁止**する。具体的field名・enum/JSON schema版・旧Result migrationはD04／Architecture Reviewへ委譲する。

### 4.1. 一次根拠・現在の既存仕様

- **弱IV頑健推論の集合形状：** Mikusheva (2010), [*Robust confidence sets in the presence of weak instruments*](https://dspace.mit.edu/entities/publication/702ee950-3381-435d-8a9e-b2f7d9eb7fed) は有限区間以外の集合が生じることを示す。[Stata公式解説](https://www.stata.com/stata-news/news39-3/weak-instruments-wacky-confidence-intervals/)も全実数・複数区間等を記載する。
- **重要な反証／G2原案の修正：** [Davidson & MacKinnon (2014), *Confidence sets based on inverting Anderson–Rubin tests*](https://academic.oup.com/ectj/article/17/2/S39/5056440) は**just-identified ARの信頼集合は空にならない**ことを導く。Stata公式解説もAR反転の空集合をoveridentifiedの場合と区別する。したがって、今回のB0/B1（1 excluded IV／1 endogenous treatment）は、**適格で非退化なAR反転が`EMPTY`を正常に返すMethodではない**。空集合を「モデル棄却」として無条件採用せず、有限gridの打切り／数値不具合／検定定義やrankの不適格を優先検証する。
- **標準JSON：** [RFC 8259 §6](https://www.rfc-editor.org/rfc/rfc8259.html#section-6) でJSON数値の`Infinity`／`-Infinity`／`NaN`は不許可。非有界端点は数値として捏造せず、nullable端点＋明示的な無界flagで型付けする。
- **既存Ariadneコード（参照HEAD：`83f94ff`）：** `src/ariadne/scientific/inference/adapter.py`はNative推定のpayloadに`confidence_interval: [ci_low, ci_high]`または`null`を保存し、`json.dumps`でartifact化する（同ファイル197〜213行）。現行`causal-analysis-spec/2`（`product/domain/analysis_spec.py`）の読み取りを保護する。これは**新規IV Result schemaが実装済みである証拠ではない**。旧Resultを破壊せず、新版で別集合契約を設ける方向をD04で審議する。

### 4.2. 比較した表現案

| 案 | 表現 | 科学的・互換上の評価 | 今回の推奨 |
|---|---|---|---|
| G0：有限CIのみ | `confidence_interval:[low,high]`のみ | 非有界・非連結の情報を喪失、ARの初期基準推論I2と不整合 | 不採用推奨 |
| G1：有限CI＋`unbounded`一個 | 1組の端点とflag | 二つの半無限区間の和集合や複数成分を表せない | 不採用推奨 |
| **G2改訂** | 集合形状＋**順序付けられた区間components**＋各端点のboundedness／推論状態 | 科学的集合を忠実に保存。既存有限CIと分離でき、Method別の許容集合を検証可能 | **オーナー採用（2026-11-06）** |
| G3：任意関数・predicate・高次元形状まで記述 | 将来Methodへ一般化可能 | 初期の1次元ARには過剰。監査とmigrationが重くなる | 初期非推奨 |

### 4.3. G2改訂案の型・不変条件

| Field群（設計案） | 不変条件 |
|---|---|
| `inference_method`, `confidence_level`, `covariance_type`, `test_distribution` | AR反転方式、名目水準、採用したcovarianceと漸近近似条件を記録。信頼水準の具体defaultは未承認 |
| `inference_status`, `reason_codes`, `validity_scope` | `AVAILABLE/UNAVAILABLE/NOT_REQUESTED/NOT_APPLICABLE/FAILED`等の区別（enum名は未確定）。科学的適格性と数値計算成否を混同しない |
| `confidence_set.set_kind` | 候補：`BOUNDED_INTERVAL / UNBOUNDED_CONNECTED / DISCONNECTED / ALL_REAL / EMPTY`。**Method別の結果形状制約を検証**し、B0/B1の正常AR結果では`EMPTY`を拒否 |
| `confidence_set.components[]` | 各要素は数直線上の区間（端点を昇順に列挙）。重複区間や接続する区間は正規化して結合し、`set_kind`との整合を検査する。AR反転の初期候補はclosed boundaries |
| `lower`, `upper`, `lower_unbounded`, `upper_unbounded` | 端点が有限なら数値かつunbounded=false、無界なら数値nullかつunbounded=trueとし、`Infinity/NaN`を書かない。下端・上端の方向は区間ごとに意味を固定 |
| `point_estimate_status`, `effect_point` | 点推定と集合の結果を独立保持。First stageゼロで点推定不能でも、AR信頼集合が利用可能な場合はその事実を失わない |
| `diagnostics`, `lineage_hash`, `backend_version`, `estimand_kind` | First stage、Question/Design/Graph/dataset、対象Estimand、再現性を追跡。B1の線形IV構造係数を無断でLATE表示しない |

**集合形状の一貫性（初期候補）：** `BOUNDED_INTERVAL`は有限1成分、`UNBOUNDED_CONNECTED`は無界の1成分（`ALL_REAL`を除く）、`DISCONNECTED`は2成分以上、`ALL_REAL`は両端無界の1成分として正規化する。`EMPTY`は汎用schema将来拡張用の0成分だが、**B0/B1の初期just-identified ARでは正常な`AVAILABLE/EMPTY`を禁止**する。単一点・半直線の境界上の退化ケースを表すため、端点の同値や接続形状も正規化規則・テストで定義する。

**Statusの意味:** (i) 統計的に得られた集合の形状、(ii) 計算できたか、(iii) 科学的に適格なDesignか、(iv) 点推定が定義されるかは独立する。`FAILED`と`EMPTY`を同一視しない。`ALL_REAL`は「効果なし」ではなく「この水準では実質的に範囲を限定できない」を意味する。`confidence_set=null`は未計算・不適用・失敗等のときにstatus/reasonと組み合わせて使い、非有界集合の代用にしない。

### 4.4. JSON表現例（**架空の数値／説明用、実測結果ではない**）

この例は、二つの半無限区間からなるAR信頼集合を表す。値`-1`と`2`、水準`0.95`は**説明のための任意の例**であり、Ariadneの実行結果やGateのdefaultではない。

```json
{
  "inference_status": "AVAILABLE",
  "inference_method": "ANDERSON_RUBIN_INVERSION",
  "confidence_level": 0.95,
  "confidence_set": {
    "set_kind": "DISCONNECTED",
    "components": [
      {
        "lower": null,
        "upper": -1,
        "lower_unbounded": true,
        "upper_unbounded": false
      },
      {
        "lower": 2,
        "upper": null,
        "lower_unbounded": false,
        "upper_unbounded": true
      }
    ]
  }
}
```

**旧Resultの互換性境界（D04へ引渡し）：** 既存Native `confidence_interval` の2数値/nullを変更したり、非有界集合をそこに縮約したりしない。新しいversioned Result/Artifactは`confidence_set`を第一級に持ち、既存`confidence_interval`は互換性上必要なら**集合が正確に一つの有限閉区間の場合に限って**導出可能なviewとする（是否・名称はD04で採決）。`confidence_interval=null`単独では推論不能か無界かを表せないため、必ず型付きstatus／`confidence_set`と一緒に解釈する。新規readerと既存readerの差はcontract/migration testで保護する。

### 4.5. 受入の反証・テスト境界（未実行）

1. **正例B0/B1:** 既知のAR反転referenceと比較し、有限単一区間・二つの半無限区間の和集合・全実数など、**実際に構成可能な形状をMethod別に**検証する。境界端点、区間順序、inclusive、集合の全域性を確認。
2. **`EMPTY`負例:** just-identified B0/B1から`EMPTY`が出たら、有限grid truncation／退化covariance・rank／数式実装エラーの可能性を優先して`FAILED/REQUIRES_REVIEW`等に分類。**正常なEMPTYを受入fixtureに設定しない**。将来overidentified等の異なる方法では、空集合の意味をMethodごとに再審査する。
3. **数値不変条件:** JSON schema validatorでNaN/Infinity禁止、端点有限性・無界flagの整合、区間の非交差・昇順、`set_kind`とcomponentsの整合、無限遠でのテスト反転の見落としを拒否。
4. **独立した状態:** First stageがゼロ等で`effect_point`なしでも信頼集合を保存可能か、失敗と未請求と不適用を区別可能か、旧Resultを回帰保護できるかを評価。
5. **科学的検証:** Monte Carloで弱・無・強First stageの無条件被覆率とType-I errorを測り、採用するARの統計量・漸近条件・標本サイズ・仮定違反の負例を区別。信頼水準・replicate数・許容差はSR-04／Gate 07で**事前固定**。

**採用の範囲:** **G2改訂の集合意味・表現原則をオーナー採用**した。AR反転の信頼集合を有限単一区間に偽装しない。**正式JSON schema/enum、D04互換仕様、具体実装、数値・coverage検証、科学Gate PASSを意味しない**。

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
| `D03R-T04` | B0/B1のjust-identified AR反転に対する独立referenceの集合一致、有限／非有界／非連結／全実数の構造試験。EMPTYは初期B0/B1で正常なAR集合とせず、誤実装・grid truncation等の負例として検査 |
| `D03R-T05` | Instrument invalid（exclusion・independence・monotonicity違反）ではAR実行結果を「valid IV証明」としない |
| `D03R-T06` | cluster/time依存、複数IV、連続Treatment等を初期契約では明示非適用。無警告のrobust CI出力を禁止 |
| `D03R-T07` | 適格・不適格Design別のcoverage/type-I error・数値精度、ランダムseed・反復数、被覆誤差の不確実性を測定 |
| `D03R-T08` | optional backend導入不可・effective version差・旧Native ATE/ATTの回帰を科学的不適格と区別 |

既存`SR03-T05/T06`はSR-03横断fixtureの参照IDであり、本ファイルの`D03R-Txx`は**提案レベルのMethod別詳細**とする。最終のGate Test ID、confidence level、許容誤差、Monte Carlo回数、CPU/OS/backend supportは独立Scientific Reviewで固定し、実測してからPASS判定する。デフォルトの弱IV F閾値や任意の数値品質基準を根拠なしに採用しない。

## 7. 決定票：Human ownerに残す採否

| ID | 判断・推奨 | 今後の審査・実証 |
|---|---|---|
| **D03-1** | **S2採用（2026-11-05）**：B0 just-ID＋B1 単一Z/A・事前指定Cの加法線形構造2SLS | 対象は採用済み。構造仮定の適格性・Estimandの誤表示防止・数値/推論Benchmark・受入Gateは別途検証 |
| **D03-2** | **I2採用（2026-11-05）**：B0/B1でAR検定反転を弱IV頑健な基準推論とする（独立観測・異分散頑健漸近推論） | 具体的AR実装・coverage・G2 schema・Gateは未承認 |
| **D03-3** | **G2改訂オーナー採用（2026-11-06）**：有界・非有界・非連結・ALL_REALを型付き区間集合で保存。汎用EMPTYは将来用に残すが、初期just-identified B0/B1の正常AR結果では禁止 | 集合意味の採否は完了。正式schema・legacy互換はD04、数値・coverage・GateはSR-04/Gate07へ引渡し |
| **D03-4** | **C1**：Cは初期非採用を維持し、科学的使用場面に基づく後続審議trigger/責任を確定 | C専用Issue/Owner、正式な再審議契機、初期除外の承認理由 |

**D03-3オーナー判断（2026-11-06）：** **G2改訂の集合意味契約を採用**。EMPTYの初期B0/B1での扱いを修正し、Method別validatorを必要条件とした。**正式schema・D04互換・SR-04 Science Acceptanceは未完了**。

**更新判定（2026-11-05）：** `D03-1_S2_OWNER_ACCEPTED / D03-2_I2_OWNER_ACCEPTED / D03-3_G2_REVISED_OWNER_ACCEPTED_2026-11-06 / D03-4_C1_PENDING`。S2の**初期保証範囲**とI2の**AR反転方式・初期適用境界**はオーナー採用済み。**G2改訂の集合意味契約は採用済み**。Cの後続管理C1、具体的AR実装・正式schema・依存lock・科学Benchmark/Gate 07・コード実装は**未承認・未実施**。既存の`A＋B採用／C追加審議`は変更しない。
