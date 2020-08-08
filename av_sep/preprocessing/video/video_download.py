from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import datetime
import av_sep.preprocessing.lib.AVHandler as avh
import pandas as pd


class VideoDownloader:
    @staticmethod
    def run(rootpath, av_range):
        locpath = rootpath + 'video/video_train'
        framespath = rootpath + 'video/frames'
        avh.mkdir(locpath)
        avh.mkdir(framespath)
        cat_train = pd.read_csv(rootpath + 'catalog/avspeech_train.csv')

        # download video , convert to images separately
        # avh.video_download(loc='video_train',v_name='video_train',cat=cat_train,start_idx=2,end_idx=4)
        # avh.generate_frames(loc='video_train',v_name='clip_video_train',start_idx=2,end_idx=4)

        # download each video and convert to frames immediately
        # download_video_frames(loc='video_train',cat=cat_train,start_idx=1405,end_idx=2000,rm_video=True)
        VideoDownloader.download_video_frames(framespath=framespath, loc=locpath, cat=cat_train, start_idx=av_range[0], end_idx=av_range[1], rm_video=True)

    @staticmethod
    def video_download(loc, cat, start_idx, end_idx):
        # Only download the video from the link
        # loc        | the location for downloaded file
        # v_name     | the name for the video file
        # cat        | the catalog with audio link and time
        # start_idx  | the starting index of the video to download
        # end_idx    | the ending index of the video to download

        for i in range(start_idx, end_idx):
            command = 'cd %s;' % loc
            f_name = str(i)
            link = avh.m_link(cat.loc[i, 'link'])
            start_time = cat.loc[i, 'start_time']
            end_time = start_time + 3.0
            start_time = datetime.timedelta(seconds=start_time)
            end_time = datetime.timedelta(seconds=end_time)
            command += 'ffmpeg -i $(youtube-dl -f ”mp4“ --get-url ' + link + ') ' + '-c:v h264 -c:a copy -ss %s -to %s %s.mp4' \
                    % (start_time, end_time, f_name)
            #command += 'ffmpeg -i %s.mp4 -r 25 %s.mp4;' % (f_name,'clip_' + f_name) #convert fps to 25
            #command += 'rm %s.mp4' % f_name
            os.system(command)

    @staticmethod
    def generate_frames(framespath, loc, start_idx, end_idx):
        # get frames for each video clip
        # loc        | the location of video clip
        # v_name     | v_name = 'clip_video_train'
        # start_idx  | the starting index of the training sample
        # end_idx    | the ending index of the training sample

        for i in range(start_idx, end_idx):
            command = 'cd %s;' % loc
            f_name = str(i)
            command += 'ffmpeg -i %s.mp4 -y -f image2  -vframes 75 %s/%s-%%02d.jpg' % (f_name, framespath, f_name)
            os.system(command)

    @staticmethod
    def download_video_frames(framespath, loc, cat, start_idx, end_idx, rm_video):
        # Download each video and convert to frames immediately, can choose to remove video file
        # loc        | the location for downloaded file
        # cat        | the catalog with audio link and time
        # start_idx  | the starting index of the video to download
        # end_idx    | the ending index of the video to download
        # rm_video   | boolean value for delete video and only keep the frames

        for i in range(start_idx, end_idx + 1):
            command = 'cd %s;' % loc
            f_name = str(i)
            link = avh.m_link(cat.loc[i, 'link'])
            start_time = cat.loc[i, 'start_time']
            end_time = start_time + 3.0
            start_time = datetime.timedelta(seconds=start_time)
            end_time = datetime.timedelta(seconds=end_time)
            command += 'ffmpeg -i $(youtube-dl -f ”mp4“ --get-url ' + link + ') ' + '-c:v h264 -c:a copy -ss %s -to %s %s.mp4;' \
                       % (start_time, end_time, f_name)
            #command += 'ffmpeg -i %s.mp4 -r 25 %s.mp4;' % (f_name, 'clip_' + f_name)  # convert fps to 25
            #command += 'rm %s.mp4;' % f_name

            #converts to frames
            #command += 'ffmpeg -i %s.mp4 -y -f image2  -vframes 75 ../frames/%s-%%02d.jpg;' % (f_name, f_name)
            command += 'ffmpeg -i %s.mp4 -vf fps=25 %s/%s-%%02d.jpg;' % (f_name, framespath, f_name)
            #command += 'ffmpeg -i %s.mp4 ../frames/%sfr_%%02d.jpg;' % ('clip_' + f_name, f_name)

            if rm_video:
                command += 'rm %s.mp4' % f_name
            os.system(command)


if __name__ == "__main__":
    rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))) + "/data/"
    av_range = (0, 1000)
    VideoDownloader.run(rootpath, av_range)
