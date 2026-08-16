"""Các chỉ số đánh giá dự báo PM2.5.

Module này gom các metric thường dùng như MAE, RMSE, MAPE, SMAPE, R2 và độ
chính xác chiều tăng/giảm. Kết quả được đưa vào bảng so sánh mô hình.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def align_actual_predicted(actual: pd.Series, predicted: pd.Series) -> pd.DataFrame:
    """Căn cùng ngày giữa chuỗi thực tế và chuỗi dự báo, rồi bỏ dòng thiếu.

    Metric chỉ có ý nghĩa khi so sánh đúng cặp ngày. Hàm này tạo bảng gồm
    `actual` và `predicted` để các metric phía dưới dùng chung một cách nhất quán.
    """
    return pd.DataFrame({"actual": actual, "predicted": predicted}).dropna()


def directional_accuracy(actual: pd.Series, predicted: pd.Series) -> float:
    """Tính tỷ lệ dự báo đúng chiều tăng hoặc giảm giữa hai ngày liên tiếp."""
    aligned = align_actual_predicted(actual, predicted)
    if len(aligned) < 2:
        return np.nan
    actual_direction = np.sign(aligned["actual"].diff().dropna())
    pred_direction = np.sign(aligned["predicted"].diff().dropna())
    return float((actual_direction == pred_direction).mean())


def compute_forecast_metrics(actual: pd.Series, predicted: pd.Series, model_name: str) -> dict:
    """Tính bộ chỉ số đánh giá cho một mô hình dự báo.

    MAE/RMSE đo sai số theo đơn vị µg/m³, MAPE/SMAPE đo sai số phần trăm, R2 đo
    mức giải thích biến thiên, còn DirectionalAccuracy kiểm tra mô hình có bắt
    đúng xu hướng tăng/giảm hay không.
    """
    aligned = align_actual_predicted(actual, predicted)
    if aligned.empty:
        raise ValueError(f"No overlapping observations for {model_name}.")

    y_true = aligned["actual"].to_numpy()
    y_pred = aligned["predicted"].to_numpy()
    denominator = np.where(y_true == 0, np.nan, np.abs(y_true))
    mape = np.nanmean(np.abs((y_true - y_pred) / denominator)) * 100
    smape = np.nanmean(2 * np.abs(y_pred - y_true) / (np.abs(y_true) + np.abs(y_pred))) * 100

    return {
        "Model": model_name,
        "MAE": round(float(mean_absolute_error(y_true, y_pred)), 4),
        "RMSE": round(float(np.sqrt(mean_squared_error(y_true, y_pred))), 4),
        "MAPE": round(float(mape), 4),
        "SMAPE": round(float(smape), 4),
        "R2": round(float(r2_score(y_true, y_pred)), 4),
        "DirectionalAccuracy": round(directional_accuracy(actual, predicted), 4),
        "N": int(len(aligned)),
    }


def compare_forecasts(actual: pd.Series, predictions: dict[str, pd.Series]) -> pd.DataFrame:
    """So sánh nhiều mô hình trên cùng chuỗi PM2.5 thực tế.

    Nếu có mô hình `Naive`, hàm thêm cột phần trăm cải thiện RMSE so với mốc
    tham chiếu này để dễ đọc kết quả trong báo cáo.
    """
    table = pd.DataFrame(
        [compute_forecast_metrics(actual, pred, name) for name, pred in predictions.items()]
    ).set_index("Model")
    if "Naive" in table.index:
        baseline_rmse = table.loc["Naive", "RMSE"]
        table["Cải thiện RMSE so với mô hình tham chiếu (%)"] = (
            (baseline_rmse - table["RMSE"]) / baseline_rmse * 100
        ).round(2)
    return table
