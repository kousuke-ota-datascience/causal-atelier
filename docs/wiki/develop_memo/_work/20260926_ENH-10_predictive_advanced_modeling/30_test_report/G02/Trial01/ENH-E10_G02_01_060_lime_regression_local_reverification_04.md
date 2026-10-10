# ENH-E10 G02 Trial 01 — Test Item 060: LIME Regression Local（reverification 04）

AC-06。focused command は LightGBM regression provider fixture を実行し、`PREDICTION` scale と non-empty provider contributions を確認して 10 passed / exit 0。

LIME runner integration は transformed TRAIN reference と TEST local rows を使用する。reference contract は `predictive-explanation-reference/1`、partition `TRAIN`、sampling seed を保存し、最大 500 rows・without replacement の sampling test は同 seed で同 hash、seed 19 で異なる hash を確認した。

instance/reference identity、effective seed、parameters、provider/runtime provenance は explanation result / artifacts / Model Card で runtime audit 対象とした。LIME local regression behavior は **PASS**。
