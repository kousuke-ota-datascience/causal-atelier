# 21_25_value_canonicalization


---

### 4.15 Technical persistence model

`IdempotencyRecord`はbusiness Entityではなくtechnical persistence recordである。

```text
IdempotencyRecord
├─ project_id
├─ scope
├─ idempotency_key
├─ request_hash
├─ response_json
└─ created_at
```

(`project_id`, `scope`, `idempotency_key`)を一意とし、同一commandの重複適用を防止する。business lineageやscientific resultの正本として扱わない。

### 4.16 Canonicalization model

canonical hash対象JSONは次のruleで正規化する。

1. object keyを安定順序でserializeする。
2. datetimeはtimezone-aware ISO-8601へ正規化する。
3. Enumはstable string valueへ変換する。
4. set等の順序非保証collectionは意味的に順序が不要な場合のみcanonical sortする。
5. NaN / Infinityを禁止する。
6. numpy/pandas/sklearn等のlibrary objectを直接JSONへ保存しない。
7. schema versionをsnapshotとともに保持する。
