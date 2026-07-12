# The service in one file

> transfer-service · Spring Boot 3.3.5 · Java 21 · H2 in-memory · one endpoint

## What it does
Immediate payments between internal accounts. That's it. One synchronous POST, no
queues, no external calls, no scheduler. The interesting part is the *semantics*:
idempotency and how rejections are modelled.

## The flow you must understand first
`POST /api/v1/transfers` → `TransferController.createTransfer` (`@Valid`, returns 201)
→ `TransferService.execute` (`@Transactional`):

1. `TransferRepository.findByIdempotencyKey` — seen this key before? Return the
   original transfer. **Replays never re-execute.**
2. Load both accounts via `AccountRepository.findBySortCodeAccountNumber` — a miss
   throws `AccountNotFoundException` → `GlobalExceptionHandler` → **404** ProblemDetail.
3. `validate(source, destination, request)` — first violated rule wins, in this order:
   `SELF_TRANSFER_NOT_ALLOWED`, `CURRENCY_MISMATCH`, `INSUFFICIENT_FUNDS`.
   A violation is **not an error**: we persist a `REJECTED` Transfer and return it
   with **201**. Rejections are business outcomes with an audit trail.
4. Happy path: `source.debit(amount)`, `destination.credit(amount)` (dirty checking —
   no explicit save of accounts), persist `COMPLETED` transfer, map through
   `TransferResponse.from`.

## The API
One endpoint. `TransferRequest` record: `idempotencyKey` (@NotBlank), `sourceAccount` /
`destinationAccount` (@NotBlank, @Pattern `\d{8}`), `amount` (@NotNull, @DecimalMin
0.01). Bean-validation failures → Spring's default 400, *not* ProblemDetail.
`TransferResponse` record: id, sourceAccount, destinationAccount, amount, status
(`COMPLETED`/`REJECTED`), rejectionReason (nullable), createdAt. There is **no GET** —
you cannot query transfers over HTTP today.

## The data
- `Account` → `accounts`: `sortCodeAccountNumber` (unique, 8 chars, the business key),
  `currency` (free String, exact-match compared), `balance` decimal(19,2). Mutated only
  via `debit`/`credit`. **No `@Version`** — see TRIBAL-KNOWLEDGE.md.
- `Transfer` → `transfers`: `idempotencyKey` (unique — the DB backs up the idempotency
  logic), two `@ManyToOne` Account refs, amount, `status` (enum-as-STRING, nested
  `Transfer.Status`), nullable `rejectionReason`, `createdAt` set in the constructor.
  Immutable after construction.
- Schema: `ddl-auto: create-drop` from entities. No Flyway/Liquibase, no data survives
  restart. What we'd use in production: UNKNOWN — verify with the team.

## Who calls us / what we call
Nothing in the repo answers this — no clients, no outbound calls. UNKNOWN — verify
with the team.
