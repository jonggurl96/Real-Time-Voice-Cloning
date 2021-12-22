python encoder_preprocess.py datasets_root
python encoder_train.py fin datasets_root/SV2TTS/encoder

python synthesizer_preprocess_audio.py datasets_root
    SV2TTS/synthesizer/audios, mels 생성
python synthesizer_preprocess_embeds.py datasets_root/SV2TTS/synthesizer --encoder_model_fpath=encoder/saved_models/fin_optim.pt
    SV2TTS/synthesizer/embeds 생성
python synthesizer_train.py fin datasets_root/SV2TTS/synthesizer

python vocoder_preprocess.py datasets_root --model_dir=synthesizer/saved_models/fin
python vocoder_train.py fin datasets_root



encoder/inference line 151
    embed = raw_embed / np.linalg.norm(raw_embed, 2)
    l2 norm이 0일 때가 자꾸 생겨서 norm이 0일 때 norm을 0.1로 고정
    RuntimeWarning: invalid value encountered in true_divide 0으로 나눈거 
    encoder/inference.py : embed_utterance(wav)
    partial_embeds [3, 256] 모두 0인 경우 존재
    frames_batch 0은 아님 [1|2|3, 160, 40]에서 partial_embeds가 0이 되는 부분이 있음
    일단 norm을 0.1로 고정하고 진행
    synthesizer_train.py 실행중

github token: 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

run_id aisrc: norm == 0일 때 norm = 0.1
run_id ai: norm == 0일 때 raw_embed return

encoder training loss가 높으면 encoder/model.py 59 line norm값이 0인지 확인하고 위와 같이 바꿔서 다시 학습

run1, aisrc, ai, fin...
실행 중이라 github에 push가 안되는건가?

encoder_model_fpath = Path("Real-Time-Voice-Cloning/encoder/saved_models/fin_optim.pt")
synthesizer_model_fpath = Path("Real-Time-Voice-Cloning/synthesizer/saved_models/fin/fin.pt")
vocoder_model_fpath = Path("Real-Time-Voice-Cloning/vocoder/saved_models/fin/fin.pt")

input_wavs_alignment_path = "C:\\Users\\LeeJongGeol\\Desktop\\prototype\\alignment.json"
output_wav_fpath = Path("C:\\Users\\LeeJongGeol\\Desktop\\prototype\\outputs")