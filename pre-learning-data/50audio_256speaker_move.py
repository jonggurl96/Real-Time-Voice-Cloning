import sys
import random
import shutil
from pathlib import Path

datasets_root = Path("E:/AI-Hub_data/data/Training")
out_dir = Path("C:/Users/LeeJongGeol/Desktop/Training")

speakers = [m for m in datasets_root.glob("*") if m.is_dir()]
random.shuffle(speakers)
# speaker list에서 256개 중복을 허용하지 않고 추출
more50cnt = 0 # 50
wcnt = 0 # 256 * 50 = 12800
for speaker in speakers:

  # 01: 일반통합, 02: 자유대화
  # 자유대화의 비율이 더 적어서 둘 다 있는 화자의 경우 자유대화 선택
  chapters = sorted([m for m in speaker.glob("*") if m.is_dir()])
  chapter = chapters[-1]
  wavs = sorted(chapter.glob("*.wav"))
  if len(wavs) < 50:
    continue
  
  speaker_chapter = out_dir.joinpath(speaker.name, chapter.name)
  speaker_chapter.mkdir(parents=True, exist_ok=True)
  
  wavs = wavs[:50]
  for wav in wavs:
    fname = wav.name
    copy_path = speaker_chapter.joinpath(fname)
    shutil.copy(wav, copy_path)
    wcnt += 1
  
  # trans.txt 추가
  meta = chapter.joinpath(f"{speaker.name}-{chapter.name}.trans.txt")
  texts = {}
  with meta.open("r", encoding="utf-8") as f:
    for text in f.readlines():
      text = text.rstrip()
      fn = text.split(" ")[0]
      texts[fn] = text.replace(fn + " ", "")
  
  new_metafpath = speaker_chapter.joinpath(meta.name)
  with new_metafpath.open("w", encoding="utf-8") as f:
    for wav in wavs:
      wav = wav.name
      wav = wav.replace(".wav", "")
      metadata = wav + " " + texts[wav] + "\n"
      f.write(metadata)

  more50cnt += 1
  sys.stdout.write('\r%d/256 speakers' % more50cnt)
  if more50cnt == 256:
    break
  
print(f"50 audios per {more50cnt} speakers")
print(f"total {wcnt} audios")
