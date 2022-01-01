import re

def parse_kor(text):
    return re.sub(r'[^가-힣 .,?!]', "", text)