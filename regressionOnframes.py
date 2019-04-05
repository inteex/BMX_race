import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LassoLars,ElasticNet
from sklearn.tree import DecisionTreeRegressor
import math
import pickle
from sklearn.model_selection import train_test_split
import statsmodels.api as sm

pd.set_option('max_rows', 50)
pd.set_option('max_columns', 10)


class AnalyseFrame:

    def regression_on_frames(self):
        frames = pd.read_csv("data\\AllframesConcatenated.csv")
        frames = frames.reset_index(drop=True)
        X = frames.drop('TimeEnd', axis=1)
        X = X.fillna(frames.mean())

        y = frames['TimeEnd']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=101)



        lm = LinearRegression()
        lm.fit(X_train, y_train)

        predictions = lm.predict(X_test)



        # save the model to disk
        # filename = '_frames.sav'
        # pickle.dump(lm2, open(filename, 'wb'))



        print('R2 linearReg :' + str(r2_score(y_test, predictions)))
        print('rmse {} \n\n\n'.format(math.sqrt(mean_squared_error(y_test, predictions))))
        print(y_test[0:10])
        print(predictions[0:10])

        result = sm.OLS(y, X).fit()
        print(result.summary())
        print(result.coef_)


if __name__ == '__main__':

    frame = AnalyseFrame()
    frame.regression_on_frames()