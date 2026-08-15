import numpy as np
import pandas as pd

from src.data.feature_engineering import create_supervised_features
from src.data.preprocessing import preprocess_raw_data
from src.evaluation.metrics import compare_forecasts
from src.reporting.statistics import descriptive_statistics, pm25_correlation_table, temporal_statistics


def test_preprocess_preserves_exogenous_columns():
    raw = pd.DataFrame(
        {
            "Local Time": pd.date_range("2025-01-01", periods=24, freq="h"),
            "PM25": np.arange(24, dtype=float),
            "Temperature": np.linspace(20, 22, 24),
            "Wind Speed": np.linspace(1, 2, 24),
        }
    )
    cfg = {
        "date_col": "date",
        "target_col": "PM2.5",
        "date_candidates": ["local time"],
        "target_candidates": ["pm25"],
        "exogenous_candidates": ["Temperature", "Wind Speed"],
        "min_obs_per_day": 12,
        "interpolate_limit_days": 7,
    }

    clean = preprocess_raw_data(raw, cfg)

    assert list(clean.columns) == ["PM2.5", "Temperature", "Wind Speed"]
    assert clean.loc[pd.Timestamp("2025-01-01"), "PM2.5"] == 11.5


def test_feature_engineering_uses_shifted_history():
    clean = pd.DataFrame(
        {
            "PM2.5": range(1, 41),
            "Temperature": range(101, 141),
        },
        index=pd.date_range("2025-01-01", periods=40, freq="D"),
    )
    cfg = {
        "target_col": "PM2.5",
        "random_forest": {
            "lags": [1, 7],
            "rolling_windows": [3],
            "add_diff_features": True,
            "add_calendar_features": True,
            "add_cyclic_features": True,
            "include_exogenous": True,
        },
    }

    supervised, y, feature_cols = create_supervised_features(clean, cfg)
    first_date = supervised.index.min()

    assert "pm25_lag_1" in feature_cols
    assert supervised.loc[first_date, "pm25_lag_1"] == clean.loc[first_date - pd.Timedelta(days=1), "PM2.5"]
    assert supervised.loc[first_date, "Temperature_lag_1"] == clean.loc[first_date - pd.Timedelta(days=1), "Temperature"]
    assert y.loc[first_date] == clean.loc[first_date, "PM2.5"]


def test_compare_forecasts_adds_baseline_improvement():
    actual = pd.Series([10.0, 12.0, 13.0, 15.0], index=pd.date_range("2025-01-01", periods=4))
    predictions = {
        "Naive": pd.Series([np.nan, 10.0, 12.0, 13.0], index=actual.index),
        "Model": pd.Series([10.0, 12.0, 13.0, 15.0], index=actual.index),
    }

    table = compare_forecasts(actual, predictions)

    assert "Cải thiện RMSE so với mô hình tham chiếu (%)" in table.columns
    assert table.loc["Model", "RMSE"] == 0


def test_reporting_statistics_are_created_with_vietnamese_columns():
    clean = pd.DataFrame(
        {
            "PM2.5": [20.0, 25.0, 30.0, 35.0],
            "Temperature": [18.0, 19.0, 20.0, 21.0],
        },
        index=pd.date_range("2025-01-01", periods=4, freq="D"),
    )

    desc = descriptive_statistics(clean)
    corr = pm25_correlation_table(clean, "PM2.5")
    temporal = temporal_statistics(clean, "PM2.5")

    assert "mean" in desc.columns
    assert "Tương quan với PM2.5" in corr.columns
    assert "Trung bình" in temporal["monthly"].columns
