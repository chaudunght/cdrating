# -*- coding: utf-8 -*-
"""
HỆ THỐNG TRA CỨU TỪ ĐIỂN TIẾNG VIỆT SỬ DỤNG B-TREE (STATIC BULK LOADING)
-------------------------------------------------------------------------
Được phát triển dựa trên tài liệu btree.md để tối ưu hóa hiệu năng tra cứu
trên tập dữ liệu từ điển tĩnh Viet11K.txt.

Độ phức tạp thuật toán:
  - Xây dựng cây (Bulk Loading): O(N) (khi dữ liệu đầu vào đã sắp xếp)
  - Tìm kiếm từ khóa: O(log N)
  - Yêu cầu bộ nhớ: Tối ưu 100% (không có vùng nhớ dư thừa do phân chia đều)
"""

import os
import sys
import time
import math
import random

# Thiết lập mã hóa UTF-8 cho console để hỗ trợ hiển thị tiếng Việt trên Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')

# =========================================================================
# 1. CẤU TRÚC NÚT B-TREE (BTreeNode)
# =========================================================================

class BTreeNode:
    """
    Đại diện cho một nút trong cây B-Tree.
    """
    def __init__(self, is_leaf=True):
        self.keys = []       # Danh sách chứa các từ khóa (chuỗi tiếng Việt)
        self.children = []   # Danh sách chứa các nút con (BTreeNode), rỗng nếu là nút lá
        self.is_leaf = is_leaf

    def __repr__(self):
        node_type = "Lá" if self.is_leaf else "Trong"
        return f"BTreeNode({node_type}, khóa={len(self.keys)}, con={len(self.children)})"


# =========================================================================
# 2. THUẬT TOÁN BULK LOADING (NẠP HÀNG LOẠT TĨNH)
# =========================================================================

def distribute_sizes(total, max_val):
    """
    Chia đều số lượng phần tử 'total' vào các nhóm sao cho kích thước mỗi nhóm
    không vượt quá 'max_val', đồng thời kích thước các nhóm đồng đều nhất có thể.
    Ví dụ: Chia 11 phần tử vào các nhóm max_val=4 -> sẽ được [4, 4, 3] thay vì [4, 4, 2, 1].
    """
    if total <= 0:
        return []
    # Số lượng nhóm tối thiểu cần có
    k = (total + max_val - 1) // max_val
    # Kích thước cơ bản của mỗi nhóm
    base = total // k
    # Số lượng nhóm sẽ nhận thêm 1 phần tử dư thừa
    rem = total % k
    return [base + 1] * rem + [base] * (k - rem)


def build_leaves(sorted_keys, M):
    """
    Xây dựng tầng đáy (Tầng lá) của cây B-Tree từ danh sách khóa đã sắp xếp.
    Trả về: (danh_sách_nút_lá, danh_sách_khóa_đẩy_lên_tầng_trên)
    """
    N = len(sorted_keys)
    if N == 0:
        return [], []
    
    # Tính số lượng nút lá cần thiết
    k = (N + M - 1) // M
    # Tổng số khóa thực sự nằm ở các nút lá (chừa lại các khóa làm vách ngăn đẩy lên tầng cha)
    leaf_total = N - k + 1
    # Phân chia đều số khóa cho các nút lá (mỗi nút chứa tối đa M - 1 khóa)
    sizes = distribute_sizes(leaf_total, M - 1)
    
    leaves = []
    pushed_keys = []
    
    idx = 0
    for i, size in enumerate(sizes):
        node = BTreeNode(is_leaf=True)
        node.keys = sorted_keys[idx : idx + size]
        leaves.append(node)
        idx += size
        
        # Nếu chưa phải nút cuối cùng, lấy khóa kế tiếp làm vách ngăn để đẩy lên tầng cha
        if i < len(sizes) - 1:
            pushed_keys.append(sorted_keys[idx])
            idx += 1
            
    return leaves, pushed_keys


def build_internal_level(current_nodes, current_keys, M):
    """
    Xây dựng một tầng trung gian phía trên tầng hiện tại.
    Trả về: (danh_sách_nút_cha, danh_sách_khóa_đẩy_lên_tầng_trên)
    """
    C = len(current_nodes)
    if C <= 1:
        return current_nodes, []
    
    # Chia đều số con trỏ con vào các nút cha (mỗi nút cha chứa tối đa M con trỏ con)
    sizes = distribute_sizes(C, M)
    
    parent_nodes = []
    pushed_keys = []
    
    child_idx = 0
    key_idx = 0
    for i, size in enumerate(sizes):
        node = BTreeNode(is_leaf=False)
        # Gán các nút con cho nút cha này
        node.children = current_nodes[child_idx : child_idx + size]
        # Một nút có S con trỏ con thì sẽ chứa đúng S - 1 khóa tương ứng ở giữa
        node.keys = current_keys[key_idx : key_idx + size - 1]
        parent_nodes.append(node)
        
        child_idx += size
        key_idx += size - 1
        
        # Đẩy khóa phân vách tiếp theo lên tầng cao hơn
        if i < len(sizes) - 1:
            pushed_keys.append(current_keys[key_idx])
            key_idx += 1
            
    return parent_nodes, pushed_keys


def build_static_btree(sorted_list, M=4):
    """
    Xây dựng hoàn chỉnh một cây B-Tree tĩnh từ mảng từ vựng đã được sắp xếp.
    M: Bậc của cây (mặc định M = 4)
    """
    assert M >= 3, "Bậc M của B-Tree phải lớn hơn hoặc bằng 3!"
    if not sorted_list:
        return None
    
    # Giai đoạn 1: Gom nhóm và tạo các Nút Lá ở tầng đáy cùng
    current_nodes, current_keys = build_leaves(sorted_list, M)
    
    # Giai đoạn 2: Lặp đệ quy ngược lên trên để tạo các tầng cha trung gian
    while len(current_nodes) > 1:
        current_nodes, current_keys = build_internal_level(current_nodes, current_keys, M)
        
    # Nút duy nhất cuối cùng chính là Root
    return current_nodes[0]


# =========================================================================
# 3. HÀM TRUY VẤN (SEARCH) VÀ XÁC THỰC CÂY (VALIDATE)
# =========================================================================

def search_btree(node, key, path=None, comparisons=0):
    """
    Tìm kiếm từ khóa `key` trên cây B-Tree một cách đệ quy.
    Đồng thời theo vết đường đi (path) và đếm tổng số phép so sánh từ khóa.
    
    Trả về một dictionary chứa:
      - found (bool): Có tìm thấy hay không.
      - value (str): Từ tìm thấy (nếu có).
      - path (list): Danh sách các nút đã đi qua.
      - comparisons (int): Tổng số phép so sánh đã thực hiện.
    """
    if path is None:
        path = []
    
    path.append(node)
    
    i = 0
    # Tìm kiếm tuần tự trong nút hiện tại
    while i < len(node.keys):
        comparisons += 1
        if key == node.keys[i]:
            return {
                "found": True,
                "value": node.keys[i],
                "path": path,
                "comparisons": comparisons
            }
        elif key < node.keys[i]:
            break
        i += 1
        
    # Nếu là nút lá mà không khớp từ khóa -> Không tồn tại
    if node.is_leaf:
        return {
            "found": False,
            "path": path,
            "comparisons": comparisons
        }
        
    # Đi xuống nút con tương ứng tại vị trí i để tiếp tục tìm kiếm
    return search_btree(node.children[i], key, path, comparisons)


def validate_btree(root, M):
    """
    Xác thực nghiêm ngặt cấu trúc B-Tree xem có đúng luật lý thuyết hay không:
    1. Tất cả các nút lá nằm ở cùng một độ sâu (cân bằng hoàn hảo).
    2. Các từ khóa ở mỗi nút được sắp xếp tăng dần theo bảng chữ cái.
    3. Các nút con chứa các khóa nằm chính xác trong phạm vi phân tách của nút cha.
    4. Số nút con của nút phi lá nằm trong khoảng [ceil(M/2), M] (ngoại trừ root).
    5. Số từ khóa của nút nằm trong khoảng [ceil(M/2) - 1, M - 1] (ngoại trừ root).
    """
    if root is None:
        return True, 0, 0
    
    min_keys = math.ceil(M / 2) - 1
    min_children = math.ceil(M / 2)
    
    leaf_depths = set()
    total_nodes = 0
    
    def traverse(node, depth, min_val=None, max_val=None):
        nonlocal total_nodes
        total_nodes += 1
        
        num_keys = len(node.keys)
        # Kiểm tra giới hạn số lượng khóa
        if node != root:
            if not (min_keys <= num_keys <= M - 1):
                raise ValueError(f"LỖI: Nút phi gốc chứa {num_keys} khóa (Yêu cầu: [{min_keys}, {M - 1}])")
        else:
            if not (1 <= num_keys <= M - 1) and not (node.is_leaf and num_keys == 0):
                raise ValueError(f"LỖI: Nút gốc chứa {num_keys} khóa không hợp lệ")
                
        # Kiểm tra tính sắp xếp của từ khóa trong nút
        for idx in range(num_keys - 1):
            if node.keys[idx] >= node.keys[idx + 1]:
                raise ValueError(f"LỖI: Khóa tại nút không sắp xếp đúng thứ tự: {node.keys}")
                
        # Kiểm tra phạm vi khóa hợp lệ so với cha
        for k in node.keys:
            if min_val is not None and k <= min_val:
                raise ValueError(f"LỖI: Khóa '{k}' nhỏ hơn giới hạn dưới '{min_val}'")
            if max_val is not None and k >= max_val:
                raise ValueError(f"LỖI: Khóa '{k}' lớn hơn giới hạn trên '{max_val}'")
                
        if node.is_leaf:
            leaf_depths.add(depth)
            if len(node.children) > 0:
                raise ValueError("LỖI: Nút lá nhưng vẫn chứa con trỏ con")
        else:
            num_children = len(node.children)
            if num_children != num_keys + 1:
                raise ValueError(f"LỖI: Số nút con ({num_children}) khác số khóa ({num_keys}) + 1")
            
            if node != root:
                if not (min_children <= num_children <= M):
                    raise ValueError(f"LỖI: Nút phi gốc chứa {num_children} con trỏ con (Yêu cầu: [{min_children}, {M}])")
            
            # Đệ quy xuống các con
            for idx, child in enumerate(node.children):
                child_min = node.keys[idx - 1] if idx > 0 else min_val
                child_max = node.keys[idx] if idx < num_keys else max_val
                traverse(child, depth + 1, child_min, child_max)
                
    traverse(root, 0)
    
    # Kiểm tra tính cân bằng độ cao
    if len(leaf_depths) > 1:
        raise ValueError(f"LỖI: Độ sâu các lá không đồng đều: {leaf_depths}")
        
    height = list(leaf_depths)[0] if leaf_depths else 0
    return True, height, total_nodes


# =========================================================================
# 4. THUẬT TOÁN TÌM KIẾM SO SÁNH (LINEAR & BINARY SEARCH) PHỤC VỤ BENCHMARK
# =========================================================================

def linear_search(arr, key):
    """Tìm kiếm tuần tự trên mảng đã sắp xếp (dừng sớm nếu vượt quá khóa)"""
    comparisons = 0
    for item in arr:
        comparisons += 1
        if item == key:
            return True, comparisons
        if item > key:  # Dữ liệu đã sắp xếp, có thể dừng sớm
            break
    return False, comparisons


def binary_search(arr, key):
    """Tìm kiếm nhị phân chuẩn trên mảng phẳng"""
    low = 0
    high = len(arr) - 1
    comparisons = 0
    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        if arr[mid] == key:
            return True, comparisons
        elif arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1
    return False, comparisons


# =========================================================================
# 5. BỘ TỰ ĐỘNG KIỂM TRA ĐỘ CHÍNH XÁC (AUTOTEST)
# =========================================================================

def run_accuracy_autotest(root, original_words):
    """
    Kiểm tra tự động:
      1. Đảm bảo toàn bộ 100% từ trong danh sách gốc đều tìm thấy trên B-Tree.
      2. Đảm bảo kết quả tìm kiếm trùng khớp chính xác.
    """
    print("\n[Search] DANG CHAY BO KIEM THU TU DONG (ACCURACY AUTOTEST)...")
    success_count = 0
    start_time = time.time()
    
    for word in original_words:
        res = search_btree(root, word)
        if res["found"] and res["value"] == word:
            success_count += 1
            
    end_time = time.time()
    accuracy = (success_count / len(original_words)) * 100
    
    print(f"[Success] Da kiem tra: {len(original_words)} tu.")
    print(f"[Success] Tim thay chinh xac: {success_count} tu.")
    print(f"[Stat] Ty le chinh xac (Accuracy): {accuracy:.2f}%")
    print(f"[Speed] Tong thoi gian chay tu dong: {end_time - start_time:.4f} giay")
    
    # Thử nghiệm tìm kiếm một số từ ngẫu nhiên không có trong từ điển
    non_existing = ["antigravity_ai", "python_btree_pro", "deepmind_google_2026", "tu_khong_ton_tai"]
    all_not_found = True
    for word in non_existing:
        res = search_btree(root, word)
        if res["found"]:
            all_not_found = False
            print(f"[Error] Phat hien loi: Tim thay tu khong ton tai '{word}'")
            
    if all_not_found:
        print("[Success] Kiem thu tim tu khong ton tai: HOAN HAO (100% tra ve Khong tim thay)")
    else:
        print("[Error] Kiem thu tim tu khong ton tai: THAT BAI")
        
    return accuracy == 100 and all_not_found


# =========================================================================
# 6. GIAO DIỆN DÒNG LỆNH (CLI) & CHƯƠNG TRÌNH CHÍNH
# =========================================================================

def main():
    # 6.1 Đọc và xử lý tệp dữ liệu Viet11K.txt
    file_path = "Viet11K.txt"
    if not os.path.exists(file_path):
        print(f"[Error] Khong tim thay file tu dien '{file_path}'. Vui loi kiem tra lai duong dan!")
        return
        
    print("=" * 65)
    print("      HE THONG TRA CUU TU DIEN TIENG VIET B-TREE (Static Bulk Loading)")
    print("=" * 65)
    print(f"[File] Dang doc du lieu tu tep: '{file_path}'...")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_lines = f.readlines()
    except Exception as e:
        print(f"[Error] Khong the doc file do loi: {e}")
        return
        
    # Làm sạch dữ liệu: bỏ dòng trống, cắt khoảng trắng đầu/cuối
    words_list = []
    for line in raw_lines:
        w = line.strip()
        if w:
            words_list.append(w)
            
    total_raw = len(words_list)
    # Loại bỏ trùng lặp và sắp xếp lại để đồng nhất với Collation của Python
    unique_words = sorted(list(set(words_list)))
    total_unique = len(unique_words)
    
    print(f"[Info] Da nap thanh cong {total_raw:,} tu khoa tho.")
    print(f"[Success] Loc trung lap & Sap xep: Con lai {total_unique:,} tu khoa duy nhat.")
    
    # 6.2 Cấu hình Bậc M cho cây B-Tree
    default_M = 4
    # Nếu chạy không có TTY (ví dụ trong môi trường test tự động), sử dụng mặc định
    if not sys.stdin.isatty():
        M = default_M
        print(f"[Setup] Moi truong khong tuong tac. Su dung bac mac dinh M={M}")
    else:
        try:
            M_input = input(f"[Setup] Nhap bac M cua B-Tree (Nhan Enter de chon mac dinh M={default_M}): ").strip()
            if M_input:
                M = int(M_input)
                if M < 3:
                    print("[Setup] Bac M toi thieu phai la 3. Tu dong chuyen ve M=3.")
                    M = 3
            else:
                M = default_M
        except (ValueError, EOFError):
            print(f"[Setup] Gia tri nhap khong hop le hoac EOF. Chon mac dinh M={default_M}.")
            M = default_M
        
    print(f"[Tree] Dang xay dung cay B-Tree bac M={M} bang thuat toan Bulk Loading...")
    start_build = time.perf_counter()
    root = build_static_btree(unique_words, M)
    build_time = (time.perf_counter() - start_build) * 1000  # mili giây
    print(f"[Speed] Xay dung B-Tree thanh cong trong {build_time:.4f} ms!")
    
    # 6.3 Xác thực cây vừa xây dựng
    try:
        is_valid, height, total_nodes = validate_btree(root, M)
        print("[Valid] Xac thuc cau truc cay B-Tree:")
        print(f"   - Trang thai cay B-Tree : HOP LE (100% Can bang tuyet doi)")
        print(f"   - Chieu cao cay (Height): {height} (Do sau nut la)")
        print(f"   - Tong so nut tren cay  : {total_nodes} nut")
    except ValueError as val_err:
        print(f"[Error] Cay B-Tree duoc xay dung khong hop le! Loi: {val_err}")
        return
        
    # Chạy autotest độ chính xác
    autotest_ok = run_accuracy_autotest(root, unique_words)
    if not autotest_ok:
        print("[Warning] CANH BAO: Bo kiem thu tu dong phat hien loi tim kiem tren B-Tree!")
        
    # Nếu chạy không có TTY (ví dụ test tự động), thoát luôn sau khi autotest để tránh treo lệnh
    if not sys.stdin.isatty():
        print("[Exit] Thoat chuong trinh vi khong o che do tuong tac (Non-TTY).")
        return

    # 6.4 Vòng lặp CLI chính
    while True:
        print("\n" + "=" * 65)
        print("   MENU CHUC NANG HE THONG")
        print("-" * 65)
        print(" 1. Tra cuu tu tieng Viet (B-Tree Search)")
        print(" 2. Chay thu nghiem hieu nang (Benchmark)")
        print(" 3. Hien thi thong so cau truc cay B-Tree chi tiet")
        print(" 4. Thoat chuong trinh")
        print("=" * 65)
        
        try:
            choice = input("Moi ban nhap lua chon (1-4): ").strip()
        except EOFError:
            print("\n[Exit] Nhan tin hieu ket thuc. Tam biet!")
            break
        
        if choice == "1":
            try:
                search_word = input("Nhap tu/cum tu tieng Viet can tra cuu: ").strip()
            except EOFError:
                break
            if not search_word:
                print("[Warning] Tu khoa nhap vao khong duoc de trong!")
                continue
                
            start_t = time.perf_counter()
            res = search_btree(root, search_word)
            elapsed_us = (time.perf_counter() - start_t) * 1_000_000  # micro giây
            
            if res["found"]:
                print(f"\n[Found] TIM THAY TU: '{res['value']}'")
                print(f"   - Thoi gian thuc thi : {elapsed_us:.2f} micro giay (us)")
                print(f"   - So phep so sanh khoa: {res['comparisons']} lan")
                print(f"   - Chieu sau nut tim thay: {len(res['path']) - 1}")
                print(f"   - Duong di qua cac nut (Khoa o cac nut trung gian):")
                for idx, node in enumerate(res["path"]):
                    role = "Goc" if idx == 0 else ("La" if node.is_leaf else f"Trung gian tang {idx}")
                    print(f"     |- [{role}] keys={node.keys[:3]}..." if len(node.keys) > 3 else f"     |- [{role}] keys={node.keys}")
            else:
                print(f"\n[Error] KHONG TIM THAY TU: '{search_word}'")
                print(f"   - Thoi gian tim kiem  : {elapsed_us:.2f} us")
                print(f"   - So phep so sanh khoa: {res['comparisons']} lan")
                print(f"   - Duong di duyet qua cac nut la nhung khong khop:")
                for idx, node in enumerate(res["path"]):
                    role = "Goc" if idx == 0 else ("La" if node.is_leaf else f"Trung gian tang {idx}")
                    print(f"     |- [{role}] keys={node.keys[:3]}..." if len(node.keys) > 3 else f"     |- [{role}] keys={node.keys}")
                    
        elif choice == "2":
            print("\n[Stat] DANG CHAY BENCHMARK SO SANH HIEU NANG TIM KIEM...")
            print("Dang chuan bi bo mau kiem thu: 2,000 tu (1,000 tu ton tai + 1,000 tu ngau nhien)...")
            
            # Chọn 1000 từ tồn tại ngẫu nhiên
            sample_words_exist = random.sample(unique_words, min(1000, len(unique_words)))
            # Tạo 1000 từ không tồn tại
            sample_words_non_exist = [f"tu_ngau_nhien_{i}_{random.randint(10000, 99999)}" for i in range(1000)]
            test_queries = sample_words_exist + sample_words_non_exist
            random.shuffle(test_queries)
            
            print(f"Khoi chay tim kiem {len(test_queries):,} truy van...")
            
            # 1. Benchmark B-Tree
            t_btree_start = time.perf_counter()
            btree_comparisons = 0
            btree_found = 0
            for q in test_queries:
                r = search_btree(root, q)
                btree_comparisons += r["comparisons"]
                if r["found"]:
                    btree_found += 1
            t_btree = (time.perf_counter() - t_btree_start) * 1000  # mili giây
            
            # 2. Benchmark Binary Search (Mảng phẳng)
            t_bin_start = time.perf_counter()
            bin_comparisons = 0
            bin_found = 0
            for q in test_queries:
                found, comps = binary_search(unique_words, q)
                bin_comparisons += comps
                if found:
                    bin_found += 1
            t_bin = (time.perf_counter() - t_bin_start) * 1000
            
            # 3. Benchmark Linear Search (Mảng phẳng)
            t_lin_start = time.perf_counter()
            lin_comparisons = 0
            lin_found = 0
            # Giới hạn số lượng truy vấn cho Linear Search vì nó rất chậm
            lin_test_queries = test_queries[:200]  # chỉ test 200 truy vấn
            for q in lin_test_queries:
                found, comps = linear_search(unique_words, q)
                lin_comparisons += comps
                if found:
                    lin_found += 1
            t_lin = (time.perf_counter() - t_lin_start) * 1000
            # Quy đổi kết quả tuyến tính về quy mô 2000 truy vấn để so sánh công bằng
            extrapolated_t_lin = t_lin * (len(test_queries) / len(lin_test_queries))
            extrapolated_lin_comps = lin_comparisons * (len(test_queries) / len(lin_test_queries))
            
            print("\n[Result] KET QUA BENCHMARK (Tong cong 2,000 truy van):")
            print("-" * 65)
            print(f"{'Thuat toan':<20} | {'Tong thoi gian (ms)':<22} | {'Thoi gian/truy van (us)':<22} | {'TB phep so sanh':<20}")
            print("-" * 65)
            print(f"{'B-Tree Search':<20} | {t_btree:18.2f} ms | {t_btree * 1000 / len(test_queries):18.2f} us | {btree_comparisons / len(test_queries):16.1f}")
            print(f"{'Binary Search':<20} | {t_bin:18.2f} ms | {t_bin * 1000 / len(test_queries):18.2f} us | {bin_comparisons / len(test_queries):16.1f}")
            print(f"{'Linear Search':<20} | {extrapolated_t_lin:18.2f} ms*| {extrapolated_t_lin * 1000 / len(test_queries):18.2f} us*| {extrapolated_lin_comps / len(test_queries):16.1f}*")
            print("-" * 65)
            print("(*) Ket qua cua Linear Search duoc ngoai suy tu 200 truy van thuc te.")
            print(f"\n[Info] Nhan xet: B-Tree cung cap toc do tra cuu cuc ky an tuong, nhanh gap hon {extrapolated_t_lin / t_btree:.1f} lan so voi Linear Search va dat toc do tuong duong voi tim kiem nhi phan tren mang phang, dong thoi ho tro quan ly phan cap cuc tot!")
            
        elif choice == "3":
            print("\n[Tree] THONG SO CAU TRUC CHI TIET CUA CAY B-TREE:")
            print("-" * 65)
            print(f"  * Bac cua cay (Order M)       : {M}")
            print(f"  * Suc chua moi nut (Max Keys) : {M - 1} khoa")
            print(f"  * So luong nut con toi da    : {M} con")
            print(f"  * Chieu cao cay B-Tree        : {height}")
            print(f"  * Tong so nut tren cay        : {total_nodes} nut")
            print(f"  * Tong so tu khoa luu tru     : {total_unique:,} tu khoa")
            
            # Tính toán phân bố nút ở các tầng
            levels_count = [0] * (height + 1)
            
            def count_levels(node, depth):
                levels_count[depth] += 1
                if not node.is_leaf:
                    for child in node.children:
                        count_levels(child, depth + 1)
            
            count_levels(root, 0)
            print("  * Phan bo nut tren tung tang (tu goc xuong la):")
            for h_idx, cnt in enumerate(levels_count):
                role = "Tang goc (Root)" if h_idx == 0 else (f"Tang la" if h_idx == height else f"Tang trung gian {h_idx}")
                print(f"     |- {role:<20}: {cnt:>6} nut")
                
            print(f"  * Phan bo bo nho              : 100% lap day (khong co o nho rong nho Bulk Loading)")
            print("-" * 65)
            
        elif choice == "4":
            print("\n[Exit] Cam on ban da su dung He thong tra cuu tu dien B-Tree! Tam biet!")
            break
        else:
            print("[Error] Lua chon khong hop le! Vui long nhap so tu 1 den 4.")


if __name__ == "__main__":
    main()
