"""Local JSON log storage for shift pay estimates."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from shift_pay.calculator import ShiftEstimate


class ShiftLog:
    """Append-only JSON log of shift pay estimates stored on disk."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def _load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        try:
            with self.path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (json.JSONDecodeError, OSError):
            return []
        if not isinstance(data, list):
            return []
        return data

    def append(self, estimate: ShiftEstimate, note: str = "") -> dict[str, Any]:
        record: dict[str, Any] = estimate.as_dict()
        record["recorded_at"] = datetime.now(timezone.utc).isoformat()
        if note:
            record["note"] = note
        records = self._load()
        records.append(record)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(records, handle, indent=2)
            handle.write("\n")
        return record

    def read(self) -> list[dict[str, Any]]:
        return self._load()
