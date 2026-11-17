# ENH-E11 G01 P02 — Trusted Root, Atomic Publisher, Readback

**Document class:** Primary Execution Contract  
**Self-containment:** MUST — Assigned Coding Agentが本書だけでpackageのnormative execution responsibilityを理解できること。

- Gate: G01
- Trial: Trial01（未開始）
- Package: P02
- Parent 06 (traceability): 06_Ariadne_ENH-E11_G01_implementation_instruction.md
- P00 Plan (traceability): 06_G01_P00_work_package_plan.md
- Depends on: P01
- Status at issuance: DRAFT / CODING_NOT_AUTHORIZED

## 1. Purpose
private TrustedRootとimmutable multi-artifact run publicationを実FSで安全に確立する。

## 2. Effective Gate constraints applicable to this package

このpackageが守るべきGate-level semanticsを、Parent 06 / P00を読まなくても実行判断できる粒度で記載する。

G01は正式Gate IDでPxxはbounded Coding Unit。Local laneとProduct v2を分離し旧CLI/Web/API/DB/Workerは改変しない。strict version/Method/EstimatorとJCSのハッシュ対象を検証し、PAGをDAG/ATEへ変換しない。OS root/Privacy/Atomic Publishの不適格はfail-closed、SCI不確実性をPASSに変換しない。Coding Authorization前の実装は禁止。

## 3. In scope
Application Port `ContentReferencePort.verify`をCLI Concrete `LocalContentReferenceAdapter`が実装し、dirfd/O_NOFOLLOW等で中間symlink/path race拒否、同一FDでbytes SHA。`LocalPublicationPort.begin/seal/publish`はrun-scoped `LocalArtifactPublisher.begin/stage_bytes/validate/commit/abort`へ委譲し、0600/0700・file/dir fsync・Linux同一FS `renameat2(RENAME_NOREPLACE)`・公開後独立readbackを必須とする。EEXISTは完全readbackで同request hashの場合だけreuse。post-rename不定時の削除・上書き禁止。`LocalManifestReader.read_run`はMarker→Manifest→全Artifact/Lineage/Privacyのhash/type/size。

## 4. Explicitly out of scope
他GateのMethod実装、旧Product v2変更、根拠なしのScience PASS、行出力自己許可、未承認ACL/mount、既存run上書き、Package外の便乗変更。

## 5. Entry criteria / required evidence
Gate 06/07のFreeze・Coding Authorization・固定branch HEAD確認。Depends on P01の実装checkpoint full SHAとfocused検証を確認。矛盾/依存未成立はBLOCKED。

dependency checkpoint / source state等はfactとして外部参照してよい。Entry rule自体は本書内に記載する。

## 6. Required implementation
Application Port `ContentReferencePort.verify`をCLI Concrete `LocalContentReferenceAdapter`が実装し、dirfd/O_NOFOLLOW等で中間symlink/path race拒否、同一FDでbytes SHA。`LocalPublicationPort.begin/seal/publish`はrun-scoped `LocalArtifactPublisher.begin/stage_bytes/validate/commit/abort`へ委譲し、0600/0700・file/dir fsync・Linux同一FS `renameat2(RENAME_NOREPLACE)`・公開後独立readbackを必須とする。EEXISTは完全readbackで同request hashの場合だけreuse。post-rename不定時の削除・上書き禁止。`LocalManifestReader.read_run`はMarker→Manifest→全Artifact/Lineage/Privacyのhash/type/size。

## 7. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| G01-07-02/05/06；PUB01〜09、READ01〜07、PRIV03/04/06 | `uv run --no-sync python -m pytest tests/enhancement/enh_e11/g01 -q` | 競合・fsync・crash・symlink・ACL負例でoverwrite0、偽COMMITTED0、未対応FSはfail-closed。 |

## 8. Protected contract / Transition Debt constraints
Product v2の既存CLI/Manifest/Result contractを回帰保護する。未完成のGraph/Science/個票認可を完成と見なさない。G01受入境界は再審査待ちで、勝手にGate acceptanceを変更しない。

## 9. Checkpoint / reporting rule

Package completion時:

1. implementation-affecting changeをcommitする。
2. implementation checkpoint full SHAを固定する。
3. `implementation_checkpoint_report`を作成する。
4. `*_in_progress.md`へexecution statusを記録する。
5. report-only commitが別ならcheckpoint SHAと区別する。

## 10. Package completion criteria
競合・fsync・crash・symlink・ACL負例でoverwrite0、偽COMMITTED0、未対応FSはfail-closed。 集中検証の証跡・実装checkpoint SHA・Package Reportを揃える。未検証はBLOCKEDで止める。

## 11. External reference policy

source / previous checkpoint / test output / provenanceは外部参照してよい。本書のimplementation rule、prohibited scope、completion criterionをParent 06 / P00へ委譲してはならない。

## 12. Stop rule

- package scope完了 -> `PACKAGE_COMPLETE`
- continuation不能 -> `PACKAGE_BLOCKED`
- Gate PASS / FAILは判定しない。
- next packageへ勝手に先行しない。
