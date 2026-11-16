# ENH-E11 — SR-04 Execution Environment Contract（策定Draft）

**文書区分:** `working_notes`／科学的検証の実行環境・再現性・証拠管理契約案。正式なFR/NFR/AR、Architecture Decision、Gate06/07、Work Package、実装指示、Coding許可ではない。  
**作成日:** 2026-11-15 JST  
**対象:** `kousuke-ota-datascience/causal-atelier`、`prototype/ariadne_mvp`。  
**状態:** `SR04_E_ENVIRONMENT_CONTRACT_DRAFT / LOCK_AND_PROFILE_PENDING / RESOURCE_BUDGET_PENDING / EVIDENCE_SCHEMA_PENDING / SCIENCE_NOT_RUN / PENDING_FULL_CONCEPT_APPROVAL`。  
**先行する作業記録:** [Method Acceptance Matrix（41件）](20261115_sr04_method_acceptance_matrix_draft.md) → [Scientific Fixture Catalog（DGP 24／NEG 28／横断9）](20261115_sr04_scientific_fixture_catalog_draft.md) → [Reference Specification（REF 24）](20261115_sr04_reference_specification_draft.md) → [Quantitative Acceptance Criteria（AC 45）](20261115_sr04_quantitative_acceptance_criteria_draft.md)。  
**Owner決定:** [02 構想承認記録](../00_enhance_background/02_enhancement_concept_approval_record.md)。基本方針のみ個別採用済みであり、**全体構想は`PENDING_FULL_CONCEPT_APPROVAL`**。  
**根拠となる実測:** [SR-02 Python/Linux依存・API実行記録](20261101_sr02_backend_runtime_probe_results.md)。この実測はinstall/API smokeであり、Method別科学妥当性・完全なlock・SI納入適法性を示さない。

> **2026-11-16 Owner decision:** [DEC-SR04-01/02](20261116_sr04_dec01_b1_dec02_driv_owner_decisions.md) によりB1-Aの加法線形IV構造係数とDRIV-Aの条件付き構造IV斜率は科学的semantic targetとして採用。Eで未凍結の対象は**実効backend/依存lock、B1 AR/HC、DRIV W残差化nuisance/projection/CI、seed、resource、Method固有科学Benchmark**であり、Owner意味論判断と混同しない。全体構想は未承認。

> **2026-11-16 DEC-SR04-03／04 個別判断:** [DEC-SR04-03 FD-A](20261116_sr04_dec03_frontdoor_fd_a_owner_decision.md)、[DEC-SR04-04 GRAPH-A](20261116_sr04_dec04_graph_oracle_graph_a_owner_decision.md)の2件をOwnerが採用済み。FD-A採用でもDoWhy 0.14のstage/confinders・full lockは未検証。GRAPH-A採用でもcausal-learn/Tigramiteの実効CI-test、Graph endpoint、GPL顧客SI納入判断は未検証。SR02のinstall/API smokeはScience/Legal PASSではない。 正式FR/NFR/AR・Architecture・Gate07・Coding・全体構想は未承認（`PENDING_FULL_CONCEPT_APPROVAL`）。この判断より前に記録された「Frontdoor初期Methodの未決」「Graph Oracle採用方針未決」は**Owner方針のみ**解消し、実装・独立Science Oracleの未完成は維持。

> **2026-11-16 DEC-SR04-05-1〜7をOwnerが採用済み:** [準実験7手法の独立技術判断](20261116_sr04_dec05_quasi_experimental_seven_methods_estimator_inference_decisions.md)。DEC-05の設計基準を個別採用。ENV-BASEの計算backendに加え、Sharp/Fuzzy RDはPython rdrobustのoptional候補（未pin/未lock/未API probe）、ITSはHAC候補、SCMはconstrained optimization、SDIDは独立unit/time weightsと毎Bootstrap再最適化が必要。SI顧客納入License/Dependency/Compute/Science Evidenceは未承認。 本書の旧「Quasi estimator/inference未決」は**採用するMethod baselineの方針だけ**後続判断で解消した。実効Backendと独立Science Benchmark/正式FR/ADR/Gateは依然OPEN、全体構想は`PENDING_FULL_CONCEPT_APPROVAL`。

> **2026-11-16 DEC-SR04-06判断案（OWNER_PENDING）:** [Negative Control／OLS partial R²・RVの採否案](20261116_sr04_dec06_negative_control_ols_rv_scope_decision_proposal.md)。初期候補3MethodはENV-BASE、明示opt-in・研究Design/null・古典OLS係数/SE/df・backend/seed provenanceを要求するが、Method追加・lock変更は未承認・未実行。 **DEC06-1〜5推奨Aは未承認**。正式Scope採否・科学的Benchmark・Gate07/全体構想の状態は変更しない。

## 0. 目的・システム境界・再現性の分類

### 0.1. この契約が対象にすること

SR-04の41 Methodと横断9 Contractの実行に対して、**同じ科学的問い、DGP、seed stream、Method Config、Reference、実効ライブラリ、環境資源から得られた結果を監査・再実行できること**を設計する。対象は **Scientific Core／ローカルCLI／永続ローカルファイル**と、科学検証専用のCI/ローカルバッチ実行である。新Web/API/Worker/DBやProductデータ権限統合は含めない。

本Contractを記載しただけでは、既存コードがこれに適合する事実は生じない。新E11は旧Product/v2のschema・CLIの`REQUIRES_REVIEW + override`等の既存振る舞いを**別の回帰で保護**する。SR-03 D04/D06で採用された新E11のstrict identification/lineage gateは未実装・未検証。

### 0.2. 再現性Level（提案）

| Level | 要求する再現性 | 例外・判定 |
|---|---|---|
| `ENV-L0` contract | schema/Method/Estimand/Graph endpoint/typed reason/lineage/hashの**意味的一致** | 期待した値・型と不一致ならFAIL。seedや浮動小数点許容で救済しない |
| `ENV-L1` deterministic numerical | 同一完全環境・同一固定標本におけるdeterministic algebraとReferenceの**AC-D03数値許容内一致** | BLAS順序や浮動小数点差があるので、すべてのJSONバイト一致は要求しない |
| `ENV-L2` stochastic trace replay | 同一環境・同一`cell_id/replicate_id/stream_role`・Method Configで再実行可能、結果の数値差はMethod固有許容内 | RNGとparallelism固定。非決定的backendを利用するなら、同一seedのビット完全再現を自動保証せず、原因・許容・禁止範囲を登録 |
| `ENV-L3` scientific repeatability | 異なる独立seed/replicate集合でも事前登録されたCoverage/Bias/Type-I/Graph指標を再評価できる | 一試行のeffect一致とは別。95% CIのcoverageを単一seedで判定しない |
| `ENV-L4` cross-platform portability | 別CPU/OS/Python/Backend buildにおいて科学的に同等の結果 | **初期保証対象外。** 別environment profileの独立科学再受入が必要 |

**重要:** 「seed固定」だけでは、別Library version、BLAS/LAPACK、CPU演算、parallel scheduler、任意のBootstrap/Forestモデルまでビット一致するとは言えない。NumPy `Generator`にもversionを跨ぐstream互換保証はない。

## 1. 実測Baselineと採用候補Profile

### 1.1. GitHub/CLIの現物照合（2026-11-15）

| 対象 | 観測できた事実 | SR-04で追加が必要なこと |
|---|---|---|
| [`pyproject.toml`](https://github.com/kousuke-ota-datascience/causal-atelier/blob/prototype/ariadne_mvp/pyproject.toml) | `requires-python = ">=3.12,<3.13"`。科学用DoWhy/EconML/Tigramiteのextrasは未定義。`predictive-advanced`は存在 | Optional E11依存の独立extras、特定Methodへの適格性表、互換試験 |
| [`uv.lock`](https://github.com/kousuke-ota-datascience/causal-atelier/blob/prototype/ariadne_mvp/uv.lock) | 既存lockあり、Python要求`==3.12.*`。現行Project/既存extrasについてのロックである | E11 extras追加後に**同じcommitでlock再生成・整合検査**。現行lockをE11用に固定済みと誤認しない |
| [`scientific_stage.py`](https://github.com/kousuke-ota-datascience/causal-atelier/blob/prototype/ariadne_mvp/src/ariadne/interfaces/cli/scientific_stage.py) | Manifest v2、Python version、input/output hash、seed、`backend_version="ariadne/0.1.0"` | 実効`dowhy/econml/tigramite`とtransitive依存・CI/RNG/parallelism/Reference versionの保存 |
| [`estimation.py`](https://github.com/kousuke-ota-datascience/causal-atelier/blob/prototype/ariadne_mvp/src/ariadne/interfaces/cli/estimation.py) | 上流Manifest/Graph/Dataset hash、legacy `REQUIRES_REVIEW`経路あり | 旧v2回帰を保護し、新E11のfail-closed/lineage契約へ分離 |
| SR-02 GitHub Actions | `ubuntu-24.04`／Linux x86_64／Python 3.12.15、DoWhy 0.14、EconML 0.17.0、Tigramite 5.2.10.1で単独・同時導入/API smoke PASS | Lock、既存回帰、Known-truth、CI coverage、PAG fidelity、顧客SI配布ライセンスを未実施 |

**SR-02の観測された主なtransitive版**（採用決定ではない）：NumPy 2.2.6、pandas 3.1.0、SciPy 1.13.1、scikit-learn 1.9.1、statsmodels 0.15.0、causal-learn 0.1.4.8、LiNGAM 1.13.0。今後のlockはこの一覧をコピペして成立するものではなく、完全なresolution/配布wheel hash・import確認によって凍結する。

### 1.2. 審議対象Environment Profiles（正式profile名・固定値は未承認）

| Profile ID（案） | OS/Python/arch | Library選択 | 科学的目的 |
|---|---|---|---|
| `ENV-BASE` | Ubuntu 24.04 / CPython 3.12.x / x86_64 / CPU | 基盤Ariadneのみ | 旧Scientific CLI・E9回帰、純Python/NumPy Oracle |
| `ENV-DOWHY` | 同上 | DoWhy extra | P1のBackdoor/Frontdoor/IV識別・Frontdoor数値 |
| `ENV-ECONML` | 同上 | EconML extra | P2の7非IV CATE＋DRIVのモデル・Inference |
| `ENV-TIGRAMITE` | 同上 | Tigramite extra | P3 PCMCI/PCMCI+/LPCMCIのCI/Graph endpoint |
| `ENV-COMBINED` | 同上 | 全3 extra同時 | 依存干渉・旧CLI・Method実効互換性の回帰 |

**Owner採用済みの大枠:** Python3.12／Linux、DoWhy・EconML・Tigramiteを機能別optional、採用版を科学Benchmark後にlockする。  
**採用候補にすぎない具体値:** `ubuntu-24.04`、`CPython 3.12.15`、`x86_64`、CPU-only（上表）。SR-02の実績から合理的な出発点だが、正式な最低保証環境/patch固定/architecture採否は未決。GPU・aarch64・Windows・macOSを自動保証しない。

### 1.3. Dependency Resolution契約（Owner未承認の細目）

- **Extras名候補:** `e11-dowhy`、`e11-econml`、`e11-temporal`。名称・実際のextras定義は提案であり、現行`pyproject.toml`には存在しない。既存`predictive-advanced`を暗黙選択しない。
- **採用Backendバージョン候補:** `dowhy==0.14`、`econml==0.17.0`、`tigramite==5.2.10.1`。SR-02で動作した版であり、今回の科学受入完了やその版への最終pin決定ではない。
- **Lock整合性:** 各Profileで`uv sync --locked --no-dev [--extra <profile-extra>]`を使用する案を基本とし、`uv lock --check`／依存整合`uv pip check`／実効`importlib.metadata.version`の照合を記録。既存`dev`を使用するpytest Profileは適切な`--group dev`等を別指定し、runtime profileへ開発依存を紛れ込ませない。
- **`--frozen`を正式環境確認に代用禁止:** `--frozen`はlockとProject metadataの整合検査を省略するため、CI正式受入では`--locked`を標準候補とする。
- **`uv.lock`は万能配布物ではない:** 実効Python patch/build、platform、wheel hash、optional dependency selected extras、BLAS/OS runtime、native library ABIを別に記録。editable installを利用する場合もrepo commit SHAとdirty-tree statusを保存。
- **Matrix:** `ENV-BASE / ENV-DOWHY / ENV-ECONML / ENV-TIGRAMITE / ENV-COMBINED`のProfileごとにfresh environmentでlock/install/dependency-check/import/Method smokeを実行。Combinationで成功しても単体Profilesのimport isolationを省略しない。
- **Failure:** lock stale、package/version mismatch、wheelのIntegrity failure、required optional dep missing、Backend API incompatibilityをそれぞれ型付きEnvironment failureとし、Methodの科学的`NOT_IDENTIFIED`や`INSUFFICIENT_OVERLAP`と混同しない。

## 2. RNG・独立性・再実行契約

### 2.1. RNG policy（提案）

- **Generator候補:** NumPyの`SeedSequence`＋`Generator(PCG64DXSM(...))`。`PCG64DXSM`は明示的な提案であり、既存Ariadne/外部Backendに同じBitGeneratorを強制できた証拠ではない。実際のNumPyの採用版とBitGenerator種別をfreezeする。
- **Root entropy:** 検証キャンペーン固有の128-bit等のroot entropyを事前に生成、実際の整数・生成日・秘密情報ではないこと・独立性をManifestへ記録。数値例を固定seedと偽称しない。
- **安定なstream key:** `campaign_id / dgp_id / scenario_id / replicate_id / purpose / optional method_id / bootstrap_index` を**規定した正規化UTF-8符号化→SHA-256→固定byte-order整数列→SeedSequence**に渡す。Pythonの組込み`hash()`、worker PID、処理順序、現在時刻でseedを導出しない。
- **streamの区分:** `data_generation`, `potential_outcome_noise`, `treatment_assignment`, `nuisance_split`, `method_fit`, `bootstrap_resample`, `graph_ci_test`, `reference_secondary_check`など。用途追加時は`stream_schema_version`を改訂。
- **paired comparison:** 同一DGP/scenario/replicateの**Data generation streamはMethod間で共通**にする。一方、Method固有内部乱数/fit/fold/BootstrapはMethod ID＋roleを含むstreamで分離。Method数・ジョブ分割・ワーカー順序の変更がDGP sampleの乱数列を変えない。
- **非対応Backend:** `random_state`が整数しか受け付けないAPI等は、固定seed列から各run固有の範囲内整数を導出し、完全な変換手順を保存する。単に`np.random.seed(seed)`をworkerごとに再利用して複製列を生じさせない。
- **出力:** `rng_algorithm`、`numpy_version`、`root_entropy`、`stream_schema_version`、`stream_key`、`derived_seed_digest`、Methodへ渡した`backend_random_state`、fold/bootstrapの構成、`replicate_id`、`seed_derivation_code_hash`を記録。秘密鍵・認証tokenは一切出力しない。

**Pythonコード化前の不変条件:** 同一`cell_id+replicate_id+role`で同一seed、異なるrole/replicateで別seedを得る。Method間のDGP一致、リトライ／shard数変更でDGP入力hashが維持されること。これは衝突確率が絶対に0であるとの主張ではない。

### 2.2. Parallelism・BLAS・CPU契約

- **Reference / deterministic Tier:** 初期baselineは単一process、`n_jobs=1`、`OMP_NUM_THREADS=1`、`OPENBLAS_NUM_THREADS=1`、`MKL_NUM_THREADS=1`、`BLIS_NUM_THREADS=1`、`NUMEXPR_NUM_THREADS=1`を候補とする（各env/buildで実際のthreadpool情報を計測）。**Python import前**に設定。
- **Monte Carlo Tier:** replicate単位のprocess並列化を許容し、各replicateが予定したRNG streamを受け取る。ワーカー数`n_jobs`は測定後にfreezeし、nested parallelismとBLAS oversubscriptionを禁止。並列化方法（joblib loky/spawn等）を固定。
- **Method内部並列:** Forest、Graph CI-test、Bootstrap、external backend独自thread設定は必ずeffective configとして記録。無制御な`n_jobs=-1`や共通global乱数は正式Science Tierでは許可しない。
- **異なるshardでの再現:** 集計を`replicate_id`順で行い、数値上の総和順序（compensated summation/固定reduce order）を定義する。fold/Bootstrapの実行時間による並び替えで分析母数が変わらないこと。
- **bitwise再現の制約:** 同一seedでも、非決定的GPU kernel、異なるBLAS/build、並列reduction、Library releaseでbitwiseは保証できない。ENV-L1/2で数値差許容をMethod別登録し、許容不能な非決定性は`INCONCLUSIVE`/環境非適格とする。

### 2.3. Sampling planと独立seed管理

SR-04-DのR=6,000/セルは**候補**。p=.95ならMCSE≈0.002814、反復数R・処置support・対象値x・時間T・cluster/donor単位はMethod別にfreezeする。

- **Pilot/正式のseed隔離:** `campaign_id`とroot entropyを別にし、pilot結果を見て正式seedを差し替えない。Pilotで数値ACを事後調整する場合は正式freeze前にのみ許可し、調整理由と再審議を記録。
- **途中停止/失敗再実行:** 失敗replicateを黙って捨てず`R_total/R_attempted/R_point_available/R_inference_available/R_covered`を保存。Retryは同じ`replicate_id`とseedで実施し、その試行履歴・原因・最終の採否を残す。
- **失敗の分母:** 非収束やCI unavailableだけを除外してCoverageを過大評価しない。主結果には`coverage | interval available`と`availability / all repeats`、`joint coverage-and-availability / all repeats`を併記。
- **同一replicate内の複数x/edge:** 独立replicateとして反復数を水増ししない。multi-comparison `K`をSR04-DのACに従い事前にfreezeする。
- **逐次的なR増分:** INCONCLUSIVEへの追加Rは事前定義した独立seedの増分・判定/多重性管理に従う。データを見ながら無制限に反復を増やして好都合なPASSを選ばない。

## 3. Method family別Environment Profile・RNG/推論・資源

### 3.1. 全41件への割当（Method IDは先行Matrixと同一）

| Family / Method IDs | Profile（候補） | 実行時固定すべきMethod固有変数 | 科学的注意 |
|---|---|---|---|
| P1-M01〜02 / Native Randomized, Backdoor | ENV-BASE | Graph/Design/version、reference algebra | Identity/adjustmentはdeterministic。CI要求なし |
| P1-M03〜05 / DoWhy Backdoor/Frontdoor/IV識別 | ENV-DOWHY | DoWhy method id/graph/identify config、dataset typing | 識別API successを因果効果Science PASSへ昇格禁止 |
| P1-M06 / FCI | ENV-BASE | causal-learn version/CI-test/alpha/bootstrap seed/endpoint schema | PAG oracle 未完成。loop数・CI-testの実効versionを記録 |
| P1-M07 / Frontdoor数値 | ENV-DOWHY | stage1/2回帰・confounder、single mediator、inference config | 0.14の実効stage/CI未承認 |
| P1-M08〜11 / Diff/OLS/IPW/AIPW | ENV-BASE | effective PS/Outcome nuisance/normalization/crossfit/SE | ATE/ATT別sample unit、weighted ESS |
| P1-M12〜17 / Refutation, Sensitivity | ENV-BASE（DoWhy method利用時ENV-DOWHYを別profile） | placebo/subset/Bootstrap/clip rule、resample unit、iteration count | REF-R01、真のNCとRandom CCを分ける |
| P1-M18〜20 / NCE/NCO/partial-R²候補 | ENV-BASE | opt-in、null conditioning、classic OLS SE/df、RV version | **Method正式Scope未採用**。実装しないまま科学合格と扱わない |
| P2-M01〜07 / non-IV CATE 7 estimator | ENV-ECONML | nuisance/final model・crossfit・train/test・X/W・bootstrap/forest inference | 7つを一律Bootstrapにしない。pointwise vs simultaneous |
| P2-M08 / DRIV | ENV-ECONML | Treatment/Z型、IV moment、first-stage、final projectionとCI method | DRIV-A条件付き構造斜率semantic targetは採用済み。実効0.17.0・final projection/CI未検証、complier LATEと区別 |
| P3-M01〜03 / PCMCI, PCMCI+, LPCMCI | ENV-TIGRAMITE | CI-test、tau_max、lag0、stationarity、time index、randomness | PAG/CPDAG endpoint、Tigramite experimental状態、GPL別Gate |
| P3-M04〜08 / DiD, Event, ITS, Sharp/Fuzzy RD | ENV-BASE＋採用計算backend | panel/time/cluster、HAC/bootstrap、cutoff/bandwidth、cohort weights | **specific estimator/inferenceまだ未採用**。無条件IID SEの汎用化禁止 |
| P3-M09〜11 / Wald, B0, B1, AR | ENV-BASE＋採用IV backend | binary Z/A、first-stage、pre-treatment C、HC method、AR inversion | B0/B1 I2独立観測・異分散頑健漸近、G2集合、B1-A構造係数semantic targetは採用済み、正式schema enum・AR/HC/coverage未検証 |
| P3-M12〜13 / SCM, SDID | ENV-BASE＋採用最適化backend | donor rank、unit/time weights、optimizer/tolerance/seed、preperiod | target/optimization/SE初期選定待ち |

**Method ID静的網羅:** 上表の範囲表記は次の集合を意味する。P1: P1-M01, P1-M02, P1-M03, P1-M04, P1-M05, P1-M06, P1-M07, P1-M08, P1-M09, P1-M10, P1-M11, P1-M12, P1-M13, P1-M14, P1-M15, P1-M16, P1-M17, P1-M18, P1-M19, P1-M20。 P2: P2-M01, P2-M02, P2-M03, P2-M04, P2-M05, P2-M06, P2-M07, P2-M08。 P3: P3-M01, P3-M02, P3-M03, P3-M04, P3-M05, P3-M06, P3-M07, P3-M08, P3-M09, P3-M10, P3-M11, P3-M12, P3-M13。 合計41件であり、ENV Profileが具体Methodを新規採用したという意味ではない。

**Backend未承認のMethod:** 上の`ENV-BASE＋採用計算backend`は実際に依存なしで実装可能と保証する意味ではない。method-specific external dependency/OS compatibilityはSR-02の追加判定対象とする。

### 3.2. Tier・リソース予算の契約案（数値Budgetは未承認）

| Tier | 目的 | 実行前の必須予算項目 |
|---|---|---|
| `T0-contract` | JSON、hash、Graph readback、status、AR代数shapeなど | fixture数、数値型、固定sample、wall time、memory ceiling。MC反復は不要 |
| `T1-probe` | extras単独/同時install、Backend API smoke、旧CLI/Scientific regression | Profiles数×Method API件数、OS/Python/wheel availability |
| `T2-pilot` | Methodのtime/memory/error-rate測定、DGP難度とR妥当性 | 先行SR04-Dのpilot候補R=100〜200、n/T/inner-bootstrap数、CPU threads |
| `T3-science` | pre-registered full Monte Carlo、coverage/Bias/Graph誤差 | `Σ_cell [R_cell × (median_fit_time_cell × nuisance/folds/bootstrap overhead)]`、peak RAM、ディスク、job timeout、CI保存期間 |
| `T4-regression` | 旧Product/v2、E9、optional依存無し/有り | baseline regression suite、差分許容、将来のRelease changes |

- `R=6,000`は`T3`の候補であり、**41 Method×全DGP×全n/Inferenceへ無条件に展開する資源承認ではない**。森林型・nested Bootstrap・FCI/LPCMCI・SDIDはpilot測定後にMethod×cellを選び、検出力/MCSEと予算をセットで審査。
- **予算見積りの保守性:** medianだけでなくp90/p99 wall time、peak resident memory、fail/retry率、disk per replicate、BLAS threads、job concurrency、CI artifact retentionを測定すること。
- **上限超過の扱い:** TIMEOUT、OOM、dependency failureをSCIENCE_NEGATIVE_RESULTと混同しない。必須Rを満たせない場合は`INCONCLUSIVE`／`BLOCKED`でOwnerに資源/方法/閾値の再承認を要求。勝手なサンプル削減でPASSにしない。
- **初期資源値:** vCPU数、RAM GiB、storage GiB、1-job timeout、Max workers、全Rの実行費用は**未測定・未freeze**。固定値を発明しない。

## 4. Manifest・成果物・証拠保存契約

### 4.1. 科学実行Manifestの最小必須フィールド（新E11の設計候補）

| Category | Required fields（案） | 禁止/注意 |
|---|---|---|
| Identification/Study | question/estimand definition/target population/contrast/design/graph/DGP, dataset hash、method id | Graph discovery結果を自動的にDAG/IDENTIFIEDと変換しない |
| Code | repo commit SHA、dirty-tree flag、E11 code/adapter version、reference generator/oracle source SHA | 最新branch名のみの記録は禁止 |
| Env | OS release、kernel、CPU arch/microarchitecture、Python executable/patch/build、uv version、dependency extras profile | SR-02で使用した観測版を未来のenvとして固定したと偽称禁止 |
| Dependency | pyproject/uv.lock SHA、effective all installed packages/version、critical wheel hashes、numpy/scipy/sklearn/statsmodels/BLAS/LAPACK | `backend_version="ariadne/0.1.0"`のみでは不足 |
| Runtime | core_count、threads/BLAS env、threadpool info、parallel backend、workers、CPU/GPU | 速度と科学精度が再現可能と断定しない |
| RNG | root entropy、BitGenerator、SeedSequence/derivation schema、replicate/stream keys、backend random_state | PID/time/hash()由来の導出禁止 |
| Simulation | campaign/cell id、n/T/cluster/donor/bandwidth、R planned/attempted、nuisance/folds、inner bootstrap、K/z_K | 比較セルを後出しで削除しない |
| Result status | point/inference/science/eligibility status、fail code、retry/timeout、source data and reference hashes | CI=nullとゼロ幅区間の混同禁止 |
| Metrics | Bias/RMSE/MCSE、conditional coverage、availability、size/Graph metrics、multiplicity adjustment parameters | `R_ci`を`R_total`と偽表示しない |
| Artifacts | each artifact relative path/hash/bytes/format/schema、manifest/reference evidence hash | absolute pathsや個票の無断外部export禁止 |
| Governance | proposal/approved/evidence status、reviewer、approval snapshot SHA、Gate trace | draftをOwner acceptedやScience PASSへ昇格禁止 |

**既存との差分:** 現行v2 Scientific CLIはPython version・一部input hash等を持つが、Method-specific effective Backend/RNG/parallelism/Reference・Science metric全項目を満たさない。**既存v2のManifest schemaを直接上書きする指示ではない**。D04 V2/R2の版別設計と回帰保護が前提。

### 4.2. ファイル書込み／再読込

- **Atomic commit:** 同一filesystem内の一時ファイル→flush/fsync（必要度はStorage設計で確定）→rename、manifestは全artifact hash計算完了後に確定する（実装設計前の契約案）。途中中断時はcommit済みと扱わない。
- **Canonical identifiers:** `campaign_id/cell_id/replicate_id/attempt_id` を明示。duplicate replicateの上書きは禁止。retry時に古い成功と新しい失敗を黙って置換しない。
- **Hash:** input dataset/Graph/Question/Design/Split/Reference/lock/outputsはSHA-256、byte-level hashと意味正規化digestの用途を分離。schema version・JSON canonicalization・Parquetの並び・圧縮差の扱いを後続設計で固定。
- **Readback:** Artifactsを書いた後に戻してschema/hash/point vs confidence set/CPDAG-PAG endpoint/overridden warningの意味一致を検証。AR非有界端点はJSONのInfinityではなくnull + flagsで保持。
- **個票・秘匿:** 実証はsynthetic dataを既定とし、顧客実データをScience fixtureの既定入力にしない。個票CATE Parquetは明示的許可・PII/機微情報審査・保存先制約。CIログにdataset raw value/token/秘密情報を流さない。
- **Logs:** Structured logsにenvironment/reference IDs、start/end UTC timestamps、status、reason、resource usageを記録。失敗時もManifest/診断evidenceを安全に保存。ログ保持期限と顧客データの扱いはSR-10/Architectureで決定。
- **CI Artifact:** GitHub Actionsに期限付きで残るartifact ZIPだけをcanonical科学証跡にしない。Run URL/commit/hashと必要な集約証拠を保持する永続保存先・retention policyをArchitecture/Ownerで決定する。

### 4.3. Manifest（文章上のexample）

`manifest.json`に少なくとも`env_profile_id`、`python_version`、`platform`、`uv_lock_sha256`、`effective_distributions`、`blas_info`、`cpu/thread settings`、`rng_spec`、`campaign/cell/replicate IDs`、`method/inference versions`、`input/output/reference hashes`、`R_total`と`R_ci`、`science_status`／`approval_ref`を版付きフィールドとして保存する。スキーマやJSONの具体キー名はArchitecture/SR04-Fでfreezeし、既存`CliManifest`へ無断の後方非互換変更をしない。

## 5. Preflight・試験・Gateの環境Acceptance

### 5.1. ENV-ACの定義（全9件）

| ENV-AC ID | ケース・検査 | Draftの受入条件 |
|---|---|---|
| `ENV-AC01` | Runtime/Architecture | 採用OS/Python/archと実効versionがProfileに一致。未採用profileをPASS扱い0件 |
| `ENV-AC02` | Lock/SBOM/Extras | fresh environmentで`uv sync --locked`・`uv pip check`成功、実効依存/version/profile記録率100%。欠落・stale lockがあればfail |
| `ENV-AC03` | Backend isolation | BASE、DoWhyのみ、EconMLのみ、Tigramiteのみ、Combinedの5 profileで必須Method import/API/旧回帰。disabled optionalのMethodだけtyped unavailable |
| `ENV-AC04` | RNG and splits | 同cell/replicate/role→同seed・異role/replicate→異stream、DGP sample hashesがworker count/shard/retryに不変。fold leakageの明示負例誤許可0 |
| `ENV-AC05` | Parallel numerical reproducibility | 単processと採用parallel profileでE0は100%意味一致、E1/E2はMethod別数値許容内。非決定性の証拠欠落ならBLOCKED |
| `ENV-AC06` | Budget/retry/fail denominator | `R_total`とfailure/available countsの整合、計画Rからの黙示欠落0、timeout/OOMの科学的Status混同0 |
| `ENV-AC07` | Manifest/lineage/artifact | 実効Backend・lock・source/Reference SHA、RNG/compute configの欠落0、hash/readback/atomicity/duplicate処理契約全件一致 |
| `ENV-AC08` | Privacy / legacy | 未承認の個票export/path traversalの誤許可0、旧Product/v2回帰期待差分0、新E11未識別override偽解除0 |
| `ENV-AC09` | GPL/customer delivery | Tigramiteを含む個別顧客SI納入の法務・配布構成Reviewが`APPROVED`でない限り**delivery-ready FALSE**。内部科学計算のPASSと納入適法性を混同しない |

これらは**正式Gate番号や新コード実装の承認ではない**。9件のENV-ACは先行Matrixの`X-01〜X-09`に対する環境契約の切り口であり、既存横断9件を別物に置換しない。

### 5.2. SR04-Dの45 ACとEの関係

| SR04-D Acceptance | Environment側の条件 |
|---|---|
| `AC-D` numerical/typed | 正しいfloat dtype・BLAS・source+data hash、リトライ時の同一sample |
| `AC-A` AR set | HC/exact threshold/reference precisionのversionとFull-real domainの数値処理 |
| `AC-I` confidence coverage | inferential method・bootstrap repetitions/seed・R分母・n/support・K/z_K |
| `AC-T` Type-I/power | null/alternative DGP+CI-test version・MC seed streams・family correction |
| `AC-P` bias/RMSE | target truth、nuisance/split・R_failed/nonfinite、DGP noise/scale |
| `AC-G` Graph | temporal CI test・lag/timestamp/CI-test assumptions・endpoint schema/Graph oracle |
| `AC-Q` quasi experiments | panel/cluster/time/cutoff/donor design・Method-specific SE/optimizer |
| `AC-R` refutation/sensitivity | placebo/bootstrap/null/resampling unit・classic OLS vs HC3・reference version |

**科学不合格と環境不合格の混同禁止:** 環境が整合していても不適切な識別や推定バイアスがあればScience FAIL。Environment failureを`NOT_IDENTIFIED`へ変換しない。Graph uncertaintyやMethod-specific `null`推論は、環境成功と独立に意味を保持する。

### 5.3. Negative/Regressionと実行成果の最小範囲

- **41 Method**をPhase・Method family別Profileへ全件接続、**28 NEG**は先行Scientific Fixture Catalogの同一IDを使用し、適格な拒否・科学stress・検出不能性を分離する。
- **X-01〜X-09**はversion/Graph/Result/lineage/privacy/legacyをENV-ACで回帰。**旧E9/既存CLI**は新E11未実装段階でのbaselineを保持してから差分試験する。
- **SR-02の15 API smoke**は依存作動のpreflightとして再利用可能だが、SR04-DのScience数値を満たした証拠ではない。
- **Status:** preflight failure→`ENV_BLOCKED`候補、Method scientific invalidity→従来の科学契約、対象不確定→`CONTRACT_BLOCKED`候補、sample numerical failure→`NUMERICAL_INCONCLUSIVE`候補。正式status enumとexit codesはSR-03/Architecture判断待ち。

## 6. Licensing・Supply Chain・顧客SI納入

### 6.1. 正式Owner方針と既知根拠

SR-02で採用された配布想定は**個別SIでの顧客環境への構築・納入**でありSaaS前提ではない。Tigramite upstreamはGPLv3（または以降）で配布される。**科学実行が成功したこと**、`optional import`であること、顧客が`pip install`することは、特定の納入物全体の法的な適合性の証拠ではない。

### 6.2. 納入判定に必要なEvidence（本Draftでは未承認）

| 項目 | 提案する記録 |
|---|---|
| Third-party inventory | direct/transitive packages、effective versions、配布ファイル、wheel/source hash、SPDX等のライセンス識別 |
| Distribution mode | リポジトリ／wheel／コンテナ／顧客サイトへのcopy、動的／静的結合、修改コード、別process、ソース提供手段 |
| GPL obligations | ライセンス/著作権通知、source/corresponding source提供義務、変更物の扱い、相互結合の法的評価 |
| Customer agreement | 顧客契約の再配布制限、ソース提供義務との整合、委託先/第三者の役割 |
| Human decision | 法務／契約審査の結論、対象artifact/SHA、承認者、承認対象の配布形態 |
| Failure | 法的適合性未確認／不適合時はTigramiteを含むdelivery profileを`DELIVERY_BLOCKED`。内部研究Methodを勝手にScopeから削除しない |

**法的結論はここで出さない。** 追加制限/改修/納入方法の変更が必要ならOwner+法務の正式判断を要し、科学Methodの同等代替は別の科学BenchmarkとScope再承認に付す。

## 7. 未解決Blocker・受入前の依存と次工程

### 7.1. SR-04 E策定完了の定義

**作成完了（本Draft）:** 環境Profile、optional依存/lock手順、RNG階層・repeat/shard・parallelism、科学検証計算予算、Manifest・Evidence、privacy/legacy、ENV-AC01〜09、GPL配布Gateを定義。SR04-Dの数値ACと41 Method/28 NEG/9横断を環境側へ引き渡した。

**完了していないこと:** `pyproject.toml` extras追加、`uv.lock`更新、Python patch/backend pin、E11 Manifest schema、Reference code、環境profileのfresh install、SeedSequence実装、並列Replay/Monte Carlo実測、n/R/K/計算予算のfreeze、各Method科学acceptance、SI GPL審査、正式FR/ADR/Gate07承認。

### 7.2. 実施前に決める依存事項

| 優先 | 論点 | 決定・証拠の帰属 |
|---|---|---|
| OWNER_RESOLVED / SCIENCE_BLOCKER | B1-A／DRIV-A semantic target採用済み、B1のHC AR・DRIVの実効moment/projection/CI未検証 | SR03-R01/R02、SR04-C/D/F、Scientific Methods owner |
| BLOCKER | Frontdoor二段階実効仕様、FCI/LPCMCI PAG oracle | SR04-C、Method別検証 |
| BLOCKER | Quasi/SCM/SDIDの初期Estimator＋InferenceConfig | SR-09、SR04-D/F |
| BLOCKER | Environment Profile exact版とextras・full resolution lock／旧回帰 | SR-02/10、Architecture |
| BLOCKER | Monte Carlo mandatory cells、R/n/T/KとCPU/RAM/time/cost | SR04-D/E、Owner承認 |
| BLOCKER | 実効Manifest/seed/Graph lineage/Reference・PrivacyのSchema | SR03-D04、SR04-E/F、Architecture |
| BLOCKER | 個別顧客納入時のTigramite GPLv3適合 | Legal/Distribution gate。Science Gateと独立 |
| MAJOR | NCE/NCO/partial-R²の正式Method採否、既存Product GAP帰属 | SR-01/05/06、Owner |
| MAJOR | 68 Scope行・41 Method・9横断→FR/Issue/Gateの完全追跡 | SR04-F、SR-12、05レビュー |

### 7.3. 次工程への引渡し

**次：SR-04 Gate07 Traceability（F）**。Method ID → Scope row → DGP/NEG → Reference → AC-D〜R → ENV-AC → Backend/profile → requirement/Issue → Gate07 evidenceを結ぶ。ただし実行・Acceptance・Gate freezeの開始は別の正式承認後のみ。

後続の実装工程で必要な例を示したが、**本書は実装Agentの起動指示ではない。** SR-03とSR-01〜12の未解決事項、全体構想・Architecture Review、正式FR/NFR/AR、承認Snapshot、Gate06/07 freezeまではCodingを実行しない。

## 8. 追跡可能な外部一次資料

1. [uv: Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/) — `uv sync --locked`がoutdated lockを拒否すること、`--frozen`との差。
2. [uv: Optional dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/) — extrasによる機能別依存分割。
3. [NumPy: Parallel random number generation](https://numpy.org/doc/stable/reference/random/parallel.html) — `SeedSequence`／子stream。
4. [NumPy: RNG compatibility policy](https://numpy.org/doc/stable/reference/random/compatibility.html) — `Generator`のversionを跨ぐbitwise保証制限。
5. [joblib: Random state within Parallel](https://joblib.readthedocs.io/en/stable/auto_examples/parallel_random_state.html) — multiprocessingで乱数列を重複させうる条件。
6. [Tigramite upstream license](https://github.com/jakobrunge/tigramite/blob/master/license.txt)／[README License section](https://github.com/jakobrunge/tigramite/blob/master/README.md) — GPLv3ライセンスの直接記録。
7. [SR-02独立実行記録](20261101_sr02_backend_runtime_probe_results.md) — 本Projectで実証済みなのはInstall/API smokeの範囲である。
