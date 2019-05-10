import pandas as pd
import glob
import os
from navigate_to_trials import NavigateFiles


class TempRecation:
    def get_tps_reaction_all_pilots(self):
        files = NavigateFiles().get_all_files_by_num(data_indir='.\\data\\', position_file=2)
        for frames in files:
            pilot_name = frames[0].split("\\")[-3]
            f = open('tps_reaction\\{}.csv'.format(pilot_name), 'w')
            print("TpsReaction,", file=f)
            for frame in frames:
                # pilot_name = frame.split("\\")[-3]
                frames_df = pd.read_csv(frame)
                tps_reaction = frames_df['TpsReaction'][0] - frames_df["Bip"][0]

                print("{},".format(tps_reaction), file=f)


if __name__ == '__main__':
    t = TempRecation()
    t.get_tps_reaction_all_pilots()
