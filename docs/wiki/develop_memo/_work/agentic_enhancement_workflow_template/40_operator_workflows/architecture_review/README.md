# Architecture Review Workflow — 使用ガイド

**Document class:** Authoring Guide  
**Self-containment:** MUST — このREADMEだけでarchitecture reviewの発動条件・実行順序・成果物責務が分かること。

## 1. Purpose

implementation contractを作成する前に、current architectureの事実、target architecture decision、Gate decompositionを明確化する補助workflowである。

## 2. 使用条件 — CONDITIONAL MUST

- runtime entrypoint / lifecycle change
- authority / ownership change
- persistence / schema / lineage change
- legacy path removal / consolidation
- migration strategy change
- cross-subsystem canonical source-of-truth change

## 3. 実行順序

1. Architecture Discovery — current implementation factsを調査。product codeを変更しない。
2. Target Architecture Decision Record — target authority / invariant / transition policyを決定。
3. Gate Decomposition — PASS後のdownstream reliance boundaryに基づきGateへ分解。

Gate decompositionをimplementation sizeで決めない。Execution sizeだけが問題ならGateを増やさずWork Packageを使う。

## 4. Output rule

各outputは自身の結論・事実・decisionを本文内に記載する。code / design / schemaはevidence sourceとして参照してよい。

Architecture reviewのapproved decisionは00層の正式背景・要件・設計へ反映し、Agentへ直接必要なimplementation / acceptance semanticsは06 / 07へeffective formで記載する。
