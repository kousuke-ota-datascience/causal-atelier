# ENH-E11 G01 Trial 01 P01 Execution Status

> **Document class:** Evidence Artifact
> **Self-containment:** MUST for own responsibility.

> **Evidence self-containment:** この報告に状態・実施内容・観測結果・判断理由を記録する。

- Gate: G01
- Trial: 01
- Package: P01
- Execution status: PACKAGE_COMPLETE
- Instruction: [P01 06](../../../../10_enhance_instruction/G01/06_G01_P01_local_contract_codec.md) · [AMD-E11-G01-P01-003](../../../../10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P01-003_Gate_Contract_Amendment.md)
- Starting SHA: `af304408e6daa37d395e0dc6ca2ba0c173cadd65`
- Latest implementation SHA: `ae40ab9e7a942a4aa97d7cde3c8ea34ba3686c96`
- Timestamp: 2026-11-25T02:02:23+09:00

State: PACKAGE_COMPLETE

## 1. Completed work

S09-JCS-01 の限定修正を完了した。`jcs.py` の `_number` は binary64 の最短表現を整数の位置計算と文字列操作で整形する。`test_jcs_context_independence.py` を追加し、独立数値ベクトル、Decimal の状態保存、実 ext4 の公開・Reader を確認した。変更はこの2件に限る。

## 2. Remaining work

P01 修正の残実装なし。記録273に基づく置換候補の Assembly、独立 S09 と G01 受入の再評価が後続。T3 正式実行は未認可。

## 3. Observed failures / blockers

旧 codec の precision 6 では `0.123456789` が `0.123457` に変わり、新規回帰が終了コード1で失敗した。修正版の必須回帰は通過した。既存 LightGBM ガードの FAIL とナビゲーションの影響範囲外判定を Owner 記録269/270の条件に従い保持した。P01修正の未解消 blocker はない。

## 4. Verification executed

| Command / method | Exit | Result |
|---|---:|---|
| `.venv/bin/python -m pytest -q --tb=short 'tests/enhancement/enh_e11/g01/contract/test_jcs_context_independence.py::test_numeric_bytes_digest_and_parse_do_not_depend_on_decimal_context[precision-6]'`（旧実装） | 1 | 1 failed、既知丸めを再現 |
| G01 全件、Scientific Core、関連 Product の必須回帰（コマンドはチェックポイント報告 §5） | 0 | 274 passed、2 deselected、11 warnings |
| 既存 Node/V8 の `JSON.stringify` と制限付き context の binary64 数値比較 | 0 | 有限値106,105件で一致 |
| 旧候補の実 ext4 バンドルを修正版 Reader / CLI で検証 | 0 | 読取りと同一要求の再利用を確認。異なる要求は exit 5 で拒否し、全成果物バイトが照合前後で一致 |

## 5. Relevant commits

- S10 凍結 `4a355403c2a66a76a6e2965e16fdf7637258e33e`
- S11 記録兼実行開始 `af304408e6daa37d395e0dc6ca2ba0c173cadd65`
- PACKAGE_CHECKPOINT_SHA `ae40ab9e7a942a4aa97d7cde3c8ea34ba3686c96`
- 旧 P01 チェックポイント `9bff61f0eae25236f95f31f2cd3e7c81291f0167`、旧 P01 証拠 `4248ca24204ed8ede27527191b1a53d9ced1ff5a`
- 旧 Fixed Trial Candidate `72bcd6acaab6caf48827bf2bb6cd5e249afd658b`、旧独立検証証拠 `2e56c2a04f4d11d10fdcb7b3ad5c148ab6747d91`

## 6. Next required action

P01 の端末結果は `PACKAGE_READY`。Assembly 担当は旧 P01→P02→P03→P04→P05→修正 P01 の祖先鎖を照合し、置換候補を確定する。 [Implementation Checkpoint Report](E11-G01_01_P01__checkpoint.md)
