package com.example.payments.dto;

import com.example.payments.model.Transfer;

import java.math.BigDecimal;
import java.time.Instant;

public record TransferResponse(
        Long id,
        String sourceAccount,
        String destinationAccount,
        BigDecimal amount,
        String status,
        String rejectionReason,
        Instant createdAt
) {
    public static TransferResponse from(Transfer transfer) {
        return new TransferResponse(
                transfer.getId(),
                transfer.getSource().getSortCodeAccountNumber(),
                transfer.getDestination().getSortCodeAccountNumber(),
                transfer.getAmount(),
                transfer.getStatus().name(),
                transfer.getRejectionReason(),
                transfer.getCreatedAt()
        );
    }
}
