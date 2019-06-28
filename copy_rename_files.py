import os
import shutil
import glob

class CopyRenameFiles:
    def dataCute(self,indir, dir_to_savefile):
            os.chdir(indir)
            directoryFiles = glob.glob('*.csv')
            trial = indir.split('\\')[-2]
            trialnumber = trial[-1]
            surname = indir.split('\\')[-3]
            filename = '{}\\{}'.format(indir,directoryFiles[0])
            new_name = '{}\\{}\\trial{}\\'.format(dir_to_savefile, surname, trialnumber)
            frame_complete_path = glob.glob(new_name+'\\*.csv')
            frame_complete_name = frame_complete_path[0].split('\\')[-1]
            date = frame_complete_name.split('_')[-1].split('.')[-2]
            pilot_name = frame_complete_name.split('_')[-2]
            if not os.path.exists('{}\\traitement_{}_{}.csv'.format(new_name,pilot_name,date)):
                shutil.copy(filename, '{}\\traitement_{}_{}.csv'.format(new_name, pilot_name, date))

if __name__ == '__main__' :
    directoryFiles = glob.glob("C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\data\\*\\*\\")
    dir_to_savefile = 'C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\data_v2_old'
    cpf = CopyRenameFiles()

    for directoryFile in directoryFiles:
        cpf.dataCute(directoryFile,dir_to_savefile)



