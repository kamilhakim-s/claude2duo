# API contracts — transfer-service

> Base path `/api/v1/transfers` · JSON · one endpoint · no auth configured in this repo

## POST /api/v1/transfers — create a transfer
Implemented by `TransferController.createTransfer`. Success status: **201 CREATED** —
including business rejections (see below).

### Request body (`TransferRequest` record)
| Field | Type | Validation |
|---|---|---|
| idempotencyKey | string | @NotBlank |
| sourceAccount | string | @NotBlank, @Pattern `\d{8}` (exactly 8 digits) |
| destinationAccount | string | @NotBlank, @Pattern `\d{8}` |
| amount | decimal | @NotNull, @DecimalMin 0.01 |

### Response body (`TransferResponse` record) — 201
| Field | Type | Notes |
|---|---|---|
| id | number | Transfer id |
| sourceAccount | string | 8-digit account number |
| destinationAccount | string | 8-digit account number |
| amount | decimal | |
| status | string | `COMPLETED` or `REJECTED` (`Transfer.Status` enum) |
| rejectionReason | string/null | `SELF_TRANSFER_NOT_ALLOWED` \| `CURRENCY_MISMATCH` \| `INSUFFICIENT_FUNDS` \| null |
| createdAt | ISO-8601 instant | Set server-side |

### Error responses
| Case | Status | Body | Source |
|---|---|---|---|
| Unknown source/destination account | 404 | RFC-7807 ProblemDetail, detail `"Account not found: <number>"` | `GlobalExceptionHandler.handleAccountNotFound` |
| Bean-validation failure | 400 | Spring Boot default error body (no custom handler) | Spring MVC |
| Business rule violation | **201** with `status=REJECTED` + `rejectionReason` | Not an HTTP error by design | `TransferService.validate` |
| Any other exception | 500 | Spring default | No handler exists |

### Idempotency semantics
Same `idempotencyKey` → the original persisted result is returned verbatim (same id,
same status), regardless of the other fields in the replay request. Uniqueness is also
enforced by a DB unique constraint on `transfers.idempotency_key`.

## Other endpoints / messaging
None. There is no GET endpoint — transfers cannot be queried over HTTP. No message
consumers or producers exist.
