"""Kiểm tra phần dư để đánh giá mô hình thống kê sau dự báo."""

from __future__ import annotations

import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox


def ljung_box_report(residuals: pd.Series, lags: int = 10) -> pd.DataFrame:
    """Chạy kiểm định Ljung-Box để xem phần dư còn tự tương quan không.

    Nếu phần dư vẫn còn tự tương quan mạnh, mô hình có thể chưa khai thác hết
    cấu trúc thời gian trong dữ liệu.
    """
    return acorr_ljungbox(residuals.dropna(), lags=lags, return_df=True)
