"""Các hàm đọc cấu hình YAML cho toàn bộ pipeline nghiên cứu.

Project tách cấu hình ra thư mục `configs` để người mới có thể đổi đường dẫn,
tham số ARIMA, tham số Random Forest hoặc tên thực nghiệm mà không cần sửa code
xử lý chính.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT_DIR / "configs"


def load_yaml_config(path: str | Path) -> dict[str, Any]:
    """Đọc một file YAML và trả về dict Python.

    Nếu `path` là đường dẫn tương đối, hàm tự hiểu nó bắt đầu từ thư mục gốc của
    project. Nếu file YAML rỗng, hàm trả `{}` để các bước sau không bị lỗi vì
    nhận giá trị `None`.
    """
    cfg_path = Path(path)
    if not cfg_path.is_absolute():
        cfg_path = ROOT_DIR / cfg_path
    with cfg_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_project_configs() -> dict[str, dict[str, Any]]:
    """Đọc bốn nhóm cấu hình chính dùng trong một lần chạy thực nghiệm.

    Kết quả có các khóa `data`, `arima`, `random_forest` và `experiment`. Các
    module khác lấy cấu hình qua những khóa này thay vì tự đọc file riêng lẻ.
    """
    return {
        "data": load_yaml_config(CONFIG_DIR / "data.yaml"),
        "arima": load_yaml_config(CONFIG_DIR / "arima.yaml"),
        "random_forest": load_yaml_config(CONFIG_DIR / "random_forest.yaml"),
        "experiment": load_yaml_config(CONFIG_DIR / "experiment.yaml"),
    }


def project_path(value: str | Path) -> Path:
    """Chuyển đường dẫn trong config thành đường dẫn tuyệt đối trong project.

    Config thường dùng đường dẫn tương đối như `data/raw` hoặc `results/...`.
    Hàm này giúp mọi module đều ghi/đọc đúng vị trí dù script được chạy từ đâu.
    """
    path = Path(value)
    return path if path.is_absolute() else ROOT_DIR / path
