import numpy as np
import pandas as pd


class DataFuncs:
    def __init__(self):
        self.percent = 90
        self.margin = 0
        self.df_rolling = None
        self.top_percent = 80
        self.bottom_percent = 20

    def create_rolling_df_in_time(self, df):
        df_index = df.copy()
        df_index.index = df_index.time
        df_index = df_index.sort_index()
        return df_index

    def set_percent(self, percent):
        self.percent = percent

    def set_margin(self, margin):
        self.margin = margin

    def set_top_percent(self, top_percent):
        self.top_percent = top_percent

    def set_bottom_percent(self, bottom_percent):
        self.bottom_percent = bottom_percent

    def percent_above_percentile(self, series):
        percentile_number = np.percentile(series, self.percent, interpolation='nearest')
        return np.sum(series >= (percentile_number - self.margin)) / series.shape[0]

    def different_between_percentiles(self, series):
        top_percentile = np.percentile(series, self.top_percent, interpolation='nearest')
        bottom_percentile = np.percentile(series, self.bottom_percent, interpolation='nearest')

        return top_percentile - bottom_percentile

    def percent_above_percentile_counts(self, series):
        percentile_number = np.percentile(series, self.percent, interpolation='nearest')
        return np.sum(series >= (percentile_number - self.margin))

    def switcher(self, df, func, column_name, win_size):
            if func == 'mean':
                return df[column_name].rolling(win_size, min_periods=1).mean()
            if func =='var':
                return df[column_name].rolling(win_size, min_periods=1).var()
            if func =='sum':
                return df[column_name].rolling(win_size, min_periods=1).sum()
            if func =='min':
                return df[column_name].rolling(win_size, min_periods=1).min()
            if func =='max':
                return df[column_name].rolling(win_size, min_periods=1).max()
            if func =='median':
                return df[column_name].rolling(win_size, min_periods=1).median()
            if func =='count':
                return df[column_name].rolling(win_size, min_periods=1).count()
            if func =='percentile':
                return df[column_name].rolling(win_size, min_periods=1).apply(
                    lambda x: np.percentile(x, self.percent, interpolation='nearest'))
            if func =='above_percentile':
                return df[column_name].rolling(win_size, min_periods=1).apply(
                    lambda x: self.percent_above_percentile(x))
            if func =='above_percentile_counts':
                return df[column_name].rolling(win_size, min_periods=1).apply(
                    lambda x: self.percent_above_percentile_counts(x))
            if func =='different_between_percentiles':
                return df[column_name].rolling(win_size, min_periods=1).apply(
                    lambda x: self.different_between_percentiles(x))
            if func =='distance':
                return df['distance']


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

    def normalize_by_distance_single_displayname(self, df, norm_distance, setup=None, remove_unfit_data=False, res=0.5):
        """
        Inputs:
                setup - the wanted setup for normalization
                        setup = None for all setups
        """
        unique_distances = pd.unique(df.distance)
        norm_distance_old = norm_distance
        if len(np.where(unique_distances == norm_distance)[0]) == 0:
            norm_distance = unique_distances[np.argmin(np.abs(unique_distances - norm_distance))]
            if ((norm_distance - norm_distance_old) <= res) or (not remove_unfit_data):
                print('#C: ' + df.DisplayName.iloc[0] + ':There is no ' + str(norm_distance_old) +
                      'm distance, Therefore we use ' + str(norm_distance) + 'm to normalize')
        if ((norm_distance - norm_distance_old) > res) and (remove_unfit_data):
            df_normalized = df.copy()
            df_normalized.rssi = np.nan
            print('#R: ' + df.DisplayName.iloc[0] + ':There is no ' + str(norm_distance_old) +
                  'm distance, Therefore we remove the device from data')
        else:
            if setup is None:
                df_distance = df.where(df.distance == norm_distance)
                df_distance = df_distance.dropna(how='any').reset_index(drop=True)
            else:
                df_distance = df.where((df.distance == norm_distance) & (df.setup == setup))
                df_distance = df_distance.dropna(how='any').reset_index(drop=True)
            normalized = np.median(df_distance.rssi)
            df_normalized = df.copy()
            df_normalized.rssi = df_normalized.rssi - normalized
        return df_normalized

    def normalize_by_distance(self, df, norm_distance, setup=None, remove_unfit_data=False, res=0.5):
        df_grouped = df.groupby(['DisplayName'])
        df_normalized = df_grouped.apply(lambda x:
                                         self.normalize_by_distance_single_displayname(x, norm_distance, setup,
                                                                                       remove_unfit_data, res))
        try:
            df_normalized.index = df_normalized.index.droplevel(0)
        except Exception as c:
            print('index ok')

        df_normalized = df_normalized.dropna(how='any').reset_index(drop=True)

        return df_normalized

#
# DataFuncsObj = DataFuncs()
# DB_pickle = r'useful_dbs/BBIL/tag_measurements_BBIL_all.pkl'
# all_tag_measurements = pd.read_pickle(DB_pickle)
# rolling_by_2 = 0
# setup = 'Phone in hand'
# plot_tag_data = DataFuncsObj.normalize_by_distance(all_tag_measurements, 1, setup, True, 0.25)
# distances = DataFuncsObj.run_rolling_func_df(plot_tag_data, 'distance', 'DisplayName', 'rssi', 20)
