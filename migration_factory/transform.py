"""Normalize synthetic liquidity-report rows before Parquet serialization."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Iterable, Mapping

_REQUIRED_FIELDS = {
    "transaction_id",
    "account_id",
    "booking_date",
    "currency",
    "record_type",
    "amount",
    "original_transaction_id",
}


def _signed_amount(record_type: str, amount: Decimal) -> Decimal:
    if record_type == "CR":
        return amount
    if record_type == "DR":
        return -amount
    if record_type == "RV":
        # Deliberate starter gap for MIG-1061-DEMO. A reversal must negate the
        # economic effect of the referenced transaction, not behave as a debit.
        return -amount
    raise ValueError(f"Unsupported record_type: {record_type}")


def normalize_liquidity_rows(
    rows: Iterable[Mapping[str, str]],
) -> list[dict[str, str]]:
    """Return deterministic, lineage-preserving logical reporting rows."""

    normalized: list[dict[str, str]] = []

    for row_number, row in enumerate(rows, start=2):
        missing = sorted(field for field in _REQUIRED_FIELDS if field not in row)
        if missing:
            raise ValueError(f"Row {row_number} is missing fields: {', '.join(missing)}")

        record_type = row["record_type"].strip().upper()
        try:
            amount = Decimal(row["amount"]).quantize(Decimal("0.01"))
        except InvalidOperation as exc:
            raise ValueError(f"Row {row_number} has an invalid amount") from exc

        signed_amount = _signed_amount(record_type, amount)
        transaction_id = row["transaction_id"].strip()

        normalized.append(
            {
                "transaction_id": transaction_id,
                "account_id": row["account_id"].strip(),
                "booking_date": row["booking_date"].strip(),
                "currency": row["currency"].strip().upper(),
                "record_type": record_type,
                "signed_amount": f"{signed_amount:.2f}",
                "original_transaction_id": row["original_transaction_id"].strip(),
                "lineage_source": f"liquidity_extract.csv:{row_number}:{transaction_id}",
            }
        )

    return sorted(normalized, key=lambda item: item["transaction_id"])
