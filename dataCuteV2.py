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

    for directoryFile in directoryFiles:
        fileList = glob.glob((directoryFile.split('\\')[-2] + '\\*.csv'))
        print(fileList)

        if fileList:
            print(fileList[0])
            df = pd.read_csv(fileList[1])
            frame = pd.read_csv(fileList[0])
            bip = int(frame.Bip[0])  # debut : le moment du Bip
            finDep = int(frame.FinMarkerVisible[0])  # findep : find de deplacement

            '''
                decaler le Temps au moment du prmier Bip
                et prendre l'interval entre le Bip et fin deplacement
            '''
            time = df.Time
            time = time.loc[0:finDep - bip]

            df = df.loc[bip:finDep]
            df['Time'] = time.values

            df = df.reset_index(drop=True)
            df.to_csv(fileList[1].split('\\')[0]+'\\Done'+ fileList[1].split('\\')[1], index=None)


if __name__ == '__main__':
        dataCute('.\\data\\TJ\\')