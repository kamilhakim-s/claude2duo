package com.example.payments;

import com.example.payments.dto.TransferRequest;
import com.example.payments.dto.TransferResponse;
import com.example.payments.model.Account;
import com.example.payments.repository.AccountRepository;
import com.example.payments.repository.TransferRepository;
import com.example.payments.service.TransferService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
@Transactional
class TransferServiceTest {

    @Autowired
    private TransferService transferService;

    @Autowired
    private AccountRepository accountRepository;

    @Autowired
    private TransferRepository transferRepository;

    private Account alice;
    private Account bob;

    @BeforeEach
    void setUp() {
        transferRepository.deleteAll();
        accountRepository.deleteAll();
        alice = accountRepository.save(new Account("11111111", "GBP", new BigDecimal("100.00")));
        bob = accountRepository.save(new Account("22222222", "GBP", new BigDecimal("50.00")));
    }

    @Test
    void completesTransferWhenFundsAvailable() {
        var response = transferService.execute(request("key-1", "11111111", "22222222", "40.00"));

        assertThat(response.status()).isEqualTo("COMPLETED");
        assertThat(alice.getBalance()).isEqualByComparingTo("60.00");
        assertThat(bob.getBalance()).isEqualByComparingTo("90.00");
    }

    @Test
    void rejectsTransferWhenInsufficientFunds() {
        var response = transferService.execute(request("key-2", "11111111", "22222222", "500.00"));

        assertThat(response.status()).isEqualTo("REJECTED");
        assertThat(response.rejectionReason()).isEqualTo("INSUFFICIENT_FUNDS");
        assertThat(alice.getBalance()).isEqualByComparingTo("100.00");
    }

    @Test
    void replayWithSameIdempotencyKeyReturnsOriginalResultWithoutDoubleDebit() {
        TransferResponse first = transferService.execute(request("key-3", "11111111", "22222222", "40.00"));
        TransferResponse replay = transferService.execute(request("key-3", "11111111", "22222222", "40.00"));

        assertThat(replay.id()).isEqualTo(first.id());
        assertThat(alice.getBalance()).isEqualByComparingTo("60.00");
    }

    @Test
    void rejectsSelfTransfer() {
        var response = transferService.execute(request("key-4", "11111111", "11111111", "10.00"));

        assertThat(response.status()).isEqualTo("REJECTED");
        assertThat(response.rejectionReason()).isEqualTo("SELF_TRANSFER_NOT_ALLOWED");
    }

    private TransferRequest request(String key, String source, String destination, String amount) {
        return new TransferRequest(key, source, destination, new BigDecimal(amount));
    }
}
