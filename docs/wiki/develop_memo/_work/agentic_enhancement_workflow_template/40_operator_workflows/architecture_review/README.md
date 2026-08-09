# Architecture Review Workflow

## Applicability

以下の場合に`CONDITIONAL MUST`:

- runtime entrypoint / lifecycle change
- authority / ownership change
- persistence / schema / lineage change
- legacy path removal / consolidation
- migration strategy change
- cross-subsystem canonical source-of-truth change

## Standard outputs

1. architecture discovery result
2. target architecture decision record / invariant set
3. Gate decomposition

これらをそのままCoding Agentへ自由探索させるのではなく、必要事項をGate-local 06 / 07へ抽出する。
