# Dự Báo PM2.5 Tại Hà Nội Bằng ARIMA Và Random Forest

Dự án nghiên cứu dự báo nồng độ bụi mịn PM2.5 tại Hà Nội bằng hai nhóm phương pháp chính:

- **ARIMA**: đại diện cho mô hình thống kê chuỗi thời gian.
- **Random Forest Regression**: đại diện cho mô hình học máy sử dụng đặc trưng trễ, rolling, lịch thời gian và biến ngoại sinh.

Phiên bản hiện tại đã được tái cấu trúc theo hướng phù hợp hơn với tiểu luận cao học ngành Hệ thống thông tin: có cấu hình riêng, pipeline tái lập, thống kê mô tả, đánh giá mô hình, phân tích sai số và nhiều biểu đồ phục vụ báo cáo.

## Cấu Trúc Chính

```text
configs/                  Cấu hình dữ liệu, ARIMA, Random Forest, thực nghiệm
data/raw/                 Dữ liệu gốc giai đoạn 2022-2025
data/processed/           Dữ liệu sạch đa biến sau tiền xử lý
src/config_loader.py      Đọc cấu hình YAML
src/data/                 Đọc dữ liệu, tiền xử lý, kiểm tra chất lượng, tạo đặc trưng
src/models/               Baseline, ARIMA, Random Forest
src/evaluation/           Chỉ số đánh giá và phân tích sai số
src/experiments/          Hỗ trợ walk-forward và ablation study
src/reporting/            Sinh bảng thống kê và biểu đồ
src/pipeline.py           Pipeline nghiên cứu end-to-end
tests/                    Test thành phần
results/experiments/      Kết quả từng lần chạy
```

## Cài Đặt

```powershell
cd D:\caohocday\QuanLyBuiMinPM25
pip install -r requirements.txt
```

## Chạy Dự Án

```powershell
python main.py
```

Mỗi lần chạy sẽ tạo một thư mục kết quả mới:

```text
results/experiments/<experiment_id>/
```

## Các Kết Quả Chính

Các bảng nằm trực tiếp trong thư mục thực nghiệm:

- `model_comparison.csv`: so sánh mô hình tham chiếu (Naive), tham chiếu mùa vụ 7 ngày, ARIMA và Random Forest.
- `arima_order_grid.csv`: kết quả chọn tham số ARIMA theo AIC/BIC.
- `arima_adf_test.csv`: kiểm định tính dừng của chuỗi huấn luyện.
- `random_forest_cv_results.csv`: kết quả tìm kiếm tham số Random Forest bằng TimeSeriesSplit.
- `random_forest_feature_importance.csv`: mức độ quan trọng của đặc trưng.
- `monthly_error_arima.csv`: sai số ARIMA theo tháng.
- `monthly_error_random_forest.csv`: sai số Random Forest theo tháng.
- `top_errors_arima.csv`: các ngày ARIMA dự báo sai nhiều nhất.
- `top_errors_random_forest.csv`: các ngày Random Forest dự báo sai nhiều nhất.

Các bảng thống kê bổ sung nằm trong:

```text
results/experiments/<experiment_id>/tables/
```

Bao gồm:

- `thong_ke_mo_ta.csv`: thống kê mô tả toàn bộ biến sau tiền xử lý.
- `du_lieu_thieu_sau_tien_xu_ly.csv`: tỷ lệ dữ liệu thiếu theo biến.
- `tuong_quan_pm25_bien_ngoai_sinh.csv`: tương quan giữa PM2.5 và các biến ngoại sinh.
- `so_ngay_vuot_nguong_tham_khao.csv`: số ngày vượt các ngưỡng PM2.5 tham khảo.
- `thong_ke_pm25_theo_monthly.csv`: thống kê PM2.5 theo tháng.
- `thong_ke_pm25_theo_seasonal.csv`: thống kê PM2.5 theo mùa.
- `thong_ke_pm25_theo_yearly.csv`: thống kê PM2.5 theo năm.
- `thong_ke_pm25_theo_month_year.csv`: thống kê PM2.5 theo từng cặp năm-tháng.
- `chi_tiet_sai_so_theo_ngay.csv`: sai số dự báo theo ngày của từng mô hình.

Các biểu đồ mới nằm trong:

```text
results/experiments/<experiment_id>/figures/
```

Bao gồm:

- `01_dien_bien_pm25.png`: diễn biến PM2.5 toàn giai đoạn.
- `02_phan_phoi_pm25.png`: phân phối PM2.5.
- `03_boxplot_pm25_theo_thang.png`: boxplot PM2.5 theo tháng.
- `04_trung_binh_pm25_theo_thang_nam.png`: PM2.5 trung bình theo tháng qua các năm.
- `05_heatmap_tuong_quan.png`: ma trận tương quan các biến.
- `06_dac_trung_quan_trong_random_forest.png`: đặc trưng quan trọng của Random Forest.
- `07_rmse_theo_thang.png`: RMSE theo tháng của các mô hình.
- `08_phan_phoi_sai_so_du_bao.png`: phân phối sai số dự báo.
- `09_thuc_te_va_du_bao_scatter.png`: scatter thực tế - dự báo.

Ngoài ra, biểu đồ tổng hợp chính vẫn có ở:

```text
results/experiments/<experiment_id>/forecast_comparison.png
```

## Ghi Chú Phương Pháp

Random Forest được thiết kế để tránh rò rỉ dữ liệu tương lai:

- Đặc trưng trễ PM2.5 dùng `shift`.
- Đặc trưng rolling dùng dữ liệu trước ngày dự báo.
- Biến ngoại sinh như `Temperature`, `Relative Humidity`, `Wind Speed`, `Pressure`, `PM10`, `NO2`, `CO`, `O3` cũng được dịch về quá khứ trước khi đưa vào mô hình.
- Tập huấn luyện và kiểm thử được chia theo thời gian: huấn luyện đến năm 2024, kiểm thử từ năm 2025.

## Kiểm Tra Nhanh

```powershell
python -m compileall main.py src tests
python -m pytest -q
```

Nếu `pytest` chưa có trong môi trường hiện tại, cài lại thư viện:

```powershell
pip install -r requirements.txt
```
