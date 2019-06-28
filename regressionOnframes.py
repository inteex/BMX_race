import warnings

import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LassoLars, ElasticNet
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeRegressor
import math
import pickle
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import matplotlib.pyplot as plt

pd.set_option('max_rows', 50)
pd.set_option('max_columns', 10)


class AnalyseFrame:

    def regression_on_frames(self):
        frames = pd.read_csv("concatenat/AllframesConcatenated.csv")
        frames = frames.reset_index(drop=True)
        frames = frames.fillna(frames.mean())
        X = frames.drop(['TimeEnd', 'AlphaGaitDmin', 'DAlignementMin', 'DEpauleMin',
                         'DistanceRecul', 'Dmin',
                         'ThetaManivelleDepart', 'TpsReaction',
                         'moyennePuissance1', 'moyennePuissance2', 'moyennePuissance3',
                         'moyennePuissance4'], axis=1)
        y = frames['TimeEnd']

        polynomial_features = PolynomialFeatures(degree=2)
        X = polynomial_features.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=13)

        lm = Ridge()
        lm.fit(X_train, y_train)
        predictions = lm.predict(X_test)

        # save the model to disk
        # filename = '_frames.sav'
        # pickle.dump(lm2, open(filename, 'wb'))
        print('R2 Ridge :' + str(r2_score(y_test, predictions)))
        print(lm.coef_)
        print()

        # print(y_test.values)
        # print(predictions)
        # print(frames.columns)
        # olsmod = sm.OLS(y, X)
        # result = olsmod.fit()
        # print(result.summary())
        # yp = olsmod.predict(X)
        # print(yp)

        # y_pred = lm.predict(X_test)

    def model_selection(self):
        frames = pd.read_csv("C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\concatenat\\AllframesConcatenated.csv", delimiter=',')
        frames = frames.reset_index(drop=True)
        frames = frames.fillna(frames.mean())
        models = [Ridge(alpha=0.6)]

        for model in models:
            print("-" * 50)
            print(model)
            print("=" * 50)
            for degree in range(1, 6):
                """"
                'AlphaGaitDmin', 'Braquet', 'DAlignementMin', 'DEpauleMin',
                'DistanceRecul', 'Dmin', 'MasseBike', 'MasseRider', 'TailleRider',
                'ThetaManivelleDepart', 'TpsReaction', 'longueurManivelle',
                'moyennePuissance1', 'moyennePuissance2', 'moyennePuissance3',
                'moyennePuissance4'
                """

                X = frames.drop(['TimeEnd', 'AlphaGaitDmin', 'Braquet', 'DAlignementMin', 'DEpauleMin',
                'DistanceRecul', 'Dmin', 'MasseBike', 'MasseRider', 'TailleRider',
                'ThetaManivelleDepart', 'TpsReaction', 'longueurManivelle',
                'moyennePuissance1', 'moyennePuissance2', 'moyennePuissance3',
                'moyennePuissance4'], axis=1)

                y = frames['TimeEnd']
                y = y.fillna(y.mean())

                polynomial_features = PolynomialFeatures(degree=degree)
                X = polynomial_features.fit_transform(X)

                # test set
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=13)

                # cross validation set
                X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.15, random_state=13)

                lm = model
                lm.fit(X_train, y_train)
                y_pred = lm.predict(X_test)

                y_pred_val = lm.predict(X_val)

                r2_score_test = r2_score(y_test, y_pred)
                r2_score_val = r2_score(y_val, y_pred_val)
                # if r2_score_test > 0.78 and r2_score_val > 0.79:
                print('degree {}, test_R2 {:.3f}, val_R2 {:.3f}'.format(degree, r2_score_test,
                                                                        r2_score_val))

        # result = sm.OLS(y, X).fit()
        #
        # print(result.summary())

    def test_model_frames(self):
        frames = pd.read_csv("C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\concatenat\\AllframesConcatenated.csv")
        frames = frames.reset_index(drop=True)

        X = frames.drop(['TimeEnd', 'AlphaGaitDmin', 'DAlignementMin', 'DEpauleMin',
                         'DistanceRecul', 'Dmin',
                         'ThetaManivelleDepart', 'TpsReaction',
                         'moyennePuissance1', 'moyennePuissance2', 'moyennePuissance3',
                         'moyennePuissance4'], axis=1)
        X = X.fillna(frames.mean())
        y = frames['TimeEnd']
        y = y.fillna(y.mean())

        polynomial_features = PolynomialFeatures(degree=2)
        X = polynomial_features.fit_transform(X)

        # test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=13)

        # lm = Ridge(alpha=0.5)
        lm = pickle.load(open('Ridge_deg2_frames.sav', 'rb'))
        lm.fit(X_train, y_train)
        y_pred = lm.predict(X_test)

        r2_score_test = r2_score(y_test, y_pred)

        print('test_R2 {}'.format(str(r2_score_test)))

        erreur = []
        for y_p, y_t in zip(y_pred, np.array(y_test)):
            print('prédiction: {:.3f}, Valeur réelle: {:.3f}, Erreur: {:.3f}, pourcentage: {:.3f}%'.format(y_p, y_t,
                                                                                                           abs(
                                                                                                               y_p - y_t),
                                                                                                           100 * abs(
                                                                                                               y_p - y_t) / y_t))
            erreur.append(abs(y_p - y_t))
        print('max: {:.3f}, min: {:.3f}, moyenne: {:.3f}'.format(np.max(erreur), np.min(erreur), np.mean(erreur)))


if __name__ == '__main__':
    frame = AnalyseFrame()

    warnings.filterwarnings("ignore")  # ignore warnings
    frame.model_selection()
    # frame.regression_on_frames()
    # frame.test_model_frames()

