"""Feature engineering for time-series supervised learning."""

from __future__ import annotations

import numpy as np
import pandas as pd


def month_to_season(month: int) -> int:
    """Map month to Hanoi seasons encoded as 1..4."""
    if month in (3, 4, 5):
        return 1
    if month in (6, 7, 8):
        return 2
    if month in (9, 10, 11):
        return 3
    return 4


def create_supervised_features(clean: pd.DataFrame, config: dict) -> tuple[pd.DataFrame, pd.Series, list[str]]:
    """Create lag, rolling, calendar, and optional exogenous features."""
    target = config["target_col"]
    rf_cfg = config["random_forest"]
    y = clean[target]
    features = pd.DataFrame(index=clean.index)

    for lag in rf_cfg.get("lags", []):
        features[f"pm25_lag_{lag}"] = y.shift(lag)

    for window in rf_cfg.get("rolling_windows", []):
        shifted = y.shift(1)
        features[f"pm25_roll_mean_{window}"] = shifted.rolling(window).mean()
        features[f"pm25_roll_std_{window}"] = shifted.rolling(window).std()

    if rf_cfg.get("add_diff_features", True):
        features["pm25_diff_1"] = y.diff(1).shift(1)
        features["pm25_diff_7"] = y.diff(7).shift(1)

    if rf_cfg.get("add_calendar_features", True):
        features["day_of_week"] = clean.index.dayofweek
        features["month"] = clean.index.month
        features["quarter"] = clean.index.quarter
        features["season"] = [month_to_season(m) for m in clean.index.month]
        features["year"] = clean.index.year
        features["is_weekend"] = (clean.index.dayofweek >= 5).astype(int)

    if rf_cfg.get("add_cyclic_features", True):
        features["month_sin"] = np.sin(2 * np.pi * clean.index.month / 12)
        features["month_cos"] = np.cos(2 * np.pi * clean.index.month / 12)
        features["dow_sin"] = np.sin(2 * np.pi * clean.index.dayofweek / 7)
        features["dow_cos"] = np.cos(2 * np.pi * clean.index.dayofweek / 7)

    if rf_cfg.get("include_exogenous", True):
        for col in clean.columns:
            if col != target:
                features[f"{col}_lag_1"] = clean[col].shift(1)
                features[f"{col}_roll_mean_7"] = clean[col].shift(1).rolling(7).mean()

    supervised = pd.concat([features, y.rename(target)], axis=1).dropna()
    feature_cols = [col for col in supervised.columns if col != target]
    return supervised, supervised[target], feature_cols
