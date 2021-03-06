# Before running, make sure avspeech_train.csv and avspeech_test.csv are in catalog.
# if not, see the requirement.txt
# download and preprocess the data from AVspeech dataset
import av_sep.preprocessing.lib.AVHandler as avh
import pandas as pd
import os


class AudioDownloader:
    @staticmethod
    def run(rootpath, av_range):
        cat_train = pd.read_csv(rootpath + 'catalog/avspeech_train.csv')
        cat_test = pd.read_csv(rootpath + 'catalog/avspeech_test.csv')

        # create 80000-90000 audios data from 290K
        av_dir = rootpath + 'audio/audio_train'
        avh.mkdir(av_dir)
        AudioDownloader.m_audio(av_dir, 'audio_train', cat_train, av_range[0], av_range[1])

    @staticmethod
    def m_link(youtube_id):
        # return the youtube actual link
        link = 'https://www.youtube.com/watch?v='+youtube_id
        return link

    @staticmethod
    def m_audio(loc, name, cat, start_idx, end_idx):
        # make concatenated audio following by the catalog from AVSpeech
        # loc       | the location for file to store
        # name      | name for the wav mix file
        # cat       | the catalog with audio link and time
        # start_idx | the starting index of the audio to download and concatenate
        # end_idx   | the ending index of the audio to download and concatenate

        for i in range(start_idx, end_idx):
            f_name = name+str(i)
            link = AudioDownloader.m_link(cat.loc[i, 'link'])
            start_time = cat.loc[i, 'start_time']
            end_time = start_time + 3.0
            avh.download(loc, f_name, link)
            avh.cut(loc, f_name, start_time, end_time)


if __name__ == "__main__":
    rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))) + "/data/"
    av_range = (0, 1000)
    AudioDownloader.run(rootpath, av_range)
