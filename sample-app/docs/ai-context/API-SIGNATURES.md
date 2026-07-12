# API-SIGNATURES — transfer-service (repo digest)

> Stack: Spring Boot 3.3.5, Java 21, JPA, H2. Package root: `com.example.payments`. Public members only, signatures only (no bodies). Use this as a substitute for repo-wide search when only some files are attached.

## com.example.payments
```java
@SpringBootApplication
class TransferServiceApplication {
    static void main(String[] args)
}
```

## com.example.payments.controller
```java
@RestController @RequestMapping("/api/v1/transfers")
class TransferController {
    TransferController(TransferService transferService)
    @PostMapping @ResponseStatus(HttpStatus.CREATED)
    TransferResponse createTransfer(@Valid @RequestBody TransferRequest request)   // returns 201
}

@RestControllerAdvice
class GlobalExceptionHandler {
    @ExceptionHandler(AccountNotFoundException.class)
    ProblemDetail handleAccountNotFound(AccountNotFoundException ex)               // returns 404
}
```

## com.example.payments.service
```java
@Service
class TransferService {
    TransferService(AccountRepository accountRepository, TransferRepository transferRepository)
    @Transactional TransferResponse execute(TransferRequest request)
    // private String validate(Account source, Account destination, TransferRequest request)
}

class AccountNotFoundException extends RuntimeException {
    AccountNotFoundException(String accountNumber)   // message: "Account not found: " + accountNumber
}
```

## com.example.payments.repository
```java
interface AccountRepository extends JpaRepository<Account, Long> {
    Optional<Account> findBySortCodeAccountNumber(String sortCodeAccountNumber)
    // inherited: save, findById, findAll, deleteAll, ... (Spring Data JpaRepository)
}

interface TransferRepository extends JpaRepository<Transfer, Long> {
    Optional<Transfer> findByIdempotencyKey(String idempotencyKey)
    // inherited: save, findById, findAll, deleteAll, ... (Spring Data JpaRepository)
}
```

## com.example.payments.model
```java
@Entity @Table(name = "accounts")
class Account {
    Account(String sortCodeAccountNumber, String currency, BigDecimal balance)
    void debit(BigDecimal amount)      // balance -= amount
    void credit(BigDecimal amount)     // balance += amount
    Long getId()
    String getSortCodeAccountNumber()
    String getCurrency()
    BigDecimal getBalance()
    // no setters; protected no-arg ctor for JPA
}

@Entity @Table(name = "transfers")
class Transfer {
    enum Status { COMPLETED, REJECTED }
    Transfer(String idempotencyKey, Account source, Account destination,
             BigDecimal amount, Status status, String rejectionReason)   // sets createdAt = Instant.now()
    Long getId()
    String getIdempotencyKey()
    Account getSource()
    Account getDestination()
    BigDecimal getAmount()
    Status getStatus()
    String getRejectionReason()
    Instant getCreatedAt()
    // no setters; protected no-arg ctor for JPA
}
```

## com.example.payments.dto
```java
record TransferRequest(
    @NotBlank String idempotencyKey,
    @NotBlank @Pattern(regexp="\\d{8}") String sourceAccount,
    @NotBlank @Pattern(regexp="\\d{8}") String destinationAccount,
    @NotNull @DecimalMin("0.01") BigDecimal amount
) {}

record TransferResponse(
    Long id, String sourceAccount, String destinationAccount,
    BigDecimal amount, String status, String rejectionReason, Instant createdAt
) {
    static TransferResponse from(Transfer transfer)
}
```

## Reason codes (String literals, not an enum)
`SELF_TRANSFER_NOT_ALLOWED`, `CURRENCY_MISMATCH`, `INSUFFICIENT_FUNDS`
