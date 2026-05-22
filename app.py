import math
import streamlit as st
import pandas as pd
from data import training_data as initial_data

# ==========================================
# CẤU HÌNH TRANG & GIAO DIỆN PREMIUM
# ==========================================
st.set_page_config(
    page_title="Phân loại Phản hồi Khách hàng - Python NLP Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Nhúng Google Font và Custom CSS để tạo giao diện tuyệt đẹp
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        /* CSS Reset & Font */
        html, body, [class*="css"], .stApp {
            font-family: 'Outfit', sans-serif !important;
            background-color: #f8fafc;
        }
        
        /* Custom Premium Cards */
        .custom-card {
            background-color: #ffffff;
            border-radius: 24px;
            padding: 24px;
            box-shadow: 0 4px 20px -2px rgba(50, 50, 93, 0.05), 0 2px 8px -1px rgba(0, 0, 0, 0.02);
            border: 1px solid #e2e8f0;
            margin-bottom: 24px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .custom-card:hover {
            box-shadow: 0 10px 30px -5px rgba(50, 50, 93, 0.08), 0 4px 12px -2px rgba(0, 0, 0, 0.03);
            border-color: #cbd5e1;
        }
        
        /* Banner Header */
        .banner-container {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border-radius: 24px;
            padding: 32px;
            color: #ffffff;
            border: 1px solid #334155;
            margin-bottom: 24px;
            position: relative;
            overflow: hidden;
        }
        .banner-container::before {
            content: "";
            position: absolute;
            top: -50%;
            right: -20%;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
            pointer-events: none;
        }
        .banner-title {
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 8px;
            background: linear-gradient(to right, #ffffff, #e2e8f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .banner-subtitle {
            color: #94a3b8;
            font-size: 1.05rem;
            max-width: 800px;
            line-height: 1.6;
        }
        
        /* Custom Badges */
        .custom-badge {
            display: inline-flex;
            align-items: center;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            border: 1px solid transparent;
            margin-right: 6px;
            margin-bottom: 6px;
        }
        .badge-primary { background-color: #eff6ff; color: #1d4ed8; border-color: #dbeafe; }
        .badge-outline { background-color: transparent; color: #64748b; border-color: #e2e8f0; }
        
        .badge-tich-cuc { background-color: #ecfdf5; color: #047857; border-color: #d1fae5; }
        .badge-tieu-cuc { background-color: #fff1f2; color: #be123c; border-color: #ffe4e6; }
        .badge-trung-lap { background-color: #f1f5f9; color: #475569; border-color: #e2e8f0; }
        
        /* Preprocessing Step Blocks */
        .step-block {
            background-color: #ffffff;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            padding: 16px;
            height: 100%;
        }
        .step-block-title {
            font-size: 0.9rem;
            font-weight: 600;
            color: #64748b;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .step-block-content {
            background-color: #f8fafc;
            border-radius: 12px;
            padding: 12px;
            font-size: 0.95rem;
            color: #1e293b;
            min-height: 50px;
            border: 1px dashed #cbd5e1;
            word-wrap: break-word;
        }
        
        /* Custom Vocab List Container */
        .vocab-container {
            max-height: 260px;
            overflow-y: auto;
            background-color: #f8fafc;
            border-radius: 12px;
            padding: 12px;
            border: 1px solid #e2e8f0;
        }
        
        /* Custom Progress Bars */
        .progress-container {
            margin-bottom: 16px;
        }
        .progress-label {
            display: flex;
            justify-content: space-between;
            font-size: 0.9rem;
            font-weight: 600;
            color: #334155;
            margin-bottom: 6px;
            text-transform: capitalize;
        }
        .progress-bar-outer {
            height: 12px;
            background-color: #e2e8f0;
            border-radius: 9999px;
            overflow: hidden;
            position: relative;
        }
        .progress-bar-inner {
            height: 100%;
            border-radius: 9999px;
            transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .bar-tich-cuc { background: linear-gradient(90deg, #10b981, #059669); }
        .bar-tieu-cuc { background: linear-gradient(90deg, #f43f5e, #e11d48); }
        .bar-trung-lap { background: linear-gradient(90deg, #64748b, #475569); }
        
        .log-score-label {
            font-size: 0.75rem;
            color: #64748b;
            margin-top: 4px;
        }
        
        /* Table Custom Styling */
        .custom-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
            text-align: left;
        }
        .custom-table th {
            background-color: #f8fafc;
            color: #475569;
            font-weight: 600;
            padding: 12px 16px;
            border-bottom: 2px solid #e2e8f0;
        }
        .custom-table td {
            padding: 12px 16px;
            border-bottom: 1px solid #e2e8f0;
            color: #1e293b;
        }
        .custom-table tr:hover {
            background-color: #f8fafc;
        }
        
        /* Large Conclusion Card */
        .conclusion-card {
            border-radius: 20px;
            padding: 24px;
            text-align: center;
            border: 1px solid;
            transition: all 0.3s;
        }
        .conclusion-tich-cuc {
            background-color: #f0fdf4;
            border-color: #bbf7d0;
            color: #166534;
        }
        .conclusion-tieu-cuc {
            background-color: #fff5f5;
            border-color: #fecaca;
            color: #991b1b;
        }
        .conclusion-trung-lap {
            background-color: #f8fafc;
            border-color: #e2e8f0;
            color: #334155;
        }
        .conclusion-badge {
            display: inline-block;
            font-size: 1.25rem;
            font-weight: 800;
            padding: 6px 20px;
            border-radius: 9999px;
            margin-bottom: 12px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        .conclusion-comment {
            font-size: 1rem;
            font-weight: 500;
            line-height: 1.5;
        }
        
        /* Custom Button Styling */
        div.stButton > button {
            background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%) !important;
            color: white !important;
            border: none !important;
            padding: 10px 24px !important;
            border-radius: 14px !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            box-shadow: 0 4px 10px rgba(79, 70, 229, 0.15) !important;
            transition: all 0.2s !important;
            width: 100%;
        }
        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 15px rgba(79, 70, 229, 0.25) !important;
        }
        div.stButton > button:active {
            transform: translateY(0px) !important;
        }
        
        /* Sidebar or hidden styling */
        #MainMenu, footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# MODULE 2: CÁC HÀM TIỀN XỬ LÝ VĂN BẢN
# ==========================================
import json
import os

# Load dictionary words globally
dict_path = "dictionary.json"
try:
    with open(dict_path, "r", encoding="utf-8") as f:
        DICTIONARY_WORDS = json.load(f)
except Exception:
    DICTIONARY_WORDS = []

# Get compound words, sort by word count descending, then by character length descending
COMPOUND_WORDS = sorted(
    [w.strip().lower() for w in DICTIONARY_WORDS if " " in w.strip()],
    key=lambda x: (-len(x.split()), -len(x))
)

def normalize_lower(text):
    return text.lower()

def remove_punctuation(text):
    punctuations = "!?. ,;:\"'()[]{}/\\-_"
    clean_text = ""
    for char in text:
        if char not in punctuations:
            clean_text += char
        else:
            clean_text += " "
    return clean_text

def remove_extra_spaces(text):
    return " ".join(text.strip().split())

def tokenize(text):
    words = text.split()
    if not words:
        return []
    
    tokens = []
    i = 0
    n = len(words)
    while i < n:
        matched = False
        for k in range(min(5, n - i), 1, -1):
            phrase = " ".join(words[i:i+k])
            if phrase in COMPOUND_WORDS:
                tokens.append(phrase)
                i += k
                matched = True
                break
        if not matched:
            tokens.append(words[i])
            i += 1
    return tokens

def preprocess(text):
    lower = normalize_lower(text or "")
    no_punctuation = remove_punctuation(lower)
    clean_text = remove_extra_spaces(no_punctuation)
    tokens = tokenize(clean_text)
    return {
        "lower": lower,
        "no_punctuation": no_punctuation,
        "clean_text": clean_text,
        "tokens": tokens
    }

# ==========================================
# MODULE 3: BIỂU DIỄN VĂN BẢN & TÍNH TOÁN LOGIC
# ==========================================
def build_vocab(processed_dataset):
    vocab = set()
    for item in processed_dataset:
        for word in item["tokens"]:
            vocab.add(word)
    return sorted(list(vocab))

def build_word_prob(processed_dataset, labels, vocab):
    word_prob = {}
    vocab_size = len(vocab) if len(vocab) > 0 else 1
    
    for label in labels:
        words_in_label = []
        for item in processed_dataset:
            if item["label"] == label:
                words_in_label.extend(item["tokens"])
        
        word_counts = {}
        for word in words_in_label:
            word_counts[word] = word_counts.get(word, 0) + 1
            
        total_words = len(words_in_label)
        probs = {}
        for word in vocab:
            count = word_counts.get(word, 0)
            probs[word] = (count + 1) / (total_words + vocab_size)
            
        word_prob[label] = {
            "probs": probs,
            "word_counts": word_counts,
            "total_words": total_words
        }
    return word_prob

def score_text(tokens, word_prob, labels):
    log_scores = {}
    for label in labels:
        score = 0
        for word in tokens:
            if label in word_prob and word in word_prob[label]["probs"]:
                score += math.log(word_prob[label]["probs"][word])
        log_scores[label] = score
        
    # Softmax normalization
    if log_scores:
        max_log = max(log_scores.values())
        exp_scores = {label: math.exp(score - max_log) for label, score in log_scores.items()}
        total_exp = sum(exp_scores.values()) or 1
        normalized_scores = {label: (s / total_exp) * 100 for label, s in exp_scores.items()}
    else:
        normalized_scores = {label: 0.0 for label in labels}
        
    return log_scores, normalized_scores

def get_comment(label):
    if label == "tích cực":
        return "Phản hồi mang nội dung tích cực, khách hàng hài lòng."
    elif label == "tiêu cực":
        return "Phản hồi mang nội dung tiêu cực, cần xem xét cải thiện."
    return "Phản hồi mang tính trung lập, không có phàn nàn hay khen ngợi đặc biệt."

def get_label_badge_class(label):
    if label == "tích cực":
        return "badge-tich-cuc"
    elif label == "tiêu cực":
        return "badge-tieu-cuc"
    return "badge-trung-lap"

def get_label_conclusion_class(label):
    if label == "tích cực":
        return "conclusion-tich-cuc"
    elif label == "tiêu cực":
        return "conclusion-tieu-cuc"
    return "conclusion-trung-lap"

# ==========================================
# CẬP NHẬT TRẠNG THÁI SESSION STATE
# ==========================================
if "dataset" not in st.session_state:
    # Chuyển đổi dữ liệu ban đầu sang DataFrame
    df_init = pd.DataFrame(initial_data, columns=["Văn bản", "Nhãn"])
    st.session_state.dataset = df_init

if "test_text" not in st.session_state:
    st.session_state.test_text = "Shop nhiệt tình, chăm sóc khách hàng rất tốt"

# Trigger "Chạy test ngay"
if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0

# ==========================================
# BỐ CỤC GIAO DIỆN CHÍNH
# ==========================================

# 1. BANNER TIÊU ĐỀ
st.markdown(
    """
    <div class="banner-container">
        <div>
            <div style="margin-bottom: 12px;">
                <span class="custom-badge badge-primary">Python NLP Demo</span>
                <span class="custom-badge badge-outline">3 bước xử lý</span>
            </div>
            <h1 class="banner-title">Hệ thống phân loại phản hồi khách hàng</h1>
            <p class="banner-subtitle">
                Giao diện học tập cho phép giảng viên thay đổi dataset huấn luyện thời gian thực, 
                nhập câu kiểm thử tùy ý để quan sát chi tiết 3 giai đoạn xử lý: Tiền xử lý, Tính điểm, Dự đoán.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Nút trigger nhanh
col_btn, _ = st.columns([0.2, 0.8])
with col_btn:
    if st.button("🚀 Chạy test ngay"):
        # Lấy giá trị realtime từ session state, tránh ghi đè cứng mặc định
        st.session_state.test_text = st.session_state.get("test_text", "Shop nhiệt tình, chăm sóc khách hàng rất tốt")
        # Chuyển focus tab sang Dự đoán (Tab thứ 3)
        st.session_state.active_tab = 2
        st.rerun()

# 2. PHẦN DỮ LIỆU & NHẬP CÂU HỎI (Bố cục 2 Cột)
col_left, col_right = st.columns([1.2, 0.8])

# Khai báo các nhãn hợp lệ
LABELS = ["tích cực", "tiêu cực", "trung lập"]

with col_left:
    st.markdown(
        """
        <div class="custom-card">
            <h3 style="margin-top:0; font-size: 1.3rem; font-weight:700; display:flex; align-items:center; gap:8px;">
                🗂️ Dataset huấn luyện
            </h3>
            <p style="color:#64748b; font-size: 0.88rem; margin-top:-8px; margin-bottom:16px;">
                Thầy có thể thêm dòng mới (ở cuối bảng), sửa đổi câu phản hồi trực tiếp, hoặc thay đổi phân loại nhãn. 
                Hệ thống sẽ tự động cập nhật và huấn luyện lại thuật toán Naive Bayes.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Render st.data_editor
    edited_df = st.data_editor(
        st.session_state.dataset,
        num_rows="dynamic",
        use_container_width=True,
        height=450,
        column_config={
            "Văn bản": st.column_config.TextColumn(
                "Nội dung phản hồi",
                help="Nhập phản hồi của khách hàng tại đây",
                required=True,
                validate=r"^.+$"
            ),
            "Nhãn": st.column_config.SelectboxColumn(
                "Nhãn phân loại",
                help="Chọn nhãn cảm xúc",
                options=LABELS,
                required=True
            )
        }
    )
    
    # Nếu dữ liệu thay đổi, cập nhật session_state
    if not edited_df.equals(st.session_state.dataset):
        st.session_state.dataset = edited_df.reset_index(drop=True)
        st.rerun()

# Xử lý tính toán dựa trên tập dữ liệu hiện tại
dataset_list = []
for index, row in st.session_state.dataset.iterrows():
    text = row["Văn bản"]
    label = row["Nhãn"]
    if isinstance(text, str) and text.strip() and isinstance(label, str) and label.strip():
        prep = preprocess(text)
        dataset_list.append({
            "text": text,
            "label": label,
            "tokens": prep["tokens"]
        })

# Tính từ điển và tần suất từ
vocab = build_vocab(dataset_list)
word_prob = build_word_prob(dataset_list, LABELS, vocab)

with col_right:
    # Card 1: Câu test dự đoán
    st.markdown(
        """
        <div class="custom-card" style="margin-bottom: 20px;">
            <h3 style="margin-top:0; font-size: 1.3rem; font-weight:700;">
                ✍️ Câu test cần dự đoán
            </h3>
            <p style="color:#64748b; font-size: 0.88rem; margin-top:-8px; margin-bottom:12px;">
                Thay đổi nội dung bên dưới để kiểm tra khả năng dự đoán thời gian thực.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Sử dụng key="test_text" để tự động đồng bộ hóa hai chiều realtime với st.session_state.test_text
    st.text_area(
        label="Nội dung kiểm thử",
        key="test_text",
        height=100,
        label_visibility="collapsed"
    )
        
    # Gợi ý nhập nhanh
    st.markdown(
        """
        <div style="background-color: #f1f5f9; border-radius: 12px; padding: 12px; margin-top: -8px; margin-bottom: 24px; font-size: 0.85rem;">
            <strong style="color: #334155;">Gợi ý nhập thử:</strong><br/>
            💡 <i>"Giao hàng nhanh, sản phẩm đẹp xuất sắc!"</i> (Tích cực)<br/>
            💡 <i>"Vải mỏng, áo mặc nóng bí khó chịu vô cùng."</i> (Tiêu cực)<br/>
            💡 <i>"Sản phẩm dùng tạm được, chất lượng trung bình."</i> (Trung lập)
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Card 2: Thống kê tổng quan
    st.markdown(
        """
        <div class="custom-card">
            <h3 style="margin-top:0; font-size: 1.3rem; font-weight:700; margin-bottom: 12px;">
                📊 Tổng quan dữ liệu
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Hộp số liệu lớn
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.markdown(
            f"""
            <div style="background-color: #f1f5f9; border-radius: 16px; padding: 16px; text-align: center; margin-bottom: 12px;">
                <p style="color: #64748b; font-size: 0.85rem; margin: 0;">Tổng số mẫu</p>
                <p style="font-size: 1.8rem; font-weight: 800; color: #0f172a; margin: 4px 0 0 0;">{len(dataset_list)}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with sub_col2:
        st.markdown(
            f"""
            <div style="background-color: #f1f5f9; border-radius: 16px; padding: 16px; text-align: center; margin-bottom: 12px;">
                <p style="color: #64748b; font-size: 0.85rem; margin: 0;">Số từ đặc trưng</p>
                <p style="font-size: 1.8rem; font-weight: 800; color: #0f172a; margin: 4px 0 0 0;">{len(vocab)}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # Thống kê chi tiết từng class
    for label in LABELS:
        count = sum(1 for item in dataset_list if item["label"] == label)
        words = word_prob[label]["total_words"] if label in word_prob else 0
        badge_cls = get_label_badge_class(label)
        
        st.markdown(
            f"""
            <div style="display:flex; justify-content:space-between; align-items:center; border: 1px solid #e2e8f0; border-radius: 14px; padding: 10px 14px; background-color: #ffffff; margin-bottom: 8px;">
                <span class="custom-badge {badge_cls}">{label}</span>
                <span style="font-size: 0.85rem; color: #64748b;"><b>{count}</b> mẫu &bull; <b>{words}</b> từ</span>
            </div>
            """,
            unsafe_allow_html=True
        )

# Xử lý tính toán kết quả cho câu test
processed_test = preprocess(st.session_state.test_text)
log_scores, normalized_scores = score_text(processed_test["tokens"], word_prob, LABELS)
predicted_label = max(normalized_scores, key=normalized_scores.get) if normalized_scores else "trung lập"

# 3. QUY TRÌNH 3 BƯỚC (STREAMLIT TABS)
st.markdown("<br/>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="custom-card" style="padding-bottom: 12px;">
        <h3 style="margin-top:0; font-size: 1.3rem; font-weight:700;">
            🤖 Hiển thị kết quả trực quan theo 3 bước
        </h3>
        <p style="color:#64748b; font-size: 0.88rem; margin-top:-8px; margin-bottom:12px;">
            Hệ thống phân tách toàn bộ quá trình chạy thuật toán ra làm các phần hiển thị minh bạch.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Render tab
tab1, tab2, tab3 = st.tabs(["🧹 1. Tiền xử lý", "🧮 2. Tính điểm", "🎯 3. Dự đoán"])

# Đồng bộ chuyển tab nếu nút được ấn
# Streamlit tab hiện tại không hỗ trợ set active trực tiếp qua index một cách dễ dàng mà không có cấu trúc st.session_state phức tạp cho radio,
# nhưng ta đã tạo nút Rerun và sẽ hướng dẫn người dùng click trực quan hoặc sử dụng Session State để lưu tab nếu cần.
# Ở đây ta sử dụng tab của Streamlit mặc định rất tiện lợi.

with tab1:
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    t_col1, t_col2 = st.columns(2)
    
    with t_col1:
        st.markdown(
            f"""
            <div class="step-block" style="margin-bottom: 16px;">
                <div class="step-block-title">Câu gốc (Original Text)</div>
                <div class="step-block-content">{st.session_state.test_text or "<i>Chưa nhập nội dung</i>"}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div class="step-block">
                <div class="step-block-title">Xóa dấu câu và khoảng trắng thừa</div>
                <div class="step-block-content">{processed_test["clean_text"] or "<i>Chưa có dữ liệu</i>"}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with t_col2:
        st.markdown(
            f"""
            <div class="step-block" style="margin-bottom: 16px;">
                <div class="step-block-title">Chuẩn hóa chữ thường (Lowercase)</div>
                <div class="step-block-content">{processed_test["lower"] or "<i>Chưa có dữ liệu</i>"}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Danh sách token dạng badges
        badge_html = ""
        for token in processed_test["tokens"]:
            badge_html += f'<span class="custom-badge badge-primary" style="font-size:0.85rem; padding: 6px 12px; margin-top:4px;">{token}</span>'
        
        if not badge_html:
            badge_html = "<span style='color:#94a3b8; font-size: 0.9rem;'>Chưa có token được tách</span>"
            
        st.markdown(
            f"""
            <div class="step-block">
                <div class="step-block-title">Danh sách Tokens tách được (Tokenization)</div>
                <div style="background-color: #f8fafc; border-radius: 12px; padding: 12px; border: 1px dashed #cbd5e1; min-height: 50px;">
                    <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                        {badge_html}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

with tab2:
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    t2_col1, t2_col2 = st.columns([0.8, 1.2])
    
    with t2_col1:
        # Từ điển đặc trưng
        vocab_badge_html = ""
        for w in vocab:
            vocab_badge_html += f'<span class="custom-badge badge-outline" style="background-color:#ffffff; font-size:0.8rem;">{w}</span>'
            
        if not vocab_badge_html:
            vocab_badge_html = "<span style='color:#94a3b8;'>Từ điển rỗng</span>"
            
        st.markdown(
            f"""
            <div class="step-block">
                <div class="step-block-title">🔑 Từ điển đặc trưng (Vocab Size: {len(vocab)})</div>
                <div class="vocab-container">
                    <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                        {vocab_badge_html}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with t2_col2:
        # Điểm tin cậy và thanh ngang phần trăm
        st.markdown(
            """
            <div class="step-block">
                <div class="step-block-title">📈 Điểm tin cậy từng nhóm (Độ tin cậy %)</div>
                <div style="padding: 8px 0;">
            """,
            unsafe_allow_html=True
        )
        
        for label in LABELS:
            pct = normalized_scores.get(label, 0.0)
            log_sc = log_scores.get(label, 0.0)
            
            bar_cls = "bar-trung-lap"
            if label == "tích cực":
                bar_cls = "bar-tich-cuc"
            elif label == "tiêu cực":
                bar_cls = "bar-tieu-cuc"
                
            st.markdown(
                f"""
                <div class="progress-container">
                    <div class="progress-label">
                        <span>{label}</span>
                        <span>{pct:.2f}%</span>
                    </div>
                    <div class="progress-bar-outer">
                        <div class="progress-bar-inner {bar_cls}" style="width: {pct}%"></div>
                    </div>
                    <div class="log-score-label">Log-Probability Score: <b>{log_sc:.4f}</b></div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        st.markdown("</div></div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    t3_col1, t3_col2 = st.columns([0.8, 1.2])
    
    with t3_col1:
        # Thẻ kết luận khổng lồ
        conclusion_cls = get_label_conclusion_class(predicted_label)
        badge_cls = get_label_badge_class(predicted_label)
        comment_text = get_comment(predicted_label)
        
        st.markdown(
            f"""
            <div class="conclusion-card {conclusion_cls}">
                <div style="color: #64748b; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">
                    Nhãn được dự đoán
                </div>
                <div class="conclusion-badge {badge_cls}">
                    {predicted_label}
                </div>
                <div class="conclusion-comment">
                    "{comment_text}"
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with t3_col2:
        # Bảng chi tiết
        st.markdown(
            """
            <div class="step-block">
                <div class="step-block-title">📋 Bảng kết quả phân loại chi tiết</div>
                <table class="custom-table">
                    <thead>
                        <tr>
                            <th>Nhóm cảm xúc</th>
                            <th>Log-score (Âm)</th>
                            <th>Xác suất chuẩn hóa</th>
                            <th>Kết luận</th>
                        </tr>
                    </thead>
                    <tbody>
            """,
            unsafe_allow_html=True
        )
        
        for label in LABELS:
            pct = normalized_scores.get(label, 0.0)
            log_sc = log_scores.get(label, 0.0)
            conclusion = "<b>Được chọn (Cao nhất)</b>" if label == predicted_label else "Không chọn"
            
            st.markdown(
                f"""
                <tr>
                    <td style="text-transform: capitalize; font-weight: 500;">{label}</td>
                    <td style="font-family: monospace;">{log_sc:.4f}</td>
                    <td style="font-weight: 600;">{pct:.2f}%</td>
                    <td>{conclusion}</td>
                </tr>
                """,
                unsafe_allow_html=True
            )
            
        st.markdown(
            """
                    </tbody>
                </table>
                <div style="background-color: #f8fafc; border-radius: 12px; padding: 12px; margin-top: 16px; font-size: 0.8rem; color: #64748b; border: 1px solid #e2e8f0;">
                    📝 <b>Ghi chú học thuật:</b> Khác với điểm số Log-score luôn là giá trị âm lớn và khó hình dung trực quan, 
                    hệ thống đã áp dụng kỹ thuật chuẩn hóa Softmax để đưa các giá trị Log-score về dạng phân phối phần trăm (%) có tổng bằng 100%, 
                    giúp việc giảng dạy và theo dõi kết quả trở nên trực quan sinh động hơn.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
