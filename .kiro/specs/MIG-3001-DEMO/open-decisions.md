# Open decisions: MIG-3001-DEMO revision 1

No answers are invented here. Each item needs a business or data owner.

| ID | Question | Why it is open | Needed from |
|----|----------|----------------|-------------|
| OD-1 | How are `entity`, `maturity_bucket`, and `report_date` obtained? | The source CSV has none of these columns. Mapping source and derivation authority are unknown. Also unknown is whether `report_date` equals `booking_date` or is a separate reporting date. | Business owner / data owner |
| OD-2 | What are the "expected totals"? What is the total basis? | Not defined in the repo. Unclear if signed sum, gross, or per currency. The sample mixes USD and EUR, so a cross-currency sum needs a conversion basis that has not been provided. The 0.01 tolerance applies in the synthetic currency unit. | Business owner |
| OD-3 | Reversal sign semantics and handling of reversals whose original is absent | The briefed intent is economic negation of the referenced transaction. Confirmation is needed, as is the policy for a missing original (reject, quarantine, or pass through). | Business owner |
| OD-4 | Definition of an invalid record and its disposition | "Preserve valid source records" needs a validity definition. Reject, quarantine, or fail-run rules are not specified. | Business / data owner |
| OD-5 | Parquet schema, types, and writer dependency | Target schema owner unknown. Repo is stdlib only and has no Parquet library. | Data owner / platform |
| OD-6 | Conflict between adding R4 columns and the protected expected fixture | `data/expected/liquidity_report_rows.json` has none of the R4 fields and must not be edited. How the contract is extended needs an authorized owner. | Acceptance contract owner |
| OD-7 | Content of "Liquidity report transformation blueprint v1" | Not present in the repository, so it could not be applied. | Blueprint owner |
