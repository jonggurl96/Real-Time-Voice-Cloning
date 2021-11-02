from tqdm import tqdm
from pathlib import Path

datasets_root = Path("E:/AI-Hub_data/자유대화 음성(일반남녀)/Training")

speakers = sorted(datasets_root.glob("*"))
for speaker in tqdm(speakers, unit="speakers"):
  chapters = sorted(speaker.glob("*"))

  for chapter in chapters:
    wavs = sorted(chapter.glob("*.wav"))
    meta = chapter.joinpath(f"{speaker.name}-{chapter.name}.trans.txt")
    if len(wavs) < 30 or not meta.exists():
      for wav in wavs:
        wav.unlink()
      meta.unlink()
      chapter.rmdir()

  chapters = sorted(speaker.glob("*"))
  if len(chapters) == 0:
    speaker.rmdir()


  