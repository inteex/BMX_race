import os
import glob
import pandas as pd

def concatenate(indir):
    directoryFiles = glob.glob(indir + '\\*\\')
    os.chdir(indir)
    dfList= []

    for directoryFile in directoryFiles:
        fileList = glob.glob((directoryFile.split('\\')[-2] + '\\*.csv'))
        print(fileList)
        if fileList:

            traitment = pd.read_csv(fileList[0]) #2 - > fichier traitement csv l'ordre de fichier dans le dossier important
            travail = pd.read_csv(fileList[3])  #3 - > fichier travail
            dfList.append(traitment)
            dfList.append(travail)
            outfile = fileList[1].split('\\')[0] + '\\Concatenated' + fileList[2].split('\\')[1]
            concatDf = pd.concat(dfList, axis=1)
            concatDf.to_csv(outfile, index=None)
            dfList = []

if __name__ == '__main__':
    concatenate(indir='RR')