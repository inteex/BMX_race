import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt  # Data visualisation libraries
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
import math
data = pd.read_csv('data\\AP\\trial6\\CDonetraitementArthurPilard6.csv')


X=data[['ForcePied','Puissance','Time','VitesseRider']]
X= X.fillna(X.mean())
pd.set_option("display.max_rows", 600)
pd.set_option("display.max_columns", 50)
y = data['IndiceEfficacitePiedAr']



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=101)

lm = LinearRegression()
lm.fit(X_train, y_train)

predictions = lm.predict(X_test)


lm2 = DecisionTreeRegressor(criterion='mse', max_depth=6)
lm2.fit(X_train, y_train)
predictions2 = lm2.predict(X_test)

print(r2_score(y_test,predictions))
print(r2_score(y_test, predictions2))
print(math.sqrt(mean_squared_error(y_test, predictions)))
print(math.sqrt(mean_squared_error(y_test, predictions2)))
print(predictions2)
print(y_test.values)

plt.scatter(y_test, predictions2)
plt.plot(y_test,predictions2)
plt.show()