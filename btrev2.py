# -*- coding: utf-8 -*-
"""
HỆ THỐNG TRA CỨU B-TREE TỐI GIẢN (PHIÊN BẢN HỌC TẬP)
---------------------------------------------------
Mục tiêu: Đơn giản nhất có thể để hiểu bản chất thuật toán Bulk Loading
và tìm kiếm trên cây B-Tree tĩnh, không tối ưu phức tạp.
"""

import os
import sys

# Đảm bảo in tiếng Việt không bị lỗi trên Windows Console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')

# =========================================================================
# 1. CLASS BTreeNode ĐƠN GIẢN
# =========================================================================
class BTreeNode:
    def __init__(self, is_leaf=True):
        self.keys = []       # Mảng chứa các từ khóa
        self.children = []   # Mảng chứa các nút con
        self.is_leaf = is_leaf


# =========================================================================
# 2. HÀM BULK LOADING (XÂY DỰNG CÂY TĨNH)
# =========================================================================
def build_static_btree(sorted_list):
    """
    Xây dựng cây B-Tree bậc M=4 tĩnh từ danh sách từ khóa đã sắp xếp.
    Mỗi nút chứa tối đa 3 từ khóa, tối thiểu 1 từ khóa.
    """
    if not sorted_list:
        return None

    # ---- BƯỚC 1: Gom nhóm mảng gốc thành các Nút Lá (Tầng đáy) ----
    leaves = []
    pushed_keys = []
    i = 0
    while i < len(sorted_list):
        # Tạo nút lá chứa tối đa 3 từ khóa (M - 1 = 3)
        leaf = BTreeNode(is_leaf=True)
        leaf.keys = sorted_list[i : i + 3]
        leaves.append(leaf)
        
        i += 3
        # Lấy từ khóa tiếp theo (nếu còn) làm phân vách đẩy lên tầng cha
        if i < len(sorted_list):
            pushed_keys.append(sorted_list[i])
            i += 1  # Bỏ qua từ khóa đã đẩy lên

    # ---- BƯỚC 2 & 3: Rút từ khóa làm Nút Cha và lặp đệ quy ngược lên ----
    current_nodes = leaves
    current_keys = pushed_keys
    
    while len(current_nodes) > 1:
        next_nodes = []
        next_keys = []
        
        idx_child = 0
        idx_key = 0
        while idx_child < len(current_nodes):
            # Tạo nút cha chứa tối đa 4 nút con
            parent = BTreeNode(is_leaf=False)
            parent.children = current_nodes[idx_child : idx_child + 4]
            num_children = len(parent.children)
            
            # Nút cha này sẽ chứa các khóa tương ứng ở giữa các nút con
            parent.keys = current_keys[idx_key : idx_key + num_children - 1]
            next_nodes.append(parent)
            
            idx_child += 4
            idx_key += num_children
            
            # Lấy khóa phân vách tiếp theo đẩy lên tầng cao hơn nữa
            if idx_key - 1 < len(current_keys):
                next_keys.append(current_keys[idx_key - 1])
                
        current_nodes = next_nodes
        current_keys = next_keys
        
    return current_nodes[0]  # Trả về nút duy nhất còn lại làm Root


# =========================================================================
# 3. HÀM TÌM KIẾM TRÊN CÂY (SEARCH)
# =========================================================================
def search_btree(node, key):
    """
    Tìm kiếm đệ quy từ khóa 'key' trên cây B-Tree từ nút hiện tại.
    """
    i = 0
    # 1. Tìm vị trí của từ khóa trong nút hiện tại
    while i < len(node.keys) and key > node.keys[i]:
        i += 1
        
    # 2. Nếu tìm thấy từ khóa ở nút này, trả về kết quả luôn
    if i < len(node.keys) and key == node.keys[i]:
        return f"Tìm thấy từ '{key}' tại nút này!"
        
    # 3. Nếu không tìm thấy và đây là nút lá -> Từ khóa không tồn tại
    if node.is_leaf:
        return "Không tìm thấy"
        
    # 4. Nếu chưa phải nút lá, đi xuống nút con tương ứng để tìm tiếp
    return search_btree(node.children[i], key)


# =========================================================================
# 4. CHƯƠNG TRÌNH CHẠY THỬ
# =========================================================================
if __name__ == "__main__":
    file_path = "Viet11K.txt"
    if not os.path.exists(file_path):
        print(f"Không tìm thấy file '{file_path}'!")
        sys.exit(1)
        
    # Đọc dữ liệu từ file
    with open(file_path, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]
        
    # Sắp xếp từ điển theo chuẩn so sánh của Python
    sorted_words = sorted(list(set(words)))
    
    print(f"Đã nạp {len(sorted_words):,} từ từ '{file_path}'.")
    print("Đang xây dựng cây B-Tree bậc M=4 bằng Bulk Loading...")
    root = build_static_btree(sorted_words)
    print("Xây dựng cây B-Tree thành công!")
    
    # Vòng lặp cho người dùng gõ từ tra cứu
    while True:
        try:
            query = input("\nNhập từ cần tra cứu (hoặc gõ 'exit' để thoát): ").strip()
            if not query or query.lower() == 'exit':
                print("Tạm biệt!")
                break
                
            result = search_btree(root, query)
            print(f"Kết quả: {result}")
        except (KeyboardInterrupt, EOFError):
            print("\nTạm biệt!")
            break
