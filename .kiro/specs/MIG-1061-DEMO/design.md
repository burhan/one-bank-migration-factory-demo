# Design: MIG-1061-DEMO

The transformation uses two deterministic passes over the input rows.

The first pass validates required columns, parses each amount as a two-decimal `Decimal`, records the normalized record type for every transaction ID, and retains the original source-row number. Building the transaction map before calculating signs allows a reversal to reference a transaction that appears earlier or later in the extract.

The second pass assigns credit and debit signs directly. For a reversal, it looks up the referenced transaction type and applies the opposite sign while retaining the reversal row's own amount and lineage. Missing or unsupported references fail instead of inventing a business rule.

The output schema and transaction-level `lineage_source` field remain unchanged. Results are sorted by transaction ID so identical inputs produce identical outputs.
