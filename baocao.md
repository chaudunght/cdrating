# BÁO CÁO ĐỒ ÁN: HỆ THỐNG PHÂN LOẠI PHẢN HỒI KHÁCH HÀNG

---

## 1. TRANG BÌA
**TRƯỜNG ĐẠI HỌC ...**  
**KHOA CÔNG NGHỆ THÔNG TIN**

**ĐỒ ÁN MÔN HỌC: LẬP TRÌNH PYTHON VÀ ỨNG DỤNG NLP**  
**ĐỀ TÀI: HỆ THỐNG PHÂN LOẠI PHẢN HỒI KHÁCH HÀNG**

**Giảng viên hướng dẫn:** [Tên giảng viên]  
**Sinh viên thực hiện:** [Tên của bạn / Nhóm của bạn]  
**Mã sinh viên:** [Mã SV]  
**Lớp:** [Tên lớp]

---

## 2. TÊN ĐỒ ÁN
**Hệ thống phân loại phản hồi khách hàng (Customer Feedback Classification System)**

## 3. MÔ TẢ BÀI TOÁN
Trong lĩnh vực thương mại điện tử, việc nắm bắt tâm lý khách hàng thông qua các đánh giá (feedback) là vô cùng quan trọng. Bài toán đặt ra là xây dựng một hệ thống có khả năng tự động phân tích và phân loại các đoạn văn bản phản hồi ngắn của khách hàng thành 3 nhóm cảm xúc chính:
- **Tích cực (Positive):** Khen ngợi sản phẩm, dịch vụ.
- **Tiêu cực (Negative):** Phàn nàn, đánh giá thấp chất lượng.
- **Trung lập (Neutral):** Nhận xét bình thường, không rõ thái độ hoặc có cả khen lẫn chê.

Hệ thống được xây dựng bằng ngôn ngữ Python thuần, không sử dụng các thư viện hỗ trợ xử lý ngôn ngữ tự nhiên (NLP) hay học máy chuyên dụng.

## 4. DỮ LIỆU SỬ DỤNG
Dữ liệu được khai báo trực tiếp trong tệp `data.py`, bao gồm:
- **Tập huấn luyện (Training Data):** Gồm 65 mẫu văn bản tiếng Việt đã được gán nhãn thủ công (bao gồm các nhóm tích cực, trung lập, tiêu cực). Các nội dung xoay quanh lĩnh vực dụng cụ thể thao.
- **Văn bản kiểm thử (Test Data):** Một biến `new_text` chứa câu phản hồi mới cần dự đoán: *"Vợt đánh tốt, giao hàng nhanh, shop phục vụ không nhiệt tình."*

## 5. CÁC BƯỚC XỬ LÝ
Quy trình xử lý trong tệp `main.py` được chia thành các module chính:

### Bước 1: Tiền xử lý văn bản (Text Preprocessing)
- **Chuẩn hóa chữ thường:** Chuyển toàn bộ văn bản về dạng chữ thường để đồng nhất.
- **Loại bỏ dấu câu:** Sử dụng vòng lặp để lọc bỏ các ký tự đặc biệt như `!?. ,;:...`.
- **Xóa khoảng trắng thừa:** Đảm bảo giữa các từ chỉ có duy nhất một khoảng trắng.
- **Tách từ (Tokenization):** Cắt chuỗi văn bản thành danh sách các từ đơn lẻ.

### Bước 2: Biểu diễn văn bản và Tính toán xác suất
- **Xây dựng từ điển (Vocabulary):** Tập hợp tất cả các từ đặc trưng xuất hiện trong tập huấn luyện (507 từ).
- **Tính toán xác suất từ (Word Probability):** 
    - Tính toán xác suất xuất hiện của từng từ trong mỗi nhãn.
    - Sử dụng kỹ thuật **Laplace Smoothing** (cộng 1) để tránh trường hợp xác suất bằng 0.
- **Tính điểm văn bản:** Sử dụng tổng Log-Probability để tránh hiện tượng tràn số dưới (underflow).

### Bước 3: Dự đoán và Chuẩn hóa
- Áp dụng kỹ thuật tương tự hàm **Softmax** để chuyển đổi điểm số từ hệ số Log (số âm) sang thang điểm phần trăm (0-100%) giúp người dùng dễ quan sát mức độ tin cậy.

## 6. KẾT QUẢ VÀ NHẬN XÉT

### Kết quả chạy chương trình
Với câu đầu vào: *"Vợt đánh tốt, giao hàng nhanh, shop phục vụ không nhiệt tình."*
Chương trình đưa ra kết quả phân tích:
- **Tích cực:** 72.47
- **Trung lập:** 21.41
- **Tiêu cực:** 6.12
- **Nhãn dự đoán:** **TÍCH CỰC**

### Nhận xét
- **Ưu điểm:** Hệ thống chạy nhanh, không phụ thuộc thư viện bên ngoài, giao diện trực quan. Dù câu có vế sau hơi tiêu cực ("không nhiệt tình"), nhưng các từ "tốt", "nhanh" có trọng số tích cực mạnh trong tập huấn luyện nên kết quả tổng thể vẫn nghiêng về tích cực.
- **Hạn chế:** Chưa hiểu được ngữ cảnh phức tạp (như sự đối lập giữa các vế câu) do chỉ sử dụng unigram.
- **Hướng phát triển:** Cần bổ sung thêm dữ liệu huấn luyện và áp dụng N-gram để hiểu rõ hơn các cụm từ phủ định hoặc đối lập.
