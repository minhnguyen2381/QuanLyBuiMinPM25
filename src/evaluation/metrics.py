"""Forecast metrics for PM2.5 experiments."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def align_actual_predicted(actual: pd.Series, predicted: pd.Series) -> pd.DataFrame:
    """Align actual and predicted series and drop missing values."""
    return pd.DataFrame({"actual": actual, "predicted": predicted}).dropna()


def directional_accuracy(actual: pd.Series, predicted: pd.Series) -> float:
    """Share of days where the forecast gets the direction of change right."""
    aligned = align_actual_predicted(actual, predicted)
    if len(aligned) < 2:
        return np.nan
    actual_direction = np.sign(aligned["actual"].diff().dropna())
    pred_direction = np.sign(aligned["predicted"].diff().dropna())
    return float((actual_direction == pred_direction).mean())


def compute_forecast_metrics(actual: pd.Series, predicted: pd.Series, model_name: str) -> dict:
    """Compute an expanded metric set."""
    aligned = align_actual_predicted(actual, predicted)
    if aligned.empty:
        raise ValueError(f"No overlapping observations for {model_name}.")

    y_true = aligned["actual"].to_numpy()
    y_pred = aligned["predicted"].to_numpy()
    denominator = np.where(y_true == 0, np.nan, np.abs(y_true))
    mape = np.nanmean(np.abs((y_true - y_pred) / denominator)) * 100
    smape = np.nanmean(2 * np.abs(y_pred - y_true) / (np.abs(y_true) + np.abs(y_pred))) * 100

    return {
        "Model": model_name,
        "MAE": round(float(mean_absolute_error(y_true, y_pred)), 4),
        "RMSE": round(float(np.sqrt(mean_squared_error(y_true, y_pred))), 4),
        "MAPE": round(float(mape), 4),
        "SMAPE": round(float(smape), 4),
        "R2": round(float(r2_score(y_true, y_pred)), 4),
        "DirectionalAccuracy": round(directional_accuracy(actual, predicted), 4),
        "N": int(len(aligned)),
    }


def compare_forecasts(actual: pd.Series, predictions: dict[str, pd.Series]) -> pd.DataFrame:
    """Compare multiple forecast series on the same actual values."""
    table = pd.DataFrame(
        [compute_forecast_metrics(actual, pred, name) for name, pred in predictions.items()]
    ).set_index("Model")
    if "Naive" in table.index:
        baseline_rmse = table.loc["Naive", "RMSE"]
        table["Cải thiện RMSE so với mô hình tham chiếu (%)"] = (
            (baseline_rmse - table["RMSE"]) / baseline_rmse * 100
        ).round(2)
    return table
