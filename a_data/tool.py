import json
import numpy as np
from pathlib import Path

def get_input_paths_texts(path):

  with open(path, "r", encoding="utf-8") as json_file:
    jf = json.load(json_file)
    input_text = jf["input_text"]
    output_text = jf["output_text"]

  speakers_path = Path("datasets_root/prototype/inputs")
  speaker_path = sorted([m for m in speakers_path.glob("*") if m.is_dir()])

  wavpaths = []
  for speaker in speaker_path:
    wavs = [m for m in speaker.glob("*.wav")]
    wavpaths.extend(wavs)
  return wavpaths, output_text

def add_breaks(wav, breaks, Synthesizer):
  b_ends = np.cumsum(np.array(breaks) * Synthesizer.hparams.hop_size)
  b_starts = np.concatenate(([0], b_ends[:-1]))
  wavs = [wav[start:end] for start, end, in zip(b_starts, b_ends)]
  breaks = [np.zeros(int(0.15 * Synthesizer.sample_rate))] * len(breaks)
  wav = np.concatenate([i for w, b in zip(wavs, breaks) for i in (w, b)])
  return wav
