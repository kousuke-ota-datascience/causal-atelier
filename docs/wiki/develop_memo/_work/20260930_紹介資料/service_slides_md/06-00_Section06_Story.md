# Section 06 Story｜分析実装方針とAriadne

## Polaris

**サービスの分析品質を担う主体はData Scientistであり、案件固有のQuestion・Design・Validation・InterpretationをScratch＋成熟OSSで実装する。Ariadneは分析EngineやPoC成立の前提ではなく、必要に応じてContext / Input・条件 / Execution / Result / 判断 / Lineageを構造化・追跡し、分析過程の再現・比較・根拠確認を補助する選択肢として位置づける。**

## このセクションの役割

- Section 04 / 05で示したPredictive / Causal WorkflowとEvidenceを、サービスとしてどのような実装方針で作成・管理するかを明確にする。
- 分析の主体をData Scientistに置き、特定Productや独自Algorithmをサービス価値の中心にしない。
- Scratch＋成熟OSSとAriadneの責務を分離し、AriadneをPoC成立の前提、分析者の代替、または分析Engineそのものとして誤認させない。
- Section 07の具体例へ進む前に、「Questionに合わせて分析を設計・実装し、EvidenceをDecision / Actionへ接続する」という実装上の共通方針を固定する。

## Section Entry｜Section 05からの接続

Section 04ではPredictive PoCのEvidence Package、Section 05ではCausal PoCのEvidence Stackを定義し、Model / Estimate単体ではなく成立条件・検証結果・限界まで含めてNext Phaseを判断することを示した。

Section 06では、**それらのEvidenceを誰が、何を使って作り、Ariadneがどこを補助するのか**を一枚で整理する。

## Storyline

1. **分析品質の中心はData Scientistによる設計・検証・解釈である。**
   - Business / Analysis Questionを定義する。
   - Predictive / Causalに応じてAnalysis Designと成立条件を設計する。
   - Validation、Diagnostics、Error / Sensitivity Analysisを行う。
   - 結果をInterpretし、Decision / Actionへ接続する。
   - 差別化の中心はAlgorithm数ではなく、問い・前提・手法・検証・解釈を一貫して設計できるData Science Capabilityに置く。

2. **案件固有要件にはScratch＋成熟OSSで柔軟に対応する。**
   - Python等を用いたScratch Developmentを基本とし、成熟したML / Statistical / Causal Libraryを目的に応じて組み合わせる。
   - 特定Product、単一Model Family、固定Workflowへ顧客課題を合わせない。
   - Data Structure、Outcome / Treatment、Evaluation、運用制約等に応じて必要な実装を構成する。

3. **Ariadneは分析過程の構造化・追跡を補助する選択肢である。**
   - Research / Analysis Contextを構造化する。
   - Versioned Input、Analysis Specification、Execution、Result / Artifact、判断・Annotation、Lineageを関連づけて扱う。
   - 分析結果の再現、比較、根拠確認、改訂、後続分析への引継ぎを支えるための情報を保持する方向性を持つ。
   - 現行要件には実装状態が `PARTIAL` の追跡・再現性項目もあるため、完全な再現性や自動化を既存機能として断定しない。
   - Data ScientistのQuestion Definition、Scientific Design、Validation、Interpretationを自動的に代替するものではない。

4. **Ariadne利用はPoC成立の前提ではなく、サービスScopeとも分離する。**
   - 案件・Customer環境に応じて利用する選択肢とする。
   - お客様の既存Data / Compute環境を置き換える前提にせず、併存する位置づけとする。
   - Ariadneの現時点の実装範囲と、サービスとしてScratch＋成熟OSSで対応可能な分析範囲を混同しない。
   - Ariadne内のModel / Workflow数を当チームの対応範囲や主要なWhy Usとして扱わない。

## Must Keep｜編集で崩してはいけない境界

- Ariadneをサービスそのもの、分析者の代替、またはPoC実施の必須条件として表現しない。
- 現在Ariadneに実装されているModel / Workflow数を、サービスの分析対応範囲と同一視しない。
- 要件として定義されていても `PARTIAL` / `NOT_IMPLEMENTED` の機能を、現行実装で完全に提供済みと断定しない。
- 「独自Algorithmが多いこと」を主要なWhy Usにしない。主要価値はQuestion / Design / Validation / Interpretationの一貫性に置く。
- OSS利用を単なるLibrary列挙にしない。案件の問いと成立条件に応じて選択する実装手段として扱う。
- Customer Data / Compute環境を置き換える前提にせず、既存基盤と併存する位置づけを保持する。
- Section 07で具体的なUse Caseを扱うため、このSectionでは解約・故障等の特定Domain例を主役にしない。

## Slide Mapping

| File | Deck Slide | Story上の役割 | Core Claim |
|---|---:|---|---|
| 06-01 | 28 | 実装方針 / Ariadne | Data ScientistがScratch＋成熟OSSで分析を実装し、Ariadneは分析過程の構造化・追跡を補助する |

## 編集時の判断基準

- 主語は原則としてData Scientist / Analysis Serviceとし、Ariadneを主役へ反転させない。
- ChartではData Scientist＝主体、Scratch＋成熟OSS＝実装手段、Ariadne＝任意の補助手段、お客様のData / Compute環境＝既存基盤という責務差を視覚的に崩さない。
- 新しいAriadne機能を記載する場合は、要件定義上のRequirementだけでなくImplementation Statusと現行コードを確認し、未実装機能を既存Capabilityとして断定しない。
- 技術Stackを追加する場合は「なぜその技術を採用するか」がQuestion / Data / Validation / Enterprise Constraintへ接続することを確認する。
- 一枚の役割は実装方針とAriadneの位置づけの境界整理に限定し、具体Use CaseやAlgorithm catalogを追加して第二のMessageを作らない。

## Section Transition

**実装の主体・手段・補助手段を分けた後は、その方針が実際のPoC Storyへどう落ちるかを確認する。Section 07では、PredictiveとCausalを同じレイアウト系統で並べ、Business QuestionからAnalysis、Decision / Actionまでの共通点と、Analysis Question / Evidenceの違いを具体化する。**
