# Acceptance controls: MIG-1061-DEMO

Acceptance path: acceptance/ (protected)

## Rules

- A valid record has non-null account_id, report_date and amount.
- Valid input and output record counts match.
- Reversal records remain present.
- |sum(amount, valid input) − sum(amount, output)| ≤ 0.01.
- Every required dimension remains populated.
- The implementation builds.
- Every fixed acceptance test passes.
- No required owner decision remains open.

## Required evidence

- Kiro Spec summaries
- build result
- starter vs Kiro acceptance results
- acceptance-suite hash before/after