"""Lưu các bảng kết quả nghiên cứu ra file CSV."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def save_table(df: pd.DataFrame, path: str | Path) -> Path:
    """Lưu DataFrame thành CSV UTF-8 có BOM và trả về đường dẫn output.

    `utf-8-sig` giúp Excel trên Windows mở tiếng Việt ít bị lỗi font hơn. Hàm
    cũng tự tạo thư mục cha nếu chưa tồn tại.
    """
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, encoding="utf-8-sig")
    return out
