"""
visualizer.py — Các hàm vẽ biểu đồ chuyên dụng cho phân tích PM2.5.

Mỗi hàm trả về đối tượng matplotlib Figure để notebook có thể hiển thị
và lưu ảnh theo chuẩn bài báo cáo.
"""

import logging
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from src.config import TARGET_COL, FIGURES_DIR, FIGURE_DPI, FIGURE_FORMAT

logger = logging.getLogger(__name__)

# ─── Cài đặt style mặc định ───────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "figure.dpi": FIGURE_DPI,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})

_SEASON_LABELS = {1: "Xuân", 2: "Hè", 3: "Thu", 4: "Đông"}


def _save(fig: plt.Figure, filename: str, dest: Path = FIGURES_DIR) -> None:
    """Lưu figure vào thư mục figures/."""
    dest.mkdir(parents=True, exist_ok=True)
    out = dest / f"{filename}.{FIGURE_FORMAT}"
    fig.savefig(out, dpi=FIGURE_DPI, bbox_inches="tight")
    logger.info(f"Đã lưu biểu đồ: {out}")


# ─── 1. Chuỗi thời gian toàn bộ ──────────────────────────────────────────────

def plot_time_series(df: pd.DataFrame, title: str = "PM2.5 theo thời gian (2022–2025)",
                     save: bool = True) -> plt.Figure:
    """Vẽ biểu đồ đường PM2.5 theo ngày toàn bộ giai đoạn."""
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.plot(df.index, df[TARGET_COL], linewidth=0.8, color="#2196F3", alpha=0.85)
    ax.set_title(title)
    ax.set_xlabel("Thời gian")
    ax.set_ylabel("PM2.5 (μg/m³)")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))
    plt.xticks(rotation=30)
    plt.tight_layout()
    if save:
        _save(fig, "01_time_series")
    return fig


# ─── 2. Histogram phân bố ────────────────────────────────────────────────────

def plot_histogram(df: pd.DataFrame, bins: int = 50, save: bool = True) -> plt.Figure:
    """Vẽ histogram phân bố PM2.5 kèm đường KDE."""
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df[TARGET_COL].dropna(), bins=bins, kde=True, ax=ax, color="#4CAF50")
    ax.axvline(df[TARGET_COL].mean(), color="red", linestyle="--", label=f"Trung bình: {df[TARGET_COL].mean():.1f}")
    ax.axvline(df[TARGET_COL].median(), color="orange", linestyle="--", label=f"Trung vị: {df[TARGET_COL].median():.1f}")
    ax.set_title("Phân bố nồng độ PM2.5")
    ax.set_xlabel("PM2.5 (μg/m³)")
    ax.set_ylabel("Tần suất")
    ax.legend()
    plt.tight_layout()
    if save:
        _save(fig, "02_histogram")
    return fig


# ─── 3. Boxplot theo tháng ────────────────────────────────────────────────────

def plot_boxplot_monthly(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """Vẽ boxplot PM2.5 theo từng tháng trong năm."""
    data = df.copy()
    data["month"] = data.index.month
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.boxplot(data=data, x="month", y=TARGET_COL, ax=ax, palette="coolwarm")
    ax.set_title("Phân bố PM2.5 theo tháng")
    ax.set_xlabel("Tháng")
    ax.set_ylabel("PM2.5 (μg/m³)")
    ax.set_xticklabels([f"T{m}" for m in range(1, 13)])
    plt.tight_layout()
    if save:
        _save(fig, "03_boxplot_monthly")
    return fig


# ─── 4. Trung bình theo tháng ─────────────────────────────────────────────────

def plot_monthly_mean(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """Vẽ biểu đồ cột PM2.5 trung bình theo tháng, phân theo năm."""
    data = df.copy()
    data["year"]  = data.index.year
    data["month"] = data.index.month
    monthly = data.groupby(["year", "month"])[TARGET_COL].mean().reset_index()

    fig, ax = plt.subplots(figsize=(13, 5))
    years = sorted(monthly["year"].unique())
    bar_width = 0.8 / len(years)
    offsets = np.linspace(-0.4 + bar_width / 2, 0.4 - bar_width / 2, len(years))

    for i, year in enumerate(years):
        subset = monthly[monthly["year"] == year]
        ax.bar(subset["month"] + offsets[i], subset[TARGET_COL],
               width=bar_width, label=str(year), alpha=0.85)

    ax.set_title("PM2.5 trung bình theo tháng và năm")
    ax.set_xlabel("Tháng")
    ax.set_ylabel("PM2.5 trung bình (μg/m³)")
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels([f"T{m}" for m in range(1, 13)])
    ax.legend(title="Năm")
    plt.tight_layout()
    if save:
        _save(fig, "04_monthly_mean_by_year")
    return fig


# ─── 5. ACF và PACF ──────────────────────────────────────────────────────────

def plot_acf_pacf(series: pd.Series, lags: int = 40, save: bool = True) -> plt.Figure:
    """Vẽ đồ thị ACF và PACF để xác định tham số p, q cho ARIMA."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 4))
    plot_acf(series.dropna(), lags=lags, ax=axes[0], title="ACF — Hàm tự tương quan")
    plot_pacf(series.dropna(), lags=lags, ax=axes[1], title="PACF — Hàm tự tương quan riêng")
    axes[0].set_xlabel("Độ trễ (ngày)")
    axes[1].set_xlabel("Độ trễ (ngày)")
    plt.tight_layout()
    if save:
        _save(fig, "05_acf_pacf")
    return fig


# ─── 6. So sánh dự báo vs. thực tế ───────────────────────────────────────────

def plot_forecast_vs_actual(
    actual: pd.Series,
    preds: dict[str, pd.Series],
    title: str = "Dự báo vs. Thực tế",
    save: bool = True,
    filename: str = "06_forecast_vs_actual",
) -> plt.Figure:
    """
    Vẽ đồ thị so sánh giá trị thực tế và các dự báo.

    Args:
        actual: Chuỗi giá trị thực tế.
        preds:  Dict {tên_mô_hình: chuỗi_dự_báo}.
    """
    COLORS = {"Thực tế": "#333333", "ARIMA": "#E91E63", "Random Forest": "#2196F3", "Tham chiếu": "#9E9E9E"}
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(actual.index, actual.values, label="Thực tế", color=COLORS["Thực tế"], linewidth=1.2)
    for name, pred in preds.items():
        color = COLORS.get(name, None)
        ax.plot(pred.index, pred.values, label=name, color=color, linewidth=1, alpha=0.85, linestyle="--")
    ax.set_title(title)
    ax.set_xlabel("Thời gian")
    ax.set_ylabel("PM2.5 (μg/m³)")
    ax.legend()
    plt.tight_layout()
    if save:
        _save(fig, filename)
    return fig


# ─── 7. Mức độ quan trọng của đặc trưng (Random Forest) ──────────────────────

def plot_feature_importance(
    importances: pd.Series,
    top_n: int = 15,
    save: bool = True,
) -> plt.Figure:
    """Vẽ biểu đồ cột ngang mức độ quan trọng của đặc trưng."""
    top = importances.sort_values(ascending=True).tail(top_n)
    fig, ax = plt.subplots(figsize=(8, max(4, top_n // 2)))
    top.plot(kind="barh", ax=ax, color="#FF9800")
    ax.set_title(f"Top {top_n} đặc trưng quan trọng nhất (Random Forest)")
    ax.set_xlabel("Mức độ quan trọng")
    plt.tight_layout()
    if save:
        _save(fig, "09_feature_importance")
    return fig


# ─── 8. Sai số theo tháng ─────────────────────────────────────────────────────

def plot_monthly_error(
    actual: pd.Series,
    predicted: pd.Series,
    model_name: str = "Mô hình",
    save: bool = True,
    filename: str = "10_monthly_error",
) -> plt.Figure:
    """Vẽ RMSE theo từng tháng trong tập kiểm thử."""
    err = pd.DataFrame({"actual": actual, "pred": predicted})
    err["month"] = err.index.month
    err["sq_err"] = (err["actual"] - err["pred"]) ** 2
    monthly_rmse = err.groupby("month")["sq_err"].mean().apply(np.sqrt)

    fig, ax = plt.subplots(figsize=(10, 4))
    monthly_rmse.plot(kind="bar", ax=ax, color="#9C27B0", alpha=0.85)
    ax.set_title(f"RMSE theo tháng — {model_name} (2025)")
    ax.set_xlabel("Tháng")
    ax.set_ylabel("RMSE (μg/m³)")
    ax.set_xticklabels([f"T{m}" for m in monthly_rmse.index], rotation=0)
    plt.tight_layout()
    if save:
        _save(fig, filename)
    return fig
