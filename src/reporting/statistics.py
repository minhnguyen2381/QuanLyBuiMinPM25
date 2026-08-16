"""Tạo các bảng thống kê mô tả để đưa vào báo cáo tiếng Việt."""

from __future__ import annotations

import numpy as np
import pandas as pd


SEASON_LABELS = {
    1: "Xuân (tháng 3-5)",
    2: "Hè (tháng 6-8)",
    3: "Thu (tháng 9-11)",
    4: "Đông (tháng 12-2)",
}


def month_to_season(month: int) -> int:
    """Đổi tháng thành mã mùa dùng chung trong các bảng thống kê."""
    if month in (3, 4, 5):
        return 1
    if month in (6, 7, 8):
        return 2
    if month in (9, 10, 11):
        return 3
    return 4


def descriptive_statistics(clean: pd.DataFrame) -> pd.DataFrame:
    """Tạo thống kê mô tả cho các biến số sau tiền xử lý.

    Bảng gồm số quan sát, trung bình, trung vị, độ lệch chuẩn, min/max, tứ phân
    vị, IQR, skewness và kurtosis. Những chỉ số này giúp nhận diện độ phân tán
    và mức lệch của dữ liệu PM2.5.
    """
    numeric = clean.select_dtypes(include="number")
    stats = numeric.agg(["count", "mean", "median", "std", "min", "max"]).T
    stats["q25"] = numeric.quantile(0.25)
    stats["q75"] = numeric.quantile(0.75)
    stats["iqr"] = stats["q75"] - stats["q25"]
    stats["skewness"] = numeric.skew()
    stats["kurtosis"] = numeric.kurtosis()
    return stats.round(4)


def temporal_statistics(clean: pd.DataFrame, target_col: str) -> dict[str, pd.DataFrame]:
    """Tổng hợp PM2.5 theo tháng, mùa, năm và cặp năm-tháng.

    Các bảng này giúp nhìn rõ tính mùa vụ: tháng/mùa nào PM2.5 cao hơn, năm nào
    có xu hướng khác biệt, và tập kiểm thử có đặc điểm ra sao.
    """
    work = clean[[target_col]].copy()
    work["month"] = work.index.month
    work["year"] = work.index.year
    work["season_code"] = [month_to_season(month) for month in work["month"]]
    work["season"] = work["season_code"].map(SEASON_LABELS)

    aggregations = {
        "Số ngày": (target_col, "count"),
        "Trung bình": (target_col, "mean"),
        "Trung vị": (target_col, "median"),
        "Độ lệch chuẩn": (target_col, "std"),
        "Nhỏ nhất": (target_col, "min"),
        "Lớn nhất": (target_col, "max"),
    }

    monthly = work.groupby("month").agg(**aggregations).round(4)
    seasonal = work.groupby(["season_code", "season"]).agg(**aggregations).round(4).reset_index(level=0, drop=True)
    yearly = work.groupby("year").agg(**aggregations).round(4)
    month_year = work.groupby(["year", "month"]).agg(**aggregations).round(4)

    return {
        "monthly": monthly,
        "seasonal": seasonal,
        "yearly": yearly,
        "month_year": month_year,
    }


def pm25_correlation_table(clean: pd.DataFrame, target_col: str) -> pd.DataFrame:
    """Tính tương quan giữa PM2.5 và từng biến ngoại sinh.

    Kết quả được sắp xếp theo độ lớn tuyệt đối để các biến liên quan mạnh nhất
    xuất hiện trước. Tương quan chỉ mô tả quan hệ tuyến tính, không chứng minh
    nguyên nhân - kết quả.
    """
    numeric = clean.select_dtypes(include="number")
    correlations = numeric.corr(numeric_only=True)[target_col].drop(target_col).sort_values(key=lambda s: s.abs(), ascending=False)
    return correlations.rename("Tương quan với PM2.5").to_frame().round(4)


def threshold_summary(clean: pd.DataFrame, target_col: str, thresholds: list[float] | None = None) -> pd.DataFrame:
    """Đếm số ngày PM2.5 vượt từng ngưỡng tham khảo.

    Bảng này dùng để mô tả mức độ xuất hiện của các ngày ô nhiễm cao. Các ngưỡng
    là mốc phân tích trong báo cáo, không thay thế quy chuẩn pháp lý.
    """
    thresholds = thresholds or [15, 25, 50, 75, 100]
    series = clean[target_col].dropna()
    rows = []
    for threshold in thresholds:
        count = int((series > threshold).sum())
        rows.append(
            {
                "Ngưỡng PM2.5": threshold,
                "Số ngày vượt ngưỡng": count,
                "Tỷ lệ (%)": round(count / len(series) * 100, 2),
            }
        )
    return pd.DataFrame(rows)


def forecast_error_detail(actual: pd.Series, predictions: dict[str, pd.Series]) -> pd.DataFrame:
    """Tạo bảng chi tiết dự báo và sai số tuyệt đối theo từng ngày."""
    detail = pd.DataFrame({"Thực tế": actual})
    for name, pred in predictions.items():
        aligned = pred.reindex(actual.index)
        detail[f"{name} - Dự báo"] = aligned
        detail[f"{name} - Sai số"] = aligned - actual
        detail[f"{name} - Sai số tuyệt đối"] = (aligned - actual).abs()
    return detail.dropna(how="all").round(4)


def missing_data_summary(clean: pd.DataFrame) -> pd.DataFrame:
    """Tóm tắt số lượng và tỷ lệ giá trị thiếu của từng biến sau tiền xử lý."""
    total = len(clean)
    missing = clean.isna().sum()
    return pd.DataFrame(
        {
            "Số giá trị thiếu": missing,
            "Tỷ lệ thiếu (%)": np.where(total == 0, 0, missing / total * 100),
        }
    ).round(4)
