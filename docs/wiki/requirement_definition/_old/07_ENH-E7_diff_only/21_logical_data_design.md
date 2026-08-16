# Logical Data Design — ENH-E7差分

ENH-E7ではlogical persistence modelの変更を想定せず、承認もしない。

Existing Project / Research Context / Dataset Version / Analysis View / Result / Lineage domain objectを維持する。
Analysis ViewをFamily横断analysis inputとして扱うことはUI responsibilityの明確化であり、
それだけを理由にpersistence schemaやcardinalityを変更しない。

schema changeが必要と判明した場合はaffected packageを停止し、Architecture Review / contract amendmentを要求する。
