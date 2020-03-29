import numpy as np
import pandas as pd
from DataFuncs import DataFuncs


class ScoreClass:
    def __init__(self, tag_data, win_size_seconds):
        self.tag_data = tag_data
        self.win_size_second = win_size_seconds
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
        P = (condition_distance == 1)  # positive
        # condition positive (P) the number of real positive cases in the data
        T = (condition_data == condition_distance)  # true
        N = (condition_distance == 0)  # negative
        # N the number of real negative cases in the data
        F = np.logical_not(T)  # false

        TP = np.logical_and(T, P)
        FP = np.logical_and(F, P)
        FN = np.logical_and(F, N)
        TN = np.logical_and(T, N)

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
