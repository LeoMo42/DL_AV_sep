import numpy as np
from keras.models import load_model
from keras.models import Model
import matplotlib.image as mpimg
import os


class LoadPretrained:
    @staticmethod
    def run(rootpath):
        ## Parameters
        PB = 0
        CKPT = 0
        HDF5 = 1
        ROOTPATH = rootpath
        MODEL_PATH = ROOTPATH + 'pretrain_model/FaceNet_keras/facenet_keras.h5'
        VALID_FRAME_LOG_PATH = ROOTPATH + 'video/valid_frame.txt'
        FACE_INPUT_PATH = ROOTPATH + 'video/face_input/'

        save_path = ROOTPATH + 'video/face_emb/'
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        model = load_model(MODEL_PATH)
        model.summary()
        avgPool_layer_model = Model(inputs=model.input, outputs=model.get_layer('AvgPool').output)

        with open(VALID_FRAME_LOG_PATH, 'r') as f:
            lines = f.readlines()

        for line in lines:
            embtmp = np.zeros((75, 1, 1792))
            headname = line.strip()
            for i in range(1, 76):
                if i < 10:
                    tailname = '_0{}.jpg'.format(i)
                else:
                    tailname = '_' + str(i) + '.jpg'
                picname = headname + tailname
                I = mpimg.imread(FACE_INPUT_PATH + picname)
                I_np = np.array(I)
                I_np = I_np[np.newaxis, :, :, :]
                embtmp[i - 1, :] = avgPool_layer_model.predict(I_np)

            people_index = int(line.strip().split('_')[1])
            npname = '{:05d}_face_emb.npy'.format(people_index)
            print(npname)

            np.save(save_path + npname, embtmp)
            with open(ROOTPATH + 'faceemb_dataset.txt', 'a') as d:
                d.write(npname + '\n')


if __name__ == "__main__":
    rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))) + "/data/"
    LoadPretrained.run(rootpath)
