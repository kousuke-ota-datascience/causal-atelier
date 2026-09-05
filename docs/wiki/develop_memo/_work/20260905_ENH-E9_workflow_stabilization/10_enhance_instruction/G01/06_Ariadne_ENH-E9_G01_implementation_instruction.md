# Ariadne ENH-E9 G01 Implementation Instruction

**Document class:** Primary Execution Contract  
**Contract status:** `DRAFT_NOT_FROZEN`  
**Execution mode:** `SINGLE_EXECUTION`

## 1. Gate claim

Project / Analysis Contextの既存resourceを変更せず、利用者が保存済みAnalysis Viewの内容と主要Context入力の意味をUI上で確認できる状態を成立させる。

## 2. Blocking prerequisite

- E8 G03 formal PASS exact SHAがE9 baselineとして固定済み
- residual matrixでG01項目が`RESIDUAL`に確定済み
- 本06とG01 07がFROZEN

未成立ならCodingを開始しない。

## 3. Allowed scope

Freeze時にresidual確認された次のpresentation usabilityのみ。

- Saved Analysis Viewの内容確認action/presentation
- Active Research Contextの意味説明
- required frontend wiring/style/test

## 4. Forbidden changes

- Analysis View schema / lifecycle変更
- Project Management IA redesign
- Current Project authority変更
- Research Context/Dataset/Analysis View restore/invalidation semantics変更
- new backend resource/API/persistence追加（既存contractで成立しないことが判明した場合はcontract reviewへ戻す）

## 5. Requirement/design traceability

- FR-106
- FR-168
- FR-171–FR-174
- Basic Design: Analysis Context / Project Management Data ownership

## 6. Candidate completion

- allowed scope実装完了
- focused frontend tests PASS
- context ownership regression PASS
- candidate-affecting uncommitted changeなし
- Fixed Trial Candidate SHA固定
- Implementation Completion Report作成

`READY_FOR_TEST != Gate PASS`。
