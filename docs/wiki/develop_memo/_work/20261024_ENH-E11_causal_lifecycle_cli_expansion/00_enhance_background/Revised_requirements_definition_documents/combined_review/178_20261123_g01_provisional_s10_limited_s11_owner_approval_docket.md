# G01 provisional S10 and limited S11 — separate Owner approval docket

**Date:** 2026-11-23 JST
**Controlling Owner policy:** `DEC-G01-EXEC-01=ADOPTED`, [177](177_20261123_dec_g01_exec01_owner_adopted_evidence_rephasing.md). `DEC-PREPCODE-01=B` remains applicable to other Gates.
**Docket state:** `S10_REVIEW_PACKET_READY / S10_OWNER_APPROVAL_NOT_GRANTED / S11_OWNER_APPROVAL_NOT_GRANTED / ALL_EXTERNAL_EVIDENCE_PENDING`.
**Author candidate source commit (not an Owner Freeze):** `a05fd072cbb82a7c6e43f45e7208e078f0784a2b`, branch `prototype/ariadne_mvp`. At actual S10 approval explicitly pin/verify one `G01_FROZEN_SOURCE_FULL_SHA` and `uv.lock` blob/SHA256 (not inferred from current branch HEAD); if other active contracts changed, recheck their exact content and impact before approval.
**Author normative inventory:** `s09_post_reconciliation_document_snapshot_draft14.json` 402 paths; G01 source candidate `s09_g01_scoped_review_inventory_draft8.json` 11 OWN_GATE + 69 COMMON_SHARED + 5 IMPACT_SAMPLE = 85 initial semantic candidates, 317 future Gate NOT_REVIEWED. Source SHA inventory is not an independent audit.

## A. Provisional G01-S10 — Owner action 1 (NOT YET ISSUED)

**Proposed Owner approval text:** “G01の共通・固有実装契約06/P00〜P05/07、対象E11 v1 Wire/Port/Privacy/Publisher/Reader、P1-M06 FCI、既存Product v2の保護条件と既定の独立07/999受入項目について、指定full SHAを暫定S10契約として固定する。独立S09/B02/B04/B05の未実行・未承認を明示的に留保し、G01_999までの必須判定として維持する。この承認単独ではCoding Agentを起動しない。”

**S10 fixed WHAT:** `G01` only, implementation 06, P01–P05 and P00 traceability, test 07 G01-07-01..12 / 001..013 / 999, active P1-M06 Config/Question/Design only, six public v1 Schema, other G01/common contracts within actual dependency closure, seven shared Agent prompts, `causal-analysis-spec/2` protected. Preserve DISCOVER-only no dummy Effect; E11 Graph endpoint fidelity/ContentRef/JCS, FCI`fisherz/chisq/gsq`, effective named Backend, private same-UID Linux atomic Publisher/Reader, deny row export, strict typed preflight and error phases. No future-Gate Method implementation.

**S10 exceptions (not approvals of correctness):**

| ID | Fact at provisional freeze | Unwaived finish criterion | Responsibility / gate |
| --- | --- | --- | --- |
| X-S09 | Independent common+G01 audit `NOT_RUN` | Truly separate Reviewer with exact Source SHA, findings, correction/re-freeze as needed | `G01_999` blocker |
| X-B02 | Approved Python3.12 Draft202012 six common + three active P1-M06 instances `NOT_RUN` | Runtime standard validator and strict public/method positive-negative/semantic joins | `G01_999` blocker |
| X-B03 | Cross-wire author-only; no E11 actual Reader/OS proof | Independent semantic audit plus real FS/atomic marker/Reader/privacy fail-closed and G01-07-01..07 | `G01_999` blocker |
| X-B04 | Python3.12 ENV-BASE `causal-learn==0.1.4.8` real `fisherz/chisq/gsq` fits `NOT_RUN` | Actual selected Backend API, versions, exact `node_names`, categorical preflight, no stdout/stderr leakage, negatives | `G01_999` blocker |
| X-B05 | Complete independent MAG/PAG oracle/BK science `NOT_ACCEPTED`; known upstream BK bug | Independent MAG/PAG reference, forced/uncertain endpoints, no improper BK orientation, tested BK remedy and console containment, real T2→preregister T3 | `G01_999` blocker |
| X-B06 | Author contract propagated, independent final S09 `NOT_RUN` | Exact source/ABI/legacy v2 and test independence verified | `G01_999` blocker |

**Non-negotiable:** non-null BK (including empty BK) typed `BACKEND_SEMANTICS_UNVERIFIED` exit4 pre-FCI until independently accepted correct implementation. This preserves the BK-positive final acceptance, not a waiver. No synthetic or author-only evidence may substitute for independent PASS. Future Gate S09/S10/S11 and genuine upstream 999 remain as DEC-PREPCODE-01=B.

**S10 owner result field:** `NOT_DECIDED`; once approved, record `APPROVED_PROVISIONAL` / `REJECTED`, actual full frozen SHA, source/lock digest, contract scope, exception ledger and date in a distinct Owner decision record. Do not mutate this preparatory text to imply silent approval.

## B. Limited G01-S11 — Owner action 2 (SEPARATE, ONLY AFTER S10)

**Proposed Owner approval text:** “暫定S10で固定したG01のfull SHA・source/lock・06/P01〜P05/07を対象に、G01のCoding Agentによる実装・開発者テストを限定承認する。未取得の独立S09、実Python3.12 B02/B04、独立B05及び実FS/Reader/T2/T3/独立07は、G01_999合格の必須条件として保持する。科学的PASS、Gate999、他Gate実装、本番科学的提供は許可しない。”

**Entry guard:** A **real distinct Owner provisional S10 record** with exact 40-hex freeze SHA and required 06/07/Method/source/lock identity; separate affirmative Owner S11 decision naming `GATE_ID=G01`, `EXECUTION_MODE=WORK_PACKAGE`, permitted `P01,P02,P03,P04,P05` (P00 planning only), frozen base commit, `uv.lock` and applicable tests/paths. Orchestrator must refuse missing/different approval, dirty/changed selected normative source or non-G01 Method.

**Permitted after S11:** coding assigned E11 new local CLI and shared implementation, enhancement-local developer tests within established lifecycle policy, candidate assembly, independent 07/T2/T3 and actual runtime checks *when capable agents/environment exist*. P01 → (P02,P03) → P04 → P05; protect legacy Product v2. Evidence/CI failures stay `BLOCKED` or `FAIL`, not patched by unapproved algorithm changes. If independent S09 after coding detects frozen contract defect, follow formal 09, Owner change impact and re-freeze/re-authorization when substantive; do not override science targets.

**S11 owner result field:** `NOT_DECIDED`; not implied by Owner adoption of `DEC-G01-EXEC-01` or future S10 approval. No Coding Agent execution from this docket.

## C. Practical next action — no impossible pre-code activity

1. Owner decides **only provisional G01 S10** once this packet and exact source freeze SHA are presented; use `APPROVE / CHANGE / REJECT`. Do not request B02/B04 Linux or independent S09/B05 results to issue this provisional S10.
2. **After** Owner S10, issue separate **limited G01 S11** to permit coding; do not demand unavailable experimental evidence beforehand.
3. In the actually authorized coding environment, implement 06/07 faithfully. Independently verify every X item before `G01_999 PASS`; otherwise `BLOCKED`. The present session has no Owner Linux VM or real independent reviewer; these are recorded as external pending, not executable next steps for this session.
