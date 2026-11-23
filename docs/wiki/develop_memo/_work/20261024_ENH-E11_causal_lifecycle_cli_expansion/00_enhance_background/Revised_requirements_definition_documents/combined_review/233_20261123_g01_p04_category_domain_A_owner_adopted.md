# 233 — G01/P04 category-domain authority — Owner design decision A adopted

**Date:** 2026-11-23 JST  
**Decision:** `DEC-G01-P04-CATEGORY-DOMAIN-01=A_ADOPTED`  
**State:** `OWNER_DESIGN_ADOPTED / FORMAL_AMD002_09_NOT_YET_APPROVED / S10_S11_PENDING`  
**Original stopped Agent SHA:** `56889493d101b6c3c3a13a37dcd7cfd713dbf73a`  
**Frozen S10:** `a7003b359444af64cad0edbade0341243653a8bf`

## Owner's explicit direction

> DEC-G01-P04-CATEGORY-DOMAIN-01はA案を採用する。P1-M06専用の内部Design Profileにcategory_codesを追加し、宣言済みカテゴリ集合とDatasetの整数コードを厳密に照合する方針、および必要な内部Design入力互換性の変更を承認する。既承認の全条件付け集合検査、科学的意味、公開E11 Schema Version、P01/P03チェックポイント、独立科学検証・G01_999受入条件は維持し、最小範囲の契約修正と正式09改訂案の作成を進めよ。

Decision detail and alternative analysis: `combined_review/232_20261123_g01_p04_categorical_domain_owner_decision_docket.md`.

## Approved bounded semantic choice

- The authoritative P1-M06 **internal** Design input declares the full categorical code universe in `Design.variables[].category_codes`, required only for `measurement_scale=CATEGORICAL`. It has at least two distinct ascending integer codes; negative and noncontiguous codes are legitimate when exactly representable by the Dataset/Backend adapter. CONTINUOUS forbids this field.
- Observed Dataset codes must match the immutable declared universe exactly by membership, without coercion or `np.unique` inferring/replacing the declaration. Unobserved declared codes must remain in the full Cartesian conditional support checks, including empty strata and absent X/Y levels. Previously approved `E>=5` and all pair/subset pre-FCI eligibility tests remain.
- This is a strict **internal Design input compatibility** change, not new public E11 Study/Graph/Manifest/ContentRef wire fields or public schema version. Modified Design bytes change ContentRef sha256 and derived Study request_hash; consumers must verify the actual file bytes.
- The earlier general G01 Design schema draft is not to bypass the dedicated P1-M06 schema. Strict JSON Schema validation is supplemented by semantic verification of ordered codes and lexical exact-integer representation (integer-valued JSON float tokens such as `1.0`/`1e0` must not be silently retyped).
- No transfer of this exception to the 40 non-FCI Methods or other Gate. Preserve P01/P03 complete checkpoints, science/PAG/BK/provenance contracts, independent G01_999 review and no invented Backend PASS.

## Change-management boundary

The Owner authorizes the **design choice and document drafting**, not a new formal 09 approval, not a new S10 freeze, and not S11 Coding Agent reauthorization. The Author will prepare a separate reviewable `AMD-E11-G01-P04-002` with exact changed files and compatibility impact. Coding remains stopped until formal 09 → separate S10 → separate S11.
