# Preflight / Prerequisite Workflow — 使用ガイド

**Document class:** Authoring Guide  
**Self-containment:** MUST — このREADMEだけでpreflightの目的・判定意味・instruction/result作成方法が分かること。

## 1. Purpose

Gate acceptanceとは別に、Gate execution / verificationに必要なenvironment / infrastructure / data / migration baselineを確認する。

## 2. Semantics

- preflight PASS = 指定prerequisiteが成立。
- preflight FAIL = prerequisite不成立。product implementation FAILとは限らない。
- product判定がprerequisite不足で不可能ならGate verificationは原則`BLOCKED`。

## 3. Instruction authoring

Preflight Instructionへ、purpose、target Gate、baseline、destructive permission、各checkのexact command/method、expected result、abort condition、**required result schema**を記載する。Agentへ別result templateを必須参照させない。

## 4. Result authoring

Resultへ、status、observed baseline、各checkのcommand / exit / observed fact / result、environment mutation、conclusion、Gate execution eligibilityを記載する。

## 5. Typical checks

- DB connectivity / expected database
- migration head
- required services
- credential presence（valueは記録しない）
- clean baseline fixture
- toolchain version
- working tree / branch / commit
