# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 15:05:55 2019

@author: 1mduquesnoy
"""

from sklearn import tree
from sklearn.ensemble import GradientBoostingRegressor
from Analyses.Module.DataManagement import *

class Predictions:
    
    def Predictions_Puissance_Explosivite(self,XTest):
        """
        Create a predictions model from the 'Explosivite.csv' dataset, in order to give in output the potential
        power in the first stroke. Enter the new features for N new trials.
            :param XTest  : N*P dataframe with N the number of new trials, and P the number of features included
                            in the model : .
    
        """
        
        current_directory = os.path.dirname(os.path.realpath(__file__))
        parent_directory = '\\'.join(current_directory.split('\\')[:-1])

        XTrain = pd.read_csv(parent_directory + '\\Module\\XTrain_Puissance_Explosivite.csv',sep=";",encoding='Latin')
        YTrain_Puissance = pd.read_csv(parent_directory + '\\Module\\YTrain_Puissance_Explosivite_Puissance.csv',sep=";",encoding='Latin')
        YTrain_Y = pd.read_csv(parent_directory + '\\Module\\YTrain_Puissance_Explosivite_Y.csv',sep=";",encoding='Latin')
    
        XTrain = XTrain.set_index('ID')
        YTrain_Y = YTrain_Y.set_index('ID')
        YTrain_Puissance = YTrain_Puissance.set_index('ID')

        # Modele pour prédire la classe
        
        clf = tree.DecisionTreeClassifier(min_samples_leaf=10, min_samples_split=10)
        clf_fit_logit = clf.fit(XTrain,YTrain_Y)
        
        YPred_clf = clf_fit_logit.predict(XTest)
        
        # Modele pour prédire la puissance au 1er coups associé
        
        reg = GradientBoostingRegressor(criterion="friedman_mse",subsample=1.0,max_depth=8)
        rg_reg_gdr = reg.fit(XTrain,YTrain_Puissance)

        YPred_reg = rg_reg_gdr.predict(XTest)
        
        return(YPred_clf,YPred_reg)
    
    def Lecture_XTest(self,Sortie,Index,Nom):
        
        """
        Create a CSV from the results of the predictions.
            :param Sortie     : an array with the classes predicted, and the output  of power
            :param Index     :  an array with all the ID of the trials to be predict
            :param Nom        : a string with the new name of the result, included in the folder 'Sortie_Modeles'
        """
        
        Output = pd.concat([pd.DataFrame(Sortie[0],columns=["Classe"]),pd.DataFrame(Sortie[1],columns=["Puissance"])],axis=1)
        ID = []
        for i in range(len(Index)):
            ID.append(list(Index[i])[0])
 
        Output.index = ID
        current_directory = os.path.dirname(os.path.realpath(__file__))
        parent_directory = '\\'.join(current_directory.split('\\')[:-1])

        Output.to_csv(parent_directory +  '\\Sorties_Modeles\\' + Nom,sep=";",header=True)
        

        
if __name__ == '__main__':
    
    os.chdir('C:\\Users\\1mduquesnoy\\Desktop\\Analyses\\')  
    p = Predictions()
    d = DataManagement()
    #La partie suivante teste les nouvelles valeurs issues de XTest. 
    #Les YTest pour la pouissance et Y ne seont pas fournis lors des nouveaux essais.
    #YTest_Y = pd.read_csv('C:/Users/1mduquesnoy/Desktop/Stage/Python/Module/YTest_Puissance_Explosivite_Y.csv',sep=";",encoding='Latin')
    #YTest_Puissance = pd.read_csv('C:/Users/1mduquesnoy/Desktop/Stage/Python/Module/YTest_Puissance_Explosivite_Puissance.csv',sep=";",encoding='Latin')
    #XTest = pd.read_csv('C:/Users/1mduquesnoy/Desktop/Stage/Python/Module/XTest_Puissance_Explosivite.csv',sep=";",encoding='Latin')
    
    #p.Lecture_XTest("Nouveaute","XTest_Puissance_Explosivite","Tableaux")
    
    path = 'C:\\Users\\1mduquesnoy\\Desktop\\data_v2'
    #Data = d.Base_de_donnees_Perf(path)
    #os.chdir('C:\\Users\\1mduquesnoy\\Desktop\\Analyses\\')  
    XTest = d.Data_New_Predictions(Data,["Valentino_2018-12-14"])
    #print(XTest.shape)
    #XTest.to_csv('sgsg.csv')
    Out = p.Predictions_Puissance_Explosivite(XTest[0])

    p.Lecture_XTest(Out,XTest[1],"Résultats_Valentino.csv")
    
    
    