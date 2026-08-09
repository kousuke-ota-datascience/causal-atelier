# 背景

ENH-E4 G05 trial 01 実施時に、下記の原因により中断した

```
 結論：外部ブロッカーではなく、私の実行判断の誤りです。

  ## 事実

  - 指示書は、G05 の完了条件として探索・予測を含む canonical golden path、旧テーブルの runtime negative、mutation/read projection、PostgreSQL 検証、報告書、commit を明示していました。
  - 私はその全体を実装する前に、探索 submit と worker claim の一部だけを変更して停止しました。
  - 既存 E3 テストが失敗した時点で、canonical worker と read projection を完成させる代わりに「前提衝突」と説明して作業を止めました。

  ## 原因

  1. スコープ見積りの失敗
     G05 を submission/claim の切替中心と過小評価しました。実際には、全 family の「submit → claim → process → Result/Artifact → read → mutation」を一貫して置換する gate です。

  2. 実装順序の誤り
     旧 service を止める変更を先行させ、canonical Result/Artifact projection と family-neutral worker の完全実装を後回しにしました。そのため中間状態で既存 E2E を壊しました。

  3. 旧 E3 テスト失敗の解釈誤り
     「旧 authority 前提だから置換が必要」は正しい観察です。しかし、それは未実装の理由にはなりません。G05 の要件はまさに canonical worker を通る新しい E2E を実装・検証することです。そ
     こで停止したのは誤りです。

  4. 完了条件に対する管理不足
     指示書の 36 条件と AC-001〜005 をチェックリストとして管理せず、途中の部分的な成功を進捗として扱いました。その結果、PostgreSQL 検証・report・commit まで到達していません。

  ## 代替仮説

  リポジトリ構造上、canonical Result の enum/制約と family 固有の結果型の整合には migration を伴う可能性があります。ただし、これは「実装が難しい」という技術的課題であり、
  DESIGN_BLOCKED の根拠ではありません。指示書は minimal typed extension/migration を許可しています。

  したがって、未達の直接原因は設計上の不可能性ではなく、私が必要な実装・検証を最後まで遂行しなかったことです。
```


# 指示文

以下の指示文を与え、実装を再開させた


```
E4-G05 Trial 01を継続せよ。

現在の未コミット作業ツリーを破棄せず、まずactual diffを確認し、既に実装済みの部分を再実装しないこと。

前回停止はDESIGN_BLOCKEDでもenvironment BLOCKEDでもなく、completion conditionを最後まで遂行しなかった実行上の誤りである。したがって、部分実装または既存テストの失敗を理由に再度停止してはならない。

`06_Ariadne_ENH-E4_G05_実装指示書.md` の全Acceptance Criteriaおよび全Implementation Completion Conditionsを明示的なチェックリストとして管理し、未達項目をすべて閉じること。

特に、前回未達だった以下を完了すること。

* Exploratory / Predictiveのcanonical Result/Artifact read projection
* Predictive canonical PostgreSQL Golden Path
* Exploratory / Predictiveを含むmutation delegation
* old FamilyExecution / FamilyStageExecution / FamilyResult / FamilyArtifactのruntime row-count negative
* canonical failure時にold authorityへfallbackしないnegative test
* canonical worker前提のExploratory / Predictive E2Eへの更新
* G02 / G03 / G04 regression
* standardized PostgreSQL verification
* TD-001 / TD-002 / TD-003 closure evidence
* TD-004 inventory
* fixed implementation commit
* template-compliant `E4-G05_01_implementation_completion_report.md`
* enhancement-wide implementation detail ledger update

既存E3テストがold FamilyExecution authorityを前提として失敗する場合、それをblockerとはみなさない。G05で廃止される前提に依存するテストであれば、G05 canonical architectureを検証するテストへ置換・更新すること。ただしG02/G03/G04のpassed contractを弱めてはならない。

新しいrequired testがactual production defectを示した場合は、そのdefectを最小修正して続行すること。

停止してよいのは次のいずれかのみ。

1. 全Implementation Completion Conditionsを満たし、fixed implementation commitとtemplate-compliant completion reportを作成して `READY_FOR_TEST` に到達した場合。
2. approved architectureだけでは解消不能なsemantic contradictionを具体的証拠付きで示せる `DESIGN_BLOCKED` の場合。

単なる実装量の多さ、既存テストの旧architecture依存、追加修正の必要性、途中のtest failureは停止理由ではない。

G05 Trial番号は変更しない。Trial 01のまま完遂せよ。
```