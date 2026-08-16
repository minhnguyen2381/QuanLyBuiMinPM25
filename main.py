"""Điểm bắt đầu để chạy toàn bộ nghiên cứu dự báo PM2.5 tại Hà Nội.

File này chỉ làm nhiệm vụ "bấm nút chạy": cấu hình logging, gọi pipeline chính
trong `src.pipeline`, rồi in ra các đường dẫn và kết quả quan trọng. Toàn bộ xử
lý dữ liệu, huấn luyện mô hình và lưu bảng/hình nằm trong các module `src`.

Sử dụng:
    python main.py
"""

import logging
import sys

import matplotlib

matplotlib.use("Agg")

from src.pipeline import run_research_pipeline


def run_pipeline() -> None:
    """Chạy thực nghiệm và in tóm tắt để người dùng biết kết quả nằm ở đâu.

    Hàm này không tự xử lý dữ liệu. Nó gọi `run_research_pipeline()`, nhận lại
    một dict kết quả, rồi in các thông tin dễ kiểm tra như mã thực nghiệm, thư
    mục output, bộ tham số ARIMA và tham số Random Forest tốt nhất.
    """
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
