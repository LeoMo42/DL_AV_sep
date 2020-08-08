import os, glob


class FrameInspector:
    @staticmethod
    def run(rootpath, av_range):
        dirpath = rootpath + 'video/'
        inspect_dir = dirpath + 'face_input'
        valid_frame_path = dirpath + 'valid_frame.txt'

        for i in range(av_range[0], av_range[1]):
            valid = True
            print('processing frame %s' % i)
            for j in range(1,76):
                if FrameInspector.check_frame(i, j, inspect_dir) is False:
                    path = inspect_dir + "/frame_%d_*.jpg" % i
                    for file in glob.glob(path):
                        os.remove(file)
                    valid = False
                    print('frame %s is not valid' % i)
                    break
            if valid:
                with open(valid_frame_path, 'a') as f:
                    frame_name = "frame_%d" % i
                    f.write(frame_name+'\n')

    @staticmethod
    def check_frame(idx, part, inspect_dir):
        path = inspect_dir + "/frame_%d_%02d.jpg" % (idx, part)
        if not os.path.exists(path):
            return False
        return True


if __name__ == "__main__":
    rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))) + "/data/"
    av_range = (0, 1000)
    FrameInspector.run(rootpath, av_range)
