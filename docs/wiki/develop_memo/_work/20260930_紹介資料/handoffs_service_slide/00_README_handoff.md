Document title: Ariadne分析PoCサービス紹介｜スライドブラッシュアップHandoff

# 0. INTRODUCTION

## 0.1. 背景 / 目的

私のチームでは、予測分析、因果推論のPoCサービス提供を行っている。

当チームのサービス紹介資料を作成したいと考えている。

本資料では、予測分析・因果推論を単なる分析手法のカタログとして紹介するのではなく、**顧客の業務課題・意思決定から出発し、どのような問いにどの分析を適用し、PoCを通じて何を検証し、どのような業務効果・次アクションへ接続するか**を一連のストーリーとして説明する。

資料全体では、以下の順序で論理を構成する。

1. 顧客が直面する問いを整理し、予測分析と因果推論の役割・使い分けを示す。
2. 分析PoCを業務課題・意思決定へ接続する共通設計を示す。
3. 予測分析について、適用課題、期待効果、分析プロセス、手法選定、評価、成果物・Go / No-Goまで説明する。
4. 因果推論について、適用課題、期待効果、Causal Question / Estimand、因果構造、Identification、Estimation、Diagnostics / Sensitivity、成果物まで説明する。
5. 最後に、分析実装の基本方針、Ariadneの位置づけ、具体的な適用イメージ、PoC開始までの流れを示す。

予測分析については、未知・将来のOutcomeをどの程度予測できるかだけでなく、**予測結果を誰がどの業務判断に使い、どのActionへつなげるか**を重視する。

因果推論については、相関や予測可能性と介入効果を区別し、**Causal Question / Estimand、Assumptions、Identification、Estimation、Diagnostics / Sensitivity**を必要に応じて分けて扱い、「どの前提のもとで、どこまで主張できるか」を明示する。

分析実装はデータサイエンティストによるスクラッチ開発を基本とし、成熟したOSSや既存ライブラリを必要に応じて利用する。Ariadneはサービス提供の必須前提ではなく、問い・データ・分析条件・実行・結果・判断理由を構造化し、分析プロセスの追跡可能性や再現性を補助する選択肢として位置づける。

スライドごとに、伝えたいMessageと、それを説明・論証するChartをブラッシュアップするため、30枚のスライドを1枚ずつ独立スレッドでブラッシュアップする方針である。

各独立スレッドでは、原則として以下の3ファイルのみを入力とする。

- 本ファイル `00_README_handoff.md`
- スライドMarkdown構造の正本 `../slide_skelton_structure.md`
- ブラッシュアップ対象の `[Section]-[Subsection]_[SLUG].md`

本ファイルを**資料全体の背景・ストーリー・Scientific / Business制約・Cross-slide運用ルールのSingle Source of Truth**、`slide_skelton_structure.md` を**スライドMarkdown標準構造・各構成要素の用語定義・Audience / PurposeのSingle Source of Truth**、各 `[Section]-[Subsection]_[SLUG].md` を**対象スライド内容のSingle Source of Truth**とする。個別のスライド別handoffファイルは使用しない。

## 0.2. 参考にするべきコードベース / 資料

本資料のブラッシュアップでは、分析サービスの実際の提供能力やAriadneの設計思想と説明内容が乖離しないよう、以下を参照する。

### 0.2.1. Ariadne リポジトリルート

- https://github.com/kousuke-ota-datascience/causal-atelier/tree/prototype/ariadne_mvp/

### 0.2.2. Ariadne 要件定義 / 設計

- https://github.com/kousuke-ota-datascience/causal-atelier/tree/prototype/ariadne_mvp/docs/wiki/requirement_definition
- 特に以下を確認する。
  - Exploratory / Predictive / Causal のAnalysis Familyが答える問いと意味論
  - Planning / Execution
  - Research Context
  - 分析条件・結果・Artifact・Lineage・判断理由の扱い
  - 因果推論におけるIdentificationとEstimationの責務分離
  - 予測分析におけるTrain / Predict / Metrics / Explainability等の区別
  - Predictive explanationをcausal effectとして扱わない設計原則

### 0.2.3. Ariadne コードベース

- https://github.com/kousuke-ota-datascience/causal-atelier/tree/prototype/ariadne_mvp/src/ariadne
- 特に以下を参照する。
  - `src/ariadne/capabilities/predictive/`
  - `src/ariadne/capabilities/causal/`
- 実装済みCapabilityと資料上の表現を照合し、現時点で実装されていない機能をAriadneの提供機能として断定しない。
- Ariadneで実装可能なアルゴリズムの範囲と、データサイエンティストがスクラッチ実装・OSS利用によって提供可能な分析サービスの範囲を混同しない。

### 0.2.4. Markdownスケルトン / 標準構造

- https://github.com/kousuke-ota-datascience/causal-atelier/blob/prototype/ariadne_mvp/docs/wiki/develop_memo/_work/20260823_GTM_explain/20260823_GTM_14_integrated.md.md
- ストーリーの構造化、論点の展開、スライド単位への分解方法を検討する際の参考とする。
- https://github.com/kousuke-ota-datascience/causal-atelier/blob/prototype/ariadne_mvp/docs/wiki/develop_memo/_work/20260930_%E7%B4%B9%E4%BB%8B%E8%B3%87%E6%96%99/slide_skelton_structure.md
- スライドMarkdownの標準構造、各構成要素の用語定義、および資料のAudience / Purposeについては、`slide_skelton_structure.md` を正本とする。本ファイルでは同定義を重複管理しない。

## 0.3. 資料全体のストーリー / スライド構成

### 0.3.1. 全体ストーリー

資料全体の論理は、以下の5段階で構成する。

```text
分析で何を知り、何を決めるのか
        ↓
予測分析と因果推論をどう使い分けるのか
        ↓
PoCをどのように業務意思決定へ接続するのか
        ↓
Predictive / Causalそれぞれをどう設計・検証するのか
        ↓
PoC結果を次のAction / 本番化判断へどう接続するのか
```

各スライドは、この全体ストーリーにおける固有の役割を持つ。個別スライドを改善する際に、前後スライドと同じ主張を重複させない。

### 0.3.2. 全30スライド

| Slide | タイトル | Message |
|---:|---|---|
| 01 | 当チームが提供する分析PoCサービス | 当チームは、将来を見通す「予測分析」と、施策による変化を捉える「因果推論」のPoCを、業務意思決定への接続まで含めて支援する。 |
| 02 | 問いから分析アプローチを選ぶ | サービス選択は、業務課題と「何を知りたいか」から決める。 |
| 03 | 予測分析と因果推論の使い分け | 予測は「Outcomeを当てる」ため、因果は「介入によるOutcomeの変化を知る」ための分析であり、評価軸も前提も異なる。 |
| 04 | 分析サービス適用による期待効果 | 予測分析は「先回りして資源を配分する力」を、因果推論は「効果のある施策へ資源配分する力」を高める。 |
| 05 | 分析PoCの目的 | PoCの目的はモデルや推定値を作ることではなく、業務上の意思決定に使える情報を再現可能な形で得られるかを検証することである。 |
| 06 | 業務課題から意思決定までの接続 | 分析設計の起点は「何を分析したいか」ではなく、「誰が、何を、どう決める必要があるか」を明確にすることである。 |
| 07 | 分析結果を業務で利用するための設計 | 分析結果を業務へ定着させるには、結果の利用者・利用タイミング・Action・判断基準をPoC段階から設計する必要がある。 |
| 08 | PoC全体プロセス | PoCは「業務課題の定義」から「意思決定への接続」までを一連のプロセスとして進め、分析工程だけを切り離さない。 |
| 09 | PoC開始条件と成功基準 | PoC開始時に「問い・Decision・データ・成功基準」を合意し、終了時は分析精度だけでなく業務利用可能性まで含めてGo / No-Goを判断する。 |
| 10 | 予測分析とは | 予測分析は、観測済みの情報から未知・将来のOutcomeを推定し、事前に判断や資源配分を変えるための分析である。 |
| 11 | 予測分析が適する業務課題 | 予測分析が特に有効なのは、結果が起きる前に予測を使って対象・時期・量を変えられる業務である。 |
| 12 | 予測分析適用による期待効果 | 予測分析は、将来リスクや需要を事前に可視化することで、限られた人・時間・予算を優先度の高い対象へ配分しやすくする。 |
| 13 | 予測分析PoCの分析プロセス | 予測PoCでは、モデル選定より先にPrediction Questionと検証設計を固定し、未知データで再現する性能を評価する。 |
| 14 | 代表的な予測アプローチと選定方法 | 予測モデルは一律に高度な手法を選ぶのではなく、データ特性・必要性能・説明性・運用制約のバランスで選定する。 |
| 15 | 予測モデルの評価と解釈 | 予測モデルは単一のAccuracyで評価せず、未知データ性能・Calibration・失敗パターン・業務コストを組み合わせて判断する。 |
| 16 | 予測分析PoCの成果物とGo / No-Go | 予測PoCではモデルだけでなく、利用条件・誤り方・業務適用範囲まで成果物化し、本番化の可否を判断する。 |
| 17 | 因果推論とは | 因果推論は、観測された関連ではなく「Treatmentを変えたときOutcomeがどう変わるか」という反実仮想の問いを扱う。 |
| 18 | なぜ予測だけでは施策判断に答えられないのか | 「結果が悪くなりそうな対象」と「施策によって結果を改善できる対象」は一致しないため、施策判断には因果効果が必要になる。 |
| 19 | 因果推論が適する業務課題 | 因果推論が適するのは、「施策を実施する／しない」「条件を変える／維持する」といった選択肢の効果を比較したい業務である。 |
| 20 | 因果推論適用による期待効果 | 因果推論は、施策の増分効果と不確実性を比較することで、効果のある施策・対象へ資源を集中する意思決定を支援する。 |
| 21 | 因果推論PoCの分析プロセス | 因果PoCでは、推定器を選ぶ前にCausal Question・Estimand・因果構造・Identificationを定義し、その後にEstimationと妥当性確認を行う。 |
| 22 | Causal QuestionとEstimandの定義 | 因果分析の対象は「因果関係一般」ではなく、Treatment・Outcome・Population・比較条件を明示したEstimandとして定義する。 |
| 23 | 因果構造と前提条件の整理 | 因果効果を推定するには、変数間の時間順序と役割を整理し、何を交絡として調整し、何を調整してはいけないかを明示する必要がある。 |
| 24 | IdentificationとEstimationを分けて考える | Identificationは「因果効果をデータから表現できるか」、Estimationは「その量を有限標本からどう推定するか」であり、別の問題である。 |
| 25 | 代表的な因果推論アプローチと選定方法 | 因果推論の手法は、利用できる実験・制度・時間構造・交絡情報に応じてIdentification Strategyから選定する。 |
| 26 | 診断・感度分析とPoC成果物 | 因果PoCではEffect Estimate単体を成果とせず、Overlap・Balance・Pre-trend等の診断とSensitivityを合わせて、どこまで主張できるかを判断する。 |
| 27 | 分析実装の基本方針とAriadneの位置づけ | 分析はデータサイエンティストのスクラッチ開発を基本とし、成熟OSSを適切に組み合わせ、Ariadneは分析プロセスの構造化・追跡を補助する。 |
| 28 | 予測分析PoCの適用イメージ | 予測PoCでは、解約等の将来リスクを予測するだけでなく、その確率を使って対応対象を優先し、業務施策へ接続するところまで検証する。 |
| 29 | 因果推論PoCの適用イメージ | 因果PoCでは、キャンペーン対象者の購買率差を見るだけでなく、施策を実施したことによる増分効果を識別し、施策継続・対象選定へつなげる。 |
| 30 | PoC開始までの進め方 | PoCは、業務課題・意思決定・データの初期確認から始め、分析可能性とSuccess Criteriaを合意した上でスコープを確定する。 |

### 0.3.3. セクション別の役割

| Slide | セクション | 役割 |
|---:|---|---|
| 01–04 | サービス概要 | 提供サービス、業務課題・知りたいことを基準としたPredictive/Causalの選択、両者の使い分け、期待効果を定義する |
| 05–09 | 業務接続 / PoC共通設計 | 分析PoCを業務意思決定・Action・Go / No-Goへ接続する共通設計を示す |
| 10–16 | Predictive | 予測分析の問い、適用課題、期待効果、分析設計、手法選定、評価、成果物を示す |
| 17–26 | Causal | 因果推論の問い、適用課題、期待効果、Estimand、Assumptions、Identification、Estimation、妥当性確認、成果物を示す |
| 27 | 実装方針 | スクラッチ開発・OSS・Ariadneの位置づけを示す |
| 28–29 | 適用イメージ | Predictive / Causalを具体的な業務課題へ接続した例を示す |
| 30 | PoC開始 | ヒアリングからScope・Success Criteria合意までの入口を示す |

## 0.4. 全スライド共通の設計原則

1. **1スライド・1メッセージ・1チャート**を原則とする。
2. Messageは、その1枚だけを見ても「何を主張するスライドか」が一文で分かるようにする。
3. ChartはMessageを説明・論証する**スライド上の主たる視覚表現**とする。
4. Chartは狭義の統計グラフに限定しない。Diagram、Table、Process、Comparison、Matrix、Flow等を含む。
5. 1枚の中に複数の独立した主図・独立した主張を同居させない。
6. Chart Structureは、ChartをPowerPoint上でどう配置し、どの順序で読み、何を強調するかを定義する。
7. `Chart内の最小表示テキスト` は、実際のPowerPoint上に置く文言を必要最小限まで圧縮する。Supporting Logicをそのまま転載しない。
8. Supporting Logicは、MessageとChartを成立させる論拠・前提・詳細情報を保持する。原則として全量をPowerPoint上に掲載しない。
9. Supporting LogicがMessageとは別の新しい主張を追加してはならない。
10. Speaker Noteは、スライド上へ載せると情報過多になる説明を口頭で補うために用いる。
11. 技術用語・アルゴリズム名の羅列より、顧客の業務課題・Decision・Action・期待効果との接続を優先する。
12. PredictiveとCausalの意味論を混同しない。高い予測性能やExplainabilityを因果効果と解釈しない。
13. 因果推論では、Causal Question / Estimand / Assumptions / Identification / Estimation / Diagnostics / Sensitivityを必要に応じて区別する。
14. 根拠のない精度、効果率、削減率、ROI等の数値を置かない。
15. PoCの成功を「モデルが作れた」「有意差が出た」と定義せず、業務上の判断可能性、科学的・統計的妥当性、次フェーズ判断まで含めて考える。
16. 当該スライドを改善するために他スライドの変更が必要と判断した場合、勝手に変更せず `Cross-slide suggestion` として明示する。

## 0.5. スライドMarkdown標準構造

スライドMarkdownの標準構造は、`../slide_skelton_structure.md` を正本とする。

本READMEでは標準テンプレート・見出し番号ルールを重複保持しない。構造に関する判断が必要な場合は、必ず `slide_skelton_structure.md` を参照する。

## 0.6. 各構成要素の用語定義

Message、Chart、Chart Structure、Chart内の最小表示テキスト、Supporting Logic、Speaker Note、Transitionの定義は、`../slide_skelton_structure.md` を正本とする。

本READMEでは各構成要素の定義を重複保持しない。各スライドのMessage / Chart等を作成・修正する際は、`slide_skelton_structure.md` に定義されたAudience / Purposeと用語定義に従う。

## 0.7. ブラッシュアップ時の評価基準

対象スライドをブラッシュアップする際は、少なくとも以下を評価する。

| 評価軸 | 確認事項 |
|---|---|
| **Message** | 一意か。トピック名ではなく主張になっているか。その1枚だけで意味が分かるか。 |
| **Logic** | Messageを支える論理が過不足なく整理されているか。並列・因果・時系列等の関係を混同していないか。 |
| **Chart** | 一つの主たる視覚構造でMessageを説明・論証できるか。複数の独立した主図に分裂していないか。 |
| **Chart Structure** | 読み順、要素間関係、入力 / 出力、強調点、PowerPoint上の配置が明確か。 |
| **Chart内の最小表示テキスト** | PowerPoint上に必要な情報へ十分圧縮されているか。詳細ロジックを転載していないか。 |
| **Supporting Logic** | MessageとChartを成立させる論拠・前提が十分か。第二のMessageを生んでいないか。 |
| **Scientific validity** | Predictive / Causalの用語、前提、評価軸、主張可能範囲に誤りや過剰主張がないか。 |
| **Business linkage** | 分析がどのDecision / Action / 期待効果へ接続するかが分かるか。 |
| **Deck coherence** | 前後スライドと重複せず、30枚のストーリー上で固有の役割を持っているか。 |
| **Speaker Note** | スライド上に載せない補足情報として適切か。新しい主張を追加していないか。 |
| **PowerPoint readiness** | 実際のPowerPointへ変換するとき、何を配置し何を削るか判断できる状態か。 |
| **Transition** | 次スライドへ進む必然性が説明でき、論理の飛躍がないか。 |

ブラッシュアップでは、文章を増やすこと自体を目的としない。Messageの明確性、Chartの説明力、Scientific / Business上の妥当性を高める方向で編集する。

## 0.8. Scientific / Business上の制約

### 0.8.1. Predictiveに関する制約

- Predictive analysisの目的は、未知・将来のOutcomeに対する予測性能を評価し、業務上の判断へ利用することである。
- In-sample fitとout-of-sample predictive performanceを混同しない。
- Target leakage、data leakage、時系列の未来情報混入を許容しない。
- Accuracy等の単一指標だけでモデル価値を判断しない。
- 必要に応じてCalibration、Precision / Recall、error pattern、segment別性能、業務コスト等を併せて評価する。
- Feature importance、SHAP、PDP / ICE等のPredictive explanationをcausal effectとして解釈しない。
- 「高い予測精度が得られた」ことから「その変数へ介入すればOutcomeが変わる」と結論しない。
- モデル性能が高くても、結果を利用するDecision / Actionが存在しなければ業務価値は限定される。

### 0.8.2. Causalに関する制約

- Causal analysisでは、単なるassociationやpredictionとcausal effectを区別する。
- Causal QuestionをTreatment、Outcome、Population、comparison / intervention等まで具体化する。
- 必要に応じてEstimandを明示する。
- 因果推論では、推定器の選択より前にAssumptionsとIdentification Strategyを検討する。
- IdentificationとEstimationを別の科学的問題として扱う。
- Confounder、Mediator、Collider等の役割を無批判に同列化しない。
- 観測データから因果効果を推定する場合、必要な識別仮定があることを明示する。
- Diagnostics、Refutation、Sensitivityは、Effect Estimateとは別に結果の信頼可能範囲を評価する役割を持つ。
- 統計的有意差のみをPoC成功条件にしない。
- 未観測交絡等により主張できない場合は、「言えないこと」を明示する。

### 0.8.3. Business / PoCに関する制約

- 分析手法の適用そのものをPoCの最終目的にしない。
- PoC開始時にBusiness Question、Decision / Action、利用可能データ、Success Criteriaを可能な範囲で合意する。
- PoC終了時には、分析結果に加えて、利用条件、限界、追加データ・追加検証の必要性、本番化 / 追加PoC / 中止等の次フェーズ判断を整理する。
- 「精度が高い」「効果がある」等の分析上の結果と、売上向上・コスト削減等のBusiness Outcomeを直接同一視しない。
- 根拠のないROI、削減率、改善率、精度目標等を作らない。
- 期待効果は、分析結果からDecision / Actionが変わり、その結果としてBusiness Outcomeへ接続する因果鎖を意識して記述する。
- 実際の業務制約、利用者、利用タイミング、誤判定コスト、運用負荷等を無視した提案にしない。

### 0.8.4. Ariadneに関する制約

- 分析サービスの基本は、データサイエンティストによる分析設計・スクラッチ実装である。
- AriadneをすべてのPoCで使用する前提にしない。
- Ariadneは、Research Context、分析条件、実行、結果、判断理由、Lineage等を構造化・追跡する補助的な選択肢として位置づける。
- Ariadneの現行コードベースで未実装の機能を、既存Capabilityとして断定しない。
- 成熟したOSSや既存分析基盤と競合する独自アルゴリズム群としてAriadneを説明しない。
- Ariadneの説明を追加する場合は、要件定義 / 設計とコードベースの双方との整合を確認する。

## 0.9. Cross-slide suggestionルール

### 0.9.1. 基本原則

個別スライドのブラッシュアップスレッドでは、**対象 `[Section]-[Subsection]_[SLUG].md` のみを直接修正対象**とする。

他スライドの変更が望ましいと判断しても、その場で他スライド内容を勝手に書き換えない。

### 0.9.2. Cross-slide suggestionを出す条件

以下のいずれかに該当する場合のみ、Cross-slide suggestionを提示する。

- 対象スライドと前後スライドでMessageが重複している。
- 対象スライドを改善すると、前後スライドとの論理接続が破綻する。
- 本来別スライドで扱うべき論点が対象スライドへ混入している。
- Scientific / Business上の重要な前提を別スライドで明示しないと誤解が生じる。
- Deck全体のストーリー変更が必要なほど重要な問題を発見した。

単なる好み、表現統一、軽微な文言修正のためにCross-slide suggestionを乱発しない。

### 0.9.3. 出力形式

必要な場合、対象スライドの修正版とは分離して、以下の形式で記載する。

```markdown
## Cross-slide suggestion

### 対象

- Slide XX｜[タイトル]

### 提案

- [必要な変更内容]

### 理由

- [対象スライドとの重複、論理接続、Scientific / Business上の理由]

### 影響

- [変更しない場合に残る問題]
```

Cross-slide suggestionは**提案**であり、そのスレッドでは対象外スライドを変更しない。

### 0.9.4. 独立スレッドでの推奨指示

新しいChatGPTスレッドでは、以下の3ファイルを添付する。

1. `00_README_handoff.md`
2. `slide_skelton_structure.md`
3. 対象の `[Section]-[Subsection]_[SLUG].md`

依頼文は、例えば以下とする。

> `00_README_handoff.md` を資料全体・共通ルールのauthority、`slide_skelton_structure.md` をスライドMarkdown標準構造・構成要素定義・Audience / Purposeのauthorityとして参照し、添付した `[Section]-[Subsection]_[SLUG].md` を対象スライドとしてブラッシュアップせよ。Message / Chart / Chart Structure / Chart内の最小表示テキスト / Supporting Logic / Speaker Note / Transitionを一貫させること。他スライド変更が必要な場合は、直接変更せずCross-slide suggestionとして示すこと。
