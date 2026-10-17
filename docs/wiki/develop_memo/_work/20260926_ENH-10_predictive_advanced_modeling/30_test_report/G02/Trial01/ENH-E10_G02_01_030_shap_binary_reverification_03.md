# G02 Trial 01 — 030 shap_binary (reverification 03)

## Scope / facts

AC-03, with supporting AC-09/10/11 adapter evidence. The G02 suite executed `test_enh_e10_g02_p02_shap_backend.py` on fixed synthetic binary data. It trained LightGBM, invoked `SHAP_TREE`, and asserted raw `LOG_ODDS`, two named global feature mappings, and two local rows from row ordinals 0/1.

The backend uses `tree_path_dependent`, raw model output, and frozen additivity comparison `atol=1e-6, rtol=1e-5`. Suite result: `13 passed, 1 warning`, exit 0. The only warning was SHAP's provider notice that binary classifier values may be list-of-ndarray; no assertion or product behavior failed.

## Interpretation / result

The binary SHAP adapter produces the required raw-scale global/local representation. Model Card-wide provenance is independently assessed in item 080 rather than assumed here. Target/candidate identities are in item 001. **Result: PASS.**

## 入力・判定根拠・再現条件

fixture は fixed synthetic binary data、LightGBM model、feature order を持つ fitted model、row ordinal list、`local_size=2` である。観測対象は raw library array の形状そのものではなく、canonical result の output scale、base value と contribution の mapping、global aggregation、local row identity、tree-path-dependent reference である。

provider warning は SHAP の binary output representation に関する通知であり、adapter は canonical shape への変換後に assertion を満たした。warning を PASS 根拠にも FAIL 根拠にも使っていない。item 010 の exact suite command を再実行し、`test_enh_e10_g02_p02_shap_backend.py` と 13-test suite exit `0` を確認する。
