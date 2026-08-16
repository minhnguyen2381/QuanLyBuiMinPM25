"""Phân tích chi tiết sai số dự báo sau khi đã có kết quả mô hình."""

from __future__ import annotations

import numpy as np
import pandas as pd


def top_absolute_errors(actual: pd.Series, predicted: pd.Series, top_n: int = 10) -> pd.DataFrame:
    """Lấy các ngày có sai số tuyệt đối lớn nhất.

    Bảng này giúp xem mô hình sai nặng vào những ngày nào, đặc biệt hữu ích khi
    muốn phân tích các đợt ô nhiễm cao hoặc các điểm bất thường.
    """
    err = pd.DataFrame({"actual": actual, "predicted": predicted}).dropna()
    err["absolute_error"] = (err["actual"] - err["predicted"]).abs()
    err["percentage_error"] = (err["absolute_error"] / err["actual"].replace(0, np.nan) * 100).round(2)
    return err.sort_values("absolute_error", ascending=False).head(top_n)


def monthly_error_summary(actual: pd.Series, predicted: pd.Series) -> pd.DataFrame:
    """Tổng hợp MAE/RMSE theo tháng để xem mô hình sai nhiều ở thời đoạn nào."""
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
