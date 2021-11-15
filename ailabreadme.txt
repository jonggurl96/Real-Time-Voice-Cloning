python encoder_preprocess.py datasets_root
python encoder_train.py aisrc datasets_root/SV2TTS/encoder

python synthesizer_preprocess_audio.py datasets_root
    SV2TTS/synthesizer/audios, mels 생성
python synthesizer_preprocess_embeds.py datasets_root/SV2TTS/synthesizer --encoder_model_fpath=encoder/saved_models/aisrc.pt
    SV2TTS/synthesizer/embeds 생성
python synthesizer_train.py aisrc datasets_root/SV2TTS/synthesizer

python vocoder_preprocess.py datasets_root --model_dir=synthesizer/saved_models/aisrc
python vocoder_train.py aisrc datasets_root



encoder/inference line 151
    embed = raw_embed / np.linalg.norm(raw_embed, 2)
    l2 norm이 0일 때가 자꾸 생겨서 norm이 0일 때 norm을 0.1로 고정
    RuntimeWarning: invalid value encountered in true_divide 0으로 나눈거 
    encoder/inference.py : embed_utterance(wav)
    partial_embeds [3, 256] 모두 0인 경우 존재
    frames_batch 0은 아님 [1|2|3, 160, 40]에서 partial_embeds가 0이 되는 부분이 있음
    일단 norm을 0.1로 고정하고 진행
    synthesizer_train.py 실행중
