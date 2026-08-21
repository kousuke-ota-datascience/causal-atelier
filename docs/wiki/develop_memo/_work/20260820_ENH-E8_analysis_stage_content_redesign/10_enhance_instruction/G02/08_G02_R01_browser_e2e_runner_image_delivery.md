# G02 R01 — Browser E2E Runner Image Delivery Remediation

- Document class: Remediation Execution Contract
- Status: `FROZEN`
- Gate: `G02`
- Remediation Package ID: `R01`
- Source failed Trial: `Trial01`
- Target verification Trial: `Trial02`
- Failed Fixed Trial Candidate SHA: `a2399662f4f81ceadf36ae2aa71850d49786cae4`
- Trigger: canonical `30_test_report/G02/Trial01/999_GATE_DECISION.md = FAIL`

## 1. Purpose

Trial01 の Independent Verification で確認された Browser E2E runner delivery mismatch のみを修正し、新しい immutable Fixed Trial Candidate を Trial02 に引き渡す。

この remediation は G02 の frontend/application semantics、Browser E2E runner semantics、frozen `06` / `07` Acceptance Criteria を変更しない。

`08` remediation completion は Gate PASS ではない。Gate 判定は新 candidate に対する Trial02 Independent Verification が行う。

## 2. Normative inputs

本 remediation の入力 authority は以下とする。

1. `30_test_report/G02/Trial01/001_candidate_identity_audit.md`
2. `30_test_report/G02/Trial01/002_focused_and_protected_regression.md`
3. `30_test_report/G02/Trial01/003_frozen_browser_e2e.md`
4. `30_test_report/G02/Trial01/999_GATE_DECISION.md`
5. frozen `06_Ariadne_ENH-E8_G02_implementation_instruction.md`
6. frozen `07_Ariadne_ENH-E8_G02_test_instruction.md`
7. failed Fixed Trial Candidate `a2399662f4f81ceadf36ae2aa71850d49786cae4`

上記と本 remediation の間に semantic conflict が判明した場合、推測で補完せず remediation を停止し、`09` Gate Contract Amendment の対象とする。

## 3. Established failure facts

Trial01 では以下が確認済みである。

- candidate identity audit は PASS。検証対象 SHA は `a2399662f4f81ceadf36ae2aa71850d49786cae4` に固定された。
- focused/protected regression は `19 passed`。JavaScript syntax、両 G02 Browser E2E runner の Python compile、`git diff --check` も PASS した。
- Compose bootstrap は成功し、database / migration / API / frontend / worker の起動に外部 blocker は無かった。
- frozen Causal / Predictive Chromium commands はともに candidate-built `browser-e2e` image 内の runner file-not-found で FAIL した。
- failed candidate の source tree には次の2 runner が存在する。
  - `tests/browser_e2e/run_enh_e8_g02_causal_stage_content.py`
  - `tests/browser_e2e/run_enh_e8_g02_predictive_stage_content.py`
- failed candidate の `Dockerfile.browser-e2e` は E1A / E3 / E6 / E7 / G01 runner のみを image に `COPY` し、G02 の2 runnerを `COPY` していない。
- failed candidate の `.dockerignore` は `tests/browser_e2e/*` を除外した後、既存 runner を個別に allowlist しているが、G02 の2 runnerは allowlist していない。

したがって failure は runner implementation の不存在ではなく、次の delivery chain の欠落である。

```text
repository source
  -> Docker build context (.dockerignore)
  -> browser-e2e image (Dockerfile.browser-e2e)
  -> /workspace/tests/browser_e2e/<G02 runner>
  -> frozen 07 command
```

現 candidate は source までは存在するが、build context と image delivery の両方が未定義である。

`Dockerfile.browser-e2e` に `COPY` だけを追加しても `.dockerignore` により source が build context から除外されるため不十分である。

## 4. Remediation claim

G02 の2 Browser E2E runner を、既存 browser runner と同じ delivery mechanism で candidate-built `browser-e2e` image に含め、frozen `07` command が exact path から runner を起動できる状態にする。

修正は delivery packaging のみに限定する。

## 5. Required implementation delta

### R01-A — `.dockerignore` build-context allowlist

`.dockerignore` の既存 `tests/browser_e2e` 個別 allowlist に、次の2行を追加する。

```gitignore
!tests/browser_e2e/run_enh_e8_g02_causal_stage_content.py
!tests/browser_e2e/run_enh_e8_g02_predictive_stage_content.py
```

要件:

- 既存の個別 allowlist 方針を維持する。
- `!tests/browser_e2e/**` 等の broad allowlist へ一般化しない。
- G02 remediation に不要な test artifact を build context に追加しない。

### R01-B — `Dockerfile.browser-e2e` image delivery

既存 runner の `COPY` 群に、次の2行を追加する。

```dockerfile
COPY --chmod=0755 tests/browser_e2e/run_enh_e8_g02_causal_stage_content.py /workspace/tests/browser_e2e/run_enh_e8_g02_causal_stage_content.py
COPY --chmod=0755 tests/browser_e2e/run_enh_e8_g02_predictive_stage_content.py /workspace/tests/browser_e2e/run_enh_e8_g02_predictive_stage_content.py
```

要件:

- destination path は frozen `07` command と一致させる。
- existing runner と同じ `--chmod=0755` delivery convention を維持する。
- existing `ENTRYPOINT` を変更しない。
- volume mount や host source bind による workaround を導入しない。

## 6. Explicit non-scope / prohibited changes

failed evidence が要求していないため、R01 では以下を変更してはならない。

- `tests/browser_e2e/run_enh_e8_g02_causal_stage_content.py` の test semantics
- `tests/browser_e2e/run_enh_e8_g02_predictive_stage_content.py` の test semantics
- `frontend/` implementation
- API / DB / persistence / migration / worker / runtime implementation
- `compose.yaml` / `compose.e1a.yaml` の semantic behavior
- frozen `06` / `07` の Gate claim、Acceptance Criteria、canonical command
- `--build` の削除、別 command への置換、file-not-found を回避する host bind mount
- LightGBM / LIME / SHAP その他 G02 scope 外 capability

R01 実行中に上記の変更が必要と判明した場合、scope を silent に拡大せず blocker として報告する。

## 7. Implementation self-check

Coding Agent は新 candidate 固定前に、少なくとも以下を実行する。

### 7.1 Static / delivery diff

```bash
git diff --check
git diff -- .dockerignore Dockerfile.browser-e2e
```

期待結果:

- executable remediation delta は `.dockerignore` と `Dockerfile.browser-e2e` の G02 runner delivery 追加に限定される。

### 7.2 Existing focused/protected regression

Trial01 Test Item `002` と同じ focused/protected regression、および syntax checks を新 candidate source に対して再実行する。

期待結果:

- applicable focused/protected regression が green。
- G02 runner Python compile が green。
- frontend syntax checks が green。

前 Trial の PASS を新 candidate の結果として流用してはならない。

### 7.3 Browser image delivery check

candidate source から `browser-e2e` image を rebuild し、少なくとも次を確認する。

- build context に G02 の2 runner が含まれる。
- rebuilt image の以下 exact path に2 runner が存在する。
  - `/workspace/tests/browser_e2e/run_enh_e8_g02_causal_stage_content.py`
  - `/workspace/tests/browser_e2e/run_enh_e8_g02_predictive_stage_content.py`

Coding Agent が frozen `07` の2 Chromium commands を self-check として実行してよいが、その結果は Trial02 Independent Verification を代替せず Gate PASS を意味しない。

## 8. Candidate assembly

R01 completion 後、1つの新しい immutable commit SHA を Trial02 Fixed Trial Candidate として固定する。

Trial02 Implementation Completion Report には最低限以下を記録する。

- exact Fixed Trial Candidate SHA
- source failed candidate SHA `a2399662f4f81ceadf36ae2aa71850d49786cae4`
- remediation package `G02-R01`
- `.dockerignore` と `Dockerfile.browser-e2e` の delivery delta
- focused/protected regression と syntax/diff self-check の結果
- image delivery check の結果
- unresolved blocker の有無
- `READY_FOR_TEST` は Gate PASS ではない旨

Completion Report の documentation/attestation commit を Fixed Trial Candidate SHA と混同しない。

## 9. Trial02 Independent Verification handoff

Trial02 verifier は Completion Report に固定された exact immutable SHA のみを検証する。

Trial02 では frozen `07_Ariadne_ENH-E8_G02_test_instruction.md` を変更せず適用し、少なくとも以下を再実行する。

- candidate identity audit
- focused/protected regression / syntax / diff checks
- frozen Causal Chromium journey
- frozen Predictive Chromium journey
- applicable `G02-AC01`–`G02-AC23`

Trial01 の Browser E2E FAIL evidence を Trial02 PASS evidence として流用してはならない。

## 10. Completion criteria

R01 remediation は以下をすべて満たした場合のみ `REMEDIATION_COMPLETE / READY_FOR_TRIAL02` とする。

- [ ] `.dockerignore` が G02 の2 runner のみを追加 allowlist している。
- [ ] `Dockerfile.browser-e2e` が G02 の2 runner を exact image path へ `COPY` している。
- [ ] G02 runner semantics、frontend、backend/runtime、compose semantics、frozen `06/07` に変更がない。
- [ ] new candidate に対する focused/protected regression と syntax/diff checks が green。
- [ ] rebuilt browser image 内に G02 の2 runner が存在することを確認した。
- [ ] unresolved blocker がない。
- [ ] 新しい immutable Fixed Trial Candidate SHA を固定した。
- [ ] Trial02 Implementation Completion Report に handoff evidence を記録した。

この completion は G02 Gate PASS を宣言しない。最終判定 authority は Trial02 Independent Verification の `999_GATE_DECISION.md` である。
