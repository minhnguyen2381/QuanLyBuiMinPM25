"""Đọc dữ liệu CSV thô cho project dự báo PM2.5 Hà Nội.

Module này là bước đầu của pipeline: tìm các file `.csv` trong thư mục dữ liệu
thô, đọc từng file bằng pandas, rồi ghép chúng thành một bảng duy nhất.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def list_csv_files(raw_dir: str | Path) -> list[Path]:
    """Liệt kê tất cả file CSV trong thư mục dữ liệu thô.

    Hàm sắp xếp tên file để thứ tự đọc ổn định giữa các lần chạy. Nếu không có
    file CSV nào, hàm báo lỗi sớm để người dùng biết cần kiểm tra lại dữ liệu.
    """
    files = sorted(Path(raw_dir).glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {raw_dir}")
    return files


def load_raw_data(raw_dir: str | Path) -> pd.DataFrame:
    """Đọc và ghép toàn bộ file CSV thô thành một DataFrame.

    Cột `source_file` được thêm vào để truy vết mỗi dòng đến từ file nào. Điều
    này hữu ích khi cần kiểm tra lỗi dữ liệu hoặc giải thích nguồn gốc bản ghi.
    """
    frames = []
    for csv_path in list_csv_files(raw_dir):
        frame = pd.read_csv(csv_path, low_memory=False)
        frame["source_file"] = csv_path.name
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)
