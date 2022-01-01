# 직접 녹음한 음성으로 새 음성 만들기 용

from encoder import inference as encoder
from encoder import audio
from vocoder import inference as vocoder
from synthesizer.inference import Synthesizer

from a_data.tool import add_breaks
from a_data.tool import get_input_paths_texts

from pathlib import Path
from tqdm import tqdm
import numpy as np
import soundfile
import torch

encoder_model_fpath = Path("encoder/saved_models/fin_optim.pt")
synthesizer_model_fpath = Path("synthesizer/saved_models/fin/fin.pt")
vocoder_model_fpath = Path("vocoder/saved_models/fin/fin.pt")

input_wavs_alignment_path = "datasets_root/prototype/alignment.json"
output_wav_fpath = Path("datasets_root/prototype/outputs")

encoder.load_model(encoder_model_fpath, "cpu")
synthesizer = Synthesizer(synthesizer_model_fpath, verbose = False)
synthesizer.load()
vocoder.load_model(vocoder_model_fpath)

input_wav_paths, texts = get_input_paths_texts(input_wavs_alignment_path)
texts = sorted(texts.values(), key=lambda x : x[0])

embeds = []
filenames = []

# 30 wavs per 99 speakers
for input_wav_path in tqdm(input_wav_paths, "Audio", len(input_wav_paths)):
  wav = audio.preprocess_wav(input_wav_path)
  embeds.append(encoder.embed_utterance(wav))
  filenames.append(input_wav_path.name)

erroredName = []

for embed, filename in zip(embeds, filenames):
  speakerID = filename.split("_")[0].replace(".wav", "")
  for start in range(0, 50, 5):
    text = texts[start:start+5]
    key = f"{start+1:02}_{start+5:02}"
    
    fin_wav_name = speakerID + "_" + key + "_fin.wav"
    gl_wav_name = speakerID + "_" + key + "_gl.wav"

    fin_fpath = output_wav_fpath.joinpath(fin_wav_name)
    gl_fpath = output_wav_fpath.joinpath(gl_wav_name)
    
    if gl_fpath.exists():
        continue
    
    try:
        specs = synthesizer.synthesize_spectrograms(text, [embed] * len(text))
    except IndexError:
        erroredName.append(speakerID + "_" + key)
        continue
    breaks = [spec.shape[1] for spec in specs]
    spec = np.concatenate(specs, axis=1)
    assert spec is not None

    fin_wav = vocoder.infer_waveform(spec)
    griffin_lim_wav = Synthesizer.griffin_lim(spec)

    fin_wav = add_breaks(fin_wav, breaks, Synthesizer)
    griffin_lim_wav = add_breaks(griffin_lim_wav, breaks, Synthesizer)

    fin_wav = fin_wav / np.abs(fin_wav).max() * 0.97
    griffin_lim_wav = griffin_lim_wav / np.abs(griffin_lim_wav).max() * 0.97

    soundfile.write(fin_fpath, fin_wav, Synthesizer.sample_rate)
    soundfile.write(gl_fpath, griffin_lim_wav, Synthesizer.sample_rate)
    print(f"Finish save {gl_fpath}")

with Path("datasets_root/prototype/indexErrorList.txt").open("w", encoding="utf-8") as f:
    for n in erroredName:
        f.write(n + "\n")