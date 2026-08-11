# Ariadne ENH-E5 — Family × Stage Navigation 改修（次版）

文書区分: Authoring / Orchestration Guide（作成・運用ガイド）  
Template互換性: `agentic_enhancement_workflow_template` schema v11  
Branch: `feature/ariadne_mvp_e5`  
Planning baseline pin: `46122c68333df03680b97c253a7b5d32bf9393e7`  
Bundle状態: **DRAFT_FOR_REVIEW**  
Prepared at: `2026-08-11T16:21:58+09:00`

## 0. この版の結論

本bundleは、Ariadneのanalytical capabilityを **Family × Family-owned Navigation Stage** として再構成する ENH-E5 の次版指示書一式である。

この版では、前版の問題だった「00〜30層の過度な要約」と「Execution Agentに上流資料の再探索余地が残ること」を修正した。

中心原則は次の2つである。

1. **Planning文書は厚くする。** 背景、問題、判断理由、責務境界、具体例、互換性、scope外、edge caseまで記載し、人間とPlanning Agentが十分に判断できる状態を作る。
2. **Execution Agentのnormative contextは狭くする。** 上流判断を06/07/Pxxへ収束させ、Coding/Test Agentが仕様探索・architecture再判断を行わないようにする。

```text
00〜30: WHY / WHAT / HOW を十分な粒度で検討・保存
       ↓ Human / Architecture review
06 / 07 / Pxx: effective contractへ収束
       ↓ FREEZE
Execution Agent: 単一normative contractだけで実装・検証
```

## 0.1 既存実装・設計整合性監査

ENH-E5で変更しないcurrent contractについてPlanning baseline sourceとRevised 21/22/23/30を突合し、検出した乖離を設計側へ反映した。詳細な検出事項・修正内容・残存制約は`00_enhance_background/06_existing_implementation_design_alignment_review.md`を参照する。監査判定は`PASS_WITH_CORRECTIONS_APPLIED`。

## 1. 文書言語ポリシー

本bundleは**日本語話者が当該文書だけを読み、意味・判断理由・実行条件を理解できること**を品質要件とする。

原則として日本語で記載するもの:

- 背景・問題意識
- 設計判断と理由
- 責務境界
- 実装指示
- テスト指示
- Acceptance Criteriaの意味
- 禁止事項・停止条件

英語を維持してよいもの:

- `Family`, `Navigation Stage`, `Execution Stage`
- `Gate`, `Trial`, `Work Package`, `Acceptance Criteria`, `Transition Debt`
- API / route / schema / type / class / function / enum / state value
- 翻訳するとrepository上の識別子との対応が不明瞭になる専門概念

英語用語を使う場合も、周辺の説明は日本語で理解できるようにする。

## 2. Product / architecture の中心契約

1. `Family = global analytical context`。
2. `Navigation Stage = Family-local work/view context`。
3. UIは **上部横タブ = Family、左サイド = selected FamilyのNavigation Stage**。
4. `Navigation Stage != Execution Stage`。
5. concrete Navigation Stage catalogは各Capabilityが所有する。
6. `Family × Navigation Stage` はapplication/navigation modelであり、CLI / library / backend use caseの必須execution inputではない。
7. Current Family / Stageのtarget canonical stateはURLとし、E5ではDB永続化しない。
8. Predictive既存configuration / generated spec / execution semanticsを保持する。
9. LightGBM / DoWhy / EconML等の新規engineはscope外。
10. Overview/Flagship、専用Findings/Evidence persistent domain、AnalysisResult再設計はE5では実装しない。

## 3. Execution isolation — 次版の重要なworkflow invariant

### 3.1 SINGLE_EXECUTION Gate

Coding Agentの唯一のnormative sourceは対象Gateのfreeze済み`06_*_implementation_instruction.md`である。

Coding Agentは仕様を補う目的で次を読んではならない:

- 00〜30層
- ADR / Architecture Review
- Gate decomposition
- 07
- 他Gateの06/07
- 過去Enhancement文書
- issue / discussion / commit message
- 外部Web資料

current repositoryは**実装対象・既存事実を調査するimplementation substrate**として読んでよい。ただし仕様authorityではない。

### 3.2 WORK_PACKAGE Gate

各Package Coding Agentの唯一のnormative sourceは、割り当てられたfreeze済み`Pxx` instructionである。

Pxxは担当packageに必要なGate-level制約を自己完結的に保持しなければならない。Package Agentに06、07、P00、ADR等を併読させて仕様を合成させてはならない。

### 3.3 Test / Audit

Test / Audit Agentの唯一のnormative verification sourceは対象Gateのfreeze済み`07_*_test_instruction.md`である。

Implementation Completion Reportやrepository stateはcandidate identity / evidenceとして参照してよいが、Acceptance Criteriaを補完・変更するauthorityではない。

### 3.4 Contract ambiguity

単一normative contractだけではrequired behaviorやarchitecture boundaryを一意に決定できない場合、Agentは探索を広げず、`BLOCKED_CONTRACT_AMBIGUITY`で停止する。

> Repositoryから実装方法を発見してよい。Repositoryや上流資料から仕様を発見してはならない。

この原則は、Agentの探索空間を縮小し、推論資源をcode comprehension・implementation・test designへ集中させるためのものである。AIクレジット削減は期待効果であり、品質を下げてtoken量だけを削ることを目的としない。

## 4. Gate map

| Gate | Semantic acceptance boundary | Execution Mode |
|---|---|---|
| G00 | Family / Navigation Stage domain contractとcapability-owned catalogがExecution Stageから独立して成立する | SINGLE_EXECUTION |
| G01 | URL-driven Family/Stage navigation shellとlegacy navigation compatibilityが成立する | WORK_PACKAGE |
| G02 | Predictiveを6 Stageへ再配置し、既存設定・実行semanticsの完全互換が成立する | WORK_PACKAGE |
| G03 | Causalを7 Stageへ再配置し、Identification / Estimation分離と既存操作互換が成立する | WORK_PACKAGE |
| G04 | Exploratoryを6 Stageへ再配置し、探索観点ベースnavigationと既存操作互換が成立する | WORK_PACKAGE |
| G05 | 3 Family横断のcontext/result continuityとproduct-wide regression contractが成立する | SINGLE_EXECUTION |

## 5. Freeze preconditions

本bundleは`DRAFT_FOR_REVIEW`であり、未承認decisionをproduction factとして扱わない。

各Gateをfreezeする前に最低限:

1. Human approvalを得る。
2. local checkoutのbranch/SHAを確認する。
3. baseline testを実行する。
4. 先行PASS Gateがある場合、そのprotected contract identityを06/07/Pxx本文へ具体値として収束させる。
5. Agent実行時に「別資料を見ないと意味が分からない」記述が残っていないことを確認する。
6. unresolved placeholder / `UNKNOWN` がnormative semanticsに残る場合はfreezeしない。

Planning pinは`46122c68333df03680b97c253a7b5d32bf9393e7`である。freeze直前にremote/localのcurrent stateと一致するか再確認すること。

## 6. Directory entry points

- Background / effective snapshots: `00_enhance_background/`
- Gate / Package contracts: `10_enhance_instruction/`
- Implementation evidence: `20_implementation_reports/`
- Independent verification evidence: `30_test_report/`
- Architecture / operator workflow: `40_operator_workflows/`
- Change history: `90_change_history/`
- Current State: `ENH-E5_Current_State_Control_Sheet.md`
- Revision summary: `ENH-E5_next_revision_summary.md`
- Manifest: `MANIFEST.json`
