# Migration jobs

Each directory in this collection is the authoritative record for one migration job. Directory names use the job ID exactly as it appears in Quick, Jira, evidence, and branch names.

## Required files

A job directory contains:

- `README.md`: developer context and validation commands for the job.
- `request.json`: approved intent, ownership, controls, and required evidence.
- `blueprint.json`: the versioned migration blueprint applied to the job.
- `contract.sha256`: the fingerprint that binds the request to its implementation evidence.

Related artifacts use the same job ID:

- `.kiro/steering/<job-id>/`
- `.kiro/specs/<job-id>/`
- a feature branch named `factory/<job-id>/r<revision>`
- evidence whose `jobId`, revision, and contract fingerprint match the job record

## Add a job

1. Create `migration-jobs/<job-id>/`.
2. Add the required files without copying evidence from another job.
3. Create a feature branch for the job revision.
4. Add steering that records the approved scope and controls.
5. Let Kiro create the Spec, implementation, tests, and validation evidence on that branch.

Do not reuse a contract fingerprint across different requests or revisions.
