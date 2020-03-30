import numpy as np
import pandas as pd
from DataFuncs import DataFuncs


class ScoreClass:
    def __init__(self, tag_data, win_size_seconds):
        self.tag_data = tag_data
        self.win_size_seconds = win_size_seconds
        self.func = None
        self.distance_th = None
        self.data_th = None

    def set_func(self, func):
        self.func = func
        self.column_name = func + '_' + 'rssi'

    def set_distance_th(self, distance_m):
        self.distance_th = distance_m

    def set_data_th(self, th):
        self.data_th = th

    def scores(self, score):
        DataFuncsObj = DataFuncs()
        if self.func is None:
            print('Please set wanted function')
            return
        if self.win_size_seconds is None:
            print('Please set wanted window size')
            return
        if self.distance_th is None:
            print('Please set distance th [m]')
            return
        if self.data_th is None:
            print('Please set data th')
            return
        result = DataFuncsObj.run_rolling_func_df_2_columns(self.tag_data, self.func, 'DisplayName', 'distance',
                                                            'rssi', self.win_size_seconds)
        condition_data = result[self.column_name] >= self.data_th
        condition_distance = result['distance'] <= self.distance_th
        P_ = (condition_distance == 1)  # positive
        # condition positive (P) the number of real positive cases in the data
        T_ = (condition_data == condition_distance)  # true
        N_ = (condition_distance == 0)  # negative
        # N the number of real negative cases in the data
        F_ = np.logical_not(T_)  # false

        TP = np.sum(np.logical_and(T_, P_))
        FP = np.sum(np.logical_and(F_, P_))
        FN = np.sum(np.logical_and(F_, N_))
        TN = np.sum(np.logical_and(T_, N_))
        P = np.sum(P_)
        N = np.sum(N_)
        F = np.sum(F_)
        T = np.sum(T_)

        return {
            'TP': TP,
            'FP': FP,
            'FN': FN,
            'RECALL': TP / P,
            'TPR': TP / P,
            'TNR': TN / N,
            'PRECISION': TP / (TP + FN),
            'PPV': TP / (TP + FN),
            'ACC': T / (P + N),
            'ACCURACY': T / (P + N),
        }[score.upper()]


all_tag_measurements = pd.read_pickle(r'tag_measurements_2020_03_28.pkl')
all_tag_measurements = all_tag_measurements.dropna(how='any').reset_index(drop=True)
score_obj = ScoreClass(all_tag_measurements, 60)
score_obj.set_func('mean')
score_obj.set_distance_th(3)
score_obj.set_data_th(-80)
print(score_obj.scores('TP'))
print(score_obj.scores('FP'))
print(score_obj.scores('FN'))
print(score_obj.scores('RECALL'))

pass