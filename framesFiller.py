from framesConcat import FramesConcate
import pandas as pd
from navigate_to_trials import NavigateFiles

class FramesFiller:
    def filleframes(self,indir):
        frames = NavigateFiles().get_all_files_by_num(indir=indir,fileNum=2)
        for frame in frames:
            for f in frame:
                dataframes =pd.read_csv(f)
                pilote = f.split('\\')[2]
                print(pilote)
                if pilote == 'AP':
                        dataframes['Braquet']= 2.764705
                if pilote == 'JR':
                                     dataframes['Braquet']= 2.75
                if pilote == 'MR':
                                     dataframes['Braquet']= 2.8125
                if pilote == 'RM':
                                     dataframes['Braquet']= 2.79375
                if pilote == 'RMathieu':
                                     dataframes['Braquet']= 2.75
                if pilote == 'RR':
                                     dataframes['Braquet']= 2.764705
                if pilote == 'SA':
                                     dataframes['Braquet']= 2.7222
                if pilote == 'SD':
                                     dataframes['Braquet']= 2.8823
                print( dataframes['Braquet'][0])


if __name__ == '__main__':
    obj = FramesFiller()
    obj.filleframes(indir='.\\data\\')