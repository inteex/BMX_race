import os
import glob
import pandas as pd
from navigate_to_trials import NavigateFiles


class ConcatCsv:
    def concat_to_frames_traitement_travail(self, csv_files_indir,
                                            dir_to_savefile='C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\data'):
        """
        concatenat csv files that have same range of size onto 3 concatenated csv files
        frames,traitement and travail.

            :param csv_files_indir: Path to csv files.
            :param dir_to_savefile: Path to save the new data base.

        """
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

            if (size <= 53) & (size > 5):
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

            if size > 53:
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
            concattraitement.to_csv('{}\\traitement_{}_{}.csv'.format(path_files, piloteName, '-'.join(date_passage)),
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

    def concat_all_traitement(self, data_indir, position_traitement=1):
        """
        Concatenat all csv traitement files onto 1 concatenated csv file

            :param data_indir: Path to data file.
            :param position_traitement: Position of the file taitement in a trial by default 1.
        """
        files = NavigateFiles().get_all_files_by_num(data_indir, position_traitement)
        appended_data = []
        for pilote in files:
            for file in pilote:  # the file in th trial
                traitemnt = pd.read_csv(file)
                appended_data.append(traitemnt)
        appended_data = pd.concat(appended_data, axis=0)
        current_directory = os.path.dirname(os.path.realpath(__file__))
        appended_data.to_csv("{}\\AlltraitementConcatenated.csv".format(current_directory), index=0)

    def concat_all_frames(self, data_indir, position_frames=0):
        """
        Concatenat all csv frame files onto 1 concatenated csv file

            :param data_indir: Path to data.
            :param position_frames: Position of the file frames in a trial by default 0.

        """

        frames = NavigateFiles().get_all_files_by_num(data_indir, position_frames)
        appended_data = []
        for pilote in frames:
            for f in pilote:
                trials = "\\".join(f.split('\\')[0:-1])
                traitements = glob.glob((trials + '\\traitement_*.csv'))
                traits = pd.read_csv(traitements[0])
                time = traits['Time'][len(traits) - 2]
                frames = pd.read_csv(f)
                frame = frames[['TailleRider', 'longueurManivelle']]
                if 'Braquet' in frames.columns:
                    frame['Braquet'] = frames['Braquet']
                if 'MasseRider' in frames.columns:
                    frame['MasseRider'] = frames['MasseRider']
                if 'MasseBike' in frames.columns:
                    frame['MasseBike'] = frames['MasseBike']
                frame['TimeEnd'] = time
                appended_data.append(frame.iloc[0:1])

        appended_data = pd.concat(appended_data, axis=0)
        current_directory = os.path.dirname(os.path.realpath(__file__))
        print(current_directory)
        appended_data.to_csv("{}\\AllframesConcatenated.csv".format(current_directory), index=0)

    def concat_traitement_travail(self, pilote_indir, position_travail, position_traitement):
        """
         concatenat travaill files and traitement onto 1 concatenated csv file in each trial

            :param pilote_indir: Path to data pilote.
            :param position_travail: Position of the file traivail in a trial.
            :param position_traitement: Position of the file traivail in a trial.
            :return:Csv file.
        """
        # To Do ...
        # trials = glob.glob(pilote_indir + '\\*\\')
        # os.chdir(pilote_indir)
        # dfList = []
        #
        # for trial in trials:
        #     fileList = glob.glob((trial.split('\\')[-2] + '\\*.csv'))
        #     if fileList:
        #         traitment = pd.read_csv(fileList[position_traitement])
        #         travail = pd.read_csv(fileList[position_travail])
        #         dfList.append(traitment)
        #         dfList.append(travail)
        #         outfile = trial.split('\\')[-2] + '\\Concatenated' + fileList[2].split('\\')[1]
        #         concatDf = pd.concat(dfList, axis=1)
        #         concatDf.to_csv(outfile, index=None)
        #         dfList = []


if __name__ == '__main__':
    concat_csv = ConcatCsv()
    # concat_csv.concat_all_frames(data_indir="C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\data_v2",position_frames=0)
    # directoryFiles = glob.glob("C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\data_v2\\TJ\\*\\")
    # for directoryFile in directoryFiles:
    #     concat_csv.concat_to_frames_traitement_travail(csv_files_indir=directoryFile,
    #                                                    dir_to_savefile="C:\\Users\\mekhezzr\\Desktop\\e")
    concat_csv.concat_all_traitement(data_indir='C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\data_v2\\',
                                     position_traitement=1)
