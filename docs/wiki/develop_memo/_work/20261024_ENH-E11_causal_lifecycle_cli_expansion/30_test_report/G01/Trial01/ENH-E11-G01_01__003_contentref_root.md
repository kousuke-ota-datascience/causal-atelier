# ENH-E11 G01 Trial 01 Test Item 003 — ContentRef / TrustedRoot

| 項目 | 記録 |
| --- | --- |
| Test Item ID | `003_contentref_root` |
| 正式判定 | **PASS** |
| 実行層 | enhancement / contract + real ext4 integration |
| Fixed Trial Candidate / actual tested HEAD | `72bcd6acaab6caf48827bf2bb6cd5e249afd658b` |
| TEST_START_SHA | `249bc48433e1472442fdbedfb9b848896e58d648` |
| 実行日 | 2026-11-24（JST） |
| Acceptance authority | [凍結 Gate 07](../../../10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md) |

論理キーの正負例、元 FD の bytes/sha、symlink/hardlink、inode 置換、hash 不一致、実 tmpfs 拒否を観測。実 ext4 で異なる UID と非 private mode の組合せを INPUT_SECURITY として拒否。CLI の hash 不一致は exit 3。

| 検証項目 | AC | DD ID / 検証目的 | 判定 |
| --- | --- | --- | --- |
| G01-07-02 | AC-01, AC-03 | REF01–04、PUB06、READ07、PRIV03/06 | PASS |

## 観測と根拠

`ContentRef.from_payload` と `LocalContentReferenceAdapter.verify` の字句拒否、実 root の inode 置換、実所有者・mode・種類・hash の照合を確認。 `test_content_reference_rejects_unsafe_file` の5変種、`test_ref_detects_real_inode_replacement`、`test_root_rejects_symlink_permissions_and_outside`、`test_tmpfs_root_is_rejected` が通過。ハッシュ不一致の CLI は exit 3、staging/Marker なし。異なる UID 65534 とディレクトリ mode 0755 の real ext4 root は `INPUT_SECURITY` で拒否された。同一所有者の unsafe mode と上記の複合正負例を記録した。 [G01 の全 node ID と実測出力](independent_raw_evidence.md#独立-g01-pytest) · [実 UID/mode 拒否](independent_raw_evidence.md#ext4-にある異所有者非private-mode-の-root)

## 実行・再現

固定候補 checkout で上記の各テスト/プローブを再実行できる。正負例の exact command、node ID、fixture、exit、実 stdout と必要な故障注入は実測出力を参照。候補・fixture・環境 identity は [001](ENH-E11-G01_01__001_candidate_identity.md) に記録した。

[実測出力](independent_raw_evidence.md) · [再実行用資料](independent_probe_inputs.md)

検証対象に対する production code、repo tests、migration、依存定義、凍結契約の変更は0件。
