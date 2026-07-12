# Working in this codebase

> The rules we actually follow, taken from the code — not aspirations.

## Layering — non-negotiable
`controller → service → repository`. Controllers are thin (look at
`TransferController`: constructor injection, one method, zero logic). **Every business
rule goes in the service** — `TransferService.validate` is the reference. Entities keep
only their own state transitions (`Account.debit/credit`). Entities never cross the API
boundary: response records own the mapping via a static factory
(`TransferResponse.from(Transfer)`).

## Naming
`XxxController` / `XxxService` / `XxxRepository` / `XxxRequest` / `XxxResponse` /
`XxxException`. State enums nest inside their entity (`Transfer.Status`). Rejection
reasons are SCREAMING_SNAKE_CASE strings returned by `validate()`.

## Error handling — two lanes, don't mix them
1. *Can't process the request at all* (unknown account) → runtime exception in the
   service (`AccountNotFoundException`) + one `@ExceptionHandler` in
   `GlobalExceptionHandler` returning `ProblemDetail.forStatusAndDetail`. Follow this
   exact shape for new request errors.
2. *Business says no* → NOT an exception. Persist the REJECTED outcome, return 201.
   If you're adding a rule, extend `validate()` and return a new reason string.

## Validation
Annotations on request-record components + `@Valid` in the controller. Anything needing
DB state or two fields goes in the service. No custom validator classes exist.

## Transactions
`@Transactional` (Spring's) on the public service method. Balance updates rely on dirty
checking inside it — don't add redundant `save(account)` calls.

## Testing — copy `TransferServiceTest`
`@SpringBootTest` + `@Transactional`, real beans, nothing mocked. `@BeforeEach` wipes
both repos then seeds `alice ("11111111", GBP, 100.00)` / `bob ("22222222", GBP,
50.00)`. AssertJ everywhere; `isEqualByComparingTo` for money. Behaviour-sentence
method names (`rejectsSelfTransfer`). Private `request(...)` helper builds DTOs. New
currency cases: create the EUR account inside your test. There is no MockMvc precedent;
introducing one is a deliberate new pattern, flag it in review.

## Build & run
`./gradlew test` / `bootRun` (H2 in-memory, zero setup). No Dockerfile, manifests, or
CI in this repo — deployment story: UNKNOWN — verify with the team.

## Config
Single `application.yml` (name, H2 url, ddl-auto). No profiles, no flags, no secrets,
and no `@Value`/`@ConfigurationProperties` precedent — the first config consumer sets
the pattern; prefer a `@ConfigurationProperties` record and say so in the MR.
