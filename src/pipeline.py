"""Research-grade PM2.5 forecasting pipeline."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from src.config_loader import load_project_configs, project_path
from src.data.feature_engineering import create_supervised_features
from src.data.ingestion import load_raw_data
from src.data.preprocessing import preprocess_raw_data
from src.data.validation import build_quality_report
from src.evaluation.error_analysis import monthly_error_summary, top_absolute_errors
from src.evaluation.metrics import compare_forecasts
from src.models.arima import adf_test, rolling_arima_forecast, select_arima_order
from src.models.baselines import naive_forecast, seasonal_naive_forecast
from src.models.random_forest import (
    feature_importance,
    forecast_random_forest,
    split_supervised_by_year,
    train_random_forest,
)
from src.reporting.figures import (
    plot_actual_vs_predicted,
    plot_correlation_heatmap,
    plot_error_distribution,
    plot_feature_importance,
    plot_forecast_comparison,
    plot_monthly_boxplot,
    plot_monthly_mean_by_year,
    plot_monthly_rmse,
    plot_pm25_distribution,
    plot_pm25_time_series,
)
from src.reporting.statistics import (
    descriptive_statistics,
    forecast_error_detail,
    missing_data_summary,
    pm25_correlation_table,
    temporal_statistics,
    threshold_summary,
)
from src.reporting.tables import save_table


def _experiment_id(name: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{stamp}_{name}"


def _write_series(series: pd.Series, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    series.to_csv(path, header=True, encoding="utf-8-sig")
    return path


def _display_model_names() -> dict[str, str]:
    """Tên mô hình dùng trong bảng và hình để tránh dịch máy móc."""
    return {
        "Naive": "Mô hình tham chiếu (Naive)",
        "SeasonalNaive7": "Tham chiếu mùa vụ 7 ngày",
        "ARIMA": "ARIMA",
        "Random Forest": "Random Forest",
    }


def run_research_pipeline(configs: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    """Chạy toàn bộ thực nghiệm ARIMA và Random Forest, đồng thời lưu bảng/hình báo cáo."""
    configs = configs or load_project_configs()
    data_cfg = configs["data"]
    arima_cfg = configs["arima"]
    rf_cfg = configs["random_forest"]
    exp_cfg = configs["experiment"]

    exp_id = _experiment_id(exp_cfg["experiment_name"])
    exp_dir = project_path(exp_cfg["experiments_dir"]) / exp_id
    pred_dir = exp_dir / "predictions"

    raw = load_raw_data(project_path(data_cfg["raw_dir"]))
    clean = preprocess_raw_data(raw, data_cfg)
    clean_path = project_path(data_cfg["clean_path"])
    clean_path.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(clean_path, encoding="utf-8-sig")

    quality = build_quality_report(raw, clean, data_cfg)
    save_table(quality, exp_dir / "data_quality_report.csv")

    target = data_cfg["target_col"]
    table_dir = exp_dir / "tables"
    figure_dir = exp_dir / "figures"

    # Các bảng thống kê này giúp phần kết quả không chỉ dựa vào metric mô hình.
    save_table(descriptive_statistics(clean), table_dir / "thong_ke_mo_ta.csv")
    save_table(missing_data_summary(clean), table_dir / "du_lieu_thieu_sau_tien_xu_ly.csv")
    save_table(pm25_correlation_table(clean, target), table_dir / "tuong_quan_pm25_bien_ngoai_sinh.csv")
    save_table(threshold_summary(clean, target), table_dir / "so_ngay_vuot_nguong_tham_khao.csv")
    for name, table in temporal_statistics(clean, target).items():
        save_table(table, table_dir / f"thong_ke_pm25_theo_{name}.csv")

    # Bộ biểu đồ EDA được sinh lại từ pipeline mới, thay cho các hình notebook cũ.
    plot_pm25_time_series(clean, target, figure_dir / "01_dien_bien_pm25.png")
    plot_pm25_distribution(clean, target, figure_dir / "02_phan_phoi_pm25.png")
    plot_monthly_boxplot(clean, target, figure_dir / "03_boxplot_pm25_theo_thang.png")
    plot_monthly_mean_by_year(clean, target, figure_dir / "04_trung_binh_pm25_theo_thang_nam.png")
    plot_correlation_heatmap(clean, figure_dir / "05_heatmap_tuong_quan.png")

    train = clean[clean.index.year <= int(data_cfg["train_end_year"])][target]
    test = clean[clean.index.year >= int(data_cfg["test_start_year"])][target]

    adf = pd.DataFrame([adf_test(train)])
    save_table(adf, exp_dir / "arima_adf_test.csv")

    order, order_grid = select_arima_order(
        train,
        p_values=arima_cfg["p_range"],
        d_values=arima_cfg["d_range"],
        q_values=arima_cfg["q_range"],
        information_criterion=arima_cfg.get("information_criterion", "aic"),
    )
    save_table(order_grid, exp_dir / "arima_order_grid.csv")
    arima_pred = rolling_arima_forecast(train, test, order)
    _write_series(arima_pred, pred_dir / "arima_predictions.csv")

    feature_config = {"target_col": target, "random_forest": rf_cfg}
    supervised, _, feature_cols = create_supervised_features(clean, feature_config)
    x_train, x_test, y_train, y_test = split_supervised_by_year(
        supervised,
        target,
        feature_cols,
        int(data_cfg["train_end_year"]),
        int(data_cfg["test_start_year"]),
    )
    rf_model, rf_params, cv_results = train_random_forest(x_train, y_train, rf_cfg)
    rf_pred = forecast_random_forest(rf_model, x_test, y_test.index)
    _write_series(rf_pred, pred_dir / "random_forest_predictions.csv")

    if cv_results is not None:
        save_table(cv_results, exp_dir / "random_forest_cv_results.csv")
    save_table(pd.DataFrame([rf_params]), exp_dir / "random_forest_best_params.csv")
    importances = feature_importance(rf_model, feature_cols)
    save_table(importances.to_frame(), exp_dir / "random_forest_feature_importance.csv")
    plot_feature_importance(importances, figure_dir / "06_dac_trung_quan_trong_random_forest.png")

    predictions = {
        "Naive": naive_forecast(test),
        "SeasonalNaive7": seasonal_naive_forecast(test, season_length=7),
        "ARIMA": arima_pred,
        "Random Forest": rf_pred,
    }
    display_names = _display_model_names()
    display_predictions = {display_names.get(name, name): pred for name, pred in predictions.items()}

    comparison = compare_forecasts(test, predictions).rename(index=display_names)
    save_table(comparison, exp_dir / "model_comparison.csv")
    save_table(monthly_error_summary(test, arima_pred), exp_dir / "monthly_error_arima.csv")
    save_table(monthly_error_summary(y_test, rf_pred), exp_dir / "monthly_error_random_forest.csv")
    save_table(top_absolute_errors(test, arima_pred), exp_dir / "top_errors_arima.csv")
    save_table(top_absolute_errors(y_test, rf_pred), exp_dir / "top_errors_random_forest.csv")
    plot_forecast_comparison(test, display_predictions, exp_dir / "forecast_comparison.png")
    save_table(forecast_error_detail(test, display_predictions), table_dir / "chi_tiet_sai_so_theo_ngay.csv")
    plot_monthly_rmse(test, display_predictions, figure_dir / "07_rmse_theo_thang.png")
    plot_error_distribution(test, display_predictions, figure_dir / "08_phan_phoi_sai_so_du_bao.png")
    plot_actual_vs_predicted(test, display_predictions, figure_dir / "09_thuc_te_va_du_bao_scatter.png")

    return {
        "experiment_id": exp_id,
        "experiment_dir": exp_dir,
        "clean_data_path": clean_path,
        "arima_order": order,
        "random_forest_params": rf_params,
        "comparison": comparison,
    }
