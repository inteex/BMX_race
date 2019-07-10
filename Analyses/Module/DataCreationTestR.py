# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 11:22:04 2019

@author: 1mduquesnoy
"""

from Analyses.Module.DataManagement import *


class DataCreationTestR:

    def Creation_Test_Feature(self, Path, Labels, Variable, Name):
        '''
        Create of a dataset with functional power features, necessary for R programmation.
            :param Path   : a sting with the path of the data containig all the CSV files.
            :param Labels : a list with the labels of the pilots + date. Ex = ["Pilard_2012-12-13", ...]
            :param Name   : the name of the files exported in output. Ex "Name.csv"
        
        '''

        Output = []

        fls = DataManagement.get_all_files_by_num(self, Path, position_file=1)
        fls_total = []
        for i in range(len(fls)):
            for j in range(len(fls[i])):
                fls_total.append(fls[i][j])

        fls_sortie = []

        for element in fls_total:

            elementbis = element.split("\\")[-1]

            date = elementbis.split("_")[-1]

            r = re.findall('[A-Z0-9][^A-Z0-9]*', elementbis)

            if (r[1] + "_" + date[0:10] in Labels):
                fls_sortie.append(elementbis)

        N = []
        ID = []
        for element in fls_sortie:
            current_directory = os.path.dirname(os.path.realpath(__file__))
            parent_directory = '\\'.join(current_directory.split('\\')[:-1])
            X = pd.read_csv(parent_directory + '\\Données\\Traitements\\' + element, sep=",", encoding='Latin', engine='python')[Variable]
            N.append(len(X))

        N = min(N)

        for element in fls_sortie:
            current_directory = os.path.dirname(os.path.realpath(__file__))
            parent_directory = '\\'.join(current_directory.split('\\')[:-1])
            X = pd.read_csv(parent_directory + '\\Données\\Traitements\\' + element, sep=",", encoding='Latin',
                            engine='python')[Variable]
            ID.append(element.split('_')[1] + "_" + element.split('_')[2])
            Output.append(list(X)[0:N])

        Output = pd.DataFrame(Output)
        Output.index = ID
        Output.to_csv(parent_directory + '\\R\\Nouveaute\\' + Name, sep=",", header=True, index=True)

        return ("Done")

    def Creation_Test_Power(self, Path, Labels, Name):
        '''
        
        
        '''

        Output = []

        fls = DataManagement.get_all_files_by_num(self, Path, position_file=1)
        fls_total = []
        for i in range(len(fls)):
            for j in range(len(fls[i])):
                fls_total.append(fls[i][j])

        fls_sortie = []

        for element in fls_total:

            elementbis = element.split("\\")[-1]

            date = elementbis.split("_")[-1]

            r = re.findall('[A-Z0-9][^A-Z0-9]*', elementbis)

            if (r[1] + "_" + date[0:10] in Labels):
                fls_sortie.append(elementbis)

        N = 480
        ID = []

        for element in fls_sortie:
            current_directory = os.path.dirname(os.path.realpath(__file__))
            parent_directory = '\\'.join(current_directory.split('\\')[:-1])
            X = pd.read_csv(parent_directory + '\\Données\\Traitements\\' + element, sep=",", encoding='Latin', engine='python')["Puissance"]
            if (len(X) >= N):
                ID.append(element.split('_')[1] + "_" + element.split('_')[2])
                Output.append(list(X)[0:N])
            else:
                print("Due to a short number of values, you can't analyse this trial")

        Output = pd.DataFrame(Output)
        Output.index = ID
        Output.to_csv(parent_directory + '\\R\\Nouveaute\\' + Name, sep=",", header=True, index=True)

        return ("Done")


if __name__ == '__main__':
    os.chdir('C:\\Users\\1mduquesnoy\\Desktop\\Analyses\\')
    path = 'C:\\Users\\1mduquesnoy\\Desktop\\data_v2'

    d = DataManagement()
    r = DataCreationTestR()

    os.chdir('C:\\Users\\1mduquesnoy\\Desktop\\Analyses\\')
    # print(r.Creation_Test_Power(path,["Jouve_2018-06-20"],"Test_Jouve.csv"))
    print(r.Creation_Test_Feature(path, ["Jouve_2018-06-20", "Mahieu_2018-12-13"], "ForcePied", "Test_Clustering.csv"))
