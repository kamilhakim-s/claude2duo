# Data model — transfer-service

> JPA/Hibernate · H2 in-memory · schema auto-generated (`ddl-auto: create-drop`) · no migration tool

## Entities

### Account → table `accounts` (`com.example.payments.model.Account`)
| Field | Column traits | Notes |
|---|---|---|
| id | PK, identity | |
| sortCodeAccountNumber | not null, **unique**, length 8 | Business key; repositories look up by it |
| currency | not null, plain String | Free text — no enum/ISO validation |
| balance | not null, decimal(19,2) | Mutated via `debit(amount)` / `credit(amount)` methods |

No optimistic-locking `@Version` field. Protected no-arg constructor for JPA; public
constructor `(sortCodeAccountNumber, currency, balance)`.

### Transfer → table `transfers` (`com.example.payments.model.Transfer`)
| Field | Column traits | Notes |
|---|---|---|
| id | PK, identity | |
| idempotencyKey | not null, **unique** | Idempotency guarantee at DB level |
| source | @ManyToOne(optional=false) → Account | |
| destination | @ManyToOne(optional=false) → Account | |
| amount | not null, decimal(19,2) | |
| status | not null, enum as STRING | `Transfer.Status`: COMPLETED, REJECTED |
| rejectionReason | nullable String | Set only for REJECTED |
| createdAt | not null Instant | Set in constructor (`Instant.now()`), not by auditing |

Immutable after construction — getters only, no setters.

## Repositories (`com.example.payments.repository`)
| Interface | Extends | Custom finders |
|---|---|---|
| AccountRepository | JpaRepository<Account, Long> | `findBySortCodeAccountNumber(String)` → Optional |
| TransferRepository | JpaRepository<Transfer, Long> | `findByIdempotencyKey(String)` → Optional |

## Schema management
`spring.jpa.hibernate.ddl-auto: create-drop` — Hibernate creates the schema at startup
and drops it at shutdown; **all data is lost on restart**. There is no
Flyway/Liquibase. Adding a field = change the entity; no migration file exists or is
needed in this repo. (For a real service this would differ — UNKNOWN — verify with the
team what the target migration tool is.)

## Non-obvious persistence behaviour
- Balance updates rely on JPA dirty checking inside `TransferService.execute`'s
  `@Transactional` — `debit`/`credit` mutate managed entities; no explicit save call.
- Rejected transfers are persisted too (audit trail), not discarded.
- No caching, soft deletes, or auditing annotations anywhere.
