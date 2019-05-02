import os
import glob
import pandas as pd


class NavigateFiles:

    def get_best_trial(self, pilote_indir):
        """

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
                finDep = frames.FinDplcmt[0] - frames.Bip[0]
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

        :param data_indir: Path to data.
        :return: List of paths of best trial for each pilot.
        """
        directoryFiles = glob.glob(data_indir + '\\*\\')
        bestTrials = []
        for file in directoryFiles:
            l = self.get_best_trial(file)
            bestTrials.append(l)
        return bestTrials

    def get_files_by_num(self, indir, fileNum):
        """Get a the specified file from each trial.

        Parameters
        ----------
            indir : string,
                Path to data.

            fileNum : int,
                Position of file in trial.

        Returns
        -------
            files : array,
                Array of the specified file from all the pilote's trials.

        """
        directory_files = glob.glob(indir + '\\*\\')
        os.chdir(indir)
        files = []

        for directoryFile in directory_files:
            fileList = glob.glob((directoryFile.split('\\')[-2] + '\\*.csv'))
            files.append(indir + fileList[fileNum])

        os.chdir('..\\..')
        return files

    def get_all_files_by_num(self, indir, fileNum):
        """Get all the specified file from each trial of each pilote.

        Parameters
        ----------
        indir : string,
            Path to data.
        fileNum : int,
            Position of file in trial.
        Returns
        -------
            files : array,
                Array of arrays of all specified file of all pilotes

        Example
        -------
        it returns this type of structure:
            [
            ['./data/AP/trial2/framesArthurPilard2.csv', ... ],
            [... ,'./data/TJ/trial7/framesThomasJouve7.csv']
            ]

        """
        current_path = os.path.dirname(os.path.realpath(__file__))
        directory_files = glob.glob('{}\\*\\'.format(indir))
        allfiles = []
        for file in directory_files:
            l = self.get_files_by_num(file, fileNum)
            allfiles.append(l)
        return allfiles

    def get_files_by_pilote_name_trial_num(self, data_indir, pilote_name, trial_num):

        directory_files = glob.glob(data_indir + '\\*')
        current_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(data_indir)
        files = []
        for directoryFile in directory_files:
            l = glob.glob(('{}\\trial{}\\*_{}*_*.csv'.format(directoryFile, trial_num, pilote_name)))
            if l:
                files.append(l)
        os.chdir(current_path)
        return files[0]

    def get_files_by_pilotes_names_trials_nums(self, data_indir, pilote_names, trial_nums):

        current_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(data_indir)
        files = []
        for pilote_name,trial_num in zip(pilote_names,trial_nums):
            files.append(self.get_files_by_pilote_name_trial_num(data_indir, pilote_name, trial_num))
        os.chdir(current_path)
        return files


if __name__ == '__main__':
    nf = NavigateFiles()
    # print(nf.get_all_files_by_num('C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\data_v2', fileNum=0))
    print(
        nf.get_files_by_pilotes_names_trials_nums(data_indir='C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\data_v2',
                                                  pilote_names=['ArthurPilard', 'JeremyRencurel','SylvainAndre'], trial_nums=[2, 1, 5]))
    # print(nf.get_all_best_trials('.\\data'))
