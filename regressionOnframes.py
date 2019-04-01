import pandas as pd
import io
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
import math

import numpy as np
from sklearn.model_selection import train_test_split

pd.set_option('max_rows', 50)
pd.set_option('max_columns', 10)


class AnalyseFrame:
    def regression_on_frames(self):
        frames = pd.read_csv("data\\AllframesConcatenated.csv")
        print(frames.describe())

        frames = frames.reset_index(drop=True)
        X = frames.drop('TimeEnd', axis=1)
        X = X.fillna(frames.mean())
        print(X)

        y = frames['TimeEnd']
        print(y)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=101)

        lm = LinearRegression()
        lm.fit(X_train, y_train)

        predictions = lm.predict(X_test)

        lm2 = DecisionTreeRegressor(criterion='mse', max_depth=6)
        lm2.fit(X_train, y_train)
        predictions2 = lm2.predict(X_test)

        print('R2 linearReg :' + str(r2_score(y_test, predictions)))
        print(lm.coef_)
        print('rmse {} \n\n\n'.format(math.sqrt(mean_squared_error(y_test, predictions))))

        print('R2 DecisionTreeRegressor :' + str(r2_score(y_test, predictions2)))
        print('rmse {}'.format(math.sqrt(mean_squared_error(y_test, predictions2))))

        print(predictions2)
        print(y_test.values)


if __name__ == '__main__':
    frame = AnalyseFrame()
    frame.regression_on_frames()
