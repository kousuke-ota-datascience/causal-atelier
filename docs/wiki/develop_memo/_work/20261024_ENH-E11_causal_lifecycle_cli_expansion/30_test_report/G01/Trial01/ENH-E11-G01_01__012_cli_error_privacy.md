# ENH-E11 G01 Trial 01 Test Item 012 — CLI error and privacy

| 項目 | 記録 |
| --- | --- |
| Test Item ID | `012_cli_error_privacy` |
| 正式判定 | **BLOCKED** |
| 実行層 | enhancement / real ext4 CLI + fault controls |
| Fixed Trial Candidate / actual tested HEAD | `72bcd6acaab6caf48827bf2bb6cd5e249afd658b` |
| TEST_START_SHA | `249bc48433e1472442fdbedfb9b848896e58d648` |
| 実行日 | 2026-11-24（JST） |
| Acceptance authority | [凍結 Gate 07](../../../10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md) |

CLI exit 2/3/4/5、check-only の零書込、旧 row flag・true の拒否、全 Decision fields を対象とする正負観測と typed failure の一部を確認。AMD の失敗行列と FS/Privacy の完全な個別立証は未完。

| 検証項目 | AC | DD ID / 検証目的 | 判定 |
| --- | --- | --- | --- |
| G01-07-11 | AC-03, AC-05, AC-06 | RUN07、PUB07、PRIV01–06、READ03、AMD-001–003 | BLOCKED |

## 観測と根拠

実 CLI 出力は check-only exit 0・staging 無、旧 row flag exit 2、Study row opt-in exit 3、BK exit 4、corrupt readback exit 5。秘密値を含む障害制御は合成値を使い、stdout 1行、入力名・パスを含まないことを確認。Artifact 内訳は aggregate のみ。実 PrivacyDecision の再構成同値、root/UID/ID/hash/Policy の相違、inventory と制限 row の拒否を既存 ext4 テストで実測。追加の分類、row flag、output shape を変えた seal の結果はすべて `PRIVACY_POLICY_CONFLICT`（privacy phase）、Marker/rename なし。 [独立 CLI/Reader プローブ](independent_raw_evidence.md#独立実-cli--reader--amd-004-controls) · [G01 の全 node ID と実測出力](independent_raw_evidence.md#独立-g01-pytest) · [AMD-001–003 独立プローブ](independent_raw_evidence.md#実-cli--amd-001003-fault-controls--decision-各-field)

AMD-001–003 の独立 fault control で check-only/失敗 begin 前 abort 0、成功 begin 後の Discovery/Runtime/Factory/Seal 失敗では abort 1 と元の exit 分類、cleanup 失敗は補助の typed log のみ、publish 以後 abort 0 を観測。全 AMD state/失敗行列と全 Privacy/Reader の組合せの独立立証は未完。 [006](ENH-E11-G01_01__006_atomic_publish.md) · [007](ENH-E11-G01_01__007_bundle_readback.md)

## 実行・再現

固定候補 checkout で上記の各テスト/プローブを再実行できる。正負例の exact command、node ID、fixture、exit、実 stdout と必要な故障注入は実測出力を参照。候補・fixture・環境 identity は [001](ENH-E11-G01_01__001_candidate_identity.md) に記録した。

[実測出力](independent_raw_evidence.md) · [再実行用資料](independent_probe_inputs.md)

検証対象に対する production code、repo tests、migration、依存定義、凍結契約の変更は0件。
