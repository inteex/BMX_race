import pandas as pd
import os
import glob


class NavigateFiles:

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
        directory_files = glob.glob(indir + '\\*\\')
        allfiles = []
        for file in directory_files:
            # if file.split('\\')[-2] != "AP":
            l = self.get_files_by_num(file, fileNum)
            allfiles.append(l)
        return allfiles


if __name__ == '__main__':
    nf = NavigateFiles()
    print(nf.get_all_files_by_num('.\\data\\', fileNum=2))
