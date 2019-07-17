# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 11:45:14 2019

@author: 1mduquesnoy
"""

import matplotlib.pyplot as plt
from math import pi
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import os

from Analyse.Module.DataManagement import *
import spm1d
import random
from collections import Counter


class DataViz:

    def Kiviat(self, Data, Pilot1, Pilot2, Num1, Num2, Date1, Date2):
        """
            Plot the Radarchart graph to compare values of 2 trials. Use Only the dataset 'Donnees.csv'
            For each variable, the valuer per pilot is scaled is scaled between 0 and 1, with 0 the smallest
            value and 1 the biggest.
                :param Data    : dataset, with the labels
                :param Pilot1  : a string with a trial from a pilot
                :param Pilot2  : another string from the same pilot, or not
                :param Num1    : the number of the trial from Pilot1
                :param Num2    : the number of the trial from Pilot2
                :param Date1   : the (string) date of the trial from Pilot1
                :param Date2   : the (string) date of the trial from Pilot2
        """

        data = Data

        data = data[
            ["Prenom", "Nom", "Numero", "Date", "TimeToPeak", "TpsBasDeButte", "VitesseBasDeButte", "DistanceRecul",
             "MoyennePuissancePremCassure"]]

        infos = data[["Prenom", "Nom", "Numero", "Date"]]
        data = data.drop(["Prenom", "Nom", "Numero", "Date"], axis=1)
        columns = data.columns
        minmax_scale = MinMaxScaler().fit(data)
        data = pd.DataFrame(minmax_scale.transform(data), columns=columns)
        data = pd.concat([data, infos], axis=1)

        p1 = data[data.Nom == Pilot1]
        p1 = p1[p1.Numero == str(Num1)]
        p1 = p1[p1.Date == Date1]
        p2 = data[data.Nom == Pilot2]
        p2 = p2[p2.Numero == str(Num2)]
        p2 = p2[p2.Date == Date2]

        data = pd.concat([p1, p2], axis=0)
        data = data.drop(["Prenom", "Nom", "Numero", "Date"], axis=1)

        categories = ["TimeToPeak", "TpsBasDeButte", "VitesseBasDeButte", "DistanceRecul",
                      "MoyennePuissancePremCassure"]
        N = len(categories)

        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        ax = plt.subplot(111, polar=True)

        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)

        plt.xticks(angles[:-1], categories)

        ax.set_rlabel_position(0)

        plt.yticks([0, 0.5, 1], ["0", "0.5", "1"], color="grey", size=7)
        plt.ylim(0, 1)
        values = data.iloc[0].values.tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=Pilot1 + " " + str(Num1) + " " + Date1)
        ax.fill(angles, values, 'b', alpha=0.1)

        values2 = data.iloc[1].values.tolist()

        values2 += values2[:1]

        ax.plot(angles, values2, linewidth=1, linestyle='solid', label=Pilot2 + " " + str(Num2) + " " + Date2)
        ax.fill(angles, values2, 'r', alpha=0.1)
        plt.legend(loc='upper right', bbox_to_anchor=(0, 0))
        plt.show()

    def Comparaison_Boxplot(self, path, Variable):
        """
            Make a boxplot view to compare pilots about 1 variable.
                :param : a string with the name of the variable
                
        """

        Boxplot = []
        Variation = []

        Data = DataManagement.Base_de_donnees_Perf(self, path)
        Data = Data[Data.PuissanceMaxPremCassure < 5000]
        N = len(Counter(list(Data["Label"])))
        lst = list(Counter(list(Data["Label"])))

        for i in range(N):
            p = Data[Data.Label == lst[i]]
            Boxplot.append(np.mean(p[Variable]))
            Variation.append(np.sqrt(np.var(p[Variable])))

        Z = pd.concat([pd.DataFrame(lst, columns=["lst"]), pd.DataFrame(Boxplot, columns=["Boxplot"]),
                       pd.DataFrame(Variation, columns=["Variation"])], axis=1)
        Z = Z.sort_values(by='Boxplot')
        fig = plt.figure(figsize=(12, 8))

        plt.title("Comparaison pour la variable : " + Variable)
        plt.ylabel(Variable)
        plt.bar(range(N), Z["Boxplot"], width=0.6, color='grey',
                edgecolor='blue', linewidth=2, capsize=10,
                yerr=Z["Variation"], ecolor='black')
        plt.xticks(range(N), Z["lst"], rotation=45, fontsize="7")
        plt.show()

    def SPM_Comparaison(self, nb1, nb2, alpha, YA, YB, Pilot1, Pilot2, Variable, choice):
        """
        Make a SPM analysis in order to compare 2 pilots for 1 variable, with all there trials.
            :param nb1      : the trials number for the first pilot 
            :param nb2      : the trials number for the second pilot 
            :param alpha    : threshold of the t-test
            :param YA       : dataset for pilot1 (come from Data_Two_Pilots)
            :param YB       : dataset for pilot2 (come from Data_Two_Pilots)
            :param Pilot1   : a string with the surname of the first pilot
            :param Pilot2   : a string with the surname of the second pilot
            :param Variable : a string with the name of the variable
            :param choice   : a string with the possibility independant, or not of the sample
    
        """

        if (nb1 < nb2):
            liste = list(np.arange(0, nb1, 1))
            for i in range(nb2 - nb1):
                liste = liste + [random.randint(0, nb1 - 1)]
            YA = YA[liste, :]
        if (nb1 > nb2):
            liste = list(np.arange(0, nb2, 1))
            for i in range(nb1 - nb2):
                liste = liste + [random.randint(0, nb2 - 1)]
            YB = YB[liste, :]

        alpha = alpha
        if (choice == "independant"):
            t = spm1d.stats.ttest2(YA, YB)
        elif (choice == "apparie"):
            t = spm1d.stats.ttest_paired(YA, YB)
        ti = t.inference(alpha, two_tailed=True, interp=True)

        xx = []
        v = []
        L = np.floor(YA.shape[1])
        for i in range(6):
            v.append('x=' + str(round(np.float(i*L / 5) / 300, 2)))
            xx.append(np.float(i*L / 5))
 
        fig = plt.figure(figsize=(12, 8))

        axes = plt.gca()
        axes.xaxis.set_ticks(xx)
        axes.xaxis.set_ticklabels(v)
        spm1d.plot.plot_mean_sd(YA)
        spm1d.plot.plot_mean_sd(YB, linecolor='r', facecolor='r')
        plt.title('Comparaison des essais de ' + Pilot1 + " (noir)" + " et " + Pilot2 + " (rouge)")
        plt.axhline(y=0, color='k', linestyle=':')
        plt.xlabel('Time (s)')
        plt.ylabel(Variable)

        fig = plt.figure(figsize=(12, 8))

        ti.plot()
        ti.plot_threshold_label(fontsize=8)
        ti.plot_p_values(size=10, offsets=[(0, 0.3)])
        axes = plt.gca()
        axes.xaxis.set_ticks(xx)
        axes.xaxis.set_ticklabels(v)
        plt.xlabel('Time (s)')
        plt.show()

    def Comparaison_Trials_Pilot(self, Data, Name, Date):
        """
        Create a boxplot in order to compare, for 1 pilot, the 2 best trials versus the others.
            :param Data   : the dataset used
            :param Name   : a string with the name of the pilot
            :param Date   : a string with the date of the trials chosen
        """
        Alpha = Data[Data.Nom == Name]

        Alpha = Alpha[Alpha.Date == Date]
        Alpha = Alpha.sort_values(by='TpsBasDeButte')
        Alpha.index = list(np.arange(0, len(Alpha)))
        Beta = Alpha.drop(index=[0, 1])
        Alpha = Alpha.iloc[[0, 1], :]

        Pilot = pd.DataFrame(columns=Alpha.columns)
        Pilot.loc[len(Pilot)] = Alpha.iloc[0, :]
        Pilot.loc[len(Pilot)] = Beta.mean()
        Pilot.loc[len(Pilot)] = Alpha.iloc[1, :]
        Pilot.loc[len(Pilot)] = Beta.var()
        Pilot.index = ["Best 1", "Other in mean", "Best 2", "Other in var"]
        Pilot1 = Pilot[['DistanceRecul', 'DAlignementMin',
                        'DEpauleMin', 'DistanceDmin', 'EngagementDmin', 'HauteurFWRecul',
                        'HauteurFWDmin', 'Intention','ThetaManivelleDepart']]

        Pilot2 = Pilot[['RateForceDeveloppement', 'ForceUPiedAvMax', 'ForceUPiedArMax',
                        'MoyennePuissanceButteTotale', 'MoyennePuissancePremCassure',
                        'PuissanceMaxPremCassure', 'ImpulsionParCoups', 'TravailParCoups',
                        'ImpulsionParCoups_1', 'TravailParCoups_1', 'ImpulsionParCoups_2',
                        'TravailParCoups_2', 'ImpulsionParCoups_3', 'TravailParCoups_3',
                        'ImpulsionParCoups_4', 'TravailParCoups_4']]

        Pilot3 = Pilot[['TpsReaction', 'TpsPassageGrille',
                        'TpsPremCassure', 'TpsBasDeButte', 'TimeToPeak']]

        Pilot1 = Pilot1.dropna(axis=1)
        Pilot2 = Pilot2.dropna(axis=1)
        Pilot3 = Pilot3.dropna(axis=1)

        barWidth1 = 0.2
        barWidth2 = 0.4
        barWidth3 = 0.6
        r1 = range(Pilot1.shape[1])
        r2 = [x + barWidth1 for x in r1]
        r3 = [x + barWidth2 for x in r1]

        fig = plt.figure(figsize=(12, 8))
        plt.bar(r1, Pilot1.iloc[0, :], width=barWidth1, color=['orange' for i in Pilot1.iloc[0, :]],
                edgecolor=['orange' for i in Pilot1.iloc[0, :]], linewidth=2, label="Best 1")
        plt.bar(r2, Pilot1.iloc[2, :], width=barWidth1, color=['green' for i in Pilot1.iloc[2, :]],
                edgecolor=['green' for i in Pilot1.iloc[2, :]], linewidth=2, label="Best 2")
        plt.bar(r3, Pilot1.iloc[1, :], width=barWidth1, color=['grey' for i in Pilot1.iloc[1, :]],
                edgecolor=['grey' for i in Pilot1.iloc[0, :]], linewidth=2, label="Others in mean",
                yerr=np.sqrt(Pilot1.iloc[3, :]), ecolor='black', capsize=10)
        plt.title("Bests and other trials from " + Name)
        plt.legend()
        plt.xticks([r + barWidth1 / 2 for r in range(Pilot1.shape[1])], Pilot1.columns, rotation=20)
        
        
    def Correlation_Canonique(self,Data,Variable1,Variable2):
        '''
        Make a Canonical Correlation Analysis in order to show where the correlation between the two features
        appears
            :param Data : the dataset used
            :param Variable1 : a string with the name of the variable from the columns of Data (Frames's variable) 
            ;param Variable2 : a string with the name of the functional variable, where we will see the 
                                significant correlation durong time
        '''

        X = Data[[Variable1]]
        X = np.array(list(X[Variable1]))
        
        Y = []
        N = Y.copy()
        
        for element in os.listdir('Données\\Traitements\\'):
            
            Data = pd.read_csv('Données\\Traitements\\'+element,sep=",",encoding='Latin',engine='python')[Variable2]
            N.append(len(Data))
         

        N = min(N)

        for element in os.listdir('Données\\Traitements\\'):
            
            Data = pd.read_csv('Données\\Traitements\\'+element,sep=",",encoding='Latin',engine='python')[Variable2]
            Data = Data.fillna(method='pad')
            Y.append(np.array(Data[0:N]).reshape((N,1)))
            
        Y = np.array(Y)

        
        np.random.seed(0)
        alpha      = 0.05
        two_tailed = False
        snpm       = spm1d.stats.nonparam.cca(Y,X)
        snpmi      = snpm.inference(alpha, iterations=100)
        
        xx = []
        v = []
        L = np.floor(YA.shape[1])
        for i in range(6):
            v.append('x=' + str(round(np.float(i*L / 5) / 300, 2)))
            xx.append(np.float(i*L / 5))
            
        fig = plt.figure(figsize=(12, 8))
        
        snpmi.plot()
        snpmi.plot_p_values()
        axes = plt.gca()
        axes.xaxis.set_ticks(xx)
        axes.xaxis.set_ticklabels(v)
        plt.xlabel("Time (s)")
        plt.title("Influence de " + Variable2 + " sur " + Variable1)
        plt.show()
        
        return('Done')


if __name__ == '__main__':
    os.chdir('C:\\Users\\1mduquesnoy\\Desktop\\Analyses\\')

    v = DataViz()
    d = DataManagement()
    path = 'C:\\Users\\1mduquesnoy\\Desktop\\data_v2'

    #Data_Frames = d.Base_de_donnees_Perf(path)
    os.chdir('C:\\Users\\1mduquesnoy\\Desktop\\Analyses\\')
    
    #print(v.Comparaison_Boxplot(path,"DistanceDmin"))
    # print(v.Kiviat(Data_Frames,"Pilard","Mahieu",2,2,"2018-06-21","2018-12-13"))

    #YA, YB = d.Data_Two_Pilots("Puissance","Racine","Valentino","2018-06-22","2018-12-14")
    #print(v.SPM_Comparaison(len(YA),len(YB),0.05,YA,YB,"Pilard","Valentino","Puissance","independant"))

    #(v.Comparaison_Trials_Pilot(Data_Frames,"Jouve","2018-06-20se"))
    
    #YA = pd.read_csv("C:/Users/1mduquesnoy/Desktop/Stage/Base de Données/indiceEfficacite/Manon_3D.csv",sep=";",engine='python',encoding="Latin")
    #YB = pd.read_csv("C:/Users/1mduquesnoy/Desktop/Stage/Base de Données/indiceEfficacite/Manon_2D.csv",sep=";",engine='python',encoding="Latin")
    
    #v.SPM_Comparaison(len(YA),len(YB),0.05,np.array(YA),np.array(YB),"3D","2D","Efficacité","apparie")
    #YA, YB = d.Data_Two_Pilots("IndiceEfficacitePiedAv","Racine","Valentino","2018-06-22","2018-12-14")
    #v.SPM_Comparaison(len(YA),len(YB),0.05,YA,YB,"Racine","Valentino","Efficacité","independant")

    #YA = pd.read_csv("C:/Users/1mduquesnoy/Desktop/Stage/Base de Données/indiceEfficacite/Sylvain_3D.csv",sep=";",engine='python',encoding="Latin")
    #YB = pd.read_csv("C:/Users/1mduquesnoy/Desktop/Stage/Base de Données/indiceEfficacite/Sylvain_2D.csv",sep=";",engine='python',encoding="Latin")
    
    #v.SPM_Comparaison(len(YA),len(YB),0.05,np.array(YA),np.array(YB),"3D","2D","Efficacité","apparie")
    
    