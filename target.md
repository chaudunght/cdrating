### 1. Quy định chung

* Mỗi đồ án gồm 2 phần: Python cơ bản và bài toán ứng dụng.
* Sinh viên vận dụng kiến thức xử lý văn bản, biểu diễn văn bản và phân loại văn bản đã học.
* Không sử dụng thư viện NLP hoặc học máy có sẵn như sklearn, nltk, underthesea, pyvi, gensim.
* Được sử dụng các thành phần cơ bản của Python: chuỗi, danh sách, từ điển, tập hợp, vòng lặp, hàm và câu lệnh điều kiện.
* Chương trình phải chạy được với bộ dữ liệu nhỏ do sinh viên tự chuẩn bị hoặc khai báo trực tiếp.

### 2. Sản phẩm cần nộp

* File mã nguồn Python.
* Báo cáo ngắn gồm: Có trang bìa, tên các thành viên, tên đồ án, mô tả bài toán, dữ liệu sử dụng, các bước xử lý, kết quả và nhận xét. (<10 trang, in 2 mặt)
* Nộp bản mềm báo cáo và tệp mã nguồn lên elearning.

### 3. Tiêu chí chấm đồ án

**3.1. Phần 1: Kiến thức lập trình Python cơ bản - 2 điểm**

| Tiêu chí | Điểm tối đa |
| --- | --- |
| Khai báo hoặc nhập được dữ liệu đầu vào | 0.5 |
| Sử dụng được biến, kiểu dữ liệu, danh sách, chuỗi | 0.5 |
| Có sử dụng vòng lặp, điều kiện và hàm | 0.5 |
| Chương trình chạy được và có kết quả đúng cơ bản | 0.5 |

**3.2. Phần 2: Bài toán ứng dụng xử lý ngôn ngữ tự nhiên - 3 điểm**

| Tiêu chí | Điểm tối đa |
| --- | --- |
| Có bộ dữ liệu mẫu phù hợp với bài toán | 0.5 |
| Tiền xử lý được văn bản: chữ thường, xóa dấu câu, tách từ | 0.5 |
| Biểu diễn được văn bản dưới dạng có thể tính toán | 0.5 |
| Tính được điểm hoặc xác suất cho từng nhóm/lớp | 0.5 |
| Dự đoán được kết quả phân loại phù hợp | 0.5 |
| In kết quả rõ ràng, dễ kiểm tra | 0.5 |

**3.3 Báo cáo và trả lời câu hỏi - 5 điểm**

| Tiêu chí | Điểm tối đa |
| --- | --- |
| Báo cáo mô tả được bài toán, dữ liệu và cách xử lý | 1.0 |
| Trả lời được các câu hỏi | 4.0 |

---

### Đồ án 1: Hệ thống phân loại phản hồi khách hàng

**Phần 1. Kiến thức lập trình Python cơ bản — 2 điểm**

* Khai báo hoặc nhập danh sách ít nhất 10 văn bản/câu ngắn tiếng việt phù hợp.
* In ra số lượng văn bản trong danh sách.
* Đếm số từ trong từng văn bản.
* Viết hàm chuẩn hóa văn bản về chữ thường.
* Viết hàm loại bỏ dấu câu hoặc khoảng trắng thừa.
* In kết quả sau khi xử lý.

**Phần 2. Bài toán ứng dụng xử lý ngôn ngữ tự nhiên — 8 điểm**
Một cửa hàng trực tuyến nhận nhiều phản hồi sau khi mua hàng và muốn tự động phân loại phản hồi thành tích cực, tiêu cực hoặc trung lập.

* Chuẩn bị tập dữ liệu nhỏ gồm văn bản mẫu và nhãn/nhóm tương ứng.
* Nhập hoặc khai báo một văn bản mới cần phân loại.
* Tiền xử lý văn bản: chuẩn hóa chữ thường, xóa dấu câu, xóa khoảng trắng thừa, tách từ.
* Xây dựng danh sách từ đặc trưng từ tập dữ liệu mẫu.
* Biểu diễn văn bản thành dạng dữ liệu có thể tính toán.
* Tính điểm hoặc xác suất của văn bản mới đối với từng nhóm.
* In ra điểm hoặc xác suất của từng nhóm.
* In ra nhóm/nhãn được dự đoán và nhận xét ngắn gọn.
* Không sử dụng thư viện học máy hoặc NLP có sẵn.