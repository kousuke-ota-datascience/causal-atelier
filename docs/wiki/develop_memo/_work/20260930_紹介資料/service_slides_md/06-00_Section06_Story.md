# Section 06 Story｜分析実装方針とAriadne

## Polaris

**サービスの分析品質を担う主体はData Scientistであり、案件固有のQuestion・Design・Validation・InterpretationをScratch +成熟OSSで実装する。Ariadneはそれらを置き換える製品ではなく、必要に応じてContext / Workflow / Result / Lineageを構造化・追跡し、再現性と案件運営を補助する層としてCustomer Data / Compute環境と併存する。**

## このセクションの役割

- Section 04 / 05で示したPredictive / Causal Workflowを、サービスとしてどのような実装方針で提供するかを明確にする。
- 分析の主体をData Scientistに置き、特定Productや独自Algorithmをサービス価値の中心にしない。
- Scratch + OSSとAriadneの役割を分離し、AriadneをPoC成立の前提や分析Engineそのものとして誤認させない。
- 後続の具体例で、ここまで説明した設計思想が実際のPoC Storyへどう落ちるかを示す準備をする。

## Storyline

1. **分析品質の中心はData Scientistによる設計・検証・解釈である。**
   - Business / Analysis Questionの定義。
   - Predictive / Causalに応じたAnalysis Design。
   - Validation、Diagnostics、Error / Sensitivity Analysis。
   - 結果のInterpretationとDecision / Actionへの接続。
   - 差別化の中心はAlgorithm数ではなく、問い・前提・手法・検証・解釈を一貫して設計できるData Science Capabilityに置く。

2. **案件固有要件にはScratch +成熟OSSで柔軟に対応する。**
   - Python等を用いたScratch Developmentを基本とし、成熟したML / Statistical / Causal Libraryを目的に応じて組み合わせる。
   - 特定Product、単一Model Family、固定Workflowへ顧客課題を合わせない。
   - Data Structure、Outcome / Treatment、Evaluation、運用制約等に応じて必要な実装を構成する。

3. **Ariadneは分析Workflowを補助する層として位置づける。**
   - Research / Analysis Contextの構造化。
   - Versioned Input、Workflow、Resultの追跡。
   - Predictive / Causalの分析過程やLineageの整理。
   - Data ScientistのQuestion Definition、Scientific Design、Interpretationを自動的に代替するものではない。

4. **Ariadne利用はPoC成立の前提ではない。**
   - 案件・Customer環境に応じて利用する選択肢とする。
   - お客様の既存Data / Compute環境と併存可能な構成とする。
   - Ariadneの現時点の実装範囲と、サービスとしてScratchで対応可能な分析範囲を混同しない。

## Must Keep｜編集で崩してはいけない境界

- Ariadneをサービスそのもの、分析者の代替、またはPoC実施の必須条件として表現しない。
- 現在Ariadneに実装されているModel / Workflow数を、サービスの分析対応範囲と同一視しない。
- 「独自Algorithmが多いこと」を主要なWhy Usにしない。主要価値はQuestion / Design / Validation / Interpretationの一貫性に置く。
- OSS利用を単なるLibrary列挙にしない。案件の問いと成立条件に応じて選択する実装手段として扱う。
- Customer Data / Compute環境を置き換える前提にせず、既存基盤と併存する位置づけを保持する。

## Slide Mapping

| Slide | Story上の役割 | Core Claim |
|---|---|---|
| 06-01 | 実装方針 / Ariadne | Data Scientist + Scratch / OSSを分析実装の中心とし、AriadneはContext / Workflow / Result / Lineage追跡を補助する |

## 編集時の判断基準

- 主語は原則としてData Scientist / Analysis Serviceとし、Ariadneを主役へ反転させない。
- 新しいAriadne機能を記載する場合も、それがどの分析Context / Workflow / Result / Lineage管理を支援するかを明確にする。
- 技術Stackを追加する場合は「なぜその技術を採用するか」がQuestion / Data / Validation / Enterprise Constraintへ接続することを確認する。

## Section Transition

**実装方針を示した後は、ここまでの抽象的な設計原則を具体的なPoC Storyで確認する。Section 07では、PredictiveとCausalを同じレイアウト系統で並べ、Business QuestionからAnalysis、Decision / Actionまでの違いと共通点を具体化する。**
