import librosa
import os
import numpy as np
import scipy.io.wavfile as wavfile


class AudioNorm:
    @staticmethod
    def run(rootpath, av_range):
        if not os.path.isdir(rootpath + 'audio/norm_audio_train'):
            os.mkdir(rootpath + 'audio/norm_audio_train')

        for num in range(av_range[0], av_range[1]):
            path = rootpath + 'audio/audio_train/trim_audio_train%s.wav' % num
            norm_path = rootpath + 'audio/norm_audio_train/trim_audio_train%s.wav' % num
            if os.path.exists(path):
                audio, _ = librosa.load(path, sr=16000)
                max_v = np.max(np.abs(audio))
                norm_audio = np.divide(audio, max_v)
                wavfile.write(norm_path, 16000, norm_audio)


if __name__ == "__main__":
    rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))) + "/data/"
    av_range = (0, 1000)
    AudioNorm.run(rootpath, av_range)
