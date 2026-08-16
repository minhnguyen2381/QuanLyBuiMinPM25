"""Các mô hình tham chiếu đơn giản để so sánh với ARIMA và Random Forest."""

from __future__ import annotations

import pandas as pd


def naive_forecast(series: pd.Series) -> pd.Series:
    """Dự báo hôm nay bằng giá trị của ngày ngay trước đó.

    Đây là mốc tham chiếu rất cơ bản. Mô hình chính chỉ thật sự có ích nếu tốt
    hơn cách "lấy hôm qua dự báo hôm nay" này.
    """
    return series.shift(1)


def seasonal_naive_forecast(series: pd.Series, season_length: int = 7) -> pd.Series:
    """Dự báo hôm nay bằng giá trị cách đây `season_length` ngày.

    Với mặc định 7 ngày, hàm dùng giá trị cùng thứ trong tuần trước, giúp kiểm
    tra mô hình chính có vượt qua được một mốc mùa vụ đơn giản hay không.
    """
    return series.shift(season_length)
