# Real-Time Voice Cloning
This repository is an implementation of [Transfer Learning from Speaker Verification to
Multispeaker Text-To-Speech Synthesis](https://arxiv.org/pdf/1806.04558.pdf) (SV2TTS) with a vocoder that works in real-time. Feel free to check [my thesis](https://matheo.uliege.be/handle/2268.2/6801) if you're curious or if you're looking for info I haven't documented. Mostly I would recommend giving a quick look to the figures beyond the introduction.

SV2TTS is a three-stage deep learning framework that allows to create a numerical representation of a voice from a few seconds of audio, and to use it to condition a text-to-speech model trained to generalize to new voices.

**Video demonstration** (click the picture):

[![Toolbox demo](https://i.imgur.com/8lFUlgz.png)](https://www.youtube.com/watch?v=-O_hYhToKoA)



### Papers implemented  
| URL | Designation | Title | Implementation source |
| --- | ----------- | ----- | --------------------- |
|[**1806.04558**](https://arxiv.org/pdf/1806.04558.pdf) | **SV2TTS** | **Transfer Learning from Speaker Verification to Multispeaker Text-To-Speech Synthesis** | This repo |
|[1802.08435](https://arxiv.org/pdf/1802.08435.pdf) | WaveRNN (vocoder) | Efficient Neural Audio Synthesis | [fatchord/WaveRNN](https://github.com/fatchord/WaveRNN) |
|[1703.10135](https://arxiv.org/pdf/1703.10135.pdf) | Tacotron (synthesizer) | Tacotron: Towards End-to-End Speech Synthesis | [fatchord/WaveRNN](https://github.com/fatchord/WaveRNN)
|[1710.10467](https://arxiv.org/pdf/1710.10467.pdf) | GE2E (encoder)| Generalized End-To-End Loss for Speaker Verification | This repo |

## News
**14/02/21**: This repo now runs on PyTorch instead of Tensorflow, thanks to the help of @bluefish. If you wish to run the tensorflow version instead, checkout commit `5425557`.

**13/11/19**: I'm now working full time and I will not maintain this repo anymore. To anyone who reads this:
- **If you just want to clone your voice (and not someone else's):** I recommend our free plan on [Resemble.AI](https://www.resemble.ai/). You will get a better voice quality and less prosody errors.
- **If this is not your case:** proceed with this repository, but you might end up being disappointed by the results. If you're planning to work on a serious project, my strong advice: find another TTS repo. Go [here](https://github.com/CorentinJ/Real-Time-Voice-Cloning/issues/364) for more info.

**20/08/19:** I'm working on [resemblyzer](https://github.com/resemble-ai/Resemblyzer), an independent package for the voice encoder. You can use your trained encoder models from this repo with it.

**06/07/19:** Need to run within a docker container on a remote server? See [here](https://sean.lane.sh/posts/2019/07/Running-the-Real-Time-Voice-Cloning-project-in-Docker/).

**25/06/19:** Experimental support for low-memory GPUs (~2gb) added for the synthesizer. Pass `--low_mem` to `demo_cli.py` or `demo_toolbox.py` to enable it. It adds a big overhead, so it's not recommended if you have enough VRAM.


## Setup

### 1. Install Requirements

**Python 3.6 or 3.7** is needed to run the toolbox.

* Install [PyTorch](https://pytorch.org/get-started/locally/) (>=1.0.1).
* Install [ffmpeg](https://ffmpeg.org/download.html#get-packages).
* Run `pip install -r requirements.txt` to install the remaining necessary packages.

### 2. Download Pretrained Models
Download the latest [here](https://github.com/CorentinJ/Real-Time-Voice-Cloning/wiki/Pretrained-models).

### 3. (Optional) Test Configuration
Before you download any dataset, you can begin by testing your configuration with:

`python demo_cli.py`

If all tests pass, you're good to go.

### 4. (Optional) Download Datasets
For playing with the toolbox alone, I only recommend downloading [`LibriSpeech/train-clean-100`](https://www.openslr.org/resources/12/train-clean-100.tar.gz). Extract the contents as `<datasets_root>/LibriSpeech/train-clean-100` where `<datasets_root>` is a directory of your choosing. Other datasets are supported in the toolbox, see [here](https://github.com/CorentinJ/Real-Time-Voice-Cloning/wiki/Training#datasets). You're free not to download any dataset, but then you will need your own data as audio files or you will have to record it with the toolbox.

### 5. Launch the Toolbox
You can then try the toolbox:

`python demo_toolbox.py -d <datasets_root>`  
or  
`python demo_toolbox.py`  

depending on whether you downloaded any datasets. If you are running an X-server or if you have the error `Aborted (core dumped)`, see [this issue](https://github.com/CorentinJ/Real-Time-Voice-Cloning/issues/11#issuecomment-504733590).

## 한국어 적용하기
* Ai Hub 자유대화 음성(일반남여) [**source**](https://aihub.or.kr/aidata/30703)
* 실행 순서
0. data preprocess
```
aihub_dataset 폴더 내 파이썬 코드 실행
두 코드 모두 drive 변수, 경로 확인 후 실행
move_wav.py
  - LibriSpeech와 같은 구조로 데이터 이동
json2txt.py
  - json 파일 내의 정보로 LibriSpeech와 같은 형태의 text 파일 만들기
두 코드 실행 후 원본 데이터들 [원천], [라벨]로 시작하는 폴더 삭제
less_than_10wavs.py
  - wav파일 10개 이하인 speaker dir 삭제
```

1. encoder
```
python encoder_preprocess.py E:\AI-Hub_data
python encoder_train.py run1 E:\AI-Hub_data\SV2TTS\encoder
```
* E:\AI-Hub_data\SV2TTS\encoder
  - 자유대화 음성(일반남녀)_Training_0.0baesubin
  - ...

2. synthesize
```
python synthesizer_preprocess_audio.py E:\AI-Hub_data
python synthesizer_preprocess_embeds.py E:\AI-Hub_data\SV2TTS\synthesizer
python synthesizer_train.py run1 E:\AI-Hub_data\SV2TTS\synthesizer
```
* E:\AI-Hub_data\SV2TTS\synthesizer
  - mels
  - audio
  - embed
  - train.txt - audio/mel/embed/wav_length/mel_frame/text
  - damaged.txt - 손상된 파일, 제거 요망 (JSON 메타데이터, .wav파일)

3. vocoder (Mel-spectrogram to audio)
```
python vocoder_preprocess.py E:\AI-Hub_data
python vocoder_train.py run1 E:\AI-Hub_data
```

## dataset 구조 비교
### datasets_root = E:\\AI-Hub data
[*각자 data 폴더 구조에 맞게 변경*]
|datasets_name|LibriSpeech|자유대화 음성(일반남녀)|
|---|---|---|
|subfolder|train-clean-100|Training|
|speaker|19|0.0baesubin	=> Speaker self.root|
|chapter|198|일반통합:01, 자유대화:02|
|text|19-198.trans.txt|0.0baesubin-01.trans.txt|
|audio|19-198-0000.flac|0.0baesubin-01-00002.wav|

==============================



## 한국어 입력 시 주의사항
숫자는 모두 한글로 표현하고 십진 단위로 띄어쓰기
```
  숫자를 하나씩 발음한 경우 띄어쓰기
  단위를 나타내는 '년', '월', '일', '시', '분' 등은 붙여쓰기
    - 이십 사시간, 스물 네시간, 오대 그룹, 자동차 다섯대, 팔 육 공에 이 사 삼 칠(860-2437)
    - 십 사시, 열 네시, 천 구백 구십 구년에
  숫자만으로 이루어진 기념일 등 특정 의미가 있는 단어들은 숫자 단위로 띄어쓰기
    - 팔 일 오(8.15), 사 일 구(4.19), 오 칠 오 공 부대(5750부대)
```

## 한글 jamo 분리 후 유니코드 변환 표
![`here`](https://user-images.githubusercontent.com/20488694/136505384-32791ea4-a406-4ab7-a0fc-812df7d1eb08.PNG)

*`EX) 나는 아름다운 나비`*

|ㄴ|ㅏ|ㄴ|ㅡ|ㄴ| |
|---|---|---|---|---|---|
|4|21|4|39|45|69|

|ㅇ|ㅏ|ㄹ|ㅡ|ㅁ|ㄷ|ㅏ|ㅇ|ㅜ|ㄴ| |
|---|---|---|---|---|---|---|---|---|---|---|
|13|21|7|39|57|5|21|13|34|45|69|

|ㄴ|ㅏ|ㅂ|ㅣ|EOS|
|---|---|---|---|---|
|4|21|9|41|1|
