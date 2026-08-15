"""Data quality summaries for repeatable research reporting."""

from __future__ import annotations

import pandas as pd


def build_quality_report(raw: pd.DataFrame, clean: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Create a compact before/after quality report."""
    target = config["target_col"]
    rows = [
        ("raw_rows", len(raw), None),
        ("clean_daily_rows", None, len(clean)),
        ("clean_start_date", None, clean.index.min().date().isoformat()),
        ("clean_end_date", None, clean.index.max().date().isoformat()),
        ("clean_columns", None, ", ".join(clean.columns)),
        ("target_missing_after", None, int(clean[target].isna().sum())),
        ("duplicate_raw_rows", int(raw.duplicated().sum()), None),
    ]
    raw_target_candidates = [
        col for col in raw.columns if str(col).strip().lower().replace("_", "") in {"pm25", "pm2.5"}
    ]
    if raw_target_candidates:
        raw_target = raw_target_candidates[0]
        numeric_target = pd.to_numeric(raw[raw_target], errors="coerce")
        rows.append(("target_missing_before", int(numeric_target.isna().sum()), None))
        rows.append(("target_negative_before", int((numeric_target < 0).sum()), None))
    return pd.DataFrame(rows, columns=["indicator", "before", "after"])
