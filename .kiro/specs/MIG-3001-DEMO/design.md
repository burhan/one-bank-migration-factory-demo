# Design: MIG-3001-DEMO revision 1

No implementation code is part of this spec. This document describes the intended versioned-code design.

## Scope and inputs
- Source: `data/input/liquidity_extract.csv` (columns: transaction_id, account_id, booking_date, currency, record_type, amount, original_transaction_id). Synthetic.
- Existing code: `migration_factory/transform.py`, `normalize_liquidity_rows`, returning logical rows (strings) sorted by `transaction_id`, with `lineage_source`.
- Target: synthetic Parquet reporting dataset. Logical rows are the contract; the Parquet schema is pending OD-5.

## Components
1. **Reader**: read CSV with `csv.DictReader`, keep 1-based file row numbers (header is row 1, first data row is 2) for lineage.
2. **Validator**: check required fields, record_type in {CR, DR, RV}, parsable Decimal amount, non-empty currency, and the dimension fields of R4. Invalid rows go to a reject report with row number and reason. Disposition per OD-4.
3. **Signer**: CR is +amount, DR is -amount. RV is the negation of the referenced transaction's signed amount, resolved by `original_transaction_id` lookup over all source rows (two-pass, order independent). The current starter code treats RV as a debit (`-amount`), which gives -25000.00 for TXN-1003 and breaks reconciliation of the DR/RV pair. Unresolved references follow OD-3.
4. **Dimension enrichment**: add `entity`, `maturity_bucket`, `report_date` once OD-1 provides authorized mapping. Until then the design only defines the hook (a mapping input), no default values.
5. **Reconciler**: compute totals per currency (OD-2) with Decimal; assert abs(expected - output) <= Decimal("0.01"); raise with the difference otherwise.
6. **Serializer**: write logical rows to Parquet per the schema from OD-5. Amounts as decimal with scale 2, not float. Because the repository is stdlib only, the Parquet writer dependency is itself a decision to confirm (OD-5); logical rows remain the tested contract.

## Output row (current contract, from data/expected)
transaction_id, account_id, booking_date, currency, record_type, signed_amount, original_transaction_id, lineage_source. R4 adds entity, maturity_bucket, report_date once OD-1 is resolved. Note that adding fields changes the logical row shape, so the protected expected fixture would no longer match. This conflict needs resolution through the owner of the acceptance contract (OD-6), not by editing protected files.

## Determinism
Sort by transaction_id, no timestamps or randomness in output, Decimal quantized to 0.01.

## Validation strategy
- Unit tests under `tests/` for each sign rule, absent-original reversal, invalid rows, mandatory dimensions, reconciliation pass and fail at the 0.01 boundary, determinism (run twice, compare).
- Protected acceptance suite run unchanged: `python3 -m unittest discover -s acceptance -p 'test_*.py' -v`. The reversal case fails on the starter by design and should pass after the Signer fix.
- Hash `acceptance/` and `data/expected/` before and after (see manifest.sha256) and require equality.
- No network, synthetic data only.

## Sample reconciliation (synthetic)
USD: +125000.00 - 25000.00 + 25000.00 = 125000.00 (signed, with RV as negation of DR). EUR: 43000.50. Whether the expected total for USD is 125000.00 or something else depends on OD-2.
