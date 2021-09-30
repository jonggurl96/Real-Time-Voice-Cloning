
import os
import glob
from jamo import h2j, j2hcj
from tqdm import tqdm

print("seperate jamo start...")
filenames = []
txts = []
with open("Real-Time-Voice-Cloning\\kss\\transcript.txt", "rt", encoding="UTF-8") as f:
  lines = f.readlines()
  for line in tqdm(lines):
    txt = line.split(" ")
    filenames.append(txt[0])
    txt = "".join(txt[1:])
    txt = j2hcj(h2j(txt))
    txts.append(txt)

print("write transcript.jamo.txt start...")
with open("Real-Time-Voice-Cloning\\kss\\transcript.jamo.txt", "wt", encoding="UTF-8") as f:
  for filename, txt in tqdm(zip(filenames, txts)):
    f.write(filename + " " + txt)
