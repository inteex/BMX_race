import scipy.io
import numpy as np
import pandas as pd
import scipy
import os

df= pd.read_csv('Time.csv')
# df.reset_index(drop=True)
series = df.T
#series = series.reset_index(drop=False)

series.to_csv('./cc.csv')

