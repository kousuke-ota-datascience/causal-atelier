# Detailed Design — ENH-E7差分

## Project route

- `/projects`
- `/projects/new`
- `/projects/<id>/overview`
- `/projects/<id>/context`
- `/projects/<id>/data`
- `/projects/<id>/results`
- `/projects/<id>` → `/projects/<id>/overview`

## Analysis route

`/projects/<id>/analysis/<family>/<stage>` をcanonicalとして維持し、existing resource-route semanticsも保護する。

## Context behavior

- Current Project: URL由来 / read-only
- Research Context: existing resourceから選択
- Dataset Version: existing resourceから選択
- Analysis View: Dataset Versionと整合するexisting viewから選択
- context変更だけを理由にFamily / Stage routeを書き換えない

## Browser semantics

Direct link / reload / Back / ForwardをProduct behaviorとして検証する。
