# Enhancement Background — ENH-E6

このdirectoryは ENH-E6 の背景、source anomaly provenance、要件・設計差分、existing implementation alignment、traceabilityを保持する Planning / historical layer である。

## Source anomaly

`ENH-E5 / ANOM-E5-001 — Family Tab Observable UI Gap`

ENH-E5 は再openしない。E5 frozen contract / Trial candidate / independent verification / Gate Decision は historical evidence として immutable に保持し、E6 で新しいbaselineとacceptance evidenceを構築する。

## Primary planning conclusion

Family tab DOM/CSS/renderer の不存在が主因ではない。baseline source では次の integration mismatch が存在する。

1. canonical route restore は Family/Stage navigation renderer を実行する。
2. legacy/normal workspace activation は Navigation Context と history を変更し得るが、同じ renderer lifecycle を保証しない。
3. Family -> workspace の粗い mapping が残り、特に `CAUSAL -> discovery` のため Family-local Stage と presentation surface の binding が不足する。
4. E5 test には source existence inspection があり、real user journey の observable UI regression を十分に固定していない。

Planning の結論は Gate 06/07 に自己完結する形で収束させる。
