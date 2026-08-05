# BẢN THIẾT KẾ: HỆ THỐNG PHÂN TÍCH VÀ DỰ BÁO PM2.5 TẠI HÀ NỘI

## 1. Tổng quan
Dự án nhằm phân tích và dự báo nồng độ bụi mịn PM2.5 tại Hà Nội dựa trên bộ dữ liệu từ Kaggle (2022-2025). Phương pháp tiếp cận sử dụng Modular Python kết hợp với Jupyter Notebook nhằm đảm bảo mã nguồn tái sử dụng được, sạch sẽ và phù hợp với tiêu chuẩn thực tế.

## 2. Kiến trúc và Cấu trúc thư mục
Cấu trúc dự án bao gồm thư mục dữ liệu, thư mục chứa mã nguồn (`src/`), các notebook để chạy và trực quan hóa (`notebooks/`), cũng như các thư mục đầu ra.

```text
PM25_Hanoi/
├── requirements.txt        # File chứa danh sách các thư viện cần cài đặt
├── data/
│   ├── raw/                # Chứa file CSV gốc tải từ Kaggle
│   └── processed/          # Chứa dữ liệu sau khi làm sạch
├── src/                    
│   ├── __init__.py
│   ├── config.py           # Lưu các cấu hình (đường dẫn Kaggle, file paths)
│   ├── data_fetcher.py     # Tải dữ liệu tự động từ Kaggle bằng Kaggle API
│   ├── data_processor.py   # Làm sạch, nội suy, tạo thuộc tính (lag, rolling)
│   ├── visualizer.py       # Các hàm vẽ biểu đồ chuyên dụng
│   ├── arima_model.py      # Đóng gói logic train/dự báo ARIMA
│   ├── rf_model.py         # Đóng gói logic train/dự báo Random Forest
│   └── evaluator.py        # Hàm tính MAE, RMSE, R2
├── notebooks/
│   ├── 00_data_download.ipynb      # Kéo dữ liệu từ Kaggle bằng src.data_fetcher
│   ├── 01_data_preprocessing.ipynb # Chỉ gọi hàm từ src.data_processor
│   ├── 02_eda.ipynb                # Gọi hàm từ src.visualizer
│   ├── 03_arima.ipynb              # Gọi hàm từ src.arima_model
│   ├── 04_random_forest.ipynb      # Gọi hàm từ src.rf_model
│   └── 05_model_comparison.ipynb   # Gọi hàm từ src.evaluator
├── figures/                # Lưu biểu đồ xuất ra
├── results/                # Lưu kết quả dạng bảng, log
├── report/
└── slides/
```

## 3. Luồng xử lý dữ liệu (Data Flow)
1. **Tải dữ liệu (00_data_download.ipynb):** 
   - Sử dụng thư viện `kaggle` để tự động kéo dữ liệu từ link `phungdinhdat/aqi-in-hanoi-2022-2025`.
   - Lưu dữ liệu thô vào `data/raw/`.
2. **Tiền xử lý (01_data_preprocessing.ipynb):**
   - Đọc dữ liệu thô.
   - Làm sạch, nội suy dữ liệu thiếu, định dạng thời gian.
   - Lưu dữ liệu đã làm sạch vào `data/processed/clean_data.csv`.
3. **Phân tích khám phá (02_eda.ipynb):**
   - Tải `clean_data.csv`.
   - Vẽ các biểu đồ chuỗi thời gian, boxplot, ACF/PACF. Lưu hình ảnh ra `figures/`.
4. **Mô hình ARIMA (03_arima.ipynb):**
   - Dùng `clean_data.csv` huấn luyện ARIMA (2022-2024), kiểm thử (2025).
   - Lưu kết quả dự báo ra `results/arima_predictions.csv`.
5. **Mô hình Random Forest (04_random_forest.ipynb):**
   - Tạo các features (lag, rolling) từ `clean_data.csv`.
   - Huấn luyện và dự báo RF. Lưu kết quả ra `results/rf_predictions.csv`.
6. **So sánh (05_model_comparison.ipynb):**
   - Đọc kết quả từ thư mục `results/`.
   - Đánh giá MAE, RMSE, R². Trực quan hóa và so sánh.

## 4. Công nghệ
- **Ngôn ngữ:** Python (3.10+).
- **Thư viện chính:** pandas, numpy, matplotlib, seaborn, statsmodels, scikit-learn, kaggle.
- **Môi trường:** Jupyter Notebook / IPython.
