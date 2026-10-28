"""CSV export for shift pay estimate logs."""

from __future__ import annotations

import csv
from pathlib import Path

FIELDNAMES = [
    "recorded_at",
    "base_rate",
    "hours_worked",
    "holiday_hours",
    "holiday_multiplier",
    "ot_threshold",
    "ot_multiplier",
    "differential_rate",
    "differential_hours",
    "weekly_hours_so_far",
    "holiday_pay",
    "regular_pay",
    "ot_hours",
    "ot_pay",
    "differential_pay",
    "total_pay",
    "note",
]


def export_csv(records: list[dict], path: str | Path) -> None:
    """Write shift estimate records to a CSV file."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            writer.writerow(record)
