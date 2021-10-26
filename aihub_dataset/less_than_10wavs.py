<<<<<<< HEAD
from pathlib import Path
from tqdm import tqdm

training_dir = Path("E:\AI-Hub_data\자유대화 음성(일반남녀)\Training")
speaker_dirs = [path for path in training_dir.glob("*") if path.is_dir()]
for speaker_dir in tqdm(speaker_dirs):
  wavs = list(speaker_dir.glob("**/*.wav"))
  if len(wavs) < 10:
    files = list(speaker_dir.glob("**/*.*"))
    for f in files:
      f.unlink()
    chapters = [chapter for chapter in speaker_dir.glob("*") if chapter.is_dir()]
    for chapter in chapters:
      chapter.rmdir()
=======
from pathlib import Path
from tqdm import tqdm

training_dir = Path("E:\AI-Hub_data\자유대화 음성(일반남녀)\Training")
speaker_dirs = [path for path in training_dir.glob("*") if path.is_dir()]
for speaker_dir in tqdm(speaker_dirs):
  wavs = list(speaker_dir.glob("**/*.wav"))
  if len(wavs) < 10:
    files = list(speaker_dir.glob("**/*.*"))
    for f in files:
      f.unlink()
    chapters = [chapter for chapter in speaker_dir.glob("*") if chapter.is_dir()]
    for chapter in chapters:
      chapter.rmdir()
>>>>>>> d3beaaef442272542859e96fac99cfef9eb68735
    speaker_dir.rmdir()