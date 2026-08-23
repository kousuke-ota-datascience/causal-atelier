# ENH-E8 G03 Gate Contract Amendment A01

- Document class: Gate Contract Amendment
- Status: `APPROVED/APPLIED`
- Gate: `G03`
- Amendment ID: `A01`
- Amendment date: `2026-08-23`
- Trigger: G03初回retrospective reconstruction後に追加されたCausal Estimation bugfixの再評価

## 1. Amendment reason

G03のoriginal retrospective 06/07は、Causal Estimation actionがhidden Identification form validationから独立し、selected Identification Resultのexecution lineageからsubmission入力を復元するsemantic claimを定義していた。

その後の追加bugfix evidenceから、同じsemantic claimをruntime上で成立させるために、次の2点がblocking conditionであることが明確になった。

1. **bootstrap timing safety** — Estimation submission moduleのhandler attachmentを`window.load`まで遅延すると、DOM表示後からhandler attachmentまでの間にuser interaction raceが存在し得る。Estimation buttonはその期間にnative/shared-form submitへfallbackしてはならない。
2. **frontend asset delivery** — Estimation submission moduleがcanonical Compose frontend runtimeで確実に配信・読取可能でなければ、button ownership contract自体が成立しない。追加実装ではfrontendをhost bind mountからimage buildへ変更し、static filesのread permissionをimage build時に正規化している。

original G03 claimそのものは正しいが、original 07は上記timing / delivery conditionをblocking Acceptance Criterionとして十分に具体化していなかった。

## 2. Why 08 remediation is insufficient

本件はformal Independent Verificationの`FAIL`後に発生したTrial remediationではない。G03はまだformal PASS / FAIL / BLOCKED decisionを持たず、Fixed Verification Candidateも確定していない。

また、追加事実は単一candidateの局所的修正方法ではなく、Acceptance Criteria / verification coverageの不足を示す。したがって`08`ではなく`09`でcontract completenessをamendし、06/07をre-baselineする。

## 3. Before / After semantic change

### Before

- Estimation actionはhidden Identification native validationに阻害されない。
- selected Identification Resultのexecution prefillをlineage authorityとする。
- presentation moduleはapp runtime ready後にsubmission moduleをloadする。

### After

上記に加えて、次をnormative conditionとする。

- Estimation buttonはsubmission handler attachment前から`type="button"`であり、handler未ready期間はdisabledである。
- handler attachment完了後にのみbuttonをenableする。
- bootstrapは`window.load`待ちによるuser-visible interaction gapを作らず、app runtime declaration後の`DOMContentLoaded`時点でsubmission module loadを開始する。
- canonical Compose frontend runtimeはcurrent sourceの`causal_estimation_submission.js`をreadable static assetとして配信する。
- verificationはhandler-ready最終状態だけでなく、**handler loadを意図的に遅延させたpre-ready state**でもnative submit fallbackがないことを確認する。
- historical product regression testが旧bootstrap implementation detailをassertしてstaleになっている場合、そのtestをG03 PASS evidenceとして無条件に使用しない。

## 4. Affected Acceptance Criteria

original `G03-AC01` / `G03-AC02`をtemporal bootstrap semanticsまで具体化し、次のblocking ACを追加する。

- `G03-AC11` — handler attachment前のEstimation buttonは`type="button"`かつdisabledで、native/shared-form submitへfallbackしない。
- `G03-AC12` — app runtime declaration後、`DOMContentLoaded`を起点としてsubmission module loadを開始し、`window.load`待ちのinteraction raceを作らない。
- `G03-AC13` — canonical Compose frontend runtimeが`/causal_estimation_submission.js`をcurrent sourceからHTTP successで配信し、nginx processからread可能である。
- `G03-AC14` — regression evidenceはcurrent implementation semanticsを検証し、obsoleteなexact source-string assertionをPASS authorityにしない。

## 5. Implementation evidence / provenance

Initial G03 reconstruction後のrepository差分では、次が変更されている。

- `frontend/causal_estimation_submission.js`
  - current blob: `d0d22e6fbbac4df5492c4f100849c0b0b895cbe4`
  - `#run-estimation`を優先してbuttonを取得し、handler ready後に`disabled=false`とする。
- `frontend/causal_stage_presentation.js`
  - current blob: `ac73d00f2ee8402083d23177c3e8f0036f45ddd5`
  - Estimation buttonを即時`type=button` / disabled化し、bootstrap triggerを`window.load`から`DOMContentLoaded`へ変更する。
- `Dockerfile.frontend`
  - current blob: `c8fb2d6a7666266b6145109b973c97a07f4aedd1`
  - frontend / nginx configをimageへcopyし、static file permissionを正規化する。
- `compose.yaml`
  - current blob: `3f34951762c3919b2d2a98024a343da33ad3a089`
  - frontend serviceをhost bind mount方式から`Dockerfile.frontend`によるbuild方式へ変更する。

Historical regression artifact `tests/product/test_enh_e9_estimation_submission_regression.py` はcurrent blob `89f91cb950f14444269f323c4a2ab8dd59c70438` のままであり、旧`window.load`および旧button lookup source stringをassertしているため、current implementationに対してstaleである。

## 6. Protected passed-Gate impact

次のENH-E8 protected semanticsは変更しない。

- G01 Project Return Navigation
- G02 Causal/Predictive Stage Content separation
- canonical Causal Navigation Stage catalog
- API route grammar
- DB / persistence schema
- backend causal estimation semantics
- Identification Result / execution lineage semantics

frontend Compose packaging変更は、G03 required static assetをcanonical runtimeへ配信するためのimplementation/runtime delivery boundaryとして扱い、新しいproduct API / persistence semanticsを導入しない。

## 7. Trial handling

G03は本amendment時点でformal Independent Verification未実施である。

したがって:

- Trial番号は増加させない。
- failed candidateを捏造しない。
- G03 Trial01のFixed Verification Candidateは、A01適用済み06/07に対するverification開始直前のexact repository commitとして将来固定する。

## 8. Approval evidence

2026-08-23、Human ownerから「追加bugfixを行ったため、02_因果推論の使い方を再評価し、Enhance Instructionを修正または追加する」旨の明示指示を受け、本追加bugfixをENH-E8後追い証跡へ反映することが承認された。

本amendmentは既存G03 semantic claimを緩和せず、追加bugfixで判明したblocking runtime/verification conditionを明示する方向にのみ強化する。

## 9. Required re-baseline artifacts

- `06_Ariadne_ENH-E8_G03_implementation_instruction.md`
- `07_Ariadne_ENH-E8_G03_test_instruction.md`
- `README_10_G03.md`
- `../../00_enhance_background/80_contract_amendment_log.md`

A01適用後は、上記re-baselined 06/07をG03 effective primary contractsとする。
