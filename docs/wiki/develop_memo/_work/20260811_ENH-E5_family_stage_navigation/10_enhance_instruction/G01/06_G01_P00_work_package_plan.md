# ENH-E5 G01 P00 Work Package計画

文書区分: Planning / Operator Artifact（計画・運用資料）
自己完結性: orchestration用途としてMUST（必須）

- Gate: G01
- Trial適用範囲: Trial01。後続Trialでのre-baselineはremediation/amendment上必要な場合のみ実施する
- Parent 06: `06_Ariadne_ENH-E5_G01_implementation_instruction.md`
- Parent 07: `07_Ariadne_ENH-E5_G01_test_instruction.md`
- Plan状態: **DRAFT_FOR_REVIEW**（レビュー前ドラフト）
- P00はexecution controlであり、implementation packageではない。

## 1. Work Package Modeを採用する理由

Gateのsemantic boundaryは分割せず保持する一方、実装はroute/state/UI/Family固有挙動/regression surfaceへ広がる。Work Packageはpartial Gate acceptanceを作らず、coding実行単位とfailure localizationだけを分離するために用いる。

## 2. このGateで有効なsemantic boundary

- Gate acceptance claim: canonical catalogを利用してtop Family tabs + Family-local Stage sidebarを成立させ、URL/deep link/history/legacy route compatibilityを確立する。
- Downstream result: Family-specific G02-G04が同一navigation shell上へStage contentを安全に配置できる。
- 全Packageで`Navigation Stage != Execution Stage`、未承認schema/engine変更禁止、既PASS Gate保護を維持する。

## 3. Package一覧

| Package | 目的 | 依存 | 開始条件 | 完了条件 | Focused verification |
|---|---|---|---|---|---|
| P01 | canonical route parser/serializer、legacy route map、descriptor loading/state activation。 | NONE | upstream Package完了またはNONE | focused implementation + verification + checkpoint report | Package固有focused test |
| P02 | 上部Family tab + Family-local Stage sidebar + catalog駆動active/error state。 | P01 | upstream Package完了またはNONE | focused implementation + verification + checkpoint report | Package固有focused test |
| P03 | direct load、popstate/back-forward、global workspace分離、legacy navigation regression。 | P01,P02 | upstream Package完了またはNONE | focused implementation + verification + checkpoint report | Package固有focused test |

## 4. Execution DAG

```text
P01 -> P02 -> P03
```

## 5. 共通ルール

- Package completeはGate PASSを意味しない。
- Candidate Assembly前であれば、同一Trial内で同じPackageを再開・修正してよい。
- 各Packageは正確なSHAとfocused verificationを含むcheckpoint reportを作成する。
- 依存先Packageが完了してから依存元Packageを開始する。
- PxxはGate semantic claimまたはACを変更してはならない。

## 6. Package完了条件

Package completeには、implementation scope完了、focused check PASS、未解決Package blockerなし、checkpoint SHA記録、report作成のすべてが必要である。

## 7. Restart policy

Coding中断またはfocused self-check失敗だけではTrialを増やさない。同一Trial内で同じPackageを再開し、Package report履歴を保持する。

## 8. Checkpoint policy

各Packageは最終checkpoint SHAを1つ記録する。中間commitは存在してよいが、Gate acceptance identityにはしない。

## 9. Candidate Assembly

全Package完了後、指定された1回のassembly stepで以下を実施する:
- Package chainの完全性を確認する;
- Gate-wide testを実行する;
- 全diffをレビューする;
- blockerを解消する;
- Fixed Trial Candidate SHAを1つfreezeする;
- implementation completion reportを作成する。

## 10. Trial完了

07に基づくIndependent VerificationだけがPASS/FAIL/BLOCKEDを判定できる。

## 11. Remediation

Formal FAILの場合は必要に応じて08とRxxを使用する。candidate失敗を理由に、freeze済み06/07/P00のsemanticsを編集してはならない。

## Execution context isolation rule

P00はPlanning / orchestration artifactであり、通常のPackage Coding Agentへnormative inputとして渡さない。

各Pxx作成時に、P00/06から必要なentry condition、dependency、protected invariant、focused verificationをPxx本文へ収束する。

**Package AgentへP00を読ませない。** Pxxだけで担当packageを実行できない場合はPxxのfreeze不備である。
