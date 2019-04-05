import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression, Ridge, ElasticNet, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import math
import pickle
from navigate_to_trials import NavigateFiles
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
    def preprocessing_data(self, indir='C:/Users/mekhezzr/PycharmProjects/bmx_race/data/AlltraitementConcatenated.csv'):
        traitemnt = pd.read_csv(indir)
        traitemnt = traitemnt.drop(['OMOPdRM', 'OMOPdRM.1', 'OMOPdRM.2',
                                    'OMOPgRM', 'OMOPgRM.1', 'OMOPgRM.2', 'Time',
                                    'Time - Copie', 'alphaGait', 'normForceGuidon', 'Unnamed: 0', 'DistanceAligne',
                                    'DistanceEngage', 'DistanceFWGait',
                                    'DistanceFWRButte', 'AngleBike', 'AngleBike.1', 'AngleBike.2', 'VitessePedalier',
                                    'ForceGuidon', 'ForceGuidon.1', 'ForceGuidon.2',
                                    'ForceGuidon_R0', 'ForceGuidon_R0.1', 'ForceGuidon_R0.2',
                                    'ForcePedaleD_R0', 'ForcePedaleD_R0.1', 'ForcePedaleD_R0.2',
                                    'ForcePedaleG_R0', 'ForcePedaleG_R0.1', 'ForcePedaleG_R0.2', 'ForcePiedAv.1'],
                                   axis=1)

        traitemnt = traitemnt.dropna(axis=0)

        return traitemnt

    def regression_traitement(self):

        X = self.preprocessing_data()
        # Get column names first
        names = X.columns
        # Create the Scaler object
        scaler = preprocessing.StandardScaler()
        # Fit your data on the scaler object
        scaled_df = scaler.fit_transform(X)
        X = pd.DataFrame(scaled_df, columns=names)

        y = X['ForceUPiedAv']
        X = X.drop('ForceUPiedAv', axis=1)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

        lm = Ridge(alpha=500)
        lm.fit(X_train, y_train)

        # save the model to disk
        # filename = 'Ridge_traitement.sav'
        # pickle.dump(lm, open(filename, 'wb'))

        predictions = lm.predict(X_test)

        print('R^2 Ridge :' + str(r2_score(y_test, predictions)))
        print('rmse {} \n\n\n'.format(math.sqrt(mean_squared_error(y_test, predictions))))
        print(lm.coef_)
        # print("f-test : {}".format(f_regression(X, y, center=True)))
        # print("t-test : {}".format(stats.ttest_ind(X['AngleBike'], y, axis=0, equal_var=True)))
        # print("mutual-test : {}".format(mutual_info_regression(X, y)))

        result = sm.OLS(y, X).fit()
        print(result.rsquared_adj)
        print(result.rsquared)
        print(result.summary())

        # polynomial Regression

        # polynomial_features = PolynomialFeatures(degree=2)
        # x_poly = polynomial_features.fit_transform(X_train)
        #
        # model = LinearRegression()
        # model.fit(x_poly, y_train)
        #
        # y_pred = lm.predict(X_test)
        # print('R^2 Ridge++++++++++ :' + str(r2_score(y_test, y_pred)))
        # print('rmse {}++ \n\n\n'.format(math.sqrt(mean_squared_error(y_test, y_pred))))

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

    def concat_all_traitement(self, indir, file_num):
        files = NavigateFiles().get_all_files_by_num(indir, file_num)
        appended_data = []
        for pilote in files:
            for file in pilote:  # the file in th trial

                trials = "\\".join(file.split('\\')[1:4])  # get Trial path
                traitemnt = pd.read_csv(file)

                appended_data.append(traitemnt)
        appended_data = pd.concat(appended_data, axis=0)
        appended_data.to_csv("data\\AlltraitementConcatenated.csv", index=0)


if __name__ == '__main__':
    a = AnalyseTraitement()
    # a.concat_all_traitement(indir='./data',file_num=0)
    # a.test_regression()
    a.regression_traitement()
    # a.preprocessing_data()
