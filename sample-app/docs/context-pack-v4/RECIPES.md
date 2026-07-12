# RECIPES — how changes are made in transfer-service

Each recipe is distilled from the real code. Follow the file order; the app must compile
after each numbered row. Reference implementations are named — read them before writing.

## R1 · Add a new REST endpoint (query / GET)
WHEN: exposing existing data, e.g. "get transfer by id".
No GET precedent exists — model the class structure on `TransferController` and keep the
service-layer split.
| # | Where | What |
|---|---|---|
| 1 | `..dto` | New response record with static `from(entity)` factory — copy `TransferResponse` |
| 2 | `..repository` | Add finder to `TransferRepository` if `findById` isn't enough (derived query, returns Optional — copy `findByIdempotencyKey`) |
| 3 | `..service` | New method on `TransferService`; not-found ⇒ throw a `..service` exception like `AccountNotFoundException` |
| 4 | `..controller` | `@GetMapping("/{id}")` method on `TransferController`; no logic beyond delegation |
| 5 | `..controller` | `@ExceptionHandler` for the new exception in `GlobalExceptionHandler` → `ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, …)` |
| 6 | test | New methods in `TransferServiceTest` style (see R7) |
PITFALL: don't return the entity — always a response record.

## R2 · Add a new REST endpoint (mutation / POST)
WHEN: a new command, e.g. "create account".
Reference: the whole `TransferController` → `TransferService.execute` chain.
| # | Where | What |
|---|---|---|
| 1 | `..dto` | Request record with bean-validation annotations — copy `TransferRequest` |
| 2 | `..service` | Business method, `@Transactional`, all rules here; outcome-style rejections return persisted state, request errors throw |
| 3 | `..dto` + `..controller` | Response record + `@PostMapping` with `@Valid @RequestBody`, `@ResponseStatus(HttpStatus.CREATED)` |
| 4 | test | Happy path + each rejection/exception path in `TransferServiceTest` style |
PITFALL: decide rejection-vs-exception deliberately — this repo persists business
rejections (201) and throws only for "can't process at all" (R6).

## R3 · Add a field to an existing entity (+ "migration")
WHEN: e.g. add `description` to Transfer.
| # | Where | What |
|---|---|---|
| 1 | `..model.Transfer` | Private field + `@Column` traits + constructor param + getter (entity is immutable — no setter) |
| 2 | — | No migration file: schema is `ddl-auto: create-drop` from entities. State this in the plan; a real environment would need one — UNKNOWN, verify with team |
| 3 | `..dto.TransferRequest` | Add record component with validation annotations (e.g. `@Size(max=140)`; optional ⇒ no `@NotBlank`) |
| 4 | `..service.TransferService` | Pass the value through in BOTH `new Transfer(...)` call sites (REJECTED and COMPLETED branches) |
| 5 | `..dto.TransferResponse` | Add component + map it in `from(Transfer)` |
| 6 | test | Extend `request(...)` helper + add assertions; existing calls must be updated (record constructors are positional) |
PITFALL: `Transfer` has TWO construction sites in `execute()` — update both or the field
is silently null on one path.

## R4 · Add a new entity/table end-to-end
Reference: `Account` + `AccountRepository`.
| # | Where | What |
|---|---|---|
| 1 | `..model` | Entity: `@Entity @Table(name="plural")`, identity PK, protected no-arg ctor + public ctor, no setters unless state transition methods are needed (cf. `Account.debit/credit`) |
| 2 | `..repository` | `interface XxxRepository extends JpaRepository<Xxx, Long>` + derived Optional finders |
| 3 | `..service`/`..dto`/`..controller` | Per R1/R2 as needed |
| 4 | test | Seed instances in `@BeforeEach` like `alice`/`bob` |

## R5 · Add a configuration property / feature flag
No precedent exists (application.yml has only name/datasource/ddl-auto).
| # | Where | What |
|---|---|---|
| 1 | `application.yml` | Add property under a service-specific prefix, e.g. `transfer:` |
| 2 | new `..config` or `..service` | Prefer a `@ConfigurationProperties` record (new pattern — flag in MR); inject into `TransferService` via constructor |
| 3 | test | `@SpringBootTest` picks up application.yml; override with `@TestPropertySource` if needed (also a new pattern) |

## R6 · Handle a new error case
Decide the lane first:
- **Business outcome** (rule says no): add check to `TransferService.validate()`
  returning a new SCREAMING_SNAKE_CASE reason. Order matters — first violation wins;
  append at the end unless the plan says otherwise. Persisted as REJECTED, still 201.
- **Request error** (can't process): new `RuntimeException` subclass in `..service`
  (copy `AccountNotFoundException` — message in constructor), plus an
  `@ExceptionHandler` in `GlobalExceptionHandler` returning
  `ProblemDetail.forStatusAndDetail(<status>, ex.getMessage())`.
PITFALL: never throw for business rules — the audit trail of REJECTED transfers is a
feature.

## R7 · Add a test
Copy the `TransferServiceTest` pattern exactly: `@SpringBootTest @Transactional` class,
autowire real beans, `@BeforeEach` `deleteAll()` + seed accounts
(`new Account("11111111","GBP", new BigDecimal("100.00"))`), behaviour-sentence method
name, AssertJ (`isEqualByComparingTo` for money), private builder helper for requests.
Run: `./gradlew test`.

## R8 · Call another service / external API — NO PATTERN
This repo makes no outbound calls; no RestClient/WebClient/Feign precedent exists.
UNKNOWN — verify with the team before inventing one.

## R9 · Scheduled/async job — NO PATTERN
No `@Scheduled`/`@Async`/executor usage exists. UNKNOWN — verify with the team.
