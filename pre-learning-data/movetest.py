from tqdm import tqdm
from pathlib import Path

datasets_root = Path("../datasets_root/자유대화 음성(일반남녀)/Training")

speakers = [m for m in datasets_root.glob("*") if m.is_dir()]
print(f"Find {len(speakers)} speakers")

for speaker in tqdm(speakers, unit="speakers"):

  chapter = speaker.joinpath("일반통합")
  cname = "일반통합"
  if not chapter.exists():
    chapter = speaker.joinpath("자유대화")
    cname = "자유대화"
  
  sname = speaker.name
  wavs = sorted([m for m in chapter.glob("*.wav")])
  metadata_fpath = chapter.joinpath(f"{sname}-{cname}.trans.txt")

  with metadata_fpath.open("r", encoding="utf-8") as f:
    texts = f.readlines()
    for i, text in enumerate(texts):
        wname = wavs[i].name.replace(".wav", "")
        assert text.startswith(wname)
    

print("정상적으로 종료됨")
