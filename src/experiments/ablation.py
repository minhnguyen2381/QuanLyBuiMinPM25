"""Feature ablation helpers for Random Forest experiments."""

from __future__ import annotations

import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from src.evaluation.metrics import compute_forecast_metrics


def evaluate_feature_sets(
    feature_sets: dict[str, list[str]],
    x_train: pd.DataFrame,
    x_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    model_params: dict,
) -> pd.DataFrame:
    """Fit one RF model per feature set and compare metrics."""
    rows = []
    for name, cols in feature_sets.items():
        model = RandomForestRegressor(**model_params)
        model.fit(x_train[cols], y_train)
        pred = pd.Series(model.predict(x_test[cols]), index=y_test.index)
        rows.append(compute_forecast_metrics(y_test, pred, name))
    return pd.DataFrame(rows).set_index("Model")
