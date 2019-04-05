import pandas as pd
import os
import glob
import numpy as np
from navigate_to_trials import NavigateFiles


class FramesConcate:

    def concatenatallframes(self,indir,fileNum = 2):
        """
        Concatenate all frames of all pilotes in a single csv file.

        Parameters
        ----------
            indir : string,
                Path to data.

            fileNum :int,
                File position in the trial of a pilote.

        """
        frames = NavigateFiles().get_all_files_by_num(indir,fileNum)
        appended_data=[]
        for pilote in frames:
            for f in pilote:

                trials = "\\".join(f.split('\\')[1:4])
                fileList = glob.glob((trials + '\\*.csv'))
                traits = pd.read_csv(fileList[0])
                time = traits['Time'][len(traits)-2]
                frames =pd.read_csv(f)
                frame = frames[['TailleRider','longueurManivelle']]
                if 'Braquet' in frames.columns:
                    frame['Braquet']=frames['Braquet']
                if 'MasseRider' in frames.columns:
                    frame['MasseRider']=frames['MasseRider']
                if 'MasseBike' in frames.columns:
                    frame['MasseBike']=frames['MasseBike']
                frame['TimeEnd'] = time
                appended_data.append(frame.iloc[0:1])
        appended_data = pd.concat(appended_data,axis=0)
        appended_data.to_csv("data\\AllframesConcatenated.csv",index=0)





if __name__ == '__main__':
    frames = FramesConcate()
    print(frames.concatenatallframes('.\\data\\'))
    # print(frames.getAllFrames('data\\'))