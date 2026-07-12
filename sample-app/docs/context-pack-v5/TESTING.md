# Testing — transfer-service

> JUnit 5 + AssertJ via spring-boot-starter-test · run with `./gradlew test`

## Test layers present
| Layer | Exists? | Example |
|---|---|---|
| Service-level integration (`@SpringBootTest`) | Yes | `com.example.payments.TransferServiceTest` |
| Unit tests (mocked) | No | — |
| Web layer tests (`@WebMvcTest`/MockMvc) | No | — |
| Contract tests | No | — |

## The established pattern (`TransferServiceTest`)
- Class annotations: `@SpringBootTest` + `@Transactional` (each test rolls back).
- Real beans autowired: `TransferService`, `AccountRepository`, `TransferRepository`.
  **Nothing is mocked** — H2 makes the full stack cheap.
- `@BeforeEach setUp()`: `deleteAll()` both repositories, then persist fixture accounts
  `alice ("11111111", GBP, 100.00)` and `bob ("22222222", GBP, 50.00)`.
- Assertions: AssertJ `assertThat`, `isEqualByComparingTo` for BigDecimal balances.
- Private helper builds requests: `request(key, source, destination, amount)`.
- Method names are behaviour sentences: `rejectsTransferWhenInsufficientFunds`,
  `replayWithSameIdempotencyKeyReturnsOriginalResultWithoutDoubleDebit`.

## Writing a new test
Add a method to `TransferServiceTest` following the pattern above; create additional
fixture accounts in the test itself when the defaults don't fit (e.g. a EUR account for
currency-mismatch cases). For a new endpoint, no MockMvc precedent exists — either
extend the service-level style or deliberately introduce `@WebMvcTest` as a new pattern.

## Fixtures
No fixture files/factories; fixtures are built inline in the test class.

## When DTO records change
`TransferRequest` is constructed positionally in the private `request(key, source,
destination, amount)` helper — adding a record component means updating this helper
(and with it all tests at once). Prefer extending the helper's signature over
scattering `new TransferRequest(...)` calls.

## Overriding config in tests
No precedent exists; if needed use `@TestPropertySource` or
`@SpringBootTest(properties = …)` and flag it as a new pattern in the MR.
