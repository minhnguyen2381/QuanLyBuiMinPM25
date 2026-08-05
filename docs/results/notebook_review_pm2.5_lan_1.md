# 📊 Review Toàn Bộ Kết Quả Notebooks — Dự Báo PM2.5 Hà Nội

## Tổng Quan Dự Án

Dự án dự báo nồng độ bụi mịn PM2.5 tại Hà Nội (2022–2025) sử dụng 2 mô hình: **ARIMA** (chuỗi thời gian) và **Random Forest** (học máy). Pipeline gồm 6 notebooks từ tải dữ liệu → tiền xử lý → EDA → huấn luyện → so sánh.

---

## 1. Pipeline Tổng Thể

| Notebook | Mục đích | Trạng thái |
|:---------|:---------|:----------:|
| [00_data_download.ipynb](file:///d:/DuAn/QuanLyBuiMinPM25/notebooks/00_data_download.ipynb) | Tải dữ liệu từ Kaggle | ✅ |
| [01_data_preprocessing.ipynb](file:///d:/DuAn/QuanLyBuiMinPM25/notebooks/01_data_preprocessing.ipynb) | Tiền xử lý & làm sạch | ✅ |
| [02_eda.ipynb](file:///d:/DuAn/QuanLyBuiMinPM25/notebooks/02_eda.ipynb) | Phân tích khám phá dữ liệu | ✅ |
| [03_arima.ipynb](file:///d:/DuAn/QuanLyBuiMinPM25/notebooks/03_arima.ipynb) | Mô hình ARIMA | ✅ |
| [04_random_forest.ipynb](file:///d:/DuAn/QuanLyBuiMinPM25/notebooks/04_random_forest.ipynb) | Mô hình Random Forest | ✅ |
| [05_model_comparison.ipynb](file:///d:/DuAn/QuanLyBuiMinPM25/notebooks/05_model_comparison.ipynb) | So sánh mô hình | ✅ |

---

## 2. Đánh Giá Chi Tiết Từng Bước

### 2.1. Dữ Liệu (Notebook 00 & 01)

**Dữ liệu thô:**
- Nguồn: Kaggle (`phungdinhdat/aqi-in-hanoi-2022-2025`)
- 4 file CSV (2022–2025), tổng **~30,341 bản ghi theo giờ**
- 19 cột bao gồm: AQI, PM2.5, CO, NO₂, O₃, PM10, SO₂ + các biến khí tượng (nhiệt độ, độ ẩm, gió, mưa, UV...)

**Sau tiền xử lý:**
- Resample hourly → daily (trung bình ngày)
- Kết quả: **1,265 ngày** (13/01/2022 → 30/06/2025)
- Missing: gần như 0% (chỉ nội suy 1 ngày)
- Giá trị âm: 0

**Thống kê PM2.5 sau xử lý:**

| Chỉ số | Giá trị |
|:-------|--------:|
| Mean | 50.77 µg/m³ |
| Std | 32.69 |
| Min | 2.33 |
| Q25 | 28.97 |
| Median | 41.50 |
| Q75 | 62.69 |
| Max | 261.01 |
| Skewness | 1.621 |

> [!IMPORTANT]
> **Vấn đề nghiêm trọng #1 — Lãng phí dữ liệu ngoại sinh:** Dữ liệu thô chứa **7 biến khí tượng** (nhiệt độ, độ ẩm, gió, mưa, áp suất, UV, mây) và **5 chất ô nhiễm** (CO, NO₂, O₃, PM10, SO₂) nhưng bước tiền xử lý **đã loại bỏ hết**, chỉ giữ lại PM2.5. Đây là nguồn thông tin cực kỳ quan trọng cho dự báo mà không được sử dụng.

> [!WARNING]
> **Vấn đề #2 — Không xử lý outlier:** Dữ liệu có Max = 261 µg/m³ và Skewness = 1.621 (lệch phải mạnh). Các đỉnh ô nhiễm mùa đông không được xử lý, ảnh hưởng đến khả năng học pattern của mô hình.

---

### 2.2. EDA (Notebook 02)

**Phát hiện chính:**

![PM2.5 Time Series](file:///d:/DuAn/QuanLyBuiMinPM25/figures/01_time_series.png)

- ✅ **Tính mùa vụ rõ rệt:** PM2.5 cao mùa đông (T11–T2), thấp mùa hè (T6–T8)
- ✅ **PM2.5 trung bình vượt xa tiêu chuẩn WHO** (50.77 vs 15 µg/m³)
- ✅ **ACF/PACF:** Tự tương quan mạnh, PACF cut-off sau lag 1 → phù hợp cho chuỗi thời gian

**Thống kê theo mùa:**

| Mùa | Mean (µg/m³) | Std | Nhận xét |
|:----|:---:|:---:|:---------|
| Đông (T12–T2) | 67.30 | — | Ô nhiễm nặng nhất |
| Thu (T9–T11) | 54.84 | 41.53 | Biến động mạnh nhất |
| Xuân (T3–T5) | 50.98 | — | Trung bình |
| Hè (T6–T8) | 29.71 | 12.08 | Ổn định nhất |

> [!TIP]
> EDA được làm tốt, trực quan hóa đầy đủ. Tuy nhiên thiếu phân tích tương quan giữa PM2.5 với các biến khí tượng (đã bị loại ở bước trước).

---

### 2.3. Mô hình ARIMA (Notebook 03)

**Cấu hình:**
- Kiểm định ADF: p-value = 0.0001 → chuỗi dừng ✅
- Grid search tìm được: **ARIMA(3, 1, 1)** (AIC = 9376.38)
- Train: 1,084 ngày (2022–2024) | Test: 181 ngày (2025 H1)
- Dự báo rolling one-step-ahead

**Kết quả:**

| Metric | Giá trị |
|:-------|--------:|
| MAE | 16.95 |
| RMSE | 22.55 |
| R² | 0.43 |
| Cải thiện vs Naive | **-0.68%** ❌ |

> [!CAUTION]
> **ARIMA kém hơn cả Naive Forecast!** Cải thiện RMSE là **-0.68%** (tức là tệ hơn phương pháp đơn giản nhất: lấy giá trị hôm qua làm dự báo hôm nay). Đây là dấu hiệu cho thấy ARIMA(3,1,1) không phù hợp với dữ liệu này.

**Nguyên nhân:**
1. **Không có thành phần mùa vụ (SARIMA):** Mô hình chỉ là ARIMA thuần, không bắt được chu kỳ mùa vụ rõ rệt trong dữ liệu
2. **Lỗi code trong rolling forecast:** Notebook có cảnh báo `'numpy.ndarray' object has no attribute 'iloc'` → fallback dùng giá trị cuối, ảnh hưởng chất lượng dự báo
3. **Mô hình tuyến tính đơn biến:** Không thể nắm bắt mối quan hệ phi tuyến phức tạp của PM2.5

---

### 2.4. Mô hình Random Forest (Notebook 04)

**Cấu hình:**
- 14 features: 5 lag + 4 rolling + 5 calendar
- RandomizedSearchCV với TimeSeriesSplit (3 folds) ✅
- Tham số tối ưu: `n_estimators=100, max_depth=5, min_samples_leaf=1`
- Train: 1,070 mẫu | Test: 181 mẫu

**Kết quả:**

| Metric | Giá trị |
|:-------|--------:|
| MAE | 15.86 |
| RMSE | 21.24 |
| R² | 0.50 |
| Cải thiện vs Naive | **+5.14%** ✅ |

**Feature Importance:**

![Feature Importance](file:///d:/DuAn/QuanLyBuiMinPM25/figures/09_feature_importance.png)

> [!WARNING]
> **Vấn đề nghiêm trọng #3 — Phụ thuộc quá mức vào `lag_1`:** Feature `lag_1` chiếm **85.91%** importance! Mô hình gần như chỉ sao chép giá trị ngày hôm qua, tương tự Naive Forecast. Điều này giải thích tại sao R² chỉ đạt 0.50 — mô hình không thực sự "học" được pattern sâu.

---

### 2.5. So Sánh Mô Hình (Notebook 05)

![Model Comparison](file:///d:/DuAn/QuanLyBuiMinPM25/figures/11_all_models_comparison.png)

**Bảng tổng hợp từ [`model_comparison.csv`](file:///d:/DuAn/QuanLyBuiMinPM25/results/model_comparison.csv):**

| Mô hình | MAE | RMSE | R² | Cải thiện RMSE |
|:--------|:---:|:----:|:--:|:---:|
| **Naive (Baseline)** | 16.81 | 22.40 | 0.42 | 0% |
| **ARIMA(3,1,1)** | 16.95 | 22.55 | 0.43 | **-0.68%** ❌ |
| **Random Forest** | **15.86** | **21.24** | **0.50** | **+5.14%** ✅ |

![Absolute Errors](file:///d:/DuAn/QuanLyBuiMinPM25/figures/14_absolute_errors.png)

> [!IMPORTANT]
> **Đánh giá tổng thể: Kết quả CHƯA ĐẠT yêu cầu.**
> - R² < 0.5 cho tất cả mô hình → giải thích dưới 50% phương sai
> - Random Forest chỉ cải thiện 5.14% so với Naive → giá trị gia tăng rất thấp
> - ARIMA tệ hơn Naive → mô hình không hữu ích
> - Sai số trung bình ~16–17 µg/m³ trên dữ liệu có mean 50.77 → MAPE ước tính ~30%

---

## 3. Tổng Kết Các Vấn Đề Chính

| # | Vấn đề | Mức độ | Tác động |
|:-:|:-------|:------:|:---------|
| 1 | **Loại bỏ toàn bộ biến ngoại sinh** (khí tượng + ô nhiễm khác) | 🔴 Critical | Mất nguồn thông tin quan trọng nhất cho dự báo |
| 2 | **ARIMA kém hơn Naive** | 🔴 Critical | Mô hình vô dụng, tốn tài nguyên |
| 3 | **RF phụ thuộc 85.9% vào lag_1** | 🟡 High | Mô hình chỉ "copy" ngày hôm qua |
| 4 | **Không dùng SARIMA** (thiếu seasonal component) | 🟡 High | Bỏ lỡ pattern mùa vụ rõ rệt |
| 5 | **Lỗi code trong ARIMA forecast** | 🟡 High | Fallback giá trị, ảnh hưởng metrics |
| 6 | **R² tối đa chỉ 0.50** | 🟡 High | Mô hình giải thích ≤50% biến động |
| 7 | **Phân bố lệch phải mạnh** (skew=1.62) chưa xử lý | 🟠 Medium | Vi phạm giả định mô hình tuyến tính |
| 8 | **Chưa thử các mô hình mạnh hơn** | 🟠 Medium | Chưa khai thác hết tiềm năng |

---

## 4. Phương Hướng Cải Thiện

### 🔴 Ưu tiên 1: Tích hợp biến ngoại sinh (Impact cao nhất)

Dữ liệu thô đã có sẵn các biến cực kỳ hữu ích:

```
Khí tượng: Temperature, Relative Humidity, Wind Speed, Pressure, Precipitation, Clouds
Ô nhiễm:  CO, NO₂, O₃, PM10, SO₂
```

**Hành động:**
1. Sửa `data_processor.py` để giữ lại các cột khí tượng khi resample
2. Thêm các biến này làm features cho Random Forest
3. Thử SARIMAX (ARIMA + biến ngoại sinh)

> Nghiên cứu cho thấy nhiệt độ, độ ẩm, tốc độ gió là 3 yếu tố ảnh hưởng mạnh nhất đến PM2.5 tại Hà Nội. Riêng việc thêm 3 biến này có thể nâng R² lên 0.65–0.75.

---

### 🟡 Ưu tiên 2: Cải thiện mô hình hiện tại

#### A. Sửa ARIMA → SARIMA
```python
# Thay vì ARIMA(3,1,1), dùng SARIMA với mùa vụ:
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Option 1: Seasonal weekly (s=7)
model = SARIMAX(train, order=(3,1,1), seasonal_order=(1,1,1,7))

# Option 2: Nếu resample monthly → Seasonal yearly (s=12) 
model = SARIMAX(train_monthly, order=(1,1,1), seasonal_order=(1,1,1,12))
```

#### B. Sửa lỗi code ARIMA forecast
- Fix lỗi `'numpy.ndarray' has no attribute 'iloc'` trong hàm `forecast_arima()`
- Đảm bảo rolling forecast hoạt động đúng ở mọi bước

#### C. Giảm phụ thuộc lag_1 cho Random Forest
- Thử **loại bỏ lag_1** hoặc giảm trọng số → buộc mô hình học pattern phức tạp hơn
- Thêm features mới: `lag_1_diff` (biến thiên ngày), `is_weekend`, `is_holiday`
- Thử biến đổi log/sqrt cho target variable để giảm skewness

---

### 🟠 Ưu tiên 3: Thử các mô hình mạnh hơn

| Mô hình | Ưu điểm | Khả năng cải thiện |
|:--------|:--------|:------------------:|
| **XGBoost / LightGBM** | Gradient boosting, xử lý phi tuyến tốt | ⭐⭐⭐⭐ |
| **Prophet (Facebook)** | Tự động bắt mùa vụ, holiday effects | ⭐⭐⭐ |
| **LSTM / GRU** | Deep learning cho chuỗi thời gian | ⭐⭐⭐⭐ |
| **SARIMAX** | ARIMA + seasonal + exogenous variables | ⭐⭐⭐ |
| **Ensemble** | Kết hợp RF + XGBoost + ARIMA | ⭐⭐⭐⭐⭐ |

---

### 🟢 Ưu tiên 4: Cải thiện quy trình & chất lượng

1. **Cross-validation cho chuỗi thời gian:** Sử dụng `TimeSeriesSplit` với nhiều folds hơn (5–10)
2. **Metrics bổ sung:** Thêm MAPE, MAE by season, Directional Accuracy (% dự đoán đúng xu hướng tăng/giảm)
3. **Log transform:** Thử `np.log1p(pm25)` để giảm skewness trước khi fit mô hình
4. **Confidence intervals:** Thêm khoảng tin cậy cho dự báo
5. **Feature selection:** Dùng Recursive Feature Elimination (RFE) thay vì chọn thủ công

---

## 5. Lộ Trình Đề Xuất

```mermaid
graph LR
    A["Phase 1<br/>Sửa lỗi + Tích hợp<br/>biến ngoại sinh"] --> B["Phase 2<br/>SARIMA/SARIMAX +<br/>RF cải tiến"]
    B --> C["Phase 3<br/>XGBoost/LightGBM +<br/>Prophet"]
    C --> D["Phase 4<br/>LSTM/GRU +<br/>Ensemble"]
    
    style A fill:#ff6b6b,color:#fff
    style B fill:#ffa502,color:#fff
    style C fill:#2ed573,color:#fff
    style D fill:#1e90ff,color:#fff
```

| Phase | Mục tiêu R² | Thời gian ước tính |
|:------|:---:|:---:|
| Phase 1: Fix bugs + exogenous vars | 0.60–0.70 | 1–2 ngày |
| Phase 2: SARIMA + RF tuning | 0.70–0.80 | 1–2 ngày |
| Phase 3: Gradient Boosting + Prophet | 0.80–0.85 | 2–3 ngày |
| Phase 4: Deep Learning + Ensemble | 0.85+ | 3–5 ngày |

---

> [!NOTE]
> **Tóm lại:** Pipeline hiện tại hoạt động đúng về mặt kỹ thuật nhưng kết quả dự báo chưa đạt yêu cầu (R² ≤ 0.50). Nguyên nhân chính là **lãng phí dữ liệu ngoại sinh** và **lựa chọn mô hình chưa tối ưu**. Với dữ liệu có sẵn, hoàn toàn có thể đạt R² > 0.75 nếu tích hợp biến khí tượng và sử dụng mô hình phù hợp hơn.
