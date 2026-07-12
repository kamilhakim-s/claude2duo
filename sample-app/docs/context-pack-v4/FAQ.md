# FAQ — transfer-service

**Q1. Where do I add a new endpoint?**
`TransferController` (or a new `XxxController` in `..controller`) — delegation only;
logic goes in `TransferService`. See RECIPES R1/R2.

**Q2. What's the error response format?**
RFC-7807 `ProblemDetail`, produced by `GlobalExceptionHandler` — but ONLY for
`AccountNotFoundException` (404). Bean-validation failures use Spring's default 400
body; unhandled exceptions → default 500.

**Q3. Why does a rejected transfer return 201, not 4xx?**
By design: business rejections are persisted `REJECTED` transfers (audit trail) and are
successful *processing*. Consumers branch on `status`/`rejectionReason`.

**Q4. Which rejections exist and where are they decided?**
`TransferService.validate()`, first match wins, in order: `SELF_TRANSFER_NOT_ALLOWED`,
`CURRENCY_MISMATCH`, `INSUFFICIENT_FUNDS`.

**Q5. How does idempotency work?**
`TransferRepository.findByIdempotencyKey` short-circuits `execute()`; replays return
the original transfer (even if the replay's payload differs!). A DB unique constraint
on `idempotencyKey` backs it up.

**Q6. How do I add a field to Transfer, including the migration?**
RECIPES R3. There IS no migration: `ddl-auto: create-drop` regenerates the schema from
entities each start. Update the entity, both `new Transfer(...)` call sites in
`execute()`, both DTO records, and the tests.

**Q7. How is validation done?**
Annotations on the request record (`@NotBlank`, `@Pattern("\\d{8}")`, `@NotNull`,
`@DecimalMin("0.01")`) + `@Valid` in the controller. Stateful rules → service.

**Q8. What do account numbers look like?**
Exactly 8 digits (`@Pattern \d{8}`), stored in `Account.sortCodeAccountNumber`
(unique, length 8) — it's the business key used for lookups.

**Q9. How do I run the tests? Only integration tests?**
`./gradlew test`. There is only one layer — `TransferServiceTest`
(`@SpringBootTest`); no separate unit/integration split exists.

**Q10. What gets mocked in tests?**
Nothing. Real beans + in-memory H2, `@Transactional` rollback per test.

**Q11. How do I add config for one environment only?**
No profile mechanism exists yet (single `application.yml`, no
`application-<env>.yml`). Environment strategy: UNKNOWN — verify with the team.

**Q12. Where are the DB connection settings / secrets?**
`application.yml` → `jdbc:h2:mem:transfers`, no credentials. No secret mechanism in
this repo.

**Q13. How are balances updated — do I need to save the Account?**
No. `Account.debit/credit` mutate managed entities inside `@Transactional
TransferService.execute`; JPA dirty checking flushes them. Don't add
`accountRepository.save(...)`.

**Q14. Is money handled safely?**
`BigDecimal` with `decimal(19,2)` columns; compare with `compareTo`
(`isEqualByComparingTo` in tests). Never use `equals` or doubles.

**Q15. What's the riskiest thing here?**
No locking/`@Version` on `Account`: concurrent transfers can double-spend. Flag any
balance-touching change. Runners-up: replay ignores payload differences; `create-drop`
schema; free-string `currency` compared exactly.

**Q16. Can I query transfers over HTTP?**
No GET endpoints exist. Adding one is RECIPES R1.

**Q17. Where would a new business rule go?**
Extend `TransferService.validate()` returning a new SCREAMING_SNAKE_CASE reason —
append after existing checks unless ordering is explicitly intended (order is
observable behaviour).

**Q18. Which classes may touch repositories?**
Only `TransferService` does today; keep repository access in the service layer.

**Q19. What Java/Spring versions do I write for?**
Java 21 (records, `var`), Spring Boot 3.3.5 (jakarta.* namespaces, ProblemDetail).

**Q20. Is there logging/metrics I should extend?**
None exists. Adding observability establishes a new pattern — say so in the plan/MR.
