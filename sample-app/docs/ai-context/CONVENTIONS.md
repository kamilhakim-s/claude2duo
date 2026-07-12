# CONVENTIONS — transfer-service

> Stack: Spring Boot 3.3.5, Java 21, Spring Data JPA, Bean Validation, H2. Package: `com.example.payments`. All rules below are observed in the actual code, not generic advice.

## Layering (what may call what)
- `controller` → `service` → `repository` → `model`. Strict downward flow.
- Controllers hold no business logic: `TransferController.createTransfer` is a one-line delegate to `transferService.execute`.
- Services depend on repositories only; no controller/web types in `service`.
- Repositories are Spring Data interfaces; no hand-written implementations.
- `dto` is referenced by `controller` and `service`; `model` (JPA entities) is never returned from the controller directly — always mapped to a DTO.

## Constructor injection
- All dependencies injected via constructor, stored in `private final` fields. No `@Autowired` on fields in main code (only `TransferServiceTest` uses field `@Autowired`).

## Naming patterns
- Suffixes: `*Controller`, `*Service`, `*Repository`, `*Request`, `*Response`, `*Exception`, `*Application`, `*Test`.
- DTOs are Java `record`s (`TransferRequest`, `TransferResponse`); entities are mutable classes annotated `@Entity`.
- Entity → DTO mapping via a static factory on the response record: `TransferResponse.from(Transfer)`. No mapper library.
- Entities have a `protected` no-arg constructor (JPA) plus a public all-args constructor; state changes go through intent-named methods (`debit`, `credit`), not setters. No setters exist.
- Repository query methods use Spring Data derived-query naming: `findByIdempotencyKey`, `findBySortCodeAccountNumber`.

## Error handling pattern
- Two distinct outcomes, deliberately separated:
  - **Business-rule rejection** (self-transfer, currency mismatch, insufficient funds): NOT an exception. `TransferService.validate` returns a String reason code; a `Transfer` with `Status.REJECTED` is persisted and returned as a normal 201 response.
  - **Missing resource**: throw. `TransferService` throws `AccountNotFoundException` (extends `RuntimeException`, message `"Account not found: " + accountNumber`).
- Exceptions are translated centrally in `GlobalExceptionHandler` (`@RestControllerAdvice`) to RFC 7807 `ProblemDetail`. Example: `handleAccountNotFound` → `ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage())`.
- Reason codes are SCREAMING_SNAKE_CASE string literals (`INSUFFICIENT_FUNDS`, `CURRENCY_MISMATCH`, `SELF_TRANSFER_NOT_ALLOWED`), not an enum.

## Validation
- Input validation is declarative via Bean Validation annotations on the `TransferRequest` record components (`@NotBlank`, `@NotNull`, `@Pattern(regexp="\\d{8}")`, `@DecimalMin("0.01")`), triggered by `@Valid` in the controller.
- Business validation (cross-entity rules) lives in the service (`TransferService.validate`), separate from input validation.

## Transactions
- Service methods that mutate state are annotated `@Transactional` (`org.springframework.transaction.annotation.Transactional`). Balance changes on `Account` are flushed by JPA dirty-checking at commit — no explicit `save` on accounts.

## Money & types
- Money is always `BigDecimal` (never double/float). Entities map it with `precision = 19, scale = 2`.
- `BigDecimal` comparisons use `compareTo` (see `validate`), never `equals`. Tests assert with `isEqualByComparingTo`.

## Testing pattern
- Framework: JUnit 5 (Jupiter) + AssertJ (`assertThat`), from spring-boot-starter-test.
- Style: `@SpringBootTest` + `@Transactional` integration tests using real beans and real (in-memory H2) repositories — **nothing is mocked**. Dependencies injected via `@Autowired` fields.
- Structure: `@BeforeEach setUp()` clears tables (`deleteAll`) and seeds fixture accounts; one behavior per `@Test`; method names are full sentences (`rejectsTransferWhenInsufficientFunds`, `replayWithSameIdempotencyKeyReturnsOriginalResultWithoutDoubleDebit`).
- A small private helper builds request objects (`request(key, source, destination, amount)`).
- Tests exercise the service layer directly (not via HTTP/MockMvc in the current suite).
