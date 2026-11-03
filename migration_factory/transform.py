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


def _signed_amount(
    record_type: str,
    amount: Decimal,
    original_record_type: str | None = None,
) -> Decimal:
    if record_type == "CR":
        return amount
    if record_type == "DR":
        return -amount
    if record_type == "RV":
        if original_record_type == "CR":
            return -amount
        if original_record_type == "DR":
            return amount
        raise ValueError("A reversal must reference a credit or debit transaction")
    raise ValueError(f"Unsupported record_type: {record_type}")


def normalize_liquidity_rows(
    rows: Iterable[Mapping[str, str]],
) -> list[dict[str, str]]:
    """Return deterministic, lineage-preserving logical reporting rows."""

    parsed_rows: list[tuple[int, Mapping[str, str], str, str, Decimal, str]] = []
    record_types: dict[str, str] = {}

    for row_number, row in enumerate(rows, start=2):
        missing = sorted(field for field in _REQUIRED_FIELDS if field not in row)
        if missing:
            raise ValueError(f"Row {row_number} is missing fields: {', '.join(missing)}")

        transaction_id = row["transaction_id"].strip()
        if transaction_id in record_types:
            raise ValueError(f"Row {row_number} repeats transaction_id: {transaction_id}")

        record_type = row["record_type"].strip().upper()
        try:
            amount = Decimal(row["amount"]).quantize(Decimal("0.01"))
        except InvalidOperation as exc:
            raise ValueError(f"Row {row_number} has an invalid amount") from exc

        original_transaction_id = row["original_transaction_id"].strip()
        record_types[transaction_id] = record_type
        parsed_rows.append(
            (
                row_number,
                row,
                transaction_id,
                record_type,
                amount,
                original_transaction_id,
            )
        )

    normalized: list[dict[str, str]] = []
    for (
        row_number,
        row,
        transaction_id,
        record_type,
        amount,
        original_transaction_id,
    ) in parsed_rows:
        original_record_type = record_types.get(original_transaction_id)
        signed_amount = _signed_amount(record_type, amount, original_record_type)

        normalized.append(
            {
                "transaction_id": transaction_id,
                "account_id": row["account_id"].strip(),
                "booking_date": row["booking_date"].strip(),
                "currency": row["currency"].strip().upper(),
                "record_type": record_type,
                "signed_amount": f"{signed_amount:.2f}",
                "original_transaction_id": original_transaction_id,
                "lineage_source": f"liquidity_extract.csv:{row_number}:{transaction_id}",
            }
        )

    return sorted(normalized, key=lambda item: item["transaction_id"])
