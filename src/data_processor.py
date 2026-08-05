"""
data_processor.py — Tiền xử lý và kỹ thuật đặc trưng (feature engineering)
cho dữ liệu PM2.5 chuỗi thời gian.

Quy trình:
    load_raw()           → Đọc và ghép nhiều file CSV thô
    preprocess()         → Làm sạch, nội suy, tổng hợp theo ngày
    create_features()    → Tạo lag, rolling mean/std, đặc trưng thời gian
    split_train_test()   → Chia tập huấn luyện / kiểm thử theo năm
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import (
    RAW_DIR, CLEAN_DATA_PATH, TARGET_COL, DATE_COL,
    TRAIN_END_YEAR, TEST_START_YEAR,
    LAG_FEATURES, ROLLING_WINDOWS,
)

logger = logging.getLogger(__name__)

# Ánh xạ tên cột có thể gặp trong file CSV gốc → tên chuẩn
_COL_ALIASES: dict[str, str] = {
    "pm2.5":       TARGET_COL,
    "pm25":        TARGET_COL,
    "pm_2_5":      TARGET_COL,
    "datetime":    DATE_COL,
    "date":        DATE_COL,
    "time":        DATE_COL,
    "timestamp":   DATE_COL,
    "local time":  DATE_COL,
}


# ─── 1. Đọc dữ liệu thô ───────────────────────────────────────────────────────

def load_raw(src_dir: Path = RAW_DIR) -> pd.DataFrame:
    """
    Đọc tất cả file CSV trong thư mục raw và ghép thành một DataFrame.

    Returns:
        DataFrame thô chưa qua xử lý.
    """
    csv_files = sorted(src_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(
            f"Không tìm thấy file CSV nào trong '{src_dir}'. "
            "Hãy chạy notebook 00_data_download.ipynb trước."
        )

    dfs = []
    for f in csv_files:
        logger.info(f"Đọc file: {f.name}")
        df = pd.read_csv(f, low_memory=False)
        # Chuẩn hóa tên cột về chữ thường
        df.columns = df.columns.str.strip().str.lower()
        dfs.append(df)

    combined = pd.concat(dfs, ignore_index=True)
    logger.info(f"Tổng số bản ghi thô: {len(combined):,}")
    return combined


# ─── 2. Làm sạch và chuẩn hóa ────────────────────────────────────────────────

def preprocess(df: pd.DataFrame, min_obs_per_day: int = 12) -> pd.DataFrame:
    """
    Làm sạch DataFrame thô, chuẩn hoá cột thời gian, xử lý giá trị thiếu
    và bất thường, tổng hợp về trung bình ngày.

    Args:
        df:               DataFrame thô.
        min_obs_per_day:  Số quan trắc hợp lệ tối thiểu trong ngày để
                          đưa vào trung bình (tránh trung bình từ 1-2 điểm).

    Returns:
        DataFrame với chỉ mục là ngày (DatetimeIndex), 1 hàng / ngày.
    """
    # 2.1 Đổi tên cột theo bảng ánh xạ
    df = df.rename(columns={k: v for k, v in _COL_ALIASES.items() if k in df.columns})

    if DATE_COL not in df.columns:
        raise KeyError(f"Không tìm thấy cột thời gian. Cần 1 trong: {list(_COL_ALIASES.keys())}")
    if TARGET_COL not in df.columns:
        raise KeyError(f"Không tìm thấy cột '{TARGET_COL}'. Cần 1 trong: {list(_COL_ALIASES.keys())}")

    # 2.2 Parse thời gian
    df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
    before = len(df)
    df = df.dropna(subset=[DATE_COL])
    logger.info(f"Loại {before - len(df):,} hàng do thời gian không hợp lệ.")

    # 2.3 Ép kiểu PM2.5 về số, thay giá trị âm bằng NaN
    df[TARGET_COL] = pd.to_numeric(df[TARGET_COL], errors="coerce")
    neg_mask = df[TARGET_COL] < 0
    if neg_mask.any():
        logger.warning(f"Tìm thấy {neg_mask.sum():,} giá trị PM2.5 âm → chuyển thành NaN.")
        df.loc[neg_mask, TARGET_COL] = np.nan

    # 2.4 Loại bỏ bản ghi trùng
    dup_count = df.duplicated().sum()
    if dup_count:
        df = df.drop_duplicates()
        logger.info(f"Đã loại {dup_count:,} bản ghi trùng.")

    # 2.5 Sắp xếp theo thời gian
    df = df.sort_values(DATE_COL).reset_index(drop=True)

    # 2.6 Tổng hợp về trung bình ngày
    df["_date_only"] = df[DATE_COL].dt.normalize()
    daily = (
        df.groupby("_date_only")[TARGET_COL]
          .agg(pm25_mean="mean", pm25_count="count")
          .reset_index()
          .rename(columns={"_date_only": DATE_COL})
    )

    # Loại ngày có quá ít quan trắc
    low_obs = daily["pm25_count"] < min_obs_per_day
    if low_obs.any():
        logger.warning(
            f"{low_obs.sum()} ngày có ít hơn {min_obs_per_day} quan trắc hợp lệ → loại bỏ."
        )
        daily = daily[~low_obs]

    daily = daily.rename(columns={"pm25_mean": TARGET_COL})
    daily = daily[[DATE_COL, TARGET_COL]].set_index(DATE_COL)
    daily.index = pd.DatetimeIndex(daily.index)

    # 2.7 Nội suy tuyến tính cho khoảng thiếu ngắn (≤ 7 ngày)
    full_idx = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
    daily = daily.reindex(full_idx)
    missing_before = daily[TARGET_COL].isna().sum()
    daily[TARGET_COL] = daily[TARGET_COL].interpolate(method="time", limit=7)
    missing_after = daily[TARGET_COL].isna().sum()
    logger.info(
        f"Nội suy: {missing_before - missing_after} giá trị thiếu đã được điền; "
        f"{missing_after} vẫn còn thiếu."
    )

    daily.index.name = DATE_COL
    logger.info(f"Dữ liệu sau xử lý: {len(daily):,} ngày "
                f"({daily.index.min().date()} → {daily.index.max().date()})")
    return daily


# ─── 3. Lưu / Tải dữ liệu đã xử lý ─────────────────────────────────────────

def save_clean(df: pd.DataFrame, path: Path = CLEAN_DATA_PATH) -> None:
    """Lưu DataFrame đã làm sạch ra file CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path)
    logger.info(f"Đã lưu dữ liệu sạch tại: {path}")


def load_clean(path: Path = CLEAN_DATA_PATH) -> pd.DataFrame:
    """Tải file CSV đã làm sạch, đặt cột date làm chỉ mục."""
    if not path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy '{path}'. "
            "Hãy chạy notebook 01_data_preprocessing.ipynb trước."
        )
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    df.index.name = DATE_COL
    return df


# ─── 4. Kỹ thuật đặc trưng (Feature Engineering) ─────────────────────────────

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tạo các đặc trưng lag, rolling mean/std và đặc trưng thời gian.
    Chỉ sử dụng thông tin quá khứ → không rò rỉ dữ liệu.

    Args:
        df: DataFrame với DatetimeIndex và cột TARGET_COL.

    Returns:
        DataFrame chứa đặc trưng và cột mục tiêu. Các hàng đầu có NaN
        (do lag/rolling) sẽ được giữ lại để caller tự xử lý.
    """
    feat = df.copy()
    pm = feat[TARGET_COL]

    # Lag features
    for lag in LAG_FEATURES:
        feat[f"lag_{lag}"] = pm.shift(lag)

    # Rolling mean
    for w in ROLLING_WINDOWS:
        feat[f"rolling_mean_{w}"] = pm.shift(1).rolling(w).mean()

    # Rolling std (7 ngày)
    feat["rolling_std_7"] = pm.shift(1).rolling(7).std()

    # Đặc trưng thời gian
    feat["day_of_week"] = feat.index.dayofweek          # 0=Thứ 2 … 6=CN
    feat["month"]       = feat.index.month               # 1–12
    feat["quarter"]     = feat.index.quarter             # 1–4
    feat["season"]      = feat["month"].map(_month_to_season)
    feat["year"]        = feat.index.year

    return feat


def _month_to_season(month: int) -> int:
    """Ánh xạ tháng → mùa (1=Xuân, 2=Hè, 3=Thu, 4=Đông)."""
    if month in (3, 4, 5):
        return 1
    elif month in (6, 7, 8):
        return 2
    elif month in (9, 10, 11):
        return 3
    else:
        return 4


# ─── 5. Chia tập huấn luyện / kiểm thử ───────────────────────────────────────

def split_train_test(
    df: pd.DataFrame,
    train_end: int = TRAIN_END_YEAR,
    test_start: int = TEST_START_YEAR,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Chia DataFrame theo thứ tự thời gian (tuyệt đối không chia ngẫu nhiên).

    Args:
        df:          DataFrame với DatetimeIndex.
        train_end:   Năm cuối của tập huấn luyện (bao gồm).
        test_start:  Năm bắt đầu của tập kiểm thử (bao gồm).

    Returns:
        (train_df, test_df)
    """
    train = df[df.index.year <= train_end]
    test  = df[df.index.year >= test_start]
    logger.info(
        f"Tập huấn luyện: {len(train):,} ngày "
        f"({train.index.min().date()} → {train.index.max().date()})"
    )
    logger.info(
        f"Tập kiểm thử:   {len(test):,} ngày "
        f"({test.index.min().date()} → {test.index.max().date()})"
    )
    return train, test


# ─── 6. Báo cáo chất lượng dữ liệu ──────────────────────────────────────────

def data_quality_report(raw: pd.DataFrame, clean: pd.DataFrame) -> pd.DataFrame:
    """Tạo bảng so sánh số bản ghi trước / sau xử lý."""
    report = pd.DataFrame({
        "Chỉ số": [
            "Số bản ghi",
            "Giá trị PM2.5 thiếu",
            "Giá trị PM2.5 âm",
            "Bản ghi trùng",
        ],
        "Trước xử lý": [
            len(raw),
            raw[TARGET_COL].isna().sum() if TARGET_COL in raw.columns else "N/A",
            (raw[TARGET_COL] < 0).sum() if TARGET_COL in raw.columns else "N/A",
            raw.duplicated().sum(),
        ],
        "Sau xử lý": [
            len(clean),
            clean[TARGET_COL].isna().sum(),
            0,
            0,
        ],
    })
    return report
