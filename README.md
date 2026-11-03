# One Bank Migration Factory Demo

This private repository contains a synthetic workload for validating the One Bank Migration Factory demo. It is intentionally separate from customer and production repositories.

## Demo flow

1. Amazon Quick creates a branch for each revision, such as `factory/MIG-1061-DEMO/r1`.
2. Quick writes the migration request, contract fingerprint, blueprint, and Kiro steering files to that branch.
3. A local worker checks out the branch and asks Kiro to implement the requested transformation.
4. Kiro runs the unit and protected acceptance suites without changing the acceptance files.
5. The worker pushes evidence files and opens a pull request.
6. Quick reads the GitHub evidence and updates the dashboard. A button click alone does not advance the engineering status.

Jira remains the source of truth for business status, ownership, and decisions. GitHub remains the source of truth for code, Specs, tests, commits, pull requests, and validation evidence.

## Included workload

`MIG-1061-DEMO` transforms a synthetic liquidity-report CSV extract into logical rows for a synthetic Parquet reporting dataset. The starter implementation handles credits and debits but deliberately mishandles reversal records. The protected acceptance suite exposes that gap for the Kiro portion of the demo.

All account IDs, transaction IDs, values, dates, and records in this repository are synthetic.

## Run the checks

Run the passing starter unit tests:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Run the protected acceptance suite:

```bash
python3 -m unittest discover -s acceptance -p 'test_*.py' -v
```

The starter implementation is expected to fail the acceptance case for reversal records. Kiro should repair the implementation, not the expected output or acceptance suite.

## Repository controls

- Never add customer data, credentials, access tokens, or production configuration.
- Do not modify files under `acceptance/` while implementing a migration request.
- Preserve deterministic output and lineage to each source record.
- Use feature branches and pull requests. Do not write directly to the protected default branch.
