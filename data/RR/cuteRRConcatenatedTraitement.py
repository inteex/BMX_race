import pandas as pd
import glob
import os

'''
couper le fichier csv traitement de la ligne de depart alant a la ligne fin marker 
decaler le temps
'''


def dataCute(indir):
    directoryFiles = glob.glob(indir + '\\*\\')
    os.chdir(indir)

    # table = pd.read_csv('RR\\trial2\\ConcatenatedtraitementRomainRacin2.csv')
    # print(table.VitesseRider.index[table.VitesseRider.isnull()])
    # print(table.VitesseRider.first_valid_index())

    for directoryFile in directoryFiles:
        fileList = glob.glob((directoryFile.split('\\')[-2] + '\\*.csv'))
        print(fileList)

        if fileList:
            print(fileList[0])
            df = pd.read_csv(fileList[0])
            bip = 0  # debut : le moment du Bip
            finDep = int(df.VitesseRider.index[df.VitesseRider.isnull()][0])  # findep : find de deplacement

            df = df.loc[bip:finDep]

            df = df.reset_index(drop=True)
            df.to_csv(fileList[1].split('\\')[0]+'\\C'+ fileList[1].split('\\')[1], index=None)


if __name__ == '__main__':
        dataCute('..\\SD')