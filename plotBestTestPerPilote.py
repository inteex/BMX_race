import pandas as pd
import  matplotlib.pyplot as plt
import glob
import os
import numpy as np


class PlotBestTestPerPilote:

    def get_best_trial(self, indir):
        directoryFiles = glob.glob(indir + '\\*\\')
        os.chdir(indir)
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
            l = self.get_best_trial(file)
            bestTrials.append(l)
        return bestTrials

    def plotDataForceUForceUPiedAv(self, indir, xaxis, columnsToPlot):
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
                # txt = "{}".format()
                # plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
                plt.savefig('figures/{}_{}.png'.format(column,xi))
                #plt.show()

    def externDetailsPilote(self,indir):

        bestTrials = self.getAllBesttrials(indir)
        masseRiders=[]
        BraquetRiders=[]
        longueurManivelleRiders=[]
        tailleRiders=[]
        f = open('DetailsRiders.txt', 'w')
        print('-----------------------------',file=f)
        for trial in bestTrials:
            fileList = glob.glob((trial + '\\*.csv'))
            traitement = pd.read_csv(fileList[0]) #0 -> first file in list its CDonetraitement.csv
            frames = pd.read_csv(fileList[2])   #2 -  > third file in list its frames
            time = traitement['Time']
            if 'Braquet' in frames.columns: braquet = frames['Braquet'][0]
            else: braquet = 0
            if 'MasseRider' in frames.columns: masseRider = frames['MasseRider'][0]
            else: masseRider = 0
            if 'longueurManivelle' in frames.columns: longueurManivelle = frames['longueurManivelle'][0]
            else: longueurManivelle = 0
            if 'TailleRider' in frames.columns: tailleRider = frames['TailleRider'][0]
            else: tailleRider = 0
            print('{} time: {:.3f}s'.format(trial.split('\\')[-2], time.iloc[-2]),file=f)
            print('-----------------------------',file=f)
            print('Poide: {} '.format(masseRider),file=f)
            print('taille: {} '.format(tailleRider),file=f)
            print('braquet: {}'.format(braquet),file=f)
            print('Longueur Manivelle: {}'.format(longueurManivelle),file=f)
            print('-----------------------------',file=f)
            masseRiders.append(masseRider)
            tailleRiders.append(tailleRider)
            BraquetRiders.append(braquet*10)
            longueurManivelleRiders.append(longueurManivelle)


if __name__ == '__main__':
    obj = PlotBestTestPerPilote()
    columns = ['ForceUPiedAr','ForceUPiedAv','Travail']
    xaxis =  ['Time']
    #obj.plotDataForceUForceUPiedAv(indir='.\\data\\',xaxis=xaxis,columnsToPlot=columns)
    obj.externDetailsPilote(indir='.\\data\\')


