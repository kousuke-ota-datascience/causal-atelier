# ENH-E11 — 構想・要件改定計画（案）

**文書区分:** Workflow所定の構想・要件改定計画（01）  
**状態:** DRAFT／対象範囲の方向性を検討中／構想・要件・設計・Gateは正式未承認  
**起案日:** 2026-10-24（日本時間）／**改訂日:** 2026-10-25（日本時間）  
**追跡Issue:** [#13（ENH-E11全体）](https://github.com/kousuke-ota-datascience/causal-atelier/issues/13)、[#14（事前照合とArchitecture Review）](https://github.com/kousuke-ota-datascience/causal-atelier/issues/14)  
**実装現状の参照SHA:** `827a6c3683e0fff0af342cb3aded45d9dde020c9`。**正式な受入Baselineではない。**

## 0. INTRODUCTION

### 0.1. 本文書の目的

本書が答えるべき問いは、**「Ariadneの現在の因果探索・因果推論では、どのような分析条件に対応できないのか」「それを補完するため、なぜ各機能を選ぶのか」「何が検証できればENH-E11を完了とするのか」**である。手法の名称や過去のEnhancementの経緯を羅列すること自体は目的ではない。

本書は、現行実装を踏まえた**機能追加の必要性、選定根拠、完了条件、要件・設計改定方針**を定義する構想案である。新規実装の対象はScientific Core・ローカルCLI・永続ローカルファイル成果物に限定する方針を採用し、承認後の要件・Gate契約へ引き渡す。

### 0.2. 先行資料との役割分担と重複排除

現行正本・コード・テストの逐次照合は、先行する次の**二つの00資料を根拠資料**とし、本書へ全文を再掲しない。

| 先行資料 | 記録する事実・責務 | 本書に引き継ぐ内容 |
|---|---|---|
| [00_foundation_gap_reconciliation.md](00_foundation_gap_reconciliation.md) | 9月末構想13項目と現行FR/NFR/AR・コード・テスト・過去999の対応。P0/P1等は**追加調査の優先順位** | 実装済み能力と新Capability候補の境界 |
| [00_foundation_gap_closure_assessment.md](00_foundation_gap_closure_assessment.md) | 現行要件の未解消4領域（GAP-C01〜C04）の証拠水準、残差、閉鎖条件、実装帰属の留保 | 未充足の要件群と未解消の判断事項 |

本書の第1章は**利用者・分析上の課題とFoundation Gapの関係**、第2章は**追加手法の選定理由**、第3章は**現行能力と完了判定の基準**を記す。8月4日のPhase 1〜3案と9月末のENH-E11申し送りは選定の来歴として第12章に記録し、現行要件や実装事実の代わりにしない。

### 0.3. 構想段階の結論

AriadneにはPCを含む複数の因果探索法、Graph、Randomized/Backdoorの識別、ATE/ATT・IPW/AIPWおよび既存Diagnosticsがある。しかし、**探索グラフの推定だけでは効果の識別・推定が保証されず、潜在交絡、処置効果の異質性、時間依存、準実験という条件を現行の方法契約では十分に扱えない**。この不足を、因果推論の問い・仮定・識別・推定・診断・反証の単位で補完する。

一方、既存正本のFoundation Gap4領域は別の問題である。**それらが未解消だからDoWhy・FCI・EconML等を導入する、という因果関係ではない**。要件未充足の解消と新しい科学的Capabilityの導入を分離し、どちらをENH-E11で実施するかは第5章・第11章の承認手続で決める。

## 1. 解決すべき問題と経緯

### 1.1. 分析者が直面する問題

現行のPCによる探索は観測変数間の条件付き独立性から**CPDAG（因果方向が一意に確定しない場合があるグラフ）**を推定する。探索結果は仮説形成に有用だが、次の分析ニーズでは十分な回答にならない。

1. **潜在交絡・方向の不確定性がある:** 観測されていない共通原因があり得るとき、PCが要求する因果的充足性を前提にしたGraphを無条件に確定DAGとして採用できない。
2. **「構造を知る」と「介入の効果を知る」は別:** 有向edgeの候補だけでは処置効果のestimand、識別可能性、調整集合、推定誤差や不確実性を確定できない。観測データでBackdoorが成立しない状況もある。
3. **平均効果だけでは回答できない:** 対象集団全体のATE/ATTが推定できても、個人属性・集団条件による効果の異質性（CATE/HTE）は分からない。
4. **時間的依存と介入タイミングが重要:** 自己相関、lag、同時点依存、パネル構造を無視した横断的なGraph探索だけでは、時系列因果関係や介入前後の評価に十分対応できない。
5. **自然実験・制度的割当が分析の入口となる:** 介入が政策導入時期、閾値、instrument、donor候補で決まる場合、PCや一般的Backdoor推定を適用するより、デザイン固有の仮定を明示したDiD・RDD・IV・Synthetic Control等が適切なことがある。
6. **数値推定の健全性を判断したい:** IPTWのoverlap/極端重み、Refutation、Sensitivity、信頼区間の被覆等を確かめられなければ、得られた効果を意思決定根拠として監査しにくい。

**制限:** これは「PCを使用できる状況が必ず少ない」という一般的な性能評価ではない。PCに適したデータと仮定の下では引き続き有用である。必要なのは**PCを置換することではなく、条件の異なる分析を適切な手法へ接続すること**である。

### 1.2. 現行Ariadne固有の制約

現行DiscoveryはPC**のみではなく**GES／LiNGAM／NOTEARSも提供する。ただし、その追加は上記1.1の識別・推定・デザイン要件を自動的に満たさない。

| 現行の能力 | ソース上の確認事項 | 対応できない／慎重な扱いが必要な範囲 |
|---|---|---|
| 因果探索 | `scientific/discovery/adapter.py`にPC・GES・LiNGAM・NOTEARSの登録がある | FCIによる潜在交絡下のPAG探索、PCMCI系による時系列lag探索は未登録 |
| Graphと識別 | DAG/CPDAG/PAGを保持し、CPDAG/PAGは曖昧なままreviewとする。識別戦略はRandomized／Backdoor | front-door、IV等の識別契約は存在せず、PAGをDAGへ変換して推定してはならない |
| 平均効果の推定 | Diff／OLS／IPW／AIPWによるATE/ATT | CATE/HTE、LATE、RDD局所効果、準実験の手法別estimandは未提供 |
| 科学的診断 | 既存のoverlap、balance、ESS、Placebo/Subset Refutation、Adjustment Set/Clipping Sensitivity | CATE固有のsupport/calibration、時間・制度デザイン固有の仮定検査等は未提供 |
| 実行経路 | Scientific CoreとDB非依存CLI、既存Product API/Worker/DBの経路がある | 新手法のlocal spec・optional依存・実効version・成果物契約は別途必要 |

詳細な既存機能の証拠は00の二資料に委ねる。ここでいう「未提供」は**当該手法の現行CLI/Scientific契約にない**という意味であり、既存実装全体に因果機能がないという意味ではない。

### 1.3. 問題を放置した場合

現行手法の適用範囲を超えた分析を同じ画面・CLIから強引に実行すると、非識別なのに推定値だけが出る、潜在交絡を無視した方向を確定する、処置効果の異質性を予測subgroup指標と混同する、時間順序・並行トレンド・weak-IV等の条件を見落とす、といった誤解が起きる。

したがってENH-E11で目指すのは**実装手法の数の増加ではなく、データ・仮定・estimandに適した分析可能範囲の拡大と、適用不可を安全に表示する能力**である。

### 1.4. 既存Foundation Gap（①〜④）と要件・調査優先度の対応

「Foundation Gap」は、**現行正本のFR/NFR/ARが要求するのに充足し切っていない部分**を指す。PCを補完する追加手法そのもの（DoWhy・FCI・CATE等）は新Capability候補であり、同じGap番号に含めない。

| 既存Gap | 先行00照合での優先度 | 関連する現行要件と実装状態 | 何が残っているか | 本構想における取扱い |
|---|---|---|---|---|
| **① GAP-C01：探索データ再利用警告** | **P0** | FR-051、AR-004：**PARTIAL** | 明示的handoffは動作。先行Exploratory Resultを用いた同一Datasetのconfirmatory分析について、適用経路全体の警告とevidence保持が未立証 | 調査・現行要件Gapとして維持。Productの修正をCLI-onlyの実装へ自動追加しない |
| **② GAP-C02：Canonical Lineage** | **P0** | FR-008/054/095、NFR-002：**PARTIAL** | Context→Spec→Plan→Stage→Result→Artifactの完全な正規lineageが未充足 | 調査・設計上のGap。DB lineageをCLI Manifestで代替したと扱わない |
| **③ GAP-C03：再現性・Provenance** | **P1** | FR-086a/087b、NFR-001b：**PARTIAL** | Scientific Library実効versionの網羅性不足。StageAttempt seed/retryの全経路は未立証 | E11のlocal CLIには必要なversion/seedを独立に要求。既存Product側の残差は別判断 |
| **④ GAP-C04：Capability所有権** | **P1** | FR-132/133/144：**PARTIAL**、FR-145/NFR-023：**NOT_IMPLEMENTED** | Family固有の具体Navigation Stage catalogをgeneric applicationが集中所有 | 全Family横断のArchitecture Gap。CLI科学手法の実装前提とは断定せず、所管を別途判断 |

**優先度の意味:** P0/P1は[00_foundation_gap_reconciliation.md](00_foundation_gap_reconciliation.md)第5章の**追加調査・閉鎖確認の優先順位**であって、「ENH-E11で必ずP0から実装する」という実装優先度ではない。第2調査[00_foundation_gap_closure_assessment.md](00_foundation_gap_closure_assessment.md)は各Gapの証拠水準・閉鎖条件を詳述する。なお現行正本にはこのほかにもPARTIAL/NOT_IMPLEMENTEDがあるため、**上表は全リポジトリの未実装要件の網羅一覧ではない**。

## 2. 実施する理由

### 2.1. 手法を追加する必要性と選定根拠

採用候補を「歴史資料に書かれていたから」ではなく、**既存の分析制約→必要な科学的契約→対応する方法**で選ぶ。複数手法は相互の代替とは限らず、データ構造・識別仮定により適用対象が異なる。

| 対応したい分析条件・問い | 選定した機能・手法群 | 選定理由と成立条件 | 防ぎたい誤用 |
|---|---|---|---|
| 未観測共通原因が疑われ、PCの因果的充足性を置けない | **FCI／PAG** | 潜在交絡の可能性を許す探索で、未確定endpoint・方向・warningを表現するため。FCIも正しいDAGや効果を無条件に確定しない | PAGをDAGへ強制変換すること |
| DAG/Designの仮定から効果を識別できるかを判定したい | **DoWhy等のoptional Identification、Backdoor／Frontdoor／IV** | 既存Native Backdoorを残したうえで、識別戦略ごとの仮定・式・非識別理由を扱う。DoWhyは識別・反証の支援手段であり仮定の真偽を保証しない | 単なるedge推定を処置効果と扱うこと |
| 観測データで平均効果を推定したが、推論や仮定の脆弱性が気になる | **既存IPTW/AIPWの品質検証、追加Refutation・Sensitivity** | 既存重みとE9 Diagnosticsを再利用し、estimated propensityを含むSE/CI、極端重み、摂動への安定性を検証する。方式追加は要件変更による | Hájek正規化とstabilized weightsの混同、診断なしの数値成功 |
| 介入効果が属性・条件によって異なる | **EconML、DML／Causal Forest／DR／Meta-learnerによるCATE/HTE** | 高次元・非線形な交絡調整や効果異質性を扱うため。交絡が十分に観測される等の識別条件、positivity、適切なsplit/cross-fittingが必要 | Predictiveのsubgroup metricを因果CATEと扱うこと |
| 観測対象が時間軸上で依存し、過去から現在への因果構造を知りたい | **Tigramite、PCMCI／PCMCI+／LPCMCI** | lag、自己相関、同時点依存、潜在交絡等の違いを表現・診断するため。手法ごとのstationarity等の仮定を明示する | 横断PCの結果を時系列因果Graphとみなすこと |
| 介入時期・処置群と比較群の差分を利用する | **DiD／Event Study／Interrupted Time Series** | 実施時点や群構造を直接利用し、並行トレンド、staggered adoption、時系列依存を手法別に検証するため | 単純前後差を因果効果と無条件に呼ぶこと |
| 閾値による割当や有効なInstrumentがある | **Sharp/Fuzzy RDD、IV／LATE** | 局所的な不連続性・外生変動を識別に利用し、bandwidth、manipulation、first-stage、exclusion等を点検するため | RDD局所効果やLATEを母集団ATEと同一視すること |
| 対照群が単純に定義できず、介入前の複数donor系列を用いる | **Synthetic Control／Synthetic DiD** | donorの選定とpre-treatment fitに基づいて反事実系列を構成し、placeboやsupportで検証するため | 合成対照の重みをIPTWの処置重みと同一視すること |

**選定は条件付きである。** たとえばIVは妥当なinstrumentがなければ解決策にならず、FCIの出力は識別不能のままかもしれない。各手法について「どの問い・データ・仮定を満たせば実行可能か」と、実行不能時の科学的結果を一対で定義する。

### 2.2. 選定・採用を決める判断基準

- **必要性:** 現行PC/GES/LiNGAM/NOTEARS＋Native Randomized/Backdoor＋ATE/ATTでは満たせない問いが具体化できること。
- **識別と妥当性:** 効果・Graphの解釈、仮定、negative result、diagnosticsをtestableに定義できること。数値を返せるだけでは採用しない。
- **方法と環境の適合:** Libraryの現在利用可能なversion/API、optional dependency、入力データ要件、実行コストを確認できること。
- **重複の排除:** 既存のGraph semantics、E9 Diagnostics、IPW/AIPW、Manifestを先に再利用し、同等の新実装を重複して作らないこと。
- **受入可能性:** 既知真値／不成立条件を持つBenchmarkと、適用できない場合の再現可能な検証が可能なこと。
- **後方互換性:** 既存のProduct API/Worker/DB/UIおよび現行CLI利用者に副作用を与えず追加できること。

ライブラリ別の必須手法一覧と「利用可能な版に実装がない場合の同等代替」は、本構想だけで黙示的に決めない。承認済みの03要件改定とGate 06/07で固定する。

### 2.3. 既存Enhancementの成果を踏まえても必要な理由

ENH-E7/E8はProject・Navigation・Scientific Stageの責務分離を、E9は適用可能なWeight/Balance/Overlap/ESS診断を、E10はPredictive向けのoptional依存分離を前進させた。これらは**再利用できる土台**であって、未観測交絡下のDiscovery、CATE推定、Temporal Discovery、準実験のestimandと固有診断を代替するものではない。

ゆえにENH-E11の必要性は「過去Enhancementを完了させるため」ではなく、**既存基盤上で扱える因果分析の条件を拡張し、問いに適した方法・仮定・限界を一貫して管理するため**にある。E7〜E10の受入範囲を尊重しつつ、未実装手法の成果をそのPASSで保証しない。

### 2.4. 今回CLI-firstで実施する理由

最初からWeb UI/API/Worker/DBまで新規統合すると、方法の科学的妥当性の検証とProduct全経路の結合作業が混ざり、失敗の原因を切り分けにくい。そこで、**Scientific Core＋DB不要のローカルCLI＋再現可能な永続ファイル**を新Capabilityの受入境界とする。既知真値・負例・方法固有の診断をこの境界で検証した後に、Product統合を別のEnhancementで判断する。

これにより、現行ProductのFoundation Gap①②④が解消されるわけではない。既存Product側のGapと新規CLI側の品質要件は、閉鎖条件とIssueの帰属を分ける。

## 3. 現状と基準

### 3.1. 現行実装の基準と実際にできること

**コード参照:** `prototype/ariadne_mvp`、`827a6c3683e0fff0af342cb3aded45d9dde020c9`（当初の計画・調査文書を含む参照SHA）。**要件Statusの訂正**は`84c5a624389b233fcb97c656f1c94d177f459c5a`を継承する。これは**調査用Snapshotであり、ENH-E11の実装・受入をfreezeしたBaseline SHAではない**。

| 現行実装で可能なこと | 具体的な入口・表現 | 実行・検証済みと断定しない範囲 |
|---|---|---|
| PC/GES/LiNGAM/NOTEARSによるDiscovery | `scientific/discovery/adapter.py`のregistryとGraph JSON | FCI・PCMCI系のDiscovery、潜在交絡下の効果識別 |
| DAG/CPDAG/PAGの保持 | `product/domain/graph_semantics.py`、graph/version関係 | FCI等が出力するPAGの全固有metadata |
| Causal Question/Design、Randomized/BackdoorのIdentificationとData Eligibility | `product/domain/analysis_spec.py`、`scientific/identification/adapter.py`、Result status | Frontdoor/IV、CATE/時系列/準実験用Design |
| ATE/ATTのDiff/OLS/IPW/AIPW、診断と区間 | `scientific/inference/adapter.py`、E9のweight/overlap/ESS | CATE・LATE・RDDのestimand、IPTWの全推論方式と被覆率の認定 |
| Placebo/SubSet RefutationとAdjustment/Clipping Sensitivity | 既存Scientific Adapter群 | 追加方式、未観測交絡Sensitivityの一般的保証 |
| Scientific CLIとローカルManifest | `interfaces/cli/config_schema.py`、`scientific_stage.py`等。既存`config_version=2.0` | 新手法の実効Library version・完全なseed/split・個票CATE/temporal file |
| Product実行・Result/Artifact・Navigation | 現行Product API/Worker/DBとNavigation catalog | [00残差確定](00_foundation_gap_closure_assessment.md)の4領域。新手法のProduct全経路統合 |

**証拠上の制限:** 以上は現行ソースと先行00調査の既存テスト・過去受入記録に基づく。**このSHAでの全件再実行は行っていない**。したがって現行機能の網羅的な科学的最終認定ではない。

### 3.2. ENH-E11で到達したい状態と現状との差分

| 分析上の要求 | 現状 | 必要な到達状態 |
|---|---|---|
| 潜在交絡の可能性を考慮した探索 | CPDAG/DAGを生成する探索法はあるがFCIはない | FCIでPAG・未確定endpoint・潜在交絡warningを保存し、非識別を許容する |
| Backdoor以外の識別と反証 | Randomized/Backdoor、既存2種のRefutationと2種のSensitivity | 承認されたFrontdoor/IV、追加Refutation/Sensitivityを入力・仮定・負結果付きで利用する |
| 効果の異質性 | ATE/ATT中心 | CATE/HTEを第一級EstimandとしてEconML等の対応推定器・診断で推定する |
| 時系列依存 | 一般の横断Graph | Lag/同時点/CI-test等を明示するPCMCI系・TemporalDesign |
| 準実験条件 | 専用Design・Estimatorなし | DiD/Event/ITS、RDD、IV/LATE、Synthetic系を各仮定と固有診断付きで提供する |
| 利用・監査 | 既存CLI/Manifestと一部のProduct lineage | E11新手法のCLI-only再現性を固定し、既存Productの未解消Gapは別に追跡する |

### 3.3. 完了判定の基準（構想段階のAcceptance Claims）

| 仮ID | ENH-E11の完了時に証明すべき状態 | 検証可能な証拠・不成立条件 |
|---|---|---|
| **E11-AC-01：Coverage** | 正式承認されたPhase 1〜3の**必須機能ごと**に、既存再利用／追加実装／承認済み代替／明示的対象外の処遇があり、必要なものをCLIで実行できる | Requirement→Design→Issue→Gate→Test対応表。手法名が並ぶだけでは不足。未承認の省略は不可 |
| **E11-AC-02：Identification/Graph** | GraphとDesignの仮定を保存し、FCI/PAG等の不確定性を失わず、識別できない場合は数値効果を無理に返さない | 既知DAG/PAG、潜在交絡、Backdoor/Frontdoor/IV、非識別・endpoint未確定のpositive/negative試験 |
| **E11-AC-03：ATE/ATT/IPTW** | 既存IPW/AIPWを再利用し、正規化重み、推論、overlap・balance・ESS、Refutation/Sensitivityの意味を検証する | 既知真値bias・SE/CI coverage・極端重み・poor overlap・seed再実行とE9回帰 |
| **E11-AC-04：CATE/HTE** | CATEと平均効果を分け、承認済みのDML/DR/Causal Forest/Meta/IV+ML手法で支持集合・不確実性を説明できる | 効果異質性の既知真値、条件不成立、cross-fitting、個票出力のprivacy、interval/calibration試験 |
| **E11-AC-05：Temporal** | PCMCI系がlag、同時点関係、Graph uncertaintyを保持し、入力時系列の仮定を検査する | 既知lagと独立系列、time index欠損・重複、autocorrelation、CI検定不適合等の試験 |
| **E11-AC-06：Quasi-experimental** | DiD/Event Study/ITS、RDD、IV/LATE、Synthetic系が方法固有estimand・仮定・negative resultを保持する | 並行トレンド違反、staggered adoption、cutoff操作、weak-IV、不良donor等の成功/失敗fixture |
| **E11-AC-07：CLI/Reproducibility** | 承認済み全手法が新規DB/Web依存なしで動き、入力・設定・乱数・実効版・結果・checksumをローカル成果物から追跡できる | 有無双方のoptional backend、固定seed再実行、Manifest schema、artifact read-back、部分失敗、秘匿情報の保護 |
| **E11-AC-08：Compatibility/Acceptance** | 既存のScientific CLIとProductの受入済み契約を保護し、新しい手法は独立した科学的受入を得る | 既存CLI契約・E9 Diagnostics回帰、承認済みRequirement/Design、Gate 06/07、独立30検証とcanonical 999判定 |

**測定値のfreezeが必要:** Scientific Benchmarkのデータ生成機構、真値との許容誤差、CI被覆率・安定性の閾値、時間系列と準実験の診断許容値、対象Library version/platformは未確定である。**これらをGate 07に数値・fixture・methodの単位で明記し、独立検証でPASSしなければ「完了」と判定しない。** 単なるimport/endpoint成功は科学的受入に不十分。

### 3.4. 既存Foundation Gapの閉鎖とENH-E11の完了の関係

第1.4節の**GAP-C01〜C04は現行正本に対する未解消の登録簿**であり、新規Capabilityの完成条件と同一ではない。CLI-onlyのENH-E11で①②④を修正しない場合も、現行要件を満たしたかのようにImplementation Statusを`IMPLEMENTED`へ変更してはならない。

ENH-E11の正式スコープを承認する際、各Gapにつき**(a)ENH-E11内で閉鎖する、(b)別Issue/別Enhancementに移管する、(c)承認済み要件変更により期待値を改訂する**のいずれかを、責任者・理由・参照Issueとともに決定する。**P0/P1はこの実装帰属やGateの優先度を決めるものではない。** ③の新規CLIへの実効version・seed要件はE11-AC-07に必須とし、既存Product側のFR-086a/087b/NFR-001bが自動的に解消されたとは扱わない。

### 3.5. 基準の権限と凍結順序

調査SHAは現状確認の証拠であり、**完了条件の権限は正式承認された要件・設計とGate 06/07**にある。①第3.3節の基準を構想審査、②対応する新FR/NFR/ARと手法仕様を承認、③Architecture Reviewで所有権・依存・Local file schemaを決定、④固定SHA・Benchmark・閾値・Gateをfreeze、⑤実装・独立検証・canonical 999 PASSの順序を守る。

## 4. 目標状態

Ariadneの利用者は、**分析対象のデータ構造・識別仮定・効果の問い**に応じて、PC等のGraph探索、潜在交絡を考慮した探索、観察研究の識別、平均/異質効果、時系列・準実験から適切な方法を選べる。方法が成立しない場合にも非識別・要レビュー・不適格を正しい科学的Resultとして受け取る。

その結果はCLIによる再実行と永続ファイルで監査でき、既存のATE/ATTやE9 Diagnosticsは壊れない。**目標の達成判定は第3.3節のE11-AC-01〜08に集約**し、本章に同じ受入条件を重複記載しない。

## 5. 対象範囲

### 5.1. 対象候補

- **Phase 1：** 既存Question/Design/Graph/Identification/Eligibilityの再利用、FCI/PAG、DoWhy等のoptional識別（Backdoor/Frontdoor/IV）、追加Refutation/Sensitivity、IPTW/AIPWの推論・診断の品質強化。
- **Phase 2：** CATE/HTE、EconMLのLinearDML／CausalForestDML／DRLearner／ForestDRLearner／S・T・X Learner／DRIV又は科学的に同等なIV+ML、support/overlap/calibration/uncertainty、永続ファイル成果物。
- **Phase 3：** TigramiteのPCMCI／PCMCI+／LPCMCI、CI-test registry、TemporalDesign、DiD、Event Study、Interrupted Time Series、Sharp/Fuzzy RDD、IV/LATE、Synthetic Control／Synthetic DiDと各固有診断。
- **横断：** CLI契約、データ・結果の版管理、local Manifest/Checksum/Seed/Library version、negative result、Known-truth Benchmark、後方互換性。
- **既存Gap：** GAP-C01〜C04の**帰属判断を行う**。何を実装するかは第3.4節の個別決定による。全件が自動的に実装対象になるものではない。

上記はオーナーの方針を反映した**構想段階の候補**であり、正式なFR/NFR/ARとGate 06/07の承認を待つ。手法ごとの科学的選定理由は第2.1節を正とし、ここには名称・提供境界のみを置く。

### 5.2. 対象外・後続送り

- E11**新機能**のWeb UI、Web API、Worker、DBへの新規統合、科学的受入のためだけのBrowser E2E追加。
- Phase 4のPolicy Evaluation、capacity/cost最適化、監視/drift、意思決定の自動執行。
- 初期必須範囲外のRPCMCI/J-PCMCI+や、すべての外部分析Libraryを網羅すること。
- [Issue #11](https://github.com/kousuke-ota-datascience/causal-atelier/issues/11)のリポジトリ全体のテスト基盤移行。
- 既存ProductのNavigation/DB要件残差を、オーナー承認なしにCLI実装作業へ取り込むこと。

## 6. 要件改定の見込み

- 既存FR-035〜050・FR-153〜156の実装済み契約は維持する。**FR-051・FR-054等の現行PARTIAL/NOT_IMPLEMENTEDを、新Capabilityの追加だけで解消としない**。詳細は00の2資料に委ねる。
- FCI/DoWhy、CATE/HTE、Temporal/Quasi-experimental Design、追加Refutation/Sensitivity、Local CLI artifactを独立した意味の新FRにする。各手法に適格性、識別・推定対象、科学的負結果、provenanceを定義する。
- FR-086a/087b、NFR-001b/002/025/028等の既存再現性・追跡・依存分離要件を新手法へ適用する一方、既存Productへの適用とlocal CLIへの適用を区別する。
- 現行要件§11の未承認DoWhy/EconML除外規定は、正式採用に必要な範囲だけ承認を得て改定する。Tigramiteその他も同じ採否判断をする。
- 新FR/NFR/ARの正式採番は承認後に実施する。`03_requirements_revision.md`は現時点で**semantic deltaの案**であり、正本更新済みではない。

## 7. 設計改定の見込み

- Domainに外部Library型を持ち込まず、Scientific Coreのoptional Adapterが手法別入力・仮定・Resultを正規化する。Native推定器を不要に置き換えない。
- PAGの方向不確定性、CATEの条件付きestimand、Temporal lag、準実験のDesign固有仮定を保持する。全手法を横断的ATE/ATTへ丸め込まない。
- Local spec・Manifest・Artifactの版と内容hash、atomicな保存、秘匿情報の保護を設計し、DBのcanonical lineageとは区別する。
- 既存Product API/Worker/DB/UIと`causal-analysis-spec/2`を暗黙に変更しない。Schema移行が必要ならArchitecture Reviewと承認付き差分で扱う。

## 8. 主なリスクと互換性

- **科学的誤認:** PCの前提、FCI/PAGの不確定性、Frontdoor/IVの仮定、CATEのpositivity、Temporalの自己相関、DiDの並行トレンド、weak-IV、局所効果の外挿を誤らない。
- **品質と再現性:** IPTWの分散・区間推定、少数サンプル、極端な重み、Library version・seed・splitを仕様に固定できるか。
- **依存環境:** DoWhy/EconML/Tigramiteのoptional install、version/platform互換性。欠落時に無関係な機能を停止しない。
- **後方互換:** 既存CLI引数、Graph・Manifest reader、ProductのE9 Diagnostics、E7/E8の実行とNavigationを保護する。
- **スコープ混同:** Product側GAP-C01〜C04と新規CLI-only機能を一つのGate PASSで閉鎖したと扱わない。
- **成果物と機密性:** 個票CATE・donor panel・入力の不用意な保存、pickle/任意import、部分的file書込みを防ぐ。

## 9. Architecture Reviewの要否

**必須・未完了。** 独立したCausal/Temporal/Quasi-experimental Design、estimand、Graph endpoint/lag、optional backend、local file identity、manifest、結果のauthorityを決定する必要がある。現行ProductのNavigation/DB所有権Gapの帰属判断も記録する。

承認前の設計・Gate案は`04_design_revision.md`および`40_operator_workflows/architecture_review/`で管理する。

## 10. 暫定Gate構成（承認前）

| Gate案 | 主な受入境界（第3.3節E11-ACとの関係） | 対応Issue |
|---|---|---|
| G01 | Local causal context、FCI/PAGの不確定性（AC-02/07） | #15、#17 |
| G02 | Identification/Eligibility、optional backend（AC-02/07） | #15、#16 |
| G03 | IPTW/AIPW、Refutation/Sensitivity（AC-03） | #16、#19 |
| G04 | CATE/HTE estimandとEconML推定器（AC-04） | #18 |
| G05 | CATE診断・privacy配慮済みファイル（AC-04/07） | #18、#24 |
| G06 | Temporal Graph・PCMCI系（AC-05） | #20 |
| G07 | DiD/Event Study/ITS（AC-06） | #21 |
| G08 | RDD/IV/LATE（AC-06） | #22 |
| G09 | Synthetic Control/SDID（AC-06） | #23 |
| G10 | Manifest、再現性、既存回帰・科学検証（AC-07/08） | #24 |

**Gate数・順序は未確定**であり、Architecture Reviewで意味上の受入単位に統合・分割する。Issueは作業追跡、Work Packageは実装作業単位、Gate 06/07は受入契約であって相互に代替しない。第3.3節のAC番号も仮番号である。

## 11. 実装前に必要な承認

- PC中心の既存能力を補完するための**分析条件・適用範囲・手法の採否**と、Phase 1〜3をE11のCLI-onlyで提供する構想の正式承認。
- 現行Foundation GAP-C01〜C04の各閉鎖または移管の決定。実装優先順位と調査優先度P0/P1を混同しない。
- 正本§11の外部engine取扱い、新FR/NFR/AR、Design/Result権威、optional version、local file/privacy contractの承認。
- Benchmark fixture・科学的閾値・適格性・負結果・互換性の固定、Architecture Review、正式Gate 06/07のfreeze。
- 実装後は独立検証とcanonical 999 PASS。**本書やIssueの更新は承認・受入に代わらない**。

## 12. 出典・補足資料

- **9月末構想と現行実装の照合:** [00_foundation_gap_reconciliation.md](00_foundation_gap_reconciliation.md)。13項目とP0/P1の調査優先度。
- **未解消Gapの確定:** [00_foundation_gap_closure_assessment.md](00_foundation_gap_closure_assessment.md)。GAP-C01〜C04、関連FR/NFR/ARと閉鎖条件。
- **歴史的な手法候補:** `docs/wiki/develop_memo/_work/20260804_causal_lifecycle_enhancement/03_01_coding_instruction_Phase1.md`、`03_02_coding_instruction_Phase2.md`、`03_03_coding_instruction_Phase3.md`。**現行の承認済み要件ではない**。
- **9月末申し送り:** [ENH-E11 Causal Lifecycle Foundation Gap Completion](https://app.notion.com/p/403e5855be3980c186c3f778a7bfaac5)（`HANDOFF_DRAFT`）。
- **現行要件正本:** `docs/wiki/requirement_definition/10_requirements_definition.md`（Status是正コミット`84c5a624389b233fcb97c656f1c94d177f459c5a`）。
- **後段の比較:** `06_three_source_reconciliation_matrix.md`（暫定）。Issue台帳：`07_github_issue_register.md`。
- **方法の適用前提についての公開参考資料:** [causal-learn PC](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/PC.html)、[causal-learn FCI](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/FCI.html)、[EconML DML](https://econml.azurewebsites.net/spec/estimation/dml.html)、[Tigramite PCMCI](https://jakobrunge.github.io/tigramite/)。
