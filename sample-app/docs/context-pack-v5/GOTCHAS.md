# Gotchas — transfer-service

Ordered most dangerous first.

1. **No concurrency protection on balances.** `Account` has no `@Version` and reads are
   not locked; two concurrent transfers from the same account can both pass the
   `INSUFFICIENT_FUNDS` check and double-spend. Any change touching balances must not
   assume this is safe.
2. **Business rejections are HTTP 201, not errors.** A `REJECTED` transfer returns
   201 CREATED with `status=REJECTED`. Only *missing accounts* produce an HTTP error
   (404). Don't "fix" this asymmetry accidentally — it is the designed contract.
3. **`ddl-auto: create-drop` + in-memory H2** — schema is generated from entities and all
   data vanishes on restart. There are no migrations; entity changes silently change the
   schema.
4. **Idempotency replay ignores payload differences.** A replay with the same key but
   different amount/accounts returns the ORIGINAL transfer — no mismatch detection.
5. **Validation order matters.** `validate()` checks self-transfer → currency →
   funds and returns only the FIRST violation. Tests may depend on that ordering.
6. **`currency` is a free-form String** — nothing prevents persisting an invalid code;
   comparison is exact `equals`.
7. **Only `AccountNotFoundException` has a handler.** Any other runtime exception
   surfaces as a default 500; bean-validation failures use Spring's default 400 body,
   which is not RFC-7807-consistent with the 404 handler.
8. **`Transfer.createdAt` is set in the constructor**, not by JPA auditing — replays keep
   the original timestamp; new code must not expect `@CreatedDate` behaviour.
9. **No GET endpoints.** Nothing can be queried over HTTP; tests observe state via
   repositories directly.
10. **`Transfer` is constructed in TWO places** inside `TransferService.execute` (the
    REJECTED branch and the COMPLETED branch). New fields must be wired through both,
    or one path silently persists null.
11. **DTOs are positional records.** Adding a component to `TransferRequest`/
    `TransferResponse` breaks every constructor call site, including the test
    `request(...)` helper and `TransferResponse.from`.
