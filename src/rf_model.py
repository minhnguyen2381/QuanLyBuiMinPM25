"""
rf_model.py — Đóng gói toàn bộ quy trình xây dựng mô hình Random Forest
Regression để dự báo PM2.5.

Quy trình:
    prepare_rf_data()   → Tạo ma trận đặc trưng từ chuỗi đã feature-engineer
    train_rf()          → Huấn luyện RandomForestRegressor
    forecast_rf()       → Dự báo trên tập kiểm thử
    get_feature_importance() → Trả về mức độ quan trọng của đặc trưng
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from src.config import (
    TARGET_COL, RF_PARAMS, RF_PRED_PATH,
    LAG_FEATURES, ROLLING_WINDOWS,
    TRAIN_END_YEAR, TEST_START_YEAR,
)
from src.data_processor import create_features

logger = logging.getLogger(__name__)


# ─── 1. Chuẩn bị dữ liệu cho Random Forest ───────────────────────────────────

def prepare_rf_data(
    clean_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series, list[str]]:
    """
    Tạo ma trận đặc trưng (X) và vector mục tiêu (y) từ dữ liệu sạch.

    Đặc trưng bao gồm lag, rolling mean/std và đặc trưng thời gian.
    Chỉ sử dụng thông tin quá khứ (shift=1) — không rò rỉ dữ liệu.

    Args:
        clean_df: DataFrame với DatetimeIndex và cột TARGET_COL.

    Returns:
        (feat_df, y, feature_cols)
        - feat_df:      DataFrame đặc trưng đã loại hàng NaN.
        - y:            Series mục tiêu tương ứng.
        - feature_cols: Danh sách tên cột đặc trưng.
    """
    feat_df = create_features(clean_df)

    # Cột đặc trưng (tất cả trừ TARGET_COL)
    feature_cols = [c for c in feat_df.columns if c != TARGET_COL]

    # Loại bỏ hàng NaN (do tính lag / rolling đầu chuỗi)
    feat_df = feat_df.dropna()
    X = feat_df[feature_cols]
    y = feat_df[TARGET_COL]

    logger.info(
        f"Ma trận đặc trưng: {X.shape[0]} mẫu × {X.shape[1]} đặc trưng "
        f"({X.index.min().date()} → {X.index.max().date()})"
    )
    return feat_df, y, feature_cols


# ─── 2. Chia tập huấn luyện / kiểm thử (theo thời gian) ─────────────────────

def split_rf_data(
    feat_df: pd.DataFrame,
    y: pd.Series,
    feature_cols: list[str],
    train_end: int = TRAIN_END_YEAR,
    test_start: int = TEST_START_YEAR,
) -> tuple:
    """
    Chia theo thứ tự thời gian — KHÔNG chia ngẫu nhiên.

    Returns:
        (X_train, X_test, y_train, y_test)
    """
    train_mask = feat_df.index.year <= train_end
    test_mask  = feat_df.index.year >= test_start

    X_train = feat_df.loc[train_mask, feature_cols]
    X_test  = feat_df.loc[test_mask,  feature_cols]
    y_train = y[train_mask]
    y_test  = y[test_mask]

    logger.info(
        f"Tập huấn luyện RF: {len(X_train):,} mẫu | "
        f"Tập kiểm thử RF: {len(X_test):,} mẫu"
    )
    return X_train, X_test, y_train, y_test


# ─── 3. Huấn luyện Random Forest ─────────────────────────────────────────────

def train_rf(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    params: dict = None,
) -> RandomForestRegressor:
    """
    Huấn luyện RandomForestRegressor.

    Args:
        X_train: Ma trận đặc trưng huấn luyện.
        y_train: Vector mục tiêu huấn luyện.
        params:  Dict tham số mô hình (mặc định: RF_PARAMS từ config).

    Returns:
        Mô hình đã được huấn luyện.
    """
    if params is None:
        params = RF_PARAMS

    logger.info(f"Huấn luyện Random Forest với tham số: {params}")
    model = RandomForestRegressor(**params)
    model.fit(X_train, y_train)
    logger.info("Huấn luyện Random Forest hoàn tất.")
    return model


# ─── 4. Dự báo và lưu kết quả ────────────────────────────────────────────────

def forecast_rf(
    model: RandomForestRegressor,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    save: bool = True,
    path: Path = RF_PRED_PATH,
) -> pd.Series:
    """
    Dự báo trên tập kiểm thử và lưu kết quả.

    Args:
        model:  Mô hình RF đã huấn luyện.
        X_test: Ma trận đặc trưng kiểm thử.
        y_test: Giá trị thực tế (dùng làm chỉ mục).
        save:   Lưu file CSV nếu True.
        path:   Đường dẫn file CSV đầu ra.

    Returns:
        pd.Series dự báo với DatetimeIndex của tập kiểm thử.
    """
    preds = model.predict(X_test)
    pred_series = pd.Series(preds, index=y_test.index, name="rf_pred")

    if save:
        path.parent.mkdir(parents=True, exist_ok=True)
        pred_series.to_csv(path, header=True)
        logger.info(f"Kết quả dự báo RF lưu tại: {path}")

    return pred_series


# ─── 5. Mức độ quan trọng của đặc trưng ──────────────────────────────────────

def get_feature_importance(
    model: RandomForestRegressor,
    feature_cols: list[str],
) -> pd.Series:
    """
    Trả về Series mức độ quan trọng của đặc trưng (sắp xếp giảm dần).

    Args:
        model:        Mô hình RF đã huấn luyện.
        feature_cols: Danh sách tên cột đặc trưng.

    Returns:
        pd.Series index = tên đặc trưng, value = importance score.
    """
    importances = pd.Series(
        model.feature_importances_,
        index=feature_cols,
        name="importance",
    ).sort_values(ascending=False)

    logger.info("Top 10 đặc trưng quan trọng nhất:")
    logger.info(importances.head(10).to_string())
    return importances
