import os
import shutil
import glob

class CopyRenameFiles:
    def copy_rename_files(self):
        movdir = r"C:\Scans"
        basedir = r"C:\Links"
        # Walk through all files in the directory that contains the files to copy
        for root, dirs, files in os.walk(movdir):
            for filename in files:
                # I use absolute path, case you want to move several dirs.
                old_name = os.path.join(os.path.abspath(root), filename)

                # Separate base from extension
                base, extension = os.path.splitext(filename)

                # Initial new name
                new_name = os.path.join(basedir, base, filename)

                # If folder basedir/base does not exist... You don't want to create it?
                if not os.path.exists(os.path.join(basedir, base)):
                    print
                    os.path.join(basedir, base), "not found"
                    continue  # Next filename
                elif not os.path.exists(new_name):  # folder exists, file does not
                    shutil.copy(old_name, new_name)
                else:  # folder exists, file exists as well
                    ii = 1
                    while True:
                        new_name = os.path.join(basedir, base, base + "_" + str(ii) + extension)
                        if os.path.exists(newname):
                            shutil.copy(old_name, new_name)
                            print
                            "Copied", old_name, "as", new_name
                            break
                        ii += 1

    def dataCute(self,indir,dir_to_savefile):
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
    dir_to_savefile = 'C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\data_v2'

    for directoryFile in directoryFiles:
        cpf = CopyRenameFiles()
        cpf.dataCute(directoryFile,dir_to_savefile)



