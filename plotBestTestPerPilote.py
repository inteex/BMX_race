import pandas as pd
import  matplotlib.pyplot as plt
import glob
import os
import numpy as np


class PlotBestTestPerPilote:
    def getBestTrial(self , indir):
        directoryFiles = glob.glob(indir + '\\*\\')
        os.chdir(indir)
        Bip = 0
        finDep = 0
        trialToTake = ''
        TimeToTake = 2000


        for directoryFile in directoryFiles:
            fileList = glob.glob((directoryFile.split('\\')[-2] + '\\*.csv'))
            traitement = pd.read_csv (fileList[0])
            frames = pd.read_csv (fileList[2])


            if 'FinDplcmt' in frames.columns:
                finDep = frames.FinDplcmt[0]-frames.Bip[0]
            else:
                finDep = len(traitement)-1


            timeFinDep = traitement.Time[finDep-1]
            vitess = traitement.VitesseRider[finDep-1]
            # print(timeFinDep)
            # print(vitess)
            currentTime = timeFinDep
            if currentTime <= TimeToTake:
                TimeToTake = currentTime
                filetotake = indir + fileList[0].split('\\')[0]


        os.chdir('..\\..')
        return filetotake

    def getAllBesttrials(self,indir):
        directoryFiles = glob.glob(indir + '\\*\\')
        bestTrials = []
        for file in directoryFiles:
            l = self.getBestTrial(file)
            bestTrials.append(l)
        return bestTrials


    def plotDataForceUForceUPiedAv(self,indir,xaxis,columnsToPlot):
        bestTrials = self.getAllBesttrials(indir)
        legend = []
        for xi in xaxis:
            for column in columnsToPlot:
                plt.figure(num=None, figsize=(12.8, 7.2), dpi=300, facecolor='w', edgecolor='k')
                for trial in bestTrials:
                    fileList = glob.glob((trial + '\\*.csv'))
                    traitement = pd.read_csv(fileList[0])
                    x = traitement[xi]
                    time =traitement['Time']
                    col = traitement[column]
                    plt.plot(x,col)
                    legend.append('{} {} time:{:.3f}s'.format(trial.split('\\')[-2],trial.split('\\')[-1],time.iloc[-2]))
                    print('{} time: {}'.format(trial.split('\\')[-2],time.iloc[-2]))

                print()
                print()
                plt.xlabel(xi)
                plt.ylabel(column)
                plt.legend(legend)
                plt.title('{} en fonction de {}'.format(column,xi))
                plt.grid()
                plt.savefig('figures/{}_{}.png'.format(column,xi))
                #plt.show()


if __name__ == '__main__':
    obj = PlotBestTestPerPilote()
    columns = ['ForceUPiedAr','ForceUPiedAv','IndiceEfficacitePiedAr','IndiceEfficacitePiedAv','VitesseRider']
    xaxis =  ['ThetaMDeg','Time']
    obj.plotDataForceUForceUPiedAv(indir='.\\data\\',xaxis=xaxis,columnsToPlot=columns)


