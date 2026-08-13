# ENH-E6 Technical Debt / Follow-up Ledger

## E6 source anomaly inheritance

### ANOM-E5-001 — Family Tab Observable UI Gap

- Source enhancement: `ENH-E5`
- Source status: `OPEN_FOLLOW_UP`
- ENH-E6 status: `IN_SCOPE / NOT YET RESOLVED`
- ENH-E6 target Gate: `G01`

Resolution condition:

- G01 final PASS
- observable Family tabs in fresh environment
- Family click / Stage click / reload / back-forward / legacy shortcut browser journeys PASS
- stage-aware presentation binding PASS
- regression test operates actual Family tabs

G01 PASS前に `RESOLVED` と記載してはならない。

## Potential follow-up excluded from E6

- Full replacement of legacy left navigation IA
- Family-specific complete stage screen redesign
- independent per-stage URL-owned microfrontend decomposition
- removal of all legacy `/explore|/predictive|/causal` route compatibility
