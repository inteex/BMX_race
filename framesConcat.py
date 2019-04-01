import pandas as pd
import os
import glob
import numpy as np


class FramesConcate:
    def getFrames(self, indir):
        directoryFiles = glob.glob(indir + '\\*\\')
        os.chdir(indir)
        frames= []

        for directoryFile in directoryFiles:
            fileList = glob.glob((directoryFile.split('\\')[-2] + '\\*.csv'))
            frame = pd.read_csv(fileList[2])
            frames.append(indir+fileList[2])

        os.chdir('..\\..')
        return frames

    def getAllFrames(self, indir):
        directoryFiles = glob.glob(indir + '\\*\\')
        allframes = []
        for file in directoryFiles:
            l = self.getFrames(file)
            allframes.append(l)
        return allframes

    def concatenatallframes(self,indir):
        frames = self.getAllFrames(indir)
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
        appended_data.fillna
        appended_data.to_csv("data\\AllframesConcatenated.csv",index=0)





if __name__ == '__main__':
    frames = FramesConcate()
    #print(frames.concatenatallframes('.\\data\\'))
    print(frames.getAllFrames('data\\'))