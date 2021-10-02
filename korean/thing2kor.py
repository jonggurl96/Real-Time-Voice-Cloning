import re # regular expression

starts = ["(NO:", "(FP:", "(SP:", "(SN:", "0NO:", "0FP:", "0SP:", "0SN:", "("]

# V: 브이/비에서 브이만 추출
# Z: 제트/지에서 지만 추출
dict_eng2kor = {
  "A": "에이", "B": "비", "C": "씨", "D": "디", "E": "이", "F": "에프", "G": "지",
  "H": "에이치", "I": "아이", "J": "제이", "K": "케이", "L": "엘", "M": "엠",
  "N": "엔", "O": "오", "P": "피", "Q": "큐", "R": "알", "S": "에스", "T": "티",
  "U": "유", "V": "브이", "W": "더블유", "X": "엑스", "Y": "와이", "Z": "지"
}

# 년, 월, 일, 분, 초
dict_num2kor_general = {
  "1": "일", "2": "이", "3": "삼", "4": "사", "5": "오",
  "6": "육", "7": "칠", "8": "팔", "9": "구", "0": "영"
}
# 시, 개, 
dict_num2kor_count = {
  "1": "한", "2": "두", "3": "세", "4": "네", "5": "다섯",
  "6": "여섯", "7": "일곱", "8": "여덟", "9": "아홉", "10": "열"
}
num_unit_kor = "천백십해천백십경천백십조천백십억천백십만천백십"

# erase guideline code
def bracket_parse(text:string):
  for start in starts:
    text = text.replace(start, "")
    text = text.replace(")", "")
    text = text.replace("0", "")
  return text


# eng2kor
def eng2kor(text):
  lowers = re.findall('[a-z]', text)
  for lower in lowers:
    text = text.replace(lower, lower.upper())
  for eng in dict_eng2kor:
    text = text.replace(eng, dict_eng2kor[eng])
  return text




# num2kor
def num2kor(num):
  # 숫자를 모두 한글로 표현
  # 전화번호 형태 000-0000-0000 또는 000-0000의 형태는 숫자 하나하나 띄어쓰기
  # 날짜와 시간
    # 0000/00/00 00시 00분 00초, (00)00년, 0월 0일
  # 개수
    # 0개 -> 영개, 123개 -> 1백 2십 3개 -> (일)백 이십 삼개
  # 기념일 형태 0.00 형태도 숫자 하나하나 띄어쓰기
  num = "1268046"
  numlen = len(num) # 7
  # 일백 이십 육만 팔천 사십 육
  num_unit = num_unit_kor[-numlen+1:] # 백십만천백십
  res = ""
  for i, u in enumerate(num_unit):
    if num[i] != "0":
      res = res + num[i] + u + " " # 1백 2십 6만 8천 4십
  if num[-1] != "0":
    res += num[-1] # 1백 2십 6만 8천 4십 6
  for n in dict_num2kor_general:
    res = res.replace(n, dict_num2kor_general[n]) # 일백 이십 육만 팔천 사십 육
  
  return res




