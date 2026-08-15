"""Residual diagnostics for statistical models."""

from __future__ import annotations

import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox


def ljung_box_report(residuals: pd.Series, lags: int = 10) -> pd.DataFrame:
    """Run Ljung-Box autocorrelation diagnostics."""
    return acorr_ljungbox(residuals.dropna(), lags=lags, return_df=True)
