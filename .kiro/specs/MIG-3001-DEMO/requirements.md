# Requirements: MIG-3001-DEMO revision 1

Liquidity report semantic transformation. Source: synthetic CSV report extracts. Target: synthetic Parquet reporting dataset. Blueprint: Liquidity report transformation blueprint v1 (content not in repository, see OD-7). Jira: MFD-2. Base branch: main.

Business objective: preserve the synthetic report population and expected totals while rebuilding the transformation as versioned code.

## Glossary

- **Transformation**: `normalize_liquidity_rows` in `migration_factory/transform.py` and its Parquet serialization step.
- **Valid record**: a source row that passes the validation rules in OD-4.
- **Expected input total**: the control total defined in OD-2.
- **Output total**: the sum of `signed_amount` over output rows on the same basis.

## Requirements

### R1 Preserve valid source records (control: preserve valid source records)
1. WHEN a source row is a valid record, THE Transformation SHALL emit exactly one output row for it.
2. THE Transformation SHALL NOT drop, merge, or duplicate valid records.
3. IF a source row is not valid, THEN THE Transformation SHALL report it with its source row number and reason, and SHALL NOT silently discard it (disposition per OD-4).

### R2 Keep reversal records in output (control: keep reversal records in output)
1. WHEN a source row has record_type `RV`, THE Transformation SHALL include it in the output.
2. WHEN a reversal references an original transaction present in the source, THE Transformation SHALL set its signed amount to the economic negation of the referenced transaction's signed amount (a reversal of a debit of 25000.00 yields +25000.00; a reversal of a credit yields a negative amount). Sign semantics are confirmed by OD-3.
3. THE Transformation SHALL retain `original_transaction_id` on reversal rows.
4. IF a reversal references an original that is absent, THEN THE Transformation SHALL follow the handling decided in OD-3 and SHALL NOT guess a sign.

### R3 Total reconciliation (control: difference within 0.01)
1. THE Transformation SHALL compute expected input total and output total on the basis decided in OD-2, using Decimal arithmetic.
2. WHEN the reconciliation runs, THE Transformation SHALL require abs(expected input total - output total) <= 0.01 in the synthetic currency unit.
3. IF the difference exceeds 0.01, THEN THE Transformation SHALL fail the run and report the difference.
4. Totals SHALL NOT be summed across currencies unless OD-2 authorizes a conversion basis; USD and EUR rows are present in the sample.

### R4 Mandatory dimensions populated (control: entity, currency, maturity_bucket, report_date populated)
1. THE Transformation SHALL populate `entity`, `currency`, `maturity_bucket`, and `report_date` on every output row, with no null or empty values.
2. The source has no `entity`, `maturity_bucket`, or `report_date` columns. THE Transformation SHALL NOT invent derivation rules; mappings follow OD-1.
3. IF a value cannot be populated from an authorized rule, THEN THE Transformation SHALL treat the record per OD-4 and report it.

### R5 Synthetic data only (control)
1. THE repository, fixtures, tests, and evidence SHALL contain synthetic data only, with no credentials or customer data.
2. THE Transformation SHALL NOT use network access.

### R6 Lineage and determinism
1. THE Transformation SHALL set `lineage_source` on each output row as `<file>:<row_number>:<transaction_id>`.
2. WHEN given identical input, THE Transformation SHALL produce identical output, ordered by `transaction_id`.

### R7 Governance controls
1. Work SHALL occur on branch `factory/MIG-3001-DEMO/r1`; the primary branch SHALL NOT be changed.
2. Files under `acceptance/` and `data/expected/` SHALL NOT be modified; the acceptance-suite hash SHALL be recorded before and after implementation and be identical.
3. WHERE business authority is missing, THE specification SHALL record an open decision in `open-decisions.md` and SHALL NOT invent an answer.

## Open decisions referenced
OD-1 to OD-7 are in `open-decisions.md`. R2.2, R3, R4 and R1.3 are conditional on them.
