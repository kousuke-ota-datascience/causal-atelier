# DEC-S05-02 / DEC-S05-03 — Owner execution governance (2026-11-22)

**Decision source:** Owner message 2026-11-22T03:19:31Z (= 12:19:31 JST): “DEC-S05-02はA案、DEC-S05-03はA案を採用する。S05の残件を続行せよ。必要な実行権限や環境アクセスがない場合はBlockerとして報告すること。”

**Authority:** Owner explicitly **ADOPTED A+A**. This approves the *review process and use of an isolated development environment*, **NOT** any new Method, dependencies in production, science acceptance, or Coding Authorization.

## DEC-S05-02 = A / independent agent and science governance

- Independent Review Agent separate from original Method author and Reference author; reviewer must have independent instruction, immutable baseline and not be supplied prior conclusions as acceptance evidence. Evidence/fixture/source sha and predeclared adjudication, formal review judgment, failures, version, and reviewer identity required.
- Owner remains final approval authority. G08 robust AR HC1/chi-square specific method remains **provisional** under adopted DEC-S05-AR01; independent mathematical-statistical review before algorithm freeze, and external specialist involvement if the independent agent cannot establish validity.
- The mere existence of two prompts/sessions or an LLM agreeing with the author is not independent science PASS; actual reviewer output and conflict-of-interest/process evidence required.
- **Execution blocker discovered:** connected Notion `notion_search_agents` returned `entitlement_required` (Business-or-higher workspace entitlement). No agent session started; this channel cannot trigger the separate existing user's Codex CLI session or operate their Linux terminal. Alternative: Owner's existing development environment invokes independent Codex CLI from a separate clean context and returns signed/logged evidence, or establishes another authorized independent-review provider. Do not present Notion upgrade as the sole route.

## DEC-S05-03 = A / existing Linux isolated review environment

- Approved **separate** read-only review environments on the Owner's existing Linux development VM (supported project Python >=3.12,<3.13; isolated profiles ENV-BASE/DOWHY/ECONML/TIGRAMITE). No production source/tests/pyproject.toml/uv.lock changes before S11. Pin each exact dependency resolution, Python/OS/architecture, method-aware imported signature/fit/CI, source hash, negative/positive fixtures and result hashes.
- **Execution blocker discovered:** current ChatGPT container has Python 3.13.5, no connected terminal to the Owner's Linux VM, and DNS resolution of github.com failed. It cannot claim target CPython 3.12 or cloned repository execution. GitHub connector can read/write approved documentation but does not provide OS execution. B02 200-schema actual Python Draft202012 validator and B04 target backend fit remain unexecuted.
- No false inference from isolated environment approval that a virtualenv has been created or validated. Record actual command outputs and exact Git SHA before closing B02/B04.

## Follow-through and stop rules

- Continue all S05 work feasible with connected Github and local review-only tooling; report obstacles as soon as confirmed.
- The structural 200 AST parity and 41 science oracle *plans* remain review candidates until independent evidence exists; cannot credit them as accepted T3 science.
- No S06 official entry, S09 independent audit PASS, S10 Freeze or S11 Coding Authorization based on A+A decisions alone.

**Status:** `OWNER_APPROVED_REVIEW_MODEL_A / OWNER_APPROVED_ISOLATED_LINUX_A / REVIEW_AGENT_NOT_LAUNCHED / OWNER_LINUX_NOT_CONNECTED / NO_BACKEND_TARGET_PROBE / NO_CODING_AUTHORIZATION`.
