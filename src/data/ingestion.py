"""Raw CSV ingestion for the Hanoi PM2.5 project."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def list_csv_files(raw_dir: str | Path) -> list[Path]:
    """Return CSV files from the raw data directory."""
    files = sorted(Path(raw_dir).glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {raw_dir}")
    return files


def load_raw_data(raw_dir: str | Path) -> pd.DataFrame:
    """Load and concatenate all raw CSV files."""
    frames = []
    for csv_path in list_csv_files(raw_dir):
        frame = pd.read_csv(csv_path, low_memory=False)
        frame["source_file"] = csv_path.name
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)
