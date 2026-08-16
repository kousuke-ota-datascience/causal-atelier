```
Workflow Template次版では

私は Status at issuance 自体を削除するか、少なくとも例えば、

**Issuance status (diagnostic only):** DRAFT

のように実行制御ではないことを明示するのがよいと考えます。

さらに理想的にはPxxからstatusをなくして、

Gate contract readiness
    ← Gate 06/07から導出


Package execution eligibility
    ← Depends on + 実成果物から導出

だけにする方が、今回のWorkflow Template設計思想と整合します。

したがって、今の G02/P01 はそのまま進めて構いません。DRAFT_NOT_FROZEN を READY_TO_EXECUTE に直す必要はありません。
```

HOW to useのセクションが、READMEにあるが、今回試した中では圧倒的に記載が足りない。

> README_Appendix_HowToUse.md

というmdを別に作る必要があると思っている。

まずは、初版を作成してほしい