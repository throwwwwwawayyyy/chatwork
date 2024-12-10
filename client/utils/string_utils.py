import random

def contains_hebrew(txt: str) -> list[tuple[int, int]]:
    hebrew_alphabet = [chr(code) for code in range(0x05D0, 0x05EA + 1)]
    hebrew_alphabet.extend(['ך', 'ם', 'ן', 'ף', 'ץ'])
    
    txt += " "
    
    idx_size = []
    
    i = 0
    idx = 0
    size = 0
    
    flag = False
    
    while(i < len(txt)):
        if txt[i] in hebrew_alphabet:
            if not flag:
                idx = i
                size = 1
                flag = True
            else:
                size += 1
        else:
            if flag:
                if txt[i] == " " and i + 1 < len(txt) and txt[i + 1] in hebrew_alphabet:
                    size += 1
                else:
                    idx_size.append((idx, size))
                    flag = False
        i += 1
        
    return idx_size

def reverse_substring(s, index, size):
    before = s[:index]
    to_reverse = s[index:index + size]
    after = s[index + size:]
    
    return before + to_reverse[::-1] + after

def handle_display_string(txt: str) -> str:
    idx_size_list = contains_hebrew(txt)
    
    for (idx, size) in idx_size_list:
        txt = reverse_substring(txt, idx, size)
    
    return txt

def generate_random_unk_username() -> str:
    id = random.randint(0, 100000)
    return "unk" + str(id)