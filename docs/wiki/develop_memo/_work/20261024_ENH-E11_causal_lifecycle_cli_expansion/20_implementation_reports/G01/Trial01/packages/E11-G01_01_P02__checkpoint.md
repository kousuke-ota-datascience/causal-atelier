# ENH-E11 G01 Trial 01 P02 Implementation Checkpoint Report

> **Document class:** Evidence Artifact
> **Self-containment:** MUST for own responsibility.

> **Evidence self-containment:** この報告に状態・実施内容・観測結果・判断理由を記録する。

- Project: Ariadne
- Enhancement: ENH-E11
- Gate: G01
- Trial: 01
- Package: P02
- Package status: PACKAGE_COMPLETE
- Instruction: [06_G01_P02_atomic_publication_reader.md](../../../../10_enhance_instruction/G01/06_G01_P02_atomic_publication_reader.md)
- Starting commit: `bcbad6b794e6b9e2b3fd899a20784b646f7e6764`
- Implementation checkpoint SHA: `3a76a0aa1698037354b284ba7b5a875300473ce6`
- Report commit SHA: PENDING
- Timestamp: 2026-11-24T08:30:26+09:00

## 1. Package objective

同一 FD での入力検証、atomic no-clobber 公開、独立 Reader を実装する。

## 2. Implementation summary

同一 FD での入力検証、atomic no-clobber 公開、独立 Reader を実装した。

## 3. Changed files

| Path | Change | Reason |
|---|---|---|
| `src/ariadne/shared/local_fs.py` | add | Linux の実効 UID と private dirfd、同一 FS とファイル同一性の確認。 |
| `src/ariadne/capabilities/causal/ports/content_ref.py` | add | ContentRef、公開、Reader、staging の境界と型。 |
| `src/ariadne/capabilities/causal/ports/local_io.py` | add | ContentRef、公開、Reader、staging の境界と型。 |
| `src/ariadne/scientific/ports/artifacts.py` | add | ContentRef、公開、Reader、staging の境界と型。 |
| `src/ariadne/interfaces/cli/local_causal/content_io.py` | add | 同一 FD のバイト列と ContentRef の SHA-256 の照合。 |
| `src/ariadne/interfaces/cli/local_causal/publication.py` | add | private staging、Publisher の独立した PrivacyDecision 再評価、Manifest/Marker、fsync と no-clobber 公開。 |
| `src/ariadne/interfaces/cli/local_causal/manifest_reader.py` | add | 公開済みの Marker・Manifest・成果物と上流参照の readback。Graph-negative の型付き四フィールド診断、run・operation・Method・理由、Graph-null と inventory を照合。 |
| `tests/enhancement/enh_e11/g01/integration/test_local_publication.py` | add | P02 の focused Linux FS 検証。 |

## 4. Observable implementation facts

Owner 承認 212・214・216 と再開ハンドオフ 217 を照合し、凍結 SHA `c37cd93d981a6d3777e20bd46b26bc3ae9b2c1f8` の [P02 契約](../../../../10_enhance_instruction/G01/06_G01_P02_atomic_publication_reader.md) を適用した。指定リポジトリへの remote、`feature/ariadne_mvp_e11`、クリーンな作業ツリー、凍結後の管理記録の差分、Trial 01 に正式な FAIL・08・既存 P02 チェックポイントがないことを確認した。P01 チェックポイント `9bff61f0eae25236f95f31f2cd3e7c81291f0167` は祖先であり、その実装は維持した。

`uv.lock` の凍結・HEAD・作業ツリーの Git blob は `2b83110e86b26b7969fbddf8f98a727370ae19f7`。実ファイルの SHA-256 は `1d92a472fc3c750c90458a40ae5a09ba3feefbd3d99eee61b0cdbff00d31cffb`。

元の証拠コミット SHA `714da741d09b1722e0755bc97cbacc4fb6ad327d`（コミット時刻 2026-11-23T13:13:11+09:00）。 Timestamp は報告の再編時刻。

## 5. Focused verification

| Command | Exit code | Result summary |
|---|---:|---|
| `.venv/bin/python -m pytest -q tests/enhancement/enh_e11/g01 tests/product/test_cli_contract.py tests/product/test_enh_e4_g07_p03_cli_boundary.py tests/product/test_enh_e4_g04_result_artifact_contract.py` | 0 | 120 件通過。 |

**120 passed**。P02 38 件、P01 69 件、Product 13 件。Linux 6.18.58.1-microsoft-standard-WSL2、Python 3.12.16、実効 UID 1000。実 FS は作業ツリーの ext4 に作成した private 一時ディレクトリ。XFS は未実測。P02 テストソースと合成 fixture の SHA-256 は `34c3d3d09d26294b11ae025cb5f8e59627f30cf0823e74a3c4ee6ae1889738d7`。テストランナーは Python 3.12 の fork に関する非推奨警告を 11 件出した。

| DD / Gate Test | Lifecycle / Layer | 観測結果 |
| --- | --- | --- |
| REF01–04、PRIV03/04/06 / 07-02 | enhancement / integration | 実 FD のハッシュ・サイズ照合が成功。モード変更、symlink、hardlink、同一バイト列での inode 置換、改変、欠落、tmpfs Root を拒否。 |
| PUB01–04 / 07-05 | enhancement / integration | Manifest の fsync にカーネルの fault injection で ENOSPC を返し、Marker と公開先が作られないことを確認。rename の直前・直後に子を SIGKILL し、前者は公開先なし、後者は Reader で完全な bundle を確認。 |
| PUB05–09 / 07-05 | enhancement / integration | ext4 上の実 renameat2 と親ディレクトリ fsync。二プロセス競合では公開ディレクトリが一件、上書きゼロ。同一候補は完全 readback 後に再利用し、異なる request は RUN_ID_CONFLICT。renameat2 の ENOSYS・EINVAL・EOPNOTSUPP・EXDEV はカーネルで注入し、公開されなかった。rename 後の fsync エラーは INDETERMINATE。 |
| READ01–07、MAN03–06 / 07-06 | enhancement / integration | 両方の合成 bundle を実公開して独立 Reader で確認。破損 Manifest、旧版、内容とハッシュを再計算した不正診断、Status 理由不一致、余剰ファイル、封印後の変更を拒否。 |
| PUB04/07、PRIV01–06 / 07-05/06/11 | enhancement / integration | 同値の別インスタンスを受理。欠落・拒否・run/hash/root FD/UID の不一致、Policy 拒否、staging 置換、個票 artifact は Marker/rename 前に拒否。 |

ENOSPC は容量枯渇ではなく syscall の戻り値の注入で検証した。renameat2 の ENOSYS 注入は raw syscall で確認し、glibc 経由では EINVAL を観測した。反映先は未作成だった。rename 後の fsync エラー検証は故障位置をテストで指定し、rename と Reader の実 FS 操作を使用した。

Graph-negative は合成データで検証した。実 FCI の科学的負結果の正当性と G01 の独立受入・G01_999 は保留。

## 6. Dependency / handoff state

- Dependencies satisfied: YES
- Next package(s): P04 完了後の P05 統合
- Handoff facts: P01 を照合した。 [Package Execution Status](E11-G01_01_P02__status.md)

## 7. Protected contract / Transition Debt impact

Product 回帰の観測結果は §5 に記録した。DEFERRED_PRODUCT_POLICY_BRIDGE の未完了依存は維持される。

## 8. Known limitations / unresolved observations

ext4 で検証した。XFS、実 FCI の科学的負結果、独立受入は未検証。


## 9. Semantic warning

チェックポイントは Package 単位の実装証跡。Fixed Trial Candidate と Gate PASS は別の成果物で確定する。
