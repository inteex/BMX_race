import pandas as pd
import matplotlib.pyplot as plt
import glob

from sklearn import preprocessing
from mpl_toolkits.mplot3d import Axes3D
from navigate_to_trials import NavigateFiles
from sklearn.preprocessing import PolynomialFeatures


class PlotBestTestPerPilote:
    def plot_best_pilots_trial_together(self, data_indir, x_axis, y_axis):
        """
            Plot the best trial of each pilot in one figure.
                :param data_indir:  Path to data.
                :param x_axis: array of features to plot in xaxis.
                :param y_axis:  array of features to plot in the y-axis.
        """

        bestTrials = NavigateFiles().get_all_best_trials(data_indir)
        legend = []
        for xi in x_axis:
            for column in y_axis:
                # plt.figure(num=None, figsize=(12.8, 7.2), dpi=300, facecolor='w', edgecolor='k')
                for trial in bestTrials:
                    fileList = glob.glob((trial + '\\*.csv'))  # all files of a trial
                    traitement = pd.read_csv(fileList[1])  # first file in the
                    x = traitement[xi]
                    time = traitement['Time']
                    pilot_name = trial.split('\\')[-2]
                    trial_and_number = trial.split('\\')[-1]
                    col = traitement[column]
                    plt.plot(x, col)
                    legend.append(
                        '{} {} time:{:.3f}s'.format(pilot_name, trial_and_number, time.iloc[-2]))
                    print('{} time: {}'.format(trial.split('\\')[-2], time.iloc[-2]))
                print()
                print()
                plt.xlabel(xi)
                plt.ylabel(column)
                plt.legend(legend)
                plt.title('{} en fonction de {}'.format(column, xi))
                plt.grid()
                # txt = "{}".format()
                # plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
                # plt.savefig('figures/{}_{}.png'.format(column, xi))
                plt.show()

    def plot_best_pilot_trial_single(self, data_indir, x_axis, y_axis):
        """
            Plot pilots best trial in separated figure.
                :param data_indir:  Path to data.
                :param x_axis: array of features to plot in x-axis.
                :param y_axis:  array of features to plot in the y-axis.
        """

        best_trials = NavigateFiles().get_all_best_trials(data_indir)
        legend = []
        for xi in x_axis:  # for all x axis variables
            for trial in best_trials:  # for the best trail of the pilot
                fileList = glob.glob((trial + '\\*.csv'))  # all files of a trial
                traitement = pd.read_csv(fileList[1])  # first file in the trail
                frames = pd.read_csv(fileList[0])
                pilot_name = trial.split('\\')[-2]
                x = traitement[xi]
                coups_de_pedal1 = frames['CoupsDePedal'][0] - frames["Bip"][0]
                coups_de_pedal2 = frames['CoupsDePedal.1'][0] - frames["Bip"][0]
                coups_de_pedal3 = frames['CoupsDePedal.2'][0] - frames["Bip"][0]
                # plt.figure(num=None, figsize=(12.8, 7.2), dpi=300, facecolor='w', edgecolor='k')

                for column in y_axis:  # for all y axis variables
                    col = traitement[column]
                    if column == 'VitesseRider':
                        col = col * 100
                        legend.append('{}'.format(column + '* 100'))
                    else:
                        legend.append('{}'.format(column))
                    plt.plot(x, col)
                str = ','.join(y_axis)
                plt.xlabel(xi)
                plt.ylabel(column)
                plt.legend(legend)
                plt.title('Pilote {}: {} en fonction de {}'.format(pilot_name, str, xi))
                plt.axvline(x[coups_de_pedal1], color='red', linestyle='--')
                plt.axvline(x[frames['TpsReaction'][0] - frames["Bip"][0]], color='red', linestyle='--')
                plt.axvline(x[coups_de_pedal2], color='red', linestyle='--')
                plt.axvline(x[coups_de_pedal3], color='red', linestyle='--')
                plt.grid()
                plt.show()
                # str = '_'.join(y_axis)
                # plt.savefig('figures/single/{}_{}_{}TTT.png'.format(pilot_name, str, xi))

    def externDetailsPilote(self, data_indir, position_frames=0, position_traitements=1):
        """
        Extern some distinct information about pilots: Poids, Taille, Braquet,
        Longueur Manivelle and the time of the best trial.
            :param data_indir:Path to data indir.
            :param position_frames: Position of the file frames in a trial by default 0.
            :param position_traitements:Position of the file taitement in a trial by default 1.
            :return:txt file.
        """
        bestTrials = NavigateFiles().get_all_best_trials(data_indir)
        masseRiders = []
        BraquetRiders = []
        longueurManivelleRiders = []
        tailleRiders = []
        f = open('Details_riders.txt', 'w')
        print('-----------------------------', file=f)
        for trial in bestTrials:
            fileList = glob.glob((trial + '\\*.csv'))
            traitement = pd.read_csv(fileList[position_traitements])  # 0 -> first file in list its CDonetraitement.csv
            frames = pd.read_csv(fileList[position_frames])  # 2 -  > third file in list its frames
            time = traitement['Time']
            if 'Braquet' in frames.columns:
                braquet = frames['Braquet'][0]
            else:
                braquet = 0
            if 'MasseRider' in frames.columns:
                masseRider = frames['MasseRider'][0]
            else:
                masseRider = 0
            if 'longueurManivelle' in frames.columns:
                longueurManivelle = frames['longueurManivelle'][0]
            else:
                longueurManivelle = 0
            if 'TailleRider' in frames.columns:
                tailleRider = frames['TailleRider'][0]
            else:
                tailleRider = 0
            print('{} time: {:.3f}s'.format(trial.split('\\')[-2], time.iloc[-2]), file=f)
            print('-----------------------------', file=f)
            print('Poids: {} '.format(masseRider), file=f)
            print('taille: {} '.format(tailleRider), file=f)
            print('braquet: {}'.format(braquet), file=f)
            print('Longueur Manivelle: {}'.format(longueurManivelle), file=f)
            print('-----------------------------', file=f)
            masseRiders.append(masseRider)
            tailleRiders.append(tailleRider)
            BraquetRiders.append(braquet * 10)
            longueurManivelleRiders.append(longueurManivelle)

    def plot_by_pilotes_names_trials_nums_dates(self, data_indir, pilotes_names, trials_nums, dates_trial, x_axis,
                                                y_axis):
        """

        :param data_indir:
        :param pilotes_names:
        :param trials_nums:
        :param x_axis:
        :param y_axis:
        :return:
        """
        trial_files = NavigateFiles().get_files_by_pilotes_names_trials_nums_dates(data_indir, pilotes_names,
                                                                                   trials_nums, dates_trial)
        legend = []
        for xi in x_axis:
            for column in y_axis:
                # plt.figure(num=None, figsize=(12.8, 7.2), dpi=300, facecolor='w', edgecolor='k')
                for trial in trial_files:
                    traitement = pd.read_csv(trial[1])  # first file in the
                    x = traitement[xi]
                    col = traitement[column]
                    pilot_name = trial[0].split('\\')[-3]
                    trial_and_number = trial[0].split('\\')[-2]
                    plt.plot(x, col)
                    legend.append(
                        '{} {} '.format(pilot_name, trial_and_number))
                plt.xlabel(xi)
                plt.ylabel(column)
                plt.legend(legend)
                plt.title('{} en fonction de {}'.format(column, xi))
                plt.grid()
                # txt = "{}".format()
                # plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
                # plt.savefig('figures/{}_{}.png'.format(column, xi))
                plt.show()

    def correlation_heatmap(self):
        import seaborn as sns

        train = pd.read_csv("../data_v2/SD/trial1/traitement_SimbaDarnand1_2018-06-21.csv")
        correlations = train.corr()

        fig, ax = plt.subplots(figsize=(40, 30))
        sns.heatmap(correlations, vmax=1.0, center=0, fmt='.2f',
                    square=True, linewidths=.5, annot=True, cbar_kws={"shrink": .70})
        # plt.savefig("corelationEntreLesVariables")
        plt.show()

    def plot_frame_concatenated(self, frames_indir):
        frames = pd.read_csv(frames_indir)
        frames = frames.fillna(frames.mean())
        time = frames['TimeEnd']
        frames = frames.drop(['TimeEnd', 'AlphaGaitDmin',  'DAlignementMin', 'DEpauleMin',
                'DistanceRecul', 'Dmin',
                'ThetaManivelleDepart'], axis=1)

        # names = frames.columns
        # # Create the Scaler object
        # scaler = preprocessing.StandardScaler()
        # # Fit your data on the scaler object
        # scaled_df = scaler.fit_transform(frames)
        # frames = pd.DataFrame(scaled_df, columns=names)

        # polynomial_features = PolynomialFeatures(degree=1)
        # frames = polynomial_features.fit_transform(frames)
        #
        # for col in range(0, frames.shape[1]):
        #     plt.scatter(time, frames[:, col])
        # plt.xlabel('Time')
        # plt.ylabel('Vars discrètes')
        # # plt.show()
        # plt.savefig('../figures/parametres_choisis/var_dsicretes_tpsReact.png')

        leg=[]
        for col in frames.columns:
            plt.scatter(time, frames[col])
            leg.append(col)
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Vars discrètes')
        plt.savefig('../figures/var_dsicretes_moyennePuissance4.png')
        # plt.show()


if __name__ == '__main__':
    obj = PlotBestTestPerPilote()
    obj.plot_frame_concatenated(
        frames_indir='C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\concatenat\\AllframesConcatenated.csv')
    exit()
    columns = ['Puissance']
    xaxis = ['Time']
    # obj.plot_by_pilotes_names_trials_nums_dates(data_indir='C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\data_v2',
    #                                             pilotes_names=['ThomasJouve', 'Arthur'], trials_nums=[7, 3],
    #                                             dates_trial=['2018-06-20', '2018-06-21'], x_axis=xaxis, y_axis=columns
    #                                             )
    #
    # obj.plot_best_pilots_trial_together(data_indir='C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\data_v2',
    #                                     x_axis=xaxis, y_axis=columns)
    # obj.plot_best_pilot_trial_single(data_indir='C:\\Users\\mekhezzr\\PycharmProjects\\bmx_race\\data_v2',
    #                                  x_axis=xaxis, y_axis=columns)
    # obj.externDetailsPilote(indir='.\\data\\')
