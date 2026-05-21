import json

def get_base_char(char):
    char = char.lower()
    mapping = {
        'a': 'aàáảãạ',
        'ă': 'ăằắẳẵặ',
        'â': 'âầấẩẫậ',
        'e': 'eèéẻẽẹ',
        'ê': 'êềếểễệ',
        'i': 'iìíỉĩị',
        'o': 'oòóỏõọ',
        'ô': 'ôồốổỗộ',
        'ơ': 'ơờớởỡợ',
        'u': 'uùúủũụ',
        'ư': 'ưừứửữự',
        'y': 'yỳýỷỹỵ'
    }
    for base, variants in mapping.items():
        if char in variants:
            return base
    return char

def main():
    try:
        with open('Viet11K.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open('Viet11K.txt', 'r', encoding='utf-16') as f:
            lines = f.readlines()

    index_list = []
    current_char = None
    last_line_seen = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
            
        first_char = stripped[0]
        base_char = get_base_char(first_char)
        
        if current_char is None:
            current_char = base_char
        
        if base_char != current_char:
            index_list.append({
                'char': current_char,
                'index': last_line_seen
            })
            current_char = base_char
        
        last_line_seen = i + 1 # 1-indexed line number
            
    # Add the last character
    if current_char:
        index_list.append({
            'char': current_char,
            'index': last_line_seen
        })
        
    with open('index.py', 'w', encoding='utf-8') as f:
        f.write('index = [\n')
        for entry in index_list:
            f.write(f"    {{'char': '{entry['char']}', 'index': {entry['index']}}},\n")
        f.write(']\n')

if __name__ == "__main__":
    main()
