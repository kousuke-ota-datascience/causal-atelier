# ENH-E6 Requirements / Design Consistency and Traceability Review

- Status: `PASS_FOR_DRAFT_CONTRACT`

## Traceability matrix

| Requirement | Design mechanism | Gate AC |
|---|---|---|
| E6-FR-001 | observable shell lifecycle + unified coordinator | AC-E6-G01-001 |
| E6-FR-002 | Family click -> defaultContext -> coordinator | AC-E6-G01-002 |
| E6-FR-003 | Stage click -> navigationContext -> coordinator | AC-E6-G01-003 |
| E6-FR-004 | parse/serialize + `historyMode=none` restore | AC-E6-G01-004 |
| E6-FR-005 | single transition authority | AC-E6-G01-005 |
| E6-FR-006 | stage-aware presentation binding | AC-E6-G01-006 |
| E6-FR-007 | compatibility shortcut boundary | AC-E6-G01-007 |
| E6-FR-008 | explicit Causal legacy mappings | AC-E6-G01-008 |
| E6-FR-009 | fail-closed binding/catalog semantics | AC-E6-G01-009 |
| E6-NFR-001 | real browser blocking journey | AC-E6-G01-010 |
| E6-NFR-002 | E5 protected regression suite | AC-E6-G01-011 |

## Consistency review

### Navigation Stage vs Execution Stage

MATCH。Stage-aware presentation bindingはUI/presentation concernに限定し、Execution runtimeへのpersist/mappingを禁止している。

### backend catalog authority

MATCH。Family labels/order/default/stage listはbackend catalog authorityを維持し、frontend mappingはpresentation surface bindingだけを保持する。

### legacy compatibility

MATCH WITH CLARIFICATION。E5は `/explore`, `/predictive`, `/causal` の一方向normalizeを規定していた。E6はvisual left-nav shortcutsについても同じ「canonical contextへ収束する」責務に統一する。

### Browser E2E scope

MATCH。workflow templateのBrowser E2E invariantに従い、detailed correctnessの主証明ではなく、今回のanomalyそのものに対応するcritical cross-layer journeyへ限定する。

## Open approval item

`Causal Inference -> causal/identification` のcompatibility targetは owner approval待ち。これ以外のcontractは当該targetをparameterized mappingとして保持可能だが、06/07 freeze前に値を確定する。
