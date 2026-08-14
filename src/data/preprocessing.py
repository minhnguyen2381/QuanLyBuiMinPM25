"""Preprocessing that preserves PM2.5 and relevant exogenous variables."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ColumnMap:
    date_col: str
    target_col: str
    exogenous_cols: list[str]


def _normalize(name: str) -> str:
    return " ".join(str(name).strip().lower().replace("_", " ").split())


def infer_column_map(raw: pd.DataFrame, config: dict) -> ColumnMap:
    """Infer date, target, and exogenous columns from config candidates."""
    normalized = {_normalize(col): col for col in raw.columns}
    date_source = next(
        (normalized[_normalize(c)] for c in config["date_candidates"] if _normalize(c) in normalized),
        None,
    )
    target_source = next(
        (normalized[_normalize(c)] for c in config["target_candidates"] if _normalize(c) in normalized),
        None,
    )
    if date_source is None:
        raise KeyError("Could not infer a datetime column from configured candidates.")
    if target_source is None:
        raise KeyError("Could not infer a PM2.5 target column from configured candidates.")

    exogenous = [
        normalized[_normalize(c)]
        for c in config.get("exogenous_candidates", [])
        if _normalize(c) in normalized and normalized[_normalize(c)] != target_source
    ]
    return ColumnMap(date_col=date_source, target_col=target_source, exogenous_cols=exogenous)


def standardize_columns(raw: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Rename inferred columns to canonical names and coerce numeric values."""
    col_map = infer_column_map(raw, config)
    target_col = config["target_col"]
    date_col = config["date_col"]

    rename_map = {col_map.date_col: date_col, col_map.target_col: target_col}
    rename_map.update({col: col for col in col_map.exogenous_cols})

    df = raw.loc[:, list(rename_map.keys())].rename(columns=rename_map).copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col]).sort_values(date_col)

    for col in [target_col, *col_map.exogenous_cols]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df.loc[df[target_col] < 0, target_col] = np.nan
    return df.drop_duplicates()


def aggregate_daily(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Aggregate hourly observations to daily means with minimum support checks."""
    date_col = config["date_col"]
    target_col = config["target_col"]
    min_obs = int(config.get("min_obs_per_day", 12))
    interpolate_limit = int(config.get("interpolate_limit_days", 7))

    work = df.copy()
    work["_date"] = work[date_col].dt.normalize()
    numeric_cols = [c for c in work.select_dtypes(include="number").columns if c != "_date"]

    grouped = work.groupby("_date")[numeric_cols].mean()
    grouped[f"{target_col}_count"] = work.groupby("_date")[target_col].count()
    grouped = grouped[grouped[f"{target_col}_count"] >= min_obs]
    grouped = grouped.drop(columns=[f"{target_col}_count"])

    full_index = pd.date_range(grouped.index.min(), grouped.index.max(), freq="D")
    daily = grouped.reindex(full_index)
    daily.index.name = date_col

    for col in daily.columns:
        daily[col] = daily[col].interpolate(method="time", limit=interpolate_limit)

    return daily


def preprocess_raw_data(raw: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Run the complete preprocessing stage."""
    return aggregate_daily(standardize_columns(raw, config), config)
