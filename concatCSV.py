import os
import glob
import pandas

"""
 concatener tous les fichier csv prensent dans un dossier en colonne
  sous 3 fichiers csv dans les nom sont frames,traitement ou travail selon la taile
"""


def concatenate(indir):
    os.chdir(indir)
    fileList = glob.glob("*.csv")
    dfListframes=[]
    dfListtrvail=[]
    dfListtraitement=[]
    colnamesframe=[]
    colnamestravail=[]
    colnamestraitement=[]
    piloteName = indir.split('\\')[-1]

    for filename in fileList:
        size = os.stat(filename).st_size//1024 #obtenir la taill en ko

        if  size <= 5:
            print(filename)
            print('<<<<<<<<<<<<<<9 ::: ' + str(size))
            df = pandas.read_csv(filename,header=None)
            for col in range(len(df.columns)):  # pour les fichier csv qui on plus d' une colonnes
                colnamesframe.append(filename[:-4])  # affecter le meme nom de colonne pour tous les colonnes
            dfListframes.append(df)  # ajouter le fichier de taille < 5 ko  dans la list dfListframes

        if (size <= 53) & (size > 5):
            print('>9  ::: ' + str(size))
            df = pandas.read_csv(filename, header=None)
            for col in range(len(df.columns)):
                colnamestravail.append(filename[:-4])
            dfListtrvail.append(df)

        if size > 53:
            print('>15  ::: ' + str(size))
            df = pandas.read_csv(filename, header=None)
            for col in range(len(df.columns)):
                colnamestraitement.append(filename[:-4])
            dfListtraitement.append(df)

    concatframes = pandas.concat(dfListframes, axis=1)  # concatener les fichier qui figure dans dfListframes
    concatframes.columns = colnamesframe  # renommer toute les colonne par les nom obtenu en haut dans la var colnamesframe
    concatframes.to_csv('dir/frames'+piloteName+'.csv', index=None)  # sauvgarder les fichier sous le nom de frames+nom du pilote+numero de test

    concattravail = pandas.concat(dfListtrvail, axis=1)
    concattravail.columns = colnamestravail
    concattravail.to_csv('dir/travail'+piloteName+'.csv', index=None)

    concattraitement = pandas.concat(dfListtraitement, axis=1)
    concattraitement.columns = colnamestraitement
    concattraitement.to_csv('dir/traitement'+piloteName+'.csv', index=None)


def concatInSingleFile(indir):
    os.chdir(indir)
    fileList = glob.glob("*.csv")
    colnamesframe = []
    dfListframes= []
    for filename in fileList:
        df = pandas.read_csv(filename, header=None)
        for col in range(len(df.columns)):
            colnamesframe.append(filename[:-4])
        dfListframes.append(df)
    concatframes = pandas.concat(dfListframes, axis=1)
    concatframes.columns = colnamesframe
    concatframes.to_csv(indir.split('\\')[-1] + 'RomainMayet5.csv', index=None)


if __name__ == '__main__':

    directoryFiles = glob.glob("C:\\Users\\mekhezzr\\Desktop\\donnees\\TJ\\ThomasJouve9")
    os.mkdir('C:\\Users\\mekhezzr\\Desktop\\donnees\\TJ\\ThomasJouve9\\dir')
    for directoryFile in directoryFiles:
        print(directoryFile)
        concatenate(indir=directoryFile)
        # ,outfile=directoryFile.split('\\')[-2] + '5.csv'

    # directoryFiles = glob.glob("C:\\Users\\mekhezzr\\Desktop\\donnees\\TJ\\ThomasJouve8\\traitement")
    # for directoryFile in directoryFiles:
    #     print(directoryFile)
    #     concatInSingleFile(indir=directoryFile)
