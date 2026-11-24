# ENH-E11 G01 Trial 01 Test Item 005 — Canonical JCS / SHA-256

| 項目 | 記録 |
| --- | --- |
| Test Item ID | `005_canonical_jcs` |
| 正式判定 | **PASS** |
| 実行層 | enhancement / contract |
| Fixed Trial Candidate / actual tested HEAD | `72bcd6acaab6caf48827bf2bb6cd5e249afd658b` |
| TEST_START_SHA | `249bc48433e1472442fdbedfb9b848896e58d648` |
| 実行日 | 2026-11-24（JST） |
| Acceptance authority | [凍結 Gate 07](../../../10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md) |

固定済み JCS-01〜07 の byte・SHA を全一致で確認。JCS-N01〜07 は拒否または Unicode 表現保持を確認。Study request、Graph 内容とファイル SHA、Manifest と Marker の digest を区別。

| 検証項目 | AC | DD ID / 検証目的 | 判定 |
| --- | --- | --- | --- |
| G01-07-04 | AC-02 | GRAPH01、MAN01–03 | PASS |

## 観測と根拠

`jcs.canonical_bytes` を7個の事前固定 `expected_canonical_utf8_json` と SHA-256 に照合。負例は NaN/Inf、JSON/YAML 重複キー、孤立 surrogate、不正確な整数、未知オブジェクト、NFC/NFD 非同一、旧 schema を全件観測。Graph semantic digest と完全なファイル SHA の混同を高水準テストで拒否し、実 CLI/Reader における Study/Manifest/Marker/Descriptor の byte join を再測定。 [Schema/JCS/FCI プローブ](independent_raw_evidence.md#b02-draft-2020-12--strict-parser--jcs--b04-api) · [G01 の全 node ID と実測出力](independent_raw_evidence.md#独立-g01-pytest) · [独立 CLI/Reader プローブ](independent_raw_evidence.md#独立実-cli--reader--amd-004-controls)

## 実行・再現

固定候補 checkout で上記の各テスト/プローブを再実行できる。正負例の exact command、node ID、fixture、exit、実 stdout と必要な故障注入は実測出力を参照。候補・fixture・環境 identity は [001](ENH-E11-G01_01__001_candidate_identity.md) に記録した。

[実測出力](independent_raw_evidence.md) · [再実行用資料](independent_probe_inputs.md)

検証対象に対する production code、repo tests、migration、依存定義、凍結契約の変更は0件。
