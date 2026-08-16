"""Các hàm hỗ trợ mô hình ARIMA cho dự báo PM2.5 đơn biến.

ARIMA dùng chính lịch sử PM2.5 để dự báo tương lai. Module này kiểm tra tính
dừng, chọn bộ tham số `(p, d, q)`, rồi dự báo cuốn chiếu từng ngày trên tập test.
"""

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
    """Chạy kiểm định Augmented Dickey-Fuller để xem chuỗi có tính dừng không.

    Với người mới: p-value nhỏ hơn `significance` thường được hiểu là có đủ bằng
    chứng để xem chuỗi đã dừng. Kết quả này giúp giải thích vì sao ARIMA cần
    tham số sai phân `d`.
    """
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
    """Thử nhiều bộ `(p, d, q)` và chọn bộ có tiêu chí AIC/BIC tốt nhất.

    Hàm chỉ dùng chuỗi huấn luyện để tránh rò rỉ dữ liệu kiểm thử. Mỗi cấu hình
    được lưu vào bảng kết quả; nếu một cấu hình fit lỗi, lỗi được ghi lại thay
    vì làm dừng toàn bộ quá trình tìm kiếm.
    """
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
    """Dự báo ARIMA kiểu cuốn chiếu từng bước một ngày.

    Mỗi vòng lặp fit ARIMA trên lịch sử hiện có, dự báo ngày kế tiếp, rồi thêm
    giá trị thực tế của ngày đó vào lịch sử. Cách này mô phỏng tình huống thực
    tế: sau mỗi ngày, ta biết thêm dữ liệu thật và có thể cập nhật mô hình.
    """
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
