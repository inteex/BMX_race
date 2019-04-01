import pandas as pd
import glob

#
# size = os.stat(file_path).st_size/1024
# print('{:2f}'.format(size))

pd.set_option('max_rows',5)
pd.set_option('max_columns',50)

data = pd.read_csv('data\\AP\\trial6\\framesArthurPilard6.csv')
data1 = pd.read_csv('data\\AP\\trial5\\framesArthurPilard5.csv')

frames = pd.concat([data.iloc[0:1],data1[0:1]],axis=0)



print(data.shape)
print(data1.shape)
print(frames.shape)

print(data.columns)
print(data1.columns)

