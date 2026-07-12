# Service overview — transfer-service

> Spring Boot 3.3.5 · Java 21 · Gradle (Kotlin DSL) · JPA + H2 in-memory

## Purpose
Executes **single immediate payments between internal accounts**. One synchronous REST
operation; no batching, no scheduling, no external calls.

## Business responsibilities
- Move money between two internal `Account` rows atomically.
- Guarantee **idempotency**: replaying the same `idempotencyKey` returns the original
  result and never double-debits.
- Enforce business rules; violations are **persisted as REJECTED transfers** (audit
  trail), not thrown as errors.

## The one business flow (happy path)
1. Client sends `POST /api/v1/transfers` with idempotency key, 8-digit source and
   destination account numbers, amount.
2. If a `Transfer` with that `idempotencyKey` already exists → return it unchanged.
3. Both accounts are loaded by account number; a missing account is an HTTP 404 error.
4. Business validation (in order): self-transfer → currency mismatch → insufficient funds.
   First failing rule creates a `REJECTED` transfer with that reason.
5. If valid: source is debited, destination credited, a `COMPLETED` transfer is saved.
6. Response (HTTP 201 in both COMPLETED and REJECTED cases) reflects the saved transfer.

## Rules the code enforces (TransferService javadoc + `validate()`)
| # | Rule | Outcome when violated |
|---|---|---|
| 1 | Idempotent on `idempotencyKey` | Replay returns original result |
| 2 | Both accounts must exist | `AccountNotFoundException` → HTTP 404 |
| 3 | No self-transfer | REJECTED, reason `SELF_TRANSFER_NOT_ALLOWED` |
| 4 | Currencies must match | REJECTED, reason `CURRENCY_MISMATCH` |
| 5 | Source balance ≥ amount | REJECTED, reason `INSUFFICIENT_FUNDS` |

## Consumers / producers
UNKNOWN — verify with the team. No client code, messaging, or external integrations exist
in this repository.
