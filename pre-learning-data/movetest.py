from tqdm import tqdm
from pathlib import Path

datasets_root = Path("C:/Users/LeeJongGeol/Desktop/Training")

speakers = [m for m in datasets_root.glob("*") if m.is_dir()]

for speaker in tqdm(speakers, unit="speakers"):

  chapter = speaker.joinpath("일반통합")
  cname = "일반통합"
  if not chapter.exists():
    chapter = speaker.joinpath("자유대화")
    cname = "자유대화"
  
  sname = speaker.name
  wavs = [m for m in chapter.glob("*.wav")]
  metadata_fpath = chapter.joinpath(f"{sname}-{cname}.trans.txt")

  with metadata_fpath.open("r", encoding="utf-8") as f:
    for text in f:
      fn = text.split(" ")[0]
      filename = chapter.joinpath(fn + ".wav")
      assert filename in wavs

print("정상적으로 종료됨")
