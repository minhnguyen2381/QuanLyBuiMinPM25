

**KHUNG HƯỚNG DẪN THỰC HIỆN TIỂU LUẬN**

**NGHIÊN CỨU VÀ DỰ BÁO**  
**NỒNG ĐỘ BỤI MỊN PM2.5 TẠI HÀ NỘI**

Bằng mô hình ARIMA và Random Forest  
Dữ liệu quan trắc giai đoạn 2022–2025

| THÔNG TIN | NỘI DUNG |
| :---: | ----- |
| Môn học | Phân tích dữ liệu |
| Quy mô nhóm | 02 thành viên |
| Công cụ | Python • Google Colab/Jupyter Notebook |
| Quy mô báo cáo | 25–30 trang, không tính phụ lục |
| Thời gian đề xuất | 06 tuần |

*Hà Nội, 2026*

# **MỤC LỤC NỘI DUNG**

1\. Tên đề tài và thông tin chung

2\. Mục tiêu, câu hỏi và phạm vi nghiên cứu

3\. Cấu trúc báo cáo chi tiết

4\. Phân công công việc cho nhóm 2 người

5\. Kế hoạch thực hiện trong 6 tuần

6\. Cấu trúc thư mục làm việc

7\. Danh mục bảng và hình tối thiểu

8\. Yêu cầu đối với mã nguồn

9\. Kịch bản thuyết trình

10\. Tiêu chí tự đánh giá trước khi nộp

# **1\. TÊN ĐỀ TÀI VÀ THÔNG TIN CHUNG**

## **1.1. Tên đề tài**

Nghiên cứu dự báo nồng độ bụi mịn PM2.5 tại Hà Nội bằng phương pháp ARIMA và Random Forest.

Tên đầy đủ đề xuất: Nghiên cứu và dự báo nồng độ bụi mịn PM2.5 tại Hà Nội bằng mô hình ARIMA và Random Forest trên dữ liệu quan trắc giai đoạn 2022–2025.

## **1.2. Thông tin chung**

* Số thành viên: 02 người.  
* Môn học: Phân tích dữ liệu.  
* Ngôn ngữ lập trình: Python.  
* Môi trường thực nghiệm: Google Colab hoặc Jupyter Notebook.  
* Dữ liệu: Chất lượng không khí tại Hà Nội giai đoạn 2022–2025.  
* Đối tượng phân tích: Nồng độ bụi mịn PM2.5.  
* Hai phương pháp chính: ARIMA và Random Forest Regression.  
* Quy mô báo cáo đề xuất: 25–30 trang, không tính phụ lục.

## **1.3. Sản phẩm cần nộp**

* Báo cáo tiểu luận hoàn chỉnh.  
* Bộ dữ liệu đã xử lý.  
* Notebook Python có thể chạy lại.  
* Biểu đồ và bảng kết quả.  
* Slide thuyết trình.

# **2\. MỤC TIÊU, CÂU HỎI VÀ PHẠM VI NGHIÊN CỨU**

## **2.1. Mục tiêu tổng quát**

Phân tích đặc điểm biến động và xây dựng mô hình dự báo nồng độ bụi mịn PM2.5 tại Hà Nội dựa trên dữ liệu quan trắc giai đoạn 2022–2025, qua đó đánh giá khả năng ứng dụng của ARIMA và Random Forest trong hỗ trợ cảnh báo ô nhiễm không khí.

## **2.2. Mục tiêu cụ thể**

* Thu thập, làm sạch và chuẩn hóa dữ liệu PM2.5.  
* Phân tích sự biến động của PM2.5 theo ngày, tháng, mùa và năm.  
* Xác định những giai đoạn có nồng độ PM2.5 cao.  
* Xây dựng mô hình ARIMA dự báo PM2.5.  
* Xây dựng mô hình Random Forest Regression dự báo PM2.5.  
* So sánh hai mô hình bằng MAE, RMSE và R².  
* Đề xuất khả năng ứng dụng mô hình tốt hơn vào hệ thống cảnh báo chất lượng không khí.

## **2.3. Câu hỏi nghiên cứu**

1. Nồng độ PM2.5 tại Hà Nội biến động như thế nào trong giai đoạn 2022–2025?

2. PM2.5 có biểu hiện xu hướng hoặc tính mùa vụ hay không?

3. Mô hình ARIMA có thể dự báo PM2.5 với độ chính xác như thế nào?

4. Random Forest có cải thiện kết quả dự báo so với ARIMA hay không?

5. Mô hình nào phù hợp hơn cho bài toán cảnh báo PM2.5 tại Hà Nội?

## **2.4. Phạm vi nghiên cứu**

* Phạm vi không gian: Hà Nội.  
* Phạm vi thời gian: Từ năm 2022 đến năm 2025\.  
* Biến mục tiêu: Nồng độ PM2.5 trung bình ngày.  
* Dữ liệu huấn luyện: 2022–2024.  
* Dữ liệu kiểm thử: Năm 2025\.  
* Không mở rộng sang quá nhiều chất ô nhiễm khác như PM10, CO, SO₂ hay NO₂.  
* Không triển khai ứng dụng hoàn chỉnh; chỉ đề xuất khả năng tích hợp vào hệ thống cảnh báo.

# **3\. CẤU TRÚC BÁO CÁO CHI TIẾT**

# **PHẦN MỞ ĐẦU — 2 đến 3 trang**

## **1\. Lý do chọn đề tài**

Phần này cần trình bày ngắn gọn bối cảnh và tính cần thiết của đề tài, tập trung vào các luận điểm sau:

* Ô nhiễm không khí là vấn đề đáng quan tâm tại các đô thị lớn.  
* PM2.5 có kích thước nhỏ, tồn tại lâu trong không khí và ảnh hưởng đến sức khỏe.  
* Hà Nội thường xuất hiện những giai đoạn chất lượng không khí suy giảm.  
* Dữ liệu quan trắc theo thời gian tạo điều kiện áp dụng các phương pháp phân tích dữ liệu.  
* Dự báo PM2.5 giúp cơ quan quản lý và người dân chủ động thực hiện các biện pháp phòng ngừa.  
* ARIMA đại diện cho phương pháp thống kê chuỗi thời gian; Random Forest đại diện cho học máy và có khả năng mô hình hóa quan hệ phi tuyến.

## **2\. Mục tiêu nghiên cứu**

Trình bày mục tiêu tổng quát và các mục tiêu cụ thể đã xác định tại Mục 2\.

## **3\. Đối tượng và phạm vi nghiên cứu**

* Đối tượng nghiên cứu.  
* Phạm vi không gian.  
* Phạm vi thời gian.  
* Nguồn dữ liệu.  
* Biến cần dự báo.

## **4\. Phương pháp nghiên cứu**

* Nghiên cứu tài liệu.  
* Thống kê mô tả và phân tích trực quan.  
* Phân tích chuỗi thời gian.  
* Mô hình ARIMA.  
* Mô hình Random Forest Regression.  
* So sánh mô hình bằng các độ đo đánh giá.

## **5\. Cấu trúc tiểu luận**

Giới thiệu ngắn gọn nội dung của ba chương, làm rõ mạch logic từ cơ sở lý thuyết, dữ liệu và phương pháp đến kết quả thực nghiệm và thảo luận.

# **CHƯƠNG 1\. TỔNG QUAN VỀ PHÂN TÍCH VÀ DỰ BÁO CHẤT LƯỢNG KHÔNG KHÍ**

| Dung lượng đề xuất: 6–8 trang. Không nên dành quá nhiều trang cho nội dung môi trường vì trọng tâm của môn học là phân tích dữ liệu. |
| :---- |

## **1.1. Tổng quan về ô nhiễm không khí**

* Khái niệm ô nhiễm không khí.  
* Các nguồn gây ô nhiễm tại đô thị.  
* Các chất ô nhiễm phổ biến.  
* Đặc điểm ô nhiễm không khí tại Hà Nội.  
* Ý nghĩa của việc quan trắc và dự báo.

## **1.2. Tổng quan về bụi mịn PM2.5**

### **1.2.1. Khái niệm PM2.5**

* Giải thích PM2.5 là gì.  
* Đơn vị đo thường dùng: μg/m³.  
* Phân biệt ngắn gọn PM2.5 và PM10.

### **1.2.2. Nguồn phát sinh PM2.5**

* Giao thông.  
* Công nghiệp.  
* Xây dựng.  
* Đốt nhiên liệu và phụ phẩm.  
* Điều kiện khí tượng làm tích tụ chất ô nhiễm.

### **1.2.3. Ý nghĩa của việc dự báo PM2.5**

* Cảnh báo sớm.  
* Hỗ trợ quản lý môi trường.  
* Hỗ trợ người dân lựa chọn thời điểm hoạt động ngoài trời.  
* Hỗ trợ ra quyết định dựa trên dữ liệu.

## **1.3. Tổng quan về phân tích dữ liệu chuỗi thời gian**

* Xu hướng.  
* Tính mùa vụ.  
* Chu kỳ.  
* Nhiễu.  
* Độ trễ.  
* Tính dừng của chuỗi.

| Yêu cầu giải thích: Dữ liệu PM2.5 là dữ liệu chuỗi thời gian nên không được chia tập huấn luyện–kiểm thử một cách ngẫu nhiên. |
| :---- |

## **1.4. Mô hình ARIMA**

### **1.4.1. Khái niệm**

ARIMA(p, d, q)

* p: bậc tự hồi quy.  
* d: số lần sai phân.  
* q: bậc trung bình trượt.

### **1.4.2. Các thành phần**

* AR – AutoRegressive.  
* I – Integrated.  
* MA – Moving Average.

### **1.4.3. Quy trình xây dựng**

1. Kiểm tra tính dừng.

2. Sai phân nếu chuỗi chưa dừng.

3. Xác định p, d, q.

4. Huấn luyện mô hình.

5. Kiểm tra phần dư.

6. Dự báo và đánh giá.

### **1.4.4. Ưu điểm và hạn chế**

| Ưu điểm | Hạn chế |
| ----- | ----- |
| Phù hợp với dữ liệu chuỗi thời gian. | Chủ yếu mô hình hóa quan hệ tuyến tính. |
| Có cơ sở thống kê rõ ràng. | Nhạy với dữ liệu thiếu và ngoại lệ. |
| Kết quả tương đối dễ giải thích. | Khó biểu diễn quan hệ phi tuyến phức tạp. |

## **1.5. Random Forest Regression**

### **1.5.1. Khái niệm**

Random Forest Regression kết hợp kết quả của nhiều cây quyết định để tạo ra giá trị dự báo cuối cùng.

### **1.5.2. Nguyên lý hoạt động**

* Lấy mẫu dữ liệu theo Bootstrap.  
* Xây dựng nhiều cây hồi quy.  
* Mỗi cây sử dụng một tập con thuộc tính.  
* Kết quả cuối là trung bình dự báo của các cây.

### **1.5.3. Các tham số chính**

* n\_estimators.  
* max\_depth.  
* min\_samples\_split.  
* min\_samples\_leaf.  
* max\_features.

### **1.5.4. Ưu điểm và hạn chế**

| Ưu điểm | Hạn chế |
| ----- | ----- |
| Mô hình hóa được quan hệ phi tuyến. | Không tự nhận biết thứ tự thời gian. |
| Ít nhạy với ngoại lệ hơn ARIMA. | Phải tạo các thuộc tính độ trễ. |
| Cho phép đánh giá mức độ quan trọng của thuộc tính. | Khó giải thích hơn mô hình thống kê. |

## **1.6. Các tiêu chí đánh giá**

### **MAE**

MAE \= (1/n) Σᵢ₌₁ⁿ |yᵢ − ŷᵢ|

MAE càng nhỏ thì sai số trung bình càng thấp.

### **RMSE**

RMSE \= √\[(1/n) Σᵢ₌₁ⁿ (yᵢ − ŷᵢ)²\]

RMSE phạt mạnh các dự báo có sai số lớn.

### **Hệ số xác định R²**

R² \= 1 − \[Σᵢ₌₁ⁿ (yᵢ − ŷᵢ)² / Σᵢ₌₁ⁿ (yᵢ − ȳ)²\]

R² càng gần 1 thì mô hình càng giải thích tốt sự biến động của dữ liệu.

## **1.7. Một số nghiên cứu liên quan**

Lập bảng tổng hợp tối thiểu 5 nghiên cứu theo mẫu sau:

| Tác giả, năm | Khu vực | Dữ liệu | Phương pháp | Kết quả chính | Hạn chế |
| :---: | :---: | :---: | :---: | :---: | :---: |
| … | … | … | … | … | … |

Cuối mục cần chỉ ra khoảng trống nghiên cứu:

* Nhiều nghiên cứu sử dụng dữ liệu tại quốc gia khác.  
* Một số nghiên cứu sử dụng dữ liệu cũ.  
* Chưa có nhiều so sánh trực tiếp ARIMA và Random Forest trên dữ liệu PM2.5 tại Hà Nội đến năm 2025\.  
* Cần đánh giá trên tập kiểm thử hoàn toàn theo thời gian.

## **1.8. Kết luận chương 1**

Tóm tắt cơ sở lý thuyết và khẳng định lý do lựa chọn hai phương pháp ARIMA và Random Forest.

# **CHƯƠNG 2\. DỮ LIỆU VÀ PHƯƠNG PHÁP NGHIÊN CỨU**

| Dung lượng đề xuất: 8–10 trang. |
| :---- |

## **2.1. Quy trình nghiên cứu**

**Thu thập dữ liệu  →  Kiểm tra và làm sạch  →  Phân tích khám phá  →  Chia dữ liệu theo thời gian  →  Xây dựng hai mô hình  →  Đánh giá và thảo luận**

## **2.2. Mô tả bộ dữ liệu**

* Tên bộ dữ liệu.  
* Nguồn cung cấp.  
* Thời gian thu thập.  
* Khu vực quan trắc.  
* Số lượng bản ghi ban đầu.  
* Tần suất quan trắc.  
* Các thuộc tính và đơn vị.  
* Giấy phép hoặc điều kiện sử dụng dữ liệu.

| Thuộc tính | Kiểu dữ liệu | Đơn vị | Ý nghĩa | Vai trò |
| :---: | :---: | :---: | ----- | :---: |
| Datetime | Thời gian | — | Thời điểm quan trắc | Chỉ mục |
| PM2.5 | Số thực | μg/m³ | Nồng độ bụi mịn | Biến mục tiêu |
| Temperature | Số thực | °C | Nhiệt độ | Nếu dữ liệu có |
| Humidity | Số thực | % | Độ ẩm | Nếu dữ liệu có |

## **2.3. Tiền xử lý dữ liệu**

### **2.3.1. Chuẩn hóa thời gian**

* Chuyển cột thời gian sang datetime.  
* Sắp xếp dữ liệu theo thời gian.  
* Loại bỏ bản ghi trùng.  
* Đặt thời gian làm chỉ mục.

### **2.3.2. Kiểm tra dữ liệu thiếu**

* Báo cáo số lượng và tỷ lệ dữ liệu thiếu.  
* Xác định vị trí và độ dài các khoảng thiếu.  
* Nội suy tuyến tính hoặc theo thời gian với khoảng thiếu ngắn.  
* Nếu khoảng thiếu quá dài, cần loại bỏ hoặc thảo luận riêng.

### **2.3.3. Xử lý dữ liệu bất thường**

* Kiểm tra giá trị PM2.5 âm.  
* Kiểm tra các giá trị quá lớn bất thường.  
* Sử dụng boxplot và IQR để nhận diện.  
* Không tự động xóa tất cả giá trị cao vì đó có thể là các đợt ô nhiễm thực tế.

### **2.3.4. Chuyển đổi tần suất**

Nếu dữ liệu theo giờ, tính PM2.5 trung bình ngày:

PM\_day \= (1/m) Σⱼ₌₁ᵐ PMⱼ

Trong đó m là số lần quan trắc hợp lệ trong ngày. Cần đặt điều kiện tối thiểu về số quan sát hợp lệ trong ngày để tránh tính trung bình từ quá ít dữ liệu.

## **2.4. Phân tích khám phá dữ liệu**

### **2.4.1. Thống kê mô tả**

* Số quan sát.  
* Trung bình và trung vị.  
* Độ lệch chuẩn.  
* Giá trị nhỏ nhất và lớn nhất.  
* Các phân vị 25%, 50%, 75%.

### **2.4.2. Phân bố PM2.5**

* Histogram.  
* Boxplot.  
* Nhận xét mức độ phân tán và phân bố lệch.

### **2.4.3. Biến động theo thời gian**

* Biểu đồ PM2.5 toàn giai đoạn.  
* Trung bình theo tháng và theo mùa.  
* So sánh giữa các năm.  
* Xác định các tháng có PM2.5 cao.

### **2.4.4. Phân tích tự tương quan**

* Sử dụng ACF và PACF.  
* Khảo sát độ trễ 1, 2, 3, 7, 14 và 30 ngày.  
* Đánh giá mức phụ thuộc của PM2.5 hiện tại vào các ngày trước.

## **2.5. Thiết kế thực nghiệm**

| Thành phần | Khoảng thời gian/giá trị | Mục đích |
| :---: | ----- | ----- |
| Tập huấn luyện | 2022–2024 | Xây dựng mô hình |
| Tập kiểm thử | 2025 | Đánh giá mô hình |
| Biến mục tiêu | PM2.5 tại ngày t | Giá trị cần dự báo |
| Tầm dự báo | Một ngày tiếp theo | Phù hợp cảnh báo ngắn hạn |

| Nguyên tắc: Tuyệt đối không dùng dữ liệu năm 2025 để lựa chọn tham số dựa trên kết quả kiểm thử cuối cùng. Có thể tách một phần cuối năm 2024 làm tập xác thực. |
| :---- |

## **2.6. Xây dựng mô hình ARIMA**

### **2.6.1. Kiểm tra tính dừng**

* Sử dụng kiểm định ADF.  
* H₀: chuỗi không dừng.  
* H₁: chuỗi dừng.  
* Nếu p-value \< 0,05, có thể bác bỏ H₀.

### **2.6.2. Lựa chọn tham số**

* Xác định d bằng sai phân.  
* Tham khảo ACF để chọn q.  
* Tham khảo PACF để chọn p.  
* Thử p \= 0,…,5; d \= 0,1; q \= 0,…,3.  
* Ưu tiên lựa chọn theo AIC trên dữ liệu huấn luyện hoặc tập xác thực, không chỉ theo RMSE trên năm 2025\.

### **2.6.3. Kiểm tra phần dư**

* Vẽ phần dư và kiểm tra trung bình phần dư.  
* Vẽ ACF phần dư.  
* Có thể sử dụng kiểm định Ljung–Box.  
* Nếu phần dư còn tự tương quan mạnh, mô hình chưa khai thác hết thông tin trong chuỗi.

## **2.7. Xây dựng Random Forest**

### **2.7.1. Tạo thuộc tính đầu vào**

| Nhóm | Thuộc tính đề xuất |
| :---: | ----- |
| Độ trễ | lag\_1, lag\_2, lag\_3, lag\_7, lag\_14 |
| Trung bình trượt | rolling\_mean\_3, rolling\_mean\_7, rolling\_mean\_14 |
| Độ biến động | rolling\_std\_7 |
| Thời gian | Thứ, tháng, mùa |

lag\_1 \= PM2.5₍ₜ₋₁₎

rolling\_mean\_7 \= (1/7) Σᵢ₌₁⁷ PM2.5₍ₜ₋ᵢ₎

| Tránh rò rỉ dữ liệu: Chỉ sử dụng dữ liệu trước ngày dự báo; không sử dụng giá trị tương lai khi tạo thuộc tính. |
| :---- |

### **2.7.2. Lựa chọn tham số**

* n\_estimators: 100, 200, 300\.  
* max\_depth: 5, 10, 15 hoặc None.  
* min\_samples\_leaf: 1, 2, 4\.  
* Không cần tìm kiếm quá rộng vì mục tiêu chính là phân tích và so sánh hai hướng tiếp cận.

### **2.7.3. Mức độ quan trọng của thuộc tính**

* Những độ trễ quan trọng nhất.  
* Trung bình 7 ngày có ảnh hưởng hay không.  
* Yếu tố tháng hoặc mùa có vai trò như thế nào.

## **2.8. Phương pháp đánh giá**

Cả hai mô hình phải được đánh giá trên cùng tập kiểm thử năm 2025 bằng MAE, RMSE, R² và có thể bổ sung thời gian huấn luyện.

Bổ sung mô hình tham chiếu đơn giản:

ŷₜ \= y₍ₜ₋₁₎

Đây là dự báo ngây thơ: PM2.5 ngày mai bằng PM2.5 hôm nay. ARIMA và Random Forest chỉ thực sự có ý nghĩa nếu cải thiện so với mốc này. Mô hình tham chiếu không được xem là phương pháp nghiên cứu thứ ba.

## **2.9. Kết luận chương 2**

Tóm tắt dữ liệu, quy trình tiền xử lý và thiết kế hai mô hình.

# **CHƯƠNG 3\. KẾT QUẢ VÀ THẢO LUẬN**

| Dung lượng đề xuất: 8–10 trang. |
| :---- |

## **3.1. Kết quả tiền xử lý**

* Số bản ghi ban đầu.  
* Số bản ghi trùng.  
* Số giá trị thiếu.  
* Số bản ghi bị loại.  
* Số quan sát còn lại.  
* Khoảng thời gian thực tế sau làm sạch.

| Nội dung | Trước xử lý | Sau xử lý |
| ----- | :---: | :---: |
| Số bản ghi | … | … |
| Giá trị thiếu | … | … |
| Bản ghi trùng | … | … |
| Giá trị không hợp lệ | … | … |

## **3.2. Kết quả phân tích khám phá**

### **3.2.1. Đặc điểm phân bố PM2.5**

* Giá trị trung bình và trung vị.  
* Mức độ phân tán.  
* Phân bố có lệch phải hay không.  
* Tần suất xuất hiện các giá trị cao.

### **3.2.2. Biến động theo tháng và mùa**

* Tháng nào có PM2.5 trung bình cao nhất?  
* Mùa nào có mức ô nhiễm cao?  
* Năm 2025 khác các năm trước như thế nào?  
* Có thể quan sát được tính mùa vụ hay không?

### **3.2.3. Các đợt PM2.5 tăng cao**

Xác định một số khoảng thời gian tiêu biểu, nhưng không suy diễn nguyên nhân nếu không có dữ liệu khí tượng hoặc nguồn phát thải hỗ trợ.

## **3.3. Kết quả mô hình ARIMA**

* Kết quả kiểm định ADF.  
* Số lần sai phân.  
* Bộ tham số p, d, q.  
* Giá trị AIC.  
* Kết quả kiểm tra phần dư.  
* MAE, RMSE và R².  
* Biểu đồ giá trị thực tế và dự báo.

| Mô hình | AIC | MAE | RMSE | R² |
| :---: | :---: | :---: | :---: | :---: |
| ARIMA(1,1,1) | … | … | … | … |
| ARIMA(3,1,1) | … | … | … | … |
| ARIMA tốt nhất | … | … | … | … |

## **3.4. Kết quả Random Forest**

* Bộ thuộc tính đầu vào.  
* Tham số mô hình tốt nhất.  
* MAE, RMSE và R².  
* Mức độ quan trọng của thuộc tính.  
* Biểu đồ giá trị thực tế và dự báo.

| Thứ hạng | Thuộc tính | Mức độ quan trọng |
| :---: | :---: | :---: |
| 1 | lag\_1 | … |
| 2 | rolling\_mean\_7 | … |
| 3 | lag\_7 | … |

## **3.5. So sánh hai phương pháp**

| Phương pháp | MAE | RMSE | R² | Ưu điểm | Hạn chế |
| :---: | :---: | :---: | :---: | :---: | ----- |
| Dự báo tham chiếu | … | … | … | Đơn giản | Không học được quy luật |
| ARIMA | … | … | … | Dễ giải thích | Hạn chế với phi tuyến |
| Random Forest | … | … | … | Xử lý phi tuyến | Cần tạo thuộc tính |

Phần nhận xét phải làm rõ:

* Mô hình nào có RMSE thấp hơn?  
* Mức cải thiện là bao nhiêu phần trăm?  
* Mô hình nào dự báo tốt hơn trong giai đoạn PM2.5 tăng cao?  
* Mô hình nào ổn định hơn?  
* Kết quả có phù hợp với đặc điểm của từng phương pháp hay không?

Improvement \= \[(RMSE\_ARIMA − RMSE\_RF) / RMSE\_ARIMA\] × 100%

## **3.6. Phân tích sai số**

* Xác định 5–10 ngày có sai số lớn nhất.  
* So sánh sai số theo tháng.  
* Kiểm tra mô hình có thường dự báo thấp tại những ngày PM2.5 tăng đột biến không.  
* Thảo luận nguyên nhân có thể do thiếu dữ liệu khí tượng, giao thông hoặc nguồn phát thải.

## **3.7. Thảo luận**

* Tính mùa vụ của PM2.5.  
* Khả năng dự báo của ARIMA.  
* Lợi thế hoặc hạn chế của Random Forest.  
* Ý nghĩa của các thuộc tính độ trễ.  
* Khả năng ứng dụng trong thực tế.

| Lưu ý kết luận: Không nên kết luận Random Forest luôn tốt hơn ARIMA trên mọi dữ liệu; chỉ kết luận trong phạm vi bộ dữ liệu và thiết kế thực nghiệm của đề tài. |
| :---- |

## **3.8. Đề xuất ứng dụng**

**Dữ liệu quan trắc  →  Cập nhật và kiểm tra  →  Mô hình dự báo  →  Dự báo ngày tiếp theo  →  Phân loại cảnh báo  →  Dashboard/thông báo**

* Dữ liệu cập nhật tự động.  
* Mô hình chạy định kỳ.  
* Kết quả hiển thị trên dashboard.  
* Gửi cảnh báo nếu giá trị dự báo vượt ngưỡng.  
* Mô hình được huấn luyện lại định kỳ.

## **3.9. Hạn chế của nghiên cứu**

* Dữ liệu chỉ đại diện cho một khu vực hoặc một số trạm.  
* Thiếu biến khí tượng hoặc nguồn phát thải.  
* ARIMA chưa mô hình hóa đầy đủ tính mùa vụ phức tạp.  
* Random Forest phụ thuộc vào thiết kế thuộc tính.  
* Chỉ dự báo ngắn hạn.  
* Chưa triển khai thành hệ thống thực tế.

## **3.10. Kết luận chương 3**

Tóm tắt kết quả chính và mô hình phù hợp hơn trong phạm vi nghiên cứu.

# **KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN — 2 đến 3 trang**

## **1\. Kết luận**

Phần kết luận cần trả lời trực tiếp:

* Đề tài đã thực hiện được những mục tiêu nào?  
* Dữ liệu PM2.5 có đặc điểm gì?  
* Kết quả ARIMA như thế nào?  
* Kết quả Random Forest như thế nào?  
* Mô hình nào tốt hơn và dựa trên tiêu chí nào?  
* Kết quả có ý nghĩa gì đối với cảnh báo chất lượng không khí?

## **2\. Hướng phát triển**

* Bổ sung nhiệt độ, độ ẩm, lượng mưa và tốc độ gió.  
* Sử dụng dữ liệu từ nhiều trạm.  
* Mở rộng dự báo theo giờ.  
* Nghiên cứu SARIMA hoặc các mô hình học sâu.  
* Xây dựng dashboard theo thời gian thực.  
* Tích hợp mô hình vào hệ thống hỗ trợ ra quyết định.

# **4\. PHÂN CÔNG CÔNG VIỆC CHO NHÓM 2 NGƯỜI**

Nguyên tắc: mỗi thành viên có phần phụ trách chính, nhưng cả hai đều phải hiểu toàn bộ quy trình và cùng kiểm tra kết quả.

| Nội dung | Thành viên 1 | Thành viên 2 |
| ----- | ----- | ----- |
| Thu thập tài liệu | ARIMA, chuỗi thời gian | Random Forest, PM2.5 |
| Thu thập dữ liệu | Phối hợp | Phụ trách chính |
| Làm sạch dữ liệu | Phối hợp | Phụ trách chính |
| Phân tích khám phá | Phối hợp | Phụ trách chính |
| Mô hình ARIMA | Phụ trách chính | Kiểm tra |
| Random Forest | Kiểm tra | Phụ trách chính |
| Đánh giá mô hình | Cùng thực hiện | Cùng thực hiện |
| Phân tích sai số | Cùng thực hiện | Cùng thực hiện |
| Viết Chương 1 | Mục 1.3–1.4 | Mục 1.1–1.2 và 1.5 |
| Viết Chương 2 | ARIMA, thiết kế đánh giá | Dữ liệu, EDA, Random Forest |
| Viết Chương 3 | Kết quả ARIMA | Kết quả Random Forest |
| So sánh và thảo luận | Cùng thực hiện | Cùng thực hiện |
| Chuẩn hóa báo cáo | Phụ trách chính | Kiểm tra |
| Làm slide | Kiểm tra nội dung | Phụ trách chính |
| Thuyết trình | Lý thuyết và ARIMA | Dữ liệu, Random Forest và kết quả |

## **Yêu cầu phối hợp**

* Dùng chung một notebook hoặc một thư mục dự án.  
* Thống nhất một phiên bản dữ liệu đã làm sạch.  
* Thống nhất cách chia tập huấn luyện và kiểm thử.  
* Không để hai thành viên tự đánh giá mô hình trên hai tập dữ liệu khác nhau.  
* Mỗi người phải đọc và kiểm tra phần của người còn lại.  
* Cả hai cùng chịu trách nhiệm về phần kết luận và thảo luận.

# **5\. KẾ HOẠCH THỰC HIỆN TRONG 6 TUẦN**

| Tuần | Nội dung | Sản phẩm |
| :---: | ----- | ----- |
| 1 | Chốt đề tài, dữ liệu, mục tiêu và câu hỏi nghiên cứu | Đề cương chính thức |
| 2 | Tổng quan tài liệu và mô tả phương pháp | Bản nháp Chương 1 |
| 3 | Làm sạch dữ liệu và phân tích khám phá | Dataset sạch, biểu đồ EDA |
| 4 | Xây dựng ARIMA và Random Forest | Notebook chạy được |
| 5 | Đánh giá, so sánh và phân tích sai số | Bảng kết quả, Chương 2–3 |
| 6 | Hoàn thiện báo cáo, slide và luyện trình bày | Báo cáo và slide hoàn chỉnh |

# **6\. CẤU TRÚC THƯ MỤC LÀM VIỆC**

| PM25\_Hanoi/├── data/│   ├── raw/│   └── processed/├── notebooks/│   ├── 01\_data\_preprocessing.ipynb│   ├── 02\_eda.ipynb│   ├── 03\_arima.ipynb│   ├── 04\_random\_forest.ipynb│   └── 05\_model\_comparison.ipynb├── figures/├── results/├── report/└── slides/ |
| :---- |

Tên tệp nên thống nhất; không sử dụng các tên như code\_moi.ipynb, final2.ipynb hoặc final\_moi\_nhat.ipynb.

# **7\. DANH MỤC BẢNG VÀ HÌNH TỐI THIỂU**

## **7.1. Các bảng**

1. Mô tả thuộc tính dữ liệu.

2. Thống kê dữ liệu thiếu.

3. Thống kê mô tả PM2.5.

4. Kết quả lựa chọn ARIMA.

5. Tham số Random Forest.

6. Mức độ quan trọng của thuộc tính.

7. So sánh MAE, RMSE và R².

8. Sai số theo tháng.

## **7.2. Các hình**

1. Quy trình nghiên cứu.

2. Biểu đồ PM2.5 theo thời gian.

3. Histogram phân bố PM2.5.

4. Boxplot theo tháng hoặc mùa.

5. PM2.5 trung bình theo tháng.

6. Biểu đồ ACF và PACF.

7. Kết quả dự báo ARIMA.

8. Kết quả dự báo Random Forest.

9. So sánh giá trị thực tế và hai mô hình.

10. Biểu đồ mức độ quan trọng của thuộc tính.

11. Biểu đồ sai số theo thời gian.

# **8\. YÊU CẦU ĐỐI VỚI MÃ NGUỒN**

Notebook phải đáp ứng các yêu cầu sau:

* Chạy lần lượt từ đầu đến cuối mà không báo lỗi.  
* Cố định random\_state cho Random Forest.  
* Không sử dụng dữ liệu tương lai để tạo đặc trưng.  
* Không chia dữ liệu ngẫu nhiên.  
* Ghi chú rõ từng bước.  
* Hiển thị số lượng dữ liệu trước và sau xử lý.  
* Xuất bảng chỉ số đánh giá.  
* Lưu các biểu đồ cần dùng trong báo cáo.  
* Tách phần xử lý dữ liệu, mô hình và đánh giá thành các mục rõ ràng.

# **9\. KỊCH BẢN THUYẾT TRÌNH CHO HAI THÀNH VIÊN**

| Thời lượng đề xuất: 12–15 phút. |
| :---- |

## **9.1. Thành viên 1 — khoảng 6–7 phút**

* Lý do chọn đề tài.  
* Mục tiêu và câu hỏi nghiên cứu.  
* Tổng quan dữ liệu chuỗi thời gian.  
* Mô hình ARIMA.  
* Kết quả thực nghiệm ARIMA.

## **9.2. Thành viên 2 — khoảng 6–7 phút**

* Bộ dữ liệu và tiền xử lý.  
* Phân tích khám phá.  
* Random Forest và cách tạo thuộc tính.  
* Kết quả so sánh.  
* Kết luận, hạn chế và hướng phát triển.

## **9.3. Cả hai cùng chuẩn bị trả lời**

* Vì sao không chia dữ liệu ngẫu nhiên?  
* Vì sao chọn ARIMA và Random Forest?  
* Vì sao sử dụng RMSE làm tiêu chí chính?  
* Có xảy ra rò rỉ dữ liệu hay không?  
* Tại sao chọn dữ liệu năm 2025 làm tập kiểm thử?  
* Mô hình có ứng dụng thực tế được không?  
* Vì sao chưa sử dụng SARIMA hoặc LSTM?

# **10\. TIÊU CHÍ TỰ ĐÁNH GIÁ TRƯỚC KHI NỘP**

| Tiêu chí | Yêu cầu |
| :---: | ----- |
| Tính thực tế | Dữ liệu PM2.5 thực tế tại Hà Nội |
| Tính cập nhật | Có dữ liệu đến năm 2025 |
| Tính nghiên cứu | Có câu hỏi, thực nghiệm, so sánh và thảo luận |
| Phương pháp | Chỉ tập trung ARIMA và Random Forest |
| Phân chia dữ liệu | Theo đúng thứ tự thời gian |
| Đánh giá | Có MAE, RMSE, R² và mô hình tham chiếu |
| Phân tích | Không chỉ trình bày kết quả chạy code |
| Tính tái lập | Notebook chạy lại được |
| Báo cáo | Hình, bảng được đánh số và nhận xét |
| Phối hợp nhóm | Hai thành viên đều có nhiệm vụ rõ ràng |

| Thông điệp cốt lõi: Chiều sâu của tiểu luận nằm ở thiết kế thực nghiệm đúng, tránh rò rỉ dữ liệu, phân tích sai số và giải thích kết quả. |
| :---- |

