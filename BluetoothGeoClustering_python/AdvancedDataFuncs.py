import pandas as pd
import numpy as np


class AdvancedDataFuncs:
    def __init__(self, window_sec, df, func='mean', func_column='rssi', receiver_column='edgenodeid', scanned_column = 'beaconid'):
        self.window = window_sec
        self.df = df
        self.receiver_column = receiver_column
        self.func = func
        self.func_column = func_column
        self.percent = 90
        self.scanned_column = scanned_column

    def set_func(self, func):
        self.func = func

    def set_func_column(self, func_column):
        self.func_column = func_column

    def set_percentile(self, percent):
        self.percent = percent

    def set_scanned_column(self, scanned_column):
        self.scanned_column = scanned_column

    def apply_func(self, df):
        if self.func == 'mean':
            return np.mean(df[self.func_column])
        if self.func == 'median':
            return np.median(df[self.func_column])
        if self.func == 'min':
            return np.min(df[self.func_column])
        if self.func == 'max':
            return np.max(df[self.func_column])
        if self.func == 'percentile':
            return np.percentile(df[self.func_column], self.percent, interpolation='nearest')
        if self.func == 'counts':
            return df[self.func_column].shape[0]

    def get_union_vecs(self, df):
        df_grouped = df.groupby(self.receiver_column)
        unique_scans = pd.unique(df[self.scanned_column])
        df_grouped.apply(lambda x: self.apply_func_on_unique(x, unique_scans))

    def apply_func_on_unique(self, df, unique_scans):
        """
        apply_func_on_unique returns df_scans
        Input:
        Output:
            df_scans : dataframe that contains 3 columns:
                scan_device_name, reciver_name, results of the wanted func.
                df_scans size len(unique_scans)x3
        """
        df_scans = pd.DataFrame([])
        df_scans[self.scanned_column] = unique_scans
        df_scans[self.receiver_column] = df[self.receiver_column][0]
        df_grouped = df.groupby(self.scanned_column)
        func_result = df_grouped.apply(lambda x: self.apply_func(x))

        return df_scans

    def run_funcs(self):
        df_index = self.df.copy()
        df_index.index = df_index.time
        df_index = df_index.sort_index()
        self.df = df_index
        win_size = str(self.window) + 's'
        df_vec = self.df.rolling(win_size, min_periods=1).apply(
            lambda x: self.get_union_vecs(x))


DB_pickle = r'useful_dbs/BBIL/tag_measurements_BBIL_all.pkl'
all_tag_measurements = pd.read_pickle(DB_pickle)
pass
