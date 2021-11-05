import shutil
import random
from tqdm import tqdm
from pathlib import Path

datasets_root = Path("E:/AI-Hub_data/자유대화 음성(일반남녀)/Training")
out_dir = Path("F:/옮길거/Training")

speakers785 = [m for m in datasets_root.glob("*") if m.is_dir()]
# speaker list에서 100개 중복을 허용하지 않고 추출
speakers = random.sample(speakers785, 256)
for speaker in tqdm(speakers, unit="speakers"):
  chapters = sorted([m for m in speaker.glob("*") if m.is_dir()])
  chapter = chapters[-1]
  wavs = sorted(chapter.glob("*.wav"))
  speaker_chapter = out_dir.joinpath(speaker.name, chapter.name)
  speaker_chapter.mkdir(parents=True, exist_ok=True)
  
  for wav in wavs[:30]:
    fname = wav.name
    copy_path = speaker_chapter.joinpath(fname)
    shutil.copy(wav, copy_path)
  
  # trans.txt 추가
  meta = chapter.joinpath(f"{speaker.name}-{chapter.name}.trans.txt")
  texts = []
  with meta.open("r", encoding="utf-8") as f:
    for _ in range(30):
      texts.append(f.readline())
  new_metafpath = speaker_chapter.joinpath(meta.name)
  with new_metafpath.open("w", encoding="utf-8") as f:
    for text in texts:
      f.write(text)
