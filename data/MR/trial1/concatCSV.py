import os
import glob
import pandas

def concatenate(indir='./',outfile='./MathisRagot1.csv'):
    os.chdir(indir)
    fileList = glob.glob("*.csv")
    dfList=[]
    colnames=[]



    for filename in fileList:
        print(filename)
        df = pandas.read_csv(filename)

        dfList.append(b)

    concatDf = pandas.concat(dfList, axis=1)
    concatDf.to_csv(outfile,index=None)

if __name__ == '__main__':
    concatenate()