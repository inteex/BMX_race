import os
import glob
import pandas

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
        size = os.stat(filename).st_size//1024
        if  size <= 5:
            print(filename)
            print('<<<<<<<<<<<<<<9 ::: ' + str(size))
            df = pandas.read_csv(filename,header=None)
            for col in range(len(df.columns)):
                colnamesframe.append(filename[:-4])
            dfListframes.append(df)
        if (size <= 49) & (size > 5):
            print('>9  ::: ' + str(size))
            df = pandas.read_csv(filename, header=None)
            for col in range(len(df.columns)):
                colnamestravail.append(filename[:-4])
            dfListtrvail.append(df)
        if size > 49:
            print('>15  ::: ' + str(size))
            df = pandas.read_csv(filename, header=None)
            for col in range(len(df.columns)):
                colnamestraitement.append(filename[:-4])
            dfListtraitement.append(df)

    concatframes = pandas.concat(dfListframes, axis=1)
    concatframes.columns = colnamesframe
    concatframes.to_csv('dir/frames'+piloteName+'.csv', index=None)

    concattravail = pandas.concat(dfListtrvail, axis=1)
    concattravail.columns = colnamestravail
    concattravail.to_csv('dir/travail'+piloteName+'.csv', index=None)

    concattraitement = pandas.concat(dfListtraitement, axis=1)
    concattraitement.columns = colnamestraitement
    concattraitement.to_csv('dir/traitement'+piloteName+'.csv', index=None)

    # for filename in fileList:
    #     df = pandas.read_csv(filename,header=None)
    #     for col in range(len(df.columns)):
    #         colnamesframe.append(filename[:-4])
    #     dfListframes.append(df)
    # concatframes = pandas.concat(dfListframes, axis=1)
    # concatframes.columns = colnamesframe
    # concatframes.to_csv('framesRomainMayet5.csv', index=None)

if __name__ == '__main__':

    directoryFiles = glob.glob("C:\\Users\\mekhezzr\\Desktop\\donnees\\RR\\RomainRacin7")
    os.mkdir('C:\\Users\\mekhezzr\\Desktop\\donnees\\RR\\RomainRacin7\\dir')
    for directoryFile in directoryFiles:
        print(directoryFile)
        concatenate(indir=directoryFile)
        #,outfile=directoryFile.split('\\')[-2] + '5.csv'

    # directoryFiles = glob.glob("C:\\Users\\mekhezzr\\Desktop\\donnees\\RM\\RomainMayet8\\frames")
    # for directoryFile in directoryFiles:
    #     print(directoryFile)
    #     concatenate(indir=directoryFile)
