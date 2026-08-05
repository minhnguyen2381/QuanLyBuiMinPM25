"""
evaluator.py — Tính toán các chỉ số đánh giá và bảng so sánh mô hình.

Hàm chính:
    compute_metrics()   → Tính MAE, RMSE, R² cho một cặp (actual, predicted)
    compare_models()    → So sánh nhiều mô hình thành một DataFrame
    naive_forecast()    → Tạo dự báo tham chiếu (ŷ_t = y_{t-1})
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.config import COMPARISON_TABLE_PATH

logger = logging.getLogger(__name__)


# ─── 1. Tính chỉ số đánh giá ─────────────────────────────────────────────────

def compute_metrics(
    actual: pd.Series,
    predicted: pd.Series,
    model_name: str = "Model",
) -> dict:
    """
    Tính MAE, RMSE và R² cho một cặp (actual, predicted).

    Args:
        actual:      Chuỗi giá trị thực tế.
        predicted:   Chuỗi giá trị dự báo (cùng chỉ mục).
        model_name:  Tên mô hình để gán vào kết quả.

    Returns:
        Dict chứa {model, MAE, RMSE, R2}.
    """
    # Căn chỉnh index và loại NaN
    aligned = pd.DataFrame({"actual": actual, "predicted": predicted}).dropna()
    if aligned.empty:
        raise ValueError("Không có dữ liệu để đánh giá sau khi loại NaN.")

    y_true = aligned["actual"].values
    y_pred = aligned["predicted"].values

    mae  = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2   = r2_score(y_true, y_pred)

    metrics = {
        "Mô hình": model_name,
        "MAE":     round(mae, 4),
        "RMSE":    round(rmse, 4),
        "R²":      round(r2, 4),
    }
    logger.info(f"[{model_name}] MAE={mae:.4f} | RMSE={rmse:.4f} | R²={r2:.4f}")
    return metrics


# ─── 2. Dự báo tham chiếu (Naïve Baseline) ───────────────────────────────────

def naive_forecast(series: pd.Series) -> pd.Series:
    """
    Tạo dự báo ngây thơ: ŷ_t = y_{t-1}.
    Dùng để làm mốc so sánh tối thiểu cho ARIMA và Random Forest.

    Args:
        series: Chuỗi PM2.5 với DatetimeIndex (thường là tập kiểm thử).

    Returns:
        Chuỗi dự báo cùng chỉ mục (giá trị đầu sẽ là NaN).
    """
    return series.shift(1)


# ─── 3. Bảng so sánh nhiều mô hình ──────────────────────────────────────────

def compare_models(
    actual: pd.Series,
    predictions: dict[str, pd.Series],
    save: bool = True,
    path: Path = COMPARISON_TABLE_PATH,
) -> pd.DataFrame:
    """
    So sánh nhiều mô hình trên cùng tập kiểm thử.

    Args:
        actual:      Chuỗi giá trị thực tế.
        predictions: Dict {tên_mô_hình: chuỗi_dự_báo}.
        save:        Lưu bảng so sánh ra CSV nếu True.
        path:        Đường dẫn lưu file.

    Returns:
        DataFrame bảng so sánh với cột MAE, RMSE, R².
    """
    rows = []
    for name, pred in predictions.items():
        rows.append(compute_metrics(actual, pred, model_name=name))

    result = pd.DataFrame(rows).set_index("Mô hình")

    # Tính phần trăm cải thiện RMSE so với Dự báo tham chiếu
    if "Dự báo tham chiếu" in result.index:
        baseline_rmse = result.loc["Dự báo tham chiếu", "RMSE"]
        result["Cải thiện RMSE (%)"] = (
            (baseline_rmse - result["RMSE"]) / baseline_rmse * 100
        ).round(2)

    if save:
        path.parent.mkdir(parents=True, exist_ok=True)
        result.to_csv(path)
        logger.info(f"Đã lưu bảng so sánh tại: {path}")

    return result


# ─── 4. Phân tích sai số chi tiết ────────────────────────────────────────────

def error_analysis(
    actual: pd.Series,
    predicted: pd.Series,
    model_name: str = "Model",
    top_n: int = 10,
) -> pd.DataFrame:
    """
    Trả về DataFrame phân tích sai số: giá trị thực, dự báo, sai số tuyệt đối
    và % sai số, sắp xếp theo sai số tuyệt đối giảm dần.

    Args:
        actual:      Chuỗi giá trị thực tế.
        predicted:   Chuỗi giá trị dự báo.
        model_name:  Tên mô hình.
        top_n:       Số hàng lỗi lớn nhất trả về.

    Returns:
        DataFrame top_n ngày có sai số lớn nhất.
    """
    df_err = pd.DataFrame({
        "Thực tế":     actual,
        "Dự báo":      predicted,
    }).dropna()
    df_err["Sai số tuyệt đối"]   = (df_err["Thực tế"] - df_err["Dự báo"]).abs()
    df_err["Sai số tương đối (%)"] = (
        df_err["Sai số tuyệt đối"] / df_err["Thực tế"] * 100
    ).round(2)

    logger.info(f"[{model_name}] Top {top_n} ngày sai số lớn nhất:")
    top = df_err.nlargest(top_n, "Sai số tuyệt đối")
    logger.info(top.to_string())
    return top
