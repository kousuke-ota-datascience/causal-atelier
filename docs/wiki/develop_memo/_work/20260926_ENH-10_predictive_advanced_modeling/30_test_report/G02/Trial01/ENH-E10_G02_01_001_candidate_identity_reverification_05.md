# ENH-E10 G02 Trial 01 — Test Item 001: Candidate Identity（reverification 05）

| 項目 | 記録値 |
| --- | --- |
| Fixed Trial Candidate | `fbd97c5b7a95084affe5e2381d85d86d0dfa2558` |
| completion report の previous failed candidate | `e9a5b412349b10ced45d822aa08a54b6d9df00ba` |
| Tested SHA（検証開始時 HEAD） | `1bf3026ba1918c8ca74af64318bdd42e90d7ed67` |
| 判定 | **PASS** |

## 再現コマンドと生出力

```bash
git cat-file -e fbd97c5b7a95084affe5e2381d85d86d0dfa2558^{commit}
git merge-base --is-ancestor e9a5b412349b10ced45d822aa08a54b6d9df00ba fbd97c5b7a95084affe5e2381d85d86d0dfa2558
git merge-base --is-ancestor fbd97c5b7a95084affe5e2381d85d86d0dfa2558 HEAD
git diff --numstat e9a5b412349b10ced45d822aa08a54b6d9df00ba fbd97c5b7a95084affe5e2381d85d86d0dfa2558 -- src tests pyproject.toml uv.lock alembic frontend
git diff --name-status fbd97c5b7a95084affe5e2381d85d86d0dfa2558 HEAD -- src tests pyproject.toml uv.lock alembic frontend
git status --short
```

```text
object check: exit 0
previous_ancestor_exit=0
candidate_ancestor_head_exit=0
66  0  src/ariadne/capabilities/predictive/explanation_runner.py
4   2  src/ariadne/capabilities/predictive/shap_backend.py
103 0  tests/product/test_enh_e10_g02_p02_shap_backend.py
post-candidate semantic paths: <none>
working tree at test start: clean
```

## 観測事実と解釈

事実: candidate object は存在し、直前の独立 FAIL candidate `e9a5b41` の descendant であり、さらに tested SHA の ancestor である。remediation diff は production 2 ファイルと test 1 ファイル、合計 173 additions / 2 deletions で空ではない。candidate 後の差分は 09 remediation instruction と completion report の文書のみであり、`src/`、`tests/`、依存 lock、migration、frontend に意味的変更はない。

解釈: completion report からのみ取得した candidate を、HEAD に置換せずに同一の製品意味状態として検証できる。previous-failed guard、非空 remediation、post-candidate semantic-state guard、clean-tree guard をすべて満たす。AC 対象外の META 項目だが、以降の Test Item の有効な前提として **PASS**。

## 監査手順の内訳

1. completion report の `FIXED_TRIAL_CANDIDATE_SHA` フィールドを唯一の candidate 入力として読んだ。依頼本文・HEAD・過去 report の SHA を candidate 値として採用していない。
2. `cat-file` により commit object であることを確認した。tag/blob/tree を candidate と誤認していない。
3. `merge-base --is-ancestor` の exit `0` を、previous-failed candidate からの remediation lineage の根拠とした。SHA 文字列の一致や commit date は ancestry の代用にしていない。
4. semantic path に限定した `numstat` により、説明用文書だけでない product/test remediation を確認した。
5. candidate と tested HEAD の semantic path diff が空であることを確認した。したがって documentation-only HEAD を実行環境として用いても candidate 製品状態を変更していない。
6. evidence 作成前の `git status --short` が空であることを確認した。後続の report 作成で発生した untracked files はこの clean-tree 観測に含めていない。

## remediation diff の意味

`explanation_runner.py` は `SHAP_TREE` を actual EXPLAIN stage へ dispatch する経路、`shap_backend.py` は provider value の shape 正規化、P02 test は binary/regression full DAG と canonical provenance を追加している。これは前回 04 で実証された `NOT_APPLICABLE` stage failure に直接関係する semantic diff である。

## 非対象と限界

本 item は candidate の正当性を検証する META item であり、SHAP/LIME の数値正しさ・provenance・G01 compatibility を判定しない。それらは item 030–090 の実行 evidence を要する。candidate identity が PASS であることは Gate PASS を単独では意味しない。
