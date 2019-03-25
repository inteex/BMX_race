import pandas as pd
import glob

# travail = pd.read_csv('MR/travailMathisRagot1.csv')
#
# df =travail.reset_index(drop=True)
#
# df.to_csv('./TtravailMathisRagot1.csv')

# directoryFiles = glob.glob("C:\\Users\\mekhezzr\\Desktop\\donnees\\SD\\CritereDePerformanceSimbaDarnar5\\*\\")
# for item in directoryFiles:
#     print(item.split('\\')[-2])


file_path = "C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\SD\\trial1\\framesSimbaDarnar1.csv"

import os

size = os.stat(file_path).st_size/1024
print('{:2f}'.format(size))