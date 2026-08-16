# Workflow Template 設計思想 Handoff — 統合版

## 0. 結論

Workflow Template の目的は、**workflow 自体を厳密に運用・証明することではない**。

本来の目的は、

- 設計・実装・テストを分離する
- 各エージェントへ必要十分なコンテキストだけを与える
- コーディングエージェントに不要な探索をさせない
- ファイルを介して工程間の引き継ぎと追跡性を確保する
- Requirements を現行仕様の正本とする
- Requirement → Design → Code → Test の変更理由を追跡可能にする
- Gate 単位で意味のあるコード変更成果の品質を保証する
- Work Package により大きな Gate をエージェントが迷わず実装できるサイズへ分割する

ことである。

ENH-E7 の運用では、これらを支えるための仕組みが次第に、

- SHA の完全一致
- placeholder の文字列レベルでの禁止
- status 値の完全一致
- Work Package ごとの過剰な状態管理
- instruction と preflight 間の厳密な private protocol
- 非本質的不整合による Hard Fail

へ発展し、**成果物の品質を守るための workflow が、それ自体を新しい failure point にする状態**が見られた。

今後は、厳密性そのものではなく、

> **正しい作業を、少ない探索と手戻りで、追跡可能かつ十分な品質で遂行できること**

を最優先とする。

---

# 1. Workflow Template の基本目的

Workflow Template は、主として以下の4つを実現するための開発補助システムである。

## 1.1 Context Management

エージェントへ必要十分な情報だけを渡し、不要な探索・推論・トークン消費を減らす。

## 1.2 Separation of Concerns

Requirements、Design、Implementation、Test の責務を分離する。

## 1.3 Traceability

Requirement から Design、Code、Test に至る変更理由を後から追跡できるようにする。

## 1.4 Staged Quality Assurance

意味のあるコード変更成果単位で品質を確認する。

したがって Workflow Template は、

> **Context Management を中心に、Traceability と Staged Quality Assurance を組み合わせた開発 workflow**

として位置付ける。

---

# 2. 設計・実装・テストを分離する

## 2.1 基本思想

工程を以下のように分ける。

```text
Requirements
    ↓
Design
    ↓
Implementation
    ↓
Test
```

目的は、各エージェントの責務と必要コンテキストを限定することである。

### Design Agent

- Requirements を読み取る
- 変更方針・構造・実装境界を決める
- coding agent が再設計しなくて済む状態まで具体化する

### Coding Agent

- 与えられた設計・Work Package に従って実装する
- Requirements や過去議論を広範囲に再探索しない

### Test Agent

- Gate / Enhancement が要求成果を満たすことを検証する
- 実装者の設計判断を無条件に前提としない

---

# 3. Minimum Sufficient Context

## 3.1 トークン削減は結果であって最上位目的ではない

目指すべき状態は、

```text
Minimum Context
```

ではなく、

```text
Minimum Sufficient Context
```

である。

必要な情報まで削ると、

- 再探索
- 誤解
- 推測による補完
- 誤実装
- 修正作業

が増え、結果的にトークンも時間も余計に消費する。

## 3.2 Coding Agent に事前に与えるべき情報

原則として以下を明示する。

- 何を変更するか
- なぜ変更するか
- どこを変更するか
- 何を変更してはいけないか
- 前提となる成果物
- 依存関係
- 完了条件
- 必要な局所検証

Coding Agent 自身に、これらをシステム全体から発見させない。

---

# 4. No Unnecessary Exploration

Coding Agent に以下を極力させない。

- Requirements の所在探索
- 過去 Enhancement の横断検索
- 設計判断の再構築
- 変更対象の推測
- 作業範囲の自己定義
- Workflow のルール自体の解読

狙いは以下である。

```text
探索量低減
    ↓
irrelevant context 低減
    ↓
判断のブレ低減
    ↓
誤実装低減
    ↓
コード品質向上
```

Workflow を理解すること自体が Coding Agent の主要作業になった場合、設計思想から逸脱している。

---

# 5. Artifact-based Handoff

## 5.1 ファイルを工程間の契約とする

Agent 間、Work Package 間、Gate 間は、可能な限り永続成果物ファイルを介して引き継ぐ。

```text
前工程
   ↓
Artifact
   ↓
次工程
```

これにより、

- chat 履歴への依存低減
- 再実行可能性
- Agent 交代への耐性
- 人間による途中確認
- 判断履歴の追跡

を実現する。

## 5.2 ファイルが存在するだけでは Traceability ではない

重要なのは成果物間の関係である。

```text
Requirement
    ↓
Design Decision
    ↓
Gate / Work Package
    ↓
Code Change
    ↓
Test
```

必要に応じて、

```text
REQ-E7-XXX
    ↓
DD-E7-XXX
    ↓
G01 / P03
    ↓
Implementation
    ↓
TEST-E7-XXX
```

のように追跡できる状態を目指す。

ただし、Traceability のためだけに無意味な中間ファイルを大量生成しない。

---

# 6. Requirements を現行仕様の正本とする

## 6.1 Canonical Requirements

現在のシステムが、

> 何を満たすべきか

については Requirements を正本とする。

コードや現在の画面挙動を正本にしない。

これにより、

> 「現在そう動いているから、それが仕様」

という仕様と実装の逆転を防ぐ。

また、初見の人間・Agent がコードを逆解析しなくても、

- システムの目的
- 主要概念
- 制約
- 期待動作

を理解できる状態を維持する。

---

# 7. Requirements と Design を混同しない

Requirements が正本だからといって、全情報を Requirements へ集約しない。

責務は以下のように分離する。

```text
Requirements
「何を満たすべきか」
        ↓
Architecture / Basic Design
「どういう構造で満たすか」
        ↓
Detailed Design
「今回の変更をどう実現するか」
        ↓
Code
```

Requirements は、

- system behavior
- concepts
- constraints
- externally meaningful expectations

の正本とする。

局所的な実装判断やコード詳細は Design 側へ置く。

---

# 8. Enhancement の変更理由を一発で追跡できるようにする

Enhancement ごとに以下を追跡できるようにする。

- 何を変えたのか
- なぜ変えたのか
- Requirements のどこが変わったのか
- Requirements 差分から何を設計したのか
- その設計から何を実装したのか
- どの Test で保証したのか

理想構造：

```text
Requirements Delta
       ↓
Design Delta
       ↓
Implementation Plan
       ↓
Gate / Work Package
       ↓
Code
       ↓
Test Result
```

最終コードだけではなく、

> なぜそのコードになったか

を再構築できることを重視する。

---

# 9. Enhancement 完了後は Canonical Requirements へ統合する

Enhancement 文書を永久に積み重ね、現行仕様を理解するために過去 Enhancement をすべて読む必要がある状態にはしない。

望ましい構造：

```text
Canonical Requirements vN
        ↓
Enhancement Delta
        ↓
Design / Implementation / Test
        ↓
Canonical Requirements vN+1
```

役割を分ける。

- **Enhancement 文書**：変更過程・判断履歴
- **Canonical Requirements**：現在の完成状態

---

# 10. Gate の設計思想

## 10.1 Gate はコード成果の品質保証境界

Gate は、

> **意味のあるコード改変成果について品質を保証する単位**

である。

```text
Gate
├─ 意味のある変更成果
├─ Implementation
└─ Gate-level Test
```

単なる工程管理単位ではない。

## 10.2 Gate 単位で Test を実施する

各 Gate では、その Gate が提供すべき成果について正式な Test を行う。

ただし、

```text
G01 PASS
G02 PASS
G03 PASS
```

だからといって、

```text
G01 + G02 + G03
```

が正常とは限らない。

そのため Enhancement 完了時には別途、

- cross-gate integration
- regression
- Enhancement-level acceptance

を確認する。

---

# 11. Work Package の設計思想

## 11.1 Primary Purpose

Work Package は、

> **1 Gate の作業量が大きすぎる場合、Coding Agent が迷わず実装できるサイズへ分割するためのもの**

である。

```text
Gate G01
├─ P01
├─ P02
└─ P03
```

主目的は、

- coding scope の局所化
- 認知負荷低減
- 不要探索の抑制

である。

## 11.2 Secondary Benefits

副次的には、

- 依存関係明示
- 変更対象ファイル局所化
- 再実行範囲縮小
- Agent 分割・並列化

にも利用できる。

ただし、これらを目的化して Work Package 管理そのものを肥大化させない。

---

# 12. Work Package は Gate と同じ品質保証境界ではない

Work Package ごとに局所的 self-check は必要である。

しかし、Gate と同等の acceptance process を要求する必要はない。

```text
Work Package
    ↓
局所実装 + self-check

Gate
    ↓
変更成果単位の正式 Test

Enhancement
    ↓
Integration / Regression
```

Work Package に、

- 過剰な checkpoint
- 厳密な状態遷移
- SHA 固定
- package ごとの承認
- package ごとの完全な品質証明

を要求すると、元々の「Agent を迷わせない」という目的と逆行する。

---

# 13. Hard Constraint と Diagnostic Information を分離する

Workflow 上の不一致をすべて FAIL にしない。

基本的に以下を区別する。

```text
FAIL
WARN
INFO
```

## 13.1 FAIL

作業継続すると、実際に誤実装・誤検証・対象誤認などにつながるもの。

例：

- 必須入力成果物が存在しない
- Gate / Work Package が特定できない
- 変更対象が一意でない
- 必須依存成果が未完了
- 実行値として使用される placeholder が未解決
- 実装対象を誤る危険がある
- 安全に作業を開始するための必須情報がない

## 13.2 WARN

確認は必要だが、ただちに作業停止する理由にはならないもの。

例：

- Planning 時点から Git SHA が変化
- optional metadata 欠落
- workspace に非本質的差分がある
- 推奨命名と異なる
- status 表現に軽微な不整合がある

## 13.3 INFO

診断・追跡上便利だが、実行可否に関係しない情報。

---

# 14. SHA の扱い

SHA を記録すること自体には意味がある。

主用途：

> 「この計画・実装・テスト結果が、どのコード状態に対するものか」

を追跡すること。

しかし、

```text
SHA mismatch
    ↓
即 FAIL
```

とはしない。

本当に確認すべきなのは、

> 前工程が前提としたコード状態から、今回の作業前提を壊す meaningful change が入ったか

である。

望ましい考え方：

```text
SHA mismatch
    ↓
meaningful diff check
    ↓
PASS / WARN / FAIL
```

SHA は証跡であって、原則として作業を停止させるための絶対ロックではない。

---

# 15. Placeholder の扱い

Placeholder の文字列自体を全面禁止しない。

防ぐべきものは、

> 未解決 placeholder が実際の実行値として使われること

である。

例えば、

```text
PACKAGE_ID=<PACKAGE_ID>
```

が runtime input に残っていれば FAIL。

一方、

```text
Example:
PACKAGE_ID=<PACKAGE_ID>
```

は説明用なので問題ない。

文字列一致ではなく、**意味論と利用位置**を評価する。

---

# 16. Status 管理の問題

ENH-E7 では、`READY_TO_EXECUTE` などの status 値が想定値と異なるだけで処理が停止する事例が散見された。

これは重要な設計上の問題である。

## 16.1 問題の本質

例えば以下は意味的には近い。

```text
READY
READY_TO_EXECUTE
READY_FOR_EXECUTION
EXECUTION_READY
```

しかし consumer が、

```text
status == "READY_TO_EXECUTE"
```

という完全一致を要求すると、

```text
成果物あり
依存関係OK
対象一意
作業可能
    +
status文字列だけ違う
        ↓
FAIL
```

となる。

これは品質上の failure ではなく、**protocol conformity failure** である。

結果として、

```text
instruction 作成上の軽微な不備
        ↓
preflight FAIL
        ↓
人間が instruction 修正
        ↓
再実行
        ↓
本来不要な手戻り
```

が発生する。

今回の運用では、こうした手戻りの影響が、厳密な status 管理によって回避できるリスクより大きくなっている。

---

# 17. Declared State より Derived State を優先する

重要な状態は、可能な限り instruction に「宣言させる」のではなく、実際の成果物・依存関係から導出する。

## 悪い例

```text
Status: READY_TO_EXECUTE
```

がなければ実行不可。

## 望ましい例

```text
required artifacts exist?
        +
dependencies satisfied?
        +
execution target resolved?
        +
blocking condition absent?
        ↓
READY
```

つまり、

> **READY_TO_EXECUTE は入力値ではなく検査結果として導出する**

方が堅牢である。

---

# 18. Status の種類を整理する

Status を使う場合は、役割を混同しない。

## 18.1 Human-readable Status

人間向け説明。

```text
Status: Ready to execute
```

Workflow 制御の絶対条件には使わない。

## 18.2 Machine Control State

どうしても必要な場合のみ、enum を極小化する。

例：

```text
BLOCKED
READY
DONE
```

可能な限り実際の状態から導出する。

## 18.3 Diagnostic Metadata

例：

```text
PLANNED
REVIEWED
CHECKPOINTED
```

主として INFO / WARN 用途とし、安易に execution blocker にしない。

---

# 19. Robustness over Protocol Exactness

Workflow は、非本質的な表記差異に対して堅牢であるべき。

原則：

> **意味的に同一な状態を、文字列・命名・metadata の差だけで FAIL させない。**

特に自然言語 Agent が生成する instruction と、machine validator の間で厳密な private protocol を多数設けると、

```text
Planning Agent
    ↓
instruction
    ↓
parser / validator
    ↓
preflight
    ↓
Coding Agent
```

の各境界が新たな failure point になる。

Workflow の層を増やすほど自動的に安全になるわけではない。

---

# 20. Instruction-generated Protocol を最小化する

自然言語 Agent に、machine-readable protocol の完全な生成責任を負わせない。

例えば、

- exact status literal
- exact placeholder syntax
- exact checkpoint state
- exact SHA field
- exact metadata combination

を複数同時に要求すると、instruction generator の小さなミスが execution blocker になる。

Workflow が要求する machine contract は、

- 少数
- 明示的
- 単純
- 安定的

であるべき。

可能なら downstream 側が既存成果物から状態を導出する。

---

# 21. False Positive Failure を重視する

従来は、

> 危険な状態を見逃す

false negative を防ぐ方向へ強く寄っていた。

しかし、ENH-E7 では、

> 本当は実行可能なのに workflow が停止させる

false positive のコストが顕在化した。

False positive は、

- instruction 修正
- prompt 再実行
- context 再構築
- Agent の再探索
- 人間による原因調査
- 開発フロー中断

につながる。

したがって、Hard Fail 判定では両方のコストを見る。

```text
誤って通すリスク
vs
誤って止めるリスク
```

厳密さだけを最大化しない。

---

# 22. Preflight の役割

Preflight は、

> **Coding Agent が安全かつ迷わず作業を開始できる状態か**

を確認するためのもの。

Workflow 自身の完全性を証明するシステムではない。

原則として確認するもの：

- 必須入力が存在する
- runtime identity が解決している
- Gate / Package が一意に特定できる
- 必須依存成果が揃っている
- 作業範囲が十分明確
- blocking condition がない

一方、以下だけを理由に原則 FAIL させない。

- status literal の軽微な違い
- SHA の単純不一致
- 説明用 placeholder
- optional metadata 欠落
- cosmetic naming mismatch

---

# 23. Hard Fail を追加する際の判定質問

新しい FAIL 条件を追加するときは、必ず以下を問う。

> **これは「誤ったコードを書くこと」または「誤った対象を検証すること」を具体的に防いでいるか？**

それとも、

> **instruction が想定フォーマットどおりではないことを検出しているだけか？**

後者であれば、原則として WARN または INFO とする。

---

# 24. Minimal Enforcement

新しい workflow rule / validator / metadata / status を導入するときは、

> これをなくした場合、以下のどれかが実質的に悪化するか？

を確認する。

- Coding Agent の探索量
- 誤実装率
- コード品質
- 回帰リスク
- 判断の再現性
- Traceability
- 人間による理解コスト

**Yes** なら採用候補。

**No** なら、削除・WARN 化・INFO 化を検討する。

---

# 25. Instruction 作成不備のコストを明示的に扱う

Workflow 制約を増やすときは、それを正しく記述する instruction 側の難易度も評価する。

制御機構には必ず、

```text
Safety Benefit
```

だけでなく、

```text
Instruction Complexity
+
Maintenance Cost
+
False Positive Cost
```

が存在する。

したがって評価は、

```text
Net Benefit
=
Risk Reduction
-
Instruction Failure Cost
-
Operational Overhead
```

として考える。

ENH-E7 では、一部の機構で Operational Overhead と Instruction Failure Cost が Risk Reduction を上回ったと考えられる。

---

# 26. Workflow Template の設計原則一覧

今後は以下を基本原則とする。

## 1. Separation of Concerns

Requirements、Design、Implementation、Test の責務を分離する。

## 2. Minimum Sufficient Context

各 Agent には作業に必要十分な情報だけを与える。

## 3. No Unnecessary Exploration

Coding Agent に要件・設計・過去経緯を不必要に探索させない。

## 4. Artifact-based Handoff

Agent、Work Package、Gate 間の引き継ぎは永続成果物を基本とする。

## 5. Canonical Requirements

現在のシステムが満たすべき仕様は Requirements を正本とする。

## 6. Separation of Requirement and Design

「何を満たすか」と「どう実現するか」を分ける。

## 7. Traceable Change Reasoning

Requirement → Design → Work Package → Code → Test の因果関係を追跡可能にする。

## 8. Quality Boundary by Gate

Gate を意味のあるコード変更成果＋品質保証の単位とする。

## 9. Work Package for Cognitive Load Reduction

Work Package は Gate を Coding Agent が扱えるサイズへ分割するために使う。

## 10. Enhancement-level Integration Verification

Gate 単体 Test に加え、Enhancement 完了時に cross-gate integration / regression を確認する。

## 11. Canonicalization after Enhancement

Enhancement 完了後、その結果を Canonical Requirements へ統合する。

## 12. Semantic Validation over String Validation

SHA、placeholder、status 等は文字列完全一致より意味上のリスクを見る。

## 13. Derived State over Declared State

重要な実行状態は可能な限り実成果物・依存関係から導出する。

## 14. Robustness over Protocol Exactness

非本質的な protocol 差異で正常作業を停止させない。

## 15. Minimal Machine Contract

Instruction Agent と validator 間の machine protocol は少数・単純・安定的にする。

## 16. FAIL / WARN / INFO Separation

すべての不一致を Hard Fail にしない。

## 17. False Positive Awareness

「危険なのに通す」だけでなく「安全なのに止める」コストも考慮する。

## 18. Minimal Enforcement

実害を防がない制約・状態・検査は増やさない。

---

# 27. ENH-E7 で確認された過剰設計パターン

以下は、今後の Workflow Template 見直しで特に警戒する。

```text
SHA が完全一致しなければ作業不可
```

```text
placeholder という文字列自体が存在すれば FAIL
```

```text
READY_TO_EXECUTE など status literal が完全一致しなければ FAIL
```

```text
Work Package ごとに Gate 級の品質保証を要求
```

```text
workflow 上の状態差異をすべて FAIL
```

```text
instruction generator に多数の厳密な protocol 値を書かせる
```

```text
preflight が成果物の準備状態より metadata の形式を重視する
```

```text
追跡性向上のために不要な Artifact を大量生成する
```

```text
Coding Agent の仕事を簡単にする workflow が、
workflow 自体を理解・修正する仕事を増やす
```

```text
正常な実装を止める false positive が頻発する
```

これらが見られる場合、元の設計思想から逸脱している可能性が高い。

---

# 28. Workflow 見直し時のチェックリスト

各機構について以下を確認する。

- [ ] これは誰の仕事を簡単にする仕組みか
- [ ] これが存在しない場合、何が具体的に壊れるか
- [ ] Coding Agent の探索量を減らしているか
- [ ] Coding Agent に新しい workflow 理解作業を増やしていないか
- [ ] Hard Fail である必要があるか
- [ ] WARN で十分ではないか
- [ ] INFO だけで十分ではないか
- [ ] 状態は declaration ではなく導出できないか
- [ ] 文字列ではなく意味を検証できないか
- [ ] instruction generator に過度な protocol 精度を要求していないか
- [ ] 同じ情報を別 Artifact がすでに持っていないか
- [ ] Requirement → Design → Code → Test を追跡できるか
- [ ] Gate と Work Package の責務を混同していないか
- [ ] 正常な作業を誤って止める false positive のコストを考慮したか
- [ ] 最終成果物の品質向上に実際に寄与しているか

明確な Yes が得られない制約は、削減対象とする。

---

# 29. 今後優先して見直す対象

Workflow Template を修正する場合、機構追加より先に以下を棚卸しする。

1. `READY_TO_EXECUTE` 等の status literal による Hard Fail
2. Status を成果物・依存関係から導出できる箇所
3. Planning / instruction / preflight 間の private protocol
4. SHA 完全一致制約
5. Placeholder の全面検査
6. Work Package ごとの過剰な checkpoint / state management
7. FAIL / WARN / INFO の境界
8. Coding Agent が workflow 解読を必要としている箇所
9. 重複 Artifact / metadata
10. Enhancement 完了後の Canonical Requirements 更新
11. Gate Test と Enhancement-level integration / regression の責務分離

---

# 30. 一言で表現した設計思想

Workflow Template の目的は、

```text
厳密な workflow protocol に
すべての Agent を従わせること
```

ではない。

目指す状態は、

```text
必要な人・Agent が
必要なタイミングで
必要十分な情報だけを受け取り
余計な探索をせず
迷わず作業し
意味のあるコード成果単位で品質を確認し
変更理由を後から追跡でき
非本質的不整合によって正常な作業を止められない
```

ことである。

**Workflow は開発成果を効率的かつ安全に作るための補助システムである。  
Workflow 自体の完全性・厳密性を成果物より優先してはならない。**

---

# 31. 次スレッドへの引き継ぎ方針

次スレッドで Workflow Template を見直す場合、本書を設計判断の基準とする。

方向性は、

> **新しい制御機構を追加することではなく、元の目的に寄与しない Hard Fail・状態管理・protocol・metadata を削減すること**

を第一とする。

特に `READY_TO_EXECUTE` 等の status 問題については、

> **status 名を統一するだけでは根本解決ではない。  
> そもそもその status literal を実行可否判定に使う必要があるのか**

から再検討する。

Instruction の表記不備を厳密な validator で取り締まるのではなく、

> **instruction の軽微な不備が実装作業の停止へ波及しない Workflow**

を目標とする。