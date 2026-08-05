"""
config.py — Cấu hình đường dẫn và tham số chung cho toàn bộ dự án.
Tất cả module khác import từ đây để đảm bảo nhất quán.
"""

from pathlib import Path

# ─── Gốc dự án ────────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent

# ─── Thư mục dữ liệu ──────────────────────────────────────────────────────────
DATA_DIR       = ROOT_DIR / "data"
RAW_DIR        = DATA_DIR / "raw"
PROCESSED_DIR  = DATA_DIR / "processed"

# ─── Thư mục đầu ra ───────────────────────────────────────────────────────────
FIGURES_DIR    = ROOT_DIR / "figures"
RESULTS_DIR    = ROOT_DIR / "results"

# ─── File dữ liệu chính ───────────────────────────────────────────────────────
CLEAN_DATA_PATH        = PROCESSED_DIR / "clean_data.csv"
ARIMA_PRED_PATH        = RESULTS_DIR   / "arima_predictions.csv"
RF_PRED_PATH           = RESULTS_DIR   / "rf_predictions.csv"
COMPARISON_TABLE_PATH  = RESULTS_DIR   / "model_comparison.csv"

# ─── Kaggle Dataset ───────────────────────────────────────────────────────────
KAGGLE_DATASET = "phungdinhdat/aqi-in-hanoi-2022-2025"

# ─── Cột mục tiêu & cột thời gian ─────────────────────────────────────────────
TARGET_COL  = "PM2.5"
DATE_COL    = "date"          # Tên cột sau khi chuẩn hoá

# ─── Phân chia tập dữ liệu ────────────────────────────────────────────────────
TRAIN_END_YEAR = 2024         # Dữ liệu huấn luyện: 2022–2024
TEST_START_YEAR = 2025        # Dữ liệu kiểm thử:   2025

# ─── Tham số Random Forest ────────────────────────────────────────────────────
RF_PARAMS = {
    "n_estimators": 200,
    "max_depth": 10,
    "min_samples_leaf": 2,
    "random_state": 42,
    "n_jobs": -1,
}

# ─── Độ trễ (lag) và cửa sổ trượt (rolling window) ───────────────────────────
LAG_FEATURES     = [1, 2, 3, 7, 14]
ROLLING_WINDOWS  = [3, 7, 14]

# ─── Tham số biểu đồ ──────────────────────────────────────────────────────────
FIGURE_DPI    = 150
FIGURE_FORMAT = "png"

# Tạo thư mục nếu chưa tồn tại
for _dir in [RAW_DIR, PROCESSED_DIR, FIGURES_DIR, RESULTS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)
