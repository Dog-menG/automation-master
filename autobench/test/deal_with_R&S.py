import pandas as pd
import os


class process_RS_file(object):

    def __init__(self, file_name):
        self.file_name = file_name
        self.mid_file = pd.read_csv(file_name, header=None)

    def process_the_file(self):
        index = self.mid_file[self.mid_file[0].str.contains('Values')].index.tolist()
        length = len(index)
        if length == 0:
            print 'The file does not contain wanted data, please make sure using the right file.'
            return -1
        else:
            phase_noise = self.mid_file[int(index[0])+1:].copy()
        phase_noise.columns = ['whole data']
        transition = phase_noise['whole data'].apply(lambda x: x.split(';'))
        phase_noise['Offset Frequency (Hz)'] = transition.apply(lambda x: x[0])
        phase_noise['Phase Noise (dBc/Hz)'] = transition.apply(lambda x: x[1])
        del phase_noise['whole data']
        file_name = 'Processed_' + self.file_name
        phase_noise.to_csv(file_name, index=False)


def main():
    path = r'C:\Users\jgou\Desktop\test'
    os.chdir(path)
    file_names = os.listdir(path)
    for file_name in file_names:
        if file_name.endswith('csv') or file_name.endswith('CSV'):
            process_file = process_RS_file(file_name)
            process_file.process_the_file()

if __name__ == "__main__":
    main()
