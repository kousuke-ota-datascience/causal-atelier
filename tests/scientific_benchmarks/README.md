# ENH-E1a Scientific Benchmark data

`SB-E1A-001`〜`010`は、固定したコード上のDGPから作成するSynthetic dataである。

`SB-E1A-011` は `statsmodels.datasets.longley` に同梱されたLongley dataの共変量分布を使うSemi-synthetic benchmarkである。TreatmentとOutcomeは保存データではなく、既知のコード上DGPで生成する。

- Source: J. W. Longley (1967), *An Appraisal of Least Squares Programs from the Point of View of the User*, JASA 62(319), 819–841; statsmodels dataset metadataがNIST Longley dataをsourceとして記録している。
- Distribution: statsmodels package fixture (`statsmodels.datasets.longley`)
- Distribution license: statsmodels BSD-3-Clause (`LICENSE.txt`)
- Network: 実行時の外部network accessなし
- Preprocessing: `GNPDEFL`と`GNP`を選択し、各列を平均0・標準偏差1に標準化し、固定順序で30回反復する。共変量はseed間で固定する。
- Known DGP: `P(T=1|X)=logit^{-1}(0.8 X1 - 0.5 X2)`、`Y=2T+0.7X1-0.4X2+ε`
- Ground truth: ATE = ATT = 2.0
