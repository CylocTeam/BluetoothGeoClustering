import numpy as np
import pandas as pd


class DataFuncs:
    def __init__(self):
        self.percent = 90
        self.margin = 0
        self.df_rolling = None

    def create_rolling_df_in_time(self, df):
        df_index = df.copy()
        df_index.index = df_index.time
        df_index = df_index.sort_index()
        return df_index

    def set_percent(self, percent):
        self.percent = percent

    def set_margin(self, margin):
        self.margin = margin

    def percent_above_percentile(self, series):
        percentile_number = np.percentile(series, self.percent, interpolation='nearest')
        return np.sum(series >= (percentile_number - self.margin)) / series.shape[0]

    def percent_above_percentile_counts(self, series):
        percentile_number = np.percentile(series, self.percent, interpolation='nearest')
        return np.sum(series >= (percentile_number - self.margin))

    def switcher(self, df, func, column_name, win_size):
        return {
            'mean': df[column_name].rolling(win_size, min_periods=1).mean(),
            'var': df[column_name].rolling(win_size, min_periods=1).var(),
            'sum': df[column_name].rolling(win_size, min_periods=1).sum(),
            'min': df[column_name].rolling(win_size, min_periods=1).min(),
            'max': df[column_name].rolling(win_size, min_periods=1).max(),
            'median': df[column_name].rolling(win_size, min_periods=1).median(),
            'count': df[column_name].rolling(win_size, min_periods=1).count(),
            'percentile': df[column_name].rolling(win_size, min_periods=1).apply(
                lambda x: np.percentile(x, self.percent, interpolation='nearest')),
            'above_percentile': df[column_name].rolling(win_size, min_periods=1).apply(
                lambda x: self.percent_above_percentile(x)),
            'above_percentile_counts': df[column_name].rolling(win_size, min_periods=1).apply(
                lambda x: self.percent_above_percentile_counts(x)),
        }[func]

    def exclude_display_name_from_df(self, df, exclude_name):
        df_exclude = df[df.DisplayName != exclude_name]
        return df_exclude

    def apply_and_add_rolling_func_to_df(self, df, func, column_name, win_size_seconds):
        # """
        # Inputs:
        #         df - DataFrame time indexed
        #         func - str of the wanted applying function ('min', 'max', 'sum','count','mean','median','var')
        #             (can add any of pandas.core.window.rolling.Rolling functions)
        #         column_name - str of the wanted column name to apply the function
        #         win_size_seconds - int of window size in seconds
        # """

        df = self.create_rolling_df_in_time(df)
        win_size = str(win_size_seconds) + 's'
        column_func_name = func + '_' + column_name
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
        # needed to group by distance and display name so the results from one distance influence other distance
        df_grouped = df.groupby([column_name_group_first, column_name_group_second])
        df_rolling = df_grouped.apply(lambda x:
                                      self.apply_and_add_rolling_func_to_df(x, func, column_name_func,
                                                                            win_size_seconds))
        return df_rolling

    def normalize_by_distance_single_displayname(self, df, norm_distance, setup=None):
        """
        Inputs:
                setup - the wanted setup for normalization
                        setup = None for all setups
        """
        unique_distances = pd.unique(df.distance)
        if len(np.where(unique_distances == norm_distance)[0]) == 0:
            norm_distance_old = norm_distance
            norm_distance = unique_distances[np.argmin(np.abs(unique_distances - norm_distance))]
            print(df.DisplayName.iloc[0] + ':There is no ' + str(norm_distance_old) +
                  'm distance, Therefore we use ' + str(norm_distance) + 'm to normalize')
        if setup is None:
            df_distance = df.where(df.distance == norm_distance)
            df_distance = df_distance.dropna(how='any').reset_index(drop=True)
        else:
            df_distance = df.where((df.distance == norm_distance) & (df.setup == setup))
            df_distance = df_distance.dropna(how='any').reset_index(drop=True)
        normalized = np.mean(df_distance.rssi)
        df_normalized = df.copy()
        df_normalized.rssi = df_normalized.rssi - normalized
        return df_normalized

    def normalize_by_distance(self, df, norm_distance, setup=None):
        df_grouped = df.groupby(['DisplayName'])
        df_normalized = df_grouped.apply(lambda x:
                                         self.normalize_by_distance_single_displayname(x, norm_distance, setup))
        df_normalized.index = df_normalized.index.droplevel(0)

        return df_normalized
