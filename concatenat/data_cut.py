import pandas as pd
import glob
import os
from shutil import copyfile


class DataCut:
    def data_cut(self, data_indir):
        """
        cut traitement csv file from Bip to fin Marker
        time satarts from -0.36.

        <<2>>
           :param data_indir: Path to pilot data.
           :return: Csv File.
        """
        directory_files = glob.glob('{}\\*\\'.format(data_indir))
        print("=" * 50)
        print("cut traitement and shif time (starts -0.36)")
        print("=" * 50)
        for pilote_indir in directory_files:
            trials = glob.glob(pilote_indir + '\\*\\')
            os.chdir(pilote_indir)
            print('cut ...\n{}'.format(pilote_indir))
            for trial in trials:
                traitement_path = glob.glob((trial.split('\\')[-2] + '\\traitement_*.csv'))
                frames_path = glob.glob((trial.split('\\')[-2] + '\\frames_*.csv'))

                traitement = pd.read_csv(traitement_path[0])
                frame = pd.read_csv(frames_path[0])

                bip = int(frame.Bip[0])  # debut : le moment du Bip
                if 'FinMarkerVisible' in frame.columns:
                    finDep = int(frame.FinMarkerVisible[0])
                else:
                    finDep = int(frame.FinDplcmt[0])

                # decaler le Temps au moment du prmier Bip
                # et prendre l'interval entre le Bip et fin deplacement
                time = traitement.Time
                time_before_reaction = -(time.loc[0:109][::-1])

                time_before_reaction = time_before_reaction.reset_index(drop=True)
                time_before_reaction = time_before_reaction.append(pd.Series([0]), ignore_index=True)
                """
                indeccies are shifted by 111 when time starts from 
                -0.36 instead of 0 so the index of finDep is shifted too by 111 .
                 """
                time = time.loc[0:finDep - bip - 111]
                time_before_reaction = pd.Series(time_before_reaction)
                time = pd.Series(time)

                time = time_before_reaction.append(time, ignore_index=True)

                traitement = traitement.loc[bip:finDep]
                traitement['Time'] = time.values

                traitement = traitement.reset_index(drop=True)
                outfile = '.\\{}\\cuted_fin_dep_{}'.format(trial.split('\\')[-2], traitement_path[0].split('\\')[-1])
                traitement.to_csv(outfile, index=None)

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

    def copy_files(self, data_indir, destination_data_indir):
        """
        Copy traitment and frames only in the specified directory

        <<4>>
            :param data_indir: Path to pilot data.
            :param destination_data_indir: Path to save the new data base.
        """
        directoryFiles = glob.glob("{}\\*\\".format(data_indir))
        print("="*50)
        print("Copy")
        print("="*50)
        for pilote_indir in directoryFiles:
            print(pilote_indir.split('\\')[-2])
            trials = glob.glob('{}\\*\\'.format(pilote_indir))
            for trial in trials:
                traitement_path = glob.glob(('{}\\concat_cuted_fin_dep_traitement_*.csv'.format(trial)))
                frames_path = glob.glob(('{}\\frames_*.csv'.format(trial)))

                path_files = '{}\\{}\\{}\\'.format(destination_data_indir, trial.split('\\')[-3], trial.split('\\')[-2])
                try:
                    os.makedirs(path_files)
                except FileExistsError:
                    pass
                new_name_traitement = '_'.join(traitement_path[0].split('\\')[-1].split('_')[-3:])
                new_name_frmaes = '_'.join(frames_path[0].split('\\')[-1].split('_')[-3:])
                copyfile(traitement_path[0], '{}\\{}'.format(path_files, new_name_traitement))
                copyfile(frames_path[0], '{}\\{}'.format(path_files, new_name_frmaes))


if __name__ == '__main__':
    cut = DataCut()
    # cut.data_cut('C:\\Users\\mekhezzr\\Desktop\\data_Lts\\')
    cut.copy_files(data_indir='C:\\Users\\mekhezzr\\Desktop\\data_Lts\\',
                   destination_data_indir='C:\\Users\\mekhezzr\\Desktop\\data_cleaned\\')
