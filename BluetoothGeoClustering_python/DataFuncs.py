import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns


class DataFuncs:
    def create_rolling_df_in_time(self, df):
        df_index = df.copy()
        df_index.index = df_index.time
        df_index = df_index.sort_index()
        return df_index

    def switcher(self, df, func, column_name, win_size, percent=90):
        return {
            'mean': df[column_name].rolling(win_size, min_periods=1).mean(),
            'var': df[column_name].rolling(win_size, min_periods=1).var(),
            'sum': df[column_name].rolling(win_size, min_periods=1).sum(),
            'min': df[column_name].rolling(win_size, min_periods=1).min(),
            'max': df[column_name].rolling(win_size, min_periods=1).max(),
            'median': df[column_name].rolling(win_size, min_periods=1).median(),
            'count': df[column_name].rolling(win_size, min_periods=1).count(),
            'percentile': df[column_name].rolling(win_size, min_periods=1).apply(
                lambda x: np.percentile(x, percent, interpolation='nearest')),
        }[func]

    def apply_and_add_rolling_func_to_df(self, df, func, column_name, win_size_seconds):
        # """
        # Inputs:
        #         df - DataFrame time indexed
        #         func - str of the wanted applying function ('min', 'max', 'sum','count','mean','median','var')
        #             (can add any of pandas.core.window.rolling.Rolling functions)
        #         column_name - str of the wanted column name to apply the function
        #         win_size_seconds - int of window size in seconds
        # """

        win_size = str(win_size_seconds) + 's'
        column_func_name = func + '_' + column_name
        df = self.create_rolling_df_in_time(df)
        x = self.switcher(df, func, column_name, win_size)
        df[column_func_name] = x
        return df

    def run_rolling_func_df(self, df, func, column_name_group, column_name_func, win_size_seconds):
        df_grouped = df.groupby(column_name_group)
        df_rolling = df_grouped.apply(lambda x:
                                      self.apply_and_add_rolling_func_to_df(x, func, column_name_func,
                                                                            win_size_seconds))
        return df_rolling

    def run_rolling_func_df_2_columns(self, df, func, column_name_group_first, column_name_group_second,
                                      column_name_func, win_size_seconds):
        df_grouped = df.groupby([column_name_group_first, column_name_group_second])
        df_rolling = df_grouped.apply(lambda x:
                                      self.apply_and_add_rolling_func_to_df(x, func, column_name_func,
                                                                            win_size_seconds))
        return df_rolling


DataFuncsObj = DataFuncs()
all_tag_measurements = pd.read_pickle(r'tag_measurements_2020_03_28.pkl')
all_tag_measurements = all_tag_measurements.dropna(how='any').reset_index(drop=True)
all_tag_rolling = DataFuncsObj.run_rolling_func_df_2_columns(all_tag_measurements, 'mean', 'DisplayName','distance', 'rssi', 10)
# all_tag_rolling = DataFuncsObj.run_rolling_func_df(all_tag_measurements, 'mean', 'DisplayName', 'rssi', 10)
