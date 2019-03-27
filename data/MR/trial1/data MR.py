import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class DataMr:
    def draw(self):
        df = pd.read_csv('MathisRagot1.csv')
        frame = pd.read_csv('framesMathisRagot1.csv')
        print(df.columns)
        print(frame.columns)
        print(frame.Bip)
        print(frame.BasDeButte)
        print(df.ThetaMrDeg)
        print(df.ThetaMDeg)

        plt.plot(df.Time,df.VitesseRider)
        plt.plot(df.Time,abs(df.ForcePedaleD_R0/100))
        plt.plot(df.Time,abs(df.ForcePedaleG_R0/100))
        plt.plot(df.Time,df.DeplacementRider/1000)
        plt.plot(df.Time,df.DistanceEngage)
        plt.legend(['vitesse','piedGauche','piedDroit','DeplacementRider'])
        plt.title('temps en bas de butt'+ str(frame.FinDplcmt[0]-frame.Bip[0]))
        plt.show()


    def correlation_heatmap(self):
            import seaborn as sns

            train = pd.read_csv("./MathisRagot1.csv")
            correlations = train.corr()[train.corr().apply(lambda x: abs(x) > 0.5)]

            fig, ax = plt.subplots(figsize=(40, 30))
            sns.heatmap(correlations, vmax=1.0, center=0, fmt='.2f',
                        square=True, linewidths=.5, annot=True, cbar_kws={"shrink": .70})
            #plt.savefig("corelationEntreLesVariables")
            plt.show()

if __name__ == '__main__':
    data = DataMr()
    data.draw()
    #data.correlation_heatmap()

    

