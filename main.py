"""Chạy toàn bộ pipeline dự báo PM2.5 từ dữ liệu thô có sẵn.

Sử dụng:
    python main.py
"""

import logging

import matplotlib

# Chạy được cả trên máy không có giao diện đồ họa (terminal/CI).
matplotlib.use("Agg")

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit

from src.arima_model import forecast_arima, select_arima_order, train_arima
from src.config import TARGET_COL
from src.data_processor import load_raw, preprocess, save_clean, split_train_test
from src.evaluator import compare_models, naive_forecast
from src.rf_model import forecast_rf, prepare_rf_data, split_rf_data


def run_pipeline() -> None:
    """Tiền xử lý, huấn luyện ARIMA/RF, dự báo và lưu bảng so sánh."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    clean = preprocess(load_raw())
    save_clean(clean)
    train, test = split_train_test(clean)

    order = select_arima_order(train[TARGET_COL])
    arima_preds = forecast_arima(
        train[TARGET_COL], test[TARGET_COL], order=order, save=True
    )

    feat_df, y, feature_cols = prepare_rf_data(clean)
    x_train, x_test, y_train, y_test = split_rf_data(feat_df, y, feature_cols)
    search = RandomizedSearchCV(
        RandomForestRegressor(random_state=42, n_jobs=-1),
        param_distributions={
            "n_estimators": [100, 200, 300],
            "max_depth": [5, 10, 15, None],
            "min_samples_leaf": [1, 2, 4],
        },
        n_iter=15,
        cv=TimeSeriesSplit(n_splits=3),
        scoring="neg_root_mean_squared_error",
        random_state=42,
        n_jobs=-1,
    )
    search.fit(x_train, y_train)
    rf_preds = forecast_rf(search.best_estimator_, x_test, y_test, save=True)

    comparison = compare_models(
        test[TARGET_COL],
        {
            "Dự báo tham chiếu": naive_forecast(test[TARGET_COL]),
            "ARIMA": arima_preds,
            "Random Forest": rf_preds,
        },
        save=True,
    )
    print("ARIMA order:", order)
    print("Random Forest parameters:", search.best_params_)
    print(comparison.to_string())


if __name__ == "__main__":
    run_pipeline()
