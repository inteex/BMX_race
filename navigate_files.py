import os
import glob
import pandas as pd


class NavigateFiles:

    def get_best_trial(self, pilote_indir):
        """
            get the best trial for the specified pilot
                :param pilote_indir: Path to pilot directory.
                :return: Path to the best trial.
        """
        directoryFiles = glob.glob(pilote_indir + '\\*\\')
        current_directory = os.path.dirname(os.path.realpath(__file__))
        os.chdir('{}'.format(pilote_indir))
        TimeToTake = 2000

        for directoryFile in directoryFiles:
            fileList = glob.glob((directoryFile.split('\\')[-2] + '\\*.csv'))
            traitement = pd.read_csv(fileList[1])
            frames = pd.read_csv(fileList[0])

            if 'FinDplcmt' in frames.columns:
                """
                indeccies are shifted by 111 when time starts from 
                -0.36 instead of 0 so the index of finDep is shifted too.
                """
                finDep = frames.FinDplcmt[0] - frames.Bip[0] - 111
            else:
                finDep = len(traitement) - 1

            timeFinDep = traitement.Time[finDep - 1]
            vitess = traitement.VitesseRider[finDep - 1]
            # print(timeFinDep)
            # print(vitess)
            currentTime = timeFinDep
            if currentTime <= TimeToTake:
                TimeToTake = currentTime
                filetotake = pilote_indir + fileList[0].split('\\')[0]

        os.chdir(current_directory)
        return filetotake

    def get_all_best_trials(self, data_indir):
        """
            Get the best trial for every pilot in the data base.
                :param data_indir: Path to data.
                :return: List of paths of best trial for each pilot.
        """
        directoryFiles = glob.glob(data_indir + '\\*\\')
        bestTrials = []
        for file in directoryFiles:
            l = self.get_best_trial(file)
            bestTrials.append(l)
        return bestTrials

    def get_files_by_name(self, pilot_indir, file_name):
        """
            Get the file at this position from each trial of this pilot.

                :param pilot_indir: Path to pilot data.
                :param file_name:Prefix of file name .
                :return: Array of the specified file from all the pilote's trials.
        """

        directory_files = glob.glob(pilot_indir + '\\*\\')
        os.chdir(pilot_indir)
        files = []

        for directoryFile in directory_files:
            file = glob.glob(('{}\\{}*.csv'.format(directoryFile, file_name)))
            files.append(file[0])

        os.chdir('..\\..')
        return files

    def get_all_files_by_name(self, data_indir, file_name):
        """
            Get all files at this position from each trial.

                :param data_indir: Path to data.
                :param file_name: prefix of file name.
                :return: Array of arrays of all specified file of all pilotes

        """
        directory_files = glob.glob('{}\\*\\'.format(data_indir))
        allfiles = []
        for file in directory_files:
            l = self.get_files_by_name(file, file_name)
            allfiles.append(l)
        return allfiles

    def get_files_by_pilote_name_trial_num_date(self, data_indir, pilote_name, trial_num, date_trial):
        """

            :param data_indir:
            :param pilote_name:
            :param trial_num:
            :return:
        """
        directory_files = glob.glob(data_indir + '\\*')
        current_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(data_indir)
        files = []
        for directoryFile in directory_files:
            l = glob.glob(('{}\\trial{}\\*_{}*_{}.csv'.format(directoryFile, trial_num, pilote_name, date_trial)))
            if l:
                files.append(l)
        os.chdir(current_path)
        if files:
            return files[0]

    def get_files_by_pilotes_names_trials_nums_dates(self, data_indir, pilote_names, trial_nums, dates_trial):
        """

            :param data_indir:
            :param pilote_names:
            :param trial_nums:
            :return:
        """
        current_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(data_indir)
        files = []
        for pilote_name, trial_num, date_trial in zip(pilote_names, trial_nums, dates_trial):
            f = self.get_files_by_pilote_name_trial_num_date(data_indir, pilote_name, trial_num, date_trial)
            if f:
                files.append(f)
            else:
                print('no trial found')
        os.chdir(current_path)
        return files


if __name__ == '__main__':
    nf = NavigateFiles()
    data = 'C:\\Users\\1mduquesnoy\\Desktop\\data_v2'
    # print(
    #     nf.get_files_by_pilotes_names_trials_nums_dates(
    #         data_indir='C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\data_v2_old',
    #         pilote_names=['ArthurPilard', 'Jeremy'], trial_nums=[2, 5],
    #         dates_trial=['2018-06-21', '2018-12-12']))
    print(nf.get_all_files_by_name(data,'traitement'))
