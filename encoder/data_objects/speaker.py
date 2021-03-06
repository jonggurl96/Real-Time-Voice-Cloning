from encoder.data_objects.random_cycler import RandomCycler
from encoder.data_objects.utterance import Utterance
from pathlib import Path

# Contains the set of utterances of a single speaker
class Speaker:
    def __init__(self, root: Path):
        # SV2TTS/encoder/recorederID
        self.root = root # recorderId까지의 Path
        self.name = root.name # Path의 마지막 File/Dir: recorderId
        self.utterances = None
        self.utterance_cycler = None
        
    def _load_utterances(self):
        with self.root.joinpath("_sources.txt").open("r", encoding="utf-8") as sources_file:
            # [일반통합_0.0baesubin-일반통합-00002.npy,E:\AI-Hub_data\자유대화 음성(일반남녀)\Training\0.0baesubin\일반통합\0.0baesubin-일반통합-00002.wav]
            sources = [l.split(",") for l in sources_file]
        # {"일반통합_0.0baesubin-일반통합-00002.npy": "E:\AI-Hub_data\자유대화 음성(일반남녀)\Training\0.0baesubin\일반통합\0.0baesubin-일반통합-00002.wav"}
        sources = {frames_fname: wave_fpath for frames_fname, wave_fpath in sources}
        self.utterances = [Utterance(self.root.joinpath(f), w) for f, w in sources.items()]
        self.utterance_cycler = RandomCycler(self.utterances)
               
    def random_partial(self, count, n_frames):
        """
        Samples a batch of <count> unique partial utterances from the disk in a way that all 
        utterances come up at least once every two cycles and in a random order every time.
        
        :param count: The number of partial utterances to sample from the set of utterances from 
        that speaker. Utterances are guaranteed not to be repeated if <count> is not larger than 
        the number of utterances available.
        :param n_frames: The number of frames in the partial utterance.
        :return: A list of tuples (utterance, frames, range) where utterance is an Utterance, 
        frames are the frames of the partial utterances and range is the range of the partial 
        utterance with regard to the complete utterance.
        """
        if self.utterances is None:
            self._load_utterances()

        utterances = self.utterance_cycler.sample(count)

        a = [(u,) + u.random_partial(n_frames) for u in utterances]

        return a
