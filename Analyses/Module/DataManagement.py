# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 11:27:50 2019

@author: 1mduquesnoy
"""

import plotly.graph_objs as go
import plotly
from plotly.offline import init_notebook_mode
import numpy as np 
import pandas as pd # librairie de gestion de bases de données comme des dataframes 
import matplotlib.pyplot as plt 
from math import pi
import os
import re
import glob
from sklearn.preprocessing import MinMaxScaler

class DataManagement:
    
    def get_files_by_num(self, pilot_indir, position_file):
        """
            Get the file at this position from each trial of this pilot.
    
                :param pilot_indir: Path to pilot data.
                :param position_file:Position of file in trial.
                :return: Array of the specified file from all the pilote's trials.
        """
    
        directory_files = glob.glob(pilot_indir + '\\*\\')
        os.chdir(pilot_indir)
        files = []
    
        for directoryFile in directory_files:
            fileList = glob.glob((directoryFile.split('\\')[-2] + '\\*.csv'))
            files.append(pilot_indir + fileList[position_file])
    
        os.chdir('..\\..')
        return files
    
    def get_all_files_by_num(self, data_indir, position_file):
        """
            Get all files at this position from each trial.
    
                :param data_indir: Path to data.
                :param position_file: Position of file in trial.
                :return: Array of arrays of all specified file of all pilotes

        """
        directory_files = glob.glob('{}\\*\\'.format(data_indir))
        allfiles = []
        for file in directory_files:
            l = DataManagement.get_files_by_num(self,file, position_file)
            allfiles.append(l)
        return allfiles
    
    def Base_de_donnees_Perf(self,data):
        """
            Create a dataset with all the frames concatenated. It is usefull when you want to make factorial analysis,
            more preciasly to compare/represent pilots (or trials) each others.
        """
    
        Data = pd.DataFrame(columns=['BraquetRider','longueurManivelle','DistanceRecul',
                                     'DAlignementMin','DEpauleMin','DistanceDmin','EngagementDmin',
                                     'HauteurFWRecul','Intention','HauteurFWDmin','ThetaManivelleDepart','ThetaManivelleRecul',
                                     'RateForceDeveloppement','ForceUPiedAvMax','ForceUPiedArMax',
                                     'MoyennePuissanceButteTotale','MoyennePuissancePremCassure',
                                     'PuissanceMaxPremCassure','TpsReaction','TpsPassageGrille','TpsPremCassure',
                                     'TpsBasDeButte','TimeToPeak','VitesseBasDeButte','VMaxPremCassure','ImpulsionParCoups',"TravailParCoups",'ImpulsionParCoups_1',"TravailParCoups_1",
                                     'ImpulsionParCoups_2',"TravailParCoups_2",'ImpulsionParCoups_3',"TravailParCoups_3",
                                     'ImpulsionParCoups_4',"TravailParCoups_4","Prenom","Nom","Numero","Date","Time2Peak","Manivelle",
                                     "Theta Depart","Theta Recul","Braquet","Temps Reaction","Recul","Explosivite","Label"])
    
        
        fls = DataManagement.get_all_files_by_num(self,data, position_file=0)
        fls_total = []
        for i in range(len(fls)):
            for j in range(len(fls[i])):
                fls_total.append(fls[i][j])
    
        for element in fls_total:
            
            elementbis = element.split("\\")[7]

            date = elementbis.split("_")[2]
            r=re.findall('[A-Z0-9][^A-Z0-9]*',elementbis)
    
            X = pd.read_csv(element,sep=",",encoding='Latin')
            X = X[['BraquetRider','longueurManivelle','Bip','DistanceRecul',
                                     'DAlignementMin','DEpauleMin','DistanceDmin','EngagementDmin',
                                     'HauteurFWRecul','Intention','HauteurFWDmin','ThetaManivelleDepart','ThetaManivelleRecul',
                                     'RateForceDeveloppement','ForceUPiedAvMax','ForceUPiedArMax',
                                     'MoyennePuissanceButteTotale','MoyennePuissancePremCassure',
                                     'PuissanceMaxPremCassure','TpsReaction','TpsPassageGrille','TpsPremCassure',
                                     'TpsBasDeButte','TimeToPeak','VitesseBasDeButte','VMaxPremCassure','ImpulsionParCoups',"TravailParCoups"]]
            
            for i in range(4):
                X["ImpulsionParCoups_" + str(i+1)] = X["ImpulsionParCoups"].iloc[i]
                X["TravailParCoups_" + str(i+1)] = X["TravailParCoups"].iloc[i]
            X = X[0:1]
            X["Prenom"] = r[0]
            X["Nom"] = r[1]
            X["Numero"] = r[2][0]
            X["Date"] = date[0:10]
            X["Time2Peak"] = X["TimeToPeak"]
            X["Manivelle"] = X["longueurManivelle"]
            X["Theta Depart"] = X["ThetaManivelleDepart"]
            X["Theta Recul"] = X["ThetaManivelleRecul"]
            X["Braquet"] = float(list(X["BraquetRider"])[0].split("x")[0]) / float(list(X["BraquetRider"])[0].split("x")[1])
            X["Temps Reaction"] = ( list(X["TpsReaction"])[0] - list(X["Bip"])[0] ) / 300
            X["Recul"] = X["DistanceRecul"]
            X["Explosivite"] = X["RateForceDeveloppement"]
            X["Label"] = r[1] + "_" + date[0:10]
            
            X = X.drop(["Bip"],axis=1)
            Data.loc[len(Data)] = list(X.loc[0])
        
                
        return(Data)
        
    def Creation_Traitements_Dataset(self,data):
        """
        
        """
        
        lst = DataManagement.get_all_files_by_num(self, data, 1)
        lst_total = []
        for i in range(len(lst)):
            for j in range(len(lst[i])):
                lst_total.append(lst[i][j])
   
        for element in range(len(lst_total)):
            X = pd.read_csv(lst_total[element],sep=",",encoding='Latin')
            X.to_csv('Analyses/Données/Traitements/' + lst_total[element].split("\\")[7],sep=",",header=True,index=False)
            
        return("Done")
        
    def Data_Two_Pilots(self,Variable,Pilot1,Pilot2,Date1,Date2):
        """
            Create the 2 array of data for both groups (for 1 variable).
                :param Variable   : a string with the name of the variable 
                :param Pilot1     : a string with the surname of the first pilot
                :param Pilot2     : a string with the surname of the second pilot
                :param Date1      : a string with the date for the Pilot1's trials
                :param Date2      : a string with the date for the Pilot2's trials
        """
    
        N1 = []
        N2 = []
        
        YA = []
        YB = []
        
        
        for element in os.listdir('Données\\Traitements\\'):
            
            date = element.split("_")[2]
            r=re.findall('[A-Z0-9][^A-Z0-9]*',element)
            
            if (r[1] == Pilot1):
                Data = pd.read_csv('Données\\Traitements\\'+element,sep=",",encoding='Latin',engine='python')[Variable]
                N1.append(len(Data))
            elif (r[1] == Pilot2):
                Data = pd.read_csv('Données\\Traitements\\'+element,sep=",",encoding='Latin',engine='python')[Variable]
                N2.append(len(Data))
        N=min(min(N1),min(N2))
        
        for element in os.listdir('Données\\Traitements\\'):
            
            date = element.split("_")[2]
            r=re.findall('[A-Z0-9][^A-Z0-9]*',element)
            
            if (r[1] == Pilot1):
                Data = pd.read_csv('Données\\Traitements\\'+element,sep=",",encoding='Latin',engine='python')[Variable]
                YA.append(Data[0:N])
            elif (r[1] == Pilot2):
                Data = pd.read_csv('Données\\Traitements\\'+element,sep=",",encoding='Latin',engine='python')[Variable]
                YB.append(Data[0:N])
        return(np.array(YA),np.array(YB))
        
        
    def Data_New_Predictions(self,Data,Labels):
        """
        Create a Dataset availible for the prediction programme 'Lexture_XTest'
            :param Data   :  the dataset from frames
            :param Labels :  a list with the labels of the pilots + date. Ex = ["Pilard_2012-12-13", ...]

        """
        
        Alpha = Data[["Temps Reaction","Explosivite","Time2Peak","Intention","Braquet","Manivelle","Recul","Theta Depart","Theta Recul","Label","Numero"]]
        Beta = pd.DataFrame(columns=[["Temps Reaction","Explosivite","Time2Peak","Intention","Braquet",
                       "Manivelle","Recul","Theta Depart","Theta Recul","Label","Numero"]])
        
        N = []
        M = []
        for i in range(len(Labels)):
            Help = Alpha[Alpha.Label == Labels[i]]
            

            for j in range(len(Help)):
                Beta.loc[len(Beta)] = list(Help.iloc[j,:])
                N.append(list(Help["Numero"])[j])
                M.append(list(Help["Label"])[j])


        Beta["ID"] = [i+'_'+j for i,j in zip(M,N)]
        Beta.index = np.array(Beta["ID"])
        Beta = Beta[["Temps Reaction","Explosivite","Time2Peak","Intention","Braquet","Manivelle","Recul","Theta Depart","Theta Recul"]] 
        return(Beta,Beta.index)

if __name__ == '__main__':
    
    os.chdir('C:\\Users\\1mduquesnoy\\Desktop\\Analyses\\') 
    data = 'C:\\Users\\1mduquesnoy\\Desktop\\data_v2'
    
    d = DataManagement()
    Data = d.Base_de_donnees_Perf(data)

    os.chdir('C:\\Users\\1mduquesnoy\\Desktop\\Analyses\\')
    YA,YB = d.Data_Two_Pilots("ForcePied","Mayet","Racine","2018-06-19","2018-06-22")

    #print(d.Data_New_Predictions(Data,["Mayet_2018-06-19","Racine_2018-06-22"]))

    