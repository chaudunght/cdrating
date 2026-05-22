Nếu mục tiêu của bạn **chỉ là xây dựng cây một lần để lưu trữ và truy vấn** (dữ liệu tĩnh - Read-only), thì bạn có thể bỏ qua toàn bộ những phần phức tạp nhất của B-Tree như: hàm Delete (Xóa), cơ chế Borrow (Mượn phần tử khi thiếu hụt), hay Merge (Gộp nút).

Tuy nhiên, thay vì xây dựng cây bằng cách chèn (Insert) từng từ một từ đầu đến cuối như cây động (mất công kiểm tra tràn nút, chia tách nút liên tục), người ta sẽ dùng một kỹ thuật tối ưu hơn rất nhiều gọi là **Bulk Loading (Nạp dữ liệu hàng loạt)**.

Quy trình xây dựng một cây B-Tree tĩnh từ 10,000 từ có sẵn sẽ diễn ra theo trình tự tối ưu sau:

---

## Giai đoạn 1: Chuẩn bị dữ liệu (Bắt buộc)

### 1. Sắp xếp dữ liệu gốc (Sort)

* Sắp xếp toàn bộ 10,000 từ của bạn theo thứ tự từ điển (A-Z).
* *Tại sao cần?* Vì dữ liệu đã sắp xếp giúp chúng ta có thể xây dựng cây B-Tree theo cơ chế **đắp từ trái qua phải, từ dưới lên trên** một cách tuần tự mà không bao giờ sợ nút bị mất cân bằng.

---

## Giai đoạn 2: Quy trình Nạp hàng loạt (Bulk Loading)

Thay vì tạo một cây trống rồi chèn từng từ, bạn sẽ tính toán và chia cắt mảng dữ liệu đã sort trực tiếp thành các khối (Nút).

Giả sử bạn chọn xây dựng **B-Tree bậc $M=4$** (Mỗi nút chứa tối đa 3 từ khóa, tối thiểu 1 từ khóa).

1. **Gom nhóm mảng gốc thành các Nút Lá:** Tầng đáy.
Cắt mảng 10,000 từ đã sort thành các đoạn nhỏ, mỗi đoạn chứa tối đa 3 từ khóa. Mỗi đoạn này chính là một nút lá (is_leaf = True).
*Ví dụ: [A, B, C], [D, E, F], [G, H, I]...*


2. **Rút từ khóa làm Nút Cha (Tầng trên):** Trích xuất chỉ mục.
Để liên kết các nút lá lại, ta lấy phần tử đầu tiên (hoặc cuối cùng) của các nút lá phía sau để đẩy lên làm từ khóa định hướng cho nút cha.
*Ví dụ: Rút chữ D, G đẩy lên tầng trên để tạo nút cha [D, G]. Nút cha này sẽ giữ con trỏ trỏ xuống 3 nút lá ở Bước 1.*


3. **Lặp lại quy trình cho đến khi còn 1 Nút Gốc:** Đệ quy ngược lên.
Tiếp tục gom nhóm các nút cha vừa tạo ở Bước 2 thành các nút ở tầng cao hơn nữa. Quá trình này dừng lại khi tầng trên cùng chỉ còn lại duy nhất **1 nút**. Nút đó chính là Root.


> **Ưu điểm vượt trội:** Cách xây dựng này đạt độ phức tạp thời gian là $\mathcal{O}(N)$ (nếu dữ liệu đã sort sẵn), nhanh hơn rất nhiều so với việc chèn từng phần tử $\mathcal{O}(N \log N)$ và các nút của bạn sẽ được lấp đầy bộ nhớ 100%, không bị lãng phí các ô trống trong mảng.

---

## Giai đoạn 3: Viết hàm Truy vấn (Search)

Vì cây của bạn không bao giờ thay đổi cấu trúc, hàm truy vấn lúc này cực kỳ ngắn gọn và chạy rất nhanh.

```python
def search_btree(node, key):
    i = 0
    # 1. Tìm vị trí của từ khóa trong nút hiện tại
    while i < len(node.keys) and key > node.keys[i]:
        i += 1
        
    # 2. Nếu tìm thấy từ khóa ở nút này, trả về kết quả luôn
    if i < len(node.keys) and key == node.keys[i]:
        return f"Tìm thấy từ {key} tại nút này!"
        
    # 3. Nếu không tìm thấy và đây là nút lá -> Từ khóa không tồn tại
    if node.is_leaf:
        return "Không tìm thấy"
        
    # 4. Nếu chưa phải nút lá, đi xuống nút con tương ứng để tìm tiếp
    return search_btree(node.children[i], key)

```

## Tóm lại, code của bạn sẽ chỉ cần:

1. Một Class BTreeNode đơn giản (chỉ chứa mảng keys, children, và biến is_leaf).
2. Một hàm build_static_btree(sorted_list) chạy đúng 3 bước của quy trình Bulk Loading để trả về nút Root.
3. Hàm search_btree(root, key) để người dùng gõ từ và tìm kiếm.

Quy trình giản lược này giúp bạn giữ lại trọn vẹn sức mạnh truy vấn siêu tốc của B-Tree, thể hiện được tư duy cấu trúc dữ liệu nâng cao mà lại tiết kiệm được 70% công sức viết code so với một cây B-Tree đầy đủ.