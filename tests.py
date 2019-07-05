import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LinearRegression, Ridge, ElasticNet, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import sklearn.feature_extraction as fe
import math
import pickle
from navigate_files import NavigateFiles
from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures
import glob
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.feature_selection import f_regression, mutual_info_regression
from scipy import stats

pd.set_option('max_rows', 50)
pd.set_option('max_columns', 50)


class Tests:
    def regression_traitement(self):
        indir = 'data/AlltraitementConcatenated.csv'
        traitemnt = pd.read_csv(indir)

        pretraitement = traitemnt[['AngleBike', 'AngleBike.1', 'AngleBike.2', 'DeplacementRider',
                                   'DistanceFWGait', 'ForcePedaleD_R0',
                                   'ForcePedaleD_R0.1', 'ForcePedaleD_R0.2', 'ForcePedaleG_R0',
                                   'ForcePedaleG_R0.1', 'ForcePedaleG_R0.2', 'ForcePied', 'ForcePiedAr',
                                   'ForcePiedAr.1', 'ForcePiedAr.2', 'ForcePiedAv', 'ForcePiedAv.1', 'ForcePiedAv.2',
                                   'Moment', 'MomentPAr', 'MomentPAv', 'Puissance', 'PuissancePAr', 'PuissancePAv',
                                   'ThetaMDeg',
                                   'ThetaMrDeg', 'VitessePedalier', 'VitesseRider', 'Impulsion', 'ImpulsionPAr',
                                   'ImpulsionPAv',
                                   'Travail', 'TravailPAr', 'TravailPAv', 'ForceUPiedAv']]

        pretraitement = pretraitement.dropna()

        X = pretraitement[
            ['AngleBike', 'AngleBike.1', 'AngleBike.2', 'DeplacementRider', 'DistanceFWGait',
             'ForcePedaleD_R0', 'ForcePedaleD_R0.1', 'ForcePedaleD_R0.2',
             'ForcePedaleG_R0', 'ForcePedaleG_R0.1', 'ForcePedaleG_R0.2', 'Moment', 'Puissance',
             'ThetaMDeg', 'ThetaMrDeg', 'VitessePedalier', 'Impulsion', 'ImpulsionPAr', 'ImpulsionPAv',
             'Travail', 'ForceUPiedAv']
        ]

        # Get column names first
        names = X.columns
        # Create the Scaler object
        scaler = preprocessing.StandardScaler()
        # Fit your data on the scaler object
        scaled_df = scaler.fit_transform(X)
        X = pd.DataFrame(scaled_df, columns=names)

        y = X['ForceUPiedAv']
        X = X.drop('ForceUPiedAv', axis=1)
        print(X.columns)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

        lm = Ridge(alpha=.5)
        lm.fit(X_train, y_train)
        predictions = lm.predict(X_test)

        print('R^2 Ridge :' + str(r2_score(y_test, predictions)))
        print('rmse {} \n\n\n'.format(math.sqrt(mean_squared_error(y_test, predictions))))
        print(lm.coef_)

        # print("f-test : {}".format(f_regression(X, y, center=True)))
        # print("t-test : {}".format(stats.ttest_ind(X['AngleBike'], y, axis=0, equal_var=True)))
        # print("mutual-test : {}".format(mutual_info_regression(X, y)))

        # result = sm.OLS(y, X).fit()
        # print(result.summary())

        from sklearn.feature_selection import SelectPercentile

        pretraitement = traitemnt[['AngleBike', 'AngleBike.1', 'AngleBike.2', 'DeplacementRider',
                                   'DistanceFWGait', 'ForcePedaleD_R0',
                                   'ForcePedaleD_R0.1', 'ForcePedaleD_R0.2', 'ForcePedaleG_R0',
                                   'ForcePedaleG_R0.1', 'ForcePedaleG_R0.2', 'ForcePied', 'ForcePiedAr',
                                   'ForcePiedAr.1', 'ForcePiedAr.2', 'ForcePiedAv', 'ForcePiedAv.1', 'ForcePiedAv.2',
                                   'Moment', 'MomentPAr', 'MomentPAv', 'Puissance', 'PuissancePAr', 'PuissancePAv',
                                   'ForceUPiedAv'
                                   ]]
        pretraitement = pretraitement.dropna()

        # Get column names first
        names = pretraitement.columns
        # Create the Scaler object
        scaler = preprocessing.StandardScaler()
        # Fit your data on the scaler object
        scaled_df = scaler.fit_transform(pretraitement)

        pretraitement = pd.DataFrame(scaled_df, columns=names)

        traitemnt = pretraitement.drop('ForceUPiedAv', axis=1)

        X_train, X_test, y_train, y_test = train_test_split(traitemnt, y, random_state=0, test_size=.5)
        # select = SelectPercentile(percentile=75)
        #
        # select.fit(X_train, y_train)
        # X_train_selected = select.transform(X_train)
        # X_test_selected = select.transform(X_test)
        #
        # print('X_train.shape is: {}'.format(X_train.shape))
        # print('X_train_selected.shape is: {}'.format(X_train_selected.shape))
        #
        # mask = X_train.columns[select.get_support()]
        # print(mask)
        # print(select.get_support())

        from sklearn.feature_selection import SelectFromModel
        from sklearn.ensemble import RandomForestClassifier

        select = SelectFromModel(RandomForestClassifier(n_estimators=100, random_state=42), threshold='median')
        select.fit(X_train, y_train)

        X_train_s = select.transform(X_train)
        print('The shape of X_train is: ', X_train.shape)
        print('The shape of X_train_s is ', X_train_s.shape)

        # lm2 = Ridge(alpha=.5)
        # lm2.fit(X_train_s, y_train)
        # X_test_s = select.transform(X_test)
        # y_pr = lm2.predict(X_test_s)
        #
        # print('R^2 Ridge :' + str(r2_score(y_test, y_pr)))
        # print('rmse {} \n\n\n'.format(math.sqrt(mean_squared_error(y_test, y_pr))))
        # print(lm2.coef_)

    def ap(self):
        traitement = 'data_v2_old/RR/trial2/traitement_RomainRacine2_2018-06-22.csv'
        frame = 'data_v2_old/RR/trial2/frames_RomainRacine2_2018-06-22.csv'
        traitement = pd.read_csv(traitement)
        frame = pd.read_csv(frame)
        print(frame.columns)
        exit()
        bip = int(frame.Bip[0])  # debut : le moment du Bip
        if 'FinMarkerVisible' in frame.columns:
            finDep = int(frame.FinMarkerVisible[0])
        else:
            finDep = int(frame.FinDplcmt[0])

        time = traitement.Time
        time_before_reaction = -(time.loc[0:109][::-1])
        time_before_reaction = time_before_reaction.reset_index(drop=True)
        time_before_reaction = time_before_reaction.append(pd.Series([0]), ignore_index=True)
        time = time.loc[0:finDep - bip - 111]
        time_before_reaction = pd.Series(time_before_reaction)
        time = pd.Series(time)
        time_before_reaction.append(time, ignore_index=True)
        print(time_before_reaction.append(time, ignore_index=True))
        # print(df['Time'].loc[frame['TpsReaction'][0]-frame['Bip'][0]])

    def correlation_heatmap(self):
        import seaborn as sns

        train = pd.read_csv("./MathisRagot1.csv")
        correlations = train.corr()[train.corr().apply(lambda x: abs(x) > 0.5)]

        fig, ax = plt.subplots(figsize=(40, 30))
        sns.heatmap(correlations, vmax=1.0, center=0, fmt='.2f',
                    square=True, linewidths=.5, annot=True, cbar_kws={"shrink": .70})
        # plt.savefig("corelationEntreLesVariables")
        plt.show()

    def start1csv(self):
        start = pd.read_csv("Start1_IK.csv", delimiter=";")
        print(start.time)
        print(start.describe())

    def classifier(self):

        frames = pd.read_csv("C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\concatenat\\AllframesConcatenated.csv")
        from sklearn import svm

        X = frames.drop(['TimeEnd'], axis=1)
        y = frames['TimeEnd']
        y = y.fillna(y.mean())
        X = X.fillna(X.mean())
        clf = svm.SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1,
                      gamma='auto_deprecated', kernel='rbf', max_iter=-1, shrinking=True,
                      tol=0.001, verbose=False)

        # test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=13)

        clf.fit(X_train, y_train)
        print(clf.score(X_test, y_test))


if __name__ == '__main__':
    a = Tests()
    # a.regression_traitement()
    # a.start1csv()
    a.classifier()
