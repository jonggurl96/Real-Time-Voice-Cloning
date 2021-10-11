import os
import json
from tqdm import tqdm

"""
directory structure
Training
  [라벨]1.AI챗봇
  [라벨]2.음성수집도구
  [라벨]3.스튜디오
  [원천]1.AI챗봇_1
  [원천]1.AI챗봇_2
  [원천]2.음성수집도구_1
  [원천]3.스튜디오_1
    영역구분[일반남여, 노인남여, 소아남여, 외래어]_스크립트셋 번호_성별[M, F]_녹음자정보recorderId__나이_지역_녹음위치[실내, 실외, 녹음실]
      영역구분[일반남여, 노인남여, 소아남여, 외래어]_스크립트셋 번호_성별[M, F]_녹음자정보recorderId__나이_지역_녹음위치[실내, 실외, 녹음실]_스크립트번호

Validation
  [라벨]1.AI챗봇
  [라벨]2.음성수집도구
  [라벨]3.스튜디오
  [원천]1.AI챗봇
  [원천]2.음성수집도구
  [원천]3.스튜디오
    영역구분[일반남여, 노인남여, 소아남여, 외래어]_스크립트셋 번호_성별[M, F]_녹음자정보recorderId__나이_지역_녹음위치[실내, 실외, 녹음실]
      영역구분[일반남여, 노인남여, 소아남여, 외래어]_스크립트셋 번호_성별[M, F]_녹음자정보recorderId__나이_지역_녹음위치[실내, 실외, 녹음실]_스크립트번호

LibriSpeech와 같은 형태로 변경
  Training: sd
    recorderId: recorderId
      chapter: scriptsId("일반통합-20281") - "일반통합"
        scriptId: scriptId("일반통합-20281") - 20281
        recorderId-chapter.trans.txt
"""

drive = "E:\\"
main_dir = drive + "AI-Hub data\\자유대화 음성(일반남녀)"
sub_dir = ["Training", "Validation"]

for sd in sub_dir:
  sd_path = os.path.join(main_dir, sd)
  jsondirs = sorted(os.listdir(sd_path))
  jsondirs = [jd for jd in jsondirs if jd.startswith("[라벨]")]

  for jd in jsondirs:
    print(sd, "-", jd)
    print("=====================")
    
    # drive:\AI-Hub data\자유대화 음성(일반남녀)\Training\[라벨]1.AI챗봇
    jsondir = os.path.join(main_dir, sd, jd)

    # 일반남여_일반통합05_M_1455308554-6_37_수도권_실내, etc..
    recorderIds = sorted(os.listdir(jsondir))
    
    for recorderId in tqdm(recorderIds):
      # 1455308554-6
      recorder = recorderId.split("_")[3]

      # 녹음자가 녹음한 메타데이터 위치
      recorderIdDir = os.path.join(jsondir, recorderId)
      jsonfilenames = sorted(os.listdir(recorderIdDir))

      # 각 메타데이터 열기
      for filename in jsonfilenames:
        filename = os.path.join(recorderIdDir, filename)
        with open(filename, "rt", encoding="UTF-8") as jf:
          jf = json.load(jf)
          
          # 음성 텍스트
          stt = jf["발화정보"]["stt"]
          scriptId = jf["발화정보"]["scriptId"]

          # "일반통합-20281" => "일반통합", 20281
          if "-" in scriptId:
            chapter, scriptId = scriptId.split("-")
          
          # 자유대화의 경우 "scriptId": "P"
          elif scriptId == "P":
            chapter = "자유대화"
            scriptId = jf["발화정보"]["fileNm"].split("_")[-1].split(".")[0]
          
          # 일반통합 scriptId: "00002"
          else:
            chapter = "일반통합"
        
        # sd_path/recorder/chapter/recorder-chapter.trans.txt
        filepath = os.path.join(sd_path, recorder, chapter)
        filename = recorder + "-" + chapter + ".trans.txt"
        os.makedirs(filepath, exist_ok=True)

        fn = os.path.join(filepath, filename)
        with open(fn, "a", encoding="UTF-8") as f:
          wavname = recorder + "-" + chapter + "-" + scriptId
          txt = wavname + " " + stt + "\n"
          f.write(txt)
        



