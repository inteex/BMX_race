import pandas as pd
import glob
import os


class DataCute:
    def data_cute(self, pilote_indir):
        """
        couper le fichier csv traitement de la ligne de depart alant a la ligne fin marker
        decaler le temps
        :param pilote_indir: Path to pilot data.
        :return:Csv File.
        """

        directoryFiles = glob.glob(pilote_indir + '\\*\\')
        os.chdir(pilote_indir)
        for directoryFile in directoryFiles:
            fileList = glob.glob((directoryFile.split('\\')[-2] + '\\*.csv'))
            if fileList:
                df = pd.read_csv(fileList[0])
                frame = pd.read_csv(fileList[2])
                bip = int(frame.Bip[0])  # debut : le moment du Bip
                if 'FinMarkerVisible' in df:
                    finDep = int(frame.FinMarkerVisible[0])  # findep : find de deplacement
                else:
                    finDep = int(frame.FinDplcmt[0])
                """
                    decaler le Temps au moment du prmier Bip
                    et prendre l'interval entre le Bip et fin deplacement
                """
                time = df.Time
                time = time.loc[0:finDep - bip]
                df = df.loc[bip:finDep]
                df['Time'] = time.values

                df = df.reset_index(drop=True)
                df.to_csv(fileList[1].split('\\')[0] + '\\cuted' + fileList[1].split('\\')[1], index=None)

    def cute_in_first_null_vitesse(self, pilote_indir):
        """
        couper le fichier csv traitement de la ligne de depart alant a la ligne fin marker
        decaler le temps
        :param pilote_indir:Path to pilot data.
        :return:Csv file.
        """
        directoryFiles = glob.glob(pilote_indir + '\\*\\')
        os.chdir(pilote_indir)

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
                df.to_csv(fileList[1].split('\\')[0] + '\\cuted' + fileList[1].split('\\')[1], index=None)


if __name__ == '__main__':
    cut = DataCute()
    cut.data_cute('..\\data\\AP\\')
