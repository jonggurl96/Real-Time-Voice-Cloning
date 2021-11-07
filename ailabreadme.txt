python encoder_preprocess.py datasets_root
python encoder_train.py aisrc datasets_root\SV2TTS\encoder

python synthesizer_preprocess_audio.py datasets_root
python synthesizer_preprocess_embeds.py datasets_root\SV2TTS\synthesizer --encoder_model_fpath=encoder/saved_models/aisrc.pt
python synthesizer_train.py aisrc datasets_root\SV2TTS\synthesizer

python vocoder_preprocess.py datasets_root --model_dir=synthesizer/saved_models/aisrc
python vocoder_train.py aisrc datasets_root