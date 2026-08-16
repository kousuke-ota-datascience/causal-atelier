### 0.2. 基本フロー


- `Planning / Requirements / Design 完了`
    - これは、本READMEのスコープ外であるということで問題ないか？であればその旨記載せよ

- XX. Phase X work Package がない場合
    - work Package がない場合の記載も必要なのではないか？
    - Phase B を2つに分け、以下のパターンで記載するのはどうか？
        - Phase B1: work package を実行
        - Phase B2: ゲート全体を実行
    - Phase C, D は、PhaseB1のパターンのとき固有の処理であることを明記する


## 4. Phase C — Candidate Assembly: 各Gateにおける複数 Work Package 実装完了時の結果の統合

プロンプトはこうでは？楽しないで。

```text
下記ファイルを実行せよ

- docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/agent_entry_prompts/
    - 20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md

Runtime identityは以下の通り

- GATE_ID=G01
- TRIAL_NO=01

プロンプトの際の基本言語は日本語とする
```

## 5. Phase D — Independent Verification: Gate Candidate の独立検証

`## 4. ` と同様。プロンプトはこうでは？

```text
下記ファイルを実行せよ

- docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/agent_entry_prompts/
    - 30_independent_verification_01_test_agent_prompt.md

Runtime identityは以下の通り

- GATE_ID=G01
- TRIAL_NO=01

プロンプトの際の基本言語は日本語とする
```

## 6. Phase E — 999 Gate Decision: Gate の最終判定

`### 2.0. Phase A 最低限クイックチェック` と同様のものが必要。

## 7. Phase F — Current State promotion と次 Gate: PASS成果の昇格と次工程への移行

わざわざ実施した、以下2つのプロンプトがごっそり抜けてる

#### G02 freeze前の source confirmation をLLMに実施させる
```
下記ファイルを実行せよ。

docs/wiki/develop_memo/_work/
20260813_ENH-E7_project_analysis_workspace_separation/
40_operator_workflows/architecture_review/
01_architecture_discovery_prompt.md

目的は G02 Gate contract freeze 前の source confirmation である。

特に以下を確定すること。

- current Causal / Exploratory / Predictive surface-to-operation mapping
- Data Quality の実際のoperation / surfaceの有無
- TIME_TREND の実際のsemanticsと配置候補
- CHART がoperationなのかpresentation mechanismなのか
- legacy analytical route behavior
- G02実装にAPI / persistence変更が本当に不要か

制約:

- Product codeは変更しない
- test codeも変更しない
- Facts と Design recommendationを明確に分離する
- UI taxonomyを埋めるために存在しないoperationを捏造しない
- current source / tests / config / runtime factを根拠とする
- 基本言語は日本語とする

最後に、G02 freezeをBLOCKする未解決事項が残っているかを明示すること。
```


#### discovery結果をG02 contractへ反映する

```
ENH-E7 G02 Gate contract freeze作業を実施せよ。

前工程で実施したArchitecture Discovery / source confirmationの結果を
唯一のsource factとして使用すること。

目的:
G02 Coding Agentがassigned Pxxだけを読んで、
設計判断を再構築せず実装できる状態までcontractを確定する。

対象:

1.
40_operator_workflows/architecture_review/
02_target_architecture_decision_record.md

2.
00_enhance_background/
04_design_revision.md

3.
00_enhance_background/
05_requirements_design_consistency_and_traceability_review.md

4.
10_enhance_instruction/G02/
06_G02_P04_exploratory_stage_surface_migration.md

5.
10_enhance_instruction/G02/
06_Ariadne_ENH-E7_G02_implementation_instruction.md

6.
10_enhance_instruction/G02/
07_Ariadne_ENH-E7_G02_test_instruction.md

7.
10_enhance_instruction/G02/
README.md

実施事項:

- AR-E7-09 のdeferred confirmationをsource factで解消する
- Data Quality / TIME_TREND / CHART のfinal placementまたは明示的availability behaviorを確定する
- backendに存在しないoperationを作らない
- Requirement変更が必要でない限り03_requirements_revision.mdは変更しない
- P04をself-containedにし、Coding AgentがArchitecture Reviewや00-layerを読まずに実装できるようにする
- 06 implementation contractと07 verification contractの内容が矛盾しないことを確認する
- Requirements → Design → Pxx → AC/Testのtraceabilityを再確認する
- unresolved semantic blockerがゼロの場合のみ、
  G02 06 Contract statusをFROZEN、
  G02 07 Verification contract statusをFROZEN
  とする
- 単なるstatus literalを合わせる目的でfreezeしてはならない
- Product code / test codeは変更しない

基本言語は日本語とする。

最後に以下を報告すること。

- source facts
- freeze時に確定したdesign decisions
- 変更ファイル
- unresolved blockers
- G02 P01 preflightを実行可能か
```