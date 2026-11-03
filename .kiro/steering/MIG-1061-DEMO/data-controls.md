# Data controls: MIG-1061-DEMO

- Preserve valid source records.
- Keep reversal records in the output.
- Keep the difference between expected input and output totals within 0.01 in the synthetic currency unit.
- Keep entity, currency, maturity_bucket, and report_date populated.
- Use synthetic data only.
- Do not change the primary branch.
- Do not modify the protected acceptance suite.
- Return an open decision when business authority is missing.

## Required dimensions

- entity
- currency
- maturity_bucket
- report_date

Amount tolerance: 0.01