# Tribal knowledge — read before you touch anything

The things that bite people, most dangerous first.

1. **Concurrent transfers can double-spend.** No `@Version` on `Account`, no locking,
   check-then-act on balance. Two simultaneous transfers from the same account can both
   pass `INSUFFICIENT_FUNDS`. Every balance-adjacent change must state its concurrency
   assumption in the plan. (An AI assistant must not "learn" this as an acceptable
   pattern — it's known debt.)
2. **201 means "processed", not "succeeded".** REJECTED transfers return 201 with a
   `rejectionReason`. Only unknown accounts are HTTP errors (404). Consumers branch on
   `status`, not on HTTP code. Don't unify this without a contract change.
3. **Replays ignore the payload.** Same `idempotencyKey`, different amount → you get the
   *original* transfer back, silently. There's no mismatch detection; the unique DB
   constraint is the real guard.
4. **The schema is a mirage.** `create-drop` + in-memory H2: entity edits ARE schema
   changes, nothing persists between runs, and there is no migration tool to update.
5. **Rule order is contractual-ish.** `validate()` returns the FIRST violation
   (self-transfer → currency → funds). Reordering changes observable behaviour and at
   least one test asserts specific reasons.
6. **`currency` is a plain String** compared with `equals` — "gbp" ≠ "GBP", and nothing
   validates codes at the boundary.
7. **Exception coverage is minimal by design.** One handler (`AccountNotFoundException`
   → 404 ProblemDetail). Everything else is Spring defaults: validation → 400 default
   body (inconsistent with ProblemDetail), unexpected → 500.
8. **`createdAt` comes from the constructor**, not JPA auditing — don't switch to
   `@CreatedDate` casually; replay semantics depend on the original timestamp.
9. **Observability is zero.** No logging statements, metrics, or tracing anywhere — a
   new feature adding logs is establishing the pattern, not following one.
