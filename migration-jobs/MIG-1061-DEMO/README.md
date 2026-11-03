# MIG-1061-DEMO: Liquidity report semantic transformation

This job rebuilds a synthetic CSV liquidity report transformation as versioned code. The result must preserve valid records, reversal records, approved totals, required dimensions, and source row lineage.

## Job contract

| Item | Value |
|---|---|
| Revision | 1 |
| Business owner | Demo Finance Owner |
| Source | Synthetic CSV report extracts |
| Target | Synthetic Parquet reporting dataset |
| Blueprint | `BP-LIQUIDITY` version 1 |
| Contract fingerprint | `6f2b4cfdca22482d27e286b172d05da27ce15248f79f4a0340e79ca85402b0ee` |
| Development branch | `factory/MIG-1061-DEMO/r1` |

Read `request.json` and `blueprint.json` before changing code. The contract fingerprint in `contract.sha256` must match the fingerprint recorded in every job evidence file.

## Developer locations

- Implementation: `migration_factory/transform.py`
- Unit tests: `tests/test_transform_unit.py`
- Protected acceptance suite: `acceptance/test_liquidity_acceptance.py`
- Synthetic input: `data/input/liquidity_extract.csv`
- Protected expected output: `data/expected/liquidity_report_rows.json`
- Kiro steering: `.kiro/steering/MIG-1061-DEMO/`
- Kiro Spec: `.kiro/specs/MIG-1061-DEMO/`
- Validation evidence: `evidence/`

## Validate the job

Run these commands from the repository root:

```bash
python3 -m compileall -q migration_factory tests
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 -m unittest discover -s acceptance -p 'test_*.py' -v
shasum -a 256 acceptance/README.md acceptance/test_liquidity_acceptance.py
```

A reviewable result requires:

- All unit and acceptance tests pass.
- The protected acceptance hashes remain unchanged.
- Valid input and output record counts match.
- Reversal records remain present.
- The amount difference stays within `0.01`.
- Required dimensions remain populated.
- Every output row retains source lineage.
- No required owner decision remains open.

Do not edit `acceptance/` or `data/expected/` to make the implementation pass.
