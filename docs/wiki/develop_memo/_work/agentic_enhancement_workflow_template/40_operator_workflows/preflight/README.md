# Preflight / Prerequisite Workflow

## Purpose

Gate acceptanceとは別に、Gate executionに必要なenvironment / infrastructure / data / migration baselineを確認する。

## Semantics

- preflight PASS = test可能な前提が成立。
- preflight FAIL = prerequisite未成立。product implementation FAILとは限らない。
- Gate testがprerequisite不足で実行不能なら原則`BLOCKED`。

## Typical checks

- DB connectivity / expected database
- migration head
- required services
- credential presence (valueは記録しない)
- clean baseline fixture
- toolchain version
- working tree / branch / commit
