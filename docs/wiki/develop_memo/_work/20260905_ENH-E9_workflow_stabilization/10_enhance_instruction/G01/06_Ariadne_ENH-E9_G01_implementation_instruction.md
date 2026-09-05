# Ariadne ENH-E9 G01 Implementation Instruction

**Document class:** Primary Execution Contract  
**Contract status:** `FROZEN`  
**Execution mode:** `SINGLE_EXECUTION`  
**Baseline:** `93fc2492112889a9465296a8647c251f84151bc5`

## 1. Gate claim

Project / Analysis Contextのresource ownershipを変更せず、利用者が保存済みAnalysis Viewの内容とActive Research Contextの意味をUI上で確認できる状態を成立させる。

## 2. Required behavior

1. Saved Analysis Viewsに、selected saved viewの設定内容を確認できる明示的な表示actionを提供する。
2. 表示actionは既存Analysis Viewをread-onlyで表示し、更新・複製・新規version作成を副作用として行わない。
3. Active Research Contextに、何を意味するselectionか理解できるtooltip/helpを提供する。
4. baselineが既にACを満たす場合、不要な再実装は行わずtest/evidence整備だけでよい。

## 3. Allowed files / work

主に`frontend/index.html`, `frontend/app.js`, `frontend/styles.css`および該当frontend/product tests。既存APIを利用する範囲のwiringは許可する。

## 4. Forbidden changes

- Analysis View schema/lifecycle変更
- Project Management IA redesign
- Current Project authority変更
- Research Context/Dataset/Analysis View restore/invalidation semantics変更
- new backend resource/API/persistence追加

## 5. Traceability

FR-106, FR-168, FR-171–FR-174。

## 6. Candidate completion

focused tests、context ownership regression、candidate-affecting uncommitted changeなしを確認し、exact Fixed Trial Candidate SHAとImplementation Completion Reportを作成する。Coding側からGate PASSを宣言しない。`READY_FOR_TEST != PASS`。
