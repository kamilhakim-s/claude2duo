package com.example.payments.controller;

import com.example.payments.dto.TransferRequest;
import com.example.payments.dto.TransferResponse;
import com.example.payments.service.TransferService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/transfers")
public class TransferController {

    private final TransferService transferService;

    public TransferController(TransferService transferService) {
        this.transferService = transferService;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public TransferResponse createTransfer(@Valid @RequestBody TransferRequest request) {
        return transferService.execute(request);
    }
}
