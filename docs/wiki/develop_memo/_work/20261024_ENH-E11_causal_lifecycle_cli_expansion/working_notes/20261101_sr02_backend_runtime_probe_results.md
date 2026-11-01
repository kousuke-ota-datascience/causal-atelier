# ENH-E11 — SR-02 Python 3.12／Linux 依存・Method別API実行検証結果（第1回）

**証拠確定日:** 2026-11-01（日本時間）  
**文書区分:** `working_notes`／実機CIログに基づく一次検証結果。正式要件・設計・科学Gateではない。  
**判定:** `INSTALL_AND_API_SMOKE_PASS / SCIENTIFIC_ACCEPTANCE_PENDING / SR-02_PARTIALLY_RESOLVED`。  
**検証コミット:** [fa6fbb2c8b02b2219c6262f3c1d9363325bc26b8](https://github.com/kousuke-ota-datascience/causal-atelier/commit/fa6fbb2c8b02b2219c6262f3c1d9363325bc26b8)。  
**実行Run:** [GitHub Actions #41270427977](https://github.com/kousuke-ota-datascience/causal-atelier/actions/runs/41270427977)、`completed / success`、実行時間記録`2026-11-01T03:45:26Z〜03:46:06Z`。  
**Jobの証拠:** [DoWhy](https://github.com/kousuke-ota-datascience/causal-atelier/issues/14#issuecomment-6553025112)、[EconML](https://github.com/kousuke-ota-datascience/causal-atelier/issues/14#issuecomment-6553024687)、[Tigramite](https://github.com/kousuke-ota-datascience/causal-atelier/issues/14#issuecomment-6553023659)、[同時導入](https://github.com/kousuke-ota-datascience/causal-atelier/issues/14#issuecomment-6553026102)。  
**証跡Artifact:** Run内に`sr02-dowhy`／`sr02-econml`／`sr02-tigramite`／`sr02-combined`の各ZIP（result JSON、Method表Markdown、導入ログ）。保管期限は2026-12-01予定、永続証跡としてGitHub Issueコメントと本記録を併存させる。

## 0. INTRODUCTION

### 0.1. 何を実行したか

`prototype/ariadne_mvp`へ、検証専用の[`.github/workflows/enh-e11-sr02-probe.yml`](https://github.com/kousuke-ota-datascience/causal-atelier/blob/fa6fbb2c8b02b2219c6262f3c1d9363325bc26b8/.github/workflows/enh-e11-sr02-probe.yml)と[`scripts/verification/enh_e11_sr02_probe.py`](https://github.com/kousuke-ota-datascience/causal-atelier/blob/fa6fbb2c8b02b2219c6262f3c1d9363325bc26b8/scripts/verification/enh_e11_sr02_probe.py)を追加してGitHub Actionsで実行した。すべてのジョブは`ubuntu-24.04`で`Python 3.12.15`を作成し、**現行Ariadneを`-e .`で含め**DoWhyのみ／EconMLのみ／Tigramiteのみ／3ライブラリ同時の4通りを独立インストールした。使用した候補版は`dowhy==0.14`、`econml==0.17.0`、`tigramite==5.2.10.1`。**uv pip install／uv pip checkの両方が4通りともexit 0**。

合成データを生成して、DoWhy（4プローブ）、EconML（8プローブ）、Tigramite（3プローブ）の合計**15 API smokeプローブ**を単独・同時導入で実行。各JobのPythonコードは例外をMethod単位で記録する。Workflowが`success`でもMethod単位の`PASS`を別途確認するという**二層の証拠**を採った。今回の4Jobでは全Methodの主操作に`PASS`が記録された。

### 0.2. 実効環境・依存解決

| 項目 | Jobで観測した実効version |
|---|---|
| Runner | `ubuntu-24.04` / x86_64 / Linux（GitHub-hosted） |
| Python | `3.12.15` |
| DoWhy | `0.14` |
| EconML | `0.17.0` |
| Tigramite | `5.2.10.1` |
| NumPy | `2.2.6` |
| pandas | `3.1.0` |
| SciPy | `1.13.1` |
| scikit-learn | `1.9.1` |
| statsmodels | `0.15.0` |
| causal-learn | `0.1.4.8` |
| LiNGAM | `1.13.0` |

**注意:** この表は**実行されたversionの記録**であって、`uv.lock`の更新・上記の全transitive packageのlock確定ではない。配布用optional extrasは`pyproject.toml`にまだ導入していない。研究者のLinuxディストリビューション・GPUなどの保証にも拡張しない。

## 1. Method別API smokeの結果

### 1.1. DoWhy（Phase1）

| Method | 初回結果 | API検証の意味／未検証 |
|---|---|---|
| Backdoor identify | **PASS** | backdoor調整集合`X`を取得。モデル・DAGの妥当性や他識別条件の網羅は未認定 |
| Backdoor estimate | **PASS** | `backdoor.linear_regression`で有限推定値`1.924898...`を取得。既知真値誤差の科学Benchmarkは未実施 |
| Frontdoor identify | **PASS** | `frontdoor_variables=['M']`を取得。Frontdoor数値推定・負例は**未実行** |
| IV identify | **PASS** | `instrumental_variables=['Z']`を取得。IV/LATE数値推定・弱IV負例は**未実行** |

### 1.2. EconML（Phase2）

| Method | `fit`／`effect` | `effect_interval`（今回の実行設定） |
|---|---|---|
| LinearDML | **PASS** | **FINITE** |
| CausalForestDML | **PASS** | **FINITE** |
| DRLearner | **PASS** | **利用不可**：`Only point estimates are available!` |
| ForestDRLearner | **PASS** | **FINITE** |
| SLearner | **PASS** | **利用不可**：`inference is None` |
| TLearner | **PASS** | **利用不可**：`inference is None` |
| XLearner | **PASS** | **利用不可**：`inference is None` |
| DRIV | **PASS** | **FINITE** |

**判定上の重要点:** `fit/effect PASS`は`CI PASS`を意味しない。今回のDRLearnerはforestのfinal modelを使っており、その推論用の`prediction_stderr`が無い旨のWarningも出ている。S/T/X-Learnerは`inference=None`の設定であり、**この構成では区間が使えなかった**ことを意味する。Methodそのものに区間が存在しないと一般化しない。AriadneはMethod別`point estimate`と`interval availability`をResult／Scientific statusに分ける必要がある。

### 1.3. Tigramite（Phase3）

| Method | 初回結果 | 取得した形 |
|---|---|---|
| PCMCI | **PASS** | `graph`／`p_matrix`／`val_matrix`／`conf_matrix`、Graph形`[3,3,3]` |
| PCMCI+ | **PASS** | `graph`／`p_matrix`／`val_matrix`／`sepsets`／`ambiguous_triples`／`conf_matrix`、Graph形`[3,3,3]` |
| LPCMCI | **PASS** | `graph`／`p_matrix`／`val_matrix`、Graph形`[3,3,3]` |

3方式ともこの合成データではendpoint値として空文字と`-->`を取得した。**同時点の未確定方向やLPCMCIのcircle・bidirected endpointを保持できるかは、今回のfixtureでは試験していない。** Graphが出力されたことだけで既知真値との因果的正確性は保証されない。

## 2. 実際に解消した不確実性

- **解消（今回の条件下）:** Python 3.12＋Linux上に現行AriadneとDoWhy／EconML／Tigramiteを**個別でも同時でも依存衝突なく導入**できる証拠が得られた。
- **解消（API smoke範囲）:** DoWhy Backdoor/Frontdoor/IVの識別API、Backdoor推定API、EconMLの列挙8つのCATE fit/effect、TigramiteのPCMCI/PCMCI+/LPCMCI Graph出力が実行できた。
- **具体化された制限:** EconMLのDRLearner・S/T/X-Learnerの**今回の設定ではCIを取得できない**。Result側では`UNCERTAINTY_NOT_AVAILABLE`相当と、実際の計算失敗を区別すべき。
- **未解消:** 既存Ariadneテストの実行回帰、新規Known-truth数値精度／coverage、Frontdoor/IV estimator接続、潜在交絡endpoint fidelity、optional extrasの導入・独立import、完全`uv.lock`とManifestの実効version保存、SI納入GPLv3適合性。

## 3. 次の具体的な作業

| 追加検証 | 受入までに必要な成果 |
|---|---|
| `DEP-06`既存回帰 | 同時導入で既存Scientific Core/CLIと参照テストを実行。エラーがあれば原因と既存baselineとの差を切り分ける |
| `DEP-07`科学Benchmark | method別既知真値と負例、EconML CATE coverage、PCMCI lag0・latent/confounding端点、DoWhy非識別・弱IVを独立測定 |
| `DEP-08`配布可能なversion lock | 依存extrasごとに解決lockを固定、導入API/実効hashをManifestへ保存 |
| `SR-03`識別→推定契約 | DoWhy Frontdoor／IV識別と対応する数値Estimator、DRIV/CATE/IV/LATE・uncertaintyの互換性表 |
| `LEGAL-01`SIライセンス確認 | Tigramiteを含む顧客納入物のGPLv3適合性・提供形態・ソース義務を別途評価 |

**最終判定:** `SR-02 = OPEN（INSTALL_AND_API_SMOKE_PASS、SCIENCE／LOCK／REGRESSION／SI_LICENSE未解決）`。今回の結果をPhase1〜3の正式科学受入、Gate06/07 freeze、全体スコープ承認と取り違えない。試験Workflowは実行可能な技術証跡として保持する。
