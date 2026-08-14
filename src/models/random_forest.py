"""Random Forest training and forecasting helpers."""

from __future__ import annotations

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit


def split_supervised_by_year(
    supervised: pd.DataFrame,
    target_col: str,
    feature_cols: list[str],
    train_end_year: int,
    test_start_year: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split supervised data by time, never randomly."""
    train_mask = supervised.index.year <= train_end_year
    test_mask = supervised.index.year >= test_start_year
    return (
        supervised.loc[train_mask, feature_cols],
        supervised.loc[test_mask, feature_cols],
        supervised.loc[train_mask, target_col],
        supervised.loc[test_mask, target_col],
    )


def train_random_forest(
    x_train: pd.DataFrame,
    y_train: pd.Series,
    rf_config: dict,
) -> tuple[RandomForestRegressor, dict, pd.DataFrame | None]:
    """Train Random Forest with optional time-series hyperparameter search."""
    model = RandomForestRegressor(**rf_config["model"])
    search_cfg = rf_config.get("search", {})
    if not search_cfg.get("enabled", False):
        model.fit(x_train, y_train)
        return model, rf_config["model"], None

    search = RandomizedSearchCV(
        model,
        param_distributions=search_cfg["param_distributions"],
        n_iter=int(search_cfg.get("n_iter", 20)),
        cv=TimeSeriesSplit(n_splits=int(search_cfg.get("cv_splits", 5))),
        scoring=search_cfg.get("scoring", "neg_root_mean_squared_error"),
        random_state=search_cfg.get("random_state", 42),
        n_jobs=-1,
    )
    search.fit(x_train, y_train)
    cv_results = pd.DataFrame(search.cv_results_).sort_values("rank_test_score")
    return search.best_estimator_, search.best_params_, cv_results


def forecast_random_forest(model: RandomForestRegressor, x_test: pd.DataFrame, index: pd.Index) -> pd.Series:
    """Forecast PM2.5 with a trained Random Forest model."""
    return pd.Series(model.predict(x_test), index=index, name="Random Forest")


def feature_importance(model: RandomForestRegressor, feature_cols: list[str]) -> pd.Series:
    """Return sorted impurity-based feature importances."""
    return pd.Series(model.feature_importances_, index=feature_cols, name="importance").sort_values(ascending=False)
