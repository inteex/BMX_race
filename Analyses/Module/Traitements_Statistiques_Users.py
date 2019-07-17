# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 14:31:22 2019

@author: 1mduquesnoy
"""

from Analyse.Module.DataViz import *
from Analyse.Module.DataCreationTestR import *
from Analyse.Module.Predictions import *

if __name__ == '__main__':
    print("Bienvenu sur votre espace d'analyses statistiques")

    #### Etapes fondamentales avant utilisations

    '''
    Merci de donner le chemin de 'path', contenant l'ensemble des essais traités sous Matlab, sous forme de CSV
    Merci de modifier le répertoire courant d'utilisation afin de vous placer dans le dossier 'analyses'
    
    -Creation_Traitements_Dataset(path) va permettre d'alimenter la base de données des fichiers Traitements.
        Lors de votre première utilisation la ligne de code doit être exectuée, puis vous devez la mettre en 
        commentaire pour le reste de votre utilisation.
    -Base_de_donnees_Perf(path) va automatiquement effectuer la concaténation des fichiers frames pour l'utilisation
        des fonctions des modules DataViz et Predictions.
    -La 3ème est dernière ligne permet d'exporter cette concaténation dans le dossier Données/Frames.
    
    Choisissez votre analyse en décommentant l'example associé   
    
    Si des erreurs apparaissent dans les codes, soit :
        - vos chemins d'accès sont incorrects
        - les essais d'un pilote à une date, et pour un numéro d'essai sont faux
        
    L'utilisateur doit être en connaissance des noms des variables des fichiers Frames et Traitements
    '''

    os.chdir('C:\\Users\\1mduquesnoy\\Downloads\\BMX_race\\Analyses')
    d = DataManagement()
    v = DataViz()
    r = DataCreationTestR()
    p = Predictions()

    path = 'C:\\Users\\1mduquesnoy\\Desktop\\data_v2'

    d.Creation_Traitements_Dataset(path)
    Data = d.Base_de_donnees_Perf(path)
    Data.to_csv('C:\\Users\\1mduquesnoy\\Downloads\\BMX_race\\Analyses\\Données\\Frames\\Base_Frames.csv',sep=";",header=True)
    os.chdir('C:\\Users\\1mduquesnoy\\Downloads\\BMX_race\\Analyses')

    ########### Diagramme de Kiviat

    #v.Kiviat(Data,"Valentino","Valentino",6,3,"2018-12-14","2018-12-14")

    ########### Comparaison des pilotes pour une variables

    #v.Comparaison_Boxplot(path,"ThetaManivelleDepart")

    ########### Comparaison en temps, des essais de 2 pilotes, pour une variables temporelle (SPM)

    #YA, YB = d.Data_Two_Pilots("IndiceEfficacitePiedAv","Rencurel","Valentino","2018-12-12","2018-12-14")
    #v.SPM_Comparaison(len(YA),len(YB),0.05,YA,YB,"Rencurel","Valentino","Efficacité","independant")

    ########### Boxplot pour comparer les meilleurs essais d'un pilote, versus ses moins bons

    #v.Comparaison_Trials_Pilot(Data,"Valentino","2018-12-14")
    
    ########### Correlation Canonique pour déterminer les zones de corrélations
    
    #v.Correlation_Canonique(Data,"TpsBasDeButte","Puissance")
    
    ########### Predictions sur la base de l'explosivité avec des paramètres au "pre-depart".
    

    #XTest = d.Data_New_Predictions(Data,["Valentino_2018-12-14"])
    #Out = p.Predictions_Puissance_Explosivite(XTest[0])
    #p.Lecture_XTest(Out,XTest[1],"Resultats_Valentino.csv")

    ########## Création des bases de Test pour le programme sous R, concernant la prédiction de la classe de Puissance

    #r.Creation_Test_Power(path,["Valentino_2018-12-14"],"Base_Valentino_P.csv")
    #☺r.Creation_Test_Feature(path, ["Valentino_2018-12-14","Ragot_2018-12-11","Racine_2018-06-22","Pilard_2018-06-21"], "IndiceEfficaciteTotal", "Donnees.csv")
