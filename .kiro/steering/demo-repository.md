# Demo repository controls

- Treat every repository record as synthetic demonstration data.
- Never add credentials, tokens, customer data, or production configuration.
- Do not use network access while implementing or validating transformations.
- Do not modify files under `acceptance/` or `data/expected/`.
- Preserve transaction-level lineage from each output row to its source row.
- Keep outputs deterministic for identical inputs.
- Run unit tests and the protected acceptance suite before producing evidence.
- Record the acceptance-suite hash before and after the implementation.
- Report failures accurately. Do not mark work ready for review without passing validation and an unchanged acceptance-suite hash.
