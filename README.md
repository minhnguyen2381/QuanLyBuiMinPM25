# Dự án Phân tích và Dự báo Bụi mịn PM2.5 tại Hà Nội

Dự án này tập trung vào việc thu thập, phân tích và xây dựng mô hình dự báo nồng độ bụi mịn PM2.5 tại Hà Nội dựa trên dữ liệu chất lượng không khí từ năm 2022 đến 2025.

## 📂 Cấu trúc dự án

Dự án được tổ chức như sau:

- `data/`: 
  - `raw/`: Dữ liệu thô tải về từ Kaggle.
  - `processed/`: Dữ liệu đã được làm sạch và chuẩn hóa.
- `docs/`: Chứa các tài liệu liên quan đến dự án.
- `figures/`: Lưu trữ các biểu đồ phân tích và kết quả mô hình.
- `notebooks/`: Chứa các file Jupyter Notebook thể hiện từng bước trong quy trình phân tích và xây dựng mô hình.
- `results/`: Lưu trữ kết quả dự báo của các mô hình (ví dụ: `arima_predictions.csv`, `rf_predictions.csv`) và bảng đánh giá so sánh.
- `src/`: Các module mã nguồn Python dùng chung cho dự án:
  - `config.py`: File cấu hình đường dẫn và các tham số chung.
  - `data_fetcher.py`: Tải dữ liệu từ Kaggle.
  - `data_processor.py`: Xử lý và làm sạch dữ liệu.
  - `visualizer.py`: Các hàm vẽ biểu đồ.
  - `evaluator.py`: Các hàm đánh giá mô hình.
  - `arima_model.py` & `rf_model.py`: Chứa logic huấn luyện các mô hình.
- `requirements.txt`: Danh sách các thư viện Python cần thiết.

## 🚀 Quy trình thực hiện (Notebooks)

Để hiểu hoặc tái tạo lại kết quả của dự án, bạn có thể mở thư mục `notebooks/` và chạy các notebook theo thứ tự:

1. **`00_data_download.ipynb`**: Tự động tải dataset từ Kaggle.
2. **`01_data_preprocessing.ipynb`**: Làm sạch dữ liệu, nội suy các giá trị bị thiếu và thêm các đặc trưng thời gian.
3. **`02_eda.ipynb`**: Phân tích dữ liệu khám phá (EDA), đánh giá tính xu hướng và tính mùa vụ của PM2.5.
4. **`03_arima.ipynb`**: Huấn luyện và kiểm thử mô hình thống kê ARIMA.
5. **`04_random_forest.ipynb`**: Xây dựng các đặc trưng như độ trễ (lag), cửa sổ trượt (rolling) và huấn luyện mô hình Machine Learning Random Forest.
6. **`05_model_comparison.ipynb`**: Đối chiếu, so sánh và đánh giá hiệu năng giữa các mô hình (dựa trên RMSE, MAE, R²).

*Ghi chú: Dữ liệu huấn luyện được lấy từ 2022-2024, và kiểm thử trên dữ liệu năm 2025.*

## 🛠 Cài đặt và Sử dụng

### Yêu cầu hệ thống
- Python 3.8 trở lên.
- Cần có tài khoản Kaggle (để tải dữ liệu tự động).

### Các bước thiết lập
1. **Clone dự án (nếu cần):**
   ```bash
   git clone <đường-dẫn-repo>
   cd QuanLyBuiMinPM25
   ```

2. **Cài đặt thư viện:**
   Mở terminal và chạy lệnh sau (khuyến khích sử dụng môi trường ảo như `.venv`):
   ```bash
   pip install -r requirements.txt
   ```

3. **Cấu hình Kaggle API:**
   - Đăng nhập vào Kaggle, vào mục **Settings** -> **Create New API Token** để tải file `kaggle.json`.
   - Đặt file `kaggle.json` vào thư mục `C:\Users\<Tên_User>\.kaggle\` (đối với Windows) hoặc `~/.kaggle/` (đối với Linux/Mac).

4. **Chạy dự án:**
   Mở môi trường Jupyter:
   ```bash
   jupyter notebook
   # Hoặc jupyter lab
   ```
   Sau đó, truy cập vào thư mục `notebooks/` và chạy lần lượt các file.

## ⚙️ Quản lý cấu hình
Tất cả các cấu hình về tham số huấn luyện (như Random Forest hyper-parameters), tên cột mục tiêu, đường dẫn thư mục, và dataset Kaggle (`phungdinhdat/aqi-in-hanoi-2022-2025`) được quản lý tập trung trong file `src/config.py`. Việc thay đổi tham số tại đây sẽ áp dụng đồng loạt cho tất cả các bước.
