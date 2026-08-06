"""
arima_model.py — Đóng gói toàn bộ quy trình xây dựng mô hình ARIMA
cho dự báo PM2.5: kiểm định ADF, chọn tham số, huấn luyện, dự báo và
kiểm tra phần dư.
"""

import logging
import warnings
from pathlib import Path
from itertools import product

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox

from src.config import TARGET_COL, ARIMA_PRED_PATH, FIGURES_DIR, FIGURE_DPI, FIGURE_FORMAT

logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore", category=UserWarning)


# ─── 1. Kiểm định ADF (tính dừng) ────────────────────────────────────────────

def adf_test(series: pd.Series, significance: float = 0.05) -> dict:
    """
    Kiểm định Augmented Dickey-Fuller.

    H₀: Chuỗi không dừng (có đơn vị gốc).
    H₁: Chuỗi dừng.

    Returns:
        Dict chứa {stat, p_value, critical_values, is_stationary}.
    """
    clean = series.dropna()
    stat, p_value, _, _, critical_values, _ = adfuller(clean)
    is_stationary = p_value < significance

    result = {
        "ADF Statistic":   round(stat, 4),
        "p-value":         round(p_value, 4),
        "Critical Values": {k: round(v, 4) for k, v in critical_values.items()},
        "is_stationary":   is_stationary,
    }
    status = "DỪNG ✓" if is_stationary else "KHÔNG DỪNG — cần sai phân"
    logger.info(f"ADF Test: stat={stat:.4f}, p={p_value:.4f} → {status}")
    return result


# ─── 2. Tự động chọn tham số p, d, q ─────────────────────────────────────────

def select_arima_order(
    series: pd.Series,
    p_range: range = range(0, 4),
    d_range: range = range(0, 2),
    q_range: range = range(0, 4),
    ic: str = "aic",
) -> tuple[int, int, int]:
    """
    Tìm bộ tham số (p, d, q) tốt nhất bằng grid search trên AIC/BIC.
    Chỉ dùng dữ liệu huấn luyện — không sử dụng tập kiểm thử.

    Args:
        series:  Chuỗi huấn luyện.
        p_range: Khoảng giá trị p thử nghiệm.
        d_range: Khoảng giá trị d thử nghiệm.
        q_range: Khoảng giá trị q thử nghiệm.
        ic:      Tiêu chí chọn: 'aic' hoặc 'bic'.

    Returns:
        (p, d, q) tối ưu.
    """
    logger.info(f"Grid search ARIMA(p,d,q) — tiêu chí: {ic.upper()}...")
    best_ic   = np.inf
    best_order = (1, 1, 1)
    clean = series.dropna()

    for p, d, q in product(p_range, d_range, q_range):
        try:
            model = ARIMA(clean, order=(p, d, q))
            fit   = model.fit()
            score = getattr(fit, ic)
            if score < best_ic:
                best_ic    = score
                best_order = (p, d, q)
        except Exception:
            continue

    logger.info(f"Bộ tham số tốt nhất: ARIMA{best_order} — {ic.upper()}={best_ic:.2f}")
    return best_order


# ─── 3. Huấn luyện ARIMA ─────────────────────────────────────────────────────

def train_arima(
    train: pd.Series,
    order: tuple[int, int, int] = (1, 1, 1),
) -> object:
    """
    Huấn luyện mô hình ARIMA trên tập huấn luyện.

    Args:
        train:  Chuỗi huấn luyện.
        order:  Bộ tham số (p, d, q).

    Returns:
        Đối tượng ARIMAResults đã khớp.
    """
    logger.info(f"Huấn luyện ARIMA{order} trên {len(train)} quan sát...")
    model = ARIMA(train.dropna(), order=order)
    fit   = model.fit()
    logger.info(f"ARIMA{order} — AIC={fit.aic:.2f} | BIC={fit.bic:.2f}")
    return fit


# ─── 4. Dự báo ARIMA (rolling one-step-ahead) ────────────────────────────────

def forecast_arima(
    train: pd.Series,
    test: pd.Series,
    order: tuple[int, int, int],
    save: bool = True,
    path: Path = ARIMA_PRED_PATH,
) -> pd.Series:
    """
    Dự báo rolling one-step-ahead: mỗi ngày dự báo 1 bước tới dùng
    lịch sử thực tế tích luỹ → phù hợp với thực tế cảnh báo.

    Args:
        train:  Chuỗi huấn luyện.
        test:   Chuỗi kiểm thử (giá trị thực tế).
        order:  Bộ tham số (p, d, q).
        save:   Lưu kết quả ra CSV nếu True.
        path:   Đường dẫn file CSV đầu ra.

    Returns:
        pd.Series dự báo với cùng chỉ mục như test.
    """
    history   = list(train.dropna())
    preds_out = []
    logger.info(f"Bắt đầu dự báo rolling ARIMA{order} trên {len(test)} ngày...")

    for i, (date, _) in enumerate(test.items()):
        try:
            model = ARIMA(history, order=order)
            fit   = model.fit()
            # statsmodels trả về Series hoặc ndarray tùy kiểu dữ liệu đầu vào.
            # Dùng NumPy để lấy phần tử đầu tiên an toàn cho cả hai trường hợp.
            yhat = float(np.asarray(fit.forecast(steps=1)).reshape(-1)[0])
        except Exception as e:
            logger.warning(f"Lỗi tại {date}: {e}. Dùng giá trị cuối.")
            yhat = history[-1]

        preds_out.append(yhat)
        history.append(float(test.iloc[i]))  # Cập nhật lịch sử bằng giá trị thực

        if (i + 1) % 30 == 0:
            logger.info(f"  {i+1}/{len(test)} ngày đã dự báo.")

    pred_series = pd.Series(preds_out, index=test.index, name="arima_pred")

    if save:
        path.parent.mkdir(parents=True, exist_ok=True)
        pred_series.to_csv(path, header=True)
        logger.info(f"Kết quả dự báo ARIMA lưu tại: {path}")

    return pred_series


# ─── 5. Kiểm tra phần dư ─────────────────────────────────────────────────────

def check_residuals(fit_result, lags: int = 10, save: bool = True) -> pd.DataFrame:
    """
    Kiểm tra phần dư của mô hình ARIMA đã huấn luyện:
    - Vẽ đồ thị phần dư.
    - Kiểm định Ljung–Box.

    Args:
        fit_result: Đối tượng ARIMAResults.
        lags:       Số lag kiểm định Ljung–Box.
        save:       Lưu hình vào figures/.

    Returns:
        DataFrame kết quả kiểm định Ljung–Box.
    """
    residuals = fit_result.resid

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(residuals, linewidth=0.8, color="#607D8B")
    axes[0].axhline(0, color="red", linestyle="--")
    axes[0].set_title("Phần dư mô hình ARIMA")
    axes[0].set_xlabel("Thời gian")
    axes[0].set_ylabel("Phần dư")

    axes[1].hist(residuals, bins=40, color="#78909C", edgecolor="white")
    axes[1].set_title("Phân bố phần dư")
    axes[1].set_xlabel("Phần dư")

    plt.tight_layout()
    if save:
        out = FIGURES_DIR / f"07_arima_residuals.{FIGURE_FORMAT}"
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        fig.savefig(out, dpi=FIGURE_DPI, bbox_inches="tight")
        logger.info(f"Đã lưu biểu đồ phần dư: {out}")
    plt.show()

    lb_result = acorr_ljungbox(residuals, lags=lags, return_df=True)
    logger.info(f"Kiểm định Ljung–Box (lag 1–{lags}):\n{lb_result.to_string()}")
    return lb_result
