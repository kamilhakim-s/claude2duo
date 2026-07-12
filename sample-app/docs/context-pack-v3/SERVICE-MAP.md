# SERVICE-MAP — transfer-service
Immediate payments between internal accounts; one POST endpoint; idempotent; rejections persisted, not thrown.
Gen 2026-07-12 · commit b225393 · Boot 3.3.5 · Java 21 · H2 mem · Gradle KTS
Legend: C=controller S=service R=repository E=entity pkg root `com.example.payments`

## PACKAGES
| pkg | role |
|---|---|
| (root) | `TransferServiceApplication` boot main |
| .controller | `TransferController` (C), `GlobalExceptionHandler` (@RestControllerAdvice) |
| .dto | `TransferRequest`, `TransferResponse` records |
| .service | `TransferService` (S, all business rules), `AccountNotFoundException` |
| .repository | `AccountRepository`, `TransferRepository` (Spring Data JPA) |
| .model | `Account` (E), `Transfer` (E, nested enum `Transfer.Status`) |

## FLOW
POST /api/v1/transfers → C.createTransfer(@Valid) 201
→ S.execute [@Transactional]:
  1 R.findByIdempotencyKey → hit ⇒ return original (replay, never re-executes)
  2 R.findBySortCodeAccountNumber ×2 → miss ⇒ AccountNotFoundException → 404 ProblemDetail
  3 S.validate: SELF_TRANSFER_NOT_ALLOWED → CURRENCY_MISMATCH → INSUFFICIENT_FUNDS (first hit wins) ⇒ persist REJECTED, still 201
  4 ok ⇒ source.debit / destination.credit (dirty checking, no explicit save) ⇒ persist COMPLETED
→ TransferResponse.from(saved)

## API (the only endpoint)
| POST /api/v1/transfers | req `TransferRequest` | resp `TransferResponse` 201 |
|---|---|---|
req: idempotencyKey:str @NotBlank · sourceAccount/destinationAccount:str @NotBlank @Pattern \d{8} · amount:dec @NotNull @DecimalMin 0.01
resp: id:num · sourceAccount · destinationAccount · amount · status COMPLETED|REJECTED · rejectionReason|null · createdAt:instant
errors: unknown account→404 ProblemDetail "Account not found: n" · bean validation→400 Spring default (not ProblemDetail) · other→500 (no handler) · business rejection→**201 REJECTED** (by design)
No GET endpoints. No messaging.

## DATA
| entity | table | fields | notes |
|---|---|---|---|
| Account | accounts | sortCodeAccountNumber uniq len8 (business key) · currency str · balance dec(19,2) | mutate only via debit()/credit(); **no @Version** |
| Transfer | transfers | idempotencyKey uniq · source/destination @ManyToOne Account · amount dec(19,2) · status enum STRING · rejectionReason null · createdAt (ctor Instant.now) | immutable, getters only |
Finders: Account.findBySortCodeAccountNumber · Transfer.findByIdempotencyKey (both Optional)
Schema: ddl-auto create-drop from entities; NO migrations tool; data lost on restart.

## CONVENTIONS
- Layering C→S→R strict; ALL rules in S.validate; entities never in API — map via static `TransferResponse.from(Transfer)`
- Names: XxxController/Service/Repository/Request/Response/Exception; enums nested in entity; reasons SCREAMING_SNAKE_CASE strings from validate()
- Errors 2 lanes: request errors = service exception + @ExceptionHandler → ProblemDetail (copy AccountNotFoundException); business outcomes = persisted REJECTED, never exceptions
- Validation: annotations on request records + @Valid in C; stateful/cross-field checks in S; no custom validators
- Tx: one Spring @Transactional on public S method
- Utilities: none exist — don't invent shared helpers

## CONFIG
No profiles, no flags, no secrets. application.yml: name=transfer-service · h2 jdbc:h2:mem:transfers · ddl-auto=create-drop. No @Value/@ConfigurationProperties precedent. Deployment files: none in repo — UNKNOWN, verify with team.

## TESTS
| layer | tooling | run | pattern |
|---|---|---|---|
| service integration | @SpringBootTest @Transactional, real beans, no mocks, AssertJ | ./gradlew test | `TransferServiceTest`: @BeforeEach deleteAll + seed alice(11111111,GBP,100)/bob(22222222,GBP,50); behaviour-sentence names; private request() helper; isEqualByComparingTo for money |
No unit/MockMvc/contract layers exist.

## GOTCHAS
1 No locking on Account balance ⇒ concurrent transfers can double-spend (known debt — flag, don't copy)
2 REJECTED = 201 not error; only missing account is 404 — consumers branch on status
3 create-drop: entity edit = silent schema change; nothing survives restart
4 Replay ignores payload diffs — original returned even if amount differs
5 validate() order is observable: self→currency→funds, first only
6 currency free-string, exact equals ("gbp"≠"GBP")
7 Only AccountNotFoundException handled; 400 body inconsistent with 404 ProblemDetail
8 createdAt from ctor, not auditing
9 Zero logging/metrics — first logger sets the pattern
