"""
KSS - Korean Single Speech dataset
KSS dataset txt file structure

kss/train/subset/[1, 2, 3, 4]/*.wav

BEFORE)

1/1_0000.wav|그는 괜찮은 척하려고 애쓰는 것 같았다.|그는 괜찮은 척하려고 애쓰는 것 같았다.|그는 괜찮은 척하려고 애쓰는 것 같았다.|3.5|He seemed to be pretending to be okay.
subset/subset_*.wav|korean|eng, num, ... -> korean|jamo seperate|time(s)|eng

AFTER)

19-198-0000 NORTHANGER ABBEY
subset-1-0000 그는 괜찮은 척하려고 애쓰는 것 같았다.
subset-[1, 2, 3, 4]-* jamo seperate

"""

import os
import glob

with open("Real-Time-Voice-Cloning\\kss\\transcript.v.1.4.txt", "rt", encoding="UTF-8") as f:
  lines = f.readlines()
  subsets = []
  for line in lines:
    kwrds = list(line.split("|"))
    fn = kwrds[0].split("/")[-1]
    fn = "subset-" + fn
    fn = fn.replace("_", "-")
    fn = fn.split(".")[0]
    txt = kwrds[-3]
    kwrds = " ".join([fn, txt])
    subsets.append(kwrds)

with open("Real-Time-Voice-Cloning\\kss\\transcript.txt", "wt", encoding="UTF-8") as f:
  for line in subsets:
    line = line + "\n"
    f.write(line)
