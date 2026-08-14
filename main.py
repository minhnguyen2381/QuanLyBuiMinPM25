"""Chạy pipeline nghiên cứu dự báo PM2.5 tại Hà Nội.

Sử dụng:
    python main.py
"""

import logging
import sys

import matplotlib

matplotlib.use("Agg")

from src.pipeline import run_research_pipeline


def run_pipeline() -> None:
    """Chạy thực nghiệm ARIMA và Random Forest, sau đó in tóm tắt kết quả."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    result = run_research_pipeline()

    print("Mã thực nghiệm:", result["experiment_id"])
    print("Thư mục kết quả:", result["experiment_dir"])
    print("Dữ liệu sạch đa biến:", result["clean_data_path"])
    print("Bộ tham số ARIMA được chọn:", result["arima_order"])
    print("Tham số Random Forest tốt nhất:", result["random_forest_params"])
    print(result["comparison"].to_string())


if __name__ == "__main__":
    run_pipeline()
