# Conventions — transfer-service

> Derived from the actual code, not generic best practice.

## Layering rules
- `controller` → `service` → `repository`. Controllers never touch repositories or
  entities directly.
- **All business rules live in the service layer** (`TransferService.validate`), never in
  controllers or entities. Entities hold only their own state transitions
  (`Account.debit/credit`).
- DTO boundary: controllers accept/return records from `..dto`; entities never appear in
  API types. Conversion is a static factory on the response record:
  `TransferResponse.from(Transfer)`.

## Naming patterns
- Controller `XxxController`, service `XxxService`, repository `XxxRepository`, request
  `XxxRequest`, response `XxxResponse`, exception `XxxException`.
- Enum for state lives nested in its entity (`Transfer.Status`).
- Rejection reasons are SCREAMING_SNAKE_CASE string constants returned from
  `validate()` (e.g. `INSUFFICIENT_FUNDS`).

## Error handling pattern
Two distinct categories — keep them separate when adding rules:
1. **Request errors** → runtime exception in `..service` (e.g.
   `AccountNotFoundException`) mapped to a ProblemDetail response in
   `GlobalExceptionHandler` (`@RestControllerAdvice`, one `@ExceptionHandler` per
   exception, `ProblemDetail.forStatusAndDetail`).
2. **Business rule outcomes** → NOT exceptions. `TransferService.validate` returns a
   reason string; the transfer is persisted as REJECTED and returned normally (201).

## Validation approach
Jakarta bean validation annotations directly on request-record components
(`@NotBlank`, `@Pattern`, `@NotNull`, `@DecimalMin`), triggered by `@Valid` on the
controller parameter. No custom validators. Cross-field/stateful rules go in the
service, not in annotations.

## Transactions
One `@Transactional` (Spring's annotation, not Jakarta's) on the public service method.
Balance changes rely on dirty checking within that transaction.

## DTOs
Java records only. Response mapping via static `from(...)` factory on the record.

## Testing conventions
See TESTING.md — `@SpringBootTest @Transactional` with real repositories (no mocks),
AssertJ, private request-builder helper methods.

## Reusable utilities
There is no shared utility/helper package in this repo. Follow the patterns above rather
than introducing new abstractions.
