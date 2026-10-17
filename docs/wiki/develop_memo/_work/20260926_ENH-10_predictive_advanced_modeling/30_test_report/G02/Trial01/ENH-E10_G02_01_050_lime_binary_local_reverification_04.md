# ENH-E10 G02 Trial 01 — Test Item 050: LIME Binary Local（reverification 04）

AC-05。`test_enh_e10_g02_p03_lime_backend.py` を含む focused command は 10 passed / exit 0。

binary provider probe は `PROBABILITY` scale、non-empty signed contributions、preprocessed feature representation、TEST row identity、TRAIN reference、per-row effective seed、provider `lime` version、frozen 2000 samples/default parametersを検証した。one-hot `group=A` は `categorical_feature_indices=[1]` として provider configuration に渡される。

binary target は positive-class probability であり、reference の raw TRAIN rows は persisted provenance に含まれない。**PASS**。
