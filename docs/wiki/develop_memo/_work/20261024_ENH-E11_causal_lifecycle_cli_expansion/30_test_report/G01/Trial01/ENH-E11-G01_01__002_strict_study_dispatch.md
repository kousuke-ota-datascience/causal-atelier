# ENH-E11 G01 Trial 01 Test Item 002 — Strict Study / dispatch

| 項目 | 記録 |
| --- | --- |
| Test Item ID | `002_strict_study_dispatch` |
| 正式判定 | **PASS** |
| 実行層 | enhancement / contract + CLI integration |
| Fixed Trial Candidate / actual tested HEAD | `72bcd6acaab6caf48827bf2bb6cd5e249afd658b` |
| TEST_START_SHA | `249bc48433e1472442fdbedfb9b848896e58d648` |
| 実行日 | 2026-11-24（JST） |
| Acceptance authority | [凍結 Gate 07](../../../10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md) |

JSON/YAML 正例を受理。重複、旧版、未知・余剰、P1-M06 以外、Question ID・Design 列順不一致を拒否。実 CLI の不一致は exit 2、staging なし。既存 v2 は別の実行入口で通過。

| 検証項目 | AC | DD ID / 検証目的 | 判定 |
| --- | --- | --- | --- |
| G01-07-01 | AC-01, AC-05 | SPEC01–04、RUN03/04 | PASS |

## 観測と根拠

`StrictLocalConfigDecoder.decode` の JSON/YAML projection、duplicate key、YAML alias/unsafe constructor、未知 field と旧 v2 schema を contract tests で確認。Method `P1-M05`、余剰 Method config、誤った depth/alpha、重複 BK pair は typed 拒否。Question ID と Design 順序の変更は ContentRef SHA を更新した実 CLI でも exit 2、`UNSUPPORTED_COMBINATION`、staging と final run は0。旧 Product の CLI v2 contract は実回帰で通過。 [G01 の全 node ID と実測出力](independent_raw_evidence.md#独立-g01-pytest) · [独立 CLI/Reader プローブ](independent_raw_evidence.md#独立実-cli--reader--amd-004-controls) · [必須PASS集合の全 node ID と実測出力](independent_raw_evidence.md#g01--scientific-core--product-必須pass集合)

B02 の実 Python 3.12 Draft 2020-12 validator で、Question/Design/Method Config の正負例と実公開 Study の版・構造を確認した。JSON Schema が許容する整数相当の小数表記や順序に関する制約は厳密 Design parser の負例で確認した。 [Schema/JCS/FCI プローブ](independent_raw_evidence.md#b02-draft-2020-12--strict-parser--jcs--b04-api) · [実公開 bundle の Schema 照合](independent_raw_evidence.md#b02-実公開-bundle-の-schema-照合)

## 実行・再現

固定候補 checkout で上記の各テスト/プローブを再実行できる。正負例の exact command、node ID、fixture、exit、実 stdout と必要な故障注入は実測出力を参照。候補・fixture・環境 identity は [001](ENH-E11-G01_01__001_candidate_identity.md) に記録した。

[実測出力](independent_raw_evidence.md) · [再実行用資料](independent_probe_inputs.md)

検証対象に対する production code、repo tests、migration、依存定義、凍結契約の変更は0件。
