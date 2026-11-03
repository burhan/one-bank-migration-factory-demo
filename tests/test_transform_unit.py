from __future__ import annotations

import unittest

from migration_factory import normalize_liquidity_rows


class NormalizeLiquidityRowsUnitTest(unittest.TestCase):
    def test_credit_and_debit_signs_are_normalized(self) -> None:
        rows = [
            {
                "transaction_id": "TXN-2",
                "account_id": "ACC-1",
                "booking_date": "2026-10-30",
                "currency": "usd",
                "record_type": "DR",
                "amount": "25.00",
                "original_transaction_id": "",
            },
            {
                "transaction_id": "TXN-1",
                "account_id": "ACC-1",
                "booking_date": "2026-10-30",
                "currency": "usd",
                "record_type": "CR",
                "amount": "100.00",
                "original_transaction_id": "",
            },
        ]

        result = normalize_liquidity_rows(rows)

        self.assertEqual([row["transaction_id"] for row in result], ["TXN-1", "TXN-2"])
        self.assertEqual(result[0]["signed_amount"], "100.00")
        self.assertEqual(result[1]["signed_amount"], "-25.00")
        self.assertEqual(result[0]["currency"], "USD")

    def test_reversal_negates_the_referenced_transaction_effect(self) -> None:
        rows = [
            {
                "transaction_id": "TXN-2",
                "account_id": "ACC-1",
                "booking_date": "2026-10-31",
                "currency": "USD",
                "record_type": "RV",
                "amount": "25.00",
                "original_transaction_id": "TXN-1",
            },
            {
                "transaction_id": "TXN-1",
                "account_id": "ACC-1",
                "booking_date": "2026-10-30",
                "currency": "USD",
                "record_type": "DR",
                "amount": "25.00",
                "original_transaction_id": "",
            },
        ]

        result = normalize_liquidity_rows(rows)

        self.assertEqual(result[1]["record_type"], "RV")
        self.assertEqual(result[1]["signed_amount"], "25.00")
        self.assertEqual(result[1]["original_transaction_id"], "TXN-1")

    def test_reversal_without_a_credit_or_debit_reference_is_rejected(self) -> None:
        row = {
            "transaction_id": "TXN-3",
            "account_id": "ACC-1",
            "booking_date": "2026-10-31",
            "currency": "USD",
            "record_type": "RV",
            "amount": "25.00",
            "original_transaction_id": "TXN-404",
        }

        with self.assertRaisesRegex(ValueError, "must reference a credit or debit"):
            normalize_liquidity_rows([row])

    def test_unsupported_record_type_is_rejected(self) -> None:
        row = {
            "transaction_id": "TXN-9",
            "account_id": "ACC-9",
            "booking_date": "2026-10-30",
            "currency": "USD",
            "record_type": "XX",
            "amount": "1.00",
            "original_transaction_id": "",
        }

        with self.assertRaisesRegex(ValueError, "Unsupported record_type"):
            normalize_liquidity_rows([row])


if __name__ == "__main__":
    unittest.main()
