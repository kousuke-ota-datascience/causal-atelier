# ENH-E11 — SR-02 外部Backend採用方針・PCMCI系利用場面の精査

**作成日:** 2026-11-01（日本時間）  
**文書区分:** `working_notes`／オーナー方針の記録と技術的精査。**正本FR/NFR/AR・Architecture Review・Gateの承認ではない**。  
**対象:** SR-02・SR-04・SR-08、00_04 P1-08／P2-02〜09・11／P3-01〜06、Issue #16／#18／#20／#24。  
**判断状態:** `A/B/C/D/E = OWNER_POLICY_ACCEPTED`、`D_USE_CASES_REVIEWED`、`SI_DELIVERY_PREMISE_RECORDED`、`GPL_COMPLIANCE_REVIEW_PENDING`、`VERSION_INSTALL_SCIENCE_VERIFICATION_PENDING`。  
**調査対象ブランチ・事前HEAD:** `prototype/ariadne_mvp`／`78c56c4bb0525125d7967bf7ea0e68b7f06c61ef`。**本メモ策定時点**では実環境への外部Backend install、fit、科学Benchmarkを実行していなかった。**後続追試：** [20261101_sr02_backend_runtime_probe_results.md](20261101_sr02_backend_runtime_probe_results.md)（Ubuntu／Python3.12でInstall/API smoke成功、Scientific Benchmark未実施）。

## 0. INTRODUCTION

### 0.1. 判断の前提と権限

2026-11-01の明示的なオーナー回答に基づく。**A／B／C／Eは方針として採用**した。**Dも『配布形態を踏まえてライセンス適合性を評価する』方針を採用**し、前提は**個別SIによる顧客環境への構築・納入（SaaSは現時点で想定しない）**とした。先行指示のPCMCI／PCMCI+／LPCMCIの利用場面の精査も§2〜3で行った。**Dの方針採用はGPLv3の配布適合性・ライセンス上の義務履行の承認ではない。**

「採用」を**バージョン固定・install成功・全Method実装承認・全体構想承認**と混同しない。Phase1〜3の必須Methodは実装の追跡対象として維持し、**個々の分析で全Methodを必ず実行すること**とは分ける。

### 0.2. 直接参照した一次根拠

- [Tigramite公式README／Method・CI-testの前提比較](https://github.com/jakobrunge/tigramite/blob/master/README.md)（PCMCI: no contemporaneous causal links/no hidden variables、PCMCIplus: no hidden variables、LPCMCI: latent confounders permitted、causal stationarity。GPLv3）。
- [Tigramite公式API documentation 5.2](https://jakobrunge.github.io/tigramite/)（PCMCI、`run_pcmciplus`、`run_lpcmci`、Temporal graph/CI result。LPCMCIの既定設定は**EXPERIMENTAL**との注意）。
- [Runge (2019), *Science Advances*, DOI:10.1126/sciadv.aau4996](https://doi.org/10.1126/sciadv.aau4996)（PCMCI、time lag）。
- [Runge (2020), *UAI / PMLR 124*, PCMCI+](https://proceedings.mlr.press/v124/runge20a.html)（contemporaneous＋lag、因果的十分性）。
- [Gerhardus & Runge (2020), *NeurIPS 33*, LPCMCI](https://papers.nips.cc/paper_files/paper/2020/hash/94e70705efae423efda1088614128d0b-Abstract.html)（潜在交絡を許すtime series PAG）。
- [GNU GPL FAQ: Internal Distribution](https://www.gnu.org/licenses/gpl-faq.en.html#InternalDistribution)、[GPL Require Source Posted Public](https://www.gnu.org/licenses/gpl-faq.en.html#GPLRequireSourcePostedPublic)。**ソフトウェアの利用可否を最終的に判断する法的意見ではない**。
- 現行`pyproject.toml`、`00_04_phase1_to_phase3_cli_scope_proposal.md`、`04_design_revision.md`、`working_notes/20261029_cli_scope_review.md`。

## 1. オーナー判断A〜Eと未確定事項

| ID | オーナーからの判断 | 計画への反映 | 依然として未確定 |
|---|---|---|---|
| **A 実行環境** | **採用：Python 3.12維持、Linuxを基準環境とする** | Python`>=3.12,<3.13`を維持し、まずLinuxで依存解決・smoke・science benchmark。その他OSは別support tierとして後日検証 | Linuxディストリビューション・CPU architecture・CI image・OS別の保証範囲 |
| **B optional依存** | **採用：DoWhy・EconML・Tigramiteを機能別optional依存に** | 本体への強制依存を避け、DoWhy識別、EconML CATE、Tigramite temporalを独立extras候補として設計。lazy import、利用不可のtyped result/error、version情報を記録 | extra名・各Backendの依存解決・同時install可否・実際の配布結合形態 |
| **C 必須手法** | **採用：Phase1〜3の列挙Methodを維持、実装不能のみ根拠付き再審議** | 00_04の68行・個別Methodの追跡を保持し、代替/除外を自動認定しない | 各Methodの実行可否、科学的同等代替の評価、最終採否 |
| **D Tigramite** | **採用：個別SIで顧客環境を構築・納入。SaaSは現時点で想定せず、納入・結合形態を確定してGPLv3適合性を評価**。PCMCI系3方式の用途も精査する | §2〜§4でMethod別適用条件とSI納入時のlicense gateを設計案化 | SI案件別の納入物、誰がpackageを取得・installするか、結合/改変範囲、提供するソース・ライセンス表示、適合判断（**未実施**） |
| **E version管理** | **採用：検証で選びlock＋科学Benchmark固定** | 候補組合せ→独立環境でinstall/API probes→Benchmark→version/lock/Manifestを固定する計画 | 確定version・依存hash・再現可能なLinux image・数値閾値 |

**現行の外部依存状態:** `pyproject.toml`はPython3.12を指定し、`pandas>=3.0.2`、`causal-learn`・`lingam`等の既存依存を含むが、DoWhy/EconML/Tigramiteのextrasは未登録。公開APIにMethodが載ることは、現行環境での正常動作の証明ではない。

## 2. PCMCI系を何のために使うか（Dの精査）

### 2.1. 科学的な用途・前提・成果物

| Method | 使用する状況（仮説・観測設計） | 要求する主要な因果仮定 | 正規化すべき結果 |
|---|---|---|---|
| **PCMCI**（P3-02） | 多変量・規則的時系列で、例えば`X[t−2]→Y[t]`等、**遅延関係**のみを探索。同時点の直接因果効果を研究デザイン上無視できる場合 | Causal Markov、Faithfulness、**causal stationarity、causal sufficiency（未観測共通原因なし）、同時点因果効果なし**。選んだCI-testの分布仮定 | lag付き有向辺とCI統計量・P値／補正・CI-test設定・選定lag・注意事項。実装設定`tau_min=0`等で未確定同時点関係が出る場合、**有向因果効果と誤読しない** |
| **PCMCI+**（P3-03） | 測定時間幅が粗い等の理由で**同時点の直接関係があり得る**。その時点内の構造とlag関係を両方探索したい | Causal Markov、Faithfulness、**causal stationarity、causal sufficiency**。同時点方向が確定しない場合を受け入れる | **Time-series CPDAG**：lag・同時点、向き確定／未確定、CI検定設定・非方向付け理由 |
| **LPCMCI**（P3-04） | 測定できない共通原因の存在が疑われ、**潜在交絡を除外できない**が、lag・同時点を含む因果的候補を調べたい | Causal Markov、Faithfulness、**causal stationarity**。Hidden confoundersを許容しても全非観測構造を一意に同定できるわけではない | **Time-series PAG**：endpoint（circle／arrowhead／tail等）、lag、可能な潜在交絡・不確定性を損失なく保持。潜在交絡「確定」と断言しない |

**補足:** これらは時間依存の**因果探索（graph discovery）**であり、グラフ中のCI-test statisticや関連強度をそのままATE/CATE等の介入効果と呼ばない。介入効果推定は別のIdentification／Estimator契約を要する。元データに対する前提が成立しなければGraphの因果解釈は保証しない。

### 2.2. 研究シナリオとMethod選択の例

| 例 | データ・問い | 第一候補と根拠 | 誤用例・注意 |
|---|---|---|---|
| 工場センサーの**遅延伝播** | 1分間隔の温度・圧力・流量。時間遅れの作用を調べる。同期時点の直接作用なし／主要共通原因観測済みを事前主張 | **PCMCI**。各変数のlag-parentとMCI統計量を評価 | 同時点作用や測定外の装置状態を排除できなければ因果主張は弱い |
| 観測頻度が粗い**同時点の関係** | 毎時の環境データ。観測間隔内で複数変数が互いに影響し得る | **PCMCI+**。contemporaneous edgeとlag edge、方向未確定を区別 | `same timestamp`だから実世界で同時に因果作用したとは限らない。測定解像度・平均化方法を記録 |
| 観測不能な外部状態を伴う**時系列探索** | 設備稼働の隠れた制御状態・気象要因等が複数の観測変数へ影響しうる | **LPCMCI**。潜在交絡を許容するtemporal PAGで不確実性を保持 | 現行5.2公式APIはLPCMCIの既定設定を**EXPERIMENTAL**と注意。実装採用には固有Benchmark・安定性検査が必要 |
| **regime shift / system intervention** | 介入後に方程式そのものが変わる、または時間と共に生成機構が変化 | **3方式とも無条件には適用しない**。定常性の再検討や対象区間の限定、別method検討 | LPCMCIはlatent confoundersを許すが**非定常性を自動的には解消しない** |
| **不規則時刻・欠測多発** | 不均一な観測間隔、間引きが大きいデータ | まず`TemporalDesign`の不適合・前処理の意味をレビュー。自動PCMCIはしない | 行番号を等間隔の時刻と偽装しない。正しい時間軸とlag意味が必要 |
| **横断データ** | 1時点だけの顧客属性と成果、time lagの意味がない | **3方式とも非適用**。Cross-sectional Discovery/Identificationを用いる | 特徴量を列順に並べるだけでは時系列にならない |

## 3. Method選択とEligibilityの案

### 3.1. 選択は「方法が存在するから」ではなく仮定を申告する

提案する`TemporalDesign`入力は、少なくとも`time_index`、`sampling_interval`、`variable metadata`、`lag_min/max`、`contemporaneous_links_assumption`、`latent_confounders_assumption`、`causal_stationarity_assumption`、`CI_test`とその分布・変数型に応じた適格性、`missingness/sampling policy`を持つ。

- `no contemporaneous causal links`と`no hidden common causes`を研究者が**根拠付きで仮定**できる場合：PCMCIが候補。仮定の存在と真実性は別。
- 同時点リンクがあり得ても`no hidden common causes`を主張できる場合：PCMCI+が候補。
- 潜在交絡が疑われる／除外できないと研究者が扱う場合：LPCMCIが候補。**LPCMCI自動採用でも因果解釈が自動保証されない**。
- `stationarity`が妥当でない、time indexが壊れている、CI-test前提に明確に反する：**無理にmethodを選ばず科学的なREQUIRES_REVIEW／NOT_APPLICABLE**を返す。

**「不可視の交絡がない」かどうかを観測データだけで自動証明できない。** このためAriadneは`method_requested`と`assumption_evidence`、`machine_check`を別項目で保存し、デフォルト選択の推奨が研究者の因果的判断を置換しないようにする。

### 3.2. CI-test・Graph・時間メタデータの最低契約

- `ParCorr`は**連続・線形・Gaussian noise前提**、GPDC系は非線形のadditive dependency、CMIknnはより一般の連続関係向けなど、**CI-testにも別の分布仮定・依存・性能**がある。Methodとの組合せを採用versionでprobeする。
- `time series graph`は`(source variable, target variable, lag, endpoint semantics, assumption status)`を保存。PCMCI+の**time-series CPDAG**とLPCMCIの**time-series PAG**を横断DAGへ黙って型変換・方向付けしない。
- 検定のP値・FDRと、実際の因果的確信は同一ではない。CI出力をATE/CATEに読み替えない。値の正規化は原Backend APIのshape・双方向表現・lag0のsemanticsを検証してから行う。
- 通常のPCMCI+・LPCMCIに対して**Time-series endpoint round trip**、候補Graphの既知真値、hidden confoundingとstrong autocorrelation、lag0、underpowered CI-testを分離したScientific Benchmarkを要する。

## 4. Dのライセンス判断を科学的用途と分離する

### 4.1. SI納入形態を踏まえたライセンス審査

**オーナーが明示した事業前提:** 個別SIによって顧客環境へ構築・納入する。**現時点でSaaSは想定しない**。TigramiteのGPLv3適合性を納入形態で判断する方針（D）は採用済み。

Tigramite公式README・setup.pyは**GPLv3（又は以降）**を示す。GNU FAQは**同じ組織内のコピー利用**と**別組織へのコピーの提供**を区別する。SIという契約名称は配布義務を決めない。**顧客へのインストール済み環境・wheel・Docker image・ソース等の引渡しは、組織外への提供に当たり得る**。現時点で「GPLに適合している」「Ariadneの全コードを公開する必要がある／ない」と断定しない。

| SIで想定する構築・納入 | ライセンス審査の着眼点 |
|---|---|
| 顧客環境へ**Tigramiteを含むDocker image・wheel・installerを納入** | GPL対象ソフトのコピー提供可能性が高い。著作権表示、ライセンス文、対応ソースの提供方法、改変、結合作品か独立作品かを事前審査 |
| SI担当者が顧客環境で**依存をインストールして納入** | 誰がTigramiteを取得／複製／提供したか、成果物の帰属と引渡し対象を確認。単にpip installだから配布ではないとは断定しない |
| **顧客が自己の管理で直接入手してinstall** | ベンダー自身のコピー配布とは異なり得るが、AriadneがTigramiteとどう連携するか、契約・結合形態を別途評価 |
| **SI会社内だけで検証**し、コピーを顧客へ渡さない | 組織内利用と外部納入を区別。研究・試験で使えたことは納入時のGPL適合判断ではない |

**結合形態の審査:** AriadneからPython import／同一プロセスでTigramiteを呼ぶ場合と、別プロセスで標準化ファイル等を交換する場合とで、対象成果物のライセンス評価が変わり得る。しかし**optional依存・外部プロセス化・顧客による自己インストールを自動免責策とみなさない**。実際に配布するソフトウェア・インターフェース・提供主体について法務／ライセンス担当の判断を要する。

**決定:** `D_OWNER_POLICY_ACCEPTED / SI_DELIVERY_PREMISE_RECORDED / LICENSE_COMPLIANCE_PENDING`。SaaSは当面の対象外だが、これによってSI納入時のGPLv3審査が不要になるわけではない。**顧客環境への最初の納入・提供前**に案件別の確認と承認をGateとする。

### 4.2. 各Methodと配布判断の関係

**PCMCI/PCMCI+/LPCMCIの科学的使い分けに、GPLv3の違いはない。** 3手法とも同じTigramite配布物を利用するため、どれか一つだけを使えばGPL問題が自動解消するということではない。必要に応じてTigramiteを使わない技術案の評価もできるが、**科学的に同等であると評価するまではPhase3の対象Methodを削除しない**。

## 5. SR-02を閉鎖するための技術検証計画

### 5.1. 実行環境・依存probe（今後のWork Package候補）

| 検査ID | 技術作業 | 出力・成功条件 |
|---|---|---|
| `DEP-01` | Python 3.12・Linux基準環境の配布版、CPU、Python/NumPy/pandasを固定 | Baseline/OS image、`pip/uv`等の解決器、依存環境の同一性 |
| `DEP-02` | DoWhy/EconML/Tigramiteの**独立optional extra**と全組合せを依存解決 | インストール可能・不可能の両結果（依存conflict・解決版を含む） |
| `DEP-03` | DoWhy Backdoor／Frontdoor／IVの識別API・結果・負結果をprobe | Class/Signature、識別のみと推定可能状態を区別したprobe report |
| `DEP-04` | EconMLの**Phase2列挙8方式**を個別にfit/effect/interval probe | Method別treatment型、fit、CATE、CI availabilityのmatrix |
| `DEP-05` | PCMCI、PCMCI+、LPCMCIを**Method×CI-test**でprobe | 各methodのgraph/lag/endpoint/統計量/negative statusの可用性 |
| `DEP-06` | 既存causal-learn/LiNGAM/Scientific CLIを回帰 | Optional導入による既存機能の破壊なし |
| `DEP-07` | 同一generator・既知Graphを複数seedでBenchmark | Lag precision/recall、誤陽性、endpoint fidelity、潜在交絡、強い自己相関、runtimeを測定 |
| `DEP-08` | 採用実効version・lock・package hash・Manifestを固定 | 科学Benchmark・Gateが同じ環境で再現可能（閾値・試験seedは承認後に設定） |
| `LEGAL-01` | 内部利用／配布形態・GPLv3の結合と配布条件を法務・ライセンス担当へ確認 | **配布前**の適合判断の記録。科学的Benchmarkだけでは閉鎖しない |

`DEP-02〜08`と`LEGAL-01`は**未実施**。現時点で「最新版で動作」「Python 3.12適合」「Tigramite配布可」「LPCMCIで潜在交絡を見抜ける」などとは宣言しない。

## 6. 01/02・Architecture Reviewに残す判定

| Decision | 現在の状態 | 次の確定先 |
|---|---|---|
| A Python 3.12＋Linux baseline | **方針採用** | Architecture ReviewでLinux image／具体OSを固定 |
| B 独立optional依存 | **方針採用** | 03/04にextra/registry契約、実装でinstall試験 |
| C Phase1〜3手法維持 | **方針採用** | 00_04全68行保持、Method不能時にオーナー差戻し |
| D PCMCI系のMethod使用場面 | **精査済み（本メモ）／Method選択契約案** | 03/04でTemporalDesign・CI-Test・Graph、#20で科学検証 |
| D 個別SI（SaaS非想定）／GPLv3 | **配布前に適合性評価する方針は採用済み。具体納入のGPLv3適合判断は未承認** | 案件別納入物・インストール主体・連携/改変範囲・ライセンス表示・対応ソース等を確定し、納入前に法務審査 |
| E Version lock＋Benchmark | **方針採用** | DEP-01〜08の証拠からGate 06/07へ固定 |

**SR-02の扱い：** オーナー方針は受領し、PCMCI系の利用場面は分類した。しかし**install/API/SCIENCEとSI納入に即したGPL適合性評価が未実施のため、SR-02はOPEN**。正式な02の全体構想承認やGate freezeを意味しない。
