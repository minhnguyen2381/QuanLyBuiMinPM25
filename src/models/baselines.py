"""Baseline forecasts for time-series evaluation."""

from __future__ import annotations

import pandas as pd


def naive_forecast(series: pd.Series) -> pd.Series:
    """Forecast y_t as y_(t-1)."""
    return series.shift(1)


def seasonal_naive_forecast(series: pd.Series, season_length: int = 7) -> pd.Series:
    """Forecast y_t as y_(t-season_length)."""
    return series.shift(season_length)
