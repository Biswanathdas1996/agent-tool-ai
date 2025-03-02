CATEGORY = {
  "transactions": [
    {
      "category": "Customer Payments and Cheques",
      "message_type": "MT103",
      "sender": "BANKABC",
      "receiver": "BANKXYZ",
      "transaction_details": {
        "sender_account": "123456789",
        "receiver_account": "987654321",
        "amount": "1000.00",
        "currency": "USD",
        "payment_date": "2025-03-02",
        "purpose": "Invoice payment"
      },
      "message": "Payment for invoice 12345"
    },
    {
      "category": "Financial Institution Transfers",
      "message_type": "MT202",
      "sender": "BANKABC",
      "receiver": "BANKXYZ",
      "transaction_details": {
        "sending_institution": "BANKABC",
        "receiving_institution": "BANKXYZ",
        "amount": "5000000",
        "currency": "EUR",
        "transaction_date": "2025-03-02",
        "payment_type": "Foreign Exchange"
      },
      "message": "FX settlement for EUR/USD"
    },
    {
      "category": "Treasury Markets and Trade Finance",
      "message_type": "MT700",
      "sender": "BANKABC",
      "receiver": "BANKXYZ",
      "transaction_details": {
        "letter_of_credit_number": "LC123456",
        "issuing_bank": "BANKABC",
        "beneficiary": "SUPPLIER123",
        "amount": "250000",
        "currency": "USD",
        "expiry_date": "2025-04-01",
        "purpose": "Payment for goods"
      },
      "message": "Issuance of letter of credit for trade transaction"
    },
    {
      "category": "Securities and Investment Transactions",
      "message_type": "MT540",
      "sender": "BANKABC",
      "receiver": "BANKXYZ",
      "transaction_details": {
        "security_id": "AAPL1234",
        "quantity": "1000",
        "price_per_unit": "150.00",
        "transaction_date": "2025-03-02",
        "settlement_date": "2025-03-04",
        "amount": "150000",
        "currency": "USD",
        "transaction_type": "Buy"
      },
      "message": "Purchase of 1000 shares of AAPL"
    },
    {
      "category": "Foreign Exchange and Money Market",
      "message_type": "MT300",
      "sender": "BANKABC",
      "receiver": "BANKXYZ",
      "transaction_details": {
        "currency_pair": "EUR/USD",
        "notional_amount": "1000000",
        "exchange_rate": "1.2150",
        "transaction_date": "2025-03-02",
        "settlement_date": "2025-03-03",
        "transaction_type": "Spot"
      },
      "message": "Foreign exchange transaction for EUR/USD"
    },
    {
      "category": "Bill of Exchange and Guarantees",
      "message_type": "MT700",
      "sender": "BANKABC",
      "receiver": "BANKXYZ",
      "transaction_details": {
        "bill_of_exchange_number": "BE123456",
        "beneficiary": "SUPPLIER123",
        "amount": "50000",
        "currency": "USD",
        "issue_date": "2025-03-02",
        "maturity_date": "2025-03-30"
      },
      "message": "Issuance of bill of exchange for payment"
    },
    {
      "category": "SWIFTNet",
      "message_type": "MT999",
      "sender": "SWIFT",
      "receiver": "BANKXYZ",
      "transaction_details": {
        "status": "Network status update",
        "message": "SWIFT network maintenance notice"
      },
      "message": "Scheduled maintenance window on 2025-03-03"
    },
    {
      "category": "Other Payments",
      "message_type": "MT202",
      "sender": "BANKABC",
      "receiver": "BANKXYZ",
      "transaction_details": {
        "sender_account": "123456789",
        "receiver_account": "987654321",
        "amount": "25000",
        "currency": "USD",
        "payment_date": "2025-03-02",
        "purpose": "Loan repayment"
      },
      "message": "Repayment of loan"
    }
  ]
}
