from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path

from migration_factory import normalize_liquidity_rows

_REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class LiquidityReportAcceptanceTest(unittest.TestCase):
    def test_logical_parquet_rows_match_the_approved_contract(self) -> None:
        input_path = _REPOSITORY_ROOT / "data" / "input" / "liquidity_extract.csv"
        expected_path = (
            _REPOSITORY_ROOT / "data" / "expected" / "liquidity_report_rows.json"
        )

        with input_path.open(newline="", encoding="utf-8") as handle:
            source_rows = list(csv.DictReader(handle))
        expected_rows = json.loads(expected_path.read_text(encoding="utf-8"))

        actual_rows = normalize_liquidity_rows(source_rows)

        self.assertEqual(actual_rows, expected_rows)

    def test_every_output_row_preserves_source_lineage(self) -> None:
        input_path = _REPOSITORY_ROOT / "data" / "input" / "liquidity_extract.csv"
        with input_path.open(newline="", encoding="utf-8") as handle:
            source_rows = list(csv.DictReader(handle))

        actual_rows = normalize_liquidity_rows(source_rows)

        self.assertTrue(all(row["lineage_source"] for row in actual_rows))
        self.assertEqual(len(actual_rows), len(source_rows))


if __name__ == "__main__":
    unittest.main()
