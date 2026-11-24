# ENH-E11 G01 Trial 01 Test Item 006 — Atomic publish / session

| 項目 | 記録 |
| --- | --- |
| Test Item ID | `006_atomic_publish` |
| 正式判定 | **BLOCKED** |
| 実行層 | enhancement / real ext4 integration + fault controls |
| Fixed Trial Candidate / actual tested HEAD | `72bcd6acaab6caf48827bf2bb6cd5e249afd658b` |
| TEST_START_SHA | `249bc48433e1472442fdbedfb9b848896e58d648` |
| 実行日 | 2026-11-24（JST） |
| Acceptance authority | [凍結 Gate 07](../../../10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md) |

実 ext4 の同一/異なる hash の競合と SIGKILL 前後、実 syscall fault と post-rename fsync 不定時の型付き結果を観測。独立 abort の全 state については証拠未完。

| 検証項目 | AC | DD ID / 検証目的 | 判定 |
| --- | --- | --- | --- |
| G01-07-05 | AC-03, AC-06 | PUB01–05/07–09、AMD-002/003 | BLOCKED |

## 観測と根拠

`LocalArtifactPublisher` の real ext4 で同じ run ID の2プロセス競合（same/different hash）、rename の前後で SIGKILL、renameat2 の ENOSYS/EINVAL/EOPNOTSUPP/EXDEV、fsync 障害と post-rename indeterminate を実行した。上書き0、危険例の COMPLETED 0、同一候補の再利用は Reader 成功後。pytest の Linux fault は対象 syscall の故障注入を含む。 [G01 の全 node ID と実測出力](independent_raw_evidence.md#独立-g01-pytest)

AMD-002/003 は型付き fault を外部 Port 境界に入れ、実 ext4 staging を併用。成功 begin の永続化前に Discovery・Runtime・Factory・Seal が失敗すると、独立保持の tuple で Abort を1回呼び、final run 0。publish 呼出後の Application abort は0。S11→候補の source diff では具体 Publisher の begin/validate/commit/abort と Adapter seal/publish の変更なし。既存テストの正当な STAGING abort、異なる run/token/root/hash/issuer/policy/sink、再 abort を実行した。 [AMD-001–003 独立プローブ](independent_raw_evidence.md#実-cli--amd-001003-fault-controls--decision-各-field) · [G01 の全 node ID と実測出力](independent_raw_evidence.md#独立-g01-pytest)

BLOCKED の範囲は AMD-003 の全 state （PREPARING/PUBLISHING/COMMITTED/INDETERMINATE と正当な pre-publish VALIDATING）の独立した facade ケース、セッション両方の staged bytes と pre-existing run の個別比較、実 publish 後の全注入分類。観測した物理 no-clobber のケースは PASS。

## 実行・再現

固定候補 checkout で上記の各テスト/プローブを再実行できる。正負例の exact command、node ID、fixture、exit、実 stdout と必要な故障注入は実測出力を参照。候補・fixture・環境 identity は [001](ENH-E11-G01_01__001_candidate_identity.md) に記録した。

[実測出力](independent_raw_evidence.md) · [再実行用資料](independent_probe_inputs.md)

検証対象に対する production code、repo tests、migration、依存定義、凍結契約の変更は0件。
