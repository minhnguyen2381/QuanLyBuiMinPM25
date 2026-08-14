# Kiến Trúc Nghiên Cứu Mới Cho Đề Tài PM2.5 Hà Nội

Tái cấu trúc này giữ đúng đề tài: **nghiên cứu dự báo nồng độ bụi mịn PM2.5 tại Hà Nội bằng ARIMA và Random Forest**. Điểm nâng cấp nằm ở cách tổ chức hệ thống, thiết kế thực nghiệm, quản trị dữ liệu, khả năng tái lập và cách trình bày kết quả.

## 1. Các Lớp Chức Năng

| Lớp | Thư mục | Vai trò |
| --- | --- | --- |
| Cấu hình | `configs/` | Tách tham số dữ liệu, ARIMA, Random Forest và thực nghiệm ra khỏi mã nguồn |
| Dữ liệu | `src/data/` | Đọc raw CSV, chuẩn hóa cột, giữ biến ngoại sinh, tổng hợp theo ngày, báo cáo chất lượng |
| Mô hình | `src/models/` | Cài đặt baseline, ARIMA và Random Forest |
| Đánh giá | `src/evaluation/` | Tính metric mở rộng và phân tích sai số |
| Thực nghiệm | `src/experiments/` | Chuẩn bị walk-forward split và ablation study |
| Báo cáo | `src/reporting/` | Sinh bảng thống kê, bảng sai số và biểu đồ phục vụ tiểu luận |
| Pipeline | `src/pipeline.py` | Điều phối toàn bộ quy trình và lưu artifact theo `experiment_id` |

## 2. Điểm Nâng Cấp Học Thuật

- Dữ liệu sạch mới không chỉ giữ `PM2.5`, mà giữ thêm các biến ngoại sinh như `Temperature`, `Relative Humidity`, `Wind Speed`, `Pressure`, `PM10`, `NO2`, `CO`, `O3`.
- Random Forest được huấn luyện trên đặc trưng trễ, rolling, lịch thời gian, đặc trưng chu kỳ và biến ngoại sinh đã dịch về quá khứ để tránh rò rỉ dữ liệu tương lai.
- ARIMA có kiểm định ADF và grid-search `p,d,q` theo AIC/BIC trên tập huấn luyện.
- So sánh mô hình có thêm **mô hình tham chiếu (Naive)** và **tham chiếu mùa vụ 7 ngày** để chứng minh ARIMA/RF có giá trị hơn mốc tham chiếu đơn giản.
- Metric mở rộng gồm `MAE`, `RMSE`, `MAPE`, `SMAPE`, `R2`, `DirectionalAccuracy`.
- Mỗi lần chạy tạo một thư mục trong `results/experiments/<experiment_id>/`, lưu toàn bộ bảng, dự báo, biểu đồ và kết quả phân tích sai số.

## 3. Bảng Kết Quả Được Sinh Tự Động

Các bảng bổ sung nằm trong `tables/`:

- `thong_ke_mo_ta.csv`: thống kê mô tả cho toàn bộ biến sau tiền xử lý.
- `du_lieu_thieu_sau_tien_xu_ly.csv`: dữ liệu thiếu theo từng biến.
- `tuong_quan_pm25_bien_ngoai_sinh.csv`: tương quan giữa PM2.5 và các biến ngoại sinh.
- `so_ngay_vuot_nguong_tham_khao.csv`: số ngày vượt các ngưỡng PM2.5 tham khảo.
- `thong_ke_pm25_theo_monthly.csv`: PM2.5 theo tháng.
- `thong_ke_pm25_theo_seasonal.csv`: PM2.5 theo mùa.
- `thong_ke_pm25_theo_yearly.csv`: PM2.5 theo năm.
- `chi_tiet_sai_so_theo_ngay.csv`: sai số dự báo theo ngày của từng mô hình.

## 4. Biểu Đồ Được Sinh Tự Động

Các biểu đồ bổ sung nằm trong `figures/`:

- Diễn biến PM2.5 toàn giai đoạn.
- Phân phối PM2.5.
- Boxplot PM2.5 theo tháng.
- PM2.5 trung bình theo tháng qua các năm.
- Heatmap tương quan giữa các biến.
- Đặc trưng quan trọng của Random Forest.
- RMSE theo tháng của các mô hình.
- Phân phối sai số dự báo.
- Scatter giữa PM2.5 thực tế và PM2.5 dự báo.

## 5. Cách Chạy

```bash
pip install -r requirements.txt
python main.py
```

Kết quả mới nằm trong:

```text
results/experiments/<experiment_id>/
```

## 6. Hướng Phát Triển Tiếp

- Thêm Diebold-Mariano test để kiểm định khác biệt sai số giữa ARIMA và Random Forest.
- Thêm permutation importance để giải thích Random Forest tốt hơn impurity importance.
- Thêm SARIMAX như phần mở rộng của ARIMA khi muốn dùng biến ngoại sinh trong mô hình thống kê.
- Tạo notebook tổng hợp kết quả từ artifact thay vì tính lại thủ công.
