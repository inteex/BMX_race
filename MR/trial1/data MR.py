import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class DataMr:
    def draw(self):
        df = pd.read_csv('MathisRagot1.csv')
        frame = pd.read_csv('framesMathisRagot1.csv')
        print(df.columns)
        print(frame.columns)

        plt.plot(df.Time,df.VitesseRider)
        plt.plot(df.Time,abs(df.ForcePedaleD_R0/100))
        plt.plot(df.Time,abs(df.ForcePedaleG_R0/100))
        plt.plot(df.Time,df.DeplacementRider/1000)
        plt.plot(df.Time,df.DistanceEngage)
        plt.legend(['vitesse','piedGauche','piedDroit','DeplacementRider'])
        plt.show()


        plt.hist(df.VitesseRider)
        plt.show()

        plt.scatter(abs(df.ForcePedaleD_R0),df.VitesseRider)
        plt.show()

if __name__ == '__main__':
    data = DataMr()
    data.draw()

    

