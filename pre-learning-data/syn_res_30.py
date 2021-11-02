from pathlib import Path
from tqdm import tqdm

audio_p = Path("F:/옮길거/audio")
metafilepath = Path("F:/옮길거/train.txt")

# *.npy
audios = sorted([m.name for m in audio_p.glob("*.npy")])

# train.txt의 내용을 읽어 audio 폴더에 존재하는 파일과 연결 되는지 확인
# 실재하는 파일이라면 새로 저장하기 위해 texts list에 추가
texts = []
with metafilepath.open("r", encoding="utf-8") as f:
  lines = f.readlines()
  for line in tqdm(lines):
    # audio-speaker-chapter-*.npy
    audio = line.split("|")[0]
    audio = audio_p.joinpath(audio)

    if audio.exists():
      texts.append(line)

print(len(texts))

# texts를 train.txt에 저장, "w", encoding="utf-8"
with metafilepath.open("w", encoding="utf-8") as f:
  for text in tqdm(texts):
    f.write(text)