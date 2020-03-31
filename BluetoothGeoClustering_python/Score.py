import numpy as np
import pandas as pd
from DataFuncs import DataFuncs


class ScoreClass:
    def __init__(self, tag_data, win_size_seconds, func=None, distance_th=None, data_th=None, percent=90, margin=0):
        self.tag_data = tag_data
        self.win_size_seconds = win_size_seconds
        self.func = func
        self.column_name = func + '_' + 'rssi'
        self.distance_th = distance_th
        self.data_th = data_th
        self.reset_scores = 1
        self.DataFuncsObj = DataFuncs()
        self.DataFuncsObj.set_percent(percent)
        self.DataFuncsObj.set_margin(margin)

    def set_func(self, func):
        self.func = func
        self.column_name = func + '_' + 'rssi'
        self.reset_scores = 1

    def set_distance_th(self, distance_m):
        self.distance_th = distance_m
        self.reset_scores = 1

    def set_data_th(self, th):
        self.data_th = th
        self.reset_scores = 1

    def calc_T_F_P_N(self):
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

        result = self.DataFuncsObj.run_rolling_func_df_2_columns(self.tag_data, self.func, 'DisplayName', 'distance',
                                                                 'rssi', self.win_size_seconds)
        condition_data = result[self.column_name] >= self.data_th
        condition_distance = result['distance'] <= self.distance_th
        self.P_vec = (condition_distance == 1)  # positive
        # condition positive (P) the number of real positive cases in the data
        self.T_vec = (condition_data == condition_distance)  # true
        self.N_vec = (condition_distance == 0)  # negative
        # N the number of real negative cases in the data
        self.F_vec = np.logical_not(self.T_vec)  # false

        self.reset_scores = 0

    def scores(self, score):
        if self.reset_scores:
            self.calc_T_F_P_N()

        TP = np.sum(np.logical_and(self.T_vec, self.P_vec))
        FP = np.sum(np.logical_and(self.F_vec, self.P_vec))
        FN = np.sum(np.logical_and(self.F_vec, self.N_vec))
        TN = np.sum(np.logical_and(self.T_vec, self.N_vec))
        P = np.sum(self.P_vec)
        N = np.sum(self.N_vec)
        F = np.sum(self.F_vec)
        T = np.sum(self.T_vec)

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
            'MD': FP,
            'FA': FN,
        }[score.upper()]

    def get_all_scores(self):
        if self.reset_scores:
            self.calc_T_F_P_N()

        TP = np.sum(np.logical_and(self.T_vec, self.P_vec))
        FP = np.sum(np.logical_and(self.F_vec, self.P_vec))
        FN = np.sum(np.logical_and(self.F_vec, self.N_vec))
        TN = np.sum(np.logical_and(self.T_vec, self.N_vec))
        P = np.sum(self.P_vec)
        N = np.sum(self.N_vec)
        F = np.sum(self.F_vec)
        T = np.sum(self.T_vec)
        all = T+F
        results = pd.DataFrame.from_dict(
         {
            'All': all,
            'TP': TP,
            'MD (FP)': FP,
            'MD/P (FP/P) ': FP/P,
            'FA (FN)': FN,
            'FA/N (FN/N)': FN/N,
            'RECALL (TPR)': TP / P,
            'TNR': TN / N,
            'PRECISION (PPV)': TP / (TP + FN),
            'ACCURACY': T / (P + N),
         })
        return results

# all_tag_measurements = pd.read_pickle(r'tag_measurements_2020_03_28.pkl')
# all_tag_measurements = all_tag_measurements.dropna(how='any').reset_index(drop=True)
# score_obj = ScoreClass(all_tag_measurements, 60, 'mean', 3, -85)
# score_obj.get_all_scores()
