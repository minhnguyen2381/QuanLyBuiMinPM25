"""Sinh các biểu đồ tiếng Việt cho pipeline nghiên cứu PM2.5."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


VIETNAMESE_LABELS = {
    "Naive": "Mô hình tham chiếu (Naive)",
    "SeasonalNaive7": "Tham chiếu mùa vụ 7 ngày",
    "ARIMA": "ARIMA",
    "Random Forest": "Random Forest",
}


def _save(fig: plt.Figure, output_path: str | Path) -> Path:
    """Lưu biểu đồ ra file và đóng figure để tránh tốn bộ nhớ."""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return out


def plot_forecast_comparison(actual: pd.Series, predictions: dict[str, pd.Series], output_path: str | Path) -> Path:
    """Vẽ đường PM2.5 thực tế cùng dự báo của các mô hình trên cùng trục thời gian."""
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(actual.index, actual.values, label="Thực tế", color="#222222", linewidth=1.3)
    for name, pred in predictions.items():
        ax.plot(pred.index, pred.values, label=VIETNAMESE_LABELS.get(name, name), linewidth=1.0, alpha=0.85)
    ax.set_title("So sánh nồng độ PM2.5 thực tế và dự báo")
    ax.set_xlabel("Thời gian")
    ax.set_ylabel("PM2.5 (µg/m³)")
    ax.legend()
    fig.tight_layout()
    return _save(fig, output_path)


def plot_pm25_time_series(clean: pd.DataFrame, target_col: str, output_path: str | Path) -> Path:
    """Vẽ diễn biến PM2.5 toàn giai đoạn để thấy xu hướng và các đợt tăng cao."""
    fig, ax = plt.subplots(figsize=(14, 4.8))
    ax.plot(clean.index, clean[target_col], color="#2563eb", linewidth=0.9)
    ax.axhline(clean[target_col].mean(), color="#dc2626", linestyle="--", linewidth=1.0, label="Trung bình toàn kỳ")
    ax.set_title("Diễn biến nồng độ bụi mịn PM2.5 tại Hà Nội")
    ax.set_xlabel("Thời gian")
    ax.set_ylabel("PM2.5 (µg/m³)")
    ax.legend()
    fig.tight_layout()
    return _save(fig, output_path)


def plot_pm25_distribution(clean: pd.DataFrame, target_col: str, output_path: str | Path) -> Path:
    """Vẽ histogram/KDE để nhận diện phân phối, độ lệch và các mức PM2.5 phổ biến."""
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.histplot(clean[target_col].dropna(), bins=45, kde=True, color="#16a34a", ax=ax)
    ax.axvline(clean[target_col].mean(), color="#dc2626", linestyle="--", label=f"Trung bình: {clean[target_col].mean():.2f}")
    ax.axvline(clean[target_col].median(), color="#f59e0b", linestyle="--", label=f"Trung vị: {clean[target_col].median():.2f}")
    ax.set_title("Phân phối nồng độ PM2.5 sau tiền xử lý")
    ax.set_xlabel("PM2.5 (µg/m³)")
    ax.set_ylabel("Số ngày")
    ax.legend()
    fig.tight_layout()
    return _save(fig, output_path)


def plot_monthly_boxplot(clean: pd.DataFrame, target_col: str, output_path: str | Path) -> Path:
    """Vẽ boxplot theo tháng để so sánh trung vị, độ phân tán và ngoại lệ mùa vụ."""
    data = clean[[target_col]].copy()
    data["Tháng"] = data.index.month
    fig, ax = plt.subplots(figsize=(11, 5))
    sns.boxplot(data=data, x="Tháng", y=target_col, color="#93c5fd", ax=ax)
    ax.set_title("Phân bố PM2.5 theo tháng")
    ax.set_xlabel("Tháng")
    ax.set_ylabel("PM2.5 (µg/m³)")
    fig.tight_layout()
    return _save(fig, output_path)


def plot_monthly_mean_by_year(clean: pd.DataFrame, target_col: str, output_path: str | Path) -> Path:
    """Vẽ PM2.5 trung bình từng tháng cho từng năm để so sánh biến động theo mùa."""
    data = clean[[target_col]].copy()
    data["Năm"] = data.index.year
    data["Tháng"] = data.index.month
    monthly = data.groupby(["Năm", "Tháng"], as_index=False)[target_col].mean()
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=monthly, x="Tháng", y=target_col, hue="Năm", marker="o", ax=ax)
    ax.set_title("PM2.5 trung bình theo tháng qua các năm")
    ax.set_xlabel("Tháng")
    ax.set_ylabel("PM2.5 trung bình (µg/m³)")
    ax.set_xticks(range(1, 13))
    fig.tight_layout()
    return _save(fig, output_path)


def plot_correlation_heatmap(clean: pd.DataFrame, output_path: str | Path) -> Path:
    """Vẽ heatmap tương quan để nhìn nhanh quan hệ tuyến tính giữa các biến."""
    corr = clean.select_dtypes(include="number").corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(11, 8))
    sns.heatmap(corr, cmap="vlag", center=0, linewidths=0.4, annot=False, ax=ax)
    ax.set_title("Ma trận tương quan giữa các biến quan trắc")
    fig.tight_layout()
    return _save(fig, output_path)


def plot_feature_importance(importances: pd.Series, output_path: str | Path, top_n: int = 20) -> Path:
    """Vẽ top đặc trưng quan trọng nhất theo Random Forest."""
    top = importances.sort_values(ascending=True).tail(top_n)
    fig, ax = plt.subplots(figsize=(10, max(5, top_n * 0.3)))
    top.plot(kind="barh", color="#f97316", ax=ax)
    ax.set_title(f"Top {top_n} đặc trưng quan trọng nhất của Random Forest")
    ax.set_xlabel("Mức độ quan trọng")
    ax.set_ylabel("Đặc trưng")
    fig.tight_layout()
    return _save(fig, output_path)


def plot_monthly_rmse(actual: pd.Series, predictions: dict[str, pd.Series], output_path: str | Path) -> Path:
    """Vẽ RMSE theo tháng để xem mô hình sai nhiều vào giai đoạn nào."""
    rows = []
    for name, pred in predictions.items():
        aligned = pd.DataFrame({"actual": actual, "predicted": pred}).dropna()
        aligned["month"] = aligned.index.month
        aligned["squared_error"] = (aligned["actual"] - aligned["predicted"]) ** 2
        monthly = aligned.groupby("month")["squared_error"].mean().apply(np.sqrt)
        for month, rmse in monthly.items():
            rows.append({"Tháng": month, "Mô hình": VIETNAMESE_LABELS.get(name, name), "RMSE": rmse})
    data = pd.DataFrame(rows)

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(data=data, x="Tháng", y="RMSE", hue="Mô hình", ax=ax)
    ax.set_title("Sai số RMSE theo tháng của các mô hình")
    ax.set_xlabel("Tháng")
    ax.set_ylabel("RMSE (µg/m³)")
    fig.tight_layout()
    return _save(fig, output_path)


def plot_error_distribution(actual: pd.Series, predictions: dict[str, pd.Series], output_path: str | Path) -> Path:
    """Vẽ phân phối sai số dự báo để biết mô hình hay dự báo cao/thấp ra sao."""
    rows = []
    for name, pred in predictions.items():
        aligned = pd.DataFrame({"actual": actual, "predicted": pred}).dropna()
        errors = aligned["predicted"] - aligned["actual"]
        rows.extend({"Mô hình": VIETNAMESE_LABELS.get(name, name), "Sai số": value} for value in errors)
    data = pd.DataFrame(rows)

    fig, ax = plt.subplots(figsize=(11, 5))
    sns.kdeplot(data=data, x="Sai số", hue="Mô hình", fill=False, common_norm=False, ax=ax)
    ax.axvline(0, color="#111827", linestyle="--", linewidth=1)
    ax.set_title("Phân phối sai số dự báo")
    ax.set_xlabel("Sai số dự báo (dự báo - thực tế)")
    ax.set_ylabel("Mật độ")
    fig.tight_layout()
    return _save(fig, output_path)


def plot_actual_vs_predicted(actual: pd.Series, predictions: dict[str, pd.Series], output_path: str | Path) -> Path:
    """Vẽ scatter thực tế - dự báo; điểm càng gần đường chéo thì dự báo càng tốt."""
    rows = []
    for name, pred in predictions.items():
        aligned = pd.DataFrame({"Thực tế": actual, "Dự báo": pred}).dropna()
        aligned["Mô hình"] = VIETNAMESE_LABELS.get(name, name)
        rows.append(aligned)
    data = pd.concat(rows, ignore_index=True)

    fig, ax = plt.subplots(figsize=(8, 7))
    sns.scatterplot(data=data, x="Thực tế", y="Dự báo", hue="Mô hình", alpha=0.65, ax=ax)
    low = min(data["Thực tế"].min(), data["Dự báo"].min())
    high = max(data["Thực tế"].max(), data["Dự báo"].max())
    ax.plot([low, high], [low, high], color="#111827", linestyle="--", linewidth=1)
    ax.set_title("Quan hệ giữa PM2.5 thực tế và dự báo")
    ax.set_xlabel("PM2.5 thực tế (µg/m³)")
    ax.set_ylabel("PM2.5 dự báo (µg/m³)")
    fig.tight_layout()
    return _save(fig, output_path)
