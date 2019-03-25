import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 300)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df = pd.read_csv('CritereDePerformanceSimbaDarnar11.csv')
# df = pd.read_csv('SimbaDarnand1Traitement.csv')




'''for column in df.columns:
    print(column)
    if df[column].count() == 1:
        v = df[column][0]
        df[column] = v
        
df.to_csv('./CritereDePerformanceSimbaDarnar11.csv', index=None)

exit(1)'''


df = df[(df.Time > 0) & (df.Time < df.TpsBasDeButte[0]) ]
print(df)
print(df.describe())


vitess = df['VitesseRider']
plt.plot(df.Time, vitess)
plt.plot(df.Time, df.ForceUPiedAr/10)
plt.plot(df.Time, df.ForcePiedAv/10 )
plt.legend(['Vitesse', 'ForceUPiedAr/10','ForcePiedAv'])
plt.show()

plt.scatter(df.ForceUPiedAr/10, vitess)
plt.xlabel('force')
plt.ylabel('Vitesse')
plt.show()

vitess = df['VitesseRider']
plt.plot(df.Time, vitess)
plt.plot(df.Time, df.ForcePiedAv/10 )
plt.legend(['Vitesse', 'ForcePiedAv/10'])
plt.show()

plt.scatter(df.ForcePiedAv/10, vitess)
plt.xlabel('force')
plt.ylabel('Vitesse')
plt.show()
