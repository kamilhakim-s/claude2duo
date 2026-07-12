# ARCHITECTURE — transfer-service

> Stack: Spring Boot 3.3.5, Java 21, Spring Data JPA, Bean Validation, H2 (in-memory). Build: Gradle Kotlin DSL. Root package: `com.example.payments`.

## Purpose
Single-endpoint microservice that executes immediate payments between internal accounts. `POST /api/v1/transfers` moves money from a source account to a destination account, enforcing idempotency and business-rule rejection (self-transfer, currency mismatch, insufficient funds). All state is in-memory H2 (`ddl-auto: create-drop`); nothing persists across restarts.

## Module structure (`src/main/java/com/example/payments/`)
```
payments/
├── TransferServiceApplication.java   Spring Boot entry point (@SpringBootApplication)
├── controller/
│   ├── TransferController.java        REST endpoint POST /api/v1/transfers
│   └── GlobalExceptionHandler.java    @RestControllerAdvice → ProblemDetail
├── service/
│   ├── TransferService.java           core business logic (@Transactional)
│   └── AccountNotFoundException.java   RuntimeException for missing account
├── repository/
│   ├── AccountRepository.java         JpaRepository<Account, Long>
│   └── TransferRepository.java         JpaRepository<Transfer, Long>
├── model/
│   ├── Account.java                    @Entity accounts; debit()/credit()
│   └── Transfer.java                   @Entity transfers; Status enum
└── dto/
    ├── TransferRequest.java            record; inbound, Bean Validation
    └── TransferResponse.java           record; outbound, from(Transfer) factory
```

## Main runtime flow (HTTP request → DB)
1. `TransferController.createTransfer` receives `@Valid @RequestBody TransferRequest`. Bean Validation runs first; on failure Spring returns 400 before the service is called. Success returns HTTP 201 (`@ResponseStatus(CREATED)`).
2. `TransferService.execute(request)` runs inside `@Transactional`:
   a. `TransferRepository.findByIdempotencyKey` — if a transfer already exists for the key, return `TransferResponse.from(existing)` (no re-processing).
   b. `AccountRepository.findBySortCodeAccountNumber` for source and destination; each missing account throws `AccountNotFoundException`.
   c. `validate(source, destination, request)` returns a rejection-reason String or null.
   d. If a reason is returned → build `Transfer` with `Status.REJECTED` and the reason; balances untouched. If null → `source.debit(amount)`, `destination.credit(amount)`, build `Transfer` with `Status.COMPLETED`.
   e. `TransferRepository.save(transfer)` persists; JPA dirty-checking flushes the mutated `Account` balances on transaction commit.
   f. Return `TransferResponse.from(saved)`.
3. `AccountNotFoundException` is caught by `GlobalExceptionHandler.handleAccountNotFound` → `ProblemDetail` with HTTP 404.

No async, messaging, or scheduling exists in this codebase.

## Domain concepts & invariants (enforced in code)
- **Account**: unique `sortCodeAccountNumber` (8 chars), `currency`, `balance` (`BigDecimal`, precision 19 scale 2). Mutated only via `debit`/`credit`.
- **Transfer**: unique `idempotencyKey`, `@ManyToOne` source + destination (both required), `amount`, `Status` (COMPLETED | REJECTED), nullable `rejectionReason`, `createdAt` (`Instant.now()` at construction).
- **Idempotency**: replays on the same `idempotencyKey` return the original transfer without a second debit (invariant tested).
- **Rejection vs error**: rule violations 3–5 persist a REJECTED transfer (HTTP 201, no exception). Missing accounts throw (HTTP 404).
- **Validation rules** (`TransferService.validate`, evaluated in order): (3) source ID ≠ destination ID → `SELF_TRANSFER_NOT_ALLOWED`; (4) `source.currency` = `destination.currency` else `CURRENCY_MISMATCH`; (5) `source.balance >= amount` else `INSUFFICIENT_FUNDS`.
- **Input contract** (`TransferRequest`): `idempotencyKey` not blank; `sourceAccount`/`destinationAccount` match `\d{8}`; `amount` not null, `>= 0.01`.

## Technology stack (from `build.gradle.kts`)
- Java 21 (toolchain), Spring Boot 3.3.5, io.spring.dependency-management 1.1.6
- spring-boot-starter-web, -data-jpa, -validation
- H2 (runtime), spring-boot-starter-test (JUnit 5 via `useJUnitPlatform()`)
