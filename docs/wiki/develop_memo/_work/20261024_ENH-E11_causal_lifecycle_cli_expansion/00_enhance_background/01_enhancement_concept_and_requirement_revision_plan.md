# ENH-E11 — 構想・要件改定計画（案）

**文書区分:** Workflow所定の構想・要件改定計画（01）  
**状態:** DRAFT／ステップ4のCLI-only実装スコープ案作成済み／構想・要件・設計・Gateは正式未承認  
**起案日:** 2026-10-24（日本時間）／**改訂日:** 2026-10-25（日本時間）  
**追跡Issue:** [#13（ENH-E11全体）](https://github.com/kousuke-ota-datascience/causal-atelier/issues/13)、[#14（事前照合とArchitecture Review）](https://github.com/kousuke-ota-datascience/causal-atelier/issues/14)  
**実装現状の参照SHA:** `827a6c3683e0fff0af342cb3aded45d9dde020c9`。**正式な受入Baselineではない。**

## 0. INTRODUCTION

### 0.1. 本文書の目的

本書が答えるべき問いは、**「Ariadneの現在の因果探索・因果推論では、どのような分析条件に対応できないのか」「それを補完するため、なぜ各機能を選ぶのか」「何が検証できればENH-E11を完了とするのか」**である。手法の名称や過去のEnhancementの経緯を羅列すること自体は目的ではない。

本書は、現行実装を踏まえた**機能追加の必要性、選定根拠、完了条件、要件・設計改定方針**を定義する構想案である。新規実装の対象はScientific Core・ローカルCLI・永続ローカルファイル成果物に限定する方針を採用し、承認後の要件・Gate契約へ引き渡す。

### 0.2. 先行資料との役割分担と重複排除

現行正本・コード・テストの逐次照合と8月案との比較は**3件の事前調査資料**を根拠とし、その結果の**スコープ案00_04**とともに本書へ入力する。詳細の68行は再掲しない。

| 先行資料 | 記録する事実・責務 | 本書に引き継ぐ内容 |
|---|---|---|
| [00_01_foundation_gap_reconciliation.md](00_01_foundation_gap_reconciliation.md) | 9月末構想13項目と現行FR/NFR/AR・コード・テスト・過去999の対応。P0/P1等は**追加調査の優先順位** | 実装済み能力と新Capability候補の境界 |
| [00_02_foundation_gap_closure_assessment.md](00_02_foundation_gap_closure_assessment.md) | 現行要件の未解消4領域（GAP-C01〜C04）の証拠水準、残差、閉鎖条件、実装帰属の留保 | 未充足の要件群と未解消の判断事項 |
| [00_03_phase1_to_phase3_reconciliation.md](00_03_phase1_to_phase3_reconciliation.md) | 8月4日Phase 1〜3・A0上位構想、9月末の扱い、現行実装の68項目を照合 | 既存再利用・新規候補・後続扱い・採否未決事項 |
| [00_04_phase1_to_phase3_cli_scope_proposal.md](00_04_phase1_to_phase3_cli_scope_proposal.md) | 68項目にCLI-only実装の候補Disposition・提供範囲・後続送りとGap別帰属を提案 | 01第5章へ反映する実装スコープ案（未承認） |
| [00_05_phase1_to_phase3_cli_scope_review.md](00_05_phase1_to_phase3_cli_scope_review.md) | 00_04の技術審査。行IDの一致と、科学的・依存・Scope例外の修正要求SR-01〜12を記録 | **CHANGES_REQUIRED／修正・再審査を要する** |

**00_03の照合完了・00_04の採否案作成・00_05の技術審査実施は、いずれも新Capabilityの正式承認を意味しない。** 技術審査はCHANGES_REQUIREDであり、00_04の修正・再審査を経ずに02で承認済み扱いにしない。 A0上位構想にあるATC、matching/g-computation等の後続送り、Negative Control／未観測交絡Sensitivityの最小方式は00_04で**具体的な処遇案**を示した。承認は02で判断する。

本書の第1章は**分析上の課題とFoundation Gapの関係**、第2章は**手法の選定理由**、第3章は**現行の分析能力と適用限界（As-Is）**、第4章は**分析者の状況・問い・利用方法で表す目標状態（To-Be）**、第10章は**目標状態を検証するための暫定完了基準**を記す。8月4日のPhase 1〜3案と9月末のENH-E11申し送りは選定の来歴として第12章に記録し、現行要件や実装事実の代わりにしない。

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

**優先度の意味:** P0/P1は[00_01_foundation_gap_reconciliation.md](00_01_foundation_gap_reconciliation.md)第5章の**追加調査・閉鎖確認の優先順位**であって、「ENH-E11で必ずP0から実装する」という実装優先度ではない。第2調査[00_02_foundation_gap_closure_assessment.md](00_02_foundation_gap_closure_assessment.md)は各Gapの証拠水準・閉鎖条件を詳述する。なお現行正本にはこのほかにもPARTIAL/NOT_IMPLEMENTEDがあるため、**上表は全リポジトリの未実装要件の網羅一覧ではない**。

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

## 3. 現状と比較基準（As-Is）

### 3.1. 現行実装を判定するためのソース基準

**コード参照:** `prototype/ariadne_mvp`、`827a6c3683e0fff0af342cb3aded45d9dde020c9`（事前照合・構想草案を含む参照SHA）。正本のImplementation Status訂正は`84c5a624389b233fcb97c656f1c94d177f459c5a`を継承する。これらは**現状を調査した時点の根拠**であり、ENH-E11の完了判定や実装のBaseline SHAを確定するものではない。

| 現行実装で可能なこと | 具体的な入口・表現 | 現時点で適用範囲に含まれない事項 |
|---|---|---|
| PC／GES／LiNGAM／NOTEARSによるDiscovery | `scientific/discovery/adapter.py`のregistryとGraph JSON | FCI、PCMCI系の時系列Discovery |
| DAG／CPDAG／PAGの表現と保持 | `product/domain/graph_semantics.py`、Graph Version | 潜在交絡に配慮したFCI探索、時間lag専用のGraph |
| Causal Question/Design、Randomized／Backdoor Identification、Data Eligibility | `product/domain/analysis_spec.py`、`scientific/identification/adapter.py`とResult status | Frontdoor/IV、CATEや準実験に固有のDesign・識別 |
| ATE／ATTのDiff／OLS／IPW／AIPW、既存Diagnostics | `scientific/inference/adapter.py`、E9のbalance／overlap／ESS | CATE、LATE、RDD局所効果、科学的CI被覆率の全条件に対する認定 |
| Placebo／Data Subset Refutation、Adjustment Set／Clipping Sensitivity | Scientific Refutation／Sensitivity Adapter | 未観測交絡への感度分析を含む新規方式 |
| 既存Scientific CLIとローカルManifest | `interfaces/cli/config_schema.py`、`scientific_stage.py`等、`config_version=2.0` | 新手法の入力・結果schema、完全な実効Library version／seed／split |
| 既存Product実行・Result/Artifact・Navigation | 現行Product API／Worker／DBとNavigation catalog | 新手法のProduct統合。既存Productには別途Foundation Gapが残る |

実装・テスト・過去999判定の具体的な根拠は、[9月末構想との照合](00_01_foundation_gap_reconciliation.md)を参照する。**この調査用SHAで全件Scientific Benchmarkを再実行したわけではなく**、上表は科学的な全条件の合格認定ではない。

### 3.2. 現行能力では対応できない分析条件

第1.1節の分析課題と現行実装を突き合わせると、特に次の条件が現行のScientific契約の外にある。

| 分析条件 | 現行の制約 | 第4章の利用者ユースケース |
|---|---|---|
| 観測されない共通原因の可能性がある | PC等は利用可能でも、FCIによる潜在交絡を考慮したPAG探索がない | UC-01 |
| Backdoor以外の識別仮定を使いたい | Native識別はRandomized／Backdoor中心 | UC-02、UC-08 |
| 平均効果の推定結果がoverlap等に敏感 | IPW/AIPWとE9診断はあるが、条件別の科学的品質の追加検証が必要 | UC-03 |
| 処置効果が属性ごとに異なる | ATE/ATT中心でCATE/HTEの契約がない | UC-04 |
| 時間lag・自己相関・制度導入時点を扱う | Temporal Discoveryと準実験固有の入力・仮定・Resultがない | UC-05、UC-06 |
| 閾値、instrument、donorを用いる研究 | RDD、IV/LATE、Synthetic系の独立した推定契約がない | UC-07〜UC-09 |
| 分析結果を再実行・第三者が監査する | 既存Manifestはあるが新手法・依存version等を未定義 | UC-10 |

これらは**現行機能との差分**であり、未来に達成すべき結果そのものは第4章で、合否の試験設計は第10章で扱う。

### 3.3. 既存Foundation Gapと新規Capabilityを区別する

第1.4節の**GAP-C01〜C04は既存のFR/NFR/ARに対する残存要件Gap**であり、FCI等の追加機能そのものではない。個別の実装証拠、P0/P1の調査優先順位、閉鎖条件は[00_02_foundation_gap_closure_assessment.md](00_02_foundation_gap_closure_assessment.md)を参照する。

**実装帰属は未決定である。** CLI-onlyのENH-E11でProduct側のGAP-C01・C02・C04を修正しない場合、それらを`IMPLEMENTED`へ変更してはならない。正式なスコープ審査時に、各Gapについて(a) E11内で閉鎖、(b) 別Issue／別Enhancementへ移管、(c) 承認済み要件変更で期待値を更新、のいずれかと責任者を記録する。GAP-C03の新規CLIへの実効version・seed要件は、第10章に受入条件を定めるが、Product側の部分充足を自動的に閉鎖しない。

### 3.4. 現状判定に使用する証拠と権限

現状把握の基準は**現行要件正本＋固定コードSHA＋既存テスト・過去の999の対応**である。実装の存在、テストの存在、過去の受入PASS、当該SHAでの新規再実行を混同しない。

一方、ENH-E11の**将来の完了条件**は本章のSHAやImplementation Statusから導かれるものではない。**第4章の目標ユースケースから第10章の検証主張を設計**し、正式承認後に要件・設計・Gate 06/07の受入契約として固定する。

## 4. 目標状態（To-Be）：分析者のユースケース

### 4.1. 目標状態の記述方法と適用上の前提

本章は、**「どのような状況で、どの分析トピックについて、どんな因果的な問いを持つ分析者が、Ariadneをどのように使える状態を目指すか」**を記す。分析手法の名前や関数の提供を目標とするのではなく、**判断可能になること・判断できないことの両方**を記載する。

各ユースケースは**想定利用例**であり、実データで当該効果が実証されたことを意味しない。分析者がCausal Question・Design・仮定・対象データを明示し、**ローカルCLIから**適切な手法を選んで実行する。手法を自動選定して適用可能性を保証する機能や、新規Web UI／API／Worker／DB統合は今回の到達状態に含めない。

以下は「**状況／分析トピック／問い／利用方法／得られる結果と限界**」を共通の記載粒度とする。目標の検証内容は第10.1節でUC-IDと受入条件を対応付ける。

### 4.2. UC-01：潜在交絡が疑われる設備トラブルの因果探索

**状況・分析トピック：** 工場の温度・振動・圧力・設備停止の時系列でない観測記録から、停止に関連する原因候補を調べている。作業者の判断や外部環境など、一部の共通原因がデータに記録されていない可能性がある。

**分析の問い：** 「設備停止に関係する変数の方向について、観測データからどこまで判断できるか。潜在交絡の可能性によって、どの方向が未確定のまま残るか。」

**想定する利用方法：** 分析者は対象列と前提知識を設定し、既存PCなどと並んで**FCI**によるDiscoveryをScientific Core／CLIで実行する。結果をPAGとして保存し、circle endpoint、潜在交絡の可能性、アルゴリズム・独立性検定・入力hashを確認する。

**得られる結果・判断の限界：** 候補となる因果構造と**方向が確定できない部分を区別して**検討できる。PAGから任意のDAGを作って効果推定を確定したり、FCIによって真の因果構造が必ず識別されたと主張したりしない。

### 4.3. UC-02：観察研究で介入効果の識別条件を検討する

**状況・分析トピック：** 健康支援プログラムへの参加が本人の意思や中間的な行動に左右される観察研究を扱う。既存のBackdoor調整だけでは、分析者が置きたい仮定を表現しきれない。

**分析の問い：** 「この介入が健康指標へ与える効果は、現在のGraph・観測変数・Frontdoor／IV等の仮定の下で識別可能か。」

**想定する利用方法：** 分析者は介入、outcome、estimandと仮定を宣言し、既存Native Identificationまたは**optional DoWhy等**を選択する。識別戦略、利用する変数、根拠、識別式・理由を保存し、条件が成立した場合にのみ対応するEstimationへ進む。

**得られる結果・判断の限界：** 識別可能な条件と`NOT_IDENTIFIED`／`REQUIRES_REVIEW`を区別できる。Libraryが識別式を出したことと、その仮定が現実に成り立つことは別であり、**識別できない研究で効果の数値を捏造しない**。

### 4.4. UC-03：店舗施策の平均効果を診断付きで評価する

**状況・分析トピック：** 過去にクーポンを配布した店舗と配布しなかった店舗の売上を比較する。配布対象が店舗特性によって偏っており、極端なPropensity Scoreが含まれる可能性がある。

**分析の問い：** 「観測された交絡を調整すると、配布施策のATEまたはATTはどの程度か。その数値はoverlap不足や極端重みにどれだけ依存するか。」

**想定する利用方法：** 分析者は既存`ipw`（IPTW）／`aipw`等を再利用し、Estimationとともにweight、balance、overlap、ESS、Clipping、Refutation、Sensitivityの結果をCLI成果物として確認する。

**得られる結果・判断の限界：** 効果推定値、推論の不確実性、適用上の警告、頑健性を並べて評価できる。overlap不足や妥当でないAdjustmentの際は適切な警告・負結果を返す。**重み付けだけで未観測交絡が解消されたとは解釈しない**。

### 4.5. UC-04：顧客属性によって異なる支援施策の効果を調べる

**状況・分析トピック：** 同じ顧客支援策でも、利用歴や地域によって継続率への影響が違うと考えられる。全体ATEだけでは対象者ごとの効果の違いを説明できない。

**分析の問い：** 「条件付き処置効果（CATE）は属性・集団ごとにどう異なるか。どの領域ではデータのsupportが足りず、不確実性が大きいか。」

**想定する利用方法：** 分析者はeffect modifier、適格性、Treatment/Outcome型、cross-fittingと推論法を指定し、承認済みの**EconML DML／DR／Causal Forest／S・T・X Learner等**の中から適切な推定器を実行する。群別要約や個票CATEの安全なファイルを取得し、support・overlap・uncertaintyを確認する。

**得られる結果・判断の限界：** 平均効果と異なる**条件付き効果**を区別し、どの群で推定の根拠が弱いか判断できる。単なる予測scoreやsubgroupの結果差をCATEに読み替えず、個票CATEの利用を理由にPolicyの自動最適化・配布を行わない。

### 4.6. UC-05：センサデータの時間lagを考慮した因果探索

**状況・分析トピック：** 複数設備のセンサ値が時間を追って影響し合う生産ラインで、単なる同時刻の相関だけでは異常の伝播順を説明できない。自己相関や同時点関係がある。

**分析の問い：** 「圧力の変化が何ステップ後に温度や停止リスクの変化と関連するか。時間順序を考慮した因果構造のうち、何が未確定か。」

**想定する利用方法：** 分析者は時間軸、系列、lag範囲、stationarity等の仮定、CI-testを指定し、**PCMCI／PCMCI+／LPCMCI**から方法条件に合うものをCLIで実行する。Temporal Graphとlag・CI検定・実効parameterを保存する。

**得られる結果・判断の限界：** 時間差のある候補関係と未確定の方向・潜在交絡の注意を確認できる。欠損時刻、重複したunit-time、短すぎる系列、仮定違反では分析を拒否・要レビューとし、**lag関係の発見を介入効果と同一視しない**。

### 4.7. UC-06：段階導入された施策の効果を評価する

**状況・分析トピック：** 自治体が支援制度を地域ごとに異なる月から導入し、対象地域・対照地域の月次成果が観測されている。一部の地域は未導入で、時期ごとの影響も異なる。

**分析の問い：** 「制度導入による処置効果は、導入前の傾向・地域差・導入時期を考慮して推定できるか。効果は導入後どの時点から現れるか。」

**想定する利用方法：** 分析者は処置群・比較群・導入時刻・パネル構造と平行トレンド等の仮定を宣言し、**DiDとEvent Study**を実行する。比較群の条件、pretrend、event-time、cluster、staggered adoptionへの対応を記録する。比較群が構成できない単一系列では、**Interrupted Time Series**を別Designとして検討する。

**得られる結果・判断の限界：** 介入時点に関連する効果と不確実性、仮定違反・比較群不足を確認できる。**ITSの前後変化とDiDの比較設計を同じ識別根拠とは扱わず**、平行トレンドの成否を検定一つで証明したと主張しない。

### 4.8. UC-07：支援対象の点数閾値を利用して局所効果を推定する

**状況・分析トピック：** 一定の審査点数を超えると補助金の対象となる制度がある。閾値付近の申請者は比較的似ている一方、得点の操作や実際の受給率の差が疑われる。

**分析の問い：** 「閾値の直前と直後で成果に差があるか。その差は閾値付近の局所的な処置効果と解釈できるか。」

**想定する利用方法：** 分析者はrunning variable、cutoff、bandwidth、Sharp/Fuzzyの区別を指定し、**RDD**をCLIで実行する。local effect、bandwidth感度、密度・共変量の不連続性、first-stage等の診断を保存する。

**得られる結果・判断の限界：** 閾値付近の効果と、その解釈を制限する操作・support不足を確認できる。**局所効果を全申請者のATEとして一般化しない**。

### 4.9. UC-08：奨励の割当をInstrumentとして介入効果を調べる

**状況・分析トピック：** 研修への参加は自己選択だが、研修案内の送付対象は外生的に割り当てられている。参加者と非参加者を直接比較すると交絡が疑われる。

**分析の問い：** 「案内の割当が研修参加を十分に変化させ、適切なIV仮定が置ける場合、効果はどの対象集団の何を表すか。」

**想定する利用方法：** 分析者はinstrument、処置、outcome、exclusion restriction等の仮定を指定し、**IV／LATE**（必要に応じて承認済みIV+ML方法）を選択する。first-stage、weak-IV、識別対象集団、推論結果を保存する。

**得られる結果・判断の限界：** Instrumentに関する条件が成立する場合に限り、LATE等を明確に区別して解釈できる。弱いInstrumentや妥当性が疑われる場合は科学的なwarning／不成立結果を返し、**LATEを全母集団ATEと誤認しない**。

### 4.10. UC-09：介入地域の反事実を複数地域から構成する

**状況・分析トピック：** 一つの地域で環境施策を実施し、同じ条件の未実施地域が存在しない。過去の推移が類似する複数の地域が観測されている。

**分析の問い：** 「未実施だった場合の成果をどの程度再構成できるか。推定した施策効果はdonorの選定や介入前の当てはまりにどれだけ敏感か。」

**想定する利用方法：** 分析者は介入時点、対象地域、donor候補、pre/post期間を宣言し、**Synthetic Control／Synthetic DiD**を実行する。donor weights、pre-fit、placebo、感度診断と反事実系列のファイルを確認する。

**得られる結果・判断の限界：** 推定反事実と観測系列の差、合成の妥当性を説明できる。donor contaminationやpre-fit不良がある場合は警告・要レビューとし、**donor weightをIPTWの処置重みと混同しない**。

### 4.11. UC-10：第三者が分析結果を再現・監査する

**状況・分析トピック：** 分析者が複数手法の結果を研究報告として引き渡し、別担当者が後から同じ入力・設定と計算環境で再計算したい。結果が利用不能や非識別だった実行も経緯として残す必要がある。

**分析の問い：** 「この結果はどのデータ・Graph・Design・手法・乱数・Library versionから生じたか。再実行すると一致するか。どの科学的仮定が成立しなかったか。」

**想定する利用方法：** 分析者は各手法のローカルCLI設定を実行し、**入力hash、検証済みspec、実効seed/split、backend version、Result、Diagnostics、Artifact checksum**をManifestで受け渡す。別担当者はManifestと保存ファイルを使って再実行・差分確認する。

**得られる結果・判断の限界：** 数値結果と負結果の**来歴・再現条件を追跡**できる。optional依存が欠落する場合は明示的に利用不可とし、個票CATEなど機微情報は適切に制限する。ただし、このローカルManifestによって**既存Product DBのCanonical Lineage Gap-C02が閉鎖したとは主張しない**。

### 4.12. ユースケース全体に共通する目標

すべてのユースケースで、分析者が**問い・estimand・Design・識別仮定・データ適格性**を把握し、適用可能な手法を明示的に選択できることを目指す。成立する条件では数値と不確実性を、成立しない条件では非識別・前提不足・要レビュー等の**科学的な負結果**を受け取れる。

本章の研究例は目標を具体化するための説明であり、全業界への適用保証や自動的なPolicy意思決定を約束するものではない。**第10章はこのユースケースの能力を検証する手段**であり、テスト可能な部分だけを取り出して目標を縮小してはならない。

## 5. 対象範囲（ステップ4のCLI-only実装スコープ案）

### 5.1. 判定済みスコープ案の読み方

第1〜4章で明らかにした**分析上の必要性とユースケース**を、[00_04_phase1_to_phase3_cli_scope_proposal.md](00_04_phase1_to_phase3_cli_scope_proposal.md)の**68項目**へ対応付けた。各行を **R=既存再利用、Q=品質強化、N=新規Scientific Core／local CLI／local file、D=後続対応**として分類し、混合項目はR+N等で分けた。**00_03は事実の照合、00_04は今回何を提供するかの案**であり、正式な採否承認はまだ受けていない。

**提供面はScientific Core＋ローカルCLI＋永続ローカルファイル（Versioned Spec、JSON/Parquet、Manifest、checksum、実効version・seed/split）に限定**する。新機能のWeb UI/API/Worker/DB・migrationは実装しない。既存Product契約と既存CLIを維持する。

### 5.2. Phase 1〜3の対象Method群

| Phase | 再利用（R）・品質強化（Q） | 新規Scientific Core／CLI／Local file候補（N） | 00_04で追跡する項目 |
|---|---|---|---|
| **Phase 1** | Question/Design、DAG/CPDAG/PAG、PC/GES/LiNGAM/NOTEARS、Randomized/Backdoor、Data Eligibility、ATE/ATT・IPW/AIPW、既存E9 diagnostics／Refutation／Sensitivity。IPTW推論はQ | FCI/PAG、optional DoWhy Backdoor/Frontdoor/IV、Random Common Cause/Bootstrap Refutation、Negative Control・未観測交絡Sensitivityの最小方式（採用境界は要審査）、方法別Eligibility、Local result/manifest | `P1-01〜21` |
| **Phase 2** | 既存AIPW/cross-fittingとoptional依存分離の原則 | CATE/HTE、LinearDML、CausalForestDML、DRLearner、ForestDRLearner、S/T/X Learner、DRIVまたは承認済み同等IV+ML、support/calibration/CI、機微情報を制限したCATE Parquetと群別JSON | `P2-01〜18` |
| **Phase 3** | 既存Graph/CLI/Manifestの汎用基盤 | TemporalDesign、PCMCI/PCMCI+/LPCMCI、CI-test registry、DiD/Event Study/ITS、Sharp/Fuzzy RDD、IV/LATE、Synthetic Control/Synthetic DiD、method別Estimand／適格性／診断・結果 | `P3-01〜19` |
| **共通** | 既存Scientific CLI/E9回帰 | Versioned input・データ/Graph/Design参照、依存環境/seed/split/Manifest、科学的負結果、Known-truth Benchmark、atomic file／機微情報制御 | `X-01〜10` |

列挙したMethodは**必須候補としてすべて保持**する。Phase 2の「4 estimator family以上」を口実に他の列挙手法を無断で除外しない。外部Libraryに希望するclassが存在しない場合は、科学的同等性・要件差分・Human owner承認を条件とし、現時点で対応済みとはしない。

### 5.3. 後続送りと既存Foundation Gapの取り扱い

- **D（今回提供しない）:** 旧Phase文書の新規Web UI/API/Worker/DB、Product migration/RBAC統合、Phase4 Policy Evaluation／Monitoring／Mediation、RPCMCI/J-PCMCI+、上位A0にのみ挙がるATC・matching/g-computation・汎用Graph perturbation等の独立方式。
- **要審査の提案:** A0とPhase実装指示の強度差があるNegative ControlとUnobserved-confounding Sensitivityについては、Phase1に最小限の**実行可能な科学的方式（N）**を提案する。具体的なmethod、前提と結果の意味は03/04改定案・Architecture Reviewで審査する。上位A0の全方式を無条件採用するものではない。
- **既存Gap-C01/C02/C04:** Product探索再利用warning、canonical DB lineage、Navigation Capability所有権はCLI-onlyのコード作業対象外の案とする。要件は**未解消のまま**であり、#14を窓口として別Enhancementの担当・Issue・閉鎖条件を承認時に決める。
- **既存Gap-C03:** 新CLIに実効Library versionとseed/split・環境provenanceを独立した受入契約として課す。これで既存Product StageAttempt／Executionの`PARTIAL`を閉鎖したことにはならない。

### 5.4. ステップ4と正式な承認の境界

**成果物としてのステップ4は、68項目のScope案・Method一覧・後続送り・Gap帰属案を整備した状態まで到達した。** ただし、**スコープの人間承認は未実施**である。02の承認記録で次を確認すること：①A0上位要求のD案、②Negative Control/未観測交絡Sensitivityの方法、③EconML・Tigramite等のLibrary versionと同等代替、④Product Gapの責任移管、⑤科学的な受入値・Scopeに見合う費用と実施順序。

上記を承認後、03/04/05およびArchitecture Reviewへ反映して、Gate 06/07・Work Packageを確定する。**この段階では実装やGate凍結を許可しない。**

## 6. 要件改定の見込み

- 既存FR-035〜050・FR-153〜156の実装済み契約は維持する。**FR-051・FR-054等の現行PARTIAL/NOT_IMPLEMENTEDを、新Capabilityの追加だけで解消としない**。詳細は00_01・00_02に委ねる。スコープ案は00_04を参照する。
- FCI/DoWhy、CATE/HTE、Temporal/Quasi-experimental Design、追加Refutation/Sensitivity（Negative Control・未観測交絡の最小方式は要審査）、Local CLI artifactを独立した意味の新FRにする。各手法に適格性、識別・推定対象、科学的負結果、provenanceを定義する。
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

## 10. 完了基準と暫定Gate構成（承認前）

### 10.1. ユースケースから導く受入条件（案）

**完了基準は第4章の目標状態を判定するための手段**であり、逆に本表から実現したい分析能力を縮小しない。各UCについて、「意図した分析が可能な事例」だけでなく、**仮定不成立・識別不可・データ不適格・依存不足の事例**が扱えることを確認する。

| 仮の受入ID | 関連UC | 完了時に示すべき状態 | 検証可能な証拠・否定例 |
|---|---|---|---|
| **E11-AC-01：Coverage** | UC-01〜10 | 正式承認したPhase 1〜3の必須Capabilityが、既存再利用／新規実装／承認済み代替／明示的対象外のいずれかに追跡され、必要なものはCLIで利用できる | Requirement→Design→UC→Issue→Gate→Testの対応。未承認の手法省略や成功例のみの検証は不可 |
| **E11-AC-02：Identification/Graph** | UC-01、02、08 | Graph・Designの仮定、不確定endpoint、識別可否を保持し、非識別の効果数値を強制生成しない | 既知DAG/PAG、潜在交絡、Backdoor／Frontdoor／IV、未確定edgeの成功・負例 |
| **E11-AC-03：ATE/ATT/IPTW** | UC-03 | 既存IPW／AIPWを再利用し、推論・重み・overlap・balance・ESS・Refutation/Sensitivityを区別して評価する | 既知真値bias、CI被覆率、極端重み、poor overlap、seed再実行、E9回帰 |
| **E11-AC-04：CATE/HTE** | UC-04 | CATE/HTEのestimandとsupport・不確実性を、承認済みDML/DR/Causal Forest/Meta/IV+MLで適切に扱う | 異質性既知真値、条件不成立、cross-fitting、privacy、interval・calibration |
| **E11-AC-05：Temporal** | UC-05 | PCMCI系がlag・同時点・不確定性を保持し、入力時系列の前提を検査する | 既知lag、独立系列、欠損/重複time index、autocorrelation、CI検定不適合 |
| **E11-AC-06：Quasi-experimental** | UC-06〜09 | DiD/Event/ITS、RDD、IV/LATE、Synthetic系で各Design固有のestimand・仮定・負結果を明示する | 平行トレンド違反、staggered adoption、cutoff操作、weak-IV、donor不良等の成功・失敗fixture |
| **E11-AC-07：CLI/Reproducibility** | UC-01〜10（特にUC-10） | 承認済み全手法を新規Web/DB統合なしで実行し、実効版・入力・seed/split・Result・checksumを追跡する | optional backend有無、固定seed再実行、Manifest schema、artifact read-back、partial failure、機微情報保護 |
| **E11-AC-08：Compatibility/Acceptance** | UC-01〜10 | 既存Scientific CLIとProductの受入済み契約を保護し、各新手法に独立した科学的受入証拠がある | 旧CLI契約、E9 Diagnostics回帰、承認済みRequirement／Design、Gate 06/07、独立30検証とcanonical 999 |

**測定基準は未確定:** Scientific Benchmarkのデータ生成方法、既知真値との許容誤差、区間推定の被覆率、CI test・準実験診断閾値、依存Library version／platform等は**正式Gate 07で数値・fixture・method単位でfreeze**する。Library importや関数の正常終了だけでは科学的に受入済みとしない。

### 10.2. 暫定Gateとユースケースの対応

| Gate案 | 主な受入境界 | 主なUC／受入条件 | 対応Issue |
|---|---|---|---|
| G01 | Local causal context、FCI/PAGの不確定性 | UC-01／AC-02、AC-07 | #15、#17 |
| G02 | Identification/Eligibility、optional backend | UC-02／AC-02、AC-07 | #15、#16 |
| G03 | IPTW/AIPW、Refutation/Sensitivity | UC-03／AC-03 | #16、#19 |
| G04 | CATE/HTEとEconML推定器 | UC-04／AC-04 | #18 |
| G05 | CATE診断・秘匿性を考慮したファイル | UC-04、10／AC-04、AC-07 | #18、#24 |
| G06 | Temporal GraphとPCMCI系 | UC-05／AC-05 | #20 |
| G07 | DiD/Event Study/ITS | UC-06／AC-06 | #21 |
| G08 | RDDとIV/LATE | UC-07、08／AC-06 | #22 |
| G09 | Synthetic Control/SDID | UC-09／AC-06 | #23 |
| G10 | Local Manifest／再現性／既存回帰・科学検証 | UC-10と全UC／AC-07、08 | #24 |

**Gate数・順序は未確定。** Architecture Reviewで意味上の受入単位に統合・分割する。Issueは作業追跡、Work Packageは実装単位、Gate 06/07は受入契約であり、相互の代替にならない。E11-ACも仮番号である。

### 10.3. 完了判定を形式的なPASSへ縮退させないための原則

1. **ユースケースの問いを基準にする。** その手法が実際に何を識別・推定できるのかを説明できない場合、APIの正常応答だけで完了としない。
2. **適用限界も達成対象とする。** 非識別、weak-IV、poor overlap、PAGの未確定端点、違反したデザイン仮定を捏造・隠蔽して成功扱いしない。
3. **手法固有の科学Benchmarkを用いる。** 既知真値・再現性・負例を独立検証し、事前に凍結された閾値で判定する。
4. **UCが不足している場合は目標を削るのではなく、受入条件を追加する。** 要件変更・構想縮小を要するときはオーナーの明示承認を得る。
5. **既存ProductのGapは別管理する。** 第3.3節のGAP-C01〜C04を、局所CLIの科学的PASSで自動閉鎖しない。

## 11. 実装前に必要な承認

- PC中心の既存能力を補完するための**分析条件・適用範囲・手法の採否**と、Phase 1〜3をE11のCLI-onlyで提供する構想の正式承認。
- 現行Foundation GAP-C01〜C04の各閉鎖または移管の決定。実装優先順位と調査優先度P0/P1を混同しない。
- 正本§11の外部engine取扱い、新FR/NFR/AR、Design/Result権威、optional version、local file/privacy contractの承認。
- Benchmark fixture・科学的閾値・適格性・負結果・互換性の固定、Architecture Review、正式Gate 06/07のfreeze。
- 実装後は独立検証とcanonical 999 PASS。**本書やIssueの更新は承認・受入に代わらない**。

## 12. 出典・補足資料

- **9月末構想と現行実装の照合:** [00_01_foundation_gap_reconciliation.md](00_01_foundation_gap_reconciliation.md)。13項目とP0/P1の調査優先度。
- **未解消Gapの確定:** [00_02_foundation_gap_closure_assessment.md](00_02_foundation_gap_closure_assessment.md)。GAP-C01〜C04、関連FR/NFR/ARと閉鎖条件。
- **実装スコープ案（ステップ4準備済み・未承認）:** [00_04_phase1_to_phase3_cli_scope_proposal.md](00_04_phase1_to_phase3_cli_scope_proposal.md)。Phase1〜3のCLI-only 68行と上位A0の採否留保。
- **歴史的な手法候補:** `docs/wiki/develop_memo/_work/20260804_causal_lifecycle_enhancement/03_01_coding_instruction_Phase1.md`、`03_02_coding_instruction_Phase2.md`、`03_03_coding_instruction_Phase3.md`。**現行の承認済み要件ではない**。
- **9月末申し送り:** [ENH-E11 Causal Lifecycle Foundation Gap Completion](https://app.notion.com/p/403e5855be3980c186c3f778a7bfaac5)（`HANDOFF_DRAFT`）。
- **現行要件正本:** `docs/wiki/requirement_definition/10_requirements_definition.md`（Status是正コミット`84c5a624389b233fcb97c656f1c94d177f459c5a`）。
- **8月4日のPhase 1〜3との差分照合（ステップ3完了）:** [00_03_phase1_to_phase3_reconciliation.md](00_03_phase1_to_phase3_reconciliation.md)。**68行のソース照合完了／最終採否・実装Scopeは未承認。** Issue台帳：`07_github_issue_register.md`。
- **方法の適用前提についての公開参考資料:** [causal-learn PC](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/PC.html)、[causal-learn FCI](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/FCI.html)、[EconML DML](https://econml.azurewebsites.net/spec/estimation/dml.html)、[Tigramite PCMCI](https://jakobrunge.github.io/tigramite/)。
