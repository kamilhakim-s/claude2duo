package com.example.payments.model;

import jakarta.persistence.*;

import java.math.BigDecimal;
import java.time.Instant;

@Entity
@Table(name = "transfers")
public class Transfer {

    public enum Status {
        COMPLETED,
        REJECTED
    }

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String idempotencyKey;

    @ManyToOne(optional = false)
    private Account source;

    @ManyToOne(optional = false)
    private Account destination;

    @Column(nullable = false, precision = 19, scale = 2)
    private BigDecimal amount;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Status status;

    private String rejectionReason;

    @Column(nullable = false)
    private Instant createdAt;

    protected Transfer() {
    }

    public Transfer(String idempotencyKey, Account source, Account destination,
                    BigDecimal amount, Status status, String rejectionReason) {
        this.idempotencyKey = idempotencyKey;
        this.source = source;
        this.destination = destination;
        this.amount = amount;
        this.status = status;
        this.rejectionReason = rejectionReason;
        this.createdAt = Instant.now();
    }

    public Long getId() {
        return id;
    }

    public String getIdempotencyKey() {
        return idempotencyKey;
    }

    public Account getSource() {
        return source;
    }

    public Account getDestination() {
        return destination;
    }

    public BigDecimal getAmount() {
        return amount;
    }

    public Status getStatus() {
        return status;
    }

    public String getRejectionReason() {
        return rejectionReason;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }
}
