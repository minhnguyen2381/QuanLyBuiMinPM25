"""Detailed forecast error analysis."""

from __future__ import annotations

import numpy as np
import pandas as pd


def top_absolute_errors(actual: pd.Series, predicted: pd.Series, top_n: int = 10) -> pd.DataFrame:
    """Return the largest absolute forecast errors."""
    err = pd.DataFrame({"actual": actual, "predicted": predicted}).dropna()
    err["absolute_error"] = (err["actual"] - err["predicted"]).abs()
    err["percentage_error"] = (err["absolute_error"] / err["actual"].replace(0, np.nan) * 100).round(2)
    return err.sort_values("absolute_error", ascending=False).head(top_n)


def monthly_error_summary(actual: pd.Series, predicted: pd.Series) -> pd.DataFrame:
    """Aggregate forecast error by calendar month."""
    err = pd.DataFrame({"actual": actual, "predicted": predicted}).dropna()
    err["month"] = err.index.month
    err["absolute_error"] = (err["actual"] - err["predicted"]).abs()
    err["squared_error"] = (err["actual"] - err["predicted"]) ** 2
    grouped = err.groupby("month").agg(
        MAE=("absolute_error", "mean"),
        RMSE=("squared_error", lambda x: float(np.sqrt(x.mean()))),
        mean_actual=("actual", "mean"),
        n=("actual", "size"),
    )
    return grouped.round(4)
