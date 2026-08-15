"""Walk-forward splitting utilities for time-series experiments."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class TimeSplit:
    train_start: pd.Timestamp
    train_end: pd.Timestamp
    test_start: pd.Timestamp
    test_end: pd.Timestamp


def expanding_monthly_splits(
    index: pd.DatetimeIndex,
    initial_train_end: str,
    horizon_months: int = 1,
) -> list[TimeSplit]:
    """Create expanding-window monthly splits for research-grade evaluation."""
    train_start = index.min()
    current_train_end = pd.Timestamp(initial_train_end)
    splits: list[TimeSplit] = []

    while True:
        test_start = current_train_end + pd.Timedelta(days=1)
        test_end = test_start + pd.DateOffset(months=horizon_months) - pd.Timedelta(days=1)
        if test_start > index.max():
            break
        splits.append(
            TimeSplit(
                train_start=train_start,
                train_end=min(current_train_end, index.max()),
                test_start=test_start,
                test_end=min(test_end, index.max()),
            )
        )
        current_train_end = test_end
        if current_train_end >= index.max():
            break
    return splits
