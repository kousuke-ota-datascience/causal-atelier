# 10_14_fr_workflow_execution


---

## FR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| FR-074 | Workflow | Analysis FamilyをEXPLORATORY、CAUSAL、PREDICTIVEとして識別する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-075 | Workflow | Family別PlannerをRegistryから解決する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-076 | Workflow | 分析の実行計画を版管理し、実行時の条件を後から復元できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-077 | Workflow | Stage Typeをnamespace、name、versionで識別する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-078 | Workflow | 分析処理の依存順序と処理間の入力・出力の対応を追跡できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-079 | Workflow | Stage RunnerをRegistryから解決し、Executorへif/elif分岐を集約しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-080 | Workflow | canonical lifecycle/application serviceがExecutionのclaim、state、cancel、retry、Result/Artifact metadata commitを所有し、Generic Executorはowned workflow context内で依存順、Stage sequencing、runner invocationを実行する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-081 | Workflow | Stage ExecutionとAttemptのstatus、開始・終了時刻、errorを保持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-082 | Workflow | 再送された同一依頼の重複処理を防止し、同じ識別子で異なる依頼が来た場合は拒否する | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-083 | Workflow | 技術retryは同一Execution、条件変更は新Executionとする | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-084 | Workflow | 依存処理の成果物を適切な形式で後続処理に引き渡せる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-085 | Workflow | 計画の依存関係や必要な入力が不整合なら実行前に拒否する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-086a | Workflow | 確率的処理を再試行しても同じ実効乱数条件を再現できる | SHOULD | ACTIVE | PARTIAL | ENH-E5 |
| FR-086b | Workflow | 処理ごとの時間・資源上限を設定できる | SHOULD | DEFERRED | PARTIAL | FUTURE |
| FR-087a | Workflow | Execution snapshotにcurrent code/runtime/schema再現性metadataを保持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-087b | Workflow | 分析の再現に必要な実行環境と科学ライブラリの版を確認できる | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-088 | Workflow | Execution StatusとResult analytical statusを分離する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-089 | Workflow | Generic validationとFamily-specific validationを分離して実行する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-143 | Workflow | runtime layerはNavigation Stage ID、browser route、tab/sidebar stateへ依存しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E5 |
