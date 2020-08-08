import os

class GenLogs:
    @staticmethod
    def run(rootpath):
        with open(rootpath + 'audio/AV_model_database/dataset_train.txt', 'r') as t:
            lines = t.readlines()
            for line in lines:
                info = line.strip().split('.')
                num1 = info[0].strip().split('-')[1]
                num2 = info[0].strip().split('-')[2]

                newline = line.strip() + ' ' + num1 + '_face_emb.npy' + ' ' + num2 + '_face_emb.npy\n'
                with open(rootpath + 'audio/AVdataset_train.txt', 'a') as f:
                    f.write(newline)

        with open(rootpath + 'audio/AV_model_database/dataset_val.txt', 'r') as t:
            lines = t.readlines()
            for line in lines:
                info = line.strip().split('.')
                num1 = info[0].strip().split('-')[1]
                num2 = info[0].strip().split('-')[2]

                newline = line.strip() + ' ' + num1 + '_face_emb.npy' + ' ' + num2 + '_face_emb.npy\n'
                with open(rootpath + 'audio/AVdataset_val.txt', 'a') as f:
                    f.write(newline)


if __name__ == "__main__":
    rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))) + "/data/"
    GenLogs.run(rootpath)
