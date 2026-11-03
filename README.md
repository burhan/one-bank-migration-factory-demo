# One Bank Migration Factory

This repository is the developer workspace for versioned migration jobs. Each job has an authoritative record under `migration-jobs/<job-id>/`. Implementation changes, Kiro Specs, tests, acceptance controls, and evidence remain in Git so reviewers can reproduce every result.

The repository currently contains synthetic data only. It does not contain customer records or production configuration.

## Repository layout

| Path | Purpose |
|---|---|
| `migration-jobs/<job-id>/` | Request, blueprint, contract fingerprint, and job documentation |
| `.kiro/steering/<job-id>/` | Job constraints supplied to Kiro |
| `.kiro/specs/<job-id>/` | Requirements, design, and implementation tasks created by Kiro |
| `migration_factory/` | Versioned transformation code |
| `tests/` | Developer unit tests |
| `acceptance/` | Protected acceptance suite |
| `data/input/` | Synthetic source fixtures |
| `data/expected/` | Protected expected results |
| `evidence/` | Validation and implementation evidence for the active job revision |

Shared code and controls stay at the repository root. Job identity and authoritative inputs stay under the matching job directory. Development occurs on a job revision branch such as `factory/MIG-1061-DEMO/r1`.

## Work on a migration job

1. Open the job directory and read its `README.md`, `request.json`, and `blueprint.json`.
2. Confirm that the current branch matches the job and revision.
3. Read the matching steering files under `.kiro/steering/<job-id>/`.
4. Record the protected acceptance suite hash before changing implementation code.
5. Create or update the Kiro Spec under `.kiro/specs/<job-id>/`.
6. Change implementation code and developer tests. Do not edit protected acceptance files or expected results.
7. Run the build, unit tests, and protected acceptance suite.
8. Record the resulting hashes and test results under `evidence/`.
9. Commit the job revision and submit it for review.

## Validate the current job

Compile the implementation and tests:

```bash
python3 -m compileall -q migration_factory tests
```

Run unit tests:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Run the protected acceptance suite:

```bash
python3 -m unittest discover -s acceptance -p 'test_*.py' -v
```

Verify the protected suite against its manifest:

```bash
shasum -a 256 acceptance/README.md acceptance/test_liquidity_acceptance.py
```

The computed hashes must match `acceptance/manifest.sha256` and the before and after hashes recorded in `evidence/validation-result.json`.

## Development controls

- Use synthetic data only.
- Work on a job revision branch. Do not change the primary branch directly.
- Do not modify files under `acceptance/` or `data/expected/` while implementing a job.
- Preserve transaction-level lineage from every output row to its source row.
- Keep output deterministic for identical input.
- Return unresolved business decisions to the named owner instead of inventing an answer.
- Report validation failures accurately.
