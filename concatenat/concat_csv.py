import os
import glob
import pandas as pd
from navigate_files import NavigateFiles


class ConcatCsv:
    def concat_to_frames_traitement_travail(self, data_indir, dir_to_savefile):
        """
        concatenat csv files that have same range of size onto 3 concatenated csv files
        frames,traitement and travail.

        <<1>>
            :param csv_files_indir: Path to csv files.
            :param dir_to_savefile: Path to save the new data base.

        """
        directoryFiles = glob.glob("{}\\*\\*\\".format(data_indir))
        for csv_files_indir in directoryFiles:

            os.chdir(csv_files_indir)
            fileList = glob.glob("*.csv")
            dfListframes = []
            dfListtrvail = []
            dfListtraitement = []
            colnamesframe = []
            colnamestravail = []
            colnamestraitement = []
            piloteName = csv_files_indir.split('\\')[-2]
            trialnumber = piloteName[-1]
            surname = csv_files_indir.split('\\')[-3]
            date_passage = 'yyyy-mm-dd'
            print("=" * 50)
            print("concat travail frames and traitement")
            print("=" * 50)
            for filename in fileList:
                size = os.stat(filename).st_size // 1024  # obtenir la taill en ko

                if size <= 5:
                    """
                     # size depend on files we want to groupe 
                     # < 5 because frame files are in this interval
                    """
                    try:
                        # read your files
                        df = pd.read_csv(filename, header=None)
                    except pd.errors.EmptyDataError:
                        pass
                    if filename == 'DatePassageRider.csv':
                        date_passage = df[0][0]
                        date_passage = date_passage.split('/')[::-1]  # reverse the table to get yyyy-mm-dd
                    for col in range(len(df.columns)):  # pour les fichier csv qui on plus d' une colonnes
                        colnamesframe.append(filename[:-4])  # affecter le meme nom de colonne pour tous les colonnes
                    dfListframes.append(df)  # ajouter le fichier de taille < 5 ko  dans la list dfListframes

                else:
                    if filename == 'ImpulsionPAr.csv' or filename == 'Impulsion.csv' or \
                            filename == 'ImpulsionPAv.csv' or filename == 'TravailPAv.csv' or \
                            filename == 'Travail.csv' or filename == 'TravailPAr.csv':
                        """
                         # size depend on files we want to groupe 
                         # 53 and 5, because travail files are in this interval
                        """

                        try:
                            # read your files
                            df = pd.read_csv(filename, header=None)
                        except pd.errors.EmptyDataError:
                            pass
                        for col in range(len(df.columns)):
                            colnamestravail.append(filename[:-4])
                        dfListtrvail.append(df)
                    else:
                        """
                             # size depend on files we want to groupe 
                             # > 5 because traitement files are in this interval
                        """
                        try:
                            # read your files
                            df = pd.read_csv(filename, header=None)
                        except pd.errors.EmptyDataError:
                            pass
                        for col in range(len(df.columns)):
                            colnamestraitement.append(filename[:-4])
                        dfListtraitement.append(df)

            path_files = '{}\\{}\\trial{}\\'.format(dir_to_savefile, surname, trialnumber)
            os.makedirs(path_files)
            if dfListframes:
                concatframes = pd.concat(dfListframes, axis=1)  # concatener les fichier qui figure dans dfListframes
                concatframes.columns = colnamesframe  # renommer toute les colonne par les nom obtenu en haut dans la var colnamesframe
                concatframes.to_csv('{}\\frames_{}_{}.csv'.format(path_files, piloteName, '-'.join(date_passage)),
                                    index=None)  # sauvgarder les fichier sous le nom de frames+nom du pilote+numero de test
            if dfListtrvail:
                concattravail = pd.concat(dfListtrvail, axis=1)
                concattravail.columns = colnamestravail
                concattravail.to_csv('{}\\travail_{}_{}.csv'.format(path_files, piloteName, '-'.join(date_passage)),
                                     index=None)
            if dfListtraitement:
                concattraitement = pd.concat(dfListtraitement, axis=1)
                concattraitement.columns = colnamestraitement
                concattraitement.to_csv(
                    '{}\\traitement_{}_{}.csv'.format(path_files, piloteName, '-'.join(date_passage)),
                    index=None)

    def concat_all_csv_in_one_file(self, csv_files_indir, name_output_file="concatenated.csv"):
        """
        Concatenat csv files onto 1 concatenated csv file

            :param csv_files_indir: Path to csv files.
            :param name_output_file: Name of the concatenated csv.
        """
        os.chdir(csv_files_indir)
        fileList = glob.glob("*.csv")
        colnamesframe = []
        dfListframes = []
        print(csv_files_indir.split('\\')[-1])
        for filename in fileList:
            df = pd.read_csv(filename, header=None)
            for col in range(len(df.columns)):
                colnamesframe.append(filename[:-4])
            dfListframes.append(df)
        concatframes = pd.concat(dfListframes, axis=1)
        concatframes.columns = colnamesframe
        concatframes.to_csv(name_output_file, index=None)

    def concat_all_traitement(self, data_indir, file_name='traitement'):
        """
        Concatenat all csv traitement files onto 1 concatenated csv file

            :param data_indir: Path to data file.
            :param file_name: Prefix of file name.
        """
        files = NavigateFiles().get_all_files_by_name(data_indir, file_name)
        appended_data = []
        for pilote in files:
            for file in pilote:  # the file in th trial
                traitemnt = pd.read_csv(file)
                appended_data.append(traitemnt)
        appended_data = pd.concat(appended_data, axis=0)
        current_directory = os.path.dirname(os.path.realpath(__file__))
        appended_data.to_csv("{}\\AlltraitementConcatenated.csv".format(current_directory), index=0)

    def concat_all_frames(self, data_indir, file_name):
        """
        Concatenat all csv frame files onto 1 concatenated csv file

            :param data_indir: Path to data.
            :param file_name: Prefix of file name.

        """

        frames = NavigateFiles().get_all_files_by_name(data_indir, file_name)
        appended_data = []
        for pilote in frames:
            for f in pilote:
                trials = "\\".join(f.split('\\')[0:-1])
                traitements = glob.glob((trials + '\\traitement_*.csv'))
                traits = pd.read_csv(traitements[0])
                time = traits['Time'][len(traits) - 2]
                frames = pd.read_csv(f)
                coups_de_pedal0 = frames["TpsReaction"][0] - frames["Bip"][0]
                coups_de_pedal1 = frames['CoupsDePedal'][0] - frames["Bip"][0]
                coups_de_pedal2 = frames['CoupsDePedal.1'][0] - frames["Bip"][0]
                coups_de_pedal3 = frames['CoupsDePedal.2'][0] - frames["Bip"][0]
                frame = frames[['TailleRider', 'longueurManivelle']]

                if 'Braquet' in frames.columns:
                    frame['Braquet'] = frames['Braquet']
                if 'MasseRider' in frames.columns:
                    frame['MasseRider'] = frames['MasseRider']
                if 'MasseBike' in frames.columns:
                    frame['MasseBike'] = frames['MasseBike']
                frame['TimeEnd'] = time
                partie_coups_de_pedal1 = traits[int(coups_de_pedal0):int(coups_de_pedal1)]
                frame['moyennePuissance1'] = partie_coups_de_pedal1['Puissance'].mean()

                partie_coups_de_pedal1 = traits[int(coups_de_pedal1):int(coups_de_pedal2)]
                frame['moyennePuissance2'] = partie_coups_de_pedal1['Puissance'].mean()

                partie_coups_de_pedal1 = traits[int(coups_de_pedal2):int(coups_de_pedal3)]
                frame['moyennePuissance3'] = partie_coups_de_pedal1['Puissance'].mean()

                partie_coups_de_pedal1 = traits[int(coups_de_pedal3):]
                frame['moyennePuissance4'] = partie_coups_de_pedal1['Puissance'].mean()

                frame['ThetaManivelleDepart'] = frames['ThetaManivelleDepart'][0]
                frame['DistanceRecul'] = frames['DistanceRecul'][0]
                frame['AlphaGaitDmin'] = frames['AlphaGaitDmin'][0]
                frame['TpsReaction'] = traits['Time'][int(frames['TpsReaction'][0]) - int(frames['Bip'][0])]
                frame['DEpauleMin'] = frames['DEpauleMin'][0]
                frame['DAlignementMin'] = frames['DAlignementMin'][0]
                frame['Dmin'] = traits['Time'][int(frames['Dmin'][0]) - int(frames['Bip'][0])]
                appended_data.append(frame.iloc[0:1])

        appended_data = pd.concat(appended_data, axis=0)
        current_directory = os.path.dirname(os.path.realpath(__file__))
        print(current_directory)
        appended_data.to_csv("{}\\AllframesConcatenated.csv".format(current_directory), index=0)

    def concat_traitement_travail(self, data_indir):
        """
         concatenat travail files and traitement onto 1 concatenated csv file in each trial
         and cute at the first null value of vitesseRider.

         <<3>>
            :param data_indir: Path to data pilote.
            :return: Csv file.
        """
        directory_files = glob.glob('{}\\*\\'.format(data_indir))
        print("=" * 50)
        print("concatenat traitement and travail")
        print("=" * 50)
        for pilote_indir in directory_files:
            print('concat ...{}'.format(pilote_indir))
            trials = glob.glob(pilote_indir + '\\*\\')
            os.chdir(pilote_indir)
            dfList = []
            for trial in trials:
                traitement_path = glob.glob(('{}\\cuted_fin_dep_traitement_*.csv'.format(trial.split('\\')[-2])))
                travail_path = glob.glob(('{}\\travail_*.csv'.format(trial.split('\\')[-2])))
                frames_path = glob.glob(('{}\\frames_*.csv'.format(trial.split('\\')[-2])))

                traitment = pd.read_csv(traitement_path[0])
                travail = pd.read_csv(travail_path[0])
                frames = pd.read_csv(frames_path[0])

                # concatenate traitement travail
                dfList.append(traitment)
                dfList.append(travail)
                concatDf = pd.concat(dfList, axis=1)

                try:
                    # index of first null vitess
                    finDep = int(concatDf.VitesseRider.index[concatDf.VitesseRider.isnull()][0])
                except IndexError:
                    finDep = len(concatDf)

                concatDf = concatDf.loc[0:finDep]
                concatDf = concatDf.reset_index(drop=True)

                outfile = '.\\{}\\concat_{}'.format(trial.split('\\')[-2], traitement_path[0].split('\\')[-1])
                concatDf.to_csv(outfile, index=None)
                dfList = []


if __name__ == '__main__':
    concat_csv = ConcatCsv()
    # concat_csv.concat_all_frames(data_indir="C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\data_v2",
    #                              file_name=0)

    # concat_csv.concat_to_frames_traitement_travail(data_indir='C:\\Users\\mekhezzr\\Desktop\\data_v2\\',dir_to_savefile="C:\\Users\\mekhezzr\\Desktop\\data_Lts\\")
    concat_csv.concat_all_traitement(data_indir='C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\data_v2\\')

    # concat_csv.concat_traitement_travail(data_indir='C:\\Users\\mekhezzr\\Desktop\\data_Lts\\')
