# 238 — G01/P04 Fisher-Z numerical eligibility Owner adoption

**Date:** 2026-11-23 JST  
**Decision:** `DEC-G01-P04-FISHERZ-NUMERIC-01=A_ADOPTED`  
**Status:** `OWNER_NUMERICAL_DECISION_APPROVED / AMD003_FORMAL_09_PENDING / REVISED_S10_S11_PENDING`  
**Source docket:** `combined_review/237_20261123_g01_p04_fisherz_numerical_reliability_owner_decision_docket.md`  
**Stopped G01/P04/Trial01 START_SHA:** `b9910c9a382241a9a850fc57579badb9ccfa8b11`  
**Existing S10:** `3a63caa2d58c76c7f4289593713ee5c437e4ec91`

## Explicit Owner approval

> DEC-G01-P04-FISHERZ-NUMERIC-01はA案を採用する。float64のFisher-Z相関部分行列について、全候補(X,Y,S)で正定値性、κ₂(R)×np.finfo(float64).eps≤1e-6、左右の逆行列残差の無限大ノルム≤1e-8、有限な中間値、|partial_r|<1を検査し、不成立または判定不能ならFCI呼出前にfail-closedとする。これらは保守的な適格性基準であり、p値精度や因果的妥当性の保証とは扱わない。公開契約、P01/P03チェックポイント、既承認の科学的・独立検証・G01_999条件を維持し、DD・06・07の最小改訂とAMD-E11-G01-P04-003正式09案を作成せよ。

## Adopted numerical acceptance semantics

For **every** pair and conditioning subset in the previously approved exhaustive G01/P1-M06 Fisher-Z screen, use the verified effective float64 data correlation submatrix and require: n>|S|+3; finite strict positive-definiteness; finite 2-norm condition number times `np.finfo(np.float64).eps <= 1e-6`; finite inverse; both residuals `R@W-I` and `W@R-I` with matrix infinity norm (maximum absolute row sum) <=1e-8; finite derived Fisher-Z intermediates, and a finite partial correlation whose absolute value is strictly <1. No allowance for the Backend's partial-correlation clipping. If any relevant check is not possible or fails, refuse before FCI and do not create a Graph or success Marker. The thresholds are approved conservative screening controls, not certified forward accuracy or scientific validity.

Continue to verify all declared categories, the `chisq/gsq` floor and full conditioning coverage per `AMD-E11-G01-P04-001` and `AMD-E11-G01-P04-002`. No public E11 schema/version change; no completed P01/P03 modifications; no change to non-null BK/PAG semantics. This scientific numerical policy is approved **as a design decision and authoring authority only**. It does **not** itself approve the future formal AMD-003 09, S10 refreeze, or S11 coding permission.

## Required change management

Author prepares minimal `30_63`, P04 `06`, G01 `07`, and formal `AMD-E11-G01-P04-003` 09 candidate. Reviewer/Owner must independently approve the exact final amendment, then separately approve new immutable full SHA G01-S10, and separately issue G01/P04/Trial01 S11 authorization. No source implementation, verification fit, P04 checkpoint or G01_999 PASS is represented by this decision record.
