# Section 03 Story｜PoC共通プロセスとSuccess Criteria

## Polaris

**PoCは、Decisionと利用ルールを定義する業務設計から、Data Assessment・Analysis Design・Execution・Validation / Interpretationによる分析検証を経て、EvidenceをDecision / ActionとNext Phaseへ戻す一連のプロセスである。開始時にはQuestion / Scope・Decision / Action・Data・Success Criteriaを合意し、新事実・制約で変更が必要な場合のみ理由・新基準・妥当性を説明して再合意し、最終合意基準でExit判断する。**

## このセクションの役割

- Section 02で定義したDecision、Required Evidence、Analysis Question、利用ルールをPoC全体の工程へ配置する。
- 分析工程だけを切り離さず、`業務設計 → 分析検証 → 業務接続` を一つのPoCとして扱う。
- PoC開始時の合意事項と、終了時の判断軸をStart Gate / Exit Gateとして明確にする。
- PoC中に新しい事実や制約が判明した場合のScope / Success Criteria変更を、透明な再合意プロセスとして扱う。

## Storyline

1. **PoCは、業務から始まり業務へ戻る。**
   - **業務設計**：Business Question / Decision → Required Evidence / Analysis Question → 利用ルール。
   - **分析検証**：Data Assessment → Analysis Design → Execution → Validation / Interpretation。
   - **業務接続**：EvidenceをDecision / Actionへ利用 → Next Phaseを判断。
   - 共通メッセージは **業務 → 分析 → 業務を一つのPoCとして接続する** ことである。

2. **入口と出口のDecisionは役割が異なる。**
   - 入口のDecision：何の判断に必要なEvidenceを作るかを決める設計アンカー。
   - 出口のDecision / Action：検証で得たEvidenceを、最初に定義した利用先へ戻して実際の判断を行う工程。
   - この構造により、Model / Effect Estimateの作成だけが独立した成果になることを防ぐ。

3. **Start Gateでは、PoC開始前に4項目を合意する。**
   - **Question / Scope**：Business Question、Analysis Question、対象・期間等。
   - **Decision / Action**：WHO / WHEN / Decision Rule / Actionを含む利用仮説。
   - **Data**：所在、利用可否、対象期間、粒度、主要な不足・制約の初期確認。
   - **Success Criteria**：分析成立性、業務利用性、次フェーズ判断の判定基準。
   - Success Criteriaは「高精度が出る」「有意な効果が出る」と約束する目標値ではなく、Evidenceを見て何を判断するかの基準である。

4. **PoCは必要に応じて反復するが、場当たり的には変えない。**
   - Data Assessmentでデータ不足が判明した場合、Question / Scopeへ戻ることがある。
   - Validationで性能不足、Identification上の問題、Assumption違反等が判明した場合、Data / Design / Questionを追加検討することがある。
   - ただし、結果が期待値に届かなかったことだけを理由に事後的に基準を緩めない。
   - 新事実・制約によって当初ゴールの妥当性や実行可能性が変わった場合のみ、**変更理由 → 新ゴール / Success Criteria → 妥当性 → Stakeholder再合意**を明示する。

5. **Exit Gateでは、最終合意済み基準へEvidenceを照合する。**
   - **分析成立性**：問いへ妥当に答えられたか。再現性・前提・不確実性・限界を含めて判断する。
   - **業務利用性**：Decision / Actionの判断材料として利用できるか。
   - **Next Phase**：本番化 / 追加検証 / Data Acquisition / Scope変更 / 中止等を選ぶ。
   - Goだけを成功とせず、Additional ValidationやNo-Goも不確実性を減らした合理的な判断になり得る。

## Must Keep｜編集で崩してはいけない境界

- Predictive / Causalは共通のPoC運営骨格を持つが、Analysis DesignやValidationの科学的中身は同一ではない。
- Success Criteriaは「固定不変」でも「結果に合わせて自由に変更可能」でもない。変更には新事実・制約と再合意が必要である。
- Start GateのData確認を、詳細なData Assessmentが完了済みという意味にしない。
- Exit Gateを単一の精度指標、統計的有意差、Effect Estimateだけで判定しない。
- PoCの出口を本番化だけに限定しない。追加検証・データ取得・Scope変更・中止を正当な選択肢として保持する。
- 反復する場合も、変更理由・前提・判断を記録し、検証解釈を保つ。

## Slide Mapping

| Slide | Story上の役割 | Core Claim |
|---|---|---|
| 03-01 | PoC共通プロセス | 業務設計から分析検証を経て業務判断へ戻るまでを一つのPoCとする |
| 03-02 | Start / Exit Gate | 成功基準を合意して開始し、新事実による変更は根拠を示して再合意する |

## 編集時の判断基準

- `業務設計 → 分析検証 → 業務接続` の3フェーズを主構造として崩さない。
- Start Gate / Exit Gateは、工程の説明ではなく「何を合意し、何で判断するか」というガバナンスとして扱う。
- Predictive / Causal固有のWorkflow詳細をこのセクションへ詰め込まず、Section 04 / 05へ分離する。
- 新しいSuccess Criteriaを追加する場合は、分析成立性・業務利用性・次フェーズ判断のどこを判定するものかを明示する。

## Section Transition

**PoC共通の進め方と判断ガバナンスを定義した後は、それをPredictive / Causalそれぞれの科学的Workflowへ具体化する。Section 04では、未知・将来OutcomeをDecision時点の情報から予測し、事前Actionへ利用するPredictive PoCを扱う。**
