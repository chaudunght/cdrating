import sys
import math
from data import training_data, new_text

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("="*50)
print("THỐNG KÊ DỮ LIỆU ĐẦU VÀO")
print("="*50)

print(f"Tổng số văn bản trong training_data: {len(training_data)}")
print("-" * 50)

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
        for k in range(min(3, n - i), 1, -1):
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
    text = normalize_lower(text)
    text = remove_punctuation(text)
    text = remove_extra_spaces(text)
    return tokenize(text)

processed_data = []
for text, label in training_data:
    tokens = preprocess(text)
    processed_data.append((tokens, label))


def build_vocab(processed_data):
    vocab = set()
    for tokens, label in processed_data:
        for word in tokens:
            vocab.add(word)
    vocab_list = list(vocab)
    print(f"Số lượng từ đặc trưng (vocab size): {len(vocab_list)}")
    return vocab_list

def build_word_prob(processed_data, labels, vocab):
    word_prob = {}
    vocab_size = len(vocab)
    
    for label in labels:
        words_in_label = []
        for tokens, l in processed_data:
            if l == label:
                words_in_label.extend(tokens)
        
        word_counts = {}
        for word in words_in_label:
            word_counts[word] = word_counts.get(word, 0) + 1
            
        total_words = len(words_in_label)
        
        probs = {}
        for word in vocab:
            count = word_counts.get(word, 0)
            probs[word] = (count + 1) / (total_words + vocab_size)
        
        word_prob[label] = probs
    return word_prob

def score_text(tokens, word_prob, labels):
    scores = {}
    for label in labels:
        score = 0
        for word in tokens:
            if word in word_prob[label]:
                score += math.log(word_prob[label][word])
        scores[label] = score
    return scores

labels = ["tích cực", "tiêu cực", "trung lập"]
vocab = build_vocab(processed_data)
word_prob = build_word_prob(processed_data, labels, vocab)


def predict(text, word_prob, labels):
    tokens = preprocess(text)
    log_scores = score_text(tokens, word_prob, labels)
    
    max_log = max(log_scores.values())
    
    exp_scores = {label: math.exp(score - max_log) for label, score in log_scores.items()}
    total_exp = sum(exp_scores.values())
    
    normalized_scores = {label: (s / total_exp) * 100 for label, s in exp_scores.items()}
    
    predicted_label = max(normalized_scores, key=normalized_scores.get)
    return predicted_label, normalized_scores

def display_result(text, predicted_label, scores):
    print("\n" + "="*60)
    print("       HỆ THỐNG PHÂN LOẠI PHẢN HỒI KHÁCH HÀNG")
    print("="*60)
    print(f"Văn bản đầu vào : \"{text}\"")
    print(f"Sau tiền xử lý  : {preprocess(text)}")
    
    print("\n--- ĐIỂM SỐ TIN CẬY (Thang điểm 100) ---")
    for label, score in scores.items():
        print(f"  {label.capitalize():<10}: {score:6.2f}")
    
    print("\n--- KẾT QUẢ DỰ ĐOÁN ---")
    print(f"  Nhãn được dự đoán : {predicted_label.upper()}")
    
    if predicted_label == "tích cực":
        comment = "Phản hồi mang nội dung tích cực, khách hàng hài lòng."
    elif predicted_label == "tiêu cực":
        comment = "Phản hồi mang nội dung tiêu cực, cần xem xét cải thiện."
    else:
        comment = "Phản hồi mang tính trung lập, không có phàn nàn hay khen ngợi đặc biệt."
    
    print(f"  Nhận xét          : {comment}")
    print("="*60)

predicted_label, scores = predict(new_text, word_prob, labels)
display_result(new_text, predicted_label, scores)
