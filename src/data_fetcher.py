"""
data_fetcher.py — Tải dữ liệu từ Kaggle về thư mục data/raw/.

Yêu cầu:
    - Đã cài thư viện `kaggle` (pip install kaggle).
    - Đã đặt file kaggle.json vào ~/.kaggle/kaggle.json (hoặc
      cài đặt biến môi trường KAGGLE_USERNAME + KAGGLE_KEY).

Hướng dẫn lấy Kaggle API key:
    1. Đăng nhập tại https://www.kaggle.com
    2. Vào Account Settings → API → Create New API Token
    3. Lưu file kaggle.json vào C:/Users/<tên>/.kaggle/kaggle.json
"""

import os
import zipfile
import logging
from pathlib import Path

from src.config import KAGGLE_DATASET, RAW_DIR

logger = logging.getLogger(__name__)


def download_dataset(dataset: str = KAGGLE_DATASET, dest: Path = RAW_DIR) -> Path:
    """
    Tải dataset từ Kaggle và giải nén vào thư mục `dest`.

    Args:
        dataset: Đường dẫn dataset Kaggle dạng "owner/dataset-slug".
        dest:    Thư mục lưu file thô (mặc định: data/raw/).

    Returns:
        Đường dẫn thư mục chứa dữ liệu đã giải nén.
    """
    try:
        import kaggle  # noqa: F401  — kiểm tra import trước
    except ImportError:
        raise ImportError(
            "Thư viện 'kaggle' chưa được cài đặt. "
            "Chạy: pip install kaggle"
        )

    dest.mkdir(parents=True, exist_ok=True)
    logger.info(f"Đang tải dataset '{dataset}' vào '{dest}' ...")

    # Gọi Kaggle CLI qua Python subprocess để đảm bảo tương thích
    import subprocess
    result = subprocess.run(
        ["kaggle", "datasets", "download", "-d", dataset,
         "--path", str(dest), "--unzip"],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        logger.error(result.stderr)
        raise RuntimeError(
            f"Tải dữ liệu thất bại:\n{result.stderr}\n"
            "Kiểm tra lại file ~/.kaggle/kaggle.json và kết nối mạng."
        )

    logger.info(f"Tải thành công! Dữ liệu đã lưu tại: {dest}")
    return dest


def list_raw_files(dest: Path = RAW_DIR) -> list[Path]:
    """Trả về danh sách tất cả file CSV trong thư mục raw."""
    files = list(dest.glob("*.csv"))
    if not files:
        logger.warning(f"Không tìm thấy file CSV nào trong '{dest}'.")
    return files
