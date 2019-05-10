import warnings

import pandas as pd
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
        frames = pd.read_csv("data\\AllframesConcatenated.csv")
        frames = frames.reset_index(drop=True)
        X = frames.drop(['TimeEnd', 'MasseBike', 'TailleRider'], axis=1)
        X = X.fillna(frames.mean())
        # X['dev'] = X['Braquet'] * X['longueurManivelle']
        #
        # X['longXmass'] = X['MasseRider'] * X['longueurManivelle']
        # X['BraqXmass'] = X['Braquet'] * X['MasseRider']

        y = frames['TimeEnd']

        polynomial_features = PolynomialFeatures(degree=2)
        X = polynomial_features.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=10)

        lm = Ridge(alpha=0.0001)
        lm.fit(X_train, y_train)
        predictions = lm.predict(X_test)
        # y =-2.9150*X['Braquet']+ 0.1468* X['MasseRider']-0.0453* X['longueurManivelle']+0.0219* X['dev']
        # plt.plot(y)
        # plt.show()

        # save the model to disk
        # filename = '_frames.sav'
        # pickle.dump(lm2, open(filename, 'wb'))
        print('R2 linearReg :' + str(r2_score(y_test, predictions)))
        print(lm.coef_)
        print()

        # print(y_test.values)
        # print(predictions)

        # result = sm.OLS(y, X).fit()

        # print(result.summary())

        # y_pred = lm.predict(X_test)

    def model_selection(self):
        frames = pd.read_csv("data\\AllframesConcatenated.csv")
        frames = frames.reset_index(drop=True)

        models = [LinearRegression(), Ridge(alpha=.5), Lasso(alpha=.5), ElasticNet(alpha=.5)]

        for model in models:
            print("-" * 50)
            print(model)
            print("=" * 50)
            for degree in range(1, 11):
                X = frames.drop(['TimeEnd'], axis=1)
                X = X.fillna(frames.mean())
                y = frames['TimeEnd']

                polynomial_features = PolynomialFeatures(degree=degree)
                X = polynomial_features.fit_transform(X)

                # test set
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=13)

                # cross validation set
                X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=13)

                lm = model
                lm.fit(X_train, y_train)
                y_pred = lm.predict(X_test)

                y_pred_val = lm.predict(X_val)

                r2_score_test = r2_score(y_test, y_pred)
                r2_score_val = r2_score(y_val, y_pred_val)
                if r2_score_test > 0.70 and r2_score_val > 0.70:
                    print('degree: {}, test_R2 {}, val_R2 {}'.format(degree, str(r2_score_test),
                                                                     str(r2_score_val)))
                # print('val_R2 {}, degree: {}'.format(str(r2_score(y_test, y_pred)),d))


if __name__ == '__main__':
    frame = AnalyseFrame()
    # frame.regression_on_frames()
    warnings.filterwarnings("ignore")  # ignore warnings
    frame.model_selection()
