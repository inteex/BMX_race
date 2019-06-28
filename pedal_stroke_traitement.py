import pandas as pd
import matplotlib.pyplot as plt
import glob
from navigate_to_trials import NavigateFiles


class PedalStrokeTraitement:
    def get_mean_by_pedal_stroke(self, params, data_indir):
        traitement_files = NavigateFiles().get_all_files_by_num(data_indir, 1)
        frame_files = NavigateFiles().get_all_files_by_num(data_indir, 0)
        for traitements,frames in zip(traitement_files, frame_files):
            print("pilot :{} ... ".format(frames[0]).split('\\')[-3])
            for traitement, frame in zip(traitements, frames):
                df_traitement = pd.read_csv(traitement)
                df_frame = pd.read_csv(frame)
                coups_de_pedal0 = df_frame["TpsReaction"][0] - df_frame["Bip"][0]
                coups_de_pedal1 = df_frame['CoupsDePedal'][0] - df_frame["Bip"][0]
                coups_de_pedal2 = df_frame['CoupsDePedal.1'][0] - df_frame["Bip"][0]
                coups_de_pedal3 = df_frame['CoupsDePedal.2'][0] - df_frame["Bip"][0]

                df_coups_de_pedal0 = df_traitement[int(coups_de_pedal0):int(coups_de_pedal1)]
                print(df_coups_de_pedal0['Puissance'].mean())



        # legend = []
        # for xi in x_axis:  # for all x axis variables
        #     for trial in best_trials:  # for the best trail of the pilot
        #         fileList = glob.glob((trial + '\\*.csv'))  # all files of a trial
        #         traitement = pd.read_csv(fileList[1])  # first file in the trail
        #         frames = pd.read_csv(fileList[0])
        #         pilot_name = trial.split('\\')[-2]
        #         x = traitement[xi]



if __name__ == '__main__':
  pst = PedalStrokeTraitement()
  pst.get_mean_by_pedal_stroke(data_indir='data_v2',params=0)