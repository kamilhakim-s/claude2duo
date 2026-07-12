package com.example.payments.service;

import com.example.payments.dto.TransferRequest;
import com.example.payments.dto.TransferResponse;
import com.example.payments.model.Account;
import com.example.payments.model.Transfer;
import com.example.payments.repository.AccountRepository;
import com.example.payments.repository.TransferRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Executes single immediate payments between internal accounts.
 *
 * Business rules:
 * 1. Requests are idempotent on idempotencyKey — replays return the original result.
 * 2. Source and destination must both exist.
 * 3. Source and destination must not be the same account.
 * 4. Source and destination must hold the same currency.
 * 5. Source must have sufficient balance.
 * Rule violations 3-5 persist a REJECTED transfer rather than throwing.
 */
@Service
public class TransferService {

    private final AccountRepository accountRepository;
    private final TransferRepository transferRepository;

    public TransferService(AccountRepository accountRepository, TransferRepository transferRepository) {
        this.accountRepository = accountRepository;
        this.transferRepository = transferRepository;
    }

    @Transactional
    public TransferResponse execute(TransferRequest request) {
        var existing = transferRepository.findByIdempotencyKey(request.idempotencyKey());
        if (existing.isPresent()) {
            return TransferResponse.from(existing.get());
        }

        Account source = accountRepository.findBySortCodeAccountNumber(request.sourceAccount())
                .orElseThrow(() -> new AccountNotFoundException(request.sourceAccount()));
        Account destination = accountRepository.findBySortCodeAccountNumber(request.destinationAccount())
                .orElseThrow(() -> new AccountNotFoundException(request.destinationAccount()));

        String rejectionReason = validate(source, destination, request);

        Transfer transfer;
        if (rejectionReason != null) {
            transfer = new Transfer(request.idempotencyKey(), source, destination,
                    request.amount(), Transfer.Status.REJECTED, rejectionReason);
        } else {
            source.debit(request.amount());
            destination.credit(request.amount());
            transfer = new Transfer(request.idempotencyKey(), source, destination,
                    request.amount(), Transfer.Status.COMPLETED, null);
        }
        return TransferResponse.from(transferRepository.save(transfer));
    }

    private String validate(Account source, Account destination, TransferRequest request) {
        if (source.getId().equals(destination.getId())) {
            return "SELF_TRANSFER_NOT_ALLOWED";
        }
        if (!source.getCurrency().equals(destination.getCurrency())) {
            return "CURRENCY_MISMATCH";
        }
        if (source.getBalance().compareTo(request.amount()) < 0) {
            return "INSUFFICIENT_FUNDS";
        }
        return null;
    }
}
