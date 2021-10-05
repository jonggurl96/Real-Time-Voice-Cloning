# Korean Text Parsing

* `모델 훈련 후 실 사용 시 주의사항`

## Metadata Guideline
```
외부 잡음 Filter Noise: (NO:)
간투어 Filter Pause: (FP:) - 어, 음, 글쎄, 저 등
명확히 들리지 않는 경우: (SP:)
화자 잡음 스피커 Noise: (SN:)
```

`오타`
```
  - 0NO:)
  - 0NO:0
  - (NO:0
  - ...
```

`숫자 표현`
  - 모두 한글로 표현, 십진 단위로 띄어쓰기
  - 숫자를 하나씩 발음한 경우 띄어쓰기
  - 단위를 나타내는 '년', '월', '일', '시', '분' 등은 붙여쓰기
    - 이십 사시간, 스물 네시간, 오대 그룹, 자동차 다섯대, 팔 육 공에 이 사 삼 칠(860-2437)
    - 십 사시, 열 네시, 천 구백 구십 구년에
  - 숫자만으로 이루어진 기념일 등 특정 의미가 있는 단어들은 숫자 단위로 띄어쓰기
    - 팔 일 오(8.15), 사 일 구(4.19), 오 칠 오 공 부대(5750부대)

약어/외래어 표현
  - 약어 형태의 알파벳인 경우 붙여쓰기
  - KBS(케이비에스), AT&T(에이티앤티)

알파벳
|Eng|Kor|Eng|Kor|Eng|Kor|Eng|Kor|
|---|---|---|---|---|---|---|---|
|A|에이|B|비|C|씨|D|디|
|E|이|F|에프|G|지|H|에이치|
|I|아이|J|제이|K|케이|L|엘|
|M|엠|N|엔|O|오|P|피|
|Q|큐|R|알|S|에스|T|티|
|U|유|V|브이/비|W|더블유|X|엑스|
|Y|와이|Z|지/제트

비표준 발음으로 들리는 경우 표준어로 표현
축약 발성은 표준어로 표현

인코딩 예시는 Training/0.0baesubin/00002