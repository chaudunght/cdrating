# KẾ HOẠCH CHI TIẾT ĐỒ ÁN
## Hệ thống Phân loại Phản hồi Khách hàng

> **Project Manager:** Lò Châu Dũng 
> **Phiên bản:** 1.0  
> **Ngày lập:** 14/05/2026  
> **Tổng điểm tối đa:** 10 điểm

---

## TỔNG QUAN DỰ ÁN

| Hạng mục | Chi tiết |
|---|---|
| Mục tiêu | Xây dựng hệ thống phân loại phản hồi khách hàng (tích cực / tiêu cực / trung lập) bằng Python thuần |
| Ngôn ngữ | Python (không dùng sklearn, nltk, underthesea, pyvi, gensim) |
| Đầu vào | Danh sách ≥ 10 phản hồi tiếng Việt có nhãn + 1 văn bản mới cần phân loại |
| Đầu ra | File `.py` chạy được + Báo cáo PDF/Word < 10 trang |
| Sản phẩm nộp | Mã nguồn `.py` + Báo cáo nộp lên elearning |

---

## MODULE 1 — DỮ LIỆU & KHAI BÁO ĐẦU VÀO
> **Phụ trách:** Châu Dũng  
> **Trọng số:** Phần 1 (0.5đ) + Phần 2 (0.5đ) = **1.0đ**  
> **Deadline:** Ngày 1 (hoàn thành trước khi bắt đầu Module 2)

### Nhiệm vụ

**1.1 Chuẩn bị bộ dữ liệu mẫu (training data)**
- Khai báo danh sách `training_data` gồm **tối thiểu 10 văn bản** tiếng Việt ngắn.
- Mỗi phần tử là một `tuple`: `(văn_bản, nhãn)` với nhãn là `"tích cực"`, `"tiêu cực"`, hoặc `"trung lập"`.
- Phân bố nhãn cân bằng: ít nhất 3–4 mẫu mỗi nhóm.

```
Ví dụ:
training_data = [
    ("Sản phẩm rất tốt, tôi rất hài lòng", "tích cực"),
    ("Giao hàng chậm, hàng bị hỏng", "tiêu cực"),
    ("Sản phẩm bình thường, không có gì đặc biệt", "trung lập"),
    ...
]
```

**1.2 Khai báo văn bản mới cần phân loại**
- Khai báo biến `new_text` chứa 1 câu phản hồi mới (chưa có nhãn).
- Đây là đầu vào để hệ thống dự đoán ở Module 4.

**1.3 In thống kê dữ liệu đầu vào**
- In tổng số văn bản trong danh sách (`len(training_data)`).
- In số từ trong từng văn bản bằng vòng lặp `for`.
- Đảm bảo kết quả in ra màn hình rõ ràng, có nhãn từng dòng.

### Tiêu chí hoàn thành
- [ ] Có đúng ≥ 10 mẫu, đủ 3 nhãn
- [ ] In được tổng số văn bản
- [ ] In được số từ từng văn bản
- [ ] `new_text` đã được khai báo

---

## MODULE 2 — TIỀN XỬ LÝ VĂN BẢN
> **Phụ trách:** Châu Dũng 
> **Trọng số:** Phần 1 (1.0đ) + Phần 2 (0.5đ) = **1.5đ**  
> **Dependency:** Module 1 phải hoàn thành  
> **Deadline:** Ngày 2

### Nhiệm vụ

**2.1 Hàm chuẩn hóa chữ thường — `normalize_lower(text)`**
- Nhận đầu vào là một chuỗi, trả về chuỗi đã được chuyển toàn bộ về chữ thường.
- Sử dụng method `.lower()` của Python.

**2.2 Hàm loại bỏ dấu câu — `remove_punctuation(text)`**
- Duyệt từng ký tự trong chuỗi, loại bỏ các ký tự dấu câu phổ biến: `! ? . , ; : " ' ( ) [ ] { } / \ - _`
- Sử dụng vòng lặp `for` + câu lệnh `if` (không dùng `re`).
- Trả về chuỗi sạch.

**2.3 Hàm loại bỏ khoảng trắng thừa — `remove_extra_spaces(text)`**
- Xóa khoảng trắng dư ở đầu/cuối (`strip()`).
- Chuẩn hóa khoảng trắng giữa các từ (chỉ còn 1 space).

**2.4 Hàm tách từ — `tokenize(text)`**
- Tách chuỗi thành danh sách các từ bằng `.split()`.
- Trả về `list` các từ.

**2.5 Hàm tiền xử lý tổng hợp — `preprocess(text)`**
- Gọi tuần tự: `normalize_lower` → `remove_punctuation` → `remove_extra_spaces` → `tokenize`.
- Trả về danh sách từ đã được làm sạch.

**2.6 Áp dụng cho toàn bộ dữ liệu**
- Tạo `processed_data`: danh sách các `(danh_sách_từ, nhãn)` bằng cách áp dụng `preprocess()` cho từng văn bản trong `training_data`.
- In kết quả sau khi xử lý ít nhất 3 mẫu để kiểm tra.

### Tiêu chí hoàn thành
- [ ] 4 hàm riêng biệt, có docstring mô tả
- [ ] `preprocess()` gọi đúng thứ tự các bước
- [ ] `processed_data` được tạo thành công
- [ ] In kết quả xử lý mẫu để kiểm tra

---

## MODULE 3 — BIỂU DIỄN VĂN BẢN & TÍNH ĐIỂM
> **Phụ trách:** Châu Dũng 
> **Trọng số:** Phần 2 (1.5đ)  
> **Dependency:** Module 2 phải hoàn thành  
> **Deadline:** Ngày 3

### Nhiệm vụ

**3.1 Xây dựng danh sách từ đặc trưng — `build_vocab(processed_data)`**
- Duyệt toàn bộ `processed_data`, thu thập tất cả từ duy nhất vào một `set`.
- Chuyển thành `list` (từ điển từ vựng).
- In số lượng từ đặc trưng tìm được.

**3.2 Biểu diễn văn bản dạng Bag-of-Words — `text_to_bow(tokens, vocab)`**
- Tạo `dict` ánh xạ từ → số lần xuất hiện trong văn bản đó.
- Chỉ dùng `dict`, `for`, `if`.
- Đây là vector đặc trưng cho mỗi văn bản.

**3.3 Tính xác suất từng từ theo nhãn — `build_word_prob(processed_data, labels)`**
- Với mỗi nhãn (`tích cực`, `tiêu cực`, `trung lập`):
  - Tập hợp tất cả từ từ các văn bản thuộc nhãn đó.
  - Đếm tần suất từng từ.
  - Tính xác suất = `số lần từ xuất hiện / tổng số từ trong nhãn`.
- Lưu vào `dict` có cấu trúc: `{ nhãn: { từ: xác_suất } }`.
- Áp dụng **Laplace Smoothing** đơn giản (cộng 1 vào mỗi từ, mẫu số cộng thêm `len(vocab)`) để tránh xác suất bằng 0.

**3.4 Tính điểm phân loại — `score_text(tokens, word_prob, labels)`**
- Với mỗi nhãn, tính tổng `log(xác_suất(từ | nhãn))` cho các từ trong văn bản mới.
- Dùng `import math` → `math.log()` (đây là module chuẩn Python, không vi phạm quy định).
- Trả về `dict`: `{ nhãn: điểm }`.

### Tiêu chí hoàn thành
- [ ] `build_vocab()` trả về danh sách từ không trùng lặp
- [ ] `text_to_bow()` tạo đúng vector từ
- [ ] `build_word_prob()` có Laplace Smoothing
- [ ] `score_text()` tính điểm log-probability đúng

---

## MODULE 4 — DỰ ĐOÁN & XUẤT KẾT QUẢ
> **Phụ trách:** Châu Dũng 
> **Trọng số:** Phần 2 (1.0đ) + In kết quả (0.5đ) = **1.5đ**  
> **Dependency:** Module 3 phải hoàn thành  
> **Deadline:** Ngày 4 (ngày hoàn thiện toàn bộ)

### Nhiệm vụ

**4.1 Hàm dự đoán nhãn — `predict(new_text, word_prob, vocab, labels)`**
- Tiền xử lý `new_text` bằng `preprocess()` từ Module 2.
- Tính điểm cho từng nhãn bằng `score_text()` từ Module 3.
- Chọn nhãn có điểm cao nhất (`max(scores, key=scores.get)`).
- Trả về `(nhãn_dự_đoán, dict_điểm)`.

**4.2 In kết quả rõ ràng**

In theo đúng định dạng sau để dễ kiểm tra:

```
============================================================
       HỆ THỐNG PHÂN LOẠI PHẢN HỒI KHÁCH HÀNG
============================================================
Văn bản đầu vào : "Giao hàng nhanh, đóng gói cẩn thận"
Sau tiền xử lý  : ['giao', 'hàng', 'nhanh', 'đóng', 'gói', 'cẩn', 'thận']

--- ĐIỂM SỐ TỪNG NHÓM ---
  Tích cực  : -12.34
  Tiêu cực  : -18.76
  Trung lập : -15.50

--- KẾT QUẢ DỰ ĐOÁN ---
  Nhãn được dự đoán : TÍCH CỰC
  Nhận xét          : Phản hồi mang nội dung tích cực.
============================================================
```

**4.3 Nhận xét tự động theo nhãn**
- Nếu nhãn = `"tích cực"` → in: *"Phản hồi mang nội dung tích cực, khách hàng hài lòng."*
- Nếu nhãn = `"tiêu cực"` → in: *"Phản hồi mang nội dung tiêu cực, cần xem xét cải thiện."*
- Nếu nhãn = `"trung lập"` → in: *"Phản hồi trung lập, không rõ cảm xúc."*

**4.4 Kiểm tra thêm (tùy chọn — tăng điểm báo cáo)**
- Chạy thử dự đoán cho **tất cả văn bản trong training_data** và in kết quả dự đoán vs nhãn thật.
- Đếm số dự đoán đúng / tổng số → tính độ chính xác thủ công.

### Tiêu chí hoàn thành
- [ ] `predict()` trả về nhãn và dict điểm
- [ ] Output in đúng định dạng bảng
- [ ] Có nhận xét tự động theo nhãn
- [ ] Chương trình chạy từ đầu đến cuối không lỗi

---

## LỊCH TRÌNH TỔNG THỂ

```
Ngày 1   [Module 1] Dữ liệu & khai báo đầu vào
Ngày 2   [Module 2] Tiền xử lý văn bản
Ngày 3   [Module 3] Biểu diễn & tính điểm
Ngày 4   [Module 4] Dự đoán & xuất kết quả
Ngày 5   [Review]   Kiểm tra toàn bộ, fix lỗi, tích hợp
Ngày 6   [Report]   Viết báo cáo (bìa, mô tả, kết quả, nhận xét)
Ngày 7   [Submit]   Nộp elearning + kiểm tra lần cuối
```

---

## CHECKLIST NỘP BÀI

| Hạng mục | Trạng thái |
|---|---|
| File `.py` chạy được, không lỗi | ☐ |
| ≥ 10 văn bản mẫu đã khai báo | ☐ |
| 4 module đầy đủ chức năng | ☐ |
| Kết quả in rõ ràng, dễ kiểm tra | ☐ |
| Báo cáo có trang bìa + tên thành viên | ☐ |
| Báo cáo < 10 trang, in 2 mặt | ☐ |
| Nộp bản mềm lên elearning | ☐ |

---

## LƯU Ý QUAN TRỌNG

> ⚠️ **Không được dùng:** `sklearn`, `nltk`, `underthesea`, `pyvi`, `gensim` hoặc bất kỳ thư viện NLP/ML nào.  
> ✅ **Được phép dùng:** `math`, `string`, `os`, các cấu trúc dữ liệu cơ bản của Python.  
> 📌 Mỗi hàm nên có **docstring** mô tả ngắn gọn để dễ giải thích khi trả lời câu hỏi (chiếm 4đ).
