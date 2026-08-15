"""ARIMA utilities for selection, fitting, and rolling forecasts."""

from __future__ import annotations

from itertools import product
from typing import Iterable
import warnings

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller


warnings.filterwarnings("ignore", message="Non-stationary starting autoregressive parameters found.*")
warnings.filterwarnings("ignore", message="Non-invertible starting MA parameters found.*")


def adf_test(series: pd.Series, significance: float = 0.05) -> dict:
    """Run Augmented Dickey-Fuller stationarity test."""
    clean = series.dropna()
    stat, p_value, _, _, critical_values, _ = adfuller(clean)
    return {
        "adf_statistic": float(stat),
        "p_value": float(p_value),
        "critical_values": {k: float(v) for k, v in critical_values.items()},
        "is_stationary": bool(p_value < significance),
    }


def select_arima_order(
    series: pd.Series,
    p_values: Iterable[int],
    d_values: Iterable[int],
    q_values: Iterable[int],
    information_criterion: str = "aic",
) -> tuple[tuple[int, int, int], pd.DataFrame]:
    """Grid-search ARIMA order using only the training series."""
    rows = []
    best_score = np.inf
    best_order = (1, 1, 1)
    clean = series.dropna()

    for order in product(p_values, d_values, q_values):
        try:
            fit = ARIMA(clean, order=order).fit()
            score = float(getattr(fit, information_criterion))
            rows.append({"p": order[0], "d": order[1], "q": order[2], information_criterion: score})
            if score < best_score:
                best_score = score
                best_order = order
        except Exception as exc:
            rows.append(
                {"p": order[0], "d": order[1], "q": order[2], information_criterion: np.nan, "error": str(exc)}
            )

    return best_order, pd.DataFrame(rows).sort_values(information_criterion, na_position="last")


def rolling_arima_forecast(train: pd.Series, test: pd.Series, order: tuple[int, int, int]) -> pd.Series:
    """One-step-ahead rolling ARIMA forecast."""
    history = [float(v) for v in train.dropna()]
    predictions = []

    for actual in test:
        try:
            fit = ARIMA(history, order=order).fit()
            yhat = float(np.asarray(fit.forecast(steps=1)).reshape(-1)[0])
        except Exception:
            yhat = history[-1]
        predictions.append(yhat)
        if pd.notna(actual):
            history.append(float(actual))

    return pd.Series(predictions, index=test.index, name="ARIMA")
