# Prompt dành cho Codex — Chương 2

Bạn là một **chuyên gia Phân tích dữ liệu và Machine Learning ở trình độ cao học**, đồng thời là người hỗ trợ xây dựng báo cáo bài tập lớn cho học viên cao học ngành **Hệ thống Thông tin**.

Tôi đang thực hiện đề tài:

> **"Nghiên cứu dự báo nồng độ bụi mịn PM2.5 tại Hà Nội bằng phương pháp ARIMA và Random Forest"**

Môn học: **Phân tích dữ liệu**

Nguồn dữ liệu chính:

> https://www.kaggle.com/datasets/nitirajkulkarni/hanoi-vn-1581130

Nguồn tương ứng cần đối chiếu khi cần:

> https://zenodo.org/records/18673906

Chương này (**Chương 2 — Nghiên cứu liên quan và Cơ sở lý luận**) là chương bản lề giữa Chương 1 (Tổng quan) và Chương 3 (Thực nghiệm). Chương 2 **không chứa kết quả thực nghiệm**, không có số liệu tính từ dataset — mọi nội dung ở đây mang tính lý thuyết, tổng quan tài liệu, và thiết kế phương pháp luận sẽ được áp dụng ở Chương 3.

---

## 1. Nguyên tắc bắt buộc (áp dụng cho toàn bộ Chương 2)

### Nguyên tắc chống hallucination

1. **Không được bịa đặt tên tác giả, tên bài báo, năm xuất bản, tạp chí/hội nghị, hoặc kết quả của nghiên cứu liên quan.** Nếu không thể xác minh một nghiên cứu cụ thể, không được trích dẫn nó như thể có thật.
2. Nếu Codex không có khả năng tra cứu web trong phiên làm việc, phải nêu rõ: `CẦN TRA CỨU/XÁC MINH TRÍCH DẪN` thay vì tự tạo ra citation giả (fake reference). Tuyệt đối không "ảo giác" DOI, số trang, hay tên tạp chí.
3. Có thể trình bày các **hướng nghiên cứu điển hình** (ví dụ: "nhiều nghiên cứu ứng dụng ARIMA cho dự báo chất lượng không khí đô thị") ở mức khái quát, nhưng phải phân biệt rõ giữa:
   - phát biểu tổng quát về xu hướng nghiên cứu (chấp nhận được nếu diễn đạt thận trọng);
   - trích dẫn cụ thể một công trình với tác giả/năm cụ thể (chỉ được viết khi có nguồn xác thực).
4. Không được tự giả định dataset PM2.5 Hà Nội đang dùng có đặc điểm giống hệt các nghiên cứu khác đã dẫn ra — chỉ so sánh về mặt phương pháp luận, không so sánh về mặt số liệu vì số liệu thực tế của đề tài này chưa được phân tích (sẽ nằm ở Chương 3).
5. Mọi công thức toán học (ARIMA, Random Forest, các chỉ số đánh giá) phải đúng theo tài liệu học thuật chuẩn (Box–Jenkins, Breiman 2001, tài liệu Statsmodels, tài liệu scikit-learn). Nếu không chắc chắn về một công thức, ghi rõ `CẦN KIỂM TRA LẠI CÔNG THỨC` thay vì suy diễn.
6. Không tuyên bố trước ARIMA hay Random Forest "phù hợp hơn" cho bài toán này — Chương 2 chỉ trình bày cơ sở lý luận và lý do lựa chọn hai phương pháp để nghiên cứu, không kết luận phương pháp nào tốt hơn (kết luận đó thuộc Chương 3, dựa trên thực nghiệm).
7. Toàn bộ quy trình, sơ đồ, checklist ở Chương 2 phải **nhất quán với những gì sẽ thực sự được thực hiện ở Chương 3** — không thiết kế quy trình lý thuyết rồi Chương 3 làm khác đi.

---

## 2. Cấu trúc bắt buộc của Chương 2

### 2.1. Tổng quan PM2.5 và bài toán dự báo

Yêu cầu trình bày (ở mức khái quát, học thuật, không lặp lại nguyên văn nội dung đã có ở mục 1.1 Chương 1 mà đào sâu hơn dưới góc nhìn chuẩn bị cho bài toán mô hình hóa):

- Khái niệm PM2.5: định nghĩa, kích thước hạt, nguồn phát sinh (giao thông, công nghiệp, đốt sinh khối, khí hậu/thời tiết...), tác động đến sức khỏe và môi trường đô thị.
- Đặc điểm biến động của PM2.5 theo thời gian: tính chu kỳ (theo giờ trong ngày, theo mùa), ảnh hưởng của yếu tố khí tượng (nhiệt độ, độ ẩm, tốc độ gió, áp suất...), tính không dừng (non-stationarity) thường gặp trong chuỗi quan trắc môi trường.
- Vì sao PM2.5 phù hợp để đóng khung thành **bài toán dự báo chuỗi thời gian (time-series forecasting)**: dữ liệu được quan trắc liên tục theo mốc thời gian, có tính tự tương quan (autocorrelation), giá trị hiện tại chịu ảnh hưởng bởi các giá trị/điều kiện trong quá khứ gần.
- Phân biệt hai cách tiếp cận bài toán dự báo sẽ được nghiên cứu trong đề tài:
  - Tiếp cận thống kê chuỗi thời gian cổ điển (ARIMA) — mô hình hóa trực tiếp cấu trúc tự tương quan của chuỗi.
  - Tiếp cận Machine Learning (Random Forest) — mô hình hóa bài toán dự báo như một bài toán học có giám sát (supervised learning) sau khi biến đổi dữ liệu.
- Nêu rõ đây là bài toán **dự báo ngắn hạn, dựa trên dữ liệu lịch sử** (không phải bài toán phân loại nguồn ô nhiễm hay mô hình hóa lan truyền không khí theo không gian), nhằm giới hạn phạm vi lý thuyết đúng với những gì sẽ thực nghiệm ở Chương 3.
- Không đưa số liệu cụ thể về PM2.5 tại Hà Nội trong dataset (mean, max, xu hướng...) ở mục này — những con số đó chỉ được trình bày ở Chương 3 sau khi đã phân tích dữ liệu thật. Mục này chỉ mang tính khái niệm/nền tảng.

### 2.2. Tổng quan các nghiên cứu liên quan (Related Work)

Yêu cầu:

- Liệt kê các **nhóm hướng nghiên cứu** liên quan đến đề tài, tối thiểu bao gồm:
  1. Các nghiên cứu dự báo chất lượng không khí / PM2.5 bằng mô hình thống kê chuỗi thời gian cổ điển (ARIMA, SARIMA, các biến thể).
  2. Các nghiên cứu dự báo PM2.5 bằng phương pháp Machine Learning (Random Forest, Gradient Boosting, SVR...).
  3. Các nghiên cứu so sánh trực tiếp giữa mô hình thống kê và mô hình Machine Learning cho bài toán dự báo chuỗi thời gian môi trường.
  4. (Nếu có nguồn xác thực) Các nghiên cứu cụ thể về ô nhiễm không khí / PM2.5 tại Hà Nội hoặc Việt Nam.
- Với mỗi công trình được trích dẫn cụ thể, trình bày theo khung:

  | Tác giả (năm) | Phương pháp | Dữ liệu/khu vực | Kết quả chính | Hạn chế được ghi nhận |
  |---|---|---|---|---|

- Nếu Codex có công cụ tra cứu (web search), **phải thực sự tra cứu và trích dẫn nguồn có thể kiểm chứng** (link, DOI, hoặc tên ấn phẩm rõ ràng); nếu không có công cụ tra cứu, để trống ô kết quả với ghi chú `CẦN TRA CỨU/XÁC MINH TRÍCH DẪN` và liệt kê từ khóa tìm kiếm gợi ý (ví dụ: "ARIMA PM2.5 forecasting urban", "Random Forest air quality prediction Southeast Asia", "PM2.5 Hanoi machine learning").
- Kết thúc mục này bằng một đoạn tổng hợp (research gap): chỉ ra khoảng trống mà đề tài hiện tại hướng tới lấp đầy (ví dụ: so sánh trực tiếp ARIMA và Random Forest trên cùng một tập dữ liệu PM2.5 Hà Nội với thiết kế kiểm soát rò rỉ dữ liệu chặt chẽ).

### 2.3. Cơ sở lý luận về ARIMA

Trình bày đầy đủ và chính xác về mặt học thuật:

- Khái niệm chuỗi thời gian (time series), thành phần: trend, seasonality, residual/noise.
- Tính dừng (stationarity): định nghĩa, ý nghĩa, kiểm định (ADF, có thể đề cập KPSS như một phương pháp bổ sung).
- Toán tử sai phân (differencing) và bậc `d`.
- Thành phần AR(p): hồi quy trên giá trị quá khứ của chính chuỗi.
- Thành phần MA(q): mô hình hóa sai số dự báo quá khứ.
- Mô hình ARIMA(p,d,q) tổng quát, công thức toán học.
- ACF và PACF: vai trò trong việc nhận diện p, q.
- Tiêu chí lựa chọn mô hình: AIC, BIC.
- Kiểm tra phần dư (residual diagnostics): tính ngẫu nhiên, kiểm định Ljung-Box.
- Ưu điểm: diễn giải được, phù hợp với chuỗi có cấu trúc tuyến tính/tự tương quan rõ ràng.
- Hạn chế: giả định tuyến tính, khó nắm bắt quan hệ phi tuyến hoặc phụ thuộc vào nhiều biến ngoại sinh phức tạp (trừ khi mở rộng sang ARIMAX/SARIMAX).

Nguồn tham khảo kỹ thuật có thể dùng để đối chiếu công thức:
https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMA.html

### 2.4. Cơ sở lý luận về Random Forest

Trình bày đầy đủ và chính xác về mặt học thuật:

- Decision Tree hồi quy: cơ chế phân chia (splitting), tiêu chí giảm phương sai (variance reduction).
- Nhược điểm của một cây đơn: dễ overfitting, phương sai cao.
- Ensemble learning và bagging (bootstrap aggregating).
- Cơ chế Random Forest: bootstrap sample, random feature subset tại mỗi lần split, trung bình hóa (averaging) kết quả các cây.
- Vai trò của các siêu tham số chính: `n_estimators`, `max_depth`, `min_samples_split`, `min_samples_leaf`, `max_features`.
- Khái niệm feature importance (Gini importance / mean decrease in impurity) và giới hạn diễn giải của nó (không phải quan hệ nhân quả).
- Ưu điểm: nắm bắt quan hệ phi tuyến, tương tác giữa biến, không đòi hỏi giả định phân phối.
- Hạn chế quan trọng đối với bài toán chuỗi thời gian: **Random Forest không có khái niệm thứ tự thời gian nội tại** — mô hình chỉ học từ các đặc trưng (features) được cung cấp, do đó bắt buộc phải biến đổi chuỗi thời gian thành bài toán supervised learning thông qua lag features/rolling features/calendar features (chi tiết ở mục 2.6).

Nguồn tham khảo kỹ thuật:
https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html

Có thể trích dẫn công trình gốc Breiman, L. (2001). *Random Forests*. Machine Learning — chỉ trích dẫn nếu chắc chắn về thông tin, nếu không ghi `CẦN XÁC MINH`.

### 2.5. Quy trình phân tích dữ liệu (Data Analysis Pipeline)

Trình bày sơ đồ quy trình tổng quát sẽ được áp dụng trong Chương 3, dưới dạng các bước tuần tự:

> Data Acquisition → Data Understanding → Data Cleaning → EDA → Time-Series Analysis (stationarity, ACF/PACF) → Feature Engineering → Time-Based Split (Train/Validation/Test) → Modeling (ARIMA, Random Forest) → Hyperparameter Tuning → Evaluation → Error Analysis → Interpretation → Conclusion

Với mỗi bước, giải thích ngắn gọn:
- mục tiêu của bước;
- đầu vào/đầu ra;
- vì sao bước đó cần thiết trong bối cảnh dự báo chuỗi thời gian (khác với bài toán học máy thông thường có thể shuffle dữ liệu tự do).

Nhấn mạnh nguyên tắc xuyên suốt: **toàn bộ pipeline phải tôn trọng thứ tự thời gian (temporal order)**, không có bước nào được phép sử dụng thông tin tương lai để xử lý hoặc quyết định cho dữ liệu quá khứ.

### 2.6. Biểu diễn dữ liệu và tạo đặc trưng cho mô hình

Trình bày về mặt lý thuyết (chưa áp dụng số liệu thực tế):

- **Đối với ARIMA**: dữ liệu được biểu diễn trực tiếp dưới dạng chuỗi thời gian đơn biến (hoặc đa biến nếu mở rộng ARIMAX) theo đúng tần suất quan sát gốc; không cần feature engineering dạng bảng.
- **Đối với Random Forest**: cần chuyển bài toán chuỗi thời gian thành bài toán học có giám sát (supervised learning), bao gồm:
  - **Lag features**: `lag_1, lag_2, ..., lag_k` — giá trị PM2.5 tại các thời điểm trước đó; số lượng lag phải được xác định dựa trên phân tích ACF/PACF và đặc điểm tần suất dữ liệu thực tế (sẽ chốt ở Chương 3, không hard-code trước ở đây).
  - **Rolling features**: rolling mean, rolling std, rolling min, rolling max — tất cả phải được tính chỉ dựa trên dữ liệu quá khứ (shift trước khi rolling) để tránh rò rỉ dữ liệu.
  - **Calendar features**: giờ, thứ trong tuần, tháng, mùa — chỉ sử dụng nếu phù hợp với tần suất dữ liệu thực tế; có thể cân nhắc cyclical encoding (sin/cos) cho các biến có tính chu kỳ.
  - **Biến ngoại sinh** (nếu dataset có, ví dụ: nhiệt độ, độ ẩm, tốc độ gió...): chỉ đưa vào như đặc trưng nếu xác nhận được là biến đo tại thời điểm dự báo hợp lệ (không phải biến được tính ngược từ chính PM2.5, tránh leakage — xem mục 2.6).
- Trình bày một bảng tổng hợp loại đặc trưng dự kiến sử dụng cho Random Forest:

  | Nhóm đặc trưng | Ví dụ | Mục đích | Rủi ro cần kiểm soát |
  |---|---|---|---|

  (Bảng này ở mức thiết kế lý thuyết; danh sách đặc trưng cụ thể cuối cùng sẽ được xác nhận ở Chương 3 sau khi đã đọc dữ liệu thật.)

### 2.7. Các chỉ số đánh giá mô hình (Evaluation Metrics)

Trình bày cơ sở lý thuyết của các chỉ số sẽ dùng ở Chương 3:

- **MAE (Mean Absolute Error)**: công thức, ý nghĩa, đơn vị giống biến gốc, ít nhạy với outlier hơn RMSE.
- **RMSE (Root Mean Squared Error)**: công thức, phạt nặng hơn các sai số lớn, cùng đơn vị với biến gốc.
- **R² (Hệ số xác định)**: công thức, ý nghĩa tỷ lệ phương sai được giải thích, giới hạn diễn giải với dữ liệu chuỗi thời gian (R² cao không nhất thiết đồng nghĩa mô hình tốt cho forecasting).
- Có thể đề cập thêm (tùy chọn, nếu phù hợp): MAPE và hạn chế của nó khi giá trị thực tế gần 0.
- Giải thích vì sao cần dùng **nhiều chỉ số đồng thời** thay vì chỉ một chỉ số duy nhất, và vì sao việc so sánh mô hình phải đi kèm phân tích sai số theo thời gian (error analysis), không chỉ dựa vào bảng số tổng hợp.
- Không đưa bất kỳ con số cụ thể nào ở chương này — các giá trị MAE/RMSE/R² thực tế chỉ xuất hiện ở Chương 3 sau khi có kết quả thực nghiệm.

### 2.8. Kiểm soát rò rỉ dữ liệu (Data Leakage) và khả năng tái lập (Reproducibility)

#### Kiểm soát rò rỉ dữ liệu

Trình bày về mặt lý thuyết các dạng rò rỉ dữ liệu thường gặp trong bài toán dự báo chuỗi thời gian và nguyên tắc phòng tránh tương ứng:

| Loại rò rỉ | Mô tả | Nguyên tắc phòng tránh |
|---|---|---|
| Temporal leakage | Dùng dữ liệu tương lai để dự báo quá khứ/hiện tại | Không shuffle dữ liệu; luôn tôn trọng thứ tự thời gian khi chia tập và tạo đặc trưng |
| Feature leakage | Đặc trưng được tính từ chính biến mục tiêu theo cách không hợp lệ | Rolling/lag features phải shift về quá khứ; loại các biến được tính trực tiếp từ PM2.5 (ví dụ AQI nếu suy ra từ PM2.5) |
| Preprocessing leakage | Chuẩn hóa/impute dựa trên thống kê của toàn bộ dataset (bao gồm cả test) | Mọi thống kê dùng để xử lý (mean, std, giá trị điền khuyết...) chỉ được tính trên tập train |
| Model selection leakage | Dùng tập test để chọn hyperparameter hoặc mô hình | Chỉ dùng train/validation cho việc tuning; test chỉ dùng một lần cuối cùng để đánh giá |

#### Khả năng tái lập (Reproducibility)

Trình bày các nguyên tắc sẽ áp dụng ở Chương 3:
- Cố định random seed cho các thành phần có yếu tố ngẫu nhiên (ví dụ Random Forest).
- Ghi lại đầy đủ phiên bản thư viện sử dụng (pandas, numpy, statsmodels, scikit-learn, matplotlib, seaborn).
- Ghi lại rõ cấu hình chia tập dữ liệu (tỷ lệ hoặc mốc thời gian train/validation/test).
- Lưu lại toàn bộ mã nguồn theo cấu trúc module hóa để có thể chạy lại từ đầu ra kết quả giống nhau (ngoại trừ các sai lệch do phần cứng/phiên bản thư viện nếu có).
- Không hard-code bất kỳ kết quả nào; mọi số liệu trong báo cáo phải sinh ra được từ việc chạy lại code.

### 2.9. Cấu hình thực nghiệm dự kiến (Experimental Configuration)

Trình bày ở mức **thiết kế dự kiến** (sẽ được xác nhận/điều chỉnh dựa trên dữ liệu thật ở Chương 3), bao gồm:

- Môi trường: phiên bản Python, các thư viện chính (pandas, numpy, matplotlib, seaborn, statsmodels, scikit-learn) và vai trò của từng thư viện.
- Chiến lược chia dữ liệu: Train → Validation → Test theo thứ tự thời gian, có thể tham khảo tỷ lệ khởi điểm khoảng 70/15/15 nhưng nêu rõ đây chỉ là điểm khởi đầu, không phải quy tắc cố định; có thể sử dụng `TimeSeriesSplit` cho việc tuning.

  Nguồn: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

- Chiến lược lựa chọn tham số ARIMA: dựa trên ACF/PACF + so sánh AIC/BIC + đánh giá trên validation, không hard-code (p,d,q).
- Chiến lược tuning Random Forest: phạm vi tìm kiếm hợp lý cho `n_estimators`, `max_depth`, `min_samples_split`, `min_samples_leaf`, `max_features`, sử dụng validation hoặc `TimeSeriesSplit`, tuyệt đối không dùng test set để tuning.
- Toàn bộ mục này phải nhất quán với phần "Chia dữ liệu", "Mô hình ARIMA", "Mô hình Random Forest" đã thiết kế trong prompt Chương 3.

---

## 3. Checklist kiểm soát chất lượng phân tích (Chương 2 phải trình bày checklist này như một công cụ sẽ dùng xuyên suốt đề tài)

Trình bày checklist dưới dạng bảng, mỗi bước gồm: **Nội dung kiểm soát** và **Tiêu chí đạt**. Checklist bắt buộc bao gồm đúng các bước sau, theo thứ tự:

| # | Bước | Nội dung kiểm soát | Tiêu chí đạt |
|---|---|---|---|
| 1 | Dữ liệu gốc | Đã đọc trực tiếp file dữ liệu thật, kiểm tra shape, columns, dtypes, khoảng thời gian, tần suất | Không có thông tin nào về dataset được suy đoán mà chưa kiểm tra |
| 2 | Tiền xử lý dữ liệu | Chuẩn hóa timestamp, sắp xếp theo thời gian, kiểm tra duplicate, kiểm tra outlier | Có ghi nhận rõ ràng các bước và lý do lựa chọn phương pháp xử lý |
| 3 | Điền dữ liệu thiếu | Phân tích số lượng/tỷ lệ/pattern missing trước khi chọn chiến lược điền khuyết | Chiến lược điền khuyết được giải thích, không áp dụng máy móc |
| 4 | Xử lý rò rỉ dữ liệu | Rà soát lag/rolling/calendar features, kiểm tra biến ngoại sinh có bị tính từ target hay không | Không có đặc trưng nào chứa thông tin từ tương lai hoặc suy ra trực tiếp từ target theo cách không hợp lệ |
| 5 | Chia tập dữ liệu train/test | Chia theo thứ tự thời gian, không shuffle, ghi rõ mốc/ tỷ lệ chia | Train/Validation/Test tách biệt hoàn toàn theo thời gian, có biểu đồ minh họa |
| 6 | ARIMA | Kiểm định stationarity, xác định d, dùng ACF/PACF, so sánh AIC/BIC, kiểm tra residual | Tham số (p,d,q) được lựa chọn có căn cứ, residual được chẩn đoán |
| 7 | Random Forest | Xây dựng feature từ quá khứ, tuning trên validation/TimeSeriesSplit, không dùng test để tuning | Hyperparameter được lựa chọn có căn cứ, không có leakage trong feature |
| 8 | Đánh giá | Tính MAE, RMSE, R² trên test; phân tích sai số theo thời gian | Kết quả đi kèm phân tích, không chỉ là bảng số |
| 9 | Báo cáo | Trình bày đầy đủ bảng/biểu đồ/nhận xét, không phóng đại kết luận, ghi rõ hạn chế | Mọi số liệu trong báo cáo truy vết được về code/dataset thực tế |

Sau bảng checklist, viết một đoạn ngắn giải thích: checklist này sẽ được **áp dụng lại và xác nhận từng mục** trong Chương 3 sau khi có kết quả thực nghiệm — Chương 2 chỉ thiết lập checklist ở mức thiết kế.

---

## 4. Yêu cầu đầu ra

Hãy tạo kết quả theo thứ tự:

### A. Mục 2.1 — Tổng quan PM2.5 và bài toán dự báo
Trình bày khái niệm PM2.5, đặc điểm biến động theo thời gian, và lý do đóng khung thành bài toán dự báo chuỗi thời gian. Không đưa số liệu cụ thể từ dataset.

### B. Mục 2.2 — Tổng quan nghiên cứu liên quan
Bảng tổng hợp + đoạn phân tích research gap. Nếu không tra cứu được nguồn thật, đánh dấu `CẦN TRA CỨU/XÁC MINH TRÍCH DẪN` kèm từ khóa tìm kiếm gợi ý, tuyệt đối không bịa tác giả/năm/kết quả.

### C. Mục 2.3 và 2.4 — Cơ sở lý luận ARIMA và Random Forest
Trình bày học thuật, chính xác về công thức và khái niệm, có trích nguồn tài liệu chính thức (Statsmodels, scikit-learn).

### D. Mục 2.5 — Quy trình phân tích dữ liệu
Sơ đồ pipeline + giải thích từng bước.

### E. Mục 2.6 — Biểu diễn dữ liệu và tạo đặc trưng
Bảng đặc trưng dự kiến cho Random Forest + biểu diễn dữ liệu cho ARIMA.

### F. Mục 2.7 — Các chỉ số đánh giá mô hình
Trình bày công thức và ý nghĩa của MAE, RMSE, R² (và MAPE nếu phù hợp).

### G. Mục 2.8 — Kiểm soát rò rỉ dữ liệu và khả năng tái lập
Bảng các loại leakage + nguyên tắc reproducibility.

### H. Mục 2.9 — Cấu hình thực nghiệm dự kiến
Thiết kế môi trường, chia dữ liệu, chiến lược tuning — nhất quán với Chương 3.

### I. Checklist kiểm soát chất lượng phân tích
Bảng 9 bước như mục 3, kèm đoạn giải thích cách áp dụng ở Chương 3.

---

## 5. Tiêu chuẩn chất lượng

Kết quả Chương 2 phải đạt các tiêu chí:

- Không hallucination về trích dẫn, tác giả, công thức.
- Phân biệt rõ ràng giữa "cơ sở lý luận/thiết kế" (Chương 2) và "kết quả thực nghiệm" (Chương 3) — Chương 2 không chứa bất kỳ con số nào được tính từ dataset thật.
- Nhất quán về mặt phương pháp luận với prompt Chương 1 và Chương 3 đã có (không mâu thuẫn về quy trình, chỉ số đánh giá, cách chia dữ liệu).
- Trình bày học thuật, có cấu trúc rõ ràng, phù hợp trình độ cao học ngành Hệ thống Thông tin, môn Phân tích dữ liệu.
- Không phóng đại vai trò của bất kỳ phương pháp nào trước khi có thực nghiệm.

**Ưu tiên tính đúng đắn và khả năng kiểm chứng hơn tính dài dòng.** Nếu một phần chưa đủ nguồn để trích dẫn cụ thể, hãy nói rõ rằng cần tra cứu thêm thay vì suy đoán.
