# ENH-E10 G02 Trial 01 — Test Item 080: Provenance and Model Card（reverification 04）

AC-09 / AC-11。LIME runtime integration test は `method_provenance` を Explanation Result に、同一値を `explanation_provenance` として Model Card に記録することを確認した。両 JSON artifact は各 Result payload と等値である。

provenance contains: `method_id=LIME_TABULAR`、method version、model/task/schema/preprocessor identity、preprocessor canonical hash、feature order/hash、one-hot categorical feature indices、TEST row ordinals、TRAIN reference schema/count/hash/seed/partition、output scale、sampling、effective seeds、frozen method parameters、provider name/version、runtime versions、predictive-not-causal limitation。

raw TRAIN features は persisted provenance に含まれない。API/worker artifact test も PASS。LIME result/artifact/Model Card consistency と terminology boundary は **PASS**。

ただし SHAP stage provenance は item 030/040 の product FAIL により生成されないため、SHAP を含む AC-09 overall は FAIL となる。
