from pathlib import Path
from tqdm import tqdm
"""
3번째 실행
wav파일 10개 이하 폴더 삭제
"""

training_dir = Path("E:\AI-Hub_data\data\Training")
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
    speaker_dir.rmdir()