import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''lire les fichier csv'''

df = pd.read_csv('MR/trial7/TraitementMathisRagot7.csv')
frame = pd.read_csv('framesMathisRagot7.csv')
travail = pd.read_csv('MR/trial7/travailMathisRagot7.csv')


bip = int(frame.Bip[0]) #debut : le moment du Bip
finDep = int(frame.FinDplcmt[0]) #findep : find de deplacement


'''
    decaler le Temps au moment du prmier Bip 
    et prendre l'interval entre le Bip et fin deplacement
'''
time = df.Time
time = time.loc[0:finDep - bip]


df = df.loc[bip:finDep]
df['Time'] = time.values
df =df.reset_index(drop=True)
df.to_csv('./CtraitementMathisRagot7.csv')
