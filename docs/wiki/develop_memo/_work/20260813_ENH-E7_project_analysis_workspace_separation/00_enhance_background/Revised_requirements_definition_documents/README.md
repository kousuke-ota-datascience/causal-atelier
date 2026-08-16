# Revised Requirements / Design Documents

このディレクトリは、現在有効なAriadneのrequirements/designを**effective snapshot**として保存する。

本snapshotの読者は、過去のEnhancement計画、差分資料、Gate資料、handoff、source historyを知らなくても、Ariadneのプロダクトコンセプト、要求、論理モデル、基本設計、interface contract、詳細設計を理解できなければならない。

## 1. 文書言語

日本語話者が各文書を単独で読み、背景、要件、設計、制約を理解できることを基準とする。

API名、class/type/schema、`Family`, `Stage`, resource名、route等、英語を維持した方が実装との対応が明確な専門語は英語を許容する。

## 2. Normative snapshot rule

- 本文は**現在有効なproduct requirement/design**を記述する。
- 変更されなかった仕様も省略しない。`変更なし`、`existingを利用`等の差分表現だけで内容を外部baselineへ委譲しない。
- 過去Enhancementから継承する有効内容は本文へ統合する。
- Enhancement番号、変更理由、migration順序、Gate、Work Package等の履歴情報は、current specificationを理解するために必要な場合を除き本文へ混在させない。
- 履歴を残す場合は各文書末尾のCHANGE LOGへ分離する。
- source codeは照合対象にはできるが、normative specification本文の代替にはしない。

## 3. 自己完結性

完成文書には、次のような未解決の外部依存を残さない。

- `過去Enhancementの文書を参照`
- `既存contractを維持する`のみでcontract内容を記載しない
- `以前のFamily / Stage model`のみでmodelを再定義しない
- `旧画面と同じ`のみでcurrent behaviorを確定させる

同一snapshot内の上位・下位文書間参照は許容する。ただし、参照先がなくても当該文書の主責務と主要constraintを理解できる粒度で記述する。

## 4. 見出し階層

見出しは情報アーキテクチャとして扱う。

- 同一heading levelに異なる抽象度の概念を混在させない。
- major product concernと個別UI behaviorを同じlevelへ置かない。
- 抽象 -> 具体、Why -> What -> Howの順に降りる。
- current product structure、future extension、implementation detail、change historyを同一levelへ混在させない。

## 5. 文書責務

| 文書 | 主責務 |
| --- | --- |
| `00_product_concept_memo.md` | WHY / product vision / analytical model / application responsibility / future direction |
| `10_requirements_definition.md` | WHAT / effective requirements / E2E / FR / NFR / analytical requirements |
| `21_logical_data_design.md` | logical resource/value/state model |
| `22_product_basic_design.md` | layer/function/surface responsibilityと主要behavior |
| `23_api_interface_design.md` | external/internal/browser interface contract |
| `30_detailed_design.md` | module/component/state transition/data-flow/test seamへの具体化 |

依存方向は次を基本とする。

```text
00 Product Concept
        ↓
10 Requirements
        ↓
21 Logical Data Design
        ↓
22 Product Basic Design
        ↓
23 API / Interface Design
        ↓
30 Detailed Design
```

下位文書は上位文書の意味を勝手に変更しない。

## 6. Current application structure

Ariadneのtop-level responsibilityは次の2 scopeに分かれる。

```text
Ariadne
├─ Project Management
│  └─ Project resource / versioned analysis inputを管理する
│
└─ Analysis Workspace
   └─ 明示されたProject contextの下でanalysisを実行・閲覧する
```

`Project Management`と`Analysis Workspace`は別navigation scopeである。Analysis Workspace内では`Family`とFamily-local `Navigation Stage`を用いる。Navigation Stageはruntime `Execution Stage`ではない。

## 7. Self-containedness acceptance

本snapshotは少なくとも次を満たすこと。

1. CHANGE LOGを読まなくてもcurrent product behaviorを説明できる。
2. 過去Enhancement directoryを参照しなくても、Project Management / Analysis Workspace / Family / Navigation Stage / Execution Stageの関係を説明できる。
3. `10/21/22/23/30`から、active requirement、logical state/resource、surface ownership、canonical route、API/browser contract、runtime independenceを追跡できる。
4. persistent/API/backend domain semanticsに変更がない領域でも、current contract本文を省略しない。
5. `existing`, `legacy`, `previous`等の語を使う場合、そのcurrent behaviorを本文内で確定できる。
6. Project routeとAnalysis routeのdirect link / reload / Back / Forward semanticsが文書間で矛盾しない。
7. Analysis ContextのCurrent Project / Research Context / Dataset Version / Analysis Viewのownershipとrestore/invalidation ruleが文書間で矛盾しない。

## 8. Execution Agent boundary

本ディレクトリはPlanning / Human Review / future auditのための背景・正本層である。

Coding Agent / Test Agentへ実装・検証contractを渡す場合は、必要な決定をfreeze済みGate/Work Packageへ収束させる。通常実行時に本snapshot全体を再探索させることを前提としない。

## 20. CHANGE LOG

### 20.5 Family × Navigation Stage application model

Exploratory / Predictive / CausalをFamilyとし、Family-owned Navigation Stageをapplication/navigation concernとしてruntime execution concernから分離した。

### 20.6 Project Management / Analysis Workspace responsibility separation

Project resource managementとanalysis execution/presentationを別navigation scopeへ分離し、Project routes、Analysis Context、surface ownership、browser navigation semanticsをcurrent effective snapshotへ統合した。
