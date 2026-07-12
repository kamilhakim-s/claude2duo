# Architecture — transfer-service

> Spring Boot 3.3.5 · Java 21 · single Gradle module · root package `com.example.payments`

## Package layout

| Package | Role | Classes |
|---|---|---|
| `com.example.payments` | Boot entry point | `TransferServiceApplication` |
| `..payments.controller` | REST layer + error mapping | `TransferController`, `GlobalExceptionHandler` |
| `..payments.dto` | API request/response records | `TransferRequest`, `TransferResponse` |
| `..payments.service` | Business logic + business exceptions | `TransferService`, `AccountNotFoundException` |
| `..payments.repository` | Spring Data JPA repositories | `AccountRepository`, `TransferRepository` |
| `..payments.model` | JPA entities | `Account`, `Transfer` (with nested `Transfer.Status` enum) |

## Dependency direction
controller → service → repository → model. DTOs are used only by controller and service.
Nothing depends on `controller`. Entities never leave the service layer:
`TransferResponse.from(Transfer)` converts at the boundary.

## Runtime flow — POST /api/v1/transfers

```
HTTP POST /api/v1/transfers (JSON)
  └─ TransferController.createTransfer(@Valid TransferRequest)      [201 CREATED]
       └─ TransferService.execute(request)                          [@Transactional]
            ├─ TransferRepository.findByIdempotencyKey(key)         -- replay? return original
            ├─ AccountRepository.findBySortCodeAccountNumber(src)   -- missing → AccountNotFoundException
            ├─ AccountRepository.findBySortCodeAccountNumber(dst)   -- missing → AccountNotFoundException
            ├─ TransferService.validate(source, destination, req)   -- returns rejection reason or null
            ├─ Account.debit / Account.credit                       -- only when valid
            └─ TransferRepository.save(transfer)                    -- COMPLETED or REJECTED
       └─ TransferResponse.from(saved)
Error path: AccountNotFoundException → GlobalExceptionHandler → ProblemDetail 404
Bean-validation failure → Spring default 400 (no custom handler)
```

## External systems
None. Persistence is H2 in-memory (`jdbc:h2:mem:transfers`). No HTTP clients, no
messaging, no cache. Upstream callers: UNKNOWN — verify with the team.

## Technology stack (from build.gradle.kts)
Spring Boot 3.3.5, dependency-management 1.1.6, Java toolchain 21, starters: web,
data-jpa, validation; H2 runtime; spring-boot-starter-test + JUnit platform.
