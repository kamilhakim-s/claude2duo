# SERVICE-BRIEF — transfer-service

> Spring Boot 3.3.5 · Java 21 · H2 in-memory · Gradle KTS · root pkg `com.example.payments`

Immediate payments between internal accounts. One endpoint, idempotent, business
rejections persisted as REJECTED transfers (returned with 201, not errors).

## Package map
| Package | Classes |
|---|---|
| .controller | TransferController, GlobalExceptionHandler |
| .dto | TransferRequest, TransferResponse (records) |
| .service | TransferService (all business rules), AccountNotFoundException |
| .repository | AccountRepository, TransferRepository |
| .model | Account, Transfer (+ nested Transfer.Status enum) |

## Runtime flow
```
POST /api/v1/transfers → TransferController.createTransfer(@Valid) [201]
 → TransferService.execute [@Transactional]
    1 findByIdempotencyKey → replay? return original
    2 findBySortCodeAccountNumber ×2 → miss? AccountNotFoundException → 404
    3 validate(): SELF_TRANSFER_NOT_ALLOWED → CURRENCY_MISMATCH → INSUFFICIENT_FUNDS
      violation ⇒ persist REJECTED (still 201)
    4 ok ⇒ debit/credit (dirty checking) ⇒ persist COMPLETED
 → TransferResponse.from(saved)
```

## Endpoints
| Method | Path | Purpose |
|---|---|---|
| POST | /api/v1/transfers | Execute (or replay) a transfer — the only endpoint; no GETs exist |

## Entities
| Entity | Table | Key facts |
|---|---|---|
| Account | accounts | sortCodeAccountNumber unique len-8 business key; currency String; balance dec(19,2); no @Version |
| Transfer | transfers | idempotencyKey unique; 2× @ManyToOne Account; status enum STRING; rejectionReason nullable; createdAt from ctor |

Schema from entities via `ddl-auto: create-drop`; no migration tool; data lost on restart.
Config: single application.yml, no profiles/flags/secrets. Tests: `TransferServiceTest`
(@SpringBootTest, real beans, AssertJ) — run `./gradlew test`.
