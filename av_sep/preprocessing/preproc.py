import os
from av_sep.preprocessing.audio.audio_downloader import AudioDownloader
from av_sep.preprocessing.audio.audio_norm import AudioNorm
from av_sep.preprocessing.audio.build_audio_database import AudioDatabaseBuilder

from av_sep.preprocessing.av_log.gentxtnew import GenLogs

import av_sep.preprocessing.lib.AVHandler as avh

from av_sep.preprocessing.video.video_download import VideoDownloader
from av_sep.preprocessing.video.MTCNN_detect import MtcnnDetector
from av_sep.preprocessing.video.frame_inspector import FrameInspector

if __name__ == "__main__":
    rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) + "/data/"
    av_range = (0, 1000)
    max_num_sample = 50000

    avh.mkdir(rootpath + 'audio')
    avh.mkdir(rootpath + 'video')

    # Download audio data
    AudioDownloader.run(rootpath, av_range)

    # Normalize audio data
    AudioNorm.run(rootpath, av_range)
    
    # Download visual data
    VideoDownloader.run(rootpath, av_range)

    # Detect and Crop face
    MtcnnDetector.run(rootpath, av_range)
    FrameInspector.run(rootpath, av_range)
    
    # Create audio database
    AudioDatabaseBuilder.run(rootpath, av_range, max_num_sample)

    # Generate log file for data generator
    GenLogs.run(rootpath)
