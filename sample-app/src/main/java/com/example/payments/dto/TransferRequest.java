package com.example.payments.dto;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;

import java.math.BigDecimal;

public record TransferRequest(
        @NotBlank String idempotencyKey,
        @NotBlank @Pattern(regexp = "\\d{8}") String sourceAccount,
        @NotBlank @Pattern(regexp = "\\d{8}") String destinationAccount,
        @NotNull @DecimalMin(value = "0.01") BigDecimal amount
) {
}
