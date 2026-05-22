import sys
import json
import os
from data import training_data

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def clean_text(text):
    text = text.lower()
    punctuations = "!?. ,;:\"'()[]{}/\\-_"
    clean = ""
    for char in text:
        if char not in punctuations:
            clean += char
        else:
            clean += " "
    return " ".join(clean.strip().split())

def main():
    # 1. Nạp danh sách từ ghép từ Viet11K.txt (các từ có chứa dấu cách)
    viet_compounds = set()
    file_path = "Viet11K.txt"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip().lower()
                if " " in word:  # Chứa khoảng trắng -> Từ ghép/cụm từ
                    viet_compounds.add(word)
    else:
        print(f"Lỗi: Không tìm thấy file từ điển '{file_path}'!")
        return

    # 2. Quét toàn bộ dữ liệu training_data từ data.py
    extracted_compounds = set()
    for text, label in training_data:
        cleaned_sentence = f" {clean_text(text)} "
        for compound in viet_compounds:
            # Khớp từ ghép với biên từ rõ ràng (word boundary)
            if f" {compound} " in cleaned_sentence:
                extracted_compounds.add(compound)

    # 3. Sắp xếp danh sách từ ghép tìm thấy
    sorted_compounds = sorted(list(extracted_compounds))

    # 4. Ghi kết quả vào dictionary.json
    output_path = "dictionary.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sorted_compounds, f, ensure_ascii=False, indent=4)

    print(f"Thành công! Đã trích xuất {len(sorted_compounds)} từ ghép duy nhất vào '{output_path}'.")

if __name__ == "__main__":
    main()
