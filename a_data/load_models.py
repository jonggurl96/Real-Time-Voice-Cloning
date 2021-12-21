# Not Using...ㅠㅠ

import torch
from torch import optim
from encoder.model import SpeakerEncoder
from synthesizer.models.tacotron import Tacotron
from vocoder.models.fatchord_version import WaveRNN

from korean.korean2jamo import symbols
from synthesizer.hparams import hparams
import vocoder.hparams as hp

def load_models(encoder_model_fpath, synthesizer_model_fpath, vocoder_model_fpath):
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  loss_device = torch.device("cpu")

  encoder_model = SpeakerEncoder(device, loss_device)
  encoder_weights = torch.load(encoder_model_fpath, map_location=device)
  encoder_model.load_state_dict(encoder_weights["model_state"])

  synthesizer_model = Tacotron(embed_dims = hparams.tts_embed_dims,
    num_chars = len(symbols),
    encoder_dims = hparams.tts_encoder_dims,
    decoder_dims = hparams.tts_decoder_dims, 
    n_mels = hparams.num_mels,
    fft_bins = hparams.num_mels,
    postnet_dims = hparams.tts_postnet_dims,
    encoder_K = hparams.tts_encoder_K, 
    lstm_dims = hparams.tts_lstm_dims, 
    postnet_K = hparams.tts_postnet_K,
    num_highways = hparams.tts_num_highways,
    dropout = hparams.tts_dropout,
    stop_threshold = hparams.tts_stop_threshold,
    speaker_embedding_size = hparams.speaker_embedding_size).to(device)
  synthesizer_optimizer = optim.Adam(synthesizer_model.parameters())
  synthesizer_model.load(synthesizer_model_fpath, synthesizer_optimizer)

  vocoder_model = WaveRNN(
    rnn_dims=hp.voc_rnn_dims,
    fc_dims=hp.voc_fc_dims,
    bits=hp.bits,
    pad=hp.voc_pad,
    upsample_factors=hp.voc_upsample_factors,
    feat_dims=hp.num_mels,
    compute_dims=hp.voc_compute_dims,
    res_out_dims=hp.voc_res_out_dims,
    res_blocks=hp.voc_res_blocks,
    hop_length=hp.hop_length,
    sample_rate=hp.sample_rate,
    mode=hp.voc_mode)
  vocoder_optimizer = optim.Adam(vocoder_model.parameters())
  vocoder_model.load(vocoder_model_fpath, vocoder_optimizer, device)

  print(device)
  print(loss_device)

  return encoder_model, synthesizer_model, vocoder_model