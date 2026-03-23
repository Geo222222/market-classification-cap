"""CSV storage helpers for collected live data."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def append_rows_csv(path: str | Path, fieldnames: list[str], rows: Iterable[dict]) -> int:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    rows_list = list(rows)
    if not rows_list:
        return 0

    exists = p.exists()
    with p.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerows(rows_list)
    return len(rows_list)


def last_numeric_value(path: str | Path, column: str) -> int | None:
    """Return last numeric value in a CSV column without loading full file into memory."""
    p = Path(path)
    if not p.exists():
        return None

    last_val = None
    try:
        with p.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                raw = row.get(column)
                if raw is None or raw == "":
                    continue
                try:
                    last_val = int(float(raw))
                except Exception:
                    continue
        return last_val
    except Exception:
        return None
