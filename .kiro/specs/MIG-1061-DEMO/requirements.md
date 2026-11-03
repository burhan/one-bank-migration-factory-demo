# Requirements: MIG-1061-DEMO

## Objective

Normalize the synthetic liquidity extract into deterministic reporting rows while preserving every valid source record and its transaction-level lineage.

## Functional requirements

1. Credits produce positive signed amounts.
2. Debits produce negative signed amounts.
3. A reversal produces the opposite economic sign of the credit or debit identified by `original_transaction_id`.
4. A reversal whose referenced transaction is absent or is not a credit or debit fails with a clear validation error.
5. Output rows retain the source transaction ID, account ID, booking date, currency, record type, original transaction ID, and source-line lineage.
6. Output order remains deterministic by transaction ID.

## Acceptance criteria

- All unit tests pass.
- The protected acceptance suite passes without changes to `acceptance/` or `data/expected/`.
- The acceptance-suite hash remains `723727f67b436efec99cd4f8af4b6278fa9b1adf3da576902531e47c5cda3d16`.
- No required business-owner decision remains open.
