import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression, Ridge, ElasticNet, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import math
import pickle
from navigate_files import NavigateFiles
from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures
import glob
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt

from sklearn.feature_selection import f_regression, mutual_info_regression
from scipy import stats


pd.set_option('max_rows', 50)
pd.set_option('max_columns', 50)


class AnalyseTraitement:
    def preprocessing_data(self, indir='C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\concatenat\\AlltraitementConcatenated.csv'):
        traitemnt = pd.read_csv(indir)
        traitemnt = traitemnt.drop(['OMOPdRM', 'OMOPdRM.1', 'OMOPdRM.2',
                                    'OMOPgRM', 'OMOPgRM.1', 'OMOPgRM.2', 'Time',
                                    'Time - Copie', 'alphaGait', 'normForceGuidon', 'Unnamed: 0', 'DistanceAligne',
                                    'DistanceEngage', 'DistanceFWGait',
                                    'DistanceFWRButte', 'AngleBike', 'AngleBike.1', 'AngleBike.2',
                                    'ForceGuidon', 'ForceGuidon.1', 'ForceGuidon.2',
                                    'ForceGuidon_R0', 'ForceGuidon_R0.1', 'ForceGuidon_R0.2',
                                    'ForcePedaleD_R0', 'ForcePedaleD_R0.1', 'ForcePedaleD_R0.2',
                                    'ForcePedaleG_R0', 'ForcePedaleG_R0.1', 'ForcePedaleG_R0.2', 'ForcePiedAv.2',
                                    'ForcePiedAv.1', 'TravailPAr', 'ThetaMrv', 'ThetaMrDeg', 'ThetaM', 'ThetaMDeg',
                                    'Impulsion',
                                    'ThetaMr', 'IndiceEfficacitePiedAv', 'IndiceEfficaciteTotal', 'ForcePiedAr.2',
                                    'ForcePiedAv',
                                    'ForcePiedAr', 'ForcePied', 'PuissancePAr', 'Moment', 'MomentPAr', 'MomentPAv',
                                    'DeplacementRider', 'DeplacementRiderRAr', 'DeplacementRider_RoueArriere'],
                                   axis=1)



        traitemnt = traitemnt.replace('t', np.nan, regex=True)
        traitemnt = traitemnt.fillna(traitemnt.mean())
        # traitemnt.to_csv("allconcate.csv", index=0)
        traitemnt = traitemnt.dropna(axis=0)
        print(traitemnt.describe())
        return traitemnt

    def regression_traitement(self):
        X = self.preprocessing_data()
        # Get column names first
        # X= X[['Moment','MomentPAr','MomentPAv','ForceUPiedAv']]
        names = X.columns
        # Create the Scaler object
        scaler = preprocessing.StandardScaler()
        # Fit your data on the scaler object
        scaled_df = scaler.fit_transform(X)
        X = pd.DataFrame(scaled_df, columns=names)

        y = X['ForceUPiedAv']
        X = X.drop('ForceUPiedAv', axis=1)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=15)

        lm = Ridge(alpha=1)
        lm.fit(X_train, y_train)

        # save the model to disk
        filename = 'Ridge_traitement.sav'
        pickle.dump(lm, open(filename, 'wb'))

        predictions = lm.predict(X_test)

        print('Coefficients : {} '.format(lm.coef_))
        print('R^2 score :' + str(r2_score(y_test, predictions)))

        result = sm.OLS(y, X).fit()
        print(result.summary())


    def test_regression(self):
        traitemnt = pd.read_csv('data/AP/trial8/CDonetraitementArthurPilard8.csv')
        traitemnt = traitemnt.dropna()

        X = traitemnt[['AngleBike', 'AngleBike.1', 'AngleBike.2', 'DeplacementRider',
                       'DistanceFWGait', 'DistanceFWRButte', 'ForcePedaleD_R0',
                       'ForcePedaleD_R0.1', 'ForcePedaleD_R0.2', 'ForcePedaleG_R0',
                       'ForcePedaleG_R0.1', 'ForcePedaleG_R0.2',
                       'Moment', 'Puissance', 'ThetaMDeg',
                       'ThetaMrDeg', 'VitessePedalier', 'Impulsion', 'ImpulsionPAr', 'ImpulsionPAv',
                       'Travail']]

        # y= traitemnt['IndiceEfficaciteTotal']
        y = traitemnt['ForceUPiedAv']

        loaded_model = pickle.load(open('Ridge_traitement.sav', 'rb'))

        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=101)
        y_pred = loaded_model.predict(X)

        print(np.array(y.loc[0:15]))
        print(y_pred[0:15])

        print('R2 linearReg :' + str(r2_score(y, y_pred)))
        print(loaded_model.coef_)
        print('rmse {} \n\n\n'.format(math.sqrt(mean_squared_error(y, y_pred))))


if __name__ == '__main__':
    a = AnalyseTraitement()
    # a.test_regression()
    a.regression_traitement()
    # a.preprocessing_data()